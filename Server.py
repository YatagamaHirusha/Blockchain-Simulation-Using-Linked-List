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
    return jsonify(response), 200


# --- API ROUTE 2: MINE A NEW BLOCK ---
@app.route('/mine', methods=['GET'])
def mine():
    # 1. We run the mining algorithm
    # In a real app, you'd take transactions from pending_transactions
    # For now, let's just mine a block with some dummy data

    last_block = blockchain.get_latest_block()
    # Create a new block (using your existing logic)
    # We add a transaction giving us 1 coin reward
    blockchain.add_block(f"Block Mined! Reward to {node_identifier}")

    new_block = blockchain.get_latest_block()

    response = {
        'message': "New Block Forged",
        'index': new_block.index,
        'hash': new_block.hash,
        'data': new_block.data,
    }
    return jsonify(response), 200

# Register new nodes
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# --- API ROUTE 4: CONSENSUS (SYNC) ---
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain # Note: You might need to serialize this like in /chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    # We run on port 5000
    app.run(host='0.0.0.0', port=5000)