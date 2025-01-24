import React, { useState } from 'react';

interface TokenSwapProps {
  address: string;
  balance: string;
}

const TokenSwap: React.FC<TokenSwapProps> = ({ address, balance }) => {
  const [fromAmount, setFromAmount] = useState('');
  const [toAmount, setToAmount] = useState('');

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-bold mb-4">Swap Tokens</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              From
            </label>
            <div className="relative">
              <input
                type="number"
                value={fromAmount}
                onChange={(e) => setFromAmount(e.target.value)}
                className="w-full p-2 pr-16 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.0"
                max={parseFloat(balance)}
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <span className="text-gray-500">ADAC</span>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              To
            </label>
            <div className="relative">
              <input
                type="number"
                value={toAmount}
                onChange={(e) => setToAmount(e.target.value)}
                className="w-full p-2 pr-16 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.0"
                readOnly
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <span className="text-gray-500">ETH</span>
              </div>
            </div>
          </div>

          <button 
            className="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
          >
            Swap Tokens
          </button>
        </div>
      </div>
    </div>
  );
};

export default TokenSwap;
