// 1. 
using System;
using System.Linq;

namespace _38A
{
    class Program
    {
        static void Main(string[] args)
        {
            int N = int.Parse(Console.ReadLine());
            int[] cont = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int[] temp = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int pos = temp[0], dest = temp[1], ans = 0;

            // Calculate the number of years needed to reach rank b from rank a
            for (int i = pos - 1; i < dest - 1; i++)
            {
                ans += cont[i];
            }

            Console.WriteLine(ans);
        }
    }
}