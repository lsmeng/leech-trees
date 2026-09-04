// double_end_search.cpp -- faithful C++17 port of double_end_search.py
//
//   c++ -O2 -std=c++17 -o double_end_search double_end_search.cpp
//
// Double-end (two-anchor) gap-order search for Leech trees.  See THEORY.md.
//
// N = C(n,2), V = n-2.  Each non-anchor vertex u carries (e,f) with
//     e = N - d(a,u),  f = N - d(b,u),  p = (N+f-e)/2,  h = (N-e-f)/2.
// Gaps g = 1..N-1 are processed in increasing order; the smallest unrealised
// gap must be an e- or f-coordinate (of a new or half-known vertex), or the
// resolution of a previously deferred tied pair.  Everything else is forced.
//
// This file is a line-for-line port of the Python reference: same state, same
// branching order, same prunes, same trail-based undo, so that node counts and
// solution sets agree exactly.
//
// CLI:
//   double_end_search <n> [options]
//     --nodes-limit K        stop after K nodes (0 = unlimited)
//     --max-solutions K      stop after K solutions (default 200)
//     --split LEVEL K M      explore only shard K of M at recursion depth LEVEL
//     --verify               rebuild + BFS-check every solution
//     --progress             periodic progress to stderr
//     --quiet                suppress per-solution lines
//     --no-hall --no-lb --no-attach --no-hc --no-deferred-check
//     --no-ultra --no-parity --no-cover --no-ub --no-sym
//                            (disable one prune each; soundness testing)
//     --debug                extra counters on stderr

#include <algorithm>
#include <chrono>
#include <climits>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <string>
#include <utility>
#include <vector>

// ------------------------------------------------------------------ helpers
static long long floordiv(long long a, long long b) {
    long long q = a / b;
    if ((a % b != 0) && ((a < 0) != (b < 0))) --q;
    return q;
}

static std::vector<std::pair<int, int>> parity_splits(int n) {
    int N = n * (n - 1) / 2;
    int V = n - 2;
    int ev_needed = (N + 1) / 2;   // #even values in [0, N-1]
    int od_needed = N / 2;
    std::vector<std::pair<int, int>> out;
    for (int al = 0; al <= V; ++al) {
        int be = V - al, ev, od;
        if (N % 2 == 0) {
            ev = 1 + al + al + al * (al - 1) / 2 + be * (be - 1) / 2;
            od = be + be + al * be;
        } else {
            ev = 1 + al + be + al * be;
            od = al + be + al * (al - 1) / 2 + be * (be - 1) / 2;
        }
        if (ev == ev_needed && od == od_needed) out.push_back({al, be});
    }
    return out;
}

// ------------------------------------------------------------------ records
enum TrailTag { T_TAKE, T_COORD, T_PAIR, T_DEFER, T_NEWV, T_RESOLVE };
struct TR { int tag, a, b, c, d, e, x; };
struct Def { int i, j, base, hmax; };

static const int HC_NONE = INT_MIN;
static std::string joinv(const std::vector<int> &v);

// ------------------------------------------------------------------ search
struct Search {
    int n, N, V;
    long long nodeLimit = 0;            // 0 = unlimited
    long long maxSolutions = 200;
    bool progress = false, quiet = false, verifyMode = false, debug = false, trace = false;
    bool noHall = false, noLb = false, noAttach = false, noHc = false,
         noDeferredCheck = false, noUltra = false, noParity = false, noCover = false,
         noUb = false;
    int forceEupto = 0;          // gaps 1..forceEupto must all be e-values;
                                 // 0 disables (default, changes nothing).
                                 // Beyond the frozen reference; inert at 0.
    bool symmetryBreak = true;   // gap 1 is always a coordinate and a<->b may be
                                 // swapped, so assume 1 in E
    // The Python reference re-appends a restored deferred entry at the END of
    // the list, so the option-1 branch ORDER at a node depends on which sibling
    // subtrees ran before it.  Node counts and solution sets are invariant
    // under that order, but the DFS *order* is not -- and --split numbers
    // branches in DFS order.  stableDeferred restores the entry at the index it
    // was removed from, making rec() completely state-neutral and the shard
    // numbering path-determined.  --split turns it on automatically.
    bool stableDeferred = false;
    bool forceUnstable = false;  // diagnostic: keep Python's append-on-restore even with --split
    int splitLevel = -1;
    long long splitK = 0, splitM = 1, splitCounter = 0;

    std::vector<std::pair<int, int>> splits;
    int amax = -1, bmax = -1;

    // mutable state (mirrors the Python attributes exactly)
    std::vector<int> e, f;
    int nv = 0, alpha = 0, beta = 0;
    std::vector<uint8_t> taken;
    std::vector<int> pv;                // V*V, 0 undetermined, -1 deferred
    std::vector<Def> deferred;
    std::vector<TR> trail;
    std::vector<Def> snapStack;         // per-node snapshots of `deferred`
    std::vector<int> cov;               // #representations w = e+f, e in E u {0}, f in F u {0}
    std::vector<uint8_t> exempt;        // gaps realised by a tied pair with h_c > 0

