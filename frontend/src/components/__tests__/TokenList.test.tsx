import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TokenList from '../TokenList';

const mockTokens = [
  {
    symbol: 'ADAC',
    name: 'ADAC Token',
    address: '0x1234567890123456789012345678901234567890',
    balance: '1000.00',
    decimals: 18,
    price: 1.0,
    priceChange24h: 5.2
  },
  {
    symbol: 'ETH',
    name: 'Ethereum',
    address: '0x0987654321098765432109876543210987654321',
    balance: '10.5',
    decimals: 18,
    price: 1800.0,
    priceChange24h: -2.1
  }
];

describe('TokenList', () => {
  const mockOnAddToken = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders list of tokens', () => {
    render(<TokenList tokens={mockTokens} onAddToken={mockOnAddToken} />);
    
    expect(screen.getByText('ADAC')).toBeInTheDocument();
    expect(screen.getByText('Ethereum')).toBeInTheDocument();
    expect(screen.getByText('1000.00 ADAC')).toBeInTheDocument();
    expect(screen.getByText('10.50 ETH')).toBeInTheDocument();
  });

  it('filters tokens based on search query', async () => {
    render(<TokenList tokens={mockTokens} onAddToken={mockOnAddToken} />);
    
    const searchInput = screen.getByPlaceholderText('Search tokens');
    await userEvent.type(searchInput, 'eth');
    
    expect(screen.getByText('ETH')).toBeInTheDocument();
    expect(screen.queryByText('ADAC')).not.toBeInTheDocument();
  });

  it('shows add token modal when clicking add token button', () => {
    render(<TokenList tokens={mockTokens} onAddToken={mockOn