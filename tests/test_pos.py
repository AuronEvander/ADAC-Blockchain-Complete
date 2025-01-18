import pytest
from datetime import datetime, timedelta
from src.consensus.pos import ProofOfStake, Validator

@pytest.fixture
def pos():
    return ProofOfStake()

@pytest.fixture
def validator_address():
    return "0x1234567890abcdef"

def test_add_validator(pos, validator_address):
    # Test adding validator with sufficient stake
    assert pos.add_validator(validator_address, 2000) == True
    assert validator_address in pos.validators
    assert pos.validators[validator_address].stake == 2000

    # Test adding validator with insufficient stake
    assert pos.add_validator("0xinsufficient", 500) == False
    assert "0xinsufficient" not in pos.validators

def test_remove_validator(pos, validator_address):
    pos.add_validator(validator_address, 2000)
    assert pos.remove_validator(validator_address) == True
    assert validator_address not in pos.validators

    # Test removing non-existent validator
    assert pos.remove_validator("0xnonexistent") == False

def test_get_next_validator(pos):
    # Add multiple validators
    validators = [
        ("0x1", 2000),
        ("0x2", 3000),
        ("0x3", 4000)
    ]
    
    for addr, stake in validators:
        pos.add_validator(addr, stake)

    # Test validator selection
    selected = pos.get_next_validator()
    assert selected in [v[0] for v in validators]

def test_validate_block(pos, validator_address):
    pos.add_validator(validator_address, 2000)
    
    # Test successful validation
    assert pos.validate_block(validator_address, {"data": "test"}) == True
    
    # Test validation with non-existent validator
    assert pos.validate_block("0xnonexistent", {"data": "test"}) == False

def test_slash_validator(pos, validator_address):
    pos.add_validator(validator_address, 2000)
    
    # Test slashing
    initial_stake = pos.validators[validator_address].stake
    pos.slash_validator(validator_address, 10)  # 10% penalty
    assert pos.validators[validator_address].stake < initial_stake
    
    # Test slashing non-existent validator
    assert pos.slash_validator("0xnonexistent", 10) == False

def test_calculate_rewards(pos, validator_address):
    pos.add_validator(validator_address, 2000)
    
    # Test reward calculation
    reward = pos.calculate_rewards(validator_address, 100)  # 100 token block reward
    assert reward > 0
    assert reward <= 100  # Reward should not exceed block reward
    
    # Test reward calculation for non-existent validator
    assert pos.calculate_rewards("0xnonexistent", 100) == 0

def test_validator_reputation(pos, validator_address):
    pos.add_validator(validator_address, 2000)
    validator = pos.validators[validator_address]
    
    # Test initial reputation
    assert validator.reputation == 100
    
    # Test reputation update
    validator.update_reputation(-10)
    assert validator.reputation == 90
    
    # Test reputation bounds
    validator.update_reputation(-100)
    assert validator.reputation == 0  # Should not go below 0
    
    validator.update_reputation(200)
    assert validator.reputation == 100  # Should not exceed 100