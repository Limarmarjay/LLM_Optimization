"""
MULTI-SHOT
"""
# 1. 
n = int(input())
x = list(map(int, input().split()))
a, b = list(map(int, input().split()))
c = 0
while a != b:
    c += x[a-1]
    a += 1
print(c)

# 2. 
import sys
def reprimand(friends_list, n):
    bad_list = []
    for index in range(n):
        if len(friends_list[index]) == 1:
            bad_list.append(index)
    for index in bad_list:
        friends_list[index] = []
        for neighbor in friends_list[index]:
            friends_list[neighbor].remove(index)
    return len(bad_list)

def main():
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    m = int(data[1])

    friends_list = [[] for _ in range(n)]
    index = 2
    for i in range(m):
        a = int(data[index]) - 1
        b = int(data[index + 1]) - 1
        friends_list[a].append(b)
        friends_list[b].append(a)
        index += 2

    ans = 0
    while any(friends_list):
        ans += reprimand(friends_list, n)
    print(ans - 1)
if __name__ == "__main__":
    main()

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

# 4.
def solve(names):
    m = len(names[0])
    postfix = {}
    for name in names:
        postfix[name[-1:]] = True
    if m == 1:
        return len(postfix)

    distinct_names = set()
    for name in names:
        for i in range(1, m+1):
            distinct_names.add(name[:i])
    return len(distinct_names) % 1000000007

def main():
    firstLine = input().split()
    firstLine = list(map(int, firstLine))
    inputLines = []
    for i in range(firstLine[0]):
        line = input()
        inputLines.append(line)
    print(solve(inputLines) % 1000000007)

if __name__ == "__main__":
    main()


"""
ZERO-SHOT
"""
# 1. 
n = int(input())
x = list(map(int, input().split()))
a, b = list(map(int, input().split()))

# Directly calculate the number of years needed to reach rank b from rank a
years_needed = (b - a) * x[a-1]
print(years_needed)

# 2. 
n, m = map(int, input().split())
friends_list = [[] for _ in range(n)]
degree = [0] * n  # Degree array to keep track of the number of ties each student has
# Read the input and update the adjacency list and degree array
for i in range(m):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    friends_list[a].append(b)
    friends_list[b].append(a)
    degree[a] += 1
    degree[b] += 1
# Function to reprimand students
def reprimand():
    bad_list = []
    for index in range(n):
        if degree[index] == 1:
            bad_list.append(index)
    for index in bad_list:
        degree[index] = -1  # Mark as reprimanded
        for neighbor in friends_list[index]:
            degree[neighbor] -= 1
            friends_list[neighbor].remove(index)
# Initialize the answer and perform the reprimand process
ans = 0
while any(d > 0 for d in degree):
    reprimand()
    ans += 1
# Output the result
print(ans - 1)

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

# 4.
def solve(names):
    m = len(names[0])
    prefix_count = {}

    for name in names:
        prefix = name[:m-1]
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

    return len(prefix_count)

def main():
    firstLine = input().split()
    firstLine = list(map(int, firstLine))
    inputLines = []
    for i in range(firstLine[0]):
        line = input()
        inputLines.append(line)
    #solve(firstLine)
    print(solve(inputLines) % 1000000007)

if __name__ == "__main__":
    main()