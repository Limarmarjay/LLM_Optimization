def Sqrt(x):
    ans = 0
    for i in range(x + 1):
        if i * i <= x:
            ans = i
    return ans

def main():
    x = int(input())
    print(Sqrt(x))

main()