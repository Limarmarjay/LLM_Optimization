# 3. 
n, k = list(map(int, input().split()))
l = list(map(int, input().split()))
c = 0
while set(l) != {k}:
    t = 100000000000
    for i in range(n-1, -1, -1):
        if l[i] < k and t != l[i]:
            t = l[i]
            l[i] = l[i] + 1
    c = c + 1
print(c)


