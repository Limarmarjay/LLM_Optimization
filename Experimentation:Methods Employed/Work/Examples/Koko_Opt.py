import math
def minEatingSpeed(piles, h):
    l, r = 1, max(piles)
    res = r
    while l <= r:
        k = (l + r) // 2
        hrs = 0
        for p in piles:
            hrs += math.ceil(p / k)
        if hrs <= h:
            res = min(res, k)
            r = k - 1
        else:
            l = k + 1
    return res

def main():
    piles = list(map(int, input().split()))
    h = int(input())
    print(minEatingSpeed(piles, h))

main()
