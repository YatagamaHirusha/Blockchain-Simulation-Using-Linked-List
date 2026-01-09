from Block import Block
from MemoryPool import MemPool
import requests

class Blockchain:
    def __init__(self):
        #creating a chain
        self.chain = [self.create_genesis_block()]  #this will add the returned object from below function to a list.
        self.nodes = set()  # Stores unique node addresses in chain
        self.difficulty = 4
        self.memPool = MemPool()


    def create_genesis_block(self):
        return Block(0, "Genesis Block", "00000")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transactions(self, transaction_data):
        self.memPool.add_transaction(transaction_data)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self):
        if self.memPool.isEmpty():
            return False

        block_data = list(self.memPool.get_transactions())
        previous_block = self.get_latest_block()
        new_block = Block(previous_block.index + 1, block_data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.memPool.clear()

        return new_block

    # def add_block(self, new_data):
    #     previous_block = self.get_latest_block()
    #
    #     new_index = previous_block.index + 1
    #
    #     new_block = Block(new_index, new_data, previous_block.hash)
    #
    #     self.chain.append(new_block)

    def add_block(self, new_data):
        previous_block = self.get_latest_block()

        # Create the new block
        new_block = Block(previous_block.index + 1, new_data, previous_block.hash)

        # <--- NEW: We force the computer to solve the puzzle here
        new_block.mine_block(self.difficulty)

        # Only add it after it is mined
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def register_node(self, address):
        """
        Add a new node to a list of nodes
        (Ip address)
        """
        self.nodes.add(address)

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbors:
            try:
                response = requests.get(f"{node}/chain")
                if response.status_code == 200:
                    length = response.json()['length']
                    chain_data = response.json()['chain']

                    if length > max_length:
                        max_length = length
                        # Convert JSON back to Objects
                        new_chain_objects = []
                        for block_dict in chain_data:
                            new_block = Block(
                                block_dict['index'],
                                block_dict['data'],
                                block_dict['previous_hash']
                            )
                            new_block.nonce = block_dict['nonce']
                            new_block.timestamp = block_dict['timestamp']
                            new_block.hash = block_dict['hash']
                            new_chain_objects.append(new_block)

                        new_chain = new_chain_objects
            except:
                continue

        if new_chain:
            # --- THE RESCUE MISSION STARTS HERE ---

            # 1. Create a checklist of all transactions in the NEW chain
            # We use a Set for fast lookup
            new_chain_txs = set()
            for block in new_chain:
                # Handle List data (Normal blocks) vs String data (Genesis)
                if isinstance(block.data, list):
                    for tx in block.data:
                        new_chain_txs.add(tx)
                else:
                    new_chain_txs.add(block.data)

            # 2. Rescue missing transactions from the OLD chain
            for block in self.chain:
                if isinstance(block.data, list):
                    for tx in block.data:
                        if tx not in new_chain_txs:
                            # If this tx is NOT in the new chain, rescue it!
                            print(f"Rescuing transaction: {tx}")
                            self.memPool.add_transaction(tx)

            # --- RESCUE MISSION COMPLETE ---

            self.chain = new_chain
            return True

        return False