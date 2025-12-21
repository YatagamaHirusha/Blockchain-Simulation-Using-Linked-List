import datetime
import hashlib

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # combine all the block's data into one string
        block_str = str(self.index) + self.timestamp + str(self.data) + self.previous_hash

        # encode it so computer can process
        encoded_block = block_str.encode()

        # Apply hashing algorithm
        hash = hashlib.sha256(encoded_block)

        # return the hexadecimal string (readable)
        return hash.hexdigest()