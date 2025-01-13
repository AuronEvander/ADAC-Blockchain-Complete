from decimal import Decimal
from typing import Dict, Optional
import time

class LiquidityPool:
    def __init__(self, token_a: str, token_b: str):
        self.token_a = token_a
        self.token_b = token_b
        self.reserve_a = Decimal('0')
        self.reserve_b = Decimal('0')
        self.total_shares = Decimal('0')
        self.shares: Dict[str, Decimal] = {}
        self.fee_percent = Decimal('0.003')  # 0.3% fee

    def add_liquidity(
        self,
        provider: str,
        amount_a: Decimal,
        amount_b: Decimal
    ) -> Optional[Decimal]:
        # Calculate shares
        if self.total_shares == 0:
            shares = amount_a
        else:
            shares = min(
                (amount_a * self.total_shares) / self.reserve_a,
                (amount_b * self.total_shares) / self.reserve_b
            )

        # Update reserves
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        self.total_shares += shares

        # Update provider shares
        if provider not in self.shares:
            self.shares[provider] = Decimal('0')
        self.shares[provider] += shares

        return shares