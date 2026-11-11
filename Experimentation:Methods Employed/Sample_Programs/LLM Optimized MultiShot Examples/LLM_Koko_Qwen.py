# QwenCoder
piles = list(map(int, input().split()))
h = int(input())
def minEatingSpeed2(piles, h):
    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if sum((pile + mid - 1) // mid for pile in piles) > h:
            left = mid + 1
        else:
            right = mid
    return left
print(minEatingSpeed2(piles, h))