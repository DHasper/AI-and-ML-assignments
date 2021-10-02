import itertools

floors = range(5)
for (l, m, n, e, j) in list(itertools.permutations(floors)):
    if l == len(floors) - 1: continue
    if m == 0: continue
    if n == 0 or n == len(floors) - 1: continue
    if e < m: continue
    if j == n + 1 or j == n - 1: continue
    if n == m + 1 or n == m - 1: continue
    
    print(l, m, n, e, j)
