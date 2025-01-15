import pytest
from datetime import datetime
from src.blockchain.blockchain import Blockchain
from src.blockchain.block import Block

@pytest.fixture
def blockchain():
    return Blockchain()

def test_genesis_block(blockchain):
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].previous_hash == "0"

def test_add_block(blockchain):
    blockchain.add_transaction("address1", "address2", 100)
    blockchain.mine_pending_transactions("miner-address")
    assert len(blockchain.chain) == 2

def test_blockchain_validity(blockchain):
    blockchain.add_transaction("address1", "address2", 100)
    blockchain.mine_pending_transactions("miner-address")
    assert blockchain.is_chain_valid() == True

def test_get_balance(blockchain):
    blockchain.add_transaction("address1", "address2", 100)
    blockchain.mine_pending_transactions("miner-address")
    assert blockchain.get_balance("address1") == -100
    assert blockchain.get_balance("address2") == 100