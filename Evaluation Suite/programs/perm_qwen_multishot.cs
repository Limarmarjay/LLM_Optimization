// 2.
using System;
using System.Collections.Generic;
using System.Linq;

namespace ProblemB
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = int.Parse(Console.ReadLine());
            string[] token = Console.ReadLine().Split();
            HashSet<int> seen = new HashSet<int>();

            foreach (string s in token)
            {
                int num = int.Parse(s);
                seen.Add(num);
            }

            int result = 0;
            for (int i = 1; i <= n; i++)
            {
                if (!seen.Contains(i))
                {
                    result++;
                }
            }

            Console.WriteLine(result);
        }
    }
}