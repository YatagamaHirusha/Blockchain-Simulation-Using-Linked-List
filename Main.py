from Blockchain import Blockchain

tst = Blockchain()

print("Test block 1....")
tst.add_block("100$ deposited")

print("Test block 2....")
tst.add_block("50$ withdrawal")

for block in tst.chain:
    print("-------------------------")
    print(f"Index: {block.index}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")


print(f"Doess chain valid? {tst.is_chain_valid()}")

print("\nLet's try to hack the blockchain:")
tst.chain[1].data = "200$ deposited"

print(f"Does chain valid? {tst.is_chain_valid()}")