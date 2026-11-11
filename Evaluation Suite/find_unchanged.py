#!/usr/bin/env python3
"""Compare every generated program with its ORIGINAL (baselines/) and flag the ones that are unchanged.

Usage:  python3 find_unchanged.py
Reads   programs/*.py|cs   and   baselines/<task>.py|cs
Writes  unchanged_check.csv  and  programs/unchanged.txt  (exact matches only)

After removing comments and whitespace:
  UNCHANGED     identical to the original
  VERY SIMILAR  95% or more identical -> open both files and decide yourself
  CHANGED       anything else
"""
import csv, difflib, io, os, re, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
PROGS = os.path.join(HERE, "programs")
BASES = os.path.join(HERE, "baselines")
ALIAS = {"homework": "perm", "natalya": "ball", "natalia": "ball"}


def norm_py(src):
    skip = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
            tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER)
    try:
        return [t.string for t in tokenize.generate_tokens(io.StringIO(src).readline)
                if t.type not in skip]
    except Exception:
        return re.findall(r"\w+|[^\w\s]", re.sub(r"#.*", "", src))


def norm_cs(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"(?m)//.*$", "", src)
    return re.findall(r"\w+|[^\w\s]", src)


def tokens(path, lang):
    src = open(path, errors="ignore").read()
    return norm_py(src) if lang == "py" else norm_cs(src)


def main():
    rows = []
    for f in sorted(os.listdir(PROGS)):
        m = re.match(r"^([a-z]+)_(gptoss|qwen)_(zeroshot|multishot)\.(py|cs)$", f)
        if not m or "discarded" in f:
            continue
        task, lang = ALIAS.get(m.group(1), m.group(1)), m.group(4)
        base = os.path.join(BASES, task + "." + lang)
        if not os.path.exists(base):
            print("no baseline for", f)
            continue
        a = tokens(base, lang)
        b = tokens(os.path.join(PROGS, f), lang)
        ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
        verdict = "UNCHANGED" if a == b else ("VERY SIMILAR" if ratio >= 0.95 else "CHANGED")
        rows.append({"program": f, "similarity": round(ratio, 3), "verdict": verdict})
        print(f"{f:34s} similarity {ratio:.3f}  {verdict}")
    with open(os.path.join(HERE, "unchanged_check.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["program", "similarity", "verdict"])
        w.writeheader()
        w.writerows(rows)
    exact = [r["program"] for r in rows if r["verdict"] == "UNCHANGED"]
    with open(os.path.join(PROGS, "unchanged.txt"), "w") as fo:
        fo.write("\n".join(exact) + ("\n" if exact else ""))
    print("\nwrote unchanged_check.csv;", len(exact), "exact matches written to programs/unchanged.txt")
    print("Check every VERY SIMILAR line by hand and add the cosmetic ones to programs/unchanged.txt.")


main()
