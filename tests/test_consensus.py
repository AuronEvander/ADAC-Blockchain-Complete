import pytest
from datetime import datetime
from src.consensus.proof_of_stake import ProofOfStake

def test_validator_addition():
    pos = ProofOfStake()
    
    success = pos.add_validator("validator1", 2000)
    assert success
    assert "validator1" in pos.validators
    assert pos.validators["validator1"] == 2000
    
def test_insufficient_stake():
    pos = ProofOfStake()
    
    success = pos.add_validator("validator1", 500)  # Below threshold
    assert not success
    assert "validator1" not in pos.validators
    
def test_validator_selection():
    pos = ProofOfStake()
    pos.add_validator("validator1", 2000)
    pos.add_validator("validator2", 3000)
    
    selected = pos.get_validator()
    assert selected in ["validator1", "validator2"]
    
def test_block_validation():
    pos = ProofOfStake()
    pos.add_validator("validator1", 2000)
    
    block = {
        "index": 1,
        "timestamp": datetime.now().timestamp(),
        "transactions": []
    }
    
    is_valid = pos.validate_block(block, "validator1")
    assert is_valid