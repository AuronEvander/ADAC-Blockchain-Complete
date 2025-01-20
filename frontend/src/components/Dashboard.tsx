import React, { useState, useEffect } from 'react';
import Wallet from './Wallet';
import TransactionList from './TransactionList';

const Dashboard: React.FC = () => {
  const [walletInfo, setWalletInfo] = useState({
    balance: 0,
    address: '0x0000000000000000000000000000000000000000'
  });

  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Fetch wallet and transaction data
    // This would typically come from your API
    const mockData = {
      balance: 1000,
      address: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    };
    setWalletInfo(mockData);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">ADAC Blockchain Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Wallet balance={walletInfo.balance} address={walletInfo.address} />
        <TransactionList transactions={transactions} />
      </div>
    </div>
  );
};

export default Dashboard;