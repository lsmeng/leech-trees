#!/usr/bin/env python3
"""E1/E2/E3 analysis over samples.json + the five known Leech trees."""
import json, os, sys, statistics
from collections import Counter
from sampler import analyze_state, components

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')


def summarize(vals):
    if not vals:
        return None
    return dict(mean=statistics.mean(vals), median=statistics.median(vals),
                mn=min(vals), mx=max(vals),
                p90=sorted(vals)[int(0.9 * (len(vals) - 1))])


def main():
    os.nice(10)
    with open(os.path.join(HERE, 'samples.json')) as f:
        S = json.load(f)
    with open(os.path.join(ROOT, 'data', 'known_leech_trees.json')) as f:
        known = json.load(f)['trees']

    out = {}

    # ---------------- exact positives ----------------
    out['known'] = []
    for t in known:
        if t['n'] < 3:
            continue
        a = analyze_state([tuple(e) for e in t['edges']], t['n'])
        a['name'] = t['name']
        out['known'].append(a)

    # ---------------- E1 on sampled near-misses ----------------
    out['E1'] = {}
    out['E3'] = {}
    for nstr, blob in S.items():
        n = int(nstr)
        N = n * (n - 1) // 2
        analyses = []
        for depth, edges in blob['best']:
            analyses.append(analyze_state([tuple(e) for e in edges], n))
        tree_analyses = [analyze_state([tuple(e) for e in edges], n)
                         for depth, edges in blob.get('best_tree', [])]
        # sanity flags
        viol_AB = sum(1 for a in analyses if not a['all_AB_ok'])
        viol_cross = sum(1 for a in analyses if not a['all_cross_ok'])
        viol_Ad = sum(1 for a in analyses if not a['all_A_distinct'])
        out['E1'][n] = dict(
            nstates=len(analyses),
            depths=summarize([a['depth'] for a in analyses]),
            main_size=summarize([a['main_size'] for a in analyses]),
            ncomp=Counter(a['ncomp'] for a in analyses).most_common(),
            cen_occ_maxA=summarize([a['centroid']['occ_maxA'] for a in analyses]),
            cen_occ_N=summarize([a['centroid']['occ_N'] for a in analyses]),
            best_occ_maxA=summarize([a['best']['occ_maxA'] for a in analyses]),
            best_occ_N=summarize([a['best']['occ_N'] for a in analyses]),
            cen_sizeD=summarize([a['centroid']['sizeD'] for a in analyses]),
            cen_maxA=summarize([a['centroid']['maxA'] for a in analyses]),
            cen_lenA=summarize([a['centroid']['lenA'] for a in analyses]),
            violations_AB=viol_AB, violations_cross=viol_cross,
            violations_A_distinct=viol_Ad,
            ntree_states=len(tree_analyses),
            tree_cen_occ_maxA=summarize([a['centroid']['occ_maxA'] for a in tree_analyses]),
            tree_best_occ_maxA=summarize([a['best']['occ_maxA'] for a in tree_analyses]),
        )
        # ---------------- E3 slack ----------------
        # use only states whose main component is large (>= n-2 vertices)
        big = [a for a in analyses if a['main_size'] >= n - 2]
        slack = {}
        for q in range(1, 31):
            cnts = [sum(1 for p in a['prods'] if p <= q) for a in big]
            slack[q] = summarize([c - q for c in cnts])
        out['E3'][n] = dict(nbig=len(big), slack=slack)

    # E3 for known trees
    out['E3_known'] = {}
    for a in out['known']:
        slack = {}
        for q in range(1, 16):
            c = sum(1 for p in a['prods'] if p <= q)
            slack[q] = c - q
        out['E3_known'][a['name']] = slack

    # ---------------- E2 death-point histogram ----------------
    out['E2'] = {}
    for nstr, blob in S.items():
        n = int(nstr)
        N = n * (n - 1) // 2
        deaths = blob['deaths']
        depths = [d for d, t, c in deaths]
        dsort = sorted(depths)
        q75 = dsort[int(0.75 * (len(dsort) - 1))]
        deep_thresh = max(q75, n - 1 - 4)
        hist_all = Counter()
        hist_deep = Counter()
        tstar_deep = []
        BINS = 20
        ncomp_deep = Counter()
        for d, t, c in deaths:
            b = min(int(BINS * t / N), BINS - 1)
            hist_all[b] += 1
            if d >= deep_thresh:
                hist_deep[b] += 1
                tstar_deep.append(t / N)
                ncomp_deep[c] += 1
        out['E2'][n] = dict(
            ndeaths=len(deaths), deep_thresh=deep_thresh,
            ndeep=len(tstar_deep),
            depth_hist=Counter(depths).most_common(),
            tstar_over_N_all=[hist_all.get(b, 0) for b in range(BINS)],
            tstar_over_N_deep=[hist_deep.get(b, 0) for b in range(BINS)],
            tstar_deep_summary=summarize(tstar_deep),
            ncomp_deep=sorted(ncomp_deep.items()),
        )

    with open(os.path.join(HERE, 'analysis.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote analysis.json")

    # quick console dump
    for n in sorted(out['E1']):
        e = out['E1'][n]
        print(f"n={n}: cen occ_maxA mean={e['cen_occ_maxA']['mean']:.3f} "
              f"max={e['cen_occ_maxA']['mx']:.3f}; best occ_maxA mean={e['best_occ_maxA']['mean']:.3f} "
              f"max={e['best_occ_maxA']['mx']:.3f}; occ_N(cen) mean={e['cen_occ_N']['mean']:.3f}; "
              f"AB viol={e['violations_AB']} cross viol={e['violations_cross']}")
    for a in out['known']:
        print(f"{a['name']} (n={a['n']}): cen occ_maxA={a['centroid']['occ_maxA']:.3f} "
              f"best={a['best']['occ_maxA']:.3f} occ_N={a['centroid']['occ_N']:.3f} "
              f"AB_ok={a['all_AB_ok']} cross_ok={a['all_cross_ok']}")
    for n in sorted(out['E2']):
        e = out['E2'][n]
        print(f"n={n} E2: deep deaths={e['ndeep']} (depth>={e['deep_thresh']}), "
              f"t*/N deep: {e['tstar_deep_summary']}")
        print("   deep hist (20 bins of t*/N):", e['tstar_over_N_deep'])


if __name__ == '__main__':
    main()
