// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./AdacToken.sol";

contract AdacGovernance {
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    AdacToken public token;
    uint256 public proposalCount;
    uint256 public votingPeriod = 3 days;
    uint256 public proposalThreshold = 100_000 * 10**18; // 100k tokens to propose
    
    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 proposalId, address proposer, string description);
    event Voted(uint256 proposalId, address voter, bool support);
    event ProposalExecuted(uint256 proposalId);

    constructor(address _token) {
        token = AdacToken(_token);
    }

    function propose(string calldata description) external returns (uint256) {
        require(
            token.balanceOf(msg.sender) >= proposalThreshold,
            "AdacGovernance: insufficient balance to propose"
        );

        proposalCount++;
        Proposal storage proposal = proposals[proposalCount];
        proposal.id = proposalCount;
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;

        emit ProposalCreated(proposalCount, msg.sender, description);
        return proposalCount;
    }

    function castVote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp <= proposal.endTime, "AdacGovernance: voting is closed");
        require(!proposal.hasVoted[msg.sender], "AdacGovernance: already voted");

        uint256 votes = token.balanceOf(msg.sender);
        require(votes > 0, "AdacGovernance: no voting power");

        proposal.hasVoted[msg.sender] = true;

        if (support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }

        emit Voted(proposalId, msg.sender, support);
    }

    function execute(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp > proposal.endTime, "AdacGovernance: voting is still open");
        require(!proposal.executed, "AdacGovernance: proposal already executed");

        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }

    function getProposal(uint256 proposalId) external view returns (
        uint256 id,
        address proposer,
        string memory description,
        uint256 forVotes,
        uint256 againstVotes,
        uint256 startTime,
        uint256 endTime,
        bool executed
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.id,
            proposal.proposer,
            proposal.description,
            proposal.forVotes,
            proposal.againstVotes,
            proposal.startTime,
            proposal.endTime,
            proposal.executed
        );
    }
}