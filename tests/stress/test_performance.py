import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src.blockchain.blockchain import Blockchain

@pytest.mark.performance
async def test_transaction_throughput():
    blockchain = Blockchain()
    total_transactions = 10000
    concurrent_users = 100

    async def send_transactions(user_id: int, num_tx: int):
        for i in range(num_tx):
            tx = await blockchain.create_transaction(
                f"user_{user_id}",
                f"recipient_{i}",
                1.0
            )
            assert tx is not None

    # Create multiple users sending transactions concurrently
    tasks = [
        send_transactions(i, total_transactions // concurrent_users)
        for i in range(concurrent_users)
    ]

    # Measure execution time
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()

    execution_time = end_time - start_time
    tps = total_transactions / execution_time

    assert tps >= 1000  # Minimum 1000 TPS requirement