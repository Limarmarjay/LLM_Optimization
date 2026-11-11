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
