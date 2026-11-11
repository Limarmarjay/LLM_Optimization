// QwenCoder
using System;

class Program
{
    static int Sqrt2(int x)
    {
        if (x <= 1)
        {
            return x;
        }
        int left = 1, right = x;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if ((long)mid * mid <= x)
            {
                left = mid + 1;
            }
            else
            {
                right = mid;
            }
        }
        return left - 1;
    }

    static void Main()
    {
        int x = int.Parse(Console.ReadLine());
        Console.WriteLine(Sqrt2(x));
    }
}