import threading
import time
import random
import queue

# Constants
N_TELLERS = 3
N_CUSTOMERS = 50  # required by the project

# Semaphores and shared resources
door_sem = threading.Semaphore(2)        # At most 2 customers inside the bank
manager_sem = threading.Semaphore(1)     # Only 1 teller with the manager
safe_sem = threading.Semaphore(2)        # At most 2 tellers in the safe

bank_open_sem = threading.Semaphore(0)   # Customers wait on this until bank is open
teller_ready_sem = threading.Semaphore(0)  # For main to know all tellers are ready

# Teller availability & selection
teller_available_sem = threading.Semaphore(0)
teller_queue = queue.Queue()

# Per-teller synchronization
cust_arrived_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
teller_ask_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
cust_gave_trans_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
trans_done_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
customer_left_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]

# Per-teller state (which customer + what transaction)
current_customer_id = [None] * N_TELLERS
current_transaction = [None] * N_TELLERS



def teller_thread(tid: int):
    # Initial ready message
    print(f"Teller {tid} [Teller {tid}]: ready to serve")
    # Signal to main that this teller is ready so the bank can open
    teller_ready_sem.release()

    while True:
        # Step 1 & 2: teller is ready and waiting for a customer
        print(f"Teller {tid} [Teller {tid}]: waiting for customer")
        teller_queue.put(tid)
        teller_available_sem.release()

        # Step 2: Wait for a customer to approach this teller
        cust_arrived_sem[tid].acquire()
        cid = current_customer_id[tid]
        print(f"Teller {tid} [Customer {cid}]: asks for transaction")

        # Step 3: Ask for transaction
        teller_ask_sem[tid].release()

        # Step 4: Wait until customer gives transaction
        cust_gave_trans_sem[tid].acquire()
        txn = current_transaction[tid]
        print(f"Teller {tid} [Customer {cid}]: received transaction {txn}")

        # Step 5: If withdrawal, interact with manager
        if txn == "Withdrawal":
            print(f"Teller {tid} [Teller {tid}]: going to manager for approval")
            manager_sem.acquire()
            print(f"Teller {tid} [Teller {tid}]: interacting with manager")
            time.sleep(random.uniform(0.005, 0.03))  # 5–30 ms
            print(f"Teller {tid} [Teller {tid}]: done with manager")
            manager_sem.release()

        # Step 6 & 7: Go to safe
        print(f"Teller {tid} [Teller {tid}]: going to safe")
        safe_sem.acquire()
        print(f"Teller {tid} [Teller {tid}]: in safe performing {txn}")
        time.sleep(random.uniform(0.01, 0.05))       # 10–50 ms
        print(f"Teller {tid} [Teller {tid}]: leaving safe")
        safe_sem.release()

        # Step 8: Inform customer transaction is done
        print(f"Teller {tid} [Customer {cid}]: transaction complete")
        trans_done_sem[tid].release()

        # Step 9: Wait for customer to leave teller
        customer_left_sem[tid].acquire()
        print(f"Teller {tid} [Customer {cid}]: customer has left")


def customer_thread(cid: int):
    # Step 1: Decide transaction randomly
    txn = random.choice(["Deposit", "Withdrawal"])
    print(f"Customer {cid} [Customer {cid}]: decides on {txn}")

    # Step 2: Wait 0–100 ms before going to bank
    print(f"Customer {cid} [Customer {cid}]: waiting before going to bank")
    time.sleep(random.uniform(0, 0.1))
    print(f"Customer {cid} [Customer {cid}]: done waiting, heading to bank")

    # Step 3: Wait for bank to open
    bank_open_sem.acquire()
    print(f"Customer {cid} [Customer {cid}]: bank is open, approaching door")

    # Step 3 (door): Enter bank through the door (limit 2 customers inside)
    print(f"Customer {cid} [Customer {cid}]: waiting to enter bank")
    door_sem.acquire()
    print(f"Customer {cid} [Customer {cid}]: enters bank")

    # Step 4: Get in line / go to ready teller
    print(f"Customer {cid} [Customer {cid}]: gets in line for teller")
    teller_available_sem.acquire()
    tid = teller_queue.get()
    print(f"Customer {cid} [Teller {tid}]: selects teller")

    # Step 5: Introduce to teller
    current_customer_id[tid] = cid
    current_transaction[tid] = txn
    print(f"Customer {cid} [Teller {tid}]: introduces self to teller")
    cust_arrived_sem[tid].release()

    # Step 6: Wait for teller to ask for transaction
    teller_ask_sem[tid].acquire()
    print(f"Customer {cid} [Teller {tid}]: gives transaction {txn}")
    cust_gave_trans_sem[tid].release()

    # Step 8: Wait for transaction to complete
    trans_done_sem[tid].acquire()
    print(f"Customer {cid} [Teller {tid}]: transaction finished, leaving teller")

    # Step 9: Leave teller / bank
    customer_left_sem[tid].release()
    print(f"Customer {cid} [Customer {cid}]: leaving bank")
    door_sem.release()