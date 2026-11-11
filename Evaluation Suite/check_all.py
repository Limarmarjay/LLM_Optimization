#!/usr/bin/env python3
"""STEP 1 - CORRECTNESS (Pass@k). Compiles each program and runs it on every test case.

Usage:  python3 check_all.py
Reads   programs/<task>_<model>_<condition>.<py|cs>   (see README.txt for the names)
Writes  correctness.csv   (one row per program) and baseline_correctness.csv (the originals in baselines/) and build/*.exe (compiled C# programs)

A program passes (pass1 = yes) only if it passes EVERY test case in its task folder.
Output is compared ignoring trailing whitespace. Crash, wrong output, or >10 s = that case fails.
"""
import csv, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS, PROGS, BUILD = (os.path.join(HERE, x) for x in ("tests", "programs", "build"))
ALIAS = {"homework": "perm", "natalya": "ball", "natalia": "ball", "berland": "berland", "laces": "laces",
         "settlers": "settlers", "names": "names", "perm": "perm", "ball": "ball"}

def norm(t):
    L = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
    while L and L[-1] == "": L.pop()
    return L

def prepare(path, lang):
    if lang == "py": return [sys.executable, path], ""
    os.makedirs(BUILD, exist_ok=True)
    exe = os.path.join(BUILD, os.path.basename(path)[:-3] + ".exe")
    if os.path.exists(exe): os.remove(exe)
    r = subprocess.run(["csc", f"-out:{exe}", path], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(exe):
        msg = (r.stdout + r.stderr).strip().splitlines()
        return None, "compile error: " + (msg[0][:120] if msg else "")
    return ["mono", exe], ""

def run_case(cmd, inpath):
    with open(inpath) as fin:
        try:
            r = subprocess.run(cmd, stdin=fin, capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            return None, "timeout"
    return r, ("crash" if r.returncode != 0 else "")

def check_baselines():
    """Run the ORIGINAL programs in baselines/ on the same test cases (they should pass every case)."""
    bdir = os.path.join(HERE, "baselines")
    if not os.path.isdir(bdir): return
    out = []
    print("\nBASELINES (the original unoptimized programs):")
    for f in sorted(os.listdir(bdir)):
        m = re.match(r"^([a-z]+)\.(py|cs)$", f)
        if not m or m.group(1) not in ALIAS: continue
        task, lang = ALIAS[m.group(1)], m.group(2)
        cmd, err = prepare(os.path.join(bdir, f), lang)
        passed = total = 0; notes = err
        if cmd:
            folder = os.path.join(TESTS, task)
            names = sorted(x[:-3] for x in os.listdir(folder) if x.endswith(".in")); total = len(names); bad = []
            for nm in names:
                r, why = run_case(cmd, os.path.join(folder, nm + ".in"))
                if why: bad.append(f"{nm}:{why}"); continue
                if norm(r.stdout) == norm(open(os.path.join(folder, nm + ".out")).read()): passed += 1
                else: bad.append(f"{nm}:wrong")
            notes = " ".join(bad[:8])
        print(f"BASELINE {f:14s} passed {passed}/{total}  {'OK' if total and passed == total else 'CHECK THIS'}  {notes}")
        out.append(dict(program=f, task=task, lang=lang, passed=passed, total=total, notes=notes))
    if out:
        with open(os.path.join(HERE, "baseline_correctness.csv"), "w", newline="") as fo:
            w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
        print("wrote baseline_correctness.csv")

def main():
    rows = []
    for f in sorted(os.listdir(PROGS)):
        m = re.match(r"^([a-z]+)_(gptoss|qwen)_(zeroshot|multishot)\.(py|cs)$", f)
        if not m or "discarded" in f: continue
        t, model, cond, lang = m.groups()
        if t not in ALIAS: print("skip (unknown task):", f); continue
        task = ALIAS[t]
        cmd, err = prepare(os.path.join(PROGS, f), lang)
        row = dict(program=f, task=task, lang=lang, model=model, condition=cond, passed=0, total=0, pass1="no",
                   runs_on_case01="no", notes=err, run_cmd="|".join(cmd) if cmd else "")
        if cmd:
            folder = os.path.join(TESTS, task)
            names = sorted(x[:-3] for x in os.listdir(folder) if x.endswith(".in"))
            notes = []
            for nm in names:
                r, why = run_case(cmd, os.path.join(folder, nm + ".in"))
                if nm == "01" and r is not None and not why: row["runs_on_case01"] = "yes"
                if why: notes.append(f"{nm}:{why}"); continue
                if norm(r.stdout) == norm(open(os.path.join(folder, nm + ".out")).read()): row["passed"] += 1
                else: notes.append(f"{nm}:wrong")
            row.update(total=len(names), notes=" ".join(notes[:8]))
            row["pass1"] = "yes" if row["passed"] == row["total"] else "no"
        rows.append(row)
        print(f"{f:40s} passed {row['passed']}/{row['total']}  Pass@k={row['pass1']}  {row['notes']}")
    if not rows: sys.exit("no programs found in programs/")
    with open(os.path.join(HERE, "correctness.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("\nwrote correctness.csv")
    check_baselines()

main()
