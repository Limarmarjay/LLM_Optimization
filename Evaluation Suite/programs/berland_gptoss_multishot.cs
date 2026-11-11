// 1. 
using System;
class Program
{
    static void Main()
    {
        // Number of ranks (not used directly, but read to match input format)
        int n = int.Parse(Console.ReadLine());

        // Read the array of years needed to move from rank i to i+1
        int[] years = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);

        // Read current rank (pos) and desired rank (dest)
        int[] posDest = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);
        int pos = posDest[0];
        int dest = posDest[1];

        // Sum the years needed to go from pos to dest-1
        long totalYears = 0;
        for (int i = pos - 1; i < dest - 1; i++)
        {
            totalYears += years[i];
        }

        Console.WriteLine(totalYears);
    }
}
