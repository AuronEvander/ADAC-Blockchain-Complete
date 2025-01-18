from flask import Flask
from api.routes import blockchain_bp
from api.governance_routes import governance_bp
from blockchain.blockchain import Blockchain
from consensus.pos import ProofOfStake
from staking.staking_pool import StakingPool
from governance.governance import Governance

def create_app():
    app = Flask(__name__)

    # Initialize components
    blockchain = Blockchain()
    pos = ProofOfStake()
    staking_pool = StakingPool()
    governance = Governance()

    # Register blueprints
    app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
    app.register_blueprint(governance_bp, url_prefix='/api/governance')

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
