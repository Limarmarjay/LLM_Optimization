// 3.
using System;
using System.Text;

namespace CodeForce
{
    public class Program
    {
        public static void Main()
        {
            // Read the single integer n
            var line = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(line))
                return;

            int n = int.Parse(line);

            // If there are no throws (n == 1), print an empty line.
            if (n == 1)
            {
                Console.WriteLine();
                return;
            }

            // We will build the answer in a StringBuilder.
            // The result contains exactly n-1 numbers, so we pre-allocate.
            var sb = new StringBuilder(n * 3); // rough estimate

            int currentKid = 1;          // ball starts with kid 1
            for (int pass = 1; pass <= n - 1; pass++)
            {
                // next kid = (currentKid + pass) modulo n, but 1-based
                int nextKid = (currentKid + pass - 1) % n + 1;
                sb.Append(nextKid);
                if (pass < n - 1) sb.Append(' ');   // avoid trailing space
                currentKid = nextKid;
            }

            Console.WriteLine(sb.ToString());
        }
    }
}