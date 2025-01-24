import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import AIDashboard from './components/ai/AIDashboard';
import Wallet from './components/wallet/Wallet';
import Explorer from './components/explorer/Explorer';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard address="0x" balance="0" />} />
        <Route path="ai" element={<AIDashboard />} />
        <Route path="wallet" element={<Wallet />} />
        <Route path="explorer" element={<Explorer />} />
      </Route>
    </Routes>
  );
};

export default App;
