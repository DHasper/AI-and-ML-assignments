import itertools
import time

def brute_force():
    # Test conditions on all permutations brute-force
    floors = range(5)

    for (l, m, n, e, j) in list(itertools.permutations(floors)):
        # Sleep so time improvements by changing the order can be
        #  tested more easily
        time.sleep(0.01)
        
        # Test all conditions, ordered by highest chance to lowest
        if e < m: continue
        if l == len(floors) - 1: continue
        if m == 0: continue
        if n == 0: continue
        if n == len(floors) - 1: continue
        if j == n + 1 or j == n - 1: continue
        if n == m + 1 or n == m - 1: continue
        
        return (l, m, n, e, j)

# Pint the solution
print('Solution {}'.format(brute_force())) 

times = []
iterations = 100

# Test the average time to find a solution
for i in range(iterations):
    t0 = time.time()
    result = brute_force()
    t1 = time.time()

    # Store the time it took to find a solution
    times.append(t1 - t0)

    # If this is the last iteration print the results
    if i == iterations - 1:
        print('Solution {}'.format(result)) 
        print("Average time: {:.5f}".format(sum(times) / (i + 1)))
