from http.client import responses

from flask import Flask, jsonify, request
from Blockchain import Blockchain
from Block import Block
from uuid import uuid4

# Instantiate our node
app = Flask(__name__)

# Instantiate the blockchain
blockchain = Blockchain()

# Get the full chain
@app.route('/chain', methods=['GET'])
def full_chain():
    # Convert Block objects to JSON
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        })

    response = {
        'chain': chain_data,
        'length': len(blockchain.chain),
    }

# Register new nodes
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')