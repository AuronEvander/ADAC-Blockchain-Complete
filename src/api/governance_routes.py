from flask import Blueprint, request, jsonify
from ..governance.governance import Governance, ProposalType, ProposalStatus
from ..blockchain.blockchain import Blockchain
from typing import Dict

governance_bp = Blueprint('governance', __name__)
governance = Governance()
blockchain = Blockchain()

@governance_bp.route('/proposals', methods=['POST'])
def create_proposal():
    """Create a new governance proposal"""
    try:
        data = request.json
        required_fields = ['title', 'description', 'proposer', 'proposal_type']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Verify proposer has enough voting power
        proposer_balance = blockchain.get_balance(data['proposer'])
        if proposer_balance < governance.minimum_proposal_power:
            return jsonify({
                'error': 'Insufficient voting power to create proposal'
            }), 403

        # Create proposal
        proposal_id = governance.create_proposal(
            title=data['title'],
            description=data['description'],
            proposer=data['proposer'],
            proposal_type=ProposalType(data['proposal_type']),
            parameters=data.get('parameters'),
            voting_power=proposer_balance
        )

        if proposal_id is None:
            return jsonify({'error': 'Failed to create proposal'}), 400

        return jsonify({
            'message': 'Proposal created successfully',
            'proposal_id': proposal_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>/vote', methods=['POST'])
def vote_on_proposal(proposal_id: int):
    """Vote on an active proposal"""
    try:
        data = request.json
        required_fields = ['voter', 'vote']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Verify voter has enough voting power
        voter_balance = blockchain.get_balance(data['voter'])
        if voter_balance < governance.minimum_voting_power:
            return jsonify({
                'error': 'Insufficient voting power to vote'
            }), 403

        # Cast vote
        success = governance.vote(
            proposal_id=proposal_id,
            voter=data['voter'],
            vote=data['vote'],
            voting_power=voter_balance
        )

        if not success:
            return jsonify({'error': 'Failed to cast vote'}), 400

        return jsonify({
            'message': 'Vote cast successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id: int):
    """Get details of a specific proposal"""
    try:
        proposal = governance.get_proposal(proposal_id)
        if not proposal:
            return jsonify({'error': 'Proposal not found'}), 404

        return jsonify(proposal), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals', methods=['GET'])
def get_proposals():
    """Get all proposals with optional status filter"""
    try:
        status = request.args.get('status')
        if status:
            proposals = governance.get_all_proposals(ProposalStatus(status))
        else:
            proposals = governance.get_all_proposals()

        return jsonify(proposals), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>/comments', methods=['POST'])
def add_comment(proposal_id: int):
    """Add a comment to a proposal"""
    try:
        data = request.json
        required_fields = ['commenter', 'comment']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        success = governance.add_comment(
            proposal_id=proposal_id,
            commenter=data['commenter'],
            comment=data['comment']
        )

        if not success:
            return jsonify({'error': 'Failed to add comment'}), 400

        return jsonify({
            'message': 'Comment added successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>/update', methods=['POST'])
def update_proposal(proposal_id: int):
    """Update/amend a proposal"""
    try:
        data = request.json
        required_fields = ['proposer', 'update']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        success = governance.update_proposal(
            proposal_id=proposal_id,
            proposer=data['proposer'],
            update=data['update']
        )

        if not success:
            return jsonify({'error': 'Failed to update proposal'}), 400

        return jsonify({
            'message': 'Proposal updated successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/voters/<string:address>', methods=['GET'])
def get_voter_info(address: str):
    """Get voting history and statistics for a voter"""
    try:
        voter_info = governance.get_voter_info(address)
        return jsonify(voter_info), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get governance system statistics"""
    try:
        stats = governance.get_governance_stats()
        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>/execute', methods=['POST'])
def execute_proposal(proposal_id: int):
    """Execute a passed proposal"""
    try:
        success = governance.execute_proposal(proposal_id)
        if not success:
            return jsonify({'error': 'Failed to execute proposal'}), 400

        return jsonify({
            'message': 'Proposal executed successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@governance_bp.route('/proposals/<int:proposal_id>/finalize', methods=['POST'])
def finalize_proposal(proposal_id: int):
    """Finalize a proposal after voting period"""
    try:
        success = governance.finalize_proposal(proposal_id)
        if not success:
            return jsonify({'error': 'Failed to finalize proposal'}), 400

        return jsonify({
            'message': 'Proposal finalized successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
