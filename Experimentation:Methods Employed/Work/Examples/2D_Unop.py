def searchMatrix(matrix, target):
    Rows = len(matrix)
    Cols = len(matrix[0])
    for r in range(Rows):
        for c in range(Cols):
            if matrix[r][c] == target:
                return True
    return False

def main():
    rows = int(input())
    matrix = [list(map(int, input().split())) for _ in range(rows)]
    target = int(input())
    print(searchMatrix(matrix, target))

main()
