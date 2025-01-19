from typing import List
from .block import Block
from datetime import datetime

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        
    def create_genesis_block(self) -> Block:
        return Block(
            index=0,
            timestamp=datetime.now().timestamp(),
            transactions=[],
            previous_hash="0" * 64
        )
        
    def get_latest_block(self) -> Block:
        return self.chain[-1]
        
    def add_block(self, block: Block) -> bool:
        if self.is_valid_block(block):
            self.chain.append(block)
            return True
        return False
        
    def is_valid_block(self, block: Block) -> bool:
        previous_block = self.get_latest_block()
        if block.index != previous_block.index + 1:
            return False
        if block.previous_hash != previous_block.calculate_hash():
            return False
        if block.calculate_hash()[:self.difficulty] != '0' * self.difficulty:
            return False
        return True

    def add_transaction(self, transaction: dict) -> int:
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1