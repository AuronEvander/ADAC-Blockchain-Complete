import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface TokenPerformanceProps {
  tokens: Token[];
}

interface Token {
  symbol: string;
  name: string;
  price: number;
  priceChange24h: number;
  balance: string;
}

// Mock data for the chart
const generateChartData = (initialPrice: number, change: number) => {
  const data = [];
  let price = initialPrice - (change * 2); // Start from a point that will reach current price
  
  for (let i = 0; i < 24; i++) {
    const timestamp = new Date();
    timestamp.setHours(timestamp.getHours() - (23 - i));
    
    // Add some randomness to the price progression
    const noise = Math.random() * 0.1 * initialPrice;
    price += (change / 12) + noise - (noise / 2);
    
    data.push({
      timestamp: timestamp.toLocaleTimeString(),
      price: parseFloat(price.toFixed(2))
    });
  }
  
  return data;
};

const TokenPerformance: React.FC<TokenPerformanceProps> = ({ tokens }) => {
  const mainToken = tokens.find(t => t.symbol === 'ADAC') || tokens[0];
  const chartData = generateChartData(mainToken.price, mainToken.priceChange24h);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Performance</h3>
        <div className="flex items-center space-x-4">
          {tokens.map(token => (
            <div key={token.symbol} className="flex items-center space-x-2">
              <span className="font-medium">{token.symbol}</span>
              <span className={`flex items-center ${
                token.priceChange24h >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {token.priceChange24h >= 0 ? (
                  <ArrowUpRight className="h-4 w-4" />
                ) : (
                  <ArrowDownRight className="h-4 w-4" />
                )}
                <span>{Math.abs(token.priceChange24h).toFixed(1)}%</span>
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tick={{ fontSize: 12 }} 
              interval="preserveStartEnd"
            />
            <YAxis 
              domain={['dataMin - 1', 'dataMax + 1']}
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
              labelStyle={{ color: '#666' }}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#2563eb" 
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Token Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-sm text-gray-600">24h Volume</p>
          <p className="text-lg font-medium mt-1">$1.2M</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-sm text-gray-600">Market Cap</p>
          <p className="text-lg font-medium mt-1">$50.5M</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-sm text-gray-600">Circulating Supply</p>
          <p className="text-lg font-medium mt-1">50.5M ADAC</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-sm text-gray-600">Total Supply</p>
          <p className="text-lg font-medium mt-1">100M ADAC</p>
        </div>
      </div>
    </div>
  );
};

export default TokenPerformance;