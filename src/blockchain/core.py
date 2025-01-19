import hashlib
from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models import Block, Transaction

class BlockchainCore:
    def __init__(self, db: Session, difficulty: int = 4):
        self.db = db
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        
    def create_block(self, miner_address: str) -> Block:
        """Create a new block with pending transactions"""
        last_block = self.db.query(Block).order_by(Block.id.desc()).first()
        
        # Create the new block
        new_block = Block(
            previous_hash=last_block.hash if last_block else '0' * 64,
            timestamp=datetime.now(UTC),
            nonce=0,
            difficulty=self.difficulty
        )
        
        # Add mining reward transaction
        reward_tx = Transaction(
            hash=self._generate_hash(f"reward_{datetime.now(UTC)}"),
            from_address='0' * 40,  # System address
            to_address=miner_address,
            amount=50.0  # Mining reward
        )
        
        # Add transactions to block
        block_transactions = [reward_tx] + self.pending_transactions
        transaction_str = ''.join(tx.hash for tx in block_transactions)
        
        # Mine the block
        target = '0' * self.difficulty
        while True:
            block_string = f"{new_block.previous_hash}{transaction_str}{new_block.timestamp}{new_block.nonce}"
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
            
            if block_hash.startswith(target):
                new_block.hash = block_hash
                break
                
            new_block.nonce += 1
        
        # Assign transactions to block
        new_block.transactions = block_transactions
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return new_block
    
    def add_transaction(self, from_address: str, to_address: str, amount: float) -> str:
        """Add a new transaction to pending transactions"""
        transaction = Transaction(
            hash=self._generate_hash(f"{from_address}{to_address}{amount}{datetime.now(UTC)}"),
            from_address=from_address,
            to_address=to_address,
            amount=amount
        )
        
        self.pending_transactions.append(transaction)
        return transaction.hash
    
    def validate_block(self, block: Block) -> bool:
        """Validate a block's hash and transactions"""
        # Check difficulty
        if not block.hash.startswith('0' * self.difficulty):
            return False
            
        # Verify block hash
        transaction_str = ''.join(tx.hash for tx in block.transactions)
        block_string = f"{block.previous_hash}{transaction_str}{block.timestamp}{block.nonce}"
        calculated_hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        if calculated_hash != block.hash:
            return False
            
        # Verify previous block hash
        previous_block = self.db.query(Block).filter(Block.hash == block.previous_hash).first()
        if not previous_block and block.previous_hash != '0' * 64:  # Allow genesis block
            return False
            
        return True
    
    @staticmethod
    def _generate_hash(data: str) -> str:
        """Generate a hash for the given data"""
        return hashlib.sha256(data.encode()).hexdigest()