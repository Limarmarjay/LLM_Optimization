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
