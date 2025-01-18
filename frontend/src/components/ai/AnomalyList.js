import React from 'react';
import {
    AlertCircle,
    AlertTriangle,
    Clock,
    DollarSign,
    Hash,
    User
} from 'lucide-react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip';

const AnomalyList = ({ anomalies }) => {
    const getAnomalyType = (anomaly) => {
        if (anomaly.amount > 1000000) return 'Large Transaction';
        if (anomaly.gas_price > 100) return 'High Gas Price';
        if (anomaly.block_time > 15) return 'Slow Block Time';
        return 'Unusual Pattern';
    };

    const getAnomalySeverity = (anomaly) => {
        const type = getAnomalyType(anomaly);
        const confidence = anomaly.confidence || 0.5;

        if (type === 'Large Transaction' && confidence > 0.8) return 'high';
        if (type === 'High Gas Price' && confidence > 0.7) return 'medium';
        if (confidence > 0.9) return 'high';
        if (confidence > 0.6) return 'medium';
        return 'low';
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'high':
                return 'bg-red-100 text-red-800';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800';
            case 'low':
                return 'bg-blue-100 text-blue-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const formatAmount = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'decimal',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    };

    const formatAddress = (address) => {
        if (!address) return '--';
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    };

    if (!anomalies || anomalies.length === 0) {
        return (
            <div className="text-center p-8 text-gray-500">
                <AlertCircle className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p>No anomalies detected</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center mb-4">
                <div>
                    <h3 className="text-lg font-medium">
                        Detected Anomalies ({anomalies.length})
                    </h3>
                    <p className="text-sm text-gray-500">
                        Last updated: {new Date().toLocaleTimeString()}
                    </p>
                </div>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <Button variant="outline" size="sm">
                                <AlertTriangle className="h-4 w-4 mr-2" />
                                Export Report
                            </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                            Export detailed anomaly report
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
            </div>

            <ScrollArea className="h-[400px]">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Type</TableHead>
                            <TableHead>Amount</TableHead>
                            <TableHead>Addresses</TableHead>
                            <TableHead>Time</TableHead>
                            <TableHead>Severity</TableHead>
                            <TableHead>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {anomalies.map((anomaly, index) => {
                            const severity = getAnomalySeverity(anomaly);
                            const type = getAnomalyType(anomaly);

                            return (
                                <TableRow key={index}>
                                    <TableCell>
                                        <div className="flex items-center">
                                            <AlertCircle className="h-4 w-4 mr-2 text-red-500" />
                                            {type}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center">
                                            <DollarSign className="h-4 w-4 mr-1 text-gray-500" />
                                            {formatAmount(anomaly.amount)}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="space-y-1">
                                            <div className="flex items-center">
                                                <User className="h-3 w-3 mr-1 text-gray-500" />
                                                From: {formatAddress(anomaly.from)}
                                            </div>
                                            <div className="flex items-center">
                                                <User className="h-3 w-3 mr-1 text-gray-500" />
                                                To: {formatAddress(anomaly.to)}
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center">
                                            <Clock className="h-4 w-4 mr-1 text-gray-500" />
                                            {new Date(anomaly.timestamp).toLocaleTimeString()}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge className={getSeverityColor(severity)}>
                                            {severity.charAt(0).toUpperCase() + severity.slice(1)}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex space-x-2">
                                            <TooltipProvider>
                                                <Tooltip>
                                                    <TooltipTrigger asChild>
                                                        <Button variant="outline" size="sm">
                                                            Details
                                                        </Button>
                                                    </TooltipTrigger>
                                                    <TooltipContent>
                                                        View anomaly details
                                                    </TooltipContent>
                                                </Tooltip>
                                            </TooltipProvider>
                                            <TooltipProvider>
                                                <Tooltip>
                                                    <TooltipTrigger asChild>
                                                        <Button variant="outline" size="sm">
                                                            Investigate
                                                        </Button>
                                                    </TooltipTrigger>
                                                    <TooltipContent>
                                                        Start investigation
                                                    </TooltipContent>
                                                </Tooltip>
                                            </TooltipProvider>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </ScrollArea>

            {/* Summary Section */}
            <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="text-sm font-medium text-gray-600">High Severity</h4>
                    <p className="text-2xl font-bold text-red-600">
                        {anomalies.filter(a => getAnomalySeverity(a) === 'high').length}
                    </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="text-sm font-medium text-gray-600">Medium Severity</h4>
                    <p className="text-2xl font-bold text-yellow-600">
                        {anomalies.filter(a => getAnomalySeverity(a) === 'medium').length}
                    </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="text-sm font-medium text-gray-600">Low Severity</h4>
                    <p className="text-2xl font-bold text-blue-600">
                        {anomalies.filter(a => getAnomalySeverity(a) === 'low').length}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AnomalyList;