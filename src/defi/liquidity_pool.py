from typing import Dict, Tuple
from decimal import Decimal
from datetime import datetime

class LiquidityPool:
    def __init__(self, token_a: str, token_b: str):
        self.token_a = token_a
        self.token_b = token_b
        self.reserve_a = Decimal(0)
        self.reserve_b = Decimal(0)
        self.total_shares = Decimal(0)
        self.shares: Dict[str, Decimal] = {}
        self.fee_percent = Decimal('0.003')  # 0.3% fee
        
    def add_liquidity(self, provider: str, amount_a: Decimal, amount_b: Decimal) -> bool:
        if self.total_shares == 0:
            # Initial liquidity provision
            shares = Decimal('100')
        else:
            # Calculate shares based on proportion of current reserves
            shares = min(
                amount_a * self.total_shares / self.reserve_a,
                amount_b * self.total_shares / self.reserve_b
            )
            
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        self.total_shares += shares
        self.shares[provider] = self.shares.get(provider, Decimal(0)) + shares
        
        return True
        
    def remove_liquidity(self, provider: str, shares: Decimal) -> Tuple[Decimal, Decimal]:
        if shares > self.shares.get(provider, Decimal(0)):
            return (Decimal(0), Decimal(0))
            
        amount_a = shares * self.reserve_a / self.total_shares
        amount_b = shares * self.reserve_b / self.total_shares
        
        self.reserve_a -= amount_a
        self.reserve_b -= amount_b
        self.total_shares -= shares
        self.shares[provider] -= shares
        
        return (amount_a, amount_b)
        
    def swap(self, amount_in: Decimal, token_in: str) -> Decimal:
        if token_in not in [self.token_a, self.token_b]:
            return Decimal(0)
            
        fee = amount_in * self.fee_percent
        amount_in_with_fee = amount_in - fee
        
        if token_in == self.token_a:
            numerator = amount_in_with_fee * self.reserve_b
            denominator = self.reserve_a + amount_in_with_fee
            amount_out = numerator / denominator
            self.reserve_a += amount_in
            self.reserve_b -= amount_out
        else:
            numerator = amount_in_with_fee * self.reserve_a
            denominator = self.reserve_b + amount_in_with_fee
            amount_out = numerator / denominator
            self.reserve_b += amount_in
            self.reserve_a -= amount_out
            
        return amount_out