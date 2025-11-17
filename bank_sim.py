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