using System;

class Program
{
    static int Sqrt(int x)
    {
        int l = 0, r = x;
        int res = 0;
        while (l <= r)
        {
            int m = l + (r - l) / 2;
            long sq = (long)m * m;
            if (sq > x)
            {
                r = m - 1;
            }
            else if (sq < x)
            {
                l = m + 1;
                res = m;
            }
            else
            {
                return m;
            }
        }
        return res;
    }

    static void Main()
    {
        int x = int.Parse(Console.ReadLine());
        Console.WriteLine(Sqrt(x));
    }
}