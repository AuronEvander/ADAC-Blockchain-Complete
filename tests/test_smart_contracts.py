import pytest
from src.smart_contracts.token import Token

def test_token_creation():
    token = Token("Test Token", "TST")
    assert token.name == "Test Token"
    assert token.symbol == "TST"
    assert token.total_supply == 0

def test_token_minting():
    token = Token("Test Token", "TST")
    success = token.mint("address1", 1000)
    
    assert success
    assert token.total_supply == 1000
    assert token.balances["address1"] == 1000

def test_token_transfer():
    token = Token("Test Token", "TST")
    token.mint("address1", 1000)
    
    success = token.transfer("address1", "address2", 500)
    assert success
    assert token.balances["address1"] == 500
    assert token.balances["address2"] == 500

def test_insufficient_balance():
    token = Token("Test Token", "TST")
    token.mint("address1", 1000)
    
    success = token.transfer("address1", "address2", 1500)
    assert not success
    assert token.balances["address1"] == 1000
    assert "address2" not in token.balances