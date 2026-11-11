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