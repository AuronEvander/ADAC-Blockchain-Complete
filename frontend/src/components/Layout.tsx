import React from 'react';
import { Link, Outlet } from 'react-router-dom';

const Layout = () => {
 return (
   <div>
     <nav className="bg-white border-b">
       <div className="max-w-7xl mx-auto px-4">
         <div className="flex justify-between h-16">
           <div className="flex">
             <Link to="/" className="flex-shrink-0 flex items-center text-2xl font-bold text-blue-600">
               ADAC Blockchain
             </Link>
             <div className="ml-10 flex items-center space-x-4">
               <Link to="/" className="px-3 py-2 text-gray-600 hover:text-gray-900">Dashboard</Link>
               <Link to="/ai" className="px-3 py-2 text-gray-600 hover:text-gray-900">AI Analytics</Link>
               <Link to="/wallet" className="px-3 py-2 text-gray-600 hover:text-gray-900">Wallet</Link>
               <Link to="/explorer" className="px-3 py-2 text-gray-600 hover:text-gray-900">Explorer</Link>
             </div>
           </div>
         </div>
       </div>
     </nav>
     <main className="max-w-7xl mx-auto py-6 px-4">
       <Outlet />
     </main>
   </div>
 );
};

export default Layout;
