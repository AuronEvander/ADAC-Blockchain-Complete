from typing import Dict, List
from datetime import datetime, timedelta

class Proposal:
    def __init__(self, id: str, description: str, options: List[str], creator: str,
                 voting_period: int = 7*24*3600):  # 7 days in seconds
        self.id = id
        self.description = description
        self.options = options
        self.creator = creator
        self.votes: Dict[str, str] = {}
        self.start_time = datetime.now().timestamp()
        self.end_time = self.start_time + voting_period
        self.executed = False
        
    def is_active(self) -> bool:
        current_time = datetime.now().timestamp()
        return current_time <= self.end_time and not self.executed

class DAO:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.token_holdings: Dict[str, float] = {}
        self.proposal_threshold = 1000.0  # Minimum tokens to create proposal
        self.execution_threshold = 0.5  # 50% of total tokens needed
        
    def create_proposal(self, creator: str, description: str, 
                        options: List[str]) -> str:
        if self.token_holdings.get(creator, 0) < self.proposal_threshold:
            return ''
            
        proposal_id = f"PROP_{len(self.proposals) + 1}"
        self.proposals[proposal_id] = Proposal(
            proposal_id, description, options, creator
        )
        return proposal_id
        
    def vote(self, voter: str, proposal_id: str, option: str) -> bool:
        if proposal_id not in self.proposals:
            return False
            
        proposal = self.proposals[proposal_id]
        if not proposal.is_active():
            return False
            
        if option not in proposal.options:
            return False
            
        voting_power = self.token_holdings.get(voter, 0)
        if voting_power == 0:
            return False
            
        proposal.votes[voter] = option
        return True
        
    def execute_proposal(self, proposal_id: str) -> bool:
        if proposal_id not in self.proposals:
            return False
            
        proposal = self.proposals[proposal_id]
        if proposal.executed or proposal.is_active():
            return False
            
        total_votes = sum(self.token_holdings.get(voter, 0) 
                         for voter in proposal.votes.keys())
        total_tokens = sum(self.token_holdings.values())
        
        if total_votes < total_tokens * self.execution_threshold:
            return False
            
        # Count votes weighted by token holdings
        vote_results = {}
        for option in proposal.options:
            vote_results[option] = sum(
                self.token_holdings.get(voter, 0)
                for voter, vote in proposal.votes.items()
                if vote == option
            )
            
        # Find winning option
        winning_option = max(vote_results.items(), key=lambda x: x[1])[0]
        
        proposal.executed = True
        return True