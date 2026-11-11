#!/usr/bin/env python3
"""STEP 2 - EFFICIENCY (runtime and Opt@k). Run check_all.py first.

Usage:  python3 time_all.py                  (time every program that finishes on case 01)
        python3 time_all.py berland_qwen_multishot.cs     (time only the programs you name)
Reads   correctness.csv, baselines/ (the ORIGINAL programs: berland.py, berland.cs, perm.cs, ...), programs/unchanged.txt (optional: one program file name per line)
Writes  timing.csv  and  results.csv  (correctness + timing + Opt@k in one table)

Every program that finishes normally on test case 01 (the scoring input) is timed with
hyperfine (2 warm-ups, 10 timed runs, input from tests/<task>/01.in), correct or not.
Opt@k = passes every test AND mean runtime below the baseline AND not on the unchanged list.
"""
import csv, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "tests")
# mean runtimes of the unoptimized programs, in ms (from your hyperfine runs)
BASE = {("berland", "py"): 12.4, ("laces", "py"): 11.4, ("settlers", "py"): 13.0, ("names", "py"): 20.7,
        ("berland", "cs"): 20.3, ("perm", "cs"): 19.6, ("ball", "cs"): 14.9, ("names", "cs"): 17.0}
UNIT = {"ns": 1e-6, "us": 1e-3, "µs": 1e-3, "μs": 1e-3, "ms": 1.0, "s": 1000.0}
# hyperfine 1.x prints "Time (mean ± σ):  12.3 ms ±  0.4 ms"; hyperfine 2.x prints "Wall Time  12.3 ms ±  0.4 ms"
PAT = re.compile(r"(?:Time\s*\(mean\s*±\s*σ\)\s*:|Wall Time)\s*([\d.,]+)\s*(ns|µs|μs|us|ms|s)\s*±\s*([\d.,]+)\s*(ns|µs|μs|us|ms|s)")

def time_it(cmd, inp):
    quoted = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    r = subprocess.run(["hyperfine", "--warmup", "2", "--runs", "10", "--input", inp, quoted],
                       capture_output=True, text=True)
    text = r.stdout + "\n" + r.stderr
    m = PAT.search(text)
    if r.returncode != 0 or not m:
        return None, None, text.strip()[-300:]
    mean = float(m.group(1).replace(",", "")) * UNIT[m.group(2)]
    sd = float(m.group(3).replace(",", "")) * UNIT[m.group(4)]
    return mean, sd, ""

def time_baselines():
    """Time the ORIGINAL programs in baselines/ in this same session. Files: <task>.py or <task>.cs
    (task = berland, laces, settlers, names, perm, ball). Returns {(task, lang): mean_ms}."""
    bdir = os.path.join(HERE, "baselines")
    out = {}
    if not os.path.isdir(bdir): return out
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    alias = {"homework": "perm", "natalya": "ball", "natalia": "ball"}
    for f in sorted(os.listdir(bdir)):
        m = re.match(r"^([a-z]+)\.(py|cs)$", f)
        if not m: continue
        task, lang = alias.get(m.group(1), m.group(1)), m.group(2)
        path = os.path.join(bdir, f)
        if lang == "py": cmd = [sys.executable, path]
        else:
            exe = os.path.join(HERE, "build", "baseline_" + f[:-3] + ".exe")
            r = subprocess.run(["csc", f"-out:{exe}", path], capture_output=True, text=True)
            if r.returncode != 0: print("baseline compile error:", f); continue
            cmd = ["mono", exe]
        mean, sd, err = time_it(cmd, os.path.join(TESTS, task, "01.in"))
        if mean is None: print("baseline not timed:", f, err[:100]); continue
        out[(task, lang)] = mean
        print(f"BASELINE {f:20s} {mean:.1f} ms (sd {sd:.1f})")
    return out

def main():
    if not shutil.which("hyperfine"): sys.exit("hyperfine not found (brew install hyperfine)")
    cpath = os.path.join(HERE, "correctness.csv")
    if not os.path.exists(cpath): sys.exit("correctness.csv not found. Run check_all.py first.")
    rows = list(csv.DictReader(open(cpath)))
    only = set(sys.argv[1:])
    up = os.path.join(HERE, "programs", "unchanged.txt")
    unch = {l.strip() for l in open(up) if l.strip()} if os.path.exists(up) else set()
    old = {}
    tpath = os.path.join(HERE, "timing.csv")
    if only and os.path.exists(tpath): old = {r["program"]: r for r in csv.DictReader(open(tpath))}
    out = []
    fresh = time_baselines()
    if fresh: BASE.update(fresh); print("Using baselines timed in this session.\n")
    else: print("No baselines/ folder: using the stored baseline numbers in BASE.\n")
    for r in rows:
        f = r["program"]; base = BASE.get((r["task"], r["lang"]))
        if base: base = round(base, 1)
        t = dict(program=f, mean_ms="", sd_ms="", baseline_ms=base if base else "", faster="", timing_note="")
        if only and f not in only:
            if f in old: t.update({k: old[f][k] for k in ("mean_ms", "sd_ms", "faster", "timing_note")})
        elif r["runs_on_case01"] != "yes":
            t["timing_note"] = "no runtime (compile error, crash or timeout on case 01)"
        else:
            mean, sd, err = time_it(r["run_cmd"].split("|"), os.path.join(TESTS, r["task"], "01.in"))
            if mean is None:
                t["timing_note"] = "hyperfine output not read: " + err.replace("\n", " ")
            else:
                t.update(mean_ms=round(mean, 1), sd_ms=round(sd, 1))
                if base: t["faster"] = "yes" if mean < base else "no"
        print(f"{f:40s} mean {t['mean_ms']} ms (sd {t['sd_ms']})  baseline {t['baseline_ms']}  faster={t['faster']}  {t['timing_note']}")
        out.append(t)
    with open(tpath, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    merged = []
    for r, t in zip(rows, out):
        u = "yes" if r["program"] in unch else "no"
        opt = "yes" if (r["pass1"] == "yes" and t["faster"] == "yes" and u == "no") else "no"
        m = {k: r[k] for k in ("program", "task", "lang", "model", "condition", "passed", "total", "pass1", "notes")}
        m.update(mean_ms=t["mean_ms"], sd_ms=t["sd_ms"], baseline_ms=t["baseline_ms"], faster=t["faster"], unchanged=u, opt1=opt)
        merged.append(m)
    with open(os.path.join(HERE, "results.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(merged[0].keys())); w.writeheader(); w.writerows(merged)
    print("\nwrote timing.csv and results.csv")

main()
