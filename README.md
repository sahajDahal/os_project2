# os_project2

# Bank Simulation – OS Project 2

This project simulates a bank environment using multithreading and semaphores in Python.  
There are **3 teller threads** and **50 customer threads**, each interacting through shared resources such as the bank door, manager, and safe. The simulation enforces realistic synchronization rules to mimic real banking constraints.

## Features

- **Teller Threads (3 total)**

  - Announce readiness before bank opens
  - Serve customers in order
  - Request manager approval for withdrawals
  - Access the safe (only 2 tellers allowed inside at once)
  - Coordinate a full request/response handshake with customers

- **Customer Threads (50 total)**
  - Randomly choose deposit or withdrawal
  - Wait 0–100ms before going to the bank
  - Enter through a door with capacity 2
  - Wait in line for available tellers
  - Exchange transaction details through synchronized steps

## Synchronization Tools Used

The simulation uses Python’s built-in threading tools:

- `threading.Thread` for teller and customer threads
- `threading.Semaphore` for:
  - Bank door limit
  - Manager approval (1 teller at a time)
  - Safe access (2 tellers at a time)
  - Teller availability
  - Customer–teller handshakes
- `queue.Queue` to map customers to available tellers

## Running the Simulation

Run the simulation with:

You will see detailed output of all actions in the format:

This output matches the project specifications exactly.

## Project Structure

- **bank_sim.py** – Main simulation code
- **devlog.md** – Development log showing progress over multiple sessions

## Notes

- Output is intentionally verbose for grading and synchronization validation.
- Threads simulate timing using short sleeps to model real-world transaction delays.
