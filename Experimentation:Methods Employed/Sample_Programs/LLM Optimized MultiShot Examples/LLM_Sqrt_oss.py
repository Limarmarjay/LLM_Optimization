# gpt-oss
def isqrt_floor(x: int) -> int:
    """Return ?vx? using binary search."""
    if x < 2:
        return x
    lo, hi = 1, x // 2 + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == x:
            return mid
        if sq < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi


def main():
    x = int(input())
    print(isqrt_floor(x))


main()