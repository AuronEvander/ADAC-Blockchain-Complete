import React from 'react';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle
} from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { formatDistanceToNow } from 'date-fns';

const VoterStats = ({ voterInfo }) => {
    if (!voterInfo) {
        return (
            <div className="text-center p-8 text-gray-500">
                No voting history found
            </div>
        );
    }

    const { 
        address, 
        voted_proposals, 
        total_voting_power_used,
        participation_rate 
    } = voterInfo;

    const groupVotesByType = () => {
        return voted_proposals.reduce((acc, vote) => {
            acc[vote.vote_type] = (acc[vote.vote_type] || 0) + 1;
            return acc;
        }, {});
    };

    const votesByType = groupVotesByType();
    const participation_percentage = participation_rate * 100;

    return (
        <div className="space-y-6">
            {/* Overview Card */}
            <Card>
                <CardHeader>
                    <CardTitle>Voting Overview</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Total Proposals Voted</div>
                            <div className="text-2xl font-bold">{voted_proposals.length}</div>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Voting Power Used</div>
                            <div className="text-2xl font-bold">{total_voting_power_used.toLocaleString()}</div>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg">
                            <div className="text-sm text-gray-600">Participation Rate</div>
                            <div className="text-2xl font-bold">{participation_percentage.toFixed(1)}%</div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Vote Distribution Card */}
            <Card>
                <CardHeader>
                    <CardTitle>Vote Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {Object.entries(votesByType).map(([type, count]) => (
                            <div key={type}>
                                <div className="flex justify-between mb-1">
                                    <span className="text-sm font-medium capitalize">
                                        {type}
                                    </span>
                                    <span className="text-sm text-gray-600">
                                        {count} votes
                                    </span>
                                </div>
                                <Progress
                                    value={(count / voted_proposals.length) * 100}
                                    max={100}
                                    className={`h-2 ${
                                        type === 'for' ? 'bg-green-500' : 
                                        type === 'against' ? 'bg-red-500' : 'bg-gray-500'
                                    }`}
                                />
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Recent Votes Card */}
            <Card>
                <CardHeader>
                    <CardTitle>Recent Votes</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {voted_proposals.slice(0, 5).map((vote, index) => (
                            <div 
                                key={index}
                                className="flex justify-between items-center p-4 bg-gray-50 rounded-lg"
                            >
                                <div>
                                    <div className="font-medium">
                                        Proposal #{vote.proposal_id}
                                    </div>
                                    <div className="text-sm text-gray-600">
                                        Voted: {' '}
                                        <span 
                                            className={
                                                vote.vote_type === 'for' ? 'text-green-600' :
                                                vote.vote_type === 'against' ? 'text-red-600' :
                                                'text-gray-600'
                                            }
                                        >
                                            {vote.vote_type}
                                        </span>
                                    </div>
                                </div>
                                <div className="text-sm text-gray-500">
                                    Power: {vote.voting_power.toLocaleString()}
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Voter Details */}
            <div className="text-sm text-gray-500 text-center">
                Address: {address.slice(0, 6)}...{address.slice(-4)}
            </div>
        </div>
    );
};

export default VoterStats;