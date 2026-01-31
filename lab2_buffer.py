# lab2_buffer.py
import threading
import time
import random
from collections import deque

# Configuration
BUFFER_SIZE = 5
NUM_PRODUCERS = 2
NUM_CONSUMERS = 2
PRODUCER_DELAY = 0.2  # Avg time for producer to create item
CONSUMER_DELAY = 0.5  # Avg time for consumer to process item
ITEMS_PER_PRODUCER = 8

class BoundedBuffer:
    """
    A thread-safe bounded buffer using Lock and Condition variables.
    """
    def __init__(self, capacity):
        super().__init__()
        if capacity <= 0:
            raise ValueError("Capacity must be > 0")

        # --- TODO: Task 1 - Initialize attributes ---
        # Set capacity
        self.capacity = capacity
        # Use a deque with a fixed maxlen to represent the buffer
        self.buffer = deque(maxlen=capacity)
        # Single lock shared by both conditions
        self.lock = threading.Lock()
        # Two conditions on the same lock
        self.cv_not_full = threading.Condition(self.lock)
        self.cv_not_empty = threading.Condition(self.lock)
        # --- End TODO ---

    def put(self, item):
        """Add an item to the buffer. Blocks if the buffer is full."""
        # --- TODO: Task 2 - Implement put logic ---
        with self.lock:
            while len(self.buffer) == self.capacity:
                print("Producer waiting: buffer full")
                self.cv_not_full.wait()
            self.buffer.append(item)
            print(f"Produced {item} (size={len(self.buffer)}/{self.capacity})")
            self.cv_not_empty.notify()
        # --- End TODO ---
        return  # Placeholder so starter code runs

    def get(self):
        """Remove and return an item from the buffer. Blocks if the buffer is empty."""
        item = None
        # --- TODO: Task 3 - Implement get logic ---
        with self.lock:
            while len(self.buffer) == 0:
                print("Consumer waiting: buffer empty")
                self.cv_not_empty.wait()
            item = self.buffer.popleft()
            print(f"Consumed {item} (size={len(self.buffer)}/{self.capacity})")
            self.cv_not_full.notify()
        return item
        # --- End TODO ---
        return item  # Placeholder so starter code runs

# ==================================
# Producer & Consumer Functions
# ==================================

def producer(thread_id, buffer):
    """Producer thread function."""
    for i in range(ITEMS_PER_PRODUCER):
        item = f"Item-{thread_id}-{i}"
        # Simulate time taken to produce item
        time.sleep(random.uniform(0, PRODUCER_DELAY * 2))
        buffer.put(item)
    print(f"Producer {thread_id} finished.")

def consumer(thread_id, buffer):
    """Consumer thread function."""
    # Consumers run until producers are likely done (adjust as needed for longer runs)
    # A more robust solution might use sentinel values or other shutdown mechanisms.
    for _ in range(int(ITEMS_PER_PRODUCER * NUM_PRODUCERS / NUM_CONSUMERS)):
        item = buffer.get()
        # Simulate time taken to consume item
        time.sleep(random.uniform(0, CONSUMER_DELAY * 2))
    print(f"Consumer {thread_id} finished.")

# ==================================
# Main Execution
# ==================================

if __name__ == "__main__":
    print(f"Starting Bounded Buffer simulation (Capacity: {BUFFER_SIZE})")
    print(f"Producers: {NUM_PRODUCERS}, Consumers: {NUM_CONSUMERS}")
    print(f"Items per Producer: {ITEMS_PER_PRODUCER}")
    print("-" * 30)

    buffer = BoundedBuffer(BUFFER_SIZE)
    producers = []
    consumers = []

    # Create and start producer threads
    for i in range(NUM_PRODUCERS):
        p_thread = threading.Thread(target=producer, args=(i, buffer))
        producers.append(p_thread)
        p_thread.start()

    # Create and start consumer threads
    for i in range(NUM_CONSUMERS):
        c_thread = threading.Thread(target=consumer, args=(i, buffer))
        consumers.append(c_thread)
        c_thread.start()

    # Wait for all producer threads to complete
    print("Main: Waiting for producers...")
    for p in producers:
        p.join()
    print("Main: Producers finished.")

    # Wait for all consumer threads to complete
    # Note: Consumers might finish slightly after producers if buffer had items left
    print("Main: Waiting for consumers...")
    for c in consumers:
        c.join()
    print("Main: Consumers finished.")

    print("-" * 30)
    print(f"Final buffer size: {len(buffer.buffer)}")
    print("Simulation finished.")
