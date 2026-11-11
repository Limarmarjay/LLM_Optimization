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