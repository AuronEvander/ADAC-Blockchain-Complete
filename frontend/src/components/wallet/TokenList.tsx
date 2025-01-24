import React, { useState } from 'react';
import { 
  PlusCircle,
  Search,
  X,
  AlertCircle,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import Web3 from 'web3';

interface TokenListProps {
  tokens: Token[];
  onAddToken: (token: Token) => void;
}

interface Token {
  symbol: string;
  name: string;
  address: string;
  balance: string;
  decimals: number;
  price: number;
  priceChange24h: number;
}

interface AddTokenForm {
  address: string;
  symbol: string;
  decimals: number;
  name: string;
}

const TokenList: React.FC<TokenListProps> = ({ tokens, onAddToken }) => {
  const [showAddToken, setShowAddToken] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedToken, setExpandedToken] = useState<string | null>(null);
  const [addTokenForm, setAddTokenForm] = useState<AddTokenForm>({
    address: '',
    symbol: '',
    decimals: 18,
    name: ''
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAddToken = async () => {
    try {
      setLoading(true);
      setError(null);

      // Validate token address
      if (!Web3.utils.isAddress(addTokenForm.address)) {
        throw new Error('Invalid token address');
      }

      // This would be replaced with actual contract call to get token info
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Mock token verification and addition
      const newToken: Token = {
        ...addTokenForm,
        balance: '0',
        price: 0,
        priceChange24h: 0
      };

      onAddToken(newToken);
      setShowAddToken(false);
      setAddTokenForm({
        address: '',
        symbol: '',
        decimals: 18,
        name: ''
      });
    } catch (err) {
      console.error('Error adding token:', err);
      setError(err instanceof Error ? err.message : 'Failed to add token');
    } finally {
      setLoading(false);
    }
  };

  const filteredTokens = tokens.filter(token => 
    token.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    token.symbol.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatBalance = (balance: string) => {
    const num = parseFloat(balance);
    if (num > 1000000) return (num / 1000000).toFixed(2) + 'M';
    if (num > 1000) return (num / 1000).toFixed(2) + 'K';
    return num.toFixed(4);
  };

  return (
    <div className="space-y-4">
      {/* Search and Add Token Header */}
      <div className="flex items-center justify-between">
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search tokens"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          onClick={() => setShowAddToken(true)}
          className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:text-blue-700"
        >
          <PlusCircle className="h-5 w-5" />
          <span>Add Token</span>
        </button>
      </div>

      {/* Token List */}
      <div className="space-y-2">
        {filteredTokens.map(token => (
          <div key={token.address} className="bg-white rounded-lg shadow">
            <div
              className="p-4 cursor-pointer hover:bg-gray-50"
              onClick={() => setExpandedToken(
                expandedToken === token.address ? null : token.address
              )}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium">{token.symbol}</h3>
                  <p className="text-sm text-gray-600">{token.name}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">
                    {formatBalance(token.balance)} {token.symbol}
                  </p>
                  <p className="text-sm text-gray-600">
                    ${(parseFloat(token.balance) * token.price).toFixed(2)}
                  </p>
                </div>
              </div>

              {expandedToken === token.address && (
                <div className="mt-4 pt-4 border-t">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Price</span>
                      <div className="flex items-center space-x-2">
                        <span>${token.price.toFixed(4)}</span>
                        <span className={`flex items-center ${
                          token.priceChange24h >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {token.priceChange24h >= 0 ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                          {Math.abs(token.priceChange24h).toFixed(2)}%
                        </span>
                      </div>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Contract Address</span>
                      <span className="font-mono">{token.address.slice(0, 6)}...{token.address.slice(-4)}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Add Token Modal */}
      {showAddToken && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium">Add Custom Token</h3>
              <button
                onClick={() => setShowAddToken(false)}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded flex items-center space-x-2">
                <AlertCircle className="h-5 w-5" />
                <span>{error}</span>
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Token Contract Address
                </label>
                <input
                  type="text"
                  value={addTokenForm.address}
                  onChange={(e) => setAddTokenForm(prev => ({
                    ...prev,
                    address: e.target.value
                  }))}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="0x..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Token Symbol
                </label>
                <input
                  type="text"
                  value={addTokenForm.symbol}
                  onChange={(e) => setAddTokenForm(prev => ({
                    ...prev,
                    symbol: e.target.value.toUpperCase()
                  }))}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="TOKEN"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Token Name
                </label>
                <input
                  type="text"
                  value={addTokenForm.name}
                  onChange={(e) => setAddTokenForm(prev => ({
                    ...prev,
                    name: e.target.value
                  }))}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="My Token"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Decimals
                </label>
                <input
                  type="number"
                  value={addTokenForm.decimals}
                  onChange={(e) => setAddTokenForm(prev => ({
                    ...prev,
                    decimals: parseInt(e.target.value)
                  }))}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="0"
                  max="18"
                />
              </div>

              <button
                onClick={handleAddToken}
                disabled={loading}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
              >
                {loading ? 'Adding Token...' : 'Add Token'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TokenList;