    long long nodes = 0;
    bool bailed = false, hitSolLimit = false;
    long long solCount = 0;
    long long multiResolveNodes = 0;    // nodes taking >= 2 option-1 branches
    static const int DEPTH_HIST = 512;
    std::vector<long long> depthHist;   // rec() calls by recursion depth
    std::vector<std::vector<int>> solE, solF, solPV;

    // scratch
    std::vector<int> LBs, UBs;
    std::vector<int> defwin;            // V*V, -1 = absent
    std::vector<size_t> defwinKeys;
    std::vector<int> hbuf, hstart, hcnt;
    std::vector<int> matchOf, matchStamp, seenStamp;
    int stampM = 0, stampS = 0;
    std::vector<int> candStack;         // flat per-frame candidate pool
    std::chrono::steady_clock::time_point t0;

    explicit Search(int n_) : n(n_) {
        N = n * (n - 1) / 2;
        V = n - 2;
        splits = parity_splits(n);
        for (auto &s : splits) { amax = std::max(amax, s.first); bmax = std::max(bmax, s.second); }
        e.assign(V, 0); f.assign(V, 0);
        taken.assign(N > 0 ? N : 1, 0);
        if (N > 0) taken[0] = 1;
        pv.assign((size_t)V * V, 0);
        LBs.reserve((size_t)V * V + 4 * (size_t)V + 8);
        UBs.reserve((size_t)V * V + 4 * (size_t)V + 8);
        defwin.assign((size_t)V * V, -1);
        defwinKeys.reserve((size_t)V * V);
        hbuf.assign((size_t)(V + 1) * (N + 2), 0);
        hstart.assign(V + 1, 0); hcnt.assign(V + 1, 0);
        matchOf.assign(N + 2, -1); matchStamp.assign(N + 2, 0); seenStamp.assign(N + 2, 0);
        candStack.reserve(1024);
        trail.reserve(4096);
        snapStack.reserve(1024);
        depthHist.assign(DEPTH_HIST, 0);
        cov.assign(2 * (size_t)N + 2, 0);
        cov[0] = 1;
        exempt.assign(N > 0 ? N : 1, 0);
    }

    inline int hh(int i) const { return (N - e[i] - f[i]) / 2; }

    // ---------- prunes ----------
    bool partner_ok(int i, int g) const {
        if (e[i] && f[i]) return true;
        int known = e[i] ? e[i] : f[i];
        int par = (N - known) % 2;
        int hi = N - known;
        int w = g;
        if ((w % 2) != par) ++w;
        for (; w <= hi; w += 2) if (!taken[w]) return true;
        return false;
    }

    bool attach_ok() const {
        for (int i = 0; i < nv; ++i) {
            if (!(e[i] && f[i])) continue;
            if (e[i] + f[i] == N) continue;          // h = 0, lies on P
            int d = f[i] - e[i];
            if ((N - d) % 2) return false;
            int ew = (N - d) / 2, fw = (N + d) / 2;
            if (ew < 1 || fw < 1 || ew > N - 1 || fw > N - 1) return false;
            int we = -1, wf = -1;
            for (int j = 0; j < nv; ++j) {
                if (e[j] == ew) we = j;
                if (f[j] == fw) wf = j;
            }
            if (we >= 0 && wf >= 0) { if (we != wf) return false; continue; }
            if (we >= 0) { if (f[we] || taken[fw]) return false; continue; }
            if (wf >= 0) { if (e[wf] || taken[ew]) return false; continue; }
            if (taken[ew] || taken[fw]) return false;
        }
        return true;
    }

    bool aug(int k) {
        int base = hstart[k], cnt = hcnt[k];
        for (int q = 0; q < cnt; ++q) {
            int v = hbuf[base + q];
            if (seenStamp[v] == stampS) continue;
            seenStamp[v] = stampS;
            if (matchStamp[v] != stampM || aug(matchOf[v])) {
                matchOf[v] = k; matchStamp[v] = stampM; return true;
            }
        }
        return false;
    }

    bool hall_partners(int g) {
        int ns = 0;
        for (int i = 0; i < nv; ++i) {
            if (e[i] && f[i]) continue;
            int known = e[i] ? e[i] : f[i];
            int par = (N - known) % 2;
            int hi = N - known;
            int base = ns * (N + 2), cnt = 0;
            int w = g;
            if ((w % 2) != par) ++w;
            for (; w <= hi; w += 2) if (!taken[w]) hbuf[base + cnt++] = w;
            if (cnt == 0) return false;
            hstart[ns] = base; hcnt[ns] = cnt; ++ns;
        }
        if (ns < 2) return true;
        ++stampM;
        for (int k = 0; k < ns; ++k) {
            ++stampS;
            if (!aug(k)) return false;
        }
        return true;
    }

