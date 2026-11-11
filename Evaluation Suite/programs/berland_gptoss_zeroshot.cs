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