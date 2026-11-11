using System;
using System.Linq;

class Program
{
    static int MinEatingSpeed(int[] piles, int h)
    {
        int max = piles.Max();
        for (int speed = 1; speed <= max; speed++)
        {
            long time = 0;
            foreach (int pile in piles)
            {
                if (time > h)
                {
                    break;
                }
                time += (pile + speed - 1) / speed;
            }
            if (time <= h)
            {
                return speed;
            }
        }
        return -1;
    }

    static void Main()
    {
        int[] piles = Console.ReadLine().Split().Select(int.Parse).ToArray();
        int h = int.Parse(Console.ReadLine());
        Console.WriteLine(MinEatingSpeed(piles, h));
    }
}

