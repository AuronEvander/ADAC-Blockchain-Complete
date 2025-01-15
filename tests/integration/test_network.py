import pytest
import asyncio
from src.blockchain.blockchain import Blockchain
from src.consensus.pos import ProofOfStake

@pytest.mark.asyncio
async def test_network_consensus():
    # Initialize network with multiple nodes
    nodes = await setup_test_network(3)
    blockchain = nodes[0].blockchain
    consensus = nodes[0].consensus

    # Add transactions and test propagation
    tx = await nodes[0].create_transaction("Alice", "Bob", 100)
    await asyncio.sleep(1)  # Wait for propagation

    # Verify all nodes have the transaction
    for node in nodes[1:]:
        assert tx in node.pending_transactions

    # Test block creation and validation
    block = await nodes[0].create_block()
    assert all(node.validate_block(block) for node in nodes)

@pytest.mark.asyncio
async def test_network_recovery():
    nodes = await setup_test_network(5)
    
    # Simulate node failure
    failed_node = nodes[0]
    await failed_node.stop()
    
    # Verify network continues operation
    tx = await nodes[1].create_transaction("Carol", "Dave", 50)
    await asyncio.sleep(1)
    
    # Restart node and verify sync
    await failed_node.start()
    await asyncio.sleep(2)
    assert tx in failed_node.blockchain.get_all_transactions()