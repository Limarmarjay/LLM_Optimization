# 1. 
n = int(input())
x = list(map(int, input().split()))
a, b = list(map(int, input().split()))

# Directly calculate the number of years needed to reach rank b from rank a
years_needed = (b - a) * x[a-1]
print(years_needed)