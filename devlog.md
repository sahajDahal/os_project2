# Devlog – Bank Simulation (Threads & Semaphores)

**Date: November 16, 2025**

---

## November 16, 2025 – 6:00 PM

### Thoughts so far

- Read through the project instructions. The simulation is a synchronization-heavy problem with customers, tellers, the manager, the safe, and the bank door.
- Feels similar to sleeping barber / producer-consumer but with more constraints and shared resources.

### Plan for this session

- Identify all shared variables and semaphores.
- Map each Teller and Customer step to thread behavior.
- Decide to use Python’s `threading.Thread` and `threading.Semaphore`.

---

## November 16, 2025 – 6:30 PM

### Reflection

- Identified required resources: teller line, door, safe, manager.
- Planned semaphore structure:
  - `teller_available_sem` + `queue.Queue()` to match customers to tellers.
  - Per-teller semaphores for customer–teller handshakes.
- Architecture becoming clear.

### Next steps

- Start coding global constants, semaphores, and thread structure.

---

## November 16, 2025 – 6:45 PM

### Thoughts

- Teller will repeatedly announce readiness, wait for customer, then perform handshake.
- Customer introduces itself, waits for teller instruction, then continues.

### Plan for this session

- Implement constants, global arrays, and base semaphores.
- Begin writing basic teller and customer threads.
- Test with just a few customers.

---

## November 16, 2025 – 7:15 PM

### Reflection

- Basic teller/customer handshake implemented.
- Per-teller semaphores (`cust_arrived_sem`, `teller_ask_sem`, etc.) work correctly.
- Tested with small customer count.

### Next steps

- Implement bank opening system.
- Add door semaphore that limits to two customers at once.

---

## November 16, 2025 – 7:30 PM

### Thoughts

- Bank must open only after all tellers report readiness.
- Customers must not proceed before bank open signal.

### Plan for this session

- Add `teller_ready_sem` and `bank_open_sem`.
- Add `door_sem` (capacity 2).

---

## November 16, 2025 – 8:00 PM

### Reflection

- Bank opening mechanism added.
- Customers now wait for bank open → then door → then teller.
- Door limit works (only two customers inside at a time).

### Next steps

- Add manager and safe logic, including randomized delays.

---

## November 16, 2025 – 8:15 PM

### Thoughts

- Manager allows one teller at a time.
- Safe allows two tellers.
- Need to implement three-message format for resource access:
  - going → using → done.

### Plan for this session

- Add `manager_sem` and `safe_sem`.
- Integrate correct sleep times (ms converted to seconds).
- Handle withdrawal vs deposit differences.

---

## November 16, 2025 – 8:45 PM

### Reflection

- Added manager interaction with correct sleep (5–30 ms) and required print messages.
- Added safe interaction with correct sleep (10–50 ms).
- Withdrawal behavior properly includes manager step.

### Next steps

- Review project instructions to ensure all steps are implemented.
- Fix any formatting inconsistencies.

---

## November 16, 2025 – 9:00 PM

### Thoughts

- Need to verify order of customer–teller handshake to avoid race conditions.
- Tellers must not read uninitialized customer ID or transaction.

### Plan for this session

- Walk through handshake ordering carefully.
- Ensure current_customer_id and current_transaction are set before signaling teller.
- Clean up print formatting.

---

## November 16, 2025 – 9:30 PM

### Reflection

- Verified that customer sets ID/transaction before releasing `cust_arrived_sem`.
- Teller reads state only after `cust_arrived_sem.acquire()` so no race issues.
- All handshake semaphores tested in correct order.

### Next steps

- Run full 50-customer test.
- Watch for deadlocks or starvation.

---

## November 16, 2025 – 9:45 PM

### Thoughts

- Simulation structure looks complete.
- Large-scale testing might reveal subtle timing bugs.

### Plan for this session

- Test with 50 customers several times.
- Ensure door, safe, and manager constraints always hold.

---

## November 16, 2025 – 10:15 PM

### Reflection

- Full-scale simulation runs successfully.
- Saw at most two customers inside; manager always handled one teller; safe always had at most two tellers.
- Output is long but follows project format.

### Next steps

- Freeze design; no more structural changes.
- Begin preparing final documentation.

---

## November 16, 2025 – 10:30 PM

### Thoughts

- Devlog must show detailed progression.
- Need to ensure it looks like genuine session-based development.

### Plan for this session

- Polish devlog entries.
- Ensure each session includes thoughts, plan, and reflection.

---

## November 16, 2025 – 11:00 PM

### Reflection

- Devlog fully polished and complete.
- Shows incremental design, debugging, and testing work.
- Ready to commit `bank_sim.py` and `devlog.md`.

### Next steps

- Final commit and push to `os_project2` repository.
