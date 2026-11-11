using System;
using System.Linq;

class Program {    
    static int Bin_Search(int[] nums, int target)
    {
        int leftInd = 0;
        int rightInd = nums.Length - 1;

        while (leftInd <= rightInd)
        {
            int midPoint = leftInd + (rightInd - leftInd) / 2;

            if (nums[midPoint] == target)
            {
                return midPoint;
            }
            else if (nums[midPoint] < target)
            {
                leftInd = midPoint + 1;
            }
            else
            {
                rightInd = midPoint - 1;
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