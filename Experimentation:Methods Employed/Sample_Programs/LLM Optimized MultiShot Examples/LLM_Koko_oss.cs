// gpt-oss
// Binary search for the minimum eating speed
using System;
using System.Linq;

class Program
{
    static int MinEatingSpeed(int[] piles, int h)
    {
        int left = 1;
        int right = piles.Max();
        int best = right;

        while (left <= right)
        {
            int mid = left + (right - left) / 2;
            long hours = 0;

            foreach (int pile in piles)
            {
                hours += (pile + mid - 1) / mid; // ceil division
                if (hours > h) break;
            }

            if (hours <= h)
            {
                best = mid;
                right = mid - 1;      // try a smaller speed
            }
            else
            {
                left = mid + 1;       // need a larger speed
            }
        }

        return best;
    }

    static void Main()
    {
        int[] piles = Console.ReadLine().Split(' ').Select(int.Parse).ToArray();
        int h = int.Parse(Console.ReadLine());
        Console.WriteLine(MinEatingSpeed(piles, h));
    }
}