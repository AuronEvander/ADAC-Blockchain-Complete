import React, { useState, useEffect } from 'react';
import Wallet from './Wallet';
import TransactionList from './TransactionList';

const Dashboard: React.FC = () => {
  const [walletAddress, setWalletAddress] = useState<string>('');
  const [transactions, setTransactions] = useState([]);

  const handleWalletConnect = (address: string) => {
    setWalletAddress(address);
    // Fetch transactions for this address
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-1">
          <Wallet onConnect={handleWalletConnect} />
        </div>
        <div className="col-span-2">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
            <TransactionList transactions={transactions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;