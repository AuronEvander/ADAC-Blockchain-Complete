import React, { useState, useEffect } from 'react';
import { 
    Card,
    CardHeader,
    CardContent,
    CardTitle,
    CardDescription 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import ProposalList from './ProposalList';
import CreateProposal from './CreateProposal';
import VoterStats from './VoterStats';
import GovernanceStats from './GovernanceStats';

const GovernanceDashboard = () => {
    const [activeProposals, setActiveProposals] = useState([]);
    const [pastProposals, setPastProposals] = useState([]);
    const [governanceStats, setGovernanceStats] = useState(null);
    const [voterInfo, setVoterInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showCreateModal, setShowCreateModal] = useState(false);

    useEffect(() => {
        fetchProposals();
        fetchGovernanceStats();
        fetchVoterInfo();
    }, []);

    const fetchProposals = async () => {
        try {
            const response = await fetch('/api/governance/proposals');
            const data = await response.json();

            const active = data.filter(p => p.status === 'active');
            const past = data.filter(p => p.status !== 'active');

            setActiveProposals(active);
            setPastProposals(past);
            setError(null);
        } catch (err) {
            setError('Failed to fetch proposals');
            console.error('Error fetching proposals:', err);
        } finally {
            setLoading(false);
        }
    };

    const fetchGovernanceStats = async () => {
        try {
            const response = await fetch('/api/governance/stats');
            const stats = await response.json();
            setGovernanceStats(stats);
        } catch (err) {
            console.error('Error fetching governance stats:', err);
        }
    };

    const fetchVoterInfo = async () => {
        try {
            // In a real app, you would get the voter's address from their wallet
            const address = '0xYourAddress';
            const response = await fetch(`/api/governance/voters/${address}`);
            const info = await response.json();
            setVoterInfo(info);
        } catch (err) {
            console.error('Error fetching voter info:', err);
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
                        <h1 className="text-4xl font-bold">Governance Dashboard</h1>
                        <p className="text-gray-600 mt-2">
                            Participate in the ADAC blockchain governance
                        </p>
                    </div>
                    <Button 
                        className="bg-primary text-white hover:bg-primary/90"
                        onClick={() => setShowCreateModal(true)}
                    >
                        Create Proposal
                    </Button>
                </div>

                {/* Error Alert */}
                {error && (
                    <Alert variant="destructive">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                {/* Stats Overview */}
                {governanceStats && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <GovernanceStats stats={governanceStats} />
                    </div>
                )}

                {/* Main Content */}
                <Tabs defaultValue="active" className="w-full">
                    <TabsList>
                        <TabsTrigger value="active">Active Proposals</TabsTrigger>
                        <TabsTrigger value="past">Past Proposals</TabsTrigger>
                        <TabsTrigger value="your-votes">Your Votes</TabsTrigger>
                    </TabsList>

                    <TabsContent value="active">
                        <Card>
                            <CardHeader>
                                <CardTitle>Active Proposals</CardTitle>
                                <CardDescription>
                                    Current proposals open for voting
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ProposalList 
                                    proposals={activeProposals}
                                    onVote={fetchProposals}
                                />
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="past">
                        <Card>
                            <CardHeader>
                                <CardTitle>Past Proposals</CardTitle>
                                <CardDescription>
                                    History of executed and rejected proposals
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <ProposalList 
                                    proposals={pastProposals}
                                    isPast={true}
                                />
                            </CardContent>
                        </Card>
                    </TabsContent>

                    <TabsContent value="your-votes">
                        <Card>
                            <CardHeader>
                                <CardTitle>Your Voting History</CardTitle>
                                <CardDescription>
                                    View your participation in governance
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <VoterStats voterInfo={voterInfo} />
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>

            {/* Create Proposal Modal */}
            {showCreateModal && (
                <CreateProposal
                    onClose={() => setShowCreateModal(false)}
                    onSuccess={() => {
                        setShowCreateModal(false);
                        fetchProposals();
                    }}
                />
            )}
        </div>
    );
};

export default GovernanceDashboard;
