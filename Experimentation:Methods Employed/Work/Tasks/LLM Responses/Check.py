import subprocess, sys

cmd = sys.argv[1:]  # e.g. mono tasks/berland_unop.exe  or  python3 tasks/prog.py

tests = [
    {'input': '3\n5 6\n1 2\n', 'output': ['5\n']},
    # paste more testcases here
]

passed = 0
for i, t in enumerate(tests, 1):
    r = subprocess.run(cmd, input=t['input'], capture_output=True, text=True, timeout=30)
    got = r.stdout.split()
    ok = any(got == exp.split() for exp in t['output'])
    passed += ok
    print(f"test {i}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  expected:", t['output'][0].strip())
        print("  got:     ", r.stdout.strip(), r.stderr.strip()[:200])

print(f"{passed}/{len(tests)} passed")