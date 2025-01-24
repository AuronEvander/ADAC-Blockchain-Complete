import React, { useState } from 'react';
import { 
  Search,
  ExternalLink, 
  Clock,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Filter,
  RefreshCcw
} from 'lucide-react';

interface Transaction {
  hash: string;
  from: string;
  to: string;
  amount: string;
  timestamp: string;
  status: 'Success' | 'Failed' | 'Pending';
  gasUsed: string;
  gasPrice: string;
  blockNumber: number;
}

interface Block {
  number: number;
  hash: string;
  timestamp: string;
  transactions: number;
  miner: string;
  reward: string;
}

const Explorer: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(null);
  const [activeTab, setActiveTab] = useState<'transactions' | 'blocks'>('transactions');
  const [loading, setLoading] = useState(false);

  const mockTransactions: Transaction[] = [
    {
      hash: '0x123...abc',
      from: '0xABC...123',
      to: '0xDEF...456',
      amount: '100 ADAC',
      timestamp: 'Jan 21, 2025, 12:39 AM',
      status: 'Success',
      gasUsed: '21,000',
      gasPrice: '20 Gwei',
      blockNumber: 1234567
    },
    {
      hash: '0x456...def',
      from: '0xGHI...789',
      to: '0xJKL...012',
      amount: '250 ADAC',
      timestamp: 'Jan 21, 2025, 12:34 AM',
      status: 'Pending',
      gasUsed: '21,000',
      gasPrice: '25 Gwei',
      blockNumber: 1234566
    }
  ];

  const mockBlocks: Block[] = [
    {
      number: 1234567,
      hash: '0xabc...123',
      timestamp: 'Jan 21, 2025, 12:39 AM',
      transactions: 150,
      miner: '0xMiner...789',
      reward: '2 ADAC'
    },
    {
      number: 1234566,
      hash: '0xdef...456',
      timestamp: 'Jan 21, 2025, 12:38 AM',
      transactions: 120,
      miner: '0xMiner...012',
      reward: '2 ADAC'
    }
  ];

  const handleSearch = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1000);
  };

  const handleRefresh = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1000);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Blockchain Explorer</h1>
        <button
          onClick={handleRefresh}
          className="p-2 hover:bg-gray-100 rounded-lg"
        >
          <RefreshCcw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Search by Transaction Hash / Block Number / Address"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="w-full p-4 pl-12 pr-4 bg-white border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Search className="w-5 h-5 text-gray-400 absolute left-4 top-4" />
        </div>
      </div>

      <div className="flex items-center space-x-1 mb-6 border-b">
        <button
          onClick={() => setActiveTab('transactions')}
          className={`px-4 py-2 font-medium ${
            activeTab === 'transactions'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Transactions
        </button>
        <button
          onClick={() => setActiveTab('blocks')}
          className={`px-4 py-2 font-medium ${
            activeTab === 'blocks'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Blocks
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm">
            {activeTab === 'transactions' ? (
              <>
                <div className="p-6 border-b flex justify-between items-center">
                  <h2 className="text-xl font-bold">Recent Transactions</h2>
                  <button className="p-2 hover:bg-gray-100 rounded-lg">
                    <Filter className="w-5 h-5" />
                  </button>
                </div>
                <div className="divide-y">
                  {mockTransactions.map((tx) => (
                    <div 
                      key={tx.hash}
                      className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
                      onClick={() => setSelectedTx(tx)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {tx.status === 'Success' ? (
                            <CheckCircle2 className="w-5 h-5 text-green-500" />
                          ) : tx.status === 'Pending' ? (
                            <Clock className="w-5 h-5 text-yellow-500" />
                          ) : (
                            <AlertTriangle className="w-5 h-5 text-red-500" />
                          )}
                          <span className={`text-sm font-medium ${
                            tx.status === 'Success' ? 'text-green-700' :
                            tx.status === 'Pending' ? 'text-yellow-700' :
                            'text-red-700'
                          }`}>
                            {tx.status}
                          </span>
                        </div>
                        <span className="text-sm text-gray-500">{tx.timestamp}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-mono text-sm text-gray-500">Tx: {tx.hash}</p>
                          <div className="flex items-center mt-1 space-x-2">
                            <p className="font-mono text-sm text-gray-600">From: {tx.from}</p>
                            <ArrowRight className="w-4 h-4 text-gray-400" />
                            <p className="font-mono text-sm text-gray-600">To: {tx.to}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-medium">{tx.amount}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <>
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold">Recent Blocks</h2>
                </div>
                <div className="divide-y">
                  {mockBlocks.map((block) => (
                    <div 
                      key={block.number}
                      className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-medium mb-1">Block #{block.number}</h3>
                          <p className="font-mono text-sm text-gray-500">{block.hash}</p>
                          <div className="mt-2 text-sm text-gray-600">
                            <p>Miner: {block.miner}</p>
                            <p>{block.transactions} transactions</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-500">{block.timestamp}</p>
                          <p className="font-medium mt-1">Reward: {block.reward}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>

        <div className="lg:col-span-1">
          {selectedTx ? (
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-bold mb-6">Transaction Details</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Transaction Hash</p>
                  <p className="font-mono break-all">{selectedTx.hash}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Status</p>
                  <div className="flex items-center">
                    {selectedTx.status === 'Success' ? (
                      <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" />
                    ) : selectedTx.status === 'Pending' ? (
                      <Clock className="w-5 h-5 text-yellow-500 mr-2" />
                    ) : (
                      <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
                    )}
                    <span className={`font-medium ${
                      selectedTx.status === 'Success' ? 'text-green-700' :
                      selectedTx.status === 'Pending' ? 'text-yellow-700' :
                      'text-red-700'
                    }`}>
                      {selectedTx.status}
                    </span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Block</p>
                  <p className="font-medium">{selectedTx.blockNumber.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">From</p>
                  <p className="font-mono break-all">{selectedTx.from}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">To</p>
                  <p className="font-mono break-all">{selectedTx.to}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Value</p>
                  <p className="font-medium">{selectedTx.amount}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Gas Used</p>
                  <p className="font-medium">{selectedTx.gasUsed}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Gas Price</p>
                  <p className="font-medium">{selectedTx.gasPrice}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Timestamp</p>
                  <p className="font-medium">{selectedTx.timestamp}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <p className="text-gray-500">Select a transaction to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Explorer;
