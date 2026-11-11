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
            var pass = 1;
            var kid = 1;
            var result = new StringBuilder();
            while (throws > 0)
            {
                var targetPos = kid + pass;
                if (targetPos <= n)
                {
                    kid = targetPos;
                }
                else
                {
                    kid = targetPos - n;
                }
                throws--;
                pass++;
                result.Append($"{kid} ");
            }
 
            result.Remove(result.Length - 1, 1);
            return result.ToString();
        }
    }
}