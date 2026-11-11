def minEatingSpeed(piles, h):
    for speed in range(1, max(piles) + 1):
        time = 0
        for pile in piles:
            if time > h:
                break
            time += (pile + speed - 1) // speed
        if time <= h:
            return speed
    return -1

def main():
    piles = list(map(int, input().split()))
    h = int(input())
    print(minEatingSpeed(piles, h))

main()