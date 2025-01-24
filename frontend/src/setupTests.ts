import '@testing-library/jest-dom';

// Mock Web3
jest.mock('web3', () => {
  return jest.fn().mockImplementation(() => ({
    eth: {
      getBalance: jest.fn().mockResolvedValue('1000000000000000000'),
      sendTransaction: jest.fn().mockResolvedValue({ transactionHash: '0x123' })
    },
    utils: {
      isAddress: (address: string) => /^0x[a-fA-F0-9]{40}$/.test(address),
      fromWei: (wei: string) => (parseInt(wei) / 1e18).toString(),
      toWei: (eth: string) => (parseFloat(eth) * 1e18).toString()
    }
  }));
});

// Mock window.ethereum
const ethereum = {
  request: jest.fn(),
  on: jest.fn(),
  removeListener: jest.fn(),
  providers: [],
  isMetaMask: true
};

global.window = Object.create(window);
Object.defineProperty(window, 'ethereum', {
  value: ethereum
});

// Reset mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
  ethereum.request.mockReset();
  ethereum.request.mockImplementation((params) => {
    switch (params.method) {
      case 'eth_requestAccounts':
        return Promise.resolve(['0x742d35Cc6634C0532925a3b844Bc454e4438f44e']);
      case 'eth_accounts':
        return Promise.resolve(['0x742d35Cc6634C0532925a3b844Bc454e4438f44e']);
      default:
        return Promise.reject(new Error(`Unhandled method: ${params.method}`));
    }
  });
});