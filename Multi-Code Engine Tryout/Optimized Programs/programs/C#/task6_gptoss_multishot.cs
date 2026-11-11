// 2. 
using System;
class FastScanner
{
    private string[] _buffer;
    private int _index;

    public FastScanner()
    {
        _buffer = Array.Empty<string>();
        _index = 0;
    }

    public int NextInt()
    {
        while (_index >= _buffer.Length)
        {
            string line = Console.ReadLine();
            if (line == null) throw new InvalidOperationException("Unexpected end of input");
            _buffer = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
            _index = 0;
        }
        return int.Parse(_buffer[_index++]);
    }
}
class Program
{
    static void Main()
    {
        var fs = new FastScanner();

        int n = fs.NextInt();                 // size of the array
        bool[] seen = new bool[n + 1];        // 1-based index

        for (int i = 0; i < n; i++)
        {
            int value = fs.NextInt();        // read the element
            if (value >= 1 && value <= n)   // only numbers inside 1..n matter
                seen[value] = true;          // mark that the value exists
        }

        int missing = 0;
        for (int i = 1; i <= n; i++)
            if (!seen[i])
                missing++;                  // i is absent – one change needed

        Console.WriteLine(missing);
    }
}

