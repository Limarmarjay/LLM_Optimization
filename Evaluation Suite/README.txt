Multi-case test sets (input + expected output) for the six tasks.

Folders: berland (Berland ranks), laces (Anna and Maria), settlers (Settlers training),
names (Little Vasya names), perm (Polycarpus permutation), ball (Teacher Natalia ball game).
Each folder has NN.in, NN.out and a README.txt describing each case. Case 01 is always the
scoring test case used for timing. Expected outputs come from an independent solver and were
checked against a port of the original unoptimized program on every case.

Python tasks:  python3 check.py berland python3 your_program.py
C# tasks:      python3 check.py perm mono your_program.exe
Pass@1 = the program passes every case in the folder. Opt@1 = Pass@1 and faster than the baseline.
Timing (hyperfine) uses case 01:  hyperfine --warmup 2 --runs 10 --input berland/01.in 'python3 prog.py'
Put the generated programs in programs/ (see the header of run_all.py for the naming).
One file name per line in programs/unchanged.txt marks programs identical to the original.
