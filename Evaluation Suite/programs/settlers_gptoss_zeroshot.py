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

