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


