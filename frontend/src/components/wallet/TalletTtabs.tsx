import React, { useState } from 'react';
import { 
  Wallet as WalletIcon,
  ArrowDownUp,
  Lock,
  History
} from 'lucide-react';

interface WalletTabsProps {
  children: React.ReactNode;
}

interface TabItem {
  id: string;
  label: string;
  icon: React.ReactNode;
}

const WalletTabs: React.FC<WalletTabsProps> = ({ children }) => {
  const [activeTab, setActiveTab] = useState('send');

  const tabs: TabItem[] = [
    { id: 'send', label: 'Send', icon: <WalletIcon className="h-5 w-5" /> },
    { id: 'swap', label: 'Swap', icon: <ArrowDownUp className="h-5 w-5" /> },
    { id: 'stake', label: 'Stake', icon: <Lock className="h-5 w-5" /> },
    { id: 'history', label: 'History', icon: <History className="h-5 w-5" /> }
  ];

  return (
    <div>
      {/* Tab Navigation */}
      <div className="border-b mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}
              `}
            >
              <span className="flex items-center space-x-2">
                {tab.icon}
                <span>{tab.label}</span>
              </span>
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div>
        {React.Children.map(children, (child) => {
          if (React.isValidElement(child) && child.props.id === activeTab) {
            return child;
          }
          return null;
        })}
      </div>
    </div>
  );
};

export interface TabPanelProps {
  id: string;
  children: React.ReactNode;
}

export const TabPanel: React.FC<TabPanelProps> = ({ children }) => {
  return <div>{children}</div>;
};

export default WalletTabs;