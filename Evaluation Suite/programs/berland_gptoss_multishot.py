# 1. 
# Optimized solution for the Berland Armed Forces problem
n = int(input())                         # number of ranks
d = list(map(int, input().split()))      # years needed for each transition (n-1 values)
a, b = map(int, input().split())         # current rank and dream rank

# Ensure we sum in the correct direction
if a > b:
    a, b = b, a
# Sum the years needed to climb from rank a to rank b
# Transition i goes from rank i to i+1 and is stored at d[i-1]
years_needed = sum(d[a-1:b-1])          # b-1 is exclusive

print(years_needed)