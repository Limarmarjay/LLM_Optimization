// 3.
using System;
using System.Text;
class Program
{
    static void Main()
    {
        // Read the single integer n
        if (!int.TryParse(Console.ReadLine(), out int n))
            return;

        // If there are no throws, just output an empty line
        if (n <= 1)
        {
            Console.WriteLine();
            return;
        }

        var sb = new StringBuilder();
        int sumMod = 0;                     // current (1-based) sum modulo n

        // t is the number of the current throw (1 … n-1)
        for (int t = 1; t < n; t++)
        {
            // cumulative distance after t throws, modulo n
            sumMod = (sumMod + t) % n;

            // child that receives the ball
            sb.Append(sumMod + 1);

            // add a space except after the last number
            if (t < n - 1) sb.Append(' ');
        }

        Console.WriteLine(sb.ToString());
    }
}
