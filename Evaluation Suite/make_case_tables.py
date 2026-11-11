#!/usr/bin/env python3
"""APPENDIX TABLES: runtime on every test case.

Usage:  python3 make_case_tables.py
Reads   timing_cases.csv   (written by time_cases.py)
        correctness.csv    (written by check_all.py)
Writes  case_tables.md     (one table per task and language, ready to paste into Google Docs)
        case_tables.csv    (the same tables in one CSV, for Sheets or Excel)

Rows = test cases (and an Average row). Columns = the baseline and all four generated programs
(gpt-oss zero-shot, gpt-oss multi-shot, Qwen2.5-Coder zero-shot, Qwen2.5-Coder multi-shot).
A program that did not pass every test case was not timed, so its cells show "-".
"""
import csv, os, statistics
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
tpath = os.path.join(HERE, "timing_cases.csv")
cpath = os.path.join(HERE, "correctness.csv")
for p, hint in ((tpath, "Run time_cases.py first."), (cpath, "Run check_all.py first.")):
    if not os.path.exists(p):
        raise SystemExit(f"{os.path.basename(p)} not found. {hint}")

MODELS = {"gptoss": "gpt-oss", "qwen": "Qwen2.5-Coder"}
CONDS = {"zeroshot": "zero-shot", "multishot": "multi-shot"}
ORDER = [("gptoss", "zeroshot"), ("gptoss", "multishot"), ("qwen", "zeroshot"), ("qwen", "multishot")]
LANG = {"py": "Python", "cs": "C#"}

# every program that exists, per (task, lang), from correctness.csv
groups = OrderedDict()
for r in csv.DictReader(open(cpath)):
    g = groups.setdefault((r["task"], r["lang"]), {"cases": [], "base": {}, "times": {}})
    g["times"].setdefault((r["model"], r["condition"]), {})

for r in csv.DictReader(open(tpath)):
    g = groups.setdefault((r["task"], r["lang"]), {"cases": [], "base": {}, "times": {}})
    if r["case"] not in g["cases"]:
        g["cases"].append(r["case"])
    if r["baseline_ms"]:
        g["base"][r["case"]] = float(r["baseline_ms"])
    g["times"].setdefault((r["model"], r["condition"]), {})[r["case"]] = float(r["mean_ms"]) if r["mean_ms"] else None


def fmt(v):
    return "-" if v is None else f"{v:.1f}"


def avg(d, cases):
    vals = [d.get(c) for c in cases]
    return None if (not d or any(v is None for v in vals)) else statistics.mean(vals)


md, out = [], []
for (task, lang), g in groups.items():
    cases = sorted(g["cases"])
    if not cases:
        continue
    keys = [k for k in ORDER if k in g["times"]]
    labels = [f"{MODELS.get(m, m)} {CONDS.get(c, c)}" for m, c in keys]
    head = ["Test case", "Baseline"] + labels
    body = [[c, fmt(g["base"].get(c))] + [fmt(g["times"][k].get(c)) for k in keys] for c in cases]
    body.append(["Average", fmt(avg(g["base"], cases))] + [fmt(avg(g["times"][k], cases)) for k in keys])
    title = f"{task} ({LANG.get(lang, lang)}): runtime (ms) on each test case"
    md.append(f"**{title}**\n")
    md.append("| " + " | ".join(head) + " |")
    md.append("|" + "|".join(["---"] * len(head)) + "|")
    for b in body:
        md.append("| " + " | ".join(b) + " |")
    md.append("")
    out.append([title]); out.append(head); out.extend(body); out.append([])

open(os.path.join(HERE, "case_tables.md"), "w").write("\n".join(md))
with open(os.path.join(HERE, "case_tables.csv"), "w", newline="") as f:
    csv.writer(f).writerows(out)
print(f"wrote case_tables.md and case_tables.csv ({len([g for g in groups.values() if g['cases']])} tables)")
