// 4.
using System;
using System.IO;
using System.Text;

class Program
{
    const int MOD = 1_000_000_007;

    /* ---------- fast scanner ---------- */
    sealed class FastScanner
    {
        private readonly Stream _stream;
        private readonly byte[] _buffer = new byte[1 << 16];
        private int _ptr = 0, _len = 0;

        public FastScanner(Stream stream) { _stream = stream; }

        private int Read()
        {
            if (_ptr >= _len)
            {
                _len = _stream.Read(_buffer, 0, _buffer.Length);
                _ptr = 0;
                if (_len == 0) return -1;
            }
            return _buffer[_ptr++];
        }

        public int NextInt()
        {
            int c, sign = 1, val = 0;
            do { c = Read(); } while (c <= ' ' && c != -1);
            if (c == '-') { sign = -1; c = Read(); }
            while (c > ' ')
            {
                val = val * 10 + (c - '0');
                c = Read();
            }
            return val * sign;
        }

        public string Next()
        {
            int c;
            var sb = new StringBuilder();
            do { c = Read(); } while (c <= ' ' && c != -1);
            while (c > ' ')
            {
                sb.Append((char)c);
                c = Read();
            }
            return sb.ToString();
        }
    }
    /* ---------------------------------- */

    static void Main()
    {
        var fs = new FastScanner(Console.OpenStandardInput());

        int n = fs.NextInt();
        int m = fs.NextInt();

        string[] names = new string[n];
        for (int i = 0; i < n; i++) names[i] = fs.Next();

        long result = 1;

        for (int pos = 0; pos < m; pos++)
        {
            int mask = 0;          // bit mask for A-Z
            int distinct = 0;

            for (int i = 0; i < n; i++)
            {
                int bit = names[i][pos] - 'A';   // assume only uppercase letters
                if ((mask & (1 << bit)) == 0)
                {
                    mask |= 1 << bit;
                    distinct++;
                }
            }

            result = (result * distinct) % MOD;
        }

        Console.WriteLine(result);
    }
}

