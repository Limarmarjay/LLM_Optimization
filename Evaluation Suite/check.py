#!/usr/bin/env python3
"""Run a program on every test case in a folder and compare with the expected output.

Usage:   python3 check.py <test_folder> <command...>
Example: python3 check.py berland python3 berland_gptoss.py
         python3 check.py perm mono homework_gptoss.exe

A test passes when the program's standard output equals the expected output,
ignoring trailing whitespace on each line and trailing blank lines.
A crash, a non-zero exit code, or running longer than 10 seconds is a failure.
"""
import os, subprocess, sys

def norm(t):
    lines = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "": lines.pop()
    return lines

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    folder, cmd = sys.argv[1], sys.argv[2:]
    names = sorted(f[:-3] for f in os.listdir(folder) if f.endswith(".in"))
    passed = 0
    for nm in names:
        with open(os.path.join(folder, nm + ".in")) as fin:
            try:
                r = subprocess.run(cmd, stdin=fin, capture_output=True, text=True, timeout=10)
                got, rc, err = r.stdout, r.returncode, r.stderr.strip().splitlines()[-1:] 
            except subprocess.TimeoutExpired:
                print(f"{nm}  FAIL (timeout > 10 s)"); continue
        want = open(os.path.join(folder, nm + ".out")).read()
        if rc != 0:
            print(f"{nm}  FAIL (crash, exit code {rc}) {err[0] if err else ''}")
        elif norm(got) == norm(want):
            print(f"{nm}  PASS"); passed += 1
        else:
            g = " ".join(got.split())[:60]; w = " ".join(want.split())[:60]
            print(f"{nm}  FAIL (got: {g!r}  expected: {w!r})")
    print(f"PASSED {passed}/{len(names)}" + ("  -> Pass@1 = yes" if passed == len(names) else "  -> Pass@1 = no"))
    sys.exit(0 if passed == len(names) else 1)

main()
