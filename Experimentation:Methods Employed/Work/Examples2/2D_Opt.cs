using System;
using System.Linq;

class Program
{
    static bool SearchMatrix(int[][] matrix, int target)
    {
        int rows = matrix.Length, cols = matrix[0].Length;
        int top = 0, bot = rows - 1;
        while (top <= bot)
        {
            int row = top + (bot - top) / 2;
            if (target > matrix[row][cols - 1])
            {
                top = row + 1;
            }
            else if (target < matrix[row][0])
            {
                bot = row - 1;
            }
            else
            {
                break;
            }
        }
        if (!(top <= bot))
        {
            return false;
        }
        int midRow = top + (bot - top) / 2;
        int l = 0, r = cols - 1;
        while (l <= r)
        {
            int m = l + (r - l) / 2;
            if (target > matrix[midRow][m])
            {
                l = m + 1;
            }
            else if (target < matrix[midRow][m])
            {
                r = m - 1;
            }
            else
            {
                return true;
            }
        }
        return false;
    }

    static void Main()
    {
        int rows = int.Parse(Console.ReadLine());
        int[][] matrix = new int[rows][];
        for (int i = 0; i < rows; i++)
        {
            matrix[i] = Console.ReadLine().Split().Select(int.Parse).ToArray();
        }
        int target = int.Parse(Console.ReadLine());
        Console.WriteLine(SearchMatrix(matrix, target) ? "True" : "False");
    }
}