    bool lb_prune(int g) {
        int lo = g;      // coordinates still unassigned are >= g (one may equal g)
        int assigned = 0;
        for (int i = 0; i < nv; ++i) assigned += (e[i] ? 1 : 0) + (f[i] ? 1 : 0);
        int R = 2 * V - assigned;
        LBs.clear();
        for (int i = 0; i < nv; ++i)
            for (int j = i + 1; j < nv; ++j) {
                int p = pv[(size_t)i * V + j];
                if (p > 0) continue;
                if (p == -1) continue;              // deferred, handled below
                int ei = e[i], fi = f[i], ej = e[j], fj = f[j];
                int lb1 = (fi ? fi : lo) + (ej ? ej : lo);
                int lb2 = (fj ? fj : lo) + (ei ? ei : lo);
                LBs.push_back(lb1 < lb2 ? lb1 : lb2);
            }
        for (const Def &D : deferred) LBs.push_back(D.base > g ? D.base : g);
        int fut = V - nv;
        if (fut) {
            for (int i = 0; i < nv; ++i) {
                int ei = e[i], fi = f[i];
                int c1 = (fi ? fi : lo) + lo;
                int c2 = lo + (ei ? ei : lo);
                int lb = c1 < c2 ? c1 : c2;
                for (int q = 0; q < fut; ++q) LBs.push_back(lb);
            }
            int extra = fut * (fut - 1) / 2;
            for (int q = 0; q < extra; ++q) LBs.push_back(2 * lo);
        }
        std::sort(LBs.begin(), LBs.end());
        int k = 0, need = 0, nlb = (int)LBs.size();
        for (int t = g; t < N; ++t) {
            if (taken[t]) continue;
            ++need;
            while (k < nlb && LBs[k] <= t) ++k;
            if (need > R + k) return false;
        }
        return true;
    }

    // The meeting point of u,v is a vertex of T.  If h_c > 0 it is a vertex w
    // with the same p and height h_c, so e_w = N-p-h_c, f_w = p-h_c are forced.
    bool hc_heights(int i, int j, int hc) const {
        (void)j;
        if (hc == 0) return true;
        int p = (N + f[i] - e[i]) / 2;
        int ew = N - p - hc;
        int fw = p - hc;
        if (ew < 1 || fw < 1 || ew > N - 1 || fw > N - 1) return false;
        for (int w = 0; w < nv; ++w) {
            if (e[w] == ew && f[w] == fw) return true;
            if (e[w] == ew || f[w] == fw) {
                if (e[w] == ew && !f[w] && !taken[fw]) return true;
                if (f[w] == fw && !e[w] && !taken[ew]) return true;
                return false;
            }
        }
        return !(taken[ew] || taken[fw]);
    }

    int pair_hc(int x, int y) const {
        int v = pv[(size_t)x * V + y];
        if (v <= 0) return HC_NONE;
        return (int)floordiv((long long)v - ((long long)f[x] + e[y]), 2);
    }

    // LCA heights inside one p-class form a max-ultrametric.
    bool ultrametric_ok(int i, int j) const {
        int hij = pair_hc(i, j);
        if (hij == HC_NONE) return true;
        int d = f[i] - e[i];
        for (int k = 0; k < nv; ++k) {
            if (k == i || k == j || !(e[k] && f[k])) continue;
            if (f[k] - e[k] != d) continue;
            int hik = pair_hc(i, k);
            int hjk = pair_hc(j, k);
            if (hik == HC_NONE || hjk == HC_NONE) continue;
            int m = std::min(hij, std::min(hik, hjk));
            int c = (hij == m) + (hik == m) + (hjk == m);
            if (c < 2) return false;
        }
        // the meeting vertex of i,j is the class vertex w at height h_c(i,j);
        // it must be an ancestor of both, i.e. h_c(i,w) = h_c(j,w) = h_c(i,j)
        if (hij > 0) {
            for (int k = 0; k < nv; ++k) {
                if (k == i || k == j || !(e[k] && f[k])) continue;
                if (f[k] - e[k] != d) continue;
                if ((N - e[k] - f[k]) / 2 != hij) continue;
                int hik = pair_hc(i, k);
                int hjk = pair_hc(j, k);
                if (hik != HC_NONE && hik != hij) return false;
                if (hjk != HC_NONE && hjk != hij) return false;
            }
        }
        return true;
    }

    bool class_ok(int i) const {
        if (!(e[i] && f[i])) return true;
        int d = f[i] - e[i];
        for (int j = 0; j < nv; ++j) {
            if (j == i || !(e[j] && f[j])) continue;
            if (f[j] - e[j] != d) continue;
            if (!ultrametric_ok(i, j)) return false;
        }
        return true;
    }

    bool deferred_ok(int g) const {
        for (const Def &D : deferred) {
            bool hit = false;
            int top = D.base + 2 * D.hmax;
            for (int v = D.base; v <= top; v += 2) {
                if (v >= N) break;                  // unreachable: base+2hmax <= N-1
                if (v >= g && !taken[v]) { hit = true; break; }
            }
            if (!hit) return false;
        }
        return true;
    }

