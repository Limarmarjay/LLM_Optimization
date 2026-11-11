using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.IO;

//long a = long.Parse(Console.In.ReadLine());
//int a = int.Parse(Console.In.ReadLine());

//string[] ss = Console.In.ReadLine().Split(new char[] { ' ' });
//long l = long.Parse(ss[0]);
//int l = int.Parse(ss[0]);

class c108_p3
{
    static void Main()
    {
        new c108_p3().myMain();
    }

    void myMain()
    {
        //Console.SetIn(new StreamReader(new FileStream("../../in.txt", FileMode.Open)));
        //StreamWriter out_sw = new StreamWriter(new FileStream("../../out.txt", FileMode.Create));
        //Console.SetOut(out_sw);

        string[] ss = Console.In.ReadLine().Split(new char[] { ' ' });
        int n = int.Parse(ss[0]);
        int m = int.Parse(ss[1]);
        string[] names = new string[n];
        for (int i = 0; i < n; i++)
            names[i] = Console.In.ReadLine();
        long number = 1;
        for (int k = 0; k < m; k++)
        {
            char[] chs = new char[n];
            for (int i = 0; i < n; i++)
                chs[i] = names[i][k];
            number = (number * chs.Distinct().Count()) % 1000000007;
        }

        Console.Out.WriteLine(number);
        //out_sw.Close();
    }
}