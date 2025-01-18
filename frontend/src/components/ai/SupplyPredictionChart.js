import React, { useMemo } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Area,
    AreaChart
} from 'recharts';
import { Card } from '@/components/ui/card';

const SupplyPredictionChart = ({ data }) => {
    const chartData = useMemo(() => {
        if (!data) return [];

        // Create historical and prediction data points
        const historical = data.historical_supply || [];
        const prediction = data.predicted_supply;
        const confidenceBounds = data.confidence_bounds || {
            upper: prediction * 1.1,
            lower: prediction * 0.9
        };

        // Combine historical and prediction data
        const combinedData = [
            ...historical.map((value, index) => ({
                timestamp: new Date(Date.now() - (historical.length - index) * 3600000).toISOString(),
                supply: value,
                type: 'historical'
            })),
            {
                timestamp: new Date().toISOString(),
                supply: prediction,
                prediction: prediction,
                upperBound: confidenceBounds.upper,
                lowerBound: confidenceBounds.lower,
                type: 'prediction'
            }
        ];

        return combinedData;
    }, [data]);

    if (!data) {
        return (
            <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
                <p className="text-gray-500">No prediction data available</p>
            </div>
        );
    }

    const formatYAxis = (value) => {
        if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`;
        if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`;
        if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
        return value.toFixed(0);
    };

    const formatTooltip = (value, name) => {
        if (name === 'prediction') return ['Predicted Supply', formatYAxis(value)];
        if (name === 'supply') return ['Historical Supply', formatYAxis(value)];
        if (name === 'upperBound') return ['Upper Bound', formatYAxis(value)];
        if (name === 'lowerBound') return ['Lower Bound', formatYAxis(value)];
        return [name, value];
    };

    const formatXAxis = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    };

    return (
        <div className="w-full h-[400px]">
            <ResponsiveContainer>
                <AreaChart
                    data={chartData}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                    <defs>
                        <linearGradient id="colorHistorical" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.1}/>
                            <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorConfidence" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.2}/>
                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                        </linearGradient>
                    </defs>

                    <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200" />
                    <XAxis
                        dataKey="timestamp"
                        tickFormatter={formatXAxis}
                        stroke="#94a3b8"
                        fontSize={12}
                    />
                    <YAxis
                        tickFormatter={formatYAxis}
                        stroke="#94a3b8"
                        fontSize={12}
                    />
                    <Tooltip 
                        formatter={formatTooltip}
                        contentStyle={{
                            backgroundColor: 'rgba(255, 255, 255, 0.9)',
                            border: '1px solid #e2e8f0',
                            borderRadius: '6px',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                        }}
                    />
                    <Legend />

                    {/* Historical Supply */}
                    <Area
                        type="monotone"
                        dataKey="supply"
                        stroke="#0ea5e9"
                        fill="url(#colorHistorical)"
                        strokeWidth={2}
                        name="Historical Supply"
                        dot={false}
                    />

                    {/* Prediction */}
                    <Line
                        type="monotone"
                        dataKey="prediction"
                        stroke="#6366f1"
                        strokeWidth={2}
                        name="Predicted Supply"
                        dot={{
                            stroke: '#6366f1',
                            strokeWidth: 2,
                            r: 4,
                            fill: '#fff'
                        }}
                    />

                    {/* Confidence Bounds */}
                    <Area
                        type="monotone"
                        dataKey="upperBound"
                        stroke="transparent"
                        fill="url(#colorConfidence)"
                        name="Confidence Bound"
                    />
                    <Area
                        type="monotone"
                        dataKey="lowerBound"
                        stroke="transparent"
                        fill="url(#colorConfidence)"
                        name="Confidence Bound"
                    />
                </AreaChart>
            </ResponsiveContainer>

            {/* Prediction Details */}
            <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="text-center">
                    <p className="text-sm text-gray-500">Current Supply</p>
                    <p className="text-lg font-semibold">
                        {formatYAxis(chartData[chartData.length - 2]?.supply || 0)}
                    </p>
                </div>
                <div className="text-center">
                    <p className="text-sm text-gray-500">Predicted Supply</p>
                    <p className="text-lg font-semibold text-indigo-600">
                        {formatYAxis(data.predicted_supply)}
                    </p>
                </div>
                <div className="text-center">
                    <p className="text-sm text-gray-500">Confidence</p>
                    <p className="text-lg font-semibold">
                        {(data.confidence * 100).toFixed(1)}%
                    </p>
                </div>
            </div>
        </div>
    );
};

export default SupplyPredictionChart;