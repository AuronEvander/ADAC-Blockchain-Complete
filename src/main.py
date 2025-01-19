from flask import Flask
from api.routes import blockchain_bp
from api.ai_routes import ai_bp
from blockchain.blockchain import Blockchain
from ai.ai_manager import AIManager

def create_app():
    app = Flask(__name__)

    # Initialize components
    blockchain = Blockchain()
    ai_manager = AIManager()

    # Register blueprints
    app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)