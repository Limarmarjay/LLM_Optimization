
// QwenCoder
using System;
using System.Linq;

class Program
{
    static int MinEatingSpeed2(int[] piles, int h)
    {
        int left = 1, right = int.MaxValue;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (CanEatAllPiles(piles, mid, h))
            {
                right = mid;
            }
            else
            {
                left = mid + 1;
            }
        }
        return left;
    }

    private static bool CanEatAllPiles(int[] piles, int speed, int h)
    {
        long time = 0;
        foreach (int pile in piles)
        {
            time += (pile + speed - 1) / speed;
            if (time > h)
            {
                return false;
            }
        }
        return true;
    }

    static void Main()
    {
        int[] piles = Console.ReadLine().Split(' ').Select(int.Parse).ToArray();
        int h = int.Parse(Console.ReadLine());
        Console.WriteLine(MinEatingSpeed2(piles, h));
    }
}