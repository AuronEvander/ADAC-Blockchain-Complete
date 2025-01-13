import pytest
from decimal import Decimal
from src.blockchain.blockchain import Blockchain, Block
import time

def test_genesis_block():
    blockchain = Blockchain()
    genesis = blockchain.chain[0]
    assert genesis.index == 0
    assert genesis.previous_hash == "0"
    assert genesis.data == "Genesis Block"

def test_add_block():
    blockchain = Blockchain(difficulty=2)
    blockchain.add_block(Block(1, "", time.time(), "Test Block"))
    assert len(blockchain.chain) == 2
    assert blockchain.chain[-1].data == "Test Block"

def test_chain_validity():
    blockchain = Blockchain(difficulty=2)
    blockchain.add_block(Block(1, "", time.time(), "Test Block"))
    assert blockchain.is_chain_valid() == True

@pytest.mark.asyncio
async def test_transaction():
    blockchain = Blockchain(difficulty=2)
    sender = "Alice"
    recipient = "Bob"
    amount = Decimal("50")
    
    tx_hash = blockchain.add_transaction(sender, recipient, amount)
    assert tx_hash is not None
    
    blockchain.mine_pending_transactions("miner")
    
    assert blockchain.get_balance(recipient) == amount
    assert blockchain.get_balance("miner") == blockchain.mining_reward