import React, { useMemo } from 'react';
import { Card } from '@/components/ui/card';

const MarketSentimentGauge = ({ sentiment }) => {
    const {
        gaugeRotation,
        sentimentColor,
        sentimentText,
        confidenceWidth
    } = useMemo(() => {
        if (!sentiment) {
            return {
                gaugeRotation: 0,
                sentimentColor: 'text-gray-400',
                sentimentText: 'No Data',
                confidenceWidth: '0%'
            };
        }

        // Convert sentiment score (-1 to 1) to degrees (0 to 180)
        const degrees = (sentiment.sentiment_score + 1) * 90;
        
        // Determine color based on sentiment
        let color;
        let text;
        if (sentiment.sentiment_score > 0.3) {
            color = 'text-green-500';
            text = 'Bullish';
        } else if (sentiment.sentiment_score < -0.3) {
            color = 'text-red-500';
            text = 'Bearish';
        } else {
            color = 'text-yellow-500';
            text = 'Neutral';
        }

        return {
            gaugeRotation: degrees,
            sentimentColor: color,
            sentimentText: text,
            confidenceWidth: `${sentiment.confidence * 100}%`
        };
    }, [sentiment]);

    return (
        <div className="relative p-4">
            {/* Gauge Background */}
            <div className="relative w-48 h-24 mx-auto overflow-hidden">
                <div className="absolute w-full h-full bg-gray-200 rounded-t-full">
                    {/* Gauge Sections */}
                    <div className="absolute top-0 left-0 w-full h-full">
                        <div className="absolute top-0 left-0 w-1/3 h-full bg-red-200 rounded-tl-full" />
                        <div className="absolute top-0 left-1/3 w-1/3 h-full bg-yellow-200" />
                        <div className="absolute top-0 right-0 w-1/3 h-full bg-green-200 rounded-tr-full" />
                    </div>

                    {/* Gauge Needle */}
                    <div 
                        className="absolute top-0 left-1/2 w-1 h-24 bg-gray-800 origin-bottom"
                        style={{ 
                            transform: `translateX(-50%) rotate(${gaugeRotation}deg)`,
                            transition: 'transform 0.5s ease-out'
                        }}
                    >
                        <div className="absolute -top-1 -left-1 w-3 h-3 bg-gray-800 rounded-full" />
                    </div>
                </div>
            </div>

            {/* Sentiment Value */}
            <div className="mt-6 text-center">
                <p className={`text-2xl font-bold ${sentimentColor}`}>
                    {sentimentText}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                    Score: {sentiment?.sentiment_score.toFixed(2) || '--'}
                </p>
            </div>

            {/* Confidence Bar */}
            <div className="mt-4">
                <div className="flex justify-between text-sm text-gray-500 mb-1">
                    <span>Confidence</span>
                    <span>{sentiment ? `${(sentiment.confidence * 100).toFixed(1)}%` : '--'}</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                        className="h-full bg-blue-500 rounded-full transition-all duration-500"
                        style={{ width: confidenceWidth }}
                    />
                </div>
            </div>

            {/* Time Indicators */}
            <div className="mt-4 flex justify-between text-xs text-gray-400">
                <span>Bearish</span>
                <span>Neutral</span>
                <span>Bullish</span>
            </div>

            {/* Last Updated */}
            {sentiment?.timestamp && (
                <div className="mt-4 text-center text-xs text-gray-500">
                    Last updated: {new Date(sentiment.timestamp).toLocaleTimeString()}
                </div>
            )}

            {/* Contributing Factors */}
            {sentiment?.factors && (
                <div className="mt-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">
                        Contributing Factors
                    </h4>
                    <div className="space-y-2">
                        {sentiment.factors.map((factor, index) => (
                            <div 
                                key={index}
                                className="flex justify-between items-center text-sm"
                            >
                                <span className="text-gray-600">{factor.name}</span>
                                <span className={
                                    factor.impact > 0 ? 'text-green-500' :
                                    factor.impact < 0 ? 'text-red-500' :
                                    'text-yellow-500'
                                }>
                                    {factor.impact > 0 ? '+' : ''}{factor.impact.toFixed(2)}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default MarketSentimentGauge;