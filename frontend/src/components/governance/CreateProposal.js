import React, { useState } from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from '@/components/ui/dialog';
import {
    Form,
    FormField,
    FormItem,
    FormLabel,
    FormControl,
    FormMessage
} from '@/components/ui/form';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useForm } from 'react-hook-form';

const PROPOSAL_TYPES = [
    { value: 'parameter_change', label: 'Parameter Change' },
    { value: 'feature_request', label: 'Feature Request' },
    { value: 'treasury_spending', label: 'Treasury Spending' },
    { value: 'protocol_upgrade', label: 'Protocol Upgrade' },
    { value: 'emergency_action', label: 'Emergency Action' }
];

const DEFAULT_PARAMETERS = {
    parameter_change: {
        staking_minimum: '',
        reward_rate: '',
        transaction_fee: '',
        validator_minimum: ''
    },
    treasury_spending: {
        amount: '',
        recipient: '',
        purpose: ''
    },
    protocol_upgrade: {
        version: '',
        changelog: '',
        deployment_date: ''
    }
};

const CreateProposal = ({ onClose, onSuccess }) => {
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const form = useForm({
        defaultValues: {
            title: '',
            description: '',
            proposal_type: '',
            parameters: {}
        }
    });

    const proposalType = form.watch('proposal_type');

    const onSubmit = async (data) => {
        setLoading(true);
        setError(null);
        
        try {
            // In a real app, you would get the proposer's address from their wallet
            const proposerAddress = '0xYourAddress';
            
            const response = await fetch('/api/governance/proposals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...data,
                    proposer: proposerAddress
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to create proposal');
            }

            onSuccess();
        } catch (err) {
            setError(err.message);
            console.error('Error creating proposal:', err);
        } finally {
            setLoading(false);
        }
    };

    const onTypeChange = (type) => {
        form.setValue('proposal_type', type);
        form.setValue('parameters', DEFAULT_PARAMETERS[type] || {});
    };

    const renderParameterFields = () => {
        if (!proposalType || !DEFAULT_PARAMETERS[proposalType]) {
            return null;
        }

        const parameters = DEFAULT_PARAMETERS[proposalType];

        return Object.keys(parameters).map((param) => (
            <FormField
                key={param}
                name={`parameters.${param}`}
                control={form.control}
                render={({ field }) => (
                    <FormItem>
                        <FormLabel className="capitalize">
                            {param.replace(/_/g, ' ')}
                        </FormLabel>
                        <FormControl>
                            <Input {...field} placeholder={`Enter ${param.replace(/_/g, ' ')}`} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
        ));
    };

    return (
        <Dialog open={true} onOpenChange={onClose}>
            <DialogContent className="max-w-md">
                <DialogHeader>
                    <DialogTitle>Create New Proposal</DialogTitle>
                </DialogHeader>

                {error && (
                    <Alert variant="destructive">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                        <FormField
                            name="title"
                            control={form.control}
                            rules={{ required: 'Title is required' }}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Title</FormLabel>
                                    <FormControl>
                                        <Input {...field} placeholder="Enter proposal title" />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            name="description"
                            control={form.control}
                            rules={{ required: 'Description is required' }}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Description</FormLabel>
                                    <FormControl>
                                        <Textarea 
                                            {...field} 
                                            placeholder="Enter proposal description"
                                            className="min-h-[100px]"
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            name="proposal_type"
                            control={form.control}
                            rules={{ required: 'Proposal type is required' }}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Proposal Type</FormLabel>
                                    <Select
                                        onValueChange={onTypeChange}
                                        value={field.value}
                                    >
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select proposal type" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            {PROPOSAL_TYPES.map((type) => (
                                                <SelectItem 
                                                    key={type.value} 
                                                    value={type.value}
                                                >
                                                    {type.label}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        {renderParameterFields()}

                        <DialogFooter>
                            <Button
                                type="button"
                                variant="outline"
                                onClick={onClose}
                                disabled={loading}
                            >
                                Cancel
                            </Button>
                            <Button 
                                type="submit"
                                disabled={loading}
                            >
                                {loading ? 'Creating...' : 'Create Proposal'}
                            </Button>
                        </DialogFooter>
                    </form>
                </Form>
            </DialogContent>
        </Dialog>
    );
};

export default CreateProposal;