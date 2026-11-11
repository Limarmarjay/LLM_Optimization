// 2. 
using System;
using System.Linq;

namespace ProblemB
{
    class Program
    {
        static void Main()
        {
            // Read number of elements
            int n = int.Parse(Console.ReadLine());

            // Read the sequence
            var a = Console.ReadLine()
                          .Split()
                          .Select(int.Parse)
                          .ToArray();

            // Track which numbers 1..n have already appeared
            bool[] seen = new bool[n + 1];
            int uniqueInRange = 0;

            foreach (int v in a)
            {
                // Keep the element only if it lies in 1..n and hasn't appeared before
                if (v >= 1 && v <= n && !seen[v])
                {
                    seen[v] = true;
                    uniqueInRange++;
                }
            }

            // Minimum changes = elements that cannot stay unchanged
            int result = n - uniqueInRange;
            Console.WriteLine(result);
        }
    }
}