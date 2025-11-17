import threading
import time
import random
import queue


N_TELLERS = 3
N_CUSTOMERS = 50 

# Semaphores and shared resources
door_sem = threading.Semaphore(2)        
manager_sem = threading.Semaphore(1)     
safe_sem = threading.Semaphore(2)        

bank_open_sem = threading.Semaphore(0)   
teller_ready_sem = threading.Semaphore(0)  

# Teller availability and selection
teller_available_sem = threading.Semaphore(0)
teller_queue = queue.Queue()

# Per teller synchronization
cust_arrived_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
teller_ask_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
cust_gave_trans_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
trans_done_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]
customer_left_sem = [threading.Semaphore(0) for _ in range(N_TELLERS)]

# Per teller state
current_customer_id = [None] * N_TELLERS
current_transaction = [None] * N_TELLERS


def teller_thread(tid: int):
    
    print(f"Teller {tid} [Teller {tid}]: ready to serve")
    
    teller_ready_sem.release()

    while True:
        
        print(f"Teller {tid} [Teller {tid}]: waiting for customer")
        teller_queue.put(tid)
        teller_available_sem.release()

        
        cust_arrived_sem[tid].acquire()
        cid = current_customer_id[tid]
        print(f"Teller {tid} [Customer {cid}]: asks for transaction")

        
        teller_ask_sem[tid].release()

        
        cust_gave_trans_sem[tid].acquire()
        txn = current_transaction[tid]
        print(f"Teller {tid} [Customer {cid}]: received transaction {txn}")

        
        if txn == "Withdrawal":
            print(f"Teller {tid} [Teller {tid}]: going to manager for approval")
            manager_sem.acquire()
            print(f"Teller {tid} [Teller {tid}]: interacting with manager")
            time.sleep(random.uniform(0.005, 0.03))  
            print(f"Teller {tid} [Teller {tid}]: done with manager")
            manager_sem.release()

       
        print(f"Teller {tid} [Teller {tid}]: going to safe")
        safe_sem.acquire()
        print(f"Teller {tid} [Teller {tid}]: in safe performing {txn}")
        time.sleep(random.uniform(0.01, 0.05))       
        print(f"Teller {tid} [Teller {tid}]: leaving safe")
        safe_sem.release()

       
        print(f"Teller {tid} [Customer {cid}]: transaction complete")
        trans_done_sem[tid].release()

        
        customer_left_sem[tid].acquire()
        print(f"Teller {tid} [Customer {cid}]: customer has left")


def customer_thread(cid: int):
    
    txn = random.choice(["Deposit", "Withdrawal"])
    print(f"Customer {cid} [Customer {cid}]: decides on {txn}")

    
    print(f"Customer {cid} [Customer {cid}]: waiting before going to bank")
    time.sleep(random.uniform(0, 0.1))
    print(f"Customer {cid} [Customer {cid}]: done waiting, heading to bank")

    
    bank_open_sem.acquire()
    print(f"Customer {cid} [Customer {cid}]: bank is open, approaching door")

    
    print(f"Customer {cid} [Customer {cid}]: waiting to enter bank")
    door_sem.acquire()
    print(f"Customer {cid} [Customer {cid}]: enters bank")

    
    print(f"Customer {cid} [Customer {cid}]: gets in line for teller")
    teller_available_sem.acquire()
    tid = teller_queue.get()
    print(f"Customer {cid} [Teller {tid}]: selects teller")

    
    current_customer_id[tid] = cid
    current_transaction[tid] = txn
    print(f"Customer {cid} [Teller {tid}]: introduces self to teller")
    cust_arrived_sem[tid].release()

    
    teller_ask_sem[tid].acquire()
    print(f"Customer {cid} [Teller {tid}]: gives transaction {txn}")
    cust_gave_trans_sem[tid].release()

    
    trans_done_sem[tid].acquire()
    print(f"Customer {cid} [Teller {tid}]: transaction finished, leaving teller")

    
    customer_left_sem[tid].release()
    print(f"Customer {cid} [Customer {cid}]: leaving bank")
    door_sem.release()


if __name__ == "__main__":
    # Start teller threads
    tellers = []
    for tid in range(N_TELLERS):
        t = threading.Thread(target=teller_thread, args=(tid,), daemon=True)
        tellers.append(t)
        t.start()

    # Wait until all tellers are ready, then open the bank
    for _ in range(N_TELLERS):
        teller_ready_sem.acquire()
    print("Main [Bank]: all tellers ready, bank is now open")

    # Allow each customer to enter once the bank is open
    for _ in range(N_CUSTOMERS):
        bank_open_sem.release()

    # Start customer threads
    customers = []
    for cid in range(N_CUSTOMERS):
        t = threading.Thread(target=customer_thread, args=(cid,))
        customers.append(t)
        t.start()

    # Wait for all customers to finish
    for t in customers:
        t.join()

    print("Main [Bank]: all customers done, simulation complete")
