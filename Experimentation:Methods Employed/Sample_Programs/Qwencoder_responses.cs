/* 
MULTI-SHOT
*/
// 1. 
using System;
using System.Linq;

namespace _38A
{
    class Program
    {
        static void Main(string[] args)
        {
            int N = int.Parse(Console.ReadLine());
            int[] cont = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int[] temp = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int pos = temp[0], dest = temp[1], ans = 0;

            // Calculate the number of years needed to reach rank b from rank a
            for (int i = pos - 1; i < dest - 1; i++)
            {
                ans += cont[i];
            }

            Console.WriteLine(ans);
        }
    }
}

// 2.
using System;
using System.Collections.Generic;
using System.Linq;

namespace ProblemB
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = int.Parse(Console.ReadLine());
            string[] token = Console.ReadLine().Split();
            HashSet<int> seen = new HashSet<int>();

            foreach (string s in token)
            {
                int num = int.Parse(s);
                seen.Add(num);
            }

            int result = 0;
            for (int i = 1; i <= n; i++)
            {
                if (!seen.Contains(i))
                {
                    result++;
                }
            }

            Console.WriteLine(result);
        }
    }
}

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

// 4.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.IO;

class c108_p3
{
    static void Main()
    {
        new c108_p3().myMain();
    }

    void myMain()
    {
        string[] ss = Console.In.ReadLine().Split(new char[] { ' ' });
        int n = int.Parse(ss[0]);
        int m = int.Parse(ss[1]);
        string[] names = new string[n];
        for (int i = 0; i < n; i++)
            names[i] = Console.In.ReadLine();

        long number = 1;
        for (int k = 0; k < m; k++)
        {
            Dictionary<char, int> charCount = new Dictionary<char, int>();
            for (int i = 0; i < n; i++)
            {
                char c = names[i][k];
                if (!charCount.ContainsKey(c))
                    charCount[c] = 0;
                charCount[c]++;
            }
            number = (number * charCount.Count) % 1000000007;
        }

        Console.Out.WriteLine(number);
    }
}



/* 
ZERO-SHOT
*/
// 1. 
using System;
using System.Linq;
namespace _38A
{
    class Program
    {
        static void Main(string[] args)
        {
            int N = int.Parse(Console.ReadLine());
            int[] cont = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int[] temp = Console.ReadLine().Split().Select(int.Parse).ToArray();
            int pos = temp[0], dest = temp[1], ans = 0;
            for (int i = pos - 1; i <= dest - 2; i++)
                ans += cont[i];
            Console.WriteLine(ans);
        }
    }
}

// 2. 
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ProblemB
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = int.Parse(Console.ReadLine());
            int[] a = new int[5001];
            int[] count = new int[5001];

            string[] token = Console.ReadLine().Split();
            foreach (string t in token)
            {
                int tmp = int.Parse(t);
                a[tmp]++;
                count[tmp] = 1;
            }

            int result = 0;
            for (int i = 1; i <= n; i++)
            {
                if (count[i] == 0)
                {
                    result++;
                }
                else if (count[i] > 1)
                {
                    result += count[i] - 1;
                }
            }
            Console.WriteLine(result);
        }
    }
}

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
            var pass = 1;
            var kid = 1;
            var result = new StringBuilder();
            var cumulativePos = kid;
            while (throws > 0)
            {
                cumulativePos += pass;
                if (cumulativePos >= n)
                {
                    kid = cumulativePos - n + 1;
                }
                else
                {
                    kid = cumulativePos;
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

// 4.
using System;
using System.Collections.Generic;
using System.Linq;

class c108_p3
{
    static void Main()
    {
        new c108_p3().myMain();
    }

    void myMain()
    {
        string[] ss = Console.In.ReadLine().Split(new char[] { ' ' });
        int n = int.Parse(ss[0]);
        int m = int.Parse(ss[1]);
        string[] names = new string[n];
        for (int i = 0; i < n; i++)
            names[i] = Console.In.ReadLine();
        long number = 1;
        for (int k = 0; k < m; k++)
        {
            HashSet<char> distinctChars = new HashSet<char>();
            for (int i = 0; i < n; i++)
                distinctChars.Add(names[i][k]);
            number = (number * distinctChars.Count) % 1000000007;
        }

        Console.Out.WriteLine(number);
    }
}