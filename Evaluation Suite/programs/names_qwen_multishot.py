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
