import React from 'react';
import { 
 Boxes, 
 Users,
 History,
 Clock,
 LockIcon,
 TrendingUp,
 AlertTriangle,
 CheckCircle2,
 ExternalLink 
} from 'lucide-react';

interface DashboardProps {
 address: string;
 balance: string;
}

interface NetworkStats {
 totalBlocks: number;
 activeValidators: number;
 transactions: number;
 blockTime: string;
 stakingRatio: string;
}

interface RecentTransaction {
 hash: string;
 from: string;
 to: string;
 amount: string;
 timestamp: string;
}

const Dashboard: React.FC<DashboardProps> = () => {
 const networkStats: NetworkStats = {
   totalBlocks: 1234567,
   activeValidators: 100,
   transactions: 987654,
   blockTime: '2.5s',
   stakingRatio: '65.0%'
 };

 const recentTransactions: RecentTransaction[] = [
   {
     hash: '0x123...abc',
     from: '0xABC...123',
     to: '0xDEF...456',
     amount: '100',
     timestamp: 'Jan 21, 2025, 12:39 AM'
   },
   {
     hash: '0x456...def',
     from: '0xGHI...789',
     to: '0xJKL...012',
     amount: '250',
     timestamp: 'Jan 21, 2025, 12:34 AM'
   }
 ];

 const networkHealth = {
   status: 'Healthy',
   currentTPS: '45.2',
   nodeVersion: '1.0.0'
 };

 return (
   <div className="container mx-auto px-4 py-8">
     <div className="mb-8">
       <h1 className="text-3xl font-bold mb-2">Network Overview</h1>
       <p className="text-gray-600">Real-time blockchain statistics and recent activity</p>
     </div>

     {/* Stats Grid */}
     <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
       <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex items-center justify-between">
           <div>
             <p className="text-gray-600">Total Blocks</p>
             <h3 className="text-2xl font-bold mt-1">{networkStats.totalBlocks.toLocaleString()}</h3>
           </div>
           <Boxes className="w-10 h-10 text-blue-500" />
         </div>
       </div>

       <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex items-center justify-between">
           <div>
             <p className="text-gray-600">Active Validators</p>
             <h3 className="text-2xl font-bold mt-1">{networkStats.activeValidators}</h3>
           </div>
           <Users className="w-10 h-10 text-green-500" />
         </div>
       </div>

       <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex items-center justify-between">
           <div>
             <p className="text-gray-600">Transactions</p>
             <h3 className="text-2xl font-bold mt-1">{networkStats.transactions.toLocaleString()}</h3>
           </div>
           <History className="w-10 h-10 text-purple-500" />
         </div>
       </div>
     </div>

     {/* Secondary Stats */}
     <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
       <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex items-center justify-between">
           <div>
             <p className="text-gray-600">Block Time</p>
             <h3 className="text-2xl font-bold mt-1">{networkStats.blockTime}</h3>
           </div>
           <Clock className="w-10 h-10 text-orange-500" />
         </div>
       </div>

       <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex items-center justify-between">
           <div>
             <p className="text-gray-600">Staking Ratio</p>
             <h3 className="text-2xl font-bold mt-1">{networkStats.stakingRatio}</h3>
           </div>
           <LockIcon className="w-10 h-10 text-red-500" />
         </div>
       </div>
     </div>

     {/* Recent Transactions */}
     <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
       <div className="bg-white rounded-xl shadow-sm p-6">
         <h2 className="text-xl font-bold mb-4">Recent Transactions</h2>
         <div className="space-y-4">
           {recentTransactions.map((tx) => (
             <div key={tx.hash} className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg">
               <div className="flex items-center space-x-3">
                 <CheckCircle2 className="w-5 h-5 text-green-500" />
                 <div>
                   <p className="font-medium">{tx.amount} ADAC</p>
                   <p className="text-sm text-gray-500">{tx.timestamp}</p>
                 </div>
               </div>
               <a 
                 href={`https://explorer.adac.network/tx/${tx.hash}`}
                 target="_blank"
                 rel="noopener noreferrer"
                 className="text-blue-500 hover:text-blue-700"
               >
                 <ExternalLink className="w-4 h-4" />
               </a>
             </div>
           ))}
         </div>
       </div>

       {/* Network Health */}
       <div className="bg-white rounded-xl shadow-sm p-6">
         <h2 className="text-xl font-bold mb-4">Network Health</h2>
         <div className="space-y-4">
           <div className="p-4 bg-gray-50 rounded-lg">
             <div className="flex items-center justify-between">
               <p className="text-gray-600">Network Status</p>
               <div className="flex items-center">
                 <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                 <p className="font-medium text-green-700">{networkHealth.status}</p>
               </div>
             </div>
           </div>

           <div className="p-4 bg-gray-50 rounded-lg">
             <div className="flex items-center justify-between">
               <p className="text-gray-600">Current TPS</p>
               <div className="flex items-center">
                 <TrendingUp className="w-4 h-4 text-blue-500 mr-2" />
                 <p className="font-medium">{networkHealth.currentTPS}</p>
               </div>
             </div>
           </div>

           <div className="p-4 bg-gray-50 rounded-lg">
             <div className="flex items-center justify-between">
               <p className="text-gray-600">Node Version</p>
               <p className="font-medium">{networkHealth.nodeVersion}</p>
             </div>
           </div>
         </div>
       </div>
     </div>
   </div>
 );
};

export default Dashboard;
