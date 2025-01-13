import pytest
from src.smart_contracts.contract import SmartContract

def test_contract_creation():
    owner = "Alice"
    code = "test_code"
    initial_state = {"value": 0}
    
    contract = SmartContract(owner, code, initial_state)
    assert contract.owner == owner
    assert contract.code == code
    assert contract.state == initial_state

def test_contract_execution():
    contract = SmartContract(
        "Alice",
        "test_code",
        {"value": 0}
    )
    
    result = contract.execute(
        "update_state",
        {"value": 42},
        "Alice"
    )
    assert result["success"] == True
    assert contract.state["value"] == 42

def test_unauthorized_execution():
    contract = SmartContract(
        "Alice",
        "test_code",
        {"value": 0}
    )
    
    result = contract.execute(
        "owner_only",
        {"value": 42},
        "Bob"
    )
    assert result["success"] == False