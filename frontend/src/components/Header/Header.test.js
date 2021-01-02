import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('<Header />', () => {
  test('it should mount', () => {
    render(<Header />);
    
    expect(screen.getByTestId("Header")).toBeInTheDocument();
    expect(screen.getByTestId("Title")).toBeInTheDocument();
    expect(screen.getByTestId("Links")).toBeInTheDocument();
    expect(screen.getByTestId("Information")).toBeInTheDocument();
  });
});