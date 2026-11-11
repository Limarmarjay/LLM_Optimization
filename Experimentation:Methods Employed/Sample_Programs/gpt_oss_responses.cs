/* 
MULTI-SHOT
*/
// 1. 
using System;
class Program
{
    static void Main()
    {
        // Number of ranks (not used directly, but read to match input format)
        int n = int.Parse(Console.ReadLine());

        // Read the array of years needed to move from rank i to i+1
        int[] years = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);

        // Read current rank (pos) and desired rank (dest)
        int[] posDest = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);
        int pos = posDest[0];
        int dest = posDest[1];

        // Sum the years needed to go from pos to dest-1
        long totalYears = 0;
        for (int i = pos - 1; i < dest - 1; i++)
        {
            totalYears += years[i];
        }

        Console.WriteLine(totalYears);
    }
}

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

// 3.
using System;
using System.Text;
class Program
{
    static void Main()
    {
        // Read the single integer n
        if (!int.TryParse(Console.ReadLine(), out int n))
            return;

        // If there are no throws, just output an empty line
        if (n <= 1)
        {
            Console.WriteLine();
            return;
        }

        var sb = new StringBuilder();
        int sumMod = 0;                     // current (1-based) sum modulo n

        // t is the number of the current throw (1 … n-1)
        for (int t = 1; t < n; t++)
        {
            // cumulative distance after t throws, modulo n
            sumMod = (sumMod + t) % n;

            // child that receives the ball
            sb.Append(sumMod + 1);

            // add a space except after the last number
            if (t < n - 1) sb.Append(' ');
        }

        Console.WriteLine(sb.ToString());
    }
}

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



/* 
ZERO-SHOT
*/
// 1. 
using System;
using System.IO;
using System.Text;

namespace BerlandArmedForces
{
    /// <summary>
    /// Fast input reader that parses integers from the standard input
    /// using a large byte buffer. It is much faster than the default
    /// Console.ReadLine / Split combination for large test cases.
    /// </summary>
    internal sealed class FastScanner
    {
        private const int BufferSize = 1 << 16;          // 64 KiB
        private readonly byte[] _buffer = new byte[BufferSize];
        private int _bytesRead = 0, _pos = 0;
        private readonly Stream _input;

        public FastScanner(Stream input = null)
        {
            _input = input ?? Console.OpenStandardInput();
        }

        /// <summary>
        /// Returns the next integer from the input stream.
        /// </summary>
        public int NextInt()
        {
            int result = 0;
            int sign = 1;

            // Skip non-numeric characters
            int b = ReadByte();
            while (b <= 32)
                b = ReadByte();

            // Handle optional sign
            if (b == '-')
            {
                sign = -1;
                b = ReadByte();
            }

            // Parse number
            while (b > 32)
            {
                result = result * 10 + (b - 48);
                b = ReadByte();
            }

            return result * sign;
        }

        /// <summary>
        /// Reads the next byte from the buffer, refilling it if necessary.
        /// </summary>
        private int ReadByte()
        {
            if (_pos >= _bytesRead)
            {
                _bytesRead = _input.Read(_buffer, 0, BufferSize);
                _pos = 0;
                if (_bytesRead == 0) // End of stream
                    return -1;
            }
            return _buffer[_pos++];
        }
    }

    internal class Program
    {
        private static void Main()
        {
            var scanner = new FastScanner();

            int n = scanner.NextInt();                 // number of ranks (not used explicitly)
            var durations = new int[n - 1];
            for (int i = 0; i < n - 1; i++)
                durations[i] = scanner.NextInt();

            int a = scanner.NextInt();                 // current rank
            int b = scanner.NextInt();                 // desired rank

            // Sum durations from rank a to rank b (exclusive of b)
            long totalYears = 0;
            for (int i = a - 1; i < b - 1; i++)
                totalYears += durations[i];

            Console.WriteLine(totalYears);
        }
    }
}

// 2. 
using System;
using System.Linq;

namespace ProblemB
{
    class Program
    {
        static void Main()
        {
            // Read number of elements
            int n = int.Parse(Console.ReadLine());

            // Read the sequence
            var a = Console.ReadLine()
                          .Split()
                          .Select(int.Parse)
                          .ToArray();

            // Track which numbers 1..n have already appeared
            bool[] seen = new bool[n + 1];
            int uniqueInRange = 0;

            foreach (int v in a)
            {
                // Keep the element only if it lies in 1..n and hasn't appeared before
                if (v >= 1 && v <= n && !seen[v])
                {
                    seen[v] = true;
                    uniqueInRange++;
                }
            }

            // Minimum changes = elements that cannot stay unchanged
            int result = n - uniqueInRange;
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

