from typing import Dict, List, Optional
from decimal import Decimal
import time
import random

class ProofOfStake:
    def __init__(self):
        self.validators: Dict[str, Decimal] = {}
        self.validator_stakes: Dict[str, Decimal] = {}
        self.min_stake = Decimal('1000')

    def add_validator(self, address: str, stake: Decimal) -> bool:
        if stake < self.min_stake:
            return False
            
        if address in self.validators:
            self.validator_stakes[address] += stake
        else:
            self.validators[address] = stake
            self.validator_stakes[address] = stake
            
        return True

    def remove_validator(self, address: str) -> bool:
        if address not in self.validators:
            return False
            
        del self.validators[address]
        del self.validator_stakes[address]
        return True

    def get_next_validator(self) -> Optional[str]:
        if not self.validators:
            return None
            
        # Weight validators by stake
        total_stake = sum(self.validator_stakes.values())
        selection_pool = []
        
        for address, stake in self.validator_stakes.items():
            weight = int((stake / total_stake) * 100)
            selection_pool.extend([address] * weight)
            
        return random.choice(selection_pool) if selection_pool else None