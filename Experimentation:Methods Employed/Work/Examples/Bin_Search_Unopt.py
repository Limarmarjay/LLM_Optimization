def Bin_search(nums, target):
    left_ind = 0
    right_ind = len(nums) - 1

    while left_ind <= right_ind:
        mid_point = (left_ind + right_ind) // 2

        for _ in nums:
            if nums[mid_point] == target:
                return mid_point
            elif nums[mid_point] < target:
                left_ind = mid_point + 1
                break
            else:
                right_ind = mid_point - 1
                break
    return -1

def main():
    nums = list(map(int, input().split()))
    target = int(input())
    print(Bin_search(nums, target))

main()
