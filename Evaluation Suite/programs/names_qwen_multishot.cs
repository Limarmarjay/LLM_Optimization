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