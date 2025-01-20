import React, { useState, useEffect } from 'react';
import { 
  Brain,
  TrendingUp,
  AlertTriangle,
  Activity,
} from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface AIStats {
  models: {
    supply_model: {
      trained: boolean;
    };
  };
  historical_data_points: {
    total: number;
  };
  timestamp: string;
}

interface MarketData {
  demand: number;
  price: number;
  transaction_volume: number;
  staking_ratio: number;
  current_supply: number;
}

interface SupplyPrediction {
  predicted_supply: number;
  recommended_change: number;
  confidence: number;
}

interface MarketSentiment {
  sentiment_score: number;
  confidence: number;
  factors: string[];
}

interface Anomaly {
  id: string;
  timestamp: string;
  type: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  transaction_hash: string;
}

const AIDashboard: React.FC = () => {
  const [aiStats, setAIStats] = useState<AIStats | null>(null);
  const [supplyPrediction, setSupplyPrediction] = useState<SupplyPrediction | null>(null);
  const [marketSentiment, setMarketSentiment] = useState<MarketSentiment | null>(null);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const getCurrentMarketData = (): MarketData => ({
    demand: 5000,
    price: 10.5,
    transaction_volume: 100000,
    staking_ratio: 0.6,
    current_supply: 5000000
  });

  const fetchAIData = async () => {
    try {
      setLoading(true);
      
      // Fetch AI system stats
      const statsResponse = await fetch('/api/ai/stats');
      if (!statsResponse.ok) throw new Error('Failed to fetch AI stats');
      const stats = await statsResponse.json();
      setAIStats(stats);

      // Get current market data
      const currentMarket = getCurrentMarketData();

      // Fetch supply prediction
      const predictionResponse = await fetch('/api/ai/supply/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentMarket)
      });
      if (!predictionResponse.ok) throw new Error('Failed to fetch supply prediction');
      const prediction = await predictionResponse.json();
      setSupplyPrediction(prediction);

      // Fetch market sentiment
      const sentimentResponse = await fetch('/api/ai/market/sentiment');
      if (!sentimentResponse.ok) throw new Error('Failed to fetch market sentiment');
      const sentiment = await sentimentResponse.json();
      setMarketSentiment(sentiment);

      // Fetch recent anomalies
      const anomalyResponse = await fetch('/api/ai/transactions/analyze');
      if (!anomalyResponse.ok) throw new Error('Failed to fetch anomalies');
      const anomalyData = await anomalyResponse.json();
      setAnomalies(anomalyData.results.filter((r: Anomaly) => r.severity !== 'low'));

      setError(null);
    } catch (err) {
      console.error('Error fetching AI data:', err);
      setError('Failed to fetch AI analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAIData();
    const interval = setInterval(fetchAIData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid gap-6">
        {/* Header Section */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold">AI Analytics Dashboard</h1>
            <p className="text-gray-600 mt-2">
              Real-time AI-driven insights and predictions
            </p>
          </div>
          <Brain className="h-12 w-12 text-primary" />
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-white rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Supply Prediction</h3>
                <p className="text-3xl font-bold mt-2">
                  {supplyPrediction?.predicted_supply.toLocaleString()}
                </p>
                {supplyPrediction?.recommended_change !== 0 && (
                  <p className={`text-sm mt-1 ${supplyPrediction?.recommended_change > 0 ? 'text-green-500' : 'text-red-500'}`}>
                    {supplyPrediction?.recommended_change > 0 ? '+' : ''}
                    {supplyPrediction?.recommended_change}%
                  </p>
                )}
              </div>
              <TrendingUp className="h-10 w-10 text-blue-500" />
            </div>
          </div>

          <div className="p-4 bg-white rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Market Sentiment</h3>
                <p className="text-3xl font-bold mt-2">
                  {marketSentiment?.sentiment_score.toFixed(2)}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  {marketSentiment?.confidence.toFixed(1)}% confidence
                </p>
              </div>
              <Activity className="h-10 w-10 text-green-500" />
            </div>
          </div>

          <div className="p-4 bg-white rounded-lg shadow">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Active Anomalies</h3>
                <p className="text-3xl font-bold mt-2">
                  {anomalies.length}
                </p>
                {anomalies.length > 0 && (
                  <p className="text-sm text-red-500 mt-1">
                    Latest: {new Date(anomalies[0].timestamp).toLocaleTimeString()}
                  </p>
                )}
              </div>
              <AlertTriangle className="h-10 w-10 text-red-500" />
            </div>
          </div>
        </div>

        {/* Anomalies List */}
        {anomalies.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Recent Anomalies</h2>
            <div className="space-y-4">
              {anomalies.map((anomaly) => (
                <div key={anomaly.id} className="border-l-4 border-red-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold">{anomaly.type}</p>
                      <p className="text-sm text-gray-600">{anomaly.description}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        Transaction: {anomaly.transaction_hash}
                      </p>
                    </div>
                    <div className="flex items-center">
                      <span className={`px-2 py-1 rounded text-xs ${
                        anomaly.severity === 'high' 
                          ? 'bg-red-100 text-red-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {anomaly.severity}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI System Stats */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">System Status</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Model Status</div>
              <div className="text-2xl font-bold">
                {aiStats?.models?.supply_model?.trained ? 'Trained' : 'Not Trained'}
              </div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Historical Data Points</div>
              <div className="text-2xl font-bold">
                {aiStats?.historical_data_points?.total?.toLocaleString() || 0}
              </div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Last Update</div>
              <div className="text-lg font-bold">
                {aiStats?.timestamp ? new Date(aiStats.timestamp).toLocaleTimeString() : 'N/A'}
              </div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">System Health</div>
              <div className="text-2xl font-bold text-green-500">
                Healthy
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIDashboard;