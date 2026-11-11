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
            string[] token = Console.ReadLine().Split();
            int[] a = new int[n+1];
            int tmp;
            for (int i = 0; i < n; i++)
            {
                tmp = int.Parse(token[i]);
                a[tmp>n?n:tmp- 1]++;
            }
            int result = 0;
            for (int i=0; i<n; i++)
                if (a[i]==0) result++;
            Console.WriteLine(result);

        }
    }
}