import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { formatDistanceToNow } from 'date-fns';

const ProposalList = ({ proposals, isPast = false, onVote }) => {
    const handleVote = async (proposalId, vote) => {
        try {
            // In a real app, you would get the voter's address from their wallet
            const response = await fetch(`/api/governance/proposals/${proposalId}/vote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    voter: '0xYourAddress',
                    vote: vote
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to cast vote');
            }

            if (onVote) onVote();
        } catch (error) {
            console.error('Error casting vote:', error);
        }
    };

    const getBadgeColor = (status) => {
        switch (status) {
            case 'active':
                return 'bg-green-500';
            case 'passed':
                return 'bg-blue-500';
            case 'executed':
                return 'bg-purple-500';
            case 'rejected':
                return 'bg-red-500';
            default:
                return 'bg-gray-500';
        }
    };

    const calculateVotePercentages = (proposal) => {
        const totalVotes = Object.values(proposal.votes_for).reduce((a, b) => a + b, 0) +
                         Object.values(proposal.votes_against).reduce((a, b) => a + b, 0);
        
        const forPercentage = totalVotes === 0 ? 0 : 
            (Object.values(proposal.votes_for).reduce((a, b) => a + b, 0) / totalVotes) * 100;
        
        return {
            for: forPercentage,
            against: 100 - forPercentage,
            total: totalVotes
        };
    };

    const renderVotingButtons = (proposal) => {
        if (isPast) return null;

        return (
            <div className="flex gap-2 mt-4">
                <Button 
                    onClick={() => handleVote(proposal.id, 'for')}
                    className="bg-green-500 hover:bg-green-600 text-white"
                >
                    Vote For
                </Button>
                <Button 
                    onClick={() => handleVote(proposal.id, 'against')}
                    className="bg-red-500 hover:bg-red-600 text-white"
                >
                    Vote Against
                </Button>
            </div>
        );
    };

    if (!proposals.length) {
        return (
            <div className="text-center p-8 text-gray-500">
                No proposals found
            </div>
        );
    }

    return (
        <div className="grid gap-4">
            {proposals.map((proposal) => {
                const voteStats = calculateVotePercentages(proposal);
                
                return (
                    <Card key={proposal.id} className="hover:shadow-lg transition-shadow">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h3 className="text-xl font-semibold mb-2">
                                        {proposal.title}
                                    </h3>
                                    <p className="text-gray-600 mb-2">
                                        {proposal.description}
                                    </p>
                                </div>
                                <Badge className={getBadgeColor(proposal.status)}>
                                    {proposal.status}
                                </Badge>
                            </div>

                            <div className="mb-4">
                                <div className="flex justify-between mb-2">
                                    <span>For: {voteStats.for.toFixed(1)}%</span>
                                    <span>Against: {voteStats.against.toFixed(1)}%</span>
                                </div>
                                <Progress value={voteStats.for} max={100} />
                                <div className="text-sm text-gray-500 mt-1">
                                    Total votes: {voteStats.total}
                                </div>
                            </div>

                            <div className="flex justify-between items-center text-sm text-gray-500">
                                <div>
                                    Proposed by: {proposal.proposer.slice(0, 6)}...{proposal.proposer.slice(-4)}
                                </div>
                                <div>
                                    {formatDistanceToNow(new Date(proposal.creation_time), { addSuffix: true })}
                                </div>
                            </div>

                            {proposal.parameters && Object.keys(proposal.parameters).length > 0 && (
                                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                                    <h4 className="font-semibold mb-2">Parameters:</h4>
                                    <pre className="text-sm">
                                        {JSON.stringify(proposal.parameters, null, 2)}
                                    </pre>
                                </div>
                            )}

                            {renderVotingButtons(proposal)}

                            {proposal.comments && proposal.comments.length > 0 && (
                                <div className="mt-4">
                                    <h4 className="font-semibold mb-2">Recent Comments:</h4>
                                    <div className="space-y-2">
                                        {proposal.comments.slice(0, 3).map((comment, index) => (
                                            <div key={index} className="text-sm text-gray-600 p-2 bg-gray-50 rounded">
                                                <span className="font-medium">
                                                    {comment.commenter.slice(0, 6)}...{comment.commenter.slice(-4)}:
                                                </span> {comment.comment}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                );
            })}
        </div>
    );
};

export default ProposalList;