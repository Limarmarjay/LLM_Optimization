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