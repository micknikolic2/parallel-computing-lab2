# Lab 2 Analysis Questions

1. **Condition variables**  
   Why are two separate conditions (`cv_not_full`, `cv_not_empty`) used with the same lock? Could one condition work, and what are the trade-offs?
   The conditions are used with the same lock as they work with the same shared state (buffer and its lenght). We have two conditions because we have two different waiting reasons (i.e. condition.wait) and the linked wake signals. One is used to make the producer waits (if the buffer is full) and the other one is used to make the consumer waits (if the buffer is empty). Whether the one condition would work depends on how we define the "work". It can work in a sense that the core process can execute. However, it will lead to busy waiting and a lot of overhead (e.g. CPU usage, context switching, etc.).

2. **wait() loop**  
   Explain why `wait()` must be inside a `while` that rechecks the condition. What can go wrong with an `if` (spurious wakeups, races after notify)?
   The logic can face two edge scenarious if we use the conditional "if". One is the spurious wakup and it refers to a situation in which the thread can wake up for no strong reason (without notify() been invoked). In this situation, if we used the conditional "if" it will proceed to thread's main logic and raise the error or broke the program (and even if the program is monadic it will write the exception in the writer monad and broke the composition). The second situation happens due to threads racing after the condition is satisfied (for example, another thread can change the state before this thread can acquire the resource).

3. **notify() calls**  
   What happens if a producer skips `cv_not_empty.notify()` after adding, or a consumer skips `cv_not_full.notify()` after removing?

4. **Mutual exclusion**  
   Describe the incorrect behaviours if `with self.lock:` is removed from `put` and `get` (e.g., lost items, duplicates, corrupted counts, out-of-order state).
