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
