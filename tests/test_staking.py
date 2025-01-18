import pytest
from datetime import datetime, timedelta
from src.staking.staking_pool import StakingPool

@pytest.fixture
def staking_pool():
    return StakingPool(minimum_stake=100)

@pytest.fixture
def staker_address():
    return "0x1234567890abcdef"

def test_stake_tokens(staking_pool, staker_address):
    # Test staking with sufficient amount
    assert staking_pool.stake(staker_address, 200) == True
    staker_info = staking_pool.get_staker_info(staker_address)
    assert staker_info['total_stake'] == 200

    # Test staking with insufficient amount
    assert staking_pool.stake("0x2", 50) == False

def test_stake_with_lock_period(staking_pool, staker_address):
    # Test staking with different lock periods
    assert staking_pool.stake(staker_address, 200, lock_days=30) == True
    staker_info = staking_pool.get_staker_info(staker_address)
    stake = staker_info['stakes'][0]
    assert stake['bonus_multiplier'] == 1.2  # 20% bonus for 30-day lock

    # Test 90-day lock
    assert staking_pool.stake(staker_address, 300, lock_days=90) == True
    staker_info = staking_pool.get_staker_info(staker_address)
    stake = staker_info['stakes'][1]
    assert stake['bonus_multiplier'] == 1.5  # 50% bonus for 90-day lock

def test_unstake_tokens(staking_pool, staker_address):
    # Stake tokens first
    staking_pool.stake(staker_address, 200)
    
    # Test unstaking
    amount = staking_pool.unstake(staker_address, 100)
    assert amount >= 100  # Should include any rewards
    
    staker_info = staking_pool.get_staker_info(staker_address)
    assert staker_info['total_stake'] == 100

def test_unstake_locked_tokens(staking_pool, staker_address):
    # Stake tokens with lock period
    staking_pool.stake(staker_address, 200, lock_days=30)
    
    # Try to unstake before lock period ends
    amount = staking_pool.unstake(staker_address, 100)
    assert amount is None  # Should not be able to unstake locked tokens

def test_rewards_calculation(staking_pool, staker_address):
    # Stake tokens
    staking_pool.stake(staker_address, 1000)
    
    # Fast forward time simulation (would need to mock datetime)
    initial_info = staking_pool.get_staker_info(staker_address)
    # ... time passes ...
    final_info = staking_pool.get_staker_info(staker_address)
    
    assert final_info['total_rewards'] >= 0

def test_multiple_stakes(staking_pool, staker_address):
    # Test multiple stakes for same address
    staking_pool.stake(staker_address, 200)
    staking_pool.stake(staker_address, 300)
    staking_pool.stake(staker_address, 500)
    
    staker_info = staking_pool.get_staker_info(staker_address)
    assert len(staker_info['stakes']) == 3
    assert staker_info['total_stake'] == 1000

def test_claim_rewards(staking_pool, staker_address):
    # Stake tokens
    staking_pool.stake(staker_address, 1000)
    
    # Initially no rewards
    initial_rewards = staking_pool.claim_rewards(staker_address)
    assert initial_rewards is None or initial_rewards == 0
    
    # After some time, should have rewards
    # (would need to mock time passage)
    
def test_pool_stats(staking_pool):
    # Test empty pool stats
    stats = staking_pool.get_pool_stats()
    assert stats['total_staked'] == 0
    assert stats['total_stakers'] == 0
    
    # Add some stakes
    staking_pool.stake("0x1", 200)
    staking_pool.stake("0x2", 300)
    
    stats = staking_pool.get_pool_stats()
    assert stats['total_staked'] == 500
    assert stats['total_stakers'] == 2
    assert stats['minimum_stake'] == 100
    assert stats['annual_reward_rate'] == 0.05

def test_invalid_operations(staking_pool):
    # Test unstaking with invalid address
    assert staking_pool.unstake("0xnonexistent") is None
    
    # Test claiming rewards with invalid address
    assert staking_pool.claim_rewards("0xnonexistent") is None
    
    # Test getting info for invalid address
    assert staking_pool.get_staker_info("0xnonexistent") is None