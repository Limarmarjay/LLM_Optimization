// gpt-oss
using System;

class Program
{
    static int Sqrt(int x)
    {
        if (x < 2) return x; // 0 or 1

        int left = 1;
        int right = Math.Min(x, 46340); // sqrt(2^31-1) < 46341
        int ans = 1;

        while (left <= right)
        {
            int mid = left + (right - left) / 2;
            int sq = mid * mid;

            if (sq == x) return mid;
            if (sq < x)
            {
                ans = mid;
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        return ans;
    }

    static void Main()
    {
        int x = int.Parse(Console.ReadLine());
        Console.WriteLine(Sqrt(x));
    }
}
