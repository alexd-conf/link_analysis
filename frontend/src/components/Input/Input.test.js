import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import Input from './Input';

describe('<Input />', () => {
  test('it should mount', () => {
    render(<Input />);
    
    expect(screen.getByTestId('Input')).toBeInTheDocument();
  });

  test('it should handleChange upon input', () => {
    let handleChange = jest.spyOn(Input.prototype, "handleChange");
    render(<Input />);

    let element = screen.getByTestId("InputBar");
    fireEvent.change(element, {target: {value: 'test'}});

    expect(handleChange).toHaveBeenCalled();
  });

  test('it should handleSubmit when Analyze button is clicked', () => {
    let handleSubmit = jest.spyOn(Input.prototype, "handleSubmit");
    render(<Input />);

    let element = screen.getByTestId("InputButton");
    fireEvent.click(element);

    expect(handleSubmit).toHaveBeenCalled();
  });
});