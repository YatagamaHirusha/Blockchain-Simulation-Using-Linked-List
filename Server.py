from http.client import responses

from flask import Flask, jsonify, request

from Block import Block
from uuid import uuid4

from flask import Flask, jsonify, request, render_template # <--- Add render_template

from Blockchain import Blockchain

# Instantiate our node
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
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


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check if data exists
    if not values or 'data' not in values:
        return 'Missing values', 400

    # Add to the Blockchain's Mempool (Queue)
    index = blockchain.add_transactions(values['data'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# --- API ROUTE 2: MINE A NEW BLOCK ---
# @app.route('/mine', methods=['GET'])
# def mine():
#     # Since we don't have transactions, we just use a simple string as data.
#     # We include 'node_identifier' so we can see WHICH node created this block.
#     data = f"Block Mined by Node {node_identifier}"
#
#     # Use your existing function!
#     blockchain.add_block(data)
#
#     # Get the new block to show the user
#     new_block = blockchain.get_latest_block()
#
#     response = {
#         'message': "New Block Forged",
#         'index': new_block.index,
#         'data': new_block.data,
#         'hash': new_block.hash,
#         'previous_hash': new_block.previous_hash,
#     }
#     return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # Attempt to mine the pending transactions
    mined_block = blockchain.mine_pending_transactions()

    if not mined_block:
        return jsonify({'message': "No transactions to mine! Add data first."}), 400

    response = {
        'message': "New Block Forged",
        'index': mined_block.index,
        'data': mined_block.data,
        'hash': mined_block.hash,
        'previous_hash': mined_block.previous_hash,
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

# # --- API ROUTE 4: CONSENSUS (SYNC) ---
# @app.route('/nodes/resolve', methods=['GET'])
# def consensus():
#     replaced = blockchain.resolve_conflicts()
#
#     if replaced:
#         response = {
#             'message': 'Our chain was replaced',
#             'new_chain': blockchain.chain
#         }
#     else:
#         response = {
#             'message': 'Our chain is authoritative',
#             'chain': blockchain.chain # Note: You might need to serialize this like in /chain
#         }
#     return jsonify(response), 200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    # --- FIX START ---
    # We must convert the Block OBJECTS into simple DICTIONARIES
    # so Flask can turn them into JSON text.
    serialized_chain = []
    for block in blockchain.chain:
        # We check if it is an Object (has a __dict__) or already a Dictionary
        if hasattr(block, '__dict__'):
             # Manually map the fields you want to show
            serialized_chain.append({
                'index': block.index,
                'timestamp': block.timestamp,
                'data': block.data,
                'hash': block.hash,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce
            })
        else:
            # If it's already a dictionary (from a sync), just add it
            serialized_chain.append(block)
    # --- FIX END ---

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': serialized_chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': serialized_chain
        }
    return jsonify(response), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # We run on port 5000
    app.run(host='0.0.0.0', port=5003)