    // ---------- assignment with propagation ----------
    bool assign(int i, bool is_e, int g) {
        if (is_e) e[i] = g; else f[i] = g;
        trail.push_back({T_COORD, i, is_e ? 1 : 0, 0, 0, 0, 0});
        cov[g] += 1;                                    // g + 0
        if (is_e) { for (int j = 0; j < nv; ++j) if (f[j]) cov[g + f[j]] += 1; }
        else      { for (int j = 0; j < nv; ++j) if (e[j]) cov[g + e[j]] += 1; }
        taken[g] = 1;
        trail.push_back({T_TAKE, g, 0, 0, 0, 0, 0});
        if (e[i] && f[i]) {
            if (e[i] + f[i] > N) return false;
            if ((e[i] + f[i]) % 2 != N % 2) return false;
        }
        for (int j = 0; j < nv; ++j) {
            if (j == i || pv[(size_t)i * V + j]) continue;
            int ei = e[i], fi = f[i], ej = e[j], fj = f[j];
            int c1 = (fi && ej) ? fi + ej : 0;      // crossing f_i + e_j
            int c2 = (fj && ei) ? fj + ei : 0;
            int lo = g + 1;
            int lb1 = (fi ? fi : lo) + (ej ? ej : lo);
            int lb2 = (fj ? fj : lo) + (ei ? ei : lo);
            int val = 0;
            if (c1 && c2) {
                if (c1 != c2) {
                    val = c1 < c2 ? c1 : c2;
                } else {
                    int hmax = std::min(hh(i), hh(j));
                    if (hmax == 0) {
                        val = c1;
                    } else {
                        deferred.push_back({i, j, c1, hmax});
                        pv[(size_t)i * V + j] = pv[(size_t)j * V + i] = -1;
                        trail.push_back({T_DEFER, i, j, 0, 0, 0, 0});
                        continue;
                    }
                }
            } else if (c1 && c1 < lb2) {
                val = c1;
            } else if (c2 && c2 < lb1) {
                val = c2;
            }
            if (val) {
                if (val >= N || val <= 0 || taken[val]) return false;
                taken[val] = 1;
                pv[(size_t)i * V + j] = pv[(size_t)j * V + i] = val;
                trail.push_back({T_PAIR, i, j, val, 0, 0, 0});
            }
        }
        return true;
    }

    void undo(size_t mark) {
        while (trail.size() > mark) {
            TR r = trail.back();
            trail.pop_back();
            switch (r.tag) {
            case T_TAKE:
                taken[r.a] = 0; break;
            case T_COORD: {
                int gg = r.b ? e[r.a] : f[r.a];
                cov[gg] -= 1;
                if (r.b) { e[r.a] = 0; for (int j = 0; j < nv; ++j) if (f[j]) cov[gg + f[j]] -= 1; }
                else     { f[r.a] = 0; for (int j = 0; j < nv; ++j) if (e[j]) cov[gg + e[j]] -= 1; }
                break;
            }
            case T_PAIR:
                pv[(size_t)r.a * V + r.b] = pv[(size_t)r.b * V + r.a] = 0;
                taken[r.c] = 0; break;
            case T_DEFER: {
                pv[(size_t)r.a * V + r.b] = pv[(size_t)r.b * V + r.a] = 0;
                for (int t = (int)deferred.size() - 1; t >= 0; --t)
                    if (deferred[t].i == r.a && deferred[t].j == r.b) {
                        deferred.erase(deferred.begin() + t); break;
                    }
                break;
            }
            case T_NEWV:
                --nv; e[nv] = 0; f[nv] = 0;
                if (r.a == 0) --alpha; else --beta;
                break;
            case T_RESOLVE:
                if (r.c > r.d) exempt[r.c] = 0;
                taken[r.c] = 0;
                pv[(size_t)r.a * V + r.b] = pv[(size_t)r.b * V + r.a] = -1;
                if (stableDeferred)
                    deferred.insert(deferred.begin() + r.x, {r.a, r.b, r.d, r.e});
                else
                    deferred.push_back({r.a, r.b, r.d, r.e});
                break;
            }
        }
    }

    // Lower bound on d(u_i,u_j) from |d(a,u)-d(a,v)| = |e_i-e_j| and the same
    // on the b side; unknown coordinates are >= g.
    int dist_lb(int i, int j, int g) const {
        int lb = 1;
        int ei = e[i], fi = f[i], ej = e[j], fj = f[j];
        if (ei && ej)      { int v = ei - ej; lb = std::max(lb, v > 0 ? v : -v); }
        else if (ei)       { lb = std::max(lb, g - ei); }
        else if (ej)       { lb = std::max(lb, g - ej); }
        if (fi && fj)      { int v = fi - fj; lb = std::max(lb, v > 0 ? v : -v); }
        else if (fi)       { lb = std::max(lb, g - fi); }
        else if (fj)       { lb = std::max(lb, g - fj); }
        return lb;
    }

    int h_ub(int i, int g) const {
        if (e[i] && f[i]) return (N - e[i] - f[i]) / 2;
        int known = e[i] ? e[i] : f[i];
        return (int)floordiv((long long)N - known - g, 2);   // may be negative
    }

