#!/usr/bin/env python3
"""RESULT PER TEST CASE: Pass, Wrong output, Timeout or Crash for every program on every test case.

Usage:  python3 failure_report.py
Reads   correctness.csv (written by check_all.py), tests/<task>/NN.in and NN.out
Writes  failure_report.md   (one table per task and language, same layout as case_tables.md)
        failure_report.csv  (the same tables in one CSV)

Rows = test cases. Columns = the four generated programs. Each cell is:
  Pass          the output matched the expected output
  Wrong output  the program finished but its output differed (trailing whitespace and blank lines at the end are ignored)
  Timeout       no result within 10 s
  Crash         exception or non-zero exit code
Programs that passed every test case are not rerun: all their cells are Pass.
"""
import csv, os, subprocess
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "tests")
LIMIT = 10
TASK = {"berland": "Berland", "laces": "Laces", "names": "Little Vasya", "settlers": "Settlers",
        "ball": "Teacher Natalya", "perm": "Permutation"}
MODEL = {"gptoss": "gpt-oss", "qwen": "Qwen2.5-Coder"}
COND = {"zeroshot": "zero-shot", "multishot": "multi-shot"}
LANG = {"py": "Python", "cs": "C#"}
ORDER = [("gptoss", "zeroshot"), ("gptoss", "multishot"), ("qwen", "zeroshot"), ("qwen", "multishot")]


def norm(t):
    lines = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def result(cmd, folder, case):
    with open(os.path.join(folder, case + ".in")) as fin:
        try:
            r = subprocess.run(cmd, stdin=fin, capture_output=True, text=True, timeout=LIMIT)
        except subprocess.TimeoutExpired:
            return "Timeout"
    if r.returncode != 0:
        return "Crash"
    return "Pass" if norm(r.stdout) == norm(open(os.path.join(folder, case + ".out")).read()) else "Wrong output"


def main():
    cpath = os.path.join(HERE, "correctness.csv")
    if not os.path.exists(cpath):
        raise SystemExit("correctness.csv not found. Run check_all.py first.")
    groups = OrderedDict()   # (task, lang) -> {(model, cond): {case: result}}
    for r in csv.DictReader(open(cpath)):
        folder = os.path.join(TESTS, r["task"])
        cases = sorted(f[:-3] for f in os.listdir(folder) if f.endswith(".in"))
        if r["pass1"] == "yes":
            res = {c: "Pass" for c in cases}
        elif not r["run_cmd"]:
            res = {c: "Compile error" for c in cases}
        else:
            cmd = r["run_cmd"].split("|")
            res = {}
            for c in cases:
                print(f'{r["program"]:40s} case {c}', end="\r")
                res[c] = result(cmd, folder, c)
        groups.setdefault((r["task"], r["lang"]), {})[(r["model"], r["condition"])] = res
    md, out = [], []
    for (task, lang), progs in groups.items():
        keys = [k for k in ORDER if k in progs]
        cases = sorted(next(iter(progs.values())).keys())
        head = ["Test case"] + [f"{MODEL[m]} {COND[c]}" for m, c in keys]
        body = [[c] + [progs[k][c] for k in keys] for c in cases]
        body.append(["Passed"] + [f"{sum(1 for v in progs[k].values() if v == 'Pass')}/{len(cases)}" for k in keys])
        title = f"{TASK[task]} ({LANG[lang]}): result on each test case"
        md.append(f"**{title}**\n")
        md.append("| " + " | ".join(head) + " |")
        md.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in body:
            md.append("| " + " | ".join(b) + " |")
        md.append("")
        out.append([title]); out.append(head); out.extend(body); out.append([])
    open(os.path.join(HERE, "failure_report.md"), "w").write("\n".join(md))
    with open(os.path.join(HERE, "failure_report.csv"), "w", newline="") as f:
        csv.writer(f).writerows(out)
    print(" " * 70)
    print(f"wrote failure_report.md and failure_report.csv ({len(groups)} tables)")


main()
