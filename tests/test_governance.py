import pytest
from datetime import datetime, timedelta
from src.governance.governance import Governance, ProposalType, ProposalStatus

@pytest.fixture
def governance():
    return Governance()

@pytest.fixture
def proposer_address():
    return "0x1234567890abcdef"

@pytest.fixture
def proposal_data():
    return {
        "title": "Test Proposal",
        "description": "A test proposal for unit testing",
        "proposal_type": ProposalType.PARAMETER_CHANGE,
        "parameters": {"staking_minimum": 200}
    }

def test_create_proposal(governance, proposer_address, proposal_data):
    # Test creating proposal with sufficient voting power
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    assert proposal_id is not None
    proposal = governance.get_proposal(proposal_id)
    assert proposal['title'] == proposal_data["title"]
    
    # Test creating proposal with insufficient voting power
    insufficient_proposal = governance.create_proposal(
        title="Insufficient Proposal",
        description="Should fail",
        proposer="0x2",
        proposal_type=ProposalType.PARAMETER_CHANGE,
        voting_power=50000
    )
    
    assert insufficient_proposal is None

def test_vote_on_proposal(governance, proposer_address, proposal_data):
    # Create a proposal first
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    # Activate the proposal
    governance.activate_proposal(proposal_id)
    
    # Test voting
    assert governance.vote(proposal_id, "0x1", "for", 10000) == True
    assert governance.vote(proposal_id, "0x2", "against", 5000) == True
    
    # Test voting with insufficient power
    assert governance.vote(proposal_id, "0x3", "for", 500) == False
    
    # Get proposal and verify votes
    proposal = governance.get_proposal(proposal_id)
    assert sum(proposal['votes_for'].values()) == 10000
    assert sum(proposal['votes_against'].values()) == 5000

def test_proposal_finalization(governance, proposer_address, proposal_data):
    # Create and activate proposal
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    governance.activate_proposal(proposal_id)
    
    # Add votes
    governance.vote(proposal_id, "0x1", "for", 500000)  # 50% of required votes
    governance.vote(proposal_id, "0x2", "against", 100000)
    
    # Finalize proposal
    assert governance.finalize_proposal(proposal_id) == True
    
    proposal = governance.get_proposal(proposal_id)
    assert proposal['status'] == ProposalStatus.PASSED.value

def test_proposal_execution(governance, proposer_address, proposal_data):
    # Create, activate, and pass a proposal
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    governance.activate_proposal(proposal_id)
    governance.vote(proposal_id, "0x1", "for", 500000)
    governance.finalize_proposal(proposal_id)
    
    # Execute proposal
    assert governance.execute_proposal(proposal_id) == True
    
    # Verify parameter change
    assert governance.protocol_parameters['staking_minimum'] == 200

def test_add_proposal_comment(governance, proposer_address, proposal_data):
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    # Add comment
    assert governance.add_comment(proposal_id, "0x1", "Test comment") == True
    
    proposal = governance.get_proposal(proposal_id)
    assert len(proposal['comments']) == 1
    assert proposal['comments'][0]['comment'] == "Test comment"

def test_update_proposal(governance, proposer_address, proposal_data):
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    # Update proposal by original proposer
    assert governance.update_proposal(proposal_id, proposer_address, "Updated parameters") == True
    
    # Try updating with wrong proposer
    assert governance.update_proposal(proposal_id, "0x2", "Should fail") == False
    
    proposal = governance.get_proposal(proposal_id)
    assert len(proposal['updates']) == 1
    assert proposal['updates'][0]['update'] == "Updated parameters"

def test_voter_info(governance, proposer_address, proposal_data):
    # Create multiple proposals and vote
    proposal_id1 = governance.create_proposal(
        title="Proposal 1",
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    proposal_id2 = governance.create_proposal(
        title="Proposal 2",
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    governance.activate_proposal(proposal_id1)
    governance.activate_proposal(proposal_id2)
    
    voter = "0x1"
    governance.vote(proposal_id1, voter, "for", 10000)
    governance.vote(proposal_id2, voter, "against", 15000)
    
    voter_info = governance.get_voter_info(voter)
    assert len(voter_info['voted_proposals']) == 2
    assert voter_info['total_voting_power_used'] == 25000
    assert voter_info['participation_rate'] == 1.0  # Voted on all proposals

def test_governance_stats(governance, proposer_address, proposal_data):
    # Create proposals and add votes
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    governance.activate_proposal(proposal_id)
    governance.vote(proposal_id, "0x1", "for", 10000)
    governance.vote(proposal_id, "0x2", "against", 5000)
    
    stats = governance.get_governance_stats()
    assert stats['total_proposals'] == 1
    assert stats['unique_voters'] == 2
    assert stats['total_votes'] == 2
    assert stats['average_votes_per_proposal'] == 2.0

def test_proposal_lifecycle(governance, proposer_address, proposal_data):
    # Test complete lifecycle of a proposal
    
    # 1. Create proposal
    proposal_id = governance.create_proposal(
        title=proposal_data["title"],
        description=proposal_data["description"],
        proposer=proposer_address,
        proposal_type=proposal_data["proposal_type"],
        parameters=proposal_data["parameters"],
        voting_power=200000
    )
    
    proposal = governance.get_proposal(proposal_id)
    assert proposal['status'] == ProposalStatus.PENDING.value
    
    # 2. Activate proposal
    governance.activate_proposal(proposal_id)
    proposal = governance.get_proposal(proposal_id)
    assert proposal['status'] == ProposalStatus.ACTIVE.value
    
    # 3. Vote on proposal
    governance.vote(proposal_id, "0x1", "for", 500000)
    governance.vote(proposal_id, "0x2", "against", 100000)
    
    # 4. Add comments
    governance.add_comment(proposal_id, "0x1", "Support comment")
    governance.add_comment(proposal_id, "0x2", "Opposition comment")
    
    # 5. Finalize proposal
    governance.finalize_proposal(proposal_id)
    proposal = governance.get_proposal(proposal_id)
    assert proposal['status'] == ProposalStatus.PASSED.value
    
    # 6. Execute proposal
    governance.execute_proposal(proposal_id)
    proposal = governance.get_proposal(proposal_id)
    assert proposal['status'] == ProposalStatus.EXECUTED.value
    
    # Verify final state
    assert len(proposal['comments']) == 2
    assert proposal['execution_time'] is not None
    assert proposal['execution_data'] is not None
