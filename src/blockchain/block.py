from dataclasses import dataclass
from datetime import datetime
from typing import List
import hashlib

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[dict]
    previous_hash: str
    nonce: int = 0
    
    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> str:
        target = '0' * difficulty
        while True:
            hash_value = self.calculate_hash()
            if hash_value[:difficulty] == target:
                return hash_value
            self.nonce += 1