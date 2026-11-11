"""Type of each test case, from the descriptions in tests/<task>/README.txt.

Types: Regular, Sample, Boundary, Corner case, Large input, Varied input.
Edit a line here if you classify a case differently; failure_report.py and make_case_tables.py both read this file.
"""

R, S, B, C, L, V = "Regular", "Sample", "Boundary", "Corner case", "Large input", "Varied input"

TYPES = {
    # 01 scoring case; 02 sample; 03 n=2; 04-10 n=3..9; 11-13 n=20,50,64; 14 n=99; 15 n=100
    "ball":     [R, S, B, B, B, B, B, B, B, B, V, V, V, B, B],
    # 01 scoring; 02 minimum; 03 n=3 whole range; 04 n=100 all d=100; 05 last step only; 06 first step only; 07 all d=1; 08-15 random
    "berland":  [R, B, B, B, B, B, C, V, V, V, V, V, V, V, V],
    # 01 scoring; 02-03 no laces; 04-05 samples; 06 two isolated edges; 07 single edge; 08 cycle of 10;
    # 09 path of 100; 10 star of 99 leaves; 11 complete graph; 12 triangle with long tail; 13-18 random sparse
    "laces":    [R, B, B, S, S, C, B, C, C, C, C, C, V, V, V, V, V, V],
    # 01 scoring; 02 sample; 03 one name one letter; 04 one name 100 letters; 05 all identical; 06 100 names 1 letter;
    # 07 26 distinct letters per column; 08-09 100 x 100; 10 two different names; 11-15 random
    "names":    [R, S, B, B, C, B, C, L, L, C, V, V, V, V, V],
    # 01 scoring; 02 sample; 03 n=1 value 1; 04 n=1 value 5000; 05 all 1; 06 all larger than n; 07 n=2 values 2 2;
    # 08 shuffled n=100; 09-12 n=5000; 13-16 random
    "perm":     [R, S, B, B, C, C, B, C, L, L, L, L, V, V, V, V],
    # 01 scoring; 02 sample; 03 already all k; 04-05 single soldier; 06-07 n=100 all rank 1; 08 distinct ranks 1..100;
    # 09 one below k; 10 ranks 1 then all k; 11 two groups; 12-17 random
    "settlers": [R, S, C, B, B, L, L, C, C, C, C, V, V, V, V, V, V],
}


def case_type(task, case):
    """Type of test case NN (a string like '07') of a task, or '-' if unknown."""
    try:
        return TYPES[task][int(case) - 1]
    except (KeyError, IndexError, ValueError):
        return "-"
