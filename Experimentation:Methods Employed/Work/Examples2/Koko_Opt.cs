using System;
using System.Linq;

class Program
{
    static int MinEatingSpeed(int[] piles, int h)
    {
        int l = 1, r = piles.Max();
        int res = r;
        while (l <= r)
        {
            int k = l + (r - l) / 2;
            long hrs = 0;
            foreach (int p in piles)
            {
                hrs += (long)Math.Ceiling((double)p / k);
            }
            if (hrs <= h)
            {
                res = Math.Min(res, k);
                r = k - 1;
            }
            else
            {
                l = k + 1;
            }
        }
        return res;
    }

    static void Main()
    {
        int[] piles = Console.ReadLine().Split().Select(int.Parse).ToArray();
        int h = int.Parse(Console.ReadLine());
        Console.WriteLine(MinEatingSpeed(piles, h));
    }
}