    // Dual Hall condition: every untaken gap must be supplied by a remaining
    // coordinate or a pair whose value upper bound is large enough.
    bool ub_prune(int g) {
        int nvv = nv, fut = V - nv;
        UBs.clear();
        for (int i = 0; i < nvv; ++i) {
            if (e[i] && f[i]) continue;
            UBs.push_back(N - (e[i] ? e[i] : f[i]));
        }
        if (fut) for (int q = 0; q < 2 * fut; ++q) UBs.push_back(N - g);
        // deferred windows, keyed on the RAW (i,j) order stored in `deferred`
        for (int q = 0; q < (int)defwinKeys.size(); ++q) defwin[defwinKeys[q]] = -1;
        defwinKeys.clear();
        for (const Def &D : deferred) {
            size_t key = (size_t)D.i * V + D.j;
            defwin[key] = D.base + 2 * D.hmax;
            defwinKeys.push_back(key);
        }
        for (int i = 0; i < nvv; ++i) {
            for (int j = i + 1; j < nvv; ++j) {
                int v = pv[(size_t)i * V + j];
                if (v > 0) continue;
                if (v == -1) {
                    int w = defwin[(size_t)i * V + j];
                    UBs.push_back(w >= 0 ? w : N - 1);
                    continue;
                }
                int u = N - dist_lb(i, j, g);
                int ei = e[i], fi = f[i], ej = e[j], fj = f[j];
                int c1 = (fi && ej) ? fi + ej : 0;
                int c2 = (fj && ei) ? fj + ei : 0;
                if (c1 || c2) {
                    int c = c1 ? c1 : c2;
                    if (c1 && c2) c = c1 > c2 ? c1 : c2;
                    int ha = h_ub(i, g), hb = h_ub(j, g);
                    int cand = c + 2 * (ha < hb ? ha : hb);
                    if (cand < u) u = cand;
                }
                UBs.push_back(u < N - 1 ? u : N - 1);
            }
            if (fut) {
                int m = e[i] ? e[i] : 0;
                int mf = f[i] ? f[i] : 0;
                int lo = (m && (!mf || m < mf)) ? m : mf;
                int val = N - std::max(1, g - lo);
                if (val > N - 1) val = N - 1;
                for (int q = 0; q < fut; ++q) UBs.push_back(val);
            }
        }
        if (fut > 1) { int extra = fut * (fut - 1) / 2; for (int q = 0; q < extra; ++q) UBs.push_back(N - 1); }
        std::sort(UBs.begin(), UBs.end(), std::greater<int>());
        int k = 0, need = 0, m = (int)UBs.size();
        for (int t = N - 1; t >= g; --t) {
            if (taken[t]) continue;
            ++need;
            while (k < m && UBs[k] >= t) ++k;
            if (need > k) return false;
        }
        return true;
    }

    // Covering lemma: every w in [0,N-1] is e+f for some e in E u {0}, f in
    // F u {0}, except gaps realised by a tied pair with h_c > 0.  For w < g
    // every e,f that could represent w is already assigned, so the test is
    // exact on that range.
    bool cover_ok(int g) const {
        for (int w = 0; w < g; ++w)
            if (cov[w] == 0 && !exempt[w]) return false;
        return true;
    }

    // As g grows the lower bound on every still-unknown coordinate rises, so
    // pairs that were undetermined can become determined with no new
    // assignment.  Re-derive them.  Returns 1 if anything was marked, 0 if
    // nothing changed, -1 on contradiction.
    int rescan(int g) {
        bool changed = false;
        int lo = g;
        for (int i = 0; i < nv; ++i)
            for (int j = i + 1; j < nv; ++j) {
                if (pv[(size_t)i * V + j]) continue;
                int ei = e[i], fi = f[i], ej = e[j], fj = f[j];
                int c1 = (fi && ej) ? fi + ej : 0;
                int c2 = (fj && ei) ? fj + ei : 0;
                int lb1 = (fi ? fi : lo) + (ej ? ej : lo);
                int lb2 = (fj ? fj : lo) + (ei ? ei : lo);
                int val = 0;
                if (c1 && c2) {
                    if (c1 != c2) {
                        val = c1 < c2 ? c1 : c2;
                    } else {
                        int hmax = std::min(hh(i), hh(j));
                        if (hmax == 0) {
                            val = c1;
                        } else {
                            deferred.push_back({i, j, c1, hmax});
                            pv[(size_t)i * V + j] = pv[(size_t)j * V + i] = -1;
                            trail.push_back({T_DEFER, i, j, 0, 0, 0, 0});
                            changed = true;
                            continue;
                        }
                    }
                } else if (c1 && c1 < lb2) {
                    val = c1;
                } else if (c2 && c2 < lb1) {
                    val = c2;
                }
                if (val) {
                    if (val >= N || val <= 0 || taken[val]) return -1;
                    taken[val] = 1;
                    pv[(size_t)i * V + j] = pv[(size_t)j * V + i] = val;
                    trail.push_back({T_PAIR, i, j, val, 0, 0, 0});
                    changed = true;
                }
            }
        return changed ? 1 : 0;
    }

    // Shard filter: called exactly once per branch that the unsharded search
    // would recurse into, from a node at recursion depth == splitLevel.
    inline bool shard_take(int depth) {
        if (splitLevel < 0 || depth != splitLevel) return true;
        long long c = splitCounter++;
        return (c % splitM) == splitK;
    }

    inline bool stop() {
        if (solCount >= maxSolutions) { hitSolLimit = true; return true; }
        return bailed;
    }

    // ---------- main recursion ----------
    // rec() owns `trail0` (everything rescan() marks) and undoes it on exit;
    // rec_body() is the Python _rec_body.
    void rec(int g, int depth) {
        ++nodes;
        ++depthHist[depth < DEPTH_HIST ? depth : DEPTH_HIST - 1];
        if (nodeLimit && nodes > nodeLimit) { bailed = true; return; }
        if (progress && (nodes % 20000000LL) == 0) {
            double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
            fprintf(stderr, "PROGRESS nodes=%lld elapsed=%.1fs rate=%.0f/s\n",
                    nodes, el, el > 0 ? nodes / el : 0.0);
        }
        if (trace) {
            printf("T %lld g=%d nv=%d e=[%s] f=[%s] def=%d d=%d\n", nodes, g, nv,
                   joinv(e).c_str(), joinv(f).c_str(), (int)deferred.size(), depth);
        }
        size_t mark0 = trail.size();
        rec_body(g, depth);
        undo(mark0);
    }

