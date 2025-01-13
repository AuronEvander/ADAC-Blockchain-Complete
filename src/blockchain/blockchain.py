import hashlib
import time
from typing import List, Dict, Any
from decimal import Decimal

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: Any, nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = Decimal('10')

    def create_genesis_block(self) -> Block:
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self) -> Block:
        return self.chain[-1]