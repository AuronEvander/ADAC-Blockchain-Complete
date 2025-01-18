from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class ProposalStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CANCELLED = "cancelled"

class ProposalType(Enum):
    PARAMETER_CHANGE = "parameter_change"
    FEATURE_REQUEST = "feature_request"
    TREASURY_SPENDING = "treasury_spending"
    PROTOCOL_UPGRADE = "protocol_upgrade"
    EMERGENCY_ACTION = "emergency_action"

class Proposal:
    def __init__(self, 
                 id: int,
                 title: str,
                 description: str,
                 proposer: str,
                 proposal_type: ProposalType,
                 parameters: Dict = None,
                 required_quorum: float = 0.4,  # 40% quorum required
                 voting_period_days: int = 7):
        self.id = id
        self.title = title
        self.description = description
        self.proposer = proposer
        self.proposal_type = proposal_type
        self.parameters = parameters or {}
        self.required_quorum = required_quorum
        self.creation_time = datetime.now()
        self.end_time = self.creation_time + timedelta(days=voting_period_days)
        self.status = ProposalStatus.PENDING
        self.votes_for = {}  # address -> voting power
        self.votes_against = {}  # address -> voting power
        self.votes_abstain = {}  # address -> voting power
        self.execution_time = None
        self.execution_data = None
        self.comments = []  # List of comments on the proposal
        self.updates = []  # List of updates/amendments to the proposal

    def to_dict(self) -> Dict:
        """Convert proposal to dictionary format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'proposer': self.proposer,
            'proposal_type': self.proposal_type.value,
            'parameters': self.parameters,
            'required_quorum': self.required_quorum,
            'creation_time': self.creation_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'status': self.status.value,
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'votes_abstain': self.votes_abstain,
            'execution_time': self.execution_time.isoformat() if self.execution_time else None,
            'execution_data': self.execution_data,
            'comments': self.comments,
            'updates': self.updates
        }

class Governance:
    def __init__(self):
        self.proposals: Dict[int, Proposal] = {}
        self.next_proposal_id = 1
        self.minimum_proposal_power = 100000  # Minimum voting power to create proposal
        self.minimum_voting_power = 1000  # Minimum voting power to vote
        self.execution_delay_hours = 24  # Delay before executing passed proposals
        self.voter_rewards_enabled = True
        self.voter_reward_rate = 0.001  # 0.1% reward for voting
        self.protocol_parameters = {
            'staking_minimum': 100,
            'reward_rate': 0.05,
            'transaction_fee': 0.001,
            'validator_minimum': 1000,
            'governance_quorum': 0.4
        }
        self.treasury_balance = 0
        self.proposal_fee = 1000  # Fee required to submit a proposal

    def create_proposal(self,
                       title: str,
                       description: str,
                       proposer: str,
                       proposal_type: ProposalType,
                       parameters: Dict = None,
                       voting_power: float = 0) -> Optional[int]:
        """Create a new governance proposal"""
        if voting_power < self.minimum_proposal_power:
            return None

        proposal = Proposal(
            id=self.next_proposal_id,
            title=title,
            description=description,
            proposer=proposer,
            proposal_type=proposal_type,
            parameters=parameters
        )

        self.proposals[self.next_proposal_id] = proposal
        self.next_proposal_id += 1
        return proposal.id

    def vote(self,
            proposal_id: int,
            voter: str,
            vote: str,
            voting_power: float) -> bool:
        """Cast a vote on a proposal"""
        if voting_power < self.minimum_voting_power:
            return False

        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.status != ProposalStatus.ACTIVE:
            return False

        if datetime.now() > proposal.end_time:
            return False

        # Remove any existing votes by this voter
        self._remove_existing_votes(proposal, voter)

        # Record the new vote
        if vote == "for":
            proposal.votes_for[voter] = voting_power
        elif vote == "against":
            proposal.votes_against[voter] = voting_power
        elif vote == "abstain":
            proposal.votes_abstain[voter] = voting_power
        else:
            return False

        # Calculate and distribute voter rewards if enabled
        if self.voter_rewards_enabled:
            self._distribute_voter_rewards(voter, voting_power)

        return True

    def _distribute_voter_rewards(self, voter: str, voting_power: float):
        """Distribute rewards to voters"""
        reward = voting_power * self.voter_reward_rate
        # Implementation would interact with token contract to mint rewards
        pass

    def _remove_existing_votes(self, proposal: Proposal, voter: str):
        """Remove any existing votes by a voter"""
        if voter in proposal.votes_for:
            del proposal.votes_for[voter]
        if voter in proposal.votes_against:
            del proposal.votes_against[voter]
        if voter in proposal.votes_abstain:
            del proposal.votes_abstain[voter]

    def add_comment(self, proposal_id: int, commenter: str, comment: str) -> bool:
        """Add a comment to a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return False

        proposal.comments.append({
            'commenter': commenter,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        })
        return True

    def update_proposal(self, proposal_id: int, proposer: str, update: str) -> bool:
        """Add an update/amendment to a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.proposer != proposer:
            return False

        proposal.updates.append({
            'update': update,
            'timestamp': datetime.now().isoformat()
        })
        return True

    def _execute_parameter_change(self, proposal: Proposal) -> bool:
        """Execute a parameter change proposal"""
        try:
            for param, value in proposal.parameters.items():
                if param in self.protocol_parameters:
                    self.protocol_parameters[param] = value
            proposal.execution_data = {
                'updated_parameters': self.protocol_parameters.copy(),
                'timestamp': datetime.now().isoformat()
            }
            return True
        except Exception as e:
            proposal.execution_data = {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return False

    def _execute_treasury_spending(self, proposal: Proposal) -> bool:
        """Execute a treasury spending proposal"""
        try:
            amount = proposal.parameters.get('amount', 0)
            recipient = proposal.parameters.get('recipient')
            
            if not recipient or amount <= 0 or amount > self.treasury_balance:
                return False
                
            self.treasury_balance -= amount
            proposal.execution_data = {
                'amount': amount,
                'recipient': recipient,
                'new_balance': self.treasury_balance,
                'timestamp': datetime.now().isoformat()
            }
            return True
        except Exception as e:
            proposal.execution_data = {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return False

    def _execute_protocol_upgrade(self, proposal: Proposal) -> bool:
        """Execute a protocol upgrade proposal"""
        try:
            upgrade_data = proposal.parameters.get('upgrade_data', {})
            # Implementation would handle protocol upgrade logic
            proposal.execution_data = {
                'upgrade_data': upgrade_data,
                'timestamp': datetime.now().isoformat()
            }
            return True
        except Exception as e:
            proposal.execution_data = {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return False

    def get_proposal(self, proposal_id: int) -> Optional[Dict]:
        """Get proposal information"""
        proposal = self.proposals.get(proposal_id)
        return proposal.to_dict() if proposal else None

    def get_all_proposals(self, status: ProposalStatus = None) -> List[Dict]:
        """Get all proposals, optionally filtered by status"""
        if status:
            return [p.to_dict() for p in self.proposals.values() if p.status == status]
        return [p.to_dict() for p in self.proposals.values()]

    def get_voter_info(self, voter: str) -> Dict:
        """Get information about a voter's participation"""
        voted_proposals = []
        total_voting_power_used = 0

        for proposal in self.proposals.values():
            if (voter in proposal.votes_for or 
                voter in proposal.votes_against or 
                voter in proposal.votes_abstain):
                
                voting_power = (proposal.votes_for.get(voter, 0) or 
                              proposal.votes_against.get(voter, 0) or 
                              proposal.votes_abstain.get(voter, 0))
                
                voted_proposals.append({
                    'proposal_id': proposal.id,
                    'voting_power': voting_power,
                    'vote_type': self._get_vote_type(proposal, voter)
                })
                total_voting_power_used += voting_power

        return {
            'address': voter,
            'voted_proposals': voted_proposals,
            'total_voting_power_used': total_voting_power_used,
            'participation_rate': len(voted_proposals) / len(self.proposals) if self.proposals else 0
        }

    def _get_vote_type(self, proposal: Proposal, voter: str) -> str:
        """Get the type of vote cast by a voter"""
        if voter in proposal.votes_for:
            return "for"
        elif voter in proposal.votes_against:
            return "against"
        elif voter in proposal.votes_abstain:
            return "abstain"
        return None

    def get_governance_stats(self) -> Dict:
        """Get statistics about the governance system"""
        total_proposals = len(self.proposals)
        executed_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.EXECUTED])
        unique_voters = set()
        total_votes = 0

        for proposal in self.proposals.values():
            unique_voters.update(proposal.votes_for.keys())
            unique_voters.update(proposal.votes_against.keys())
            unique_voters.update(proposal.votes_abstain.keys())
            total_votes += len(proposal.votes_for) + len(proposal.votes_against) + len(proposal.votes_abstain)

        return {
            'total_proposals': total_proposals,
            'executed_proposals': executed_proposals,
            'unique_voters': len(unique_voters),
            'total_votes': total_votes,
            'average_votes_per_proposal': total_votes / total_proposals if total_proposals > 0 else 0,
            'treasury_balance': self.treasury_balance,
            'protocol_parameters': self.protocol_parameters
        }
