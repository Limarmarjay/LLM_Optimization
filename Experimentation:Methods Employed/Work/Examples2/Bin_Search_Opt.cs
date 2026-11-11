using System;
using System.Linq;

class Program
{
    static int Bin_Search(int[] nums, int target)
    {
        int l = 0, r = nums.Length - 1;
        while (l <= r)
        {
            int m = l + (r - l) / 2;
            if (nums[m] > target)
            {
                r = m - 1;
            }
            else if (nums[m] < target)
            {
                l = m + 1;
            }
            else
            {
                return m;
            }
        }
        return -1;
    }

    static void Main()
    {
        int[] nums = Console.ReadLine().Split().Select(int.Parse).ToArray();
        int target = int.Parse(Console.ReadLine());
        Console.WriteLine(Bin_Search(nums, target));
    }
}