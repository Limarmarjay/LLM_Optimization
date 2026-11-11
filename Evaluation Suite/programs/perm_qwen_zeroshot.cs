// 2. 
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ProblemB
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = int.Parse(Console.ReadLine());
            int[] a = new int[5001];
            int[] count = new int[5001];

            string[] token = Console.ReadLine().Split();
            foreach (string t in token)
            {
                int tmp = int.Parse(t);
                a[tmp]++;
                count[tmp] = 1;
            }

            int result = 0;
            for (int i = 1; i <= n; i++)
            {
                if (count[i] == 0)
                {
                    result++;
                }
                else if (count[i] > 1)
                {
                    result += count[i] - 1;
                }
            }
            Console.WriteLine(result);
        }
    }
}