import json, sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import checker_a, checker_b
data = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'known_leech_trees.json')))
for t in data['trees']:
    e = [tuple(x) for x in t['edges']]
    a = checker_a.is_leech(t['n'], e); b = checker_b.is_leech(t['n'], e)
    assert a[0] and b[0], (t['name'], a, b)
    print("PASS known", t['name'])
# negatives: perturb each known tree's weights; both checkers must agree on every case
random.seed(1); agree = 0
for t in data['trees']:
    for _ in range(200):
        e = [(u, v, max(1, w + random.randint(-2, 2))) for u, v, w in t['edges']]
        a = checker_a.is_leech(t['n'], e)[0]; b = checker_b.is_leech(t['n'], e)[0]
        assert a == b, (t['name'], e, a, b); agree += 1
print("PASS agreement on", agree, "perturbed cases")
# path 1,2,3 must fail (3 repeated)
assert not checker_a.is_leech(4, [(0,1,1),(1,2,2),(2,3,3)])[0]
assert not checker_b.is_leech(4, [(0,1,1),(1,2,2),(2,3,3)])[0]
print("PASS negative")
