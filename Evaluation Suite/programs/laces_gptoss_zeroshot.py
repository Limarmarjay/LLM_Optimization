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