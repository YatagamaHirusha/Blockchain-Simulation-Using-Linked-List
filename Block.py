import datetime
import hashlib

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # combine all the block's data into one string
        block_str = str(self.index) + self.timestamp + str(self.data) + self.previous_hash + str(self.nonce)

        # encode it so computer can process
        encoded_block = block_str.encode()

        # Apply hashing algorithm
        hash = hashlib.sha256(encoded_block)

        # return the hexadecimal string (readable)
        return hash.hexdigest()

    def mine_block(self, difficulty):
        # The Target: A hash starting with 'difficulty' number of zeros (e.g., "0000")
        target = "0" * difficulty

        # Keep changing the nonce until we get lucky
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block Mined! Nonce: {self.nonce}, Hash: {self.hash}")