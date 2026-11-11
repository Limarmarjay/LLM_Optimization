// EASY (Based on Leetcode's Difficulty Rankings)

// Question 1 - BINARY SEARCH
// OPTIMIZED SOLUTION
static int SearchOpt(int[] nums, int target) {
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
// UNOPTIMIZED SOLUTION
static int SearchUnop(int[] nums, int target)
{
    int leftInd = 0;
    int rightInd = nums.Length - 1;

    if (nums.Length == 1)
    {
        if (nums[leftInd] != target)
        {
            return -1;
        }
    }
    while (leftInd <= rightInd)
    {
        int midPoint = (leftInd + rightInd) / 2;

        foreach (int item in nums)
        {
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
    }
    return -1;
}


// QUESTION 1 TEST CASE(S)
int[] nums = { -1, 0, 3, 5, 9, 12 };
int target = 0;

// Question 2 - GUESS NUMBER HIGHER OR LOWER
int pick;
static int guess(int num)
{
    if (num > pick)
    {
        return -1;
    }
    else if (num < pick)
    {
        return 1;
    }
    return 0;
}

// OPTIMIZED SOLUTION
static int GuessNumberOpt(int n)
{
    int l = 1, r = n;
    while (l <= r)
    {
        int m = l + (r - l) / 2;
        int res = guess(m);
        if (res > 0)
        {
            l = m + 1;
        }
        else if (res < 0)
        {
            r = m - 1;
        }
        else
        {
            return m;
        }
    }
    return -1;
}
// UNOPTIMIZED SOLUTION
static int GuessNumberUnop(int n)
{
    for (int i = 1; i < n; i++) // Logical Bug here
    {
        if (guess(i) == 0)
        {
            return i;
        }
    }
    return -1;
}

// QUESTION 2 TEST CASE(S)
int n = 50;

// Question 3 - SQRT(X)
// OPTIMIZED SOLUTION
static int MySqrtOpt(int x)
{
    int l = 0, r = x;
    int res = 0;
    while (l <= r)
    {
        int m = l + (r - l) / 2;
        long sq = (long)m * m;
        if (sq > x)
        {
            r = m - 1;
        }
        else if (sq < x)
        {
            l = m + 1;
            res = m;
        }
        else
        {
            return m;
        }
    }
    return res;
}
// UNOPTIMIZED SOLUTION
static int MySqrtUnop(int x)
{
    int ans = 0;
    for (int i = 0; i <= x; i++)
    {
        if ((long)i * i <= x)
        {
            ans = i;
        }
    }
    return ans;
}
// QUESTION 3 TEST CASE(S)
int x = 9;

// MEDIUM (Based on Leetcode's Difficulty Rankings)

// Question 1 - KOKO EATING BANANAS
// OPTIMIZED SOLUTION
static int MinEatingSpeedOpt(int[] piles, int h)
{
    int l = 1, r = piles.Max();
    int res = r;
    while (l <= r)
    {
        int k = l + (r - l) / 2;
        long hrs = 0;
        foreach (int p in piles)
        {
            hrs += (long)Math.Ceiling((double)p / k);
        }
        if (hrs <= h)
        {
            res = Math.Min(res, k);
            r = k - 1;
        }
        else
        {
            l = k + 1;
        }
    }
    return res;
}
// UNOPTIMIZED SOLUTION
static int MinEatingSpeedUnop(int[] piles, int h)
{
    int max = piles.Max();
    for (int speed = 1; speed <= max; speed++)
    {
        long time = 0;
        foreach (int pile in piles)
        {
            if (time > h)
            {
                break;
            }
            time += (pile + speed - 1) / speed;
        }
        if (time <= h)
        {
            return speed;
        }
    }
    return -1;
}
// QUESTION 4 TEST CASE(S)
int[] piles = {2, 4, 8, 9};
int h = 7;

// Question 2 - SEARCH A 2D MATRIX
// OPTIMIZED SOLUTION
static bool SearchMatrixOpt(int[][] matrix, int target)
{
    int rows = matrix.Length, cols = matrix[0].Length;
    int top = 0, bot = rows - 1;
    while (top <= bot)
    {
        int row = top + (bot - top) / 2;
        if (target > matrix[row][cols - 1])
        {
            top = row + 1;
        }
        else if (target < matrix[row][0])
        {
            bot = row - 1;
        }
        else
        {
            break;
        }
    }
    if (!(top <= bot))
    {
        return false;
    }
    int midRow = top + (bot - top) / 2;
    int l = 0, r = cols - 1;
    while (l <= r)
    {
        int m = l + (r - l) / 2;
        if (target > matrix[midRow][m])
        {
            l = m + 1;
        }
        else if (target < matrix[midRow][m])
        {
            r = m - 1;
        }
        else
        {
            return true;
        }
    }
    return false;
}
// UNOPTIMIZED SOLUTION
static bool SearchMatrixUnop(int[][] matrix, int target)
{
    int Rows = matrix.Length;
    int Cols = matrix[0].Length;
    for (int r = 0; r < Rows; r++)
    {
        for (int c = 0; c < Cols; c++)
        {
            if (matrix[r][c] == target)
            {
                return true;
            }
        }
    }
    return false;
}
// QUESTION 5 TEST CASE(S)
int[][] matrix = {{1, 2, 3, 5}, 
                  {7, 9, 11, 13}, 
                  {15, 17, 19, 21}};
int target = 5;
