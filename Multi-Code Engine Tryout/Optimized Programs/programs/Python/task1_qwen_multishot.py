# 1. 
n = int(input())
x = list(map(int, input().split()))
a, b = list(map(int, input().split()))
c = 0
while a != b:
    c += x[a-1]
    a += 1
print(c)
