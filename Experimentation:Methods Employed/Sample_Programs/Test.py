# EASY (Based on Leetcode's Difficulty Rankings)

# Question 1 - BINARY SEARCH
# OPTIMIZED SOLUTION
def searchOpt(nums, target):
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
# UNOPTIMIZED SOLUTION
def searchUnop(nums, target):
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

# QUESTION 1 TEST CASES
listr = [1, 2, 3, 4, 5, 6]
target = 5

# Question 2 - GUESS NUMBER HIGHER OR LOWER
pick = int(input("Please enter a value"))
def guess(num):
    if num > pick:
        return -1
    elif num < pick:
        return 1
    return 0
# OPTIMIZED SOLUTION
def guessNumberOpt(n):
    l, r = 1, n
    while l <= r:
        m = l + (r - l) // 2
        res = guess(m)
        if res > 0:
            l = m + 1
        elif res < 0:
            r = m - 1
        else:
            return m
# UNOPTIMIZED SOLUTION
def guessNumberUnop(n):
    for i in range(1, n): # Logical Bug
        if guess(i) == 0:
            return i
# QUESTION 2 TEST CASE(S)
n = 50

# Question 3 - SQRT(X)
# OPTIMIZED SOLUTION
def mySqrtOpt(x):
    l, r = 0, x
    res = 0
    while l <= r:
        m = l + ((r - l) // 2)
        if m**2 > x:
            r = m - 1
        elif m**2 < x:
            l = m + 1
            res = m
        else:
            return m
    return res
# UNOPTIMIZED SOLUTION
def mySqrtUnop(x):
    ans = 0
    for i in range(x + 1):
        if i * i <= x:
            ans = i
    return ans
# QUESTION 3 TEST CASE(S)
x = 9

# MEDIUM (Based on Leetcode's Difficulty Rankings)

# Question 1 - KOKO EATING BANANAS
# OPTIMIZED SOLUTION
import math
def minEatingSpeedOpt(piles, h):
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
# UNOPTIMIZED SOLUTION
def minEatingSpeedUnop(piles, h):
    for speed in range(1, max(piles) + 1):
        time = 0
        for pile in piles:
            if time > h:
                break
            time += (pile + speed - 1) // speed
        if time <= h:
            return speed
    return -1
# QUESTION 4 TEST CASE(S)
piles = [2, 4, 8, 9]
h = 7

# Question 2 - SEARCH A 2D MATRIX
# OPTIMIZED SOLUTION
def searchMatrixOpt(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    top, bot = 0, rows - 1
    while top <= bot:
        row = (top + bot) // 2
        if target > matrix[row][-1]:
            top = row + 1
        elif target < matrix[row][0]:
            bot = row - 1
        else:
            break
    if not (top <= bot):
        return False
    row = (top + bot) // 2
    l, r = 0, cols - 1
    while l <= r:
        m = (l + r) // 2
        if target > matrix[row][m]:
            l = m + 1
        elif target < matrix[row][m]:
            r = m - 1
        else:
            return True
    return False
    
# UNOPTIMIZED SOLUTION
def searchMatrixUnop(matrix, target):
    Rows = len(matrix)
    Cols = len(matrix[0])
    for r in range(Rows):
        for c in range(Cols):
            if matrix[r][c] == target:
                return True
    return False

# QUESTION 5 TEST CASE(S)
matrix = [[1, 2, 3, 5], 
          [7, 9, 11, 13],
          [15, 17, 19, 21]]
target = 5
