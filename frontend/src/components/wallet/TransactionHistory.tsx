import React, { useState, useMemo } from 'react';
import { formatDistance } from 'date-fns';

export interface Transaction {
 id: string;
 type: string;
 amount: string;
 status: string;
 timestamp: Date;
}

export interface Token {
 symbol: string;
 balance: string;
}

interface TransactionHistoryProps {
 transactions: Transaction[];
 tokens: Token[];
}

interface SortConfig {
 key: keyof Transaction;
 direction: 'asc' | 'desc';
}

const TransactionHistory: React.FC<TransactionHistoryProps> = ({ transactions, tokens }) => {
 const [sortConfig, setSortConfig] = useState<SortConfig>({ key: 'timestamp', direction: 'desc' });
 const [searchTerm, setSearchTerm] = useState('');

 const filtered = useMemo(() => {
   return transactions.filter(tx => 
     tx.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
     tx.amount.toLowerCase().includes(searchTerm.toLowerCase()) ||
     tx.status.toLowerCase().includes(searchTerm.toLowerCase())
   );
 }, [transactions, searchTerm]);

 const sortedData = useMemo(() => {
   const sorted = [...filtered];
   if (sortConfig) {
     sorted.sort((a, b) => {
       if (sortConfig.key === 'timestamp') {
         return sortConfig.direction === 'asc' 
           ? a.timestamp.getTime() - b.timestamp.getTime()
           : b.timestamp.getTime() - a.timestamp.getTime();
       }

       const aVal = String(a[sortConfig.key]);
       const bVal = String(b[sortConfig.key]);
       
       if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
       if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
       return 0;
     });
   }
   return sorted;
 }, [filtered, sortConfig]);

 const requestSort = (key: keyof Transaction) => {
   if (sortConfig && sortConfig.key === key) {
     setSortConfig({
       key,
       direction: sortConfig.direction === 'asc' ? 'desc' : 'asc',
     });
   } else {
     setSortConfig({ key, direction: 'asc' });
   }
 };

 return (
   <div>
     <div className="mb-4">
       <input
         type="text"
         placeholder="Search transactions..."
         value={searchTerm}
         onChange={(e) => setSearchTerm(e.target.value)}
         className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
       />
     </div>

     <div className="overflow-x-auto">
       <table className="min-w-full bg-white">
         <thead>
           <tr>
             <th 
               onClick={() => requestSort('type')}
               className="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
             >
               Type
             </th>
             <th 
               onClick={() => requestSort('amount')}
               className="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
             >
               Amount
             </th>
             <th 
               onClick={() => requestSort('status')}
               className="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
             >
               Status
             </th>
             <th 
               onClick={() => requestSort('timestamp')}
               className="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
             >
               Time
             </th>
           </tr>
         </thead>
         <tbody>
           {sortedData.map((tx) => (
             <tr key={tx.id}>
               <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                 <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                   {tx.type}
                 </span>
               </td>
               <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                 {tx.amount} {tokens.find(t => t.symbol === tx.type)?.symbol || 'ADAC'}
               </td>
               <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                 <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                   tx.status === 'Completed' 
                     ? 'bg-green-100 text-green-800'
                     : tx.status === 'Pending'
                     ? 'bg-yellow-100 text-yellow-800' 
                     : 'bg-red-100 text-red-800'
                 }`}>
                   {tx.status}
                 </span>
               </td>
               <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm text-gray-500">
                 {formatDistance(tx.timestamp, new Date(), { addSuffix: true })}
               </td>
             </tr>
           ))}
         </tbody>
       </table>
     </div>
   </div>
 );
};

export default TransactionHistory;
