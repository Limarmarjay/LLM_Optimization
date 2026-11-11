using System;

class Program
{
    static int Sqrt(int x)
    {
        int ans = 0;
        for (int i = 0; i <= x; i++)
        {
            if ((long)i * i <= x)
            {
                ans = i;
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