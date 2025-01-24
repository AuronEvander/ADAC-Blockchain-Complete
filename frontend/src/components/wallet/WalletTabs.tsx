import React, { ReactNode } from 'react';

interface WalletTabsProps {
  children: ReactNode;
}

export interface TabPanelProps {
  children?: ReactNode;
  id: string;
}

export const TabPanel: React.FC<TabPanelProps> = ({ children, id }) => (
  <div id={id}>
    {children}
  </div>
);

const WalletTabs: React.FC<WalletTabsProps> = ({ children }) => {
  const [activeTab, setActiveTab] = React.useState('send');

  return (
    <div>
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex">
          {['Send', 'Swap', 'Stake', 'History'].map((tab) => (
            <button
              key={tab}
              className={`${
                activeTab === tab.toLowerCase()
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm`}
              onClick={() => setActiveTab(tab.toLowerCase())}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>
      {children}
    </div>
  );
};

export default WalletTabs;
