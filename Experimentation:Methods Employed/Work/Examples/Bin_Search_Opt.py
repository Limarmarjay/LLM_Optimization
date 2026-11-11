def Bin_search(nums, target):
    l, r = 0, len(nums) - 1

    while l <= r:
        m = l + (r - l) // 2
        if nums[m] > target:
            r = m - 1
        elif nums[m] < target:
            l = m + 1
        else:
            return m
    return -1

def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(Bin_search(nums, target))

main()