// 3.
using System;
using System.Text;

namespace CodeForce
{
    public class Program
    {
        static void Main(string[] args)
        {
            string input1 = Console.ReadLine();
            var answer = Solve(input1);
            Console.WriteLine(answer);
        }

        public static string Solve(string s)
        {
            var n = int.Parse(s);
            var throws = n - 1;
            var result = new StringBuilder();
            for (int i = 1; i <= throws; i++)
            {
                var kid = (2 * i - 1) % n + 1;
                result.Append($"{kid} ");
            }
            return result.ToString();
        }
    }
}