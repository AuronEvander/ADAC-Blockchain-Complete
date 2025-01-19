import React, { useState, useEffect } from 'react';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription
} from '@/components/ui/card';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';
import { 
    Brain,
    TrendingUp,
    AlertTriangle,
    Activity,
    DatabaseZap
} from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import AIMetricsCard from './AIMetricsCard';
import SupplyPredictionChart from './SupplyPredictionChart';
import MarketSentimentGauge from './MarketSentimentGauge';
import AnomalyList from './AnomalyList';

const AIDashboard = () => {
    const [aiStats, setAIStats] = useState(null);
    const [supplyPrediction, setSupplyPrediction] = useState(null);
    const [marketSentiment, setMarketSentiment] = useState(null);
    const [anomalies, setAnomalies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAIData();
        const interval = setInterval(fetchAIData, 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, []);

    const getCurrentDemand = () => {
        return 5000; // Placeholder
    };

    const getCurrentPrice = () => {
        return 10.5; // Placeholder
    };

    const getCurrentVolume = () => {
        return 100000; // Placeholder
    };

    const getCurrentStakingRatio = () => {
        return 0.6; // Placeholder
    };

    const getCurrentSupply = () => {
        return 5000000; // Placeholder
    };

    const getRecentTransactions = async () => {
        return []; // Placeholder
    };

    const getSocialData = async () => {
        return []; // Placeholder
    };

    const fetchAIData = async () => {
        try {
            setLoading(true);
            
            const statsResponse = await fetch('/api/ai/stats');
            const stats = await statsResponse.json();
            setAIStats(stats);

            const currentMarket = {
                demand: getCurrentDemand(),
                price: getCurrentPrice(),
                transaction_volume: getCurrentVolume(),
                staking_ratio: getCurrentStakingRatio(),
                current_supply: getCurrentSupply()
            };

            const predictionResponse = await fetch('/api/ai/supply/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentMarket)
            });
            const prediction = await predictionResponse.json();
            setSupplyPrediction(prediction);

            const sentimentResponse = await fetch('/api/ai/market/sentiment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    transactions: await getRecentTransactions(),
                    social_data: await getSocialData()
                })
            });
            const sentiment = await sentimentResponse.json();
            setMarketSentiment(sentiment);

            const anomalyResponse = await fetch('/api/ai/transactions/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(await getRecentTransactions())
            });
            const anomalyData = await anomalyResponse.json();
            setAnomalies(anomalyData.results.filter(r => r.is_anomaly));

            setError(null);
        } catch (err) {
            console.error('Error fetching AI data:', err);
            setError('Failed to fetch AI analytics data');
        } finally {
            setLoading(false);
        }
    };

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
                    <AIMetricsCard
                        title="Supply Prediction"
                        value={supplyPrediction?.predicted_supply}
                        change={supplyPrediction?.recommended_change}
                        icon={<TrendingUp className="h-6 w-6" />}
                    />
                    <AIMetricsCard
                        title="Market Sentiment"
                        value={marketSentiment?.sentiment_score}
                        confidence={marketSentiment?.confidence}
                        icon={<Activity className="h-6 w-6" />}
                    />
                    <AIMetricsCard
                        title="Detected Anomalies"
                        value={anomalies.length}
                        timestamp={anomalies[0]?.timestamp}
                        icon={<AlertTriangle className="h-6 w-6" />}
                    />
                </div>

                {/* Charts and Analysis */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Supply Prediction Chart */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Supply Prediction Analysis</CardTitle>
                            <CardDescription>
                                AI-driven supply predictions and trends
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <SupplyPredictionChart data={supplyPrediction} />
                        </CardContent>
                    </Card>

                    {/* Market Sentiment Gauge */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Market Sentiment Analysis</CardTitle>
                            <CardDescription>
                                Real-time market sentiment indicators
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <MarketSentimentGauge sentiment={marketSentiment} />
                        </CardContent>
                    </Card>
                </div>

                {/* Anomaly Detection */}
                <Card>
                    <CardHeader>
                        <CardTitle>Detected Anomalies</CardTitle>
                        <CardDescription>
                            Recent suspicious transactions and patterns
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <AnomalyList anomalies={anomalies} />
                    </CardContent>
                </Card>

                {/* AI System Stats */}
                <Card>
                    <CardHeader>
                        <CardTitle>AI System Status</CardTitle>
                        <CardDescription>
                            Current state and performance metrics
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
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
                                    {aiStats?.historical_data_points?.total || 0}
                                </div>
                            </div>
                            <div className="p-4 bg-gray-50 rounded-lg">
                                <div className="text-sm text-gray-600">Last Update</div>
                                <div className="text-lg font-bold">
                                    {new Date(aiStats?.timestamp).toLocaleTimeString()}
                                </div>
                            </div>
                            <div className="p-4 bg-gray-50 rounded-lg">
                                <div className="text-sm text-gray-600">System Health</div>
                                <div className="text-2xl font-bold text-green-500">
                                    Healthy
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default AIDashboard;