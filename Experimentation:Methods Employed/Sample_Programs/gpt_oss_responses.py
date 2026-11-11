"""
MULTI-SHOT
"""
# 1. 
# Optimized solution for the Berland Armed Forces problem
n = int(input())                         # number of ranks
d = list(map(int, input().split()))      # years needed for each transition (n-1 values)
a, b = map(int, input().split())         # current rank and dream rank

# Ensure we sum in the correct direction
if a > b:
    a, b = b, a
# Sum the years needed to climb from rank a to rank b
# Transition i goes from rank i to i+1 and is stored at d[i-1]
years_needed = sum(d[a-1:b-1])          # b-1 is exclusive

print(years_needed)

# 2. 
import sys
from collections import deque
def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n)]
    deg = [0] * n

    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # initial queue of leaves
    q = deque([i for i in range(n) if deg[i] == 1])
    removed = [False] * n
    rounds = 0

    while q:
        rounds += 1
        next_q = deque()
        while q:
            node = q.popleft()
            if removed[node]:
                continue
            removed[node] = True
            for nb in adj[node]:
                if removed[nb]:
                    continue
                deg[nb] -= 1
                if deg[nb] == 1:
                    next_q.append(nb)
        q = next_q

    print(rounds)

if __name__ == "__main__":
    main()

# 3. 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from collections import Counter
def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n, k = map(int, data[:2])
    ranks = list(map(int, data[2:2 + n]))

    # Count only ranks that are strictly less than k
    cnt = Counter(r for r in ranks if r < k)

    # If everybody already has rank k, no training is needed
    if not cnt:
        print(0)
        return

    # Compute maximum prefix sum of the counts
    cum = 0
    answer = 0
    for r in sorted(cnt):
        cum += cnt[r]
        if cum > answer:
            answer = cum

    print(answer)
if __name__ == "__main__":
    main()

# 4.
import sys
MOD = 1_000_000_007
def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n, m = map(int, data[:2])
    names = data[2:2 + n]

    # For each column keep the set of distinct letters seen so far
    col_sets = [set() for _ in range(m)]

    for name in names:
        # name is guaranteed to have length m
        for idx, ch in enumerate(name):
            col_sets[idx].add(ch)

    # The answer is the product of the sizes of all column sets
    result = 1
    for s in col_sets:
        result = (result * len(s)) % MOD

    print(result)
if __name__ == "__main__":
    solve()


"""
ZERO-SHOT
"""
# 1. 
import sys
def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:          # no input
        return

    it = iter(data)
    n = int(next(it))

    # The army has n ranks, so there are n-1 transition times
    durations = [int(next(it)) for _ in range(n - 1)]

    a = int(next(it))
    b = int(next(it))

    # If the current rank equals the dream rank – no more years are needed
    if a == b:
        print(0)
        return

    # Ensure a < b (the problem implicitly assumes a < b, but this makes it robust)
    if a > b:
        a, b = b, a

    # Sum the years needed to climb from rank a up to rank b
    # indices in Python are 0-based ? a-1 for the first element
    total_years = sum(durations[a - 1:b - 1])
    print(total_years)
if __name__ == "__main__":
    solve()

# 2. 
import sys
def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    # adjacency lists (0-based indices)
    adj = [[] for _ in range(n)]
    deg = [0] * n
    for _ in range(m):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1

    # initial leaves (degree == 1)
    current = [v for v in range(n) if deg[v] == 1]
    removed = [False] * n
    groups = 0

    while current:
        groups += 1
        next_round = []

        for leaf in current:
            if removed[leaf] or deg[leaf] == 0:   # safety check
                continue
            removed[leaf] = True
            for nb in adj[leaf]:
                if removed[nb]:
                    continue
                deg[nb] -= 1
                if deg[nb] == 1:
                    next_round.append(nb)

        # filter out vertices that became isolated in this round
        current = [v for v in next_round if deg[v] == 1]

    print(groups)
if __name__ == "__main__":
    solve()

# 3.
import sys
def solve() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    ranks = data[2:]

    # Count how many soldiers have each rank
    cnt = [0] * (k + 1)
    for r in ranks:
        cnt[r] += 1

    cum = 0          # soldiers with rank = current r
    answer = 0

    # For every rank that is not the final one
    for r in range(1, k):
        cum += cnt[r]
        if cum:   # only consider ranks that actually contain soldiers
            candidate = cum + (k - 1 - r)
            if candidate > answer:
                answer = candidate

    print(answer)
if __name__ == "__main__":
    solve()

# 4.
import sys
MOD = 1_000_000_007
ALPHA = ord('A')          # 'A' ? 0,  'B' ? 1, … , 'Z' ? 25

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:                     # empty input
        return

    n = int(data[0])
    m = int(data[1])
    names = data[2:2 + n]            # the n strings

    # bitmask for each position (column) – 26-bit mask
    masks = [0] * m

    for s in names:
        for i, ch in enumerate(s):
            masks[i] |= 1 << (ord(ch) - ALPHA)

    # product of the number of distinct letters in every column
    ans = 1
    for mask in masks:
        # count bits set in mask – number of distinct letters
        cnt = bin(mask).count('1')
        ans = (ans * cnt) % MOD

    print(ans)
if __name__ == "__main__":
    solve()