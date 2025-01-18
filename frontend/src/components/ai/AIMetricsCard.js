import React from 'react';
import {
    Card,
    CardContent,
} from '@/components/ui/card';
import { ArrowUpIcon, ArrowDownIcon } from 'lucide-react';

const AIMetricsCard = ({ title, value, change, confidence, timestamp, icon }) => {
    const formatValue = (val) => {
        if (typeof val === 'number') {
            return val > 1000 ? 
                val.toLocaleString(undefined, { maximumFractionDigits: 0 }) :
                val.toLocaleString(undefined, { maximumFractionDigits: 2 });
        }
        return '--';
    };

    const formatChange = (val) => {
        if (typeof val === 'number') {
            return val > 0 ? `+${val.toFixed(2)}%` : `${val.toFixed(2)}%`;
        }
        return null;
    };

    const getChangeColor = (val) => {
        if (typeof val !== 'number') return 'text-gray-500';
        return val > 0 ? 'text-green-500' : 'text-red-500';
    };

    const renderChangeIndicator = () => {
        if (typeof change !== 'number') return null;

        return change > 0 ? (
            <ArrowUpIcon className="h-4 w-4 text-green-500" />
        ) : (
            <ArrowDownIcon className="h-4 w-4 text-red-500" />
        );
    };

    return (
        <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
                <div className="flex justify-between items-start">
                    <div className="space-y-2">
                        <p className="text-sm font-medium text-gray-500">
                            {title}
                        </p>
                        <div className="flex items-center space-x-2">
                            <p className="text-2xl font-bold">
                                {formatValue(value)}
                            </p>
                            {renderChangeIndicator()}
                        </div>
                    </div>
                    <div className="p-2 bg-primary/10 rounded-full">
                        {icon}
                    </div>
                </div>

                {/* Additional Metrics */}
                <div className="mt-4 space-y-2">
                    {change !== undefined && (
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-500">Change</span>
                            <span className={`text-sm font-medium ${getChangeColor(change)}`}>
                                {formatChange(change)}
                            </span>
                        </div>
                    )}

                    {confidence !== undefined && (
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-500">Confidence</span>
                            <span className="text-sm font-medium">
                                {(confidence * 100).toFixed(1)}%
                            </span>
                        </div>
                    )}

                    {timestamp && (
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-500">Last Updated</span>
                            <span className="text-sm text-gray-600">
                                {new Date(timestamp).toLocaleTimeString()}
                            </span>
                        </div>
                    )}
                </div>

                {/* Progress Bar for Confidence */}
                {confidence !== undefined && (
                    <div className="mt-4">
                        <div className="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                            <div 
                                className="h-full bg-primary rounded-full transition-all duration-500"
                                style={{ width: `${confidence * 100}%` }}
                            />
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};

export default AIMetricsCard;