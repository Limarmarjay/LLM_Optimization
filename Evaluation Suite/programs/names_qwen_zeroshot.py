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