def Sqrt(x):
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

def main():
    x = int(input())
    print(Sqrt(x))

main()