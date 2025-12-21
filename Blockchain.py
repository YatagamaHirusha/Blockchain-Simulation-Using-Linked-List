from Block import Block

class Blockchain:
    def __init__(self):
        #creating a chain
        self.chain = [self.create_genesis_block()]  #this will add the returned object from below function to a list.

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "00000")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        previous_block = self.get_latest_block()

        new_index = previous_block.index + 1

        new_block = Block(new_index, new_data, previous_block.hash)

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