class MemPoolNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class MemPool:
    def __init__(self):
        self.front = None
        self.rear = None

    def isEmpty(self):
        return self.front is None

    # enqueue
    def add_transaction(self, data):
        new_node = MemPoolNode(data)

        if self.isEmpty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    # dequeue
    def get_transactions(self):
        transactions = []   # to hold pending transactions
        current = self.front
        while current is not None:
            transactions.append(current.data)
            current = current.next
        return transactions

    def clear(self):
        self.front = None
        self.rear = None
