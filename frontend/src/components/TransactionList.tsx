import React from 'react';
import { format } from 'date-fns';

interface Transaction {
  id: string;
  hash: string;
  timestamp: Date;
  from: string;
  to: string;
  amount: number;
}

interface TransactionListProps {
  transactions: Transaction[];
}

const TransactionList: React.FC<TransactionListProps> = ({ transactions }) => {
  const formatDate = (date: Date) => {
    return format(new Date(date), 'PP p');
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
      <div className="space-y-4">
        {transactions.map((tx: Transaction) => (
          <div key={tx.id} className="border-b pb-4">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-600">Hash: {tx.hash}</p>
                <p className="text-sm">
                  From: <span className="text-blue-600">{tx.from}</span>
                </p>
                <p className="text-sm">
                  To: <span className="text-blue-600">{tx.to}</span>
                </p>
              </div>
              <div className="text-right">
                <p className="text-lg font-medium">{tx.amount} ADAC</p>
                <p className="text-sm text-gray-500">
                  {formatDate(tx.timestamp)}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TransactionList;