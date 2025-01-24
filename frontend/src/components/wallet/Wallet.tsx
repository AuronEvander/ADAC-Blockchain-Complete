import React, { useState, useCallback, useEffect } from 'react';
import Web3 from 'web3';
import { 
 Wallet as WalletIcon,
 AlertTriangle,
 Power
} from 'lucide-react';

interface WalletState {
 address: string;
 balance: string;
 connected: boolean;
 network: string;
}

const Wallet: React.FC = () => {
 const [error, setError] = useState<string | null>(null);
 const [loading, setLoading] = useState(false);
 const [walletState, setWalletState] = useState<WalletState>({
   address: '',
   balance: '0',
   connected: false,
   network: ''
 });

 const connectWallet = useCallback(async () => {
   try {
     setError(null);
     setLoading(true);

     if (typeof window.ethereum !== 'undefined') {
       const web3 = new Web3(window.ethereum);
       await window.ethereum.request({ method: 'eth_requestAccounts' });
       const accounts = await web3.eth.getAccounts();
       const networkId = await web3.eth.net.getId();
       const networkName = getNetworkName(networkId);
       
       if (accounts.length > 0) {
         const address = accounts[0];
         const balance = await web3.eth.getBalance(address);
         const etherBalance = web3.utils.fromWei(balance, 'ether');

         setWalletState({
           address,
           balance: etherBalance,
           connected: true,
           network: networkName
         });
       }
     } else {
       setError('Please install MetaMask');
     }
   } catch (err) {
     console.error('Error connecting wallet:', err);
     setError('Failed to connect wallet');
   } finally {
     setLoading(false);
   }
 }, []);

 const getNetworkName = (networkId: number): string => {
   switch(networkId) {
     case 1: return 'Ethereum Mainnet';
     case 3: return 'Ropsten';
     case 4: return 'Rinkeby';
     case 5: return 'Goerli';
     case 42: return 'Kovan';
     default: return 'Unknown Network';
   }
 };

 const disconnectWallet = () => {
   setWalletState({
     address: '',
     balance: '0',
     connected: false,
     network: ''
   });
 };

 useEffect(() => {
   const handleAccountsChanged = async () => {
     const accounts = await window.ethereum.request({ method: 'eth_accounts' });
     if (accounts.length > 0) {
       await connectWallet();
     }
   };

   handleAccountsChanged();

   if (window.ethereum) {
     window.ethereum.on('accountsChanged', handleAccountsChanged);
     window.ethereum.on('chainChanged', () => window.location.reload());
   }

   return () => {
     if (window.ethereum) {
       window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
     }
   };
 }, [connectWallet]);

 return (
   <div className="container mx-auto px-4 py-8">
     {error && (
       <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg flex items-center">
         <AlertTriangle className="w-5 h-5 mr-2" />
         {error}
       </div>
     )}

     <div className="bg-white rounded-xl shadow-sm p-6">
       <div className="flex justify-between items-center mb-6">
         <div>
           <h2 className="text-2xl font-bold">Wallet</h2>
           {walletState.connected && (
             <p className="text-sm text-gray-500 mt-1">Connected to {walletState.network}</p>
           )}
         </div>
         {!walletState.connected ? (
           <button
             onClick={connectWallet}
             disabled={loading}
             className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
           >
             <WalletIcon className="w-5 h-5 mr-2" />
             {loading ? 'Connecting...' : 'Connect Wallet'}
           </button>
         ) : (
           <button
             onClick={disconnectWallet}
             className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center"
           >
             <Power className="w-5 h-5 mr-2" />
             Disconnect
           </button>
         )}
       </div>

       {walletState.connected && (
         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <div className="p-4 bg-gray-50 rounded-xl">
             <p className="text-sm text-gray-500 mb-1">Address</p>
             <p className="font-mono break-all">{walletState.address}</p>
           </div>
           <div className="p-4 bg-gray-50 rounded-xl">
             <p className="text-sm text-gray-500 mb-1">Balance</p>
             <p className="text-2xl font-bold">{parseFloat(walletState.balance).toFixed(4)} ETH</p>
           </div>
         </div>
       )}
     </div>
   </div>
 );
};

export default Wallet;
