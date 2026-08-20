/* forced_family.c — forced-weight DFS over edge orderings on a FIXED tree topology.
 *
 * Same algorithm as src/filters.py::leech_labelings_of_topology (Calhoun Lemma 2.6 /
 * SWZ Find-Next-Weight, ledger L4): the k-th smallest weight is forced to be the least
 * positive integer not realised as a distance in the forest of the k-1 lighter edges,
 * so a labeling of a fixed topology is determined by the ORDER in which edges receive
 * the forced weights.  DFS over that order with pruning (distance repeated or > S).
 * Symmetry breaking: pendant edges hanging at the same vertex are interchangeable by an
 * automorphism fixing all other edges; only the lowest-index unplaced one is tried.
 *
 * Input (stdin): one shape per line:  n  u1 v1 u2 v2 ... u_{n-1} v_{n-1}
 *   optionally followed by  "G g_1 b_1 g_2 b_2 ... g_m b_m"  (per-edge branch tags):
 *   edges tagged (g,b) with g >= 0 belong to branch b of symmetry group g, where the
 *   branches of one group are pairwise identical rooted subtrees hanging at a common
 *   vertex (e.g. equal-length spider legs, equal-size star branches of a diameter-4
 *   tree).  Permuting the branches of a group is a tree automorphism, so labelings
 *   come in orbits of size prod_g (#branches_g)!; the DFS keeps exactly one
 *   representative per orbit by requiring that branch b of a group receives its
 *   FIRST edge only after branches 0..b-1 of the same group have received one
 *   (all weights are distinct, so "first edge" times give a strict order on the
 *   branches and each orbit has exactly one representative).  g = -1: no tag.
 * Output: RES id=<line#> n=<n> nodes=<dfs placements> found=<#labelings> capped=<0/1>
 *         and for each labeling found a WITNESS line with the weighted edges.
 * Optional argv[1]: node cap per shape (0 = exact/no cap; capped shapes reported).
 * Optional argv[2]: S-slack (TEST ONLY): use S' = S + slack as the distance budget and
 *   count complete all-distinct labelings (no perfectness).  Used by validate.py to
 *   machine-check the branch symmetry logic via exact orbit-count identities.
 *
 * This file is standalone evidence tooling for theory-lab/exp-families; it does not
 * modify anything in the main repo.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

#define MAXN 64
#define MAXS 1400            /* >= C(51,2) = 1275 */

static int n, m, S;
static int eu[MAXN], ev[MAXN], ecls[MAXN];
static int placed[MAXN];
static int adj_nbr[MAXN][MAXN], adj_w[MAXN][MAXN];
static int adj_cnt[MAXN];
static unsigned char used[MAXS + 2];
static long long nodes, node_cap;
static long long attempts;
static double time_cap = 0.0, t_start;
static int nfound, capped;
static int witness_w[MAXN];
static long long line_id;
static int slack = 0;

/* branch symmetry tags: per edge, group id (or -1) and branch index in group */
static int ebg[MAXN], ebb[MAXN];
static int branch_cnt[MAXN][MAXN];   /* placed-edge count per (group, branch) */
static int nbranch[MAXN];            /* #branches in each group */
static int have_tags;

static int visited[MAXN], vstamp = 0;

static int dists_from(int src, int *lv, int *ld) {
    int stack[MAXN], sp = 0, cnt = 0;
    static int dist[MAXN];
    ++vstamp;
    stack[sp++] = src; visited[src] = vstamp; dist[src] = 0;
    while (sp) {
        int u = stack[--sp];
        lv[cnt] = u; ld[cnt] = dist[u]; cnt++;
        for (int i = 0; i < adj_cnt[u]; i++) {
            int v = adj_nbr[u][i];
            if (visited[v] != vstamp) {
                visited[v] = vstamp; dist[v] = dist[u] + adj_w[u][i];
                stack[sp++] = v;
            }
        }
    }
    return cnt;
}

static void print_witness(void) {
    printf("WITNESS id=%lld n=%d edges=", line_id, n);
    for (int i = 0; i < m; i++)
        printf("%d,%d,%d;", eu[i], ev[i], witness_w[i]);
    printf("\n");
    fflush(stdout);
}

