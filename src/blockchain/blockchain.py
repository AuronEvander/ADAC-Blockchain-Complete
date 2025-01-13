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
        """Calculate SHA-256 hash of the block's content"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Mine block with Proof of Work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = Decimal('10')  # 10 ADAC tokens

    def create_genesis_block(self) -> Block:
        """Create the genesis block"""
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self) -> Block:
        """Get the last block in the chain"""
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """Add a new block to the chain after mining"""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """Verify the blockchain's integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def add_transaction(self, sender: str, recipient: str, amount: Decimal) -> int:
        """Add a new transaction to pending transactions"""
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        })
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address: str) -> None:
        """Mine pending transactions and add them to a new block"""
        # Create reward transaction
        self.pending_transactions.append({
            'sender': "ADAC Network",
            'recipient': miner_address,
            'amount': self.mining_reward,
            'timestamp': time.time()
        })

        # Create new block with pending transactions
        block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            time.time(),
            self.pending_transactions
        )
        self.add_block(block)

        # Clear pending transactions
        self.pending_transactions = []

    def get_balance(self, address: str) -> Decimal:
        """Get the balance of an address"""
        balance = Decimal('0')
        for block in self.chain:
            if isinstance(block.data, list):
                for transaction in block.data:
                    if transaction['recipient'] == address:
                        balance += transaction['amount']
                    if transaction['sender'] == address:
                        balance -= transaction['amount']
        return balance