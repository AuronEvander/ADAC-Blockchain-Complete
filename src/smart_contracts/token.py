from typing import Dict, List
import hashlib
from datetime import datetime

class Token:
    def __init__(self, name: str, symbol: str, decimals: int = 18):
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.total_supply = 0
        self.balances: Dict[str, int] = {}
        self.allowances: Dict[str, Dict[str, int]] = {}
        
    def mint(self, to: str, amount: int) -> bool:
        if amount <= 0:
            return False
            
        self.balances[to] = self.balances.get(to, 0) + amount
        self.total_supply += amount
        return True
        
    def transfer(self, from_addr: str, to: str, amount: int) -> bool:
        if amount <= 0 or self.balances.get(from_addr, 0) < amount:
            return False
            
        self.balances[from_addr] -= amount
        self.balances[to] = self.balances.get(to, 0) + amount
        return True
        
    def approve(self, owner: str, spender: str, amount: int) -> bool:
        if owner not in self.allowances:
            self.allowances[owner] = {}
        self.allowances[owner][spender] = amount
        return True
        
    def transfer_from(self, spender: str, from_addr: str, to: str, amount: int) -> bool:
        allowed = self.allowances.get(from_addr, {}).get(spender, 0)
        if amount > allowed:
            return False
        if not self.transfer(from_addr, to, amount):
            return False
            
        self.allowances[from_addr][spender] -= amount
        return True