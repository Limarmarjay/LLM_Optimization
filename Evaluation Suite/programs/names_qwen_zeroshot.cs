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