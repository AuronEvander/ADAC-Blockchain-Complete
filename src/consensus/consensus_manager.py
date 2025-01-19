from typing import List, Dict
from .proof_of_stake import ProofOfStake

class ConsensusManager:
    def __init__(self):
        self.pos = ProofOfStake()
        self.block_rewards = 100  # Reward for validating a block
        
    def handle_new_block(self, block: dict) -> bool:
        try:
            validator = self.pos.get_validator()
            if self.pos.validate_block(block, validator):
                # Reward the validator
                self.reward_validator(validator)
                return True
            return False
        except Exception as e:
            print(f"Error in consensus: {str(e)}")
            return False
    
    def reward_validator(self, validator: str) -> None:
        # Implement reward distribution logic
        current_stake = self.pos.validators.get(validator, 0)
        self.pos.validators[validator] = current_stake + self.block_rewards
    
    def add_validator(self, address: str, stake: float) -> bool:
        return self.pos.add_validator(address, stake)
    
    def get_total_stake(self) -> float:
        return sum(self.pos.validators.values())