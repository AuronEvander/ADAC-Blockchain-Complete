from datetime import datetime
from typing import List, Dict, Optional
from .block import Block
from ..consensus.pos import ProofOfStake, Validator

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.pos = ProofOfStake()
        self.block_reward = 100
        self.minimum_transaction_fee = 0.001
        
    def create_genesis_block(self) -> Block:
        """Create the genesis block"""
        return Block(datetime.now(), [], "0")

    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]

    def add_validator(self, address: str, stake: float) -> bool:
        """Add a new validator to the PoS system"""
        return self.pos.add_validator(address, stake)

    def remove_validator(self, address: str) -> bool:
        """Remove a validator from the PoS system"""
        return self.pos.remove_validator(address)

    def process_block(self, validator_address: str) -> Optional[Block]:
        """Process pending transactions and create a new block"""
        if not self.pending_transactions:
            return None

        # Get the next validator
        if validator_address != self.pos.get_next_validator():
            return None

        # Create new block
        new_block = Block(
            datetime.now(),
            self.pending_transactions,
            self.get_latest_block().hash
        )

        # Validate the block
        if not self.pos.validate_block(validator_address, new_block.__dict__):
            return None

        # Calculate and add validator reward
        reward = self.pos.calculate_rewards(validator_address, self.block_reward)
        reward_tx = {
            "from": "network",
            "to": validator_address,
            "amount": reward,
            "type": "reward"
        }
        new_block.transactions.append(reward_tx)

        # Add block to chain
        self.chain.append(new_block)
        self.pending_transactions = []

        return new_block

    def add_transaction(self, sender: str, recipient: str, amount: float, fee: float = None) -> bool:
        """Add a new transaction to pending transactions"""
        if fee is None:
            fee = self.minimum_transaction_fee

        if fee < self.minimum_transaction_fee:
            return False

        if self.get_balance(sender) < amount + fee:
            return False

        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount,
            "fee": fee,
            "timestamp": datetime.now().isoformat()
        })

        return True

    def get_balance(self, address: str) -> float:
        """Get the balance of an address"""
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["from"] == address:
                    balance -= transaction["amount"]
                    if "fee" in transaction:
                        balance -= transaction["fee"]
                if transaction["to"] == address:
                    balance += transaction["amount"]
        return balance

    def get_validator_info(self, address: str) -> Optional[Dict]:
        """Get information about a validator"""
        validator = self.pos.validators.get(address)
        if validator:
            return {
                "address": validator.address,
                "stake": validator.stake,
                "is_active": validator.is_active,
                "reputation": validator.reputation,
                "last_block_time": validator.last_block_time
            }
        return None

    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify block link
            if current_block.previous_hash != previous_block.hash:
                return False

            # Verify transactions in block
            for tx in current_block.transactions:
                if tx["from"] != "network":  # Skip reward transactions
                    sender_balance = self.get_balance(tx["from"])
                    if sender_balance < tx["amount"]:
                        return False

        return True

    def get_blockchain_stats(self) -> Dict:
        """Get statistical information about the blockchain"""
        return {
            "total_blocks": len(self.chain),
            "total_transactions": sum(len(block.transactions) for block in self.chain),
            "total_validators": len(self.pos.validators),
            "total_stake": self.pos.total_stake,
            "average_block_time": self._calculate_average_block_time()
        }

    def _calculate_average_block_time(self) -> float:
        """Calculate the average time between blocks"""
        if len(self.chain) < 2:
            return 0

        total_time = 0
        for i in range(1, len(self.chain)):
            time_diff = (self.chain[i].timestamp - self.chain[i-1].timestamp).total_seconds()
            total_time += time_diff

        return total_time / (len(self.chain) - 1)
