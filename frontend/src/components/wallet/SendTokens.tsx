import React, { useState } from 'react';

interface Token {
  symbol: string;
  balance: string;
}

interface SendTokensProps {
  address: string;
  balance: string;
  tokens: Token[];
}

const SendTokens: React.FC<SendTokensProps> = ({ address, balance, tokens }) => {
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');
  const [selectedToken, setSelectedToken] = useState('ADAC');

  const handleSend = async () => {
    // Implementation here
    console.log('Sending', amount, selectedToken, 'to', recipient);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-bold mb-4">Send Tokens</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recipient Address
            </label>
            <input
              type="text"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="0x..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Amount
            </label>
            <div className="relative">
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full p-2 pr-24 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.0"
              />
              <div className="absolute inset-y-0 right-0 flex items-center">
                <select
                  value={selectedToken}
                  onChange={(e) => setSelectedToken(e.target.value)}
                  className="h-full py-0 pl-2 pr-7 border-transparent bg-transparent text-gray-500 sm:text-sm rounded-md"
                >
                  {tokens.map((token) => (
                    <option key={token.symbol} value={token.symbol}>
                      {token.symbol}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <button
            onClick={handleSend}
            className="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
          >
            Send Tokens
          </button>
        </div>
      </div>
    </div>
  );
};

export default SendTokens;
