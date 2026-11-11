using System;
using System.Linq;

class Program
{
    static bool SearchMatrix(int[][] matrix, int target)
    {
        int Rows = matrix.Length;
        int Cols = matrix[0].Length;
        for (int r = 0; r < Rows; r++)
        {
            for (int c = 0; c < Cols; c++)
            {
                if (matrix[r][c] == target)
                {
                    return true;
                }
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