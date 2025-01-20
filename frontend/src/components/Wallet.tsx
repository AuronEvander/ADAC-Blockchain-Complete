import React, { useState } from 'react';

interface WalletProps {
  balance: number;
  address: string;
}

const Wallet: React.FC<WalletProps> = ({ balance, address }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-xl font-bold text-blue-400 mb-4">Wallet</h2>
      <div className="space-y-2">
        <p className="text-white">
          <span className="font-semibold">Address:</span>{' '}
          <span className="font-mono text-sm">{address}</span>
        </p>
        <p className="text-white">
          <span className="font-semibold">Balance:</span>{' '}
          <span className="text-green-400">{balance} ADAC</span>
        </p>
      </div>
    </div>
  );
};

export default Wallet;