    void rec_body(int g, int depth) {
        for (;;) {
            while (g < N && taken[g]) ++g;
            if (g >= N) break;
            int ch = rescan(g);
            if (ch < 0) return;
            if (ch == 0) break;
        }
        if (g >= N) {
            if (nv == V && deferred.empty()) {
                bool all = true;
                for (int i = 0; i < V; ++i) if (!e[i] || !f[i]) { all = false; break; }
                if (all) record();
            }
            return;
        }
        // ---- global prunes
        if (!noDeferredCheck && !deferred_ok(g)) return;
        for (int i = 0; i < nv; ++i)
            if (!(e[i] && f[i]) && !partner_ok(i, g)) return;
        if (!noHall && !hall_partners(g)) return;
        if (!noLb && !lb_prune(g)) return;
        if (!noCover && !cover_ok(g)) return;
        if (!noUb && !ub_prune(g)) return;

        // ---- option 1: resolve a deferred tied pair at value g
        // Iterate over a snapshot: undo() re-appends restored entries at the
        // end of `deferred`, so live indices are not stable.
        bool eonly = (g <= forceEupto);
        if (!deferred.empty() && !eonly) {
            size_t sbase = snapStack.size();
            size_t scount = deferred.size();
            for (const Def &D : deferred) snapStack.push_back(D);
            int taken1 = 0;
            for (size_t q = 0; q < scount; ++q) {
                Def D = snapStack[sbase + q];
                if (!(D.base <= g && g <= D.base + 2 * D.hmax)) continue;
                if (((g - D.base) % 2) != 0) continue;
                if (!(noHc || hc_heights(D.i, D.j, (g - D.base) / 2))) continue;
                ++taken1;
                size_t mark = trail.size();
                int idx = -1;
                for (size_t t = 0; t < deferred.size(); ++t)
                    if (deferred[t].i == D.i && deferred[t].j == D.j) { idx = (int)t; break; }
                if (idx < 0) { fprintf(stderr, "INTERNAL: deferred entry vanished\n"); exit(3); }
                deferred.erase(deferred.begin() + idx);
                pv[(size_t)D.i * V + D.j] = pv[(size_t)D.j * V + D.i] = g;
                taken[g] = 1;
                if (g > D.base) exempt[g] = 1;
                trail.push_back({T_RESOLVE, D.i, D.j, g, D.base, D.hmax, idx});
                if (noUltra || ultrametric_ok(D.i, D.j)) {
                    if (shard_take(depth)) rec(g + 1, depth + 1);
                }
                undo(mark);
                if (stop()) { snapStack.resize(sbase); return; }
            }
            if (taken1 >= 2) ++multiResolveNodes;
            snapStack.resize(sbase);
        }

        // ---- option 2: g is a coordinate of an existing vertex
        // (candidates live on a flat stack: a recursive call must not clobber
        //  this frame's list)
        {
            size_t cbase = candStack.size();
            for (int i = 0; i < nv; ++i) {
                if (!e[i] && (f[i] + g) % 2 == N % 2 && f[i] + g <= N) candStack.push_back(2 * i + 1);
                if (!eonly && !f[i] && (e[i] + g) % 2 == N % 2 && e[i] + g <= N) candStack.push_back(2 * i + 0);
            }
            size_t ccount = candStack.size() - cbase;
            for (size_t k = 0; k < ccount; ++k) {
                int code = candStack[cbase + k];
                int ci = code >> 1;
                bool is_e = (code & 1) != 0;
                size_t mark = trail.size();
                bool ok = assign(ci, is_e, g)
                          && (noAttach || attach_ok())
                          && (noUltra || class_ok(ci));
                if (ok) { if (shard_take(depth)) rec(g + 1, depth + 1); }
                undo(mark);
                if (stop()) { candStack.resize(cbase); return; }
            }
            candStack.resize(cbase);
        }

        // ---- option 3: create a new vertex, e = g first then f = g
        if (nv < V) {
            int nsides = (eonly || (symmetryBreak && nv == 0)) ? 1 : 2;
            for (int s = 0; s < nsides; ++s) {
                bool is_e = (s == 0);
                int eps = (((is_e ? (g % 2) : ((N - g) % 2)) == 0) ? 0 : 1);
                int al = alpha + (eps == 0 ? 1 : 0);
                int be = nv + 1 - al;
                if (!noParity && (al > amax || be > bmax)) continue;
                size_t mark = trail.size();
                int i = nv;
                ++nv;
                if (eps == 0) ++alpha; else ++beta;
                trail.push_back({T_NEWV, eps, 0, 0, 0, 0, 0});
                bool ok = assign(i, is_e, g)
                          && (noAttach || attach_ok())
                          && (noUltra || class_ok(i));
                if (ok) { if (shard_take(depth)) rec(g + 1, depth + 1); }
                undo(mark);
                if (stop()) return;
            }
        }
    }

