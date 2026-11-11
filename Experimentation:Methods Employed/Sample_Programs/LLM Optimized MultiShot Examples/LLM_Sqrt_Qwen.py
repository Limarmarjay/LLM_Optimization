# QwenCoder
x = int(input())
def Sqrt2(x):
    left, right = 0, x
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= x:
            left = mid + 1
        else:
            right = mid - 1
    return right
print(Sqrt2(x))