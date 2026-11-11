// 4.
using System;
using System.IO;

class Program
{
    const long MOD = 1_000_000_007L;

    static void Main()
    {
        var fs = new FastScanner();
        int n = fs.NextInt();
        int m = fs.NextInt();

        // for every position keep a bit mask of letters that appear there
        long[] mask = new long[m];

        for (int i = 0; i < n; i++)
        {
            string s = fs.NextToken();          // name
            for (int j = 0; j < m; j++)
            {
                int bit = s[j] - 'A';           // 0 … 25 (letters are uppercase)
                mask[j] |= 1L << bit;
            }
        }

        long answer = 1;
        foreach (long bits in mask)
        {
            int cnt = PopCount(bits);          // number of different letters
            answer = (answer * cnt) % MOD;
        }

        Console.WriteLine(answer);
    }

    // pop-count for a 64-bit value – very fast
    static int PopCount(long x)
    {
        int cnt = 0;
        while (x != 0)
        {
            x &= x - 1;
            cnt++;
        }
        return cnt;
    }

    /* ---------- fast scanner ----------
       reads integers and tokens from stdin
       -----------------------------------*/
    class FastScanner
    {
        private readonly byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        private readonly Stream stream;

        public FastScanner(Stream stream = null)
        {
            this.stream = stream ?? Console.OpenStandardInput();
        }

        private int ReadByte()
        {
            if (ptr >= len)
            {
                len = stream.Read(buffer, 0, buffer.Length);
                ptr = 0;
                if (len == 0) return -1;
            }
            return buffer[ptr++];
        }

        public int NextInt()
        {
            int c;
            do { c = ReadByte(); } while (c <= 32 && c >= 0);

            int sign = 1;
            if (c == '-')
            {
                sign = -1;
                c = ReadByte();
            }

            int val = 0;
            while (c > 32 && c >= 0)
            {
                val = val * 10 + (c - '0');
                c = ReadByte();
            }
            return val * sign;
        }

        public string NextToken()
        {
            int c;
            do { c = ReadByte(); } while (c <= 32 && c >= 0);

            var sb = new System.Text.StringBuilder();
            while (c > 32 && c >= 0)
            {
                sb.Append((char)c);
                c = ReadByte();
            }
            return sb.ToString();
        }
    }
}