static void rec(int nw, int depth) {
    if (capped) return;
    if (depth == m) {
        nfound++;
        print_witness();
        return;
    }
    for (int i = 0; i < m; i++) {
        if (placed[i]) continue;
        int skip = 0;
        for (int j = 0; j < i; j++)
            if (!placed[j] && ecls[j] == ecls[i]) { skip = 1; break; }
        if (skip) continue;
        /* branch-opening order: a fresh branch of a group may open only if all
           lower-indexed branches of the group are already open */
        if (have_tags && ebg[i] >= 0 && branch_cnt[ebg[i]][ebb[i]] == 0) {
            for (int b = 0; b < ebb[i]; b++)
                if (branch_cnt[ebg[i]][b] == 0) { skip = 1; break; }
            if (skip) continue;
        }
        int u = eu[i], v = ev[i];
        attempts++;
        if (time_cap > 0 && (attempts & 0xfff) == 0 && now_s() - t_start > time_cap)
            capped = 1;
        if (capped) return;
        int luv[MAXN], lud[MAXN], lvv[MAXN], lvd[MAXN];
        int cu = dists_from(u, luv, lud);
        int cv = dists_from(v, lvv, lvd);
        int newd[MAXN * MAXN]; int nc = 0, ok = 1;
        for (int a = 0; a < cu && ok; a++) {
            int base = lud[a] + nw;
            for (int b = 0; b < cv; b++) {
                int d = base + lvd[b];
                if (d > S || used[d]) { ok = 0; break; }
                used[d] = 1; newd[nc++] = d;
            }
        }
        if (!ok) {
            for (int t = 0; t < nc; t++) used[newd[t]] = 0;
            continue;
        }
        adj_nbr[u][adj_cnt[u]] = v; adj_w[u][adj_cnt[u]] = nw; adj_cnt[u]++;
        adj_nbr[v][adj_cnt[v]] = u; adj_w[v][adj_cnt[v]] = nw; adj_cnt[v]++;
        placed[i] = 1; witness_w[i] = nw;
        if (have_tags && ebg[i] >= 0) branch_cnt[ebg[i]][ebb[i]]++;
        nodes++;
        if (node_cap && nodes > node_cap) capped = 1;
        int nw2 = nw + 1;
        while (nw2 <= S && used[nw2]) nw2++;
        rec(nw2, depth + 1);
        placed[i] = 0;
        if (have_tags && ebg[i] >= 0) branch_cnt[ebg[i]][ebb[i]]--;
        adj_cnt[u]--; adj_cnt[v]--;
        for (int t = 0; t < nc; t++) used[newd[t]] = 0;
        if (capped) return;
    }
}

int main(int argc, char **argv) {
    node_cap = (argc > 1) ? atoll(argv[1]) : 0;
    slack = (argc > 2) ? atoi(argv[2]) : 0;
    time_cap = (argc > 3) ? atof(argv[3]) : 0.0;
    setvbuf(stdout, NULL, _IOLBF, 0);
    char buf[8192];
    line_id = -1;
    while (fgets(buf, sizeof buf, stdin)) {
        line_id++;
        char *p = buf;
        n = (int)strtol(p, &p, 10);
        if (n < 2 || n >= MAXN) { fprintf(stderr, "bad n line %lld\n", line_id); return 1; }
        m = n - 1;
        S = n * (n - 1) / 2 + slack;
        if (S > MAXS) { fprintf(stderr, "S too big line %lld\n", line_id); return 1; }
        int deg[MAXN]; memset(deg, 0, sizeof deg);
        for (int i = 0; i < m; i++) {
            eu[i] = (int)strtol(p, &p, 10);
            ev[i] = (int)strtol(p, &p, 10);
            deg[eu[i]]++; deg[ev[i]]++;
        }
        /* optional branch tags */
        have_tags = 0;
        for (int i = 0; i < m; i++) { ebg[i] = -1; ebb[i] = 0; }
        while (*p == ' ' || *p == '\t') p++;
        if (*p == 'G') {
            p++;
            have_tags = 1;
            memset(nbranch, 0, sizeof nbranch);
            memset(branch_cnt, 0, sizeof branch_cnt);
            for (int i = 0; i < m; i++) {
                ebg[i] = (int)strtol(p, &p, 10);
                ebb[i] = (int)strtol(p, &p, 10);
                if (ebg[i] >= MAXN || ebb[i] >= MAXN) { fprintf(stderr, "bad tag line %lld\n", line_id); return 1; }
                if (ebg[i] >= 0 && ebb[i] + 1 > nbranch[ebg[i]]) nbranch[ebg[i]] = ebb[i] + 1;
            }
        }
        /* symmetry classes: pendant edges at the same support vertex share a class */
        for (int i = 0; i < m; i++) {
            if (deg[ev[i]] == 1)      ecls[i] = 1000 + eu[i];
            else if (deg[eu[i]] == 1) ecls[i] = 1000 + ev[i];
            else                      ecls[i] = i;
        }
        memset(placed, 0, sizeof placed);
        memset(adj_cnt, 0, sizeof adj_cnt);
        memset(used, 0, (size_t)S + 2);
        nodes = 0; attempts = 0; nfound = 0; capped = 0;
        t_start = now_s();
        rec(1, 0);
        printf("RES id=%lld n=%d nodes=%lld attempts=%lld found=%d capped=%d time=%.2f\n",
               line_id, n, nodes, attempts, nfound, capped, now_s() - t_start);
    }
    return 0;
}