    void record();
    void run() {
        t0 = std::chrono::steady_clock::now();
        if (splits.empty()) return;
        rec(1, 0);
    }
};

// -------------------------------------------------- verification of solution
struct VerifyResult { bool ok; std::string msg; };

static VerifyResult verify_solution(int n, const std::vector<int> &e,
                                    const std::vector<int> &f,
                                    const std::vector<int> &pvm) {
    int N = n * (n - 1) / 2;
    int V = n - 2;
    std::vector<int> Pp(V), Ph(V);
    for (int i = 0; i < V; ++i) {
        Pp[i] = (int)floordiv((long long)N + f[i] - e[i], 2);
        Ph[i] = (int)floordiv((long long)N - e[i] - f[i], 2);
    }
    std::vector<std::vector<std::pair<int, int>>> adj(n);
    std::vector<char> present(n, 0);
    std::vector<int> order;
    bool bad = false;
    std::string why;
    auto add = [&](int u, int v, int w) {
        if (bad) return;
        if (w <= 0) { bad = true; why = "non-positive edge weight " + std::to_string(w); return; }
        if (u < 0 || u >= n || v < 0 || v >= n) { bad = true; why = "vertex id out of range"; return; }
        if (!present[u]) { present[u] = 1; order.push_back(u); }
        adj[u].push_back({v, w});
        if (!present[v]) { present[v] = 1; order.push_back(v); }
        adj[v].push_back({u, w});
    };
    // on-path vertices, sorted by (p, id)
    std::vector<std::pair<int, int>> onp;
    for (int i = 0; i < V; ++i) if (Ph[i] == 0) onp.push_back({Pp[i], 2 + i});
    std::sort(onp.begin(), onp.end());
    std::vector<std::pair<int, int>> chain;
    chain.push_back({0, 0});
    for (auto &x : onp) chain.push_back(x);
    chain.push_back({N, 1});
    for (size_t k = 0; k + 1 < chain.size(); ++k)
        add(chain[k].second, chain[k + 1].second, chain[k + 1].first - chain[k].first);
    if (bad) return {false, why};
    // branches grouped by p, in first-occurrence order (mirrors the Python dict)
    std::vector<int> byp_key;
    std::vector<std::vector<int>> byp_mem;
    for (int i = 0; i < V; ++i) {
        if (Ph[i] <= 0) continue;
        int idx = -1;
        for (size_t q = 0; q < byp_key.size(); ++q) if (byp_key[q] == Pp[i]) { idx = (int)q; break; }
        if (idx < 0) { byp_key.push_back(Pp[i]); byp_mem.push_back({}); idx = (int)byp_key.size() - 1; }
        byp_mem[idx].push_back(i);
    }
    std::vector<int> rootp(N + 2, -1);
    for (auto &x : onp) if (x.first >= 0 && x.first <= N) rootp[x.first] = x.second;
    auto hc = [&](int i, int j) {
        long long base = (long long)f[i] + e[j];
        return (int)floordiv((long long)pvm[(size_t)i * V + j] - base, 2);
    };
    for (size_t q = 0; q < byp_key.size(); ++q) {
        int p = byp_key[q];
        if (p < 0 || p > N || rootp[p] < 0)
            return {false, "no on-path attachment vertex at p=" + std::to_string(p)};
        std::vector<int> mem = byp_mem[q];
        std::stable_sort(mem.begin(), mem.end(), [&](int a, int b) { return Ph[a] < Ph[b]; });
        for (size_t idx = 0; idx < mem.size(); ++idx) {
            int i = mem[idx];
            int best = rootp[p], bh = 0;
            for (size_t z = 0; z < idx; ++z) {
                int j = mem[z];
                int hj = Ph[j];
                if (hj < Ph[i] && hc(i, j) == hj && hj > bh) { best = 2 + j; bh = hj; }
            }
            add(best, 2 + i, Ph[i] - bh);
            if (bad) return {false, why};
        }
    }
    if ((int)order.size() != n)
        return {false, "tree has " + std::to_string(order.size()) + " vertices, expected " + std::to_string(n)};
    std::vector<long long> dists;
    std::vector<int> dist(n), vis(n, 0);
    for (int s : order) {
        std::fill(vis.begin(), vis.end(), 0);
        std::deque<int> dq;
        dist[s] = 0; vis[s] = 1; dq.push_back(s);
        int seen = 1;
        while (!dq.empty()) {
            int u = dq.front(); dq.pop_front();
            for (auto &pr : adj[u]) if (!vis[pr.first]) {
                vis[pr.first] = 1; dist[pr.first] = dist[u] + pr.second; ++seen; dq.push_back(pr.first);
            }
        }
        if (seen != n) return {false, "not connected"};
        for (int v : order) if (v > s) dists.push_back(dist[v]);
    }
    std::sort(dists.begin(), dists.end());
    if ((int)dists.size() != N) return {false, "wrong number of pairs"};
    for (int t = 0; t < N; ++t)
        if (dists[t] != t + 1) return {false, "distance multiset wrong"};
    std::vector<std::pair<std::pair<int, int>, int>> el;
    for (int u = 0; u < n; ++u)
        for (auto &pr : adj[u]) if (u < pr.first) el.push_back({{u, pr.first}, pr.second});
    std::sort(el.begin(), el.end());
    std::string edges;
    for (auto &x : el) {
        if (!edges.empty()) edges += ",";
        edges += "(" + std::to_string(x.first.first) + "," + std::to_string(x.first.second) +
                 "," + std::to_string(x.second) + ")";
    }
    return {true, "edges=[" + edges + "]"};
}

