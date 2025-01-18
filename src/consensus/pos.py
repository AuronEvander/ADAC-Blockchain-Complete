import random
from typing import List, Dict
from datetime import datetime

class Validator:
    def __init__(self, address: str, stake: float = 0):
        self.address = address
        self.stake = stake
        self.is_active = True
        self.last_block_time = None
        self.reputation = 100  # Reputation score out of 100

    def add_stake(self, amount: float) -> None:
        """Add stake to the validator"""
        self.stake += amount

    def remove_stake(self, amount: float) -> bool:
        """Remove stake from the validator"""
        if amount <= self.stake:
            self.stake -= amount
            return True
        return False

    def update_reputation(self, performance: int) -> None:
        """Update validator reputation based on performance"""
        self.reputation = max(0, min(100, self.reputation + performance))

class ProofOfStake:
    def __init__(self):
        self.validators: Dict[str, Validator] = {}
        self.minimum_stake = 1000  # Minimum stake required to become a validator
        self.total_stake = 0
        self.last_block_validators: List[str] = []  # Track recent block validators

    def add_validator(self, address: str, stake: float) -> bool:
        """Add a new validator if they meet the minimum stake requirement"""
        if stake >= self.minimum_stake:
            if address not in self.validators:
                self.validators[address] = Validator(address, stake)
            else:
                self.validators[address].add_stake(stake)
            self.total_stake += stake
            return True
        return False

    def remove_validator(self, address: str) -> bool:
        """Remove a validator and their stake"""
        if address in self.validators:
            self.total_stake -= self.validators[address].stake
            del self.validators[address]
            return True
        return False

    def get_next_validator(self) -> str:
        """Select the next validator based on stake weight and reputation"""
        active_validators = {
            addr: val for addr, val in self.validators.items()
            if val.is_active and val.reputation > 50 and addr not in self.last_block_validators[-3:]
        }

        if not active_validators:
            return None

        # Calculate weighted probabilities based on stake and reputation
        weights = {}
        total_weight = 0
        
        for addr, validator in active_validators.items():
            weight = validator.stake * (validator.reputation / 100)
            weights[addr] = weight
            total_weight += weight

        # Random selection based on weights
        selection_point = random.uniform(0, total_weight)
        current_sum = 0

        for addr, weight in weights.items():
            current_sum += weight
            if current_sum >= selection_point:
                self.last_block_validators.append(addr)
                if len(self.last_block_validators) > 10:  # Keep only last 10 validators
                    self.last_block_validators.pop(0)
                return addr

        return None

    def validate_block(self, validator_address: str, block_data: dict) -> bool:
        """Validate a block and update validator reputation"""
        validator = self.validators.get(validator_address)
        if not validator:
            return False

        # Update last block time
        current_time = datetime.now()
        if validator.last_block_time:
            time_diff = (current_time - validator.last_block_time).total_seconds()
            if time_diff < 30:  # Minimum 30 seconds between blocks
                return False

        validator.last_block_time = current_time

        # TODO: Add actual block validation logic here
        is_valid = True  # Placeholder for actual validation

        # Update validator reputation based on validation
        if is_valid:
            validator.update_reputation(1)
        else:
            validator.update_reputation(-5)

        return is_valid

    def slash_validator(self, address: str, penalty: float) -> bool:
        """Slash a validator's stake for malicious behavior"""
        validator = self.validators.get(address)
        if validator:
            slashed_amount = validator.stake * (penalty / 100)
            validator.remove_stake(slashed_amount)
            validator.update_reputation(-20)
            return True
        return False

    def calculate_rewards(self, validator_address: str, block_reward: float) -> float:
        """Calculate rewards for a validator based on stake and reputation"""
        validator = self.validators.get(validator_address)
        if not validator:
            return 0

        # Base reward adjusted by reputation
        reward = block_reward * (validator.reputation / 100)
        
        # Stake weight bonus
        stake_weight = validator.stake / self.total_stake
        reward *= (1 + stake_weight)

        return reward
