from decimal import Decimal
from typing import Dict
import time

class Staking:
    def __init__(self):
        self.stakes: Dict[str, Dict] = {}
        self.reward_rate = Decimal('0.1')  # 10% APR

    def stake(self, address: str, amount: Decimal) -> bool:
        if address not in self.stakes:
            self.stakes[address] = {
                'amount': amount,
                'timestamp': time.time()
            }
        else:
            self.stakes[address]['amount'] += amount
            self.stakes[address]['timestamp'] = time.time()
        return True

    def calculate_rewards(self, address: str) -> Decimal:
        if address not in self.stakes:
            return Decimal('0')

        stake = self.stakes[address]
        time_staked = Decimal(str(time.time() - stake['timestamp']))
        return stake['amount'] * self.reward_rate * (time_staked / (365 * 24 * 3600))