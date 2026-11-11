def min_eating_speed(piles, h):
    left, right = 1, max(piles)
    answer = right
    while left <= right:
        mid = (left + right) // 2
        hours = 0
        for pile in piles:
            hours += (pile + mid - 1) // mid  # ceil division
            if hours > h:
                break
        if hours <= h:
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
    return answer


def main():
    piles = list(map(int, input().split()))
    h = int(input())
    print(min_eating_speed(piles, h))


main()