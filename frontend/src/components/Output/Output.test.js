import React from 'react';
import { render, screen } from '@testing-library/react';
import Output from './Output';


describe('<Output />', () => {
  test('it should mount', () => {
    render(<Output />);

    expect(screen.getByTestId('Output')).toBeInTheDocument();
  });

  test('it should display data when there is data', () => {
    let data = [{'category': "One", 'content': ["one", "three"]}, {'category': "Two", 'content': ["two", "three"]}]
    render(<Output data={data} />);
    
    expect(screen.getAllByTestId("OutputData").length).toEqual(2)
  });

  test('it should not display when there is no data', () => {
    render(<Output />);
    
    expect(screen.queryAllByTestId("OutputData").length).toEqual(0);
  });

  test('it should display an error when there is an error', () => {
    render(<Output error={true}/>);
    
    expect(screen.getByTestId("OutputError")).toBeInTheDocument();
  });
});