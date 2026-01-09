# ⛓️ Python Blockchain Simulation (DSA Module)

A purely Python-based Blockchain implementation demonstrating **Hybrid Data Structures**, **Proof-of-Work Consensus**, and **Orphan Block Data Recovery**.

This project was built to simulate the core mechanics of a distributed ledger system, focusing on the interaction between Mutable Queues (Mempool) and Immutable Linked Lists (Blockchain).

---

## 🚀 Key Features

### 1. Hybrid Data Architecture
* **The Blockchain (Linked List):** Implemented as a backward-linked list for immutable data storage.
* **The Mempool (Queue):** Implemented as a **Linked-List based FIFO Queue** to buffer high-throughput transaction data before mining.

### 2. Distributed Consensus
* **Longest Chain Rule:** Nodes automatically resolve conflicts by accepting the chain with the most cumulative Proof-of-Work.
* **Dynamic Synchronization:** Nodes verify hashes and nonces to ensure data integrity during sync.

### 3. The "Rescue Mission" (Data Safety) 🛡️
In standard simulations, when a chain is reorganized (replaced), local blocks are deleted and data is lost.
* **My Solution:** Implemented a **Transaction Rescue Algorithm**.
* When a fork occurs, the system performs a set-difference scan between the old and new chains.
* "Orphaned" transactions are identified and immediately **re-enqueued** into the Mempool, ensuring zero data loss.

---

## 🛠️ Simulation vs. Real World

This project is a simulation of blockchain mechanics. Below is a comparison of how this architecture differs from production systems like Bitcoin.

| Feature | My Simulation | Real World (Bitcoin/Ethereum) |
| :--- | :--- | :--- |
| **Mempool** | **Local Queue.** Transactions exist only on the node they were sent to until mined. | **Gossiped.** Unconfirmed transactions are broadcast via P2P protocol to all nodes instantly. |
| **Block Size** | **Unlimited.** Can aggregate all rescued transactions into a single block. | **Limited (e.g., 1MB).** Transactions must wait for subsequent blocks if the size limit is reached. |
| **Mining** | **On-Demand.** Mining is triggered manually via API/GUI. | **Continuous.** Miners race 24/7 to solve the puzzle. |
| **Consensus** | **HTTP Polling.** Nodes ask neighbors for their chain. | **P2P Socket.** Nodes push new blocks to neighbors immediately. |

---

## 💻 Tech Stack

* **Language:** Python 3.x
* **Backend Framework:** Flask (REST API)
* **Data Structures:** Custom Linked Lists, Queues, Hash Maps (Sets)
* **Frontend:** HTML5, JavaScript (Fetch API)

---

## 🚦 How to Run the Network

To simulate a distributed network, we run multiple instances of the server on different ports.

### Step 1: Start the Nodes
Open two separate terminal windows.

**Terminal 1 (Node A):**
```bash
python Server.py 5001
```
**Terminal 2 (Node B):** 
Note: You may need to edit the bottom of Server.py to change the port to 5002 if not using command line args.

```Bash

python Server.py 5002
```

### Step 2: Use the Interface 
Open your browser to http://localhost:5001.

Create Transaction: Type "Alice pays Bob $10" and add to Queue.

Mine: Click "Mine Block" to move data from Mempool -> Blockchain.

Sync: Connect Node B to http://localhost:5001 and click "Sync" to test consensus.

## 🧩 Project Structure
**Block.py:** The fundamental unit of storage. Contains the Proof-of-Work logic.

**Blockchain.py:** The Controller. Manages the Linked List, verifies integrity, and handles the "Rescue Mission".

**Mempool.py:** The Queue data structure. Buffers transactions before they are hashed.

**Server.py:** The API Gateway. Connects the Python logic to the Web GUI.

## 🧪 Testing "The Rescue Mission"
* Mine 3 blocks on Node A.

* Mine 1 block with unique data ("Save Me!") on Node B.

* Connect Node B to Node A and click Sync.

* Observation: Node B's chain is replaced (Length 1 -> Length 3).

* Result: The "Save Me!" transaction is not deleted. It is moved to the Mempool.

* Mine a new block on Node B, and "Save Me!" will reappear in the chain.