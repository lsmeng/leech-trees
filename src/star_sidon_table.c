/* star_sidon_table.c -- exhaustive recomputation of the table S(d) of Lemma 2.5.
   A set W of d distinct positive integers is star-Sidon if the pairwise sums
   w_i+w_j (i<j) are distinct from one another and from the elements.  S(d) is
   the minimum of a_{d-1}+a_d over star-Sidon sets of size d; since that is the
   largest sum, S(d) is the least T admitting such a set with all elements and
   sums <= T.  For each d we increase T until a set is found, so the value is
   certified by an exhaustive refutation at T = S(d)-1 and a witness at T.
   Logic identical to src/star_sidon_table.py (which reproduces d <= 9).
   Build: cc -O2 -o bin/star_sidon_table src/star_sidon_table.c
   Usage: bin/star_sidon_table [dmax]        (default 12)                   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int T, D, w[64];
static unsigned char used[4096];
static long long nodes;

static int dfs(int k) {
    if (k == D) return 1;
    int lo = k ? w[k - 1] + 1 : 1;
    for (int p = lo; p <= T; p++) {
        nodes++;
        if (D - k >= 2 && 2 * p + 1 > T) break;
        if (k >= 1 && p + w[k - 1] > T) break;
        if (used[p]) continue;
        int ok = 1;
        for (int i = 0; i < k; i++) { int s = w[i] + p; if (s > T || used[s]) { ok = 0; break; } }
        if (!ok) continue;
        used[p] = 1;
        for (int i = 0; i < k; i++) used[w[i] + p] = 1;
        w[k] = p;
        if (dfs(k + 1)) return 1;
        used[p] = 0;
        for (int i = 0; i < k; i++) used[w[i] + p] = 0;
    }
    return 0;
}

int main(int argc, char **argv) {
    int dmax = argc > 1 ? atoi(argv[1]) : 12;
    T = 1;
    printf("d,S(d),witness,refute_nodes\n");
    for (D = 2; D <= dmax; D++) {
        long long last = 0;
        for (;;) {
            memset(used, 0, sizeof used);
            nodes = 0;
            if (dfs(0)) {
                printf("%d,%d,\"", D, T);
                for (int i = 0; i < D; i++) printf("%s%d", i ? " " : "", w[i]);
                printf("\",%lld\n", last);
                fflush(stdout);
                break;
            }
            last = nodes;
            T++;
        }
    }
    printf("VERIFIED_STAR_SIDON_TABLE\n");
    return 0;
}
