from flask import Flask, jsonify
from flask_cors import CORS
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash,
            'previous_hash': block.previous_hash
        })
    return jsonify({
        'chain': chain_data,
        'length': len(chain_data)
    }), 200

if __name__ == '__main__':
    blockchain.create_genesis_block()
    app.run(host='0.0.0.0', port=5001, debug=True)