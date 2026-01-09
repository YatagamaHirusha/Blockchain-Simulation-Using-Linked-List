from http.client import responses

from flask import Flask, jsonify, request

from Block import Block
from uuid import uuid4

from flask import Flask, jsonify, request, render_template

from Blockchain import Blockchain

# Instantiate node
app = Flask(__name__)
#
# node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

# Get the full chain
@app.route('/chain', methods=['GET'])
def full_chain():
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
    if not values or 'data' not in values:
        return 'Missing values', 400

    # add to the blockchain's mempool - Queue
    index = blockchain.add_transactions(values['data'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201



@app.route('/mine', methods=['GET'])
def mine():
    # Attempt to mine the pending transactions
    mined_block = blockchain.mine_pending_transactions()

    if not mined_block:
        return jsonify({'message': "No transactions to mine! "}), 400

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
        return "Error: please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# sync
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

    serialized_chain = []
    for block in blockchain.chain:
        # check whether its already a dictionary or object
        if hasattr(block, '__dict__'):
             # manually map the fields only we want to show
            serialized_chain.append({
                'index': block.index,
                'timestamp': block.timestamp,
                'data': block.data,
                'hash': block.hash,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce
            })
        else:
            serialized_chain.append(block)
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': serialized_chain
        }
    else:
        response = {
            'message': 'Our chain is latest',
            'chain': serialized_chain
        }
    return jsonify(response), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
