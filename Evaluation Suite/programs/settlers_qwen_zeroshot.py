# 3. 
n, k = list(map(int, input().split()))
l = list(map(int, input().split()))

# Count the number of soldiers at each rank
rank_counts = [0] * (k + 1)
for rank in l:
    rank_counts[rank] += 1

# Calculate the number of coins needed to reach rank k for each rank
coins_needed = 0
for rank in range(1, k):
    if rank_counts[rank] > 0:
        # Calculate how many soldiers need to reach rank k
        needed = rank_counts[rank]
        # Calculate the number of coins needed to increase these soldiers' ranks
        coins_needed += needed * (k - rank)

print(coins_needed)