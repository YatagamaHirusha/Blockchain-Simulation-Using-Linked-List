from Block import Block
import requests

class Blockchain:
    def __init__(self):
        #creating a chain
        self.chain = [self.create_genesis_block()]  #this will add the returned object from below function to a list.
        self.nodes = set()  # Stores unique node addresses in chain
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "00000")

    def get_latest_block(self):
        return self.chain[-1]

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
        """
        This is the consensus algorithm. It resolves conflicts
        by replacing our chain with the longest one in the chain (network)
        If our chain replaced with the longest node, it returns true, if not, false.
        """
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
                        new_chain = chain_data

            except:
                continue

        # if new chain found, replace existing one
        if new_chain:
            self.chain = new_chain
            return True
        return False