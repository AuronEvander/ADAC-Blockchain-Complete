from typing import Dict, List, Optional
from datetime import datetime, timedelta

class StakingPool:
    def __init__(self, minimum_stake: float = 100):
        self.minimum_stake = minimum_stake
        self.total_staked = 0
        self.stakers: Dict[str, Dict] = {}
        self.annual_reward_rate = 0.05  # 5% annual reward
        self.compound_frequency = 'daily'  # Rewards are compounded daily
        self.lock_periods = {
            30: 1.2,   # 30 days lock = 20% bonus
            90: 1.5,   # 90 days lock = 50% bonus
            180: 1.8,  # 180 days lock = 80% bonus
            365: 2.0   # 365 days lock = 100% bonus
        }

    def stake(self, address: str, amount: float, lock_days: int = 0) -> bool:
        """Stake tokens in the pool"""
        if amount < self.minimum_stake:
            return False

        # Calculate bonus multiplier based on lock period
        bonus_multiplier = 1.0
        if lock_days in self.lock_periods:
            bonus_multiplier = self.lock_periods[lock_days]

        current_time = datetime.now()
        unlock_time = current_time + timedelta(days=lock_days) if lock_days > 0 else None

        if address not in self.stakers:
            self.stakers[address] = {
                'total_stake': amount,
                'stakes': [{
                    'amount': amount,
                    'start_time': current_time,
                    'unlock_time': unlock_time,
                    'bonus_multiplier': bonus_multiplier,
                    'last_reward_calculation': current_time,
                    'accumulated_rewards': 0
                }]
            }
        else:
            self.stakers[address]['total_stake'] += amount
            self.stakers[address]['stakes'].append({
                'amount': amount,
                'start_time': current_time,
                'unlock_time': unlock_time,
                'bonus_multiplier': bonus_multiplier,
                'last_reward_calculation': current_time,
                'accumulated_rewards': 0
            })

        self.total_staked += amount
        return True

    def unstake(self, address: str, amount: float = None) -> Optional[float]:
        """Unstake tokens from the pool"""
        if address not in self.stakers:
            return None

        current_time = datetime.now()
        staker = self.stakers[address]
        
        # Calculate rewards before unstaking
        self._calculate_rewards(address)

        # If no amount specified, unstake everything that's unlocked
        if amount is None:
            unlocked_amount = 0
            rewards = 0
            new_stakes = []

            for stake in staker['stakes']:
                if stake['unlock_time'] is None or current_time >= stake['unlock_time']:
                    unlocked_amount += stake['amount']
                    rewards += stake['accumulated_rewards']
                else:
                    new_stakes.append(stake)

            if unlocked_amount == 0:
                return None

            self.total_staked -= unlocked_amount
            if new_stakes:
                staker['stakes'] = new_stakes
                staker['total_stake'] -= unlocked_amount
            else:
                del self.stakers[address]

            return unlocked_amount + rewards

        # Unstake specific amount
        remaining_amount = amount
        rewards = 0
        new_stakes = []

        for stake in sorted(staker['stakes'], key=lambda x: x['start_time']):
            if remaining_amount <= 0:
                new_stakes.append(stake)
                continue

            if stake['unlock_time'] is None or current_time >= stake['unlock_time']:
                if stake['amount'] <= remaining_amount:
                    remaining_amount -= stake['amount']
                    rewards += stake['accumulated_rewards']
                    self.total_staked -= stake['amount']
                else:
                    stake['amount'] -= remaining_amount
                    rewards += (remaining_amount / stake['amount']) * stake['accumulated_rewards']
                    stake['accumulated_rewards'] -= (remaining_amount / stake['amount']) * stake['accumulated_rewards']
                    self.total_staked -= remaining_amount
                    new_stakes.append(stake)
                    remaining_amount = 0
            else:
                new_stakes.append(stake)

        if remaining_amount == amount:
            return None

        unstaked_amount = amount - remaining_amount
        if new_stakes:
            staker['stakes'] = new_stakes
            staker['total_stake'] -= unstaked_amount
        else:
            del self.stakers[address]

        return unstaked_amount + rewards

    def _calculate_rewards(self, address: str) -> float:
        """Calculate rewards for a staker"""
        if address not in self.stakers:
            return 0

        current_time = datetime.now()
        staker = self.stakers[address]
        total_rewards = 0

        for stake in staker['stakes']:
            time_diff = (current_time - stake['last_reward_calculation']).total_seconds()
            if time_diff <= 0:
                continue

            # Calculate rewards based on annual rate, time period, and bonus multiplier
            reward = (stake['amount'] * self.annual_reward_rate * time_diff / (365 * 24 * 3600)) * stake['bonus_multiplier']
            stake['accumulated_rewards'] += reward
            stake['last_reward_calculation'] = current_time
            total_rewards += reward

        return total_rewards

    def get_staker_info(self, address: str) -> Optional[Dict]:
        """Get information about a staker"""
        if address not in self.stakers:
            return None

        self._calculate_rewards(address)
        staker = self.stakers[address]
        
        return {
            'address': address,
            'total_stake': staker['total_stake'],
            'stakes': [{
                'amount': stake['amount'],
                'start_time': stake['start_time'],
                'unlock_time': stake['unlock_time'],
                'accumulated_rewards': stake['accumulated_rewards'],
                'bonus_multiplier': stake['bonus_multiplier']
            } for stake in staker['stakes']],
            'total_rewards': sum(stake['accumulated_rewards'] for stake in staker['stakes'])
        }

    def get_pool_stats(self) -> Dict:
        """Get statistics about the staking pool"""
        return {
            'total_staked': self.total_staked,
            'total_stakers': len(self.stakers),
            'annual_reward_rate': self.annual_reward_rate,
            'minimum_stake': self.minimum_stake,
            'lock_periods': self.lock_periods
        }

    def claim_rewards(self, address: str) -> Optional[float]:
        """Claim accumulated rewards without unstaking"""
        if address not in self.stakers:
            return None

        self._calculate_rewards(address)
        staker = self.stakers[address]
        total_rewards = 0

        for stake in staker['stakes']:
            total_rewards += stake['accumulated_rewards']
            stake['accumulated_rewards'] = 0

        return total_rewards if total_rewards > 0 else None
