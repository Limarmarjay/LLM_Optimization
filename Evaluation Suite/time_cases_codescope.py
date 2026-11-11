#!/usr/bin/env python3
"""EFFICIENCY ON ALL TEST CASES, timed the CodeScope way (CPU time, psutil). Run check_all.py first.

Same as time_cases.py (your professor's rule: runtime per test case, then the average over all test cases),
but the TIMER is CodeScope's: it measures the program's CPU time (user + system) while it runs, instead of
hyperfine's wall-clock time. Nothing is compared inside the timer; Opt@1 is decided afterwards by YOUR rule.

Needs:  pip install psutil      (and python3, mono/csc on the machine)
Usage:  python3 time_cases_codescope.py              # CodeScope's own polling method (default)
        python3 time_cases_codescope.py rusage       # same CPU time read exactly from the OS after the program exits


Usage:  python3 time_cases.py
Reads   correctness.csv, baselines/ (the ORIGINAL programs: berland.py, berland.cs, perm.cs, ...),
        programs/unchanged.txt (optional: one program file name per line), tests/<task>/NN.in
Writes  timing_cases.csv   (one row per program and test case: its mean runtime on that case)
        results_avg.csv    (one row per program: Pass@1, average runtime, baseline average, Opt@1)

Only programs that passed EVERY test case (pass1 = yes) are timed. The ORIGINAL programs are timed
first, in the same session, on the same test cases.
For each test case, hyperfine runs the program (2 warm-ups, 10 timed runs, input from NN.in) and
gives a mean runtime. A program's runtime = the average of those per-case means over ALL test cases of its task.
Opt@1 = passes every test case AND average runtime below the original's average runtime AND not on the unchanged list.
"""
import csv, os, re, shutil, statistics, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(HERE, "tests")
ALIAS = {"homework": "perm", "natalya": "ball", "natalia": "ball"}
UNIT = {"ns": 1e-6, "us": 1e-3, "µs": 1e-3, "μs": 1e-3, "ms": 1.0, "s": 1000.0}
# hyperfine 1.x prints "Time (mean ± σ):  12.3 ms ±  0.4 ms"; hyperfine 2.x prints "Wall Time  12.3 ms ±  0.4 ms"
PAT = re.compile(r"(?:Time\s*\(mean\s*±\s*σ\)\s*:|Wall Time)\s*([\d.,]+)\s*(ns|µs|μs|us|ms|s)\s*±\s*([\d.,]+)\s*(ns|µs|μs|us|ms|s)")


METHOD = "psutil"
WARMUP, RUNS = 2, 10
LIMIT_S = 20.0


def _cpu_psutil(cmd, data):
    """CodeScope's method (test_opt_codes.py, count_memory_and_time): poll the process every 0.2 ms and keep the
    last CPU time seen (user + system + children). Returns seconds, or None on timeout/failure."""
    import psutil
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.stdin.write(data); p.stdin.close()
    cpu, t0 = 0.0, time.time()
    ps = psutil.Process(p.pid)
    while p.poll() is None:
        try:
            cpu = float(sum(ps.cpu_times()[:4]))
        except Exception:
            pass
        time.sleep(0.0002)
        if time.time() - t0 > LIMIT_S:
            p.kill(); p.wait(); return None
    return cpu if p.returncode == 0 else None


def _cpu_rusage(cmd, data):
    """Same quantity (CPU time = user + system), read exactly from the OS when the program exits."""
    import resource
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.stdin.write(data); p.stdin.close()
    t0 = time.time()
    while True:
        try:
            pid, status, ru = os.wait4(p.pid, os.WNOHANG)
        except ChildProcessError:
            return None
        if pid:
            p.returncode = 0
            return (ru.ru_utime + ru.ru_stime) if os.WEXITSTATUS(status) == 0 and os.WIFEXITED(status) else None
        if time.time() - t0 > LIMIT_S:
            p.kill(); os.waitpid(p.pid, 0); return None
        time.sleep(0.0002)


def time_it(cmd, inp):
    """Mean CPU time (ms) of one command on one input file over RUNS timed runs (after WARMUP runs),
    or (None, error text)."""
    data = open(inp, "rb").read()
    fn = _cpu_psutil if METHOD == "psutil" else _cpu_rusage
    vals = []
    for i in range(WARMUP + RUNS):
        v = fn(cmd, data)
        if v is None:
            return None, "run failed or timed out"
        if i >= WARMUP:
            vals.append(v * 1000.0)
    if METHOD == "psutil" and all(v == 0.0 for v in vals):
        return None, "psutil saw no CPU time (program too short for polling); try the rusage method"
    return statistics.mean(vals), ""


def case_files(task):
    folder = os.path.join(TESTS, task)
    return sorted(f for f in os.listdir(folder) if f.endswith(".in"))


def time_all_cases(cmd, task, label):
    """Time one program on every test case of its task. Returns {case name: mean_ms or None}."""
    per = {}
    files = case_files(task)
    for i, f in enumerate(files, 1):
        mean, err = time_it(cmd, os.path.join(TESTS, task, f))
        per[f[:-3]] = mean
        if mean is None:
            print(f"   {label} case {f[:-3]}: NOT TIMED  {err[:100]}")
        print(f"   {label} case {f[:-3]} ({i}/{len(files)}): " + ("-" if mean is None else f"{mean:.1f} ms"), end="\r")
    print(" " * 70, end="\r")
    return per