// ------------------------------------------------------------------ output
std::string joinv(const std::vector<int> &v) {
    std::string s;
    for (size_t i = 0; i < v.size(); ++i) { if (i) s += ","; s += std::to_string(v[i]); }
    return s;
}

void Search::record() {
    ++solCount;
    solE.push_back(e);
    solF.push_back(f);
    solPV.push_back(pv);
    if (!quiet) printf("SOLUTION e=%s f=%s\n", joinv(e).c_str(), joinv(f).c_str());
    if (verifyMode) {
        VerifyResult vr = verify_solution(n, e, f, pv);
        if (vr.ok) printf("VERIFIED e=%s f=%s %s\n", joinv(e).c_str(), joinv(f).c_str(), vr.msg.c_str());
        else       printf("REJECT %s e=%s f=%s\n", vr.msg.c_str(), joinv(e).c_str(), joinv(f).c_str());
    }
    fflush(stdout);
}

// ------------------------------------------------------------------ main
int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <n> [--nodes-limit K] [--max-solutions K] "
                        "[--split LEVEL K M] [--verify] [--progress] [--quiet] "
                        "[--no-hall] [--no-lb] [--no-attach] [--no-hc] "
                        "[--no-deferred-check] [--no-ultra] [--no-parity] [--no-cover] "
                        "[--no-symmetry-break] [--debug] [--trace]\n", argv[0]);
        return 2;
    }
    int n = atoi(argv[1]);
    if (n < 3) { fprintf(stderr, "n must be >= 3\n"); return 2; }
    Search S(n);
    for (int i = 2; i < argc; ++i) {
        std::string a = argv[i];
        auto need = [&](int k) {
            if (i + k >= argc) { fprintf(stderr, "missing arg for %s\n", a.c_str()); exit(2); }
        };
        if (a == "--nodes-limit")            { need(1); S.nodeLimit = atoll(argv[++i]); }
        else if (a == "--max-solutions")     { need(1); S.maxSolutions = atoll(argv[++i]); }
        else if (a == "--split")             { need(3); S.splitLevel = atoi(argv[i + 1]);
                                               S.splitK = atoll(argv[i + 2]); S.splitM = atoll(argv[i + 3]); i += 3;
                                               if (S.splitM <= 0 || S.splitK < 0 || S.splitK >= S.splitM) {
                                                   fprintf(stderr, "need 0 <= K < M\n"); return 2; }
                                               S.stableDeferred = true; }
        else if (a == "--verify")            S.verifyMode = true;
        else if (a == "--progress")          S.progress = true;
        else if (a == "--quiet")             S.quiet = true;
        else if (a == "--no-hall")           S.noHall = true;
        else if (a == "--no-lb")             S.noLb = true;
        else if (a == "--no-attach")         S.noAttach = true;
        else if (a == "--no-hc")             S.noHc = true;
        else if (a == "--no-deferred-check") S.noDeferredCheck = true;
        else if (a == "--no-ultra")          S.noUltra = true;
        else if (a == "--no-parity")         S.noParity = true;
        else if (a == "--no-cover")          S.noCover = true;
        else if (a == "--no-ub")             S.noUb = true;
        else if (a == "--force-e-upto")      { need(1); S.forceEupto = atoi(argv[++i]); }
        else if (a == "--no-symmetry-break" || a == "--no-sym") S.symmetryBreak = false;
        else if (a == "--stable-deferred")   S.stableDeferred = true;
        else if (a == "--unstable-deferred") S.forceUnstable = true;
        else if (a == "--debug")             S.debug = true;
        else if (a == "--trace")             S.trace = true;
        else { fprintf(stderr, "unknown option %s\n", a.c_str()); return 2; }
    }
    if (S.forceUnstable) S.stableDeferred = false;
    S.run();
    const char *status = S.splits.empty() ? "PARITY_IMPOSSIBLE"
                       : (S.bailed || S.hitSolLimit) ? "BAILED" : "EXHAUSTED";
    printf("DOUBLE_END n=%d N=%d V=%d split=%d:%lld/%lld nodes=%lld solutions=%lld status=%s\n",
           S.n, S.N, S.V, S.splitLevel, S.splitK, S.splitM, S.nodes, S.solCount, status);
    if (S.debug) {
        double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - S.t0).count();
        fprintf(stderr, "DEBUG multi_resolve_nodes=%lld split_counter=%lld seconds=%.3f rate=%.0f/s\n",
                S.multiResolveNodes, S.splitCounter, el, el > 0 ? S.nodes / el : 0.0);
        long long cum = 0;
        for (int d = 0; d < Search::DEPTH_HIST; ++d) {
            if (!S.depthHist[d]) continue;
            cum += S.depthHist[d];
            fprintf(stderr, "DEPTH d=%d nodes=%lld cum_le=%lld\n", d, S.depthHist[d], cum);
        }
    }
    return 0;
}
