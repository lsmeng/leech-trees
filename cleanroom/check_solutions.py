"""Run cr_forest for n, parse SOL lines, verify each with src/checker_a and src/checker_b."""
import subprocess, sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', 'src'))
import checker_a, checker_b
n = int(sys.argv[1])
out = subprocess.run([os.path.join(here, 'cr_forest'), str(n)] + sys.argv[2:], capture_output=True, text=True).stdout
sols = []
for line in out.splitlines():
    if line.startswith('SOL:'):
        edges = []
        for tok in line.split()[1:]:
            uv, w = tok.split(':'); u, v = uv.split('-')
            edges.append((int(u), int(v), int(w)))
        sols.append(edges)
    elif line.startswith('{'):
        rec = json.loads(line)
print(f"n={n} nsol={rec['nsol']} levels={rec['levels']} nodes={rec['nodes']}")
ok = True
for e in sols:
    a = checker_a.is_leech(n, e); b = checker_b.is_leech(n, e)
    print("  ", e, "checker_a:", a, "checker_b:", b)
    ok &= a[0] and b[0]
assert len(sols) == rec['nsol']
print("ALL WITNESSES PASS" if ok else "WITNESS FAILURE")