def average(per):
    vals = [v for v in per.values() if v is not None]
    return statistics.mean(vals) if vals and len(vals) == len(per) else None


def time_baselines():
    """Time the ORIGINAL programs in baselines/ on every test case.
    Returns {(task, lang): {case: mean_ms}}."""
    bdir = os.path.join(HERE, "baselines")
    out = {}
    if not os.path.isdir(bdir):
        sys.exit("baselines/ folder not found (the original programs are needed).")
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    for f in sorted(os.listdir(bdir)):
        m = re.match(r"^([a-z]+)\.(py|cs)$", f)
        if not m:
            continue
        task, lang = ALIAS.get(m.group(1), m.group(1)), m.group(2)
        path = os.path.join(bdir, f)
        if lang == "py":
            cmd = [sys.executable, path]
        else:
            exe = os.path.join(HERE, "build", "baseline_" + f[:-3] + ".exe")
            r = subprocess.run(["csc", f"-out:{exe}", path], capture_output=True, text=True)
            if r.returncode != 0:
                print("baseline compile error:", f)
                continue
            cmd = ["mono", exe]
        per = time_all_cases(cmd, task, "BASELINE " + f)
        avg = average(per)
        out[(task, lang)] = per
        print(f"BASELINE {f:20s} average {('-' if avg is None else f'{avg:.1f}')} ms over {len(per)} test cases")
    return out


def main():
    global METHOD
    if len(sys.argv) > 1:
        METHOD = sys.argv[1]
    if METHOD not in ("psutil", "rusage"):
        sys.exit("method must be psutil or rusage")
    if METHOD == "psutil":
        try:
            import psutil  # noqa: F401
        except ImportError:
            sys.exit("psutil not found (pip install psutil)")
    print(f"timing method: {METHOD}  ({WARMUP} warm-up runs + {RUNS} timed runs per test case)")
    cpath = os.path.join(HERE, "correctness.csv")
    if not os.path.exists(cpath):
        sys.exit("correctness.csv not found. Run check_all.py first.")
    rows = list(csv.DictReader(open(cpath)))
    up = os.path.join(HERE, "programs", "unchanged.txt")
    unch = {l.strip() for l in open(up) if l.strip()} if os.path.exists(up) else set()
    start = time.time()
    base = time_baselines()
    print("\nOriginals timed. Now the generated programs that passed every test case.\n")

    case_rows, summary = [], []
    for r in rows:
        f, task, lang = r["program"], r["task"], r["lang"]
        s = {k: r[k] for k in ("program", "task", "lang", "model", "condition", "passed", "total", "pass1")}
        s.update(cases_timed="", avg_ms="", baseline_avg_ms="", change_pct="", cases_faster="",
                 faster="", unchanged="yes" if f in unch else "no", opt1="no", note="")
        b = base.get((task, lang))
        bavg = average(b) if b else None
        if bavg is not None:
            s["baseline_avg_ms"] = round(bavg, 2)
        if r["pass1"] != "yes":
            s["note"] = "not timed: did not pass every test case"
            print(f"{f:40s} not timed (did not pass every test case)")
        elif bavg is None:
            s["note"] = "no baseline average (original not timed on every case)"
            print(f"{f:40s} NO BASELINE")
        else:
            per = time_all_cases(r["run_cmd"].split("|"), task, f)
            avg = average(per)
            for case, ms in per.items():
                case_rows.append(dict(program=f, task=task, lang=lang, model=r["model"], condition=r["condition"],
                                      case=case, mean_ms="" if ms is None else round(ms, 2),
                                      baseline_ms="" if b.get(case) is None else round(b[case], 2)))
            if avg is None:
                s["note"] = "not every test case could be timed"
            else:
                s.update(cases_timed=len(per), avg_ms=round(avg, 2),
                         change_pct=round((bavg - avg) / bavg * 100, 1),
                         cases_faster=f"{sum(1 for c, v in per.items() if b.get(c) is not None and v < b[c])}/{len(per)}",
                         faster="yes" if avg < bavg else "no")
                if s["faster"] == "yes" and s["unchanged"] == "no":
                    s["opt1"] = "yes"
            print(f"{f:40s} average {s['avg_ms']} ms  baseline {s['baseline_avg_ms']} ms  change {s['change_pct']}%  "
                  f"faster={s['faster']}  Opt@1={s['opt1']}")
        summary.append(s)

    with open(os.path.join(HERE, "timing_cases.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["program", "task", "lang", "model", "condition", "case", "mean_ms", "baseline_ms"])
        w.writeheader(); w.writerows(case_rows)
    with open(os.path.join(HERE, "results_avg.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(summary[0].keys()))
        w.writeheader(); w.writerows(summary)
    print(f"\nwrote timing_cases.csv and results_avg.csv  ({(time.time() - start) / 60:.1f} minutes)")


main()
