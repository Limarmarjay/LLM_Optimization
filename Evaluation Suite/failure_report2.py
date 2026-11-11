#!/usr/bin/env python3
"""TYPE OF ERROR PER TEST CASE: None, Wrong output, Timeout or Crash for every program on every test case.

Usage:  python3 failure_report.py
Reads   correctness.csv and baseline_correctness.csv (written by check_all.py), tests/<task>/NN.in and NN.out
Writes  correctness_tables.md   (one table per task and language, same layout as case_tables.md)
        correctness_tables.csv  (the same tables in one CSV)

Rows = test cases. Columns = the baseline and the four generated programs. Each cell is:
  None          no error: the output matched the expected output
  Wrong output  the program finished but its output differed (trailing whitespace and blank lines at the end are ignored)
  Timeout       no result within 10 s
  Crash         exception or non-zero exit code
Programs that passed every test case are not rerun: all their cells are None.
The Baseline column is the unoptimized program (None on every test case if it passed all of them, as recorded in baseline_correctness.csv).
The Type column is the kind of test case (see test_types.py).
"""
import csv, os, subprocess, sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_types import case_type

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
    return "None" if norm(r.stdout) == norm(open(os.path.join(folder, case + ".out")).read()) else "Wrong output"


def main():
    cpath = os.path.join(HERE, "correctness.csv")
    if not os.path.exists(cpath):
        raise SystemExit("correctness.csv not found. Run check_all.py first.")
    base_ok = {}   # (task, lang) -> True if the baseline passed every test case
    bpath = os.path.join(HERE, "baseline_correctness.csv")
    if os.path.exists(bpath):
        for b in csv.DictReader(open(bpath)):
            base_ok[(b["task"], b["lang"])] = b["total"] != "0" and b["passed"] == b["total"]
    groups = OrderedDict()   # (task, lang) -> {(model, cond): {case: result}}
    for r in csv.DictReader(open(cpath)):
        folder = os.path.join(TESTS, r["task"])
        cases = sorted(f[:-3] for f in os.listdir(folder) if f.endswith(".in"))
        if r["pass1"] == "yes":
            res = {c: "None" for c in cases}
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
        head = ["Test case", "Type", "Baseline"] + [f"{MODEL[m]} {COND[c]}" for m, c in keys]
        base = "None" if base_ok.get((task, lang)) else "-"   # the baseline passed every test case
        body = [[c, case_type(task, c), base] + [progs[k][c] for k in keys] for c in cases]
        body.append(["Passed", "", f"{len(cases)}/{len(cases)}" if base == "None" else "-"] + [f"{sum(1 for v in progs[k].values() if v == 'None')}/{len(cases)}" for k in keys])
        title = f"{TASK[task]} ({LANG[lang]}): type of error on each test case (if any)"
        md.append(f"**{title}**\n")
        md.append("| " + " | ".join(head) + " |")
        md.append("|" + "|".join(["---"] * len(head)) + "|")
        for b in body:
            md.append("| " + " | ".join(b) + " |")
        md.append("")
        out.append([title]); out.append(head); out.extend(body); out.append([])
    open(os.path.join(HERE, "correctness_tables.md"), "w").write("\n".join(md))
    with open(os.path.join(HERE, "correctness_tables.csv"), "w", newline="") as f:
        csv.writer(f).writerows(out)
    print(" " * 70)
    print(f"wrote correctness_tables.md and correctness_tables.csv ({len(groups)} tables)")


main()
