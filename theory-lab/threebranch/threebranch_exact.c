#define _POSIX_C_SOURCE 200809L

/* Exact top-down search for Leech trees with exactly three branch vertices.
 *
 * The branch centres have weighted coordinates 0, Q1, Q1+Q2.  Every selected
 * non-centre vertex is a mark on a centre leg or an interior mark of the core
 * path.  The four maximum-pair classes AA, BB, AB and AC are exactly those in
 * threebranch_cleanroom.py.  At each node the greatest missing distance is
 * realised by one new mark or by a pair of new marks.
 *
 * Default certificate mode recomputes the complete distance set at every DFS
 * node and compares it with the incremental bitset.  --fast disables only
 * that diagnostic.  --max-nodes is diagnostic: a capped run is UNKNOWN.
 *
 * Build:
 *   cc -O3 -std=c11 -Wall -Wextra -pedantic -o threebranch_exact \
 *      threebranch_exact.c
 * Usage:
 *   threebranch_exact n [AA|BB|AB|AC|all] [--fast] [--no-pairs] [--max-nodes K]
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 32
#define MAXM (MAXN - 3)
#define NWB 8                       /* 512 values; enough through n=32 here */
#define MAXNEW (MAXM + 4)
#define MAXCAND (2 * MAXN * MAXN)

typedef struct {
    int8_t kind;                    /* 'L' leg mark or 'S' spine mark */
    int8_t centre;
    int8_t leg;
    int16_t x;
} Mark;

typedef struct {
    int nvalues;
    int16_t values[MAXNEW];
    int opened_centre;
} Undo;

static int n, N, q1, q2, core_total;
static int centre_pos[3];
static int fixed_count[3], fixed_caps[3][2], fresh_caps[3];
static int nlegs[3], nmarks;
static Mark marks[MAXM];
static uint64_t used[NWB];
static const int required_legs[3] = {2, 1, 2};

static uint64_t anchors_generated, anchors, nodes, nsol;
static uint64_t candidate_marks, candidate_pairs, legal_children;
static uint64_t legal_single_children, legal_pair_children;
static uint64_t frontier;
static uint64_t node_cap;
static int deepest_missing_offset, max_noncentre_marks, window_size;
static int shard_index = -1, shard_count = 0;
static int paranoid = 1, capped = 0;
static int enumerate_pairs = 1;
static int diameter_intro = 0;
static const char *active_mode = "";
static int pair_probe = 0;
static uint64_t pair_probe_children = 0;

static double now_seconds(void) {
    struct timespec value;
    clock_gettime(CLOCK_MONOTONIC, &value);
    return value.tv_sec + 1e-9 * value.tv_nsec;
}

static inline int bit(int value) {
    return (int)((used[value >> 6] >> (value & 63)) & 1ULL);
}

static inline void set_bit(int value) {
    used[value >> 6] |= 1ULL << (value & 63);
}

static inline void clear_bit(int value) {
    used[value >> 6] &= ~(1ULL << (value & 63));
}

static inline int leg_cap(int centre, int leg) {
    return leg < fixed_count[centre] ? fixed_caps[centre][leg] : fresh_caps[centre];
}

static int legal_mark(Mark mark) {
    if (mark.kind == 'S')
        return mark.x > 0 && mark.x < core_total && mark.x != q1;
    if (mark.kind != 'L' || mark.centre < 0 || mark.centre >= 3)
        return 0;
    if (mark.leg < 0 || mark.leg > nlegs[mark.centre] || mark.x < 1)
        return 0;
    return mark.x <= leg_cap(mark.centre, mark.leg);
}

static inline int centre_distance(Mark mark, int centre) {
    if (mark.kind == 'S')
        return abs(mark.x - centre_pos[centre]);
    return mark.x + abs(centre_pos[mark.centre] - centre_pos[centre]);
}

static inline int mark_distance(Mark first, Mark second) {
    if (first.kind == 'S' && second.kind == 'S')
        return abs(first.x - second.x);
    if (first.kind == 'S')
        return second.x + abs(first.x - centre_pos[second.centre]);
    if (second.kind == 'S')
        return first.x + abs(second.x - centre_pos[first.centre]);
    if (first.centre == second.centre && first.leg == second.leg)
        return abs(first.x - second.x);
    return first.x + second.x + abs(centre_pos[first.centre] - centre_pos[second.centre]);
}

static int apply_mark(Mark mark, Undo *undo) {
    if (!legal_mark(mark) || nmarks >= n - 3)
        return 0;
    int new_values[MAXNEW];
    int count = 0;
    for (int centre = 0; centre < 3; centre++)
        new_values[count++] = centre_distance(mark, centre);
    for (int i = 0; i < nmarks; i++)
        new_values[count++] = mark_distance(mark, marks[i]);

    uint64_t local[NWB];
    memset(local, 0, sizeof local);
    for (int i = 0; i < count; i++) {
        int value = new_values[i];
        if (value < 1 || value > N || bit(value))
            return 0;
        if ((local[value >> 6] >> (value & 63)) & 1ULL)
            return 0;
        local[value >> 6] |= 1ULL << (value & 63);
    }

    undo->nvalues = count;
    undo->opened_centre = -1;
    for (int i = 0; i < count; i++) {
        set_bit(new_values[i]);
        undo->values[i] = (int16_t)new_values[i];
    }
    if (mark.kind == 'L' && mark.leg == nlegs[mark.centre]) {
        undo->opened_centre = mark.centre;
        nlegs[mark.centre]++;
    }
    marks[nmarks++] = mark;
    return 1;
}

static void undo_mark(const Undo *undo) {
    for (int i = 0; i < undo->nvalues; i++)
        clear_bit(undo->values[i]);
    nmarks--;
    if (undo->opened_centre >= 0)
        nlegs[undo->opened_centre]--;
}

static int branch_feasible(void) {
    int missing = 0;
    for (int centre = 0; centre < 3; centre++)
        if (nlegs[centre] < required_legs[centre])
            missing += required_legs[centre] - nlegs[centre];
    return missing <= n - 3 - nmarks;
}

static void paranoid_check(void) {
    uint64_t rebuilt[NWB];
    memset(rebuilt, 0, sizeof rebuilt);
    int raw_count = 0;

#define ADD_REBUILT(value_expression) do {                                      \
        int value_ = (value_expression);                                        \
        if (value_ < 1 || value_ > N) {                                         \
            fprintf(stderr, "PARANOID range mode=%s value=%d\n", active_mode, value_); \
            exit(2);                                                            \
        }                                                                       \
        if ((rebuilt[value_ >> 6] >> (value_ & 63)) & 1ULL) {                  \
            fprintf(stderr, "PARANOID duplicate mode=%s value=%d\n", active_mode, value_); \
            exit(2);                                                            \
        }                                                                       \
        rebuilt[value_ >> 6] |= 1ULL << (value_ & 63);                         \
        raw_count++;                                                            \
    } while (0)

    ADD_REBUILT(q1);
    ADD_REBUILT(q2);
    ADD_REBUILT(core_total);
    for (int i = 0; i < nmarks; i++) {
        for (int centre = 0; centre < 3; centre++)
            ADD_REBUILT(centre_distance(marks[i], centre));
        for (int j = i + 1; j < nmarks; j++)
            ADD_REBUILT(mark_distance(marks[i], marks[j]));
    }
#undef ADD_REBUILT

    int expected = (nmarks + 3) * (nmarks + 2) / 2;
    if (raw_count != expected || memcmp(rebuilt, used, sizeof used) != 0) {
        fprintf(stderr, "PARANOID mismatch mode=%s raw=%d expected=%d\n",
                active_mode, raw_count, expected);
        exit(2);
    }
}

static int compare_int(const void *left, const void *right) {
    int a = *(const int *)left, b = *(const int *)right;
    return (a > b) - (a < b);
}

typedef struct { int u, v, w; } Edge;

static void report_solution(void) {
    if (nlegs[0] < 2 || nlegs[1] < 1 || nlegs[2] < 2) {
        fprintf(stderr, "INTERNAL solution lacks three branch centres\n");
        exit(2);
    }
    Edge edges[MAXN];
    int edge_count = 0, next_vertex = 3;
    int point_x[MAXN], point_v[MAXN], point_count = 0;
    point_x[point_count] = 0; point_v[point_count++] = 0;
    point_x[point_count] = q1; point_v[point_count++] = 1;
    point_x[point_count] = core_total; point_v[point_count++] = 2;
    for (int i = 0; i < nmarks; i++) if (marks[i].kind == 'S') {
        point_x[point_count] = marks[i].x;
        point_v[point_count++] = next_vertex++;
    }
    for (int i = 0; i < point_count; i++)
        for (int j = i + 1; j < point_count; j++)
            if (point_x[j] < point_x[i]) {
                int tx = point_x[i], tv = point_v[i];
                point_x[i] = point_x[j]; point_v[i] = point_v[j];
                point_x[j] = tx; point_v[j] = tv;
            }
    for (int i = 0; i + 1 < point_count; i++)
        edges[edge_count++] = (Edge){point_v[i], point_v[i + 1], point_x[i + 1] - point_x[i]};

    for (int centre = 0; centre < 3; centre++) {
        for (int leg = 0; leg < nlegs[centre]; leg++) {
            int depths[MAXM], count = 0;
            for (int i = 0; i < nmarks; i++)
                if (marks[i].kind == 'L' && marks[i].centre == centre && marks[i].leg == leg)
                    depths[count++] = marks[i].x;
            qsort(depths, (size_t)count, sizeof depths[0], compare_int);
            int previous_vertex = centre, previous_x = 0;
            for (int i = 0; i < count; i++) {
                edges[edge_count++] = (Edge){previous_vertex, next_vertex, depths[i] - previous_x};
                previous_vertex = next_vertex++;
                previous_x = depths[i];
            }
        }
    }
    if (next_vertex != n || edge_count != n - 1) {
        fprintf(stderr, "INTERNAL witness size vertices=%d edges=%d\n", next_vertex, edge_count);
        exit(2);
    }
    nsol++;
    printf("WITNESS n=%d mode=%s q1=%d q2=%d edges=", n, active_mode, q1, q2);
    for (int i = 0; i < edge_count; i++)
        printf("%d,%d,%d;", edges[i].u, edges[i].v, edges[i].w);
    printf("\n");
    fflush(stdout);
}

static int compare_mark(Mark first, Mark second) {
    if (first.kind != second.kind)
        return (first.kind > second.kind) - (first.kind < second.kind);
    if (first.centre != second.centre)
        return (first.centre > second.centre) - (first.centre < second.centre);
    if (first.leg != second.leg)
        return (first.leg > second.leg) - (first.leg < second.leg);
    return (first.x > second.x) - (first.x < second.x);
}

static void dfs(int target);

static void try_single(int target, Mark mark) {
    candidate_marks++;
    Undo undo;
    if (!apply_mark(mark, &undo))
        return;
    if (bit(target) && branch_feasible()) {
        legal_children++;
        legal_single_children++;
        dfs(target - 1);
    }
    undo_mark(&undo);
}

static void add_unique_candidate(Mark *candidates, int *count, Mark mark) {
    if (!legal_mark(mark))
        return;
    for (int i = 0; i < *count; i++)
        if (compare_mark(candidates[i], mark) == 0)
            return;
    if (*count >= MAXCAND) {
        fprintf(stderr, "candidate buffer exceeded\n");
        exit(2);
    }
    candidates[(*count)++] = mark;
}

static int one_mark_candidates(int target, Mark *candidates) {
    int count = 0;
    /* Pair the new mark with one of the three implicit centres. */
    if (!diameter_intro) {
        for (int centre = 0; centre < 3; centre++) {
            for (int leg = 0; leg <= nlegs[centre]; leg++)
                for (int other = 0; other < 3; other++)
                    add_unique_candidate(candidates, &count,
                        (Mark){'L', centre, leg,
                               target - abs(centre_pos[centre] - centre_pos[other])});
        }
        for (int other = 0; other < 3; other++) {
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, centre_pos[other] - target});
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, centre_pos[other] + target});
        }
    }

    /* Or pair it with one already selected non-centre mark. */
    int old_limit = diameter_intro && nmarks > 2 ? 2 : nmarks;
    for (int index = 0; index < old_limit; index++) {
        Mark old = marks[index];
        for (int centre = 0; centre < 3; centre++)
            for (int leg = 0; leg <= nlegs[centre]; leg++) {
                int x;
                if (old.kind == 'S') {
                    x = target - abs(old.x - centre_pos[centre]);
                } else if (old.centre == centre && old.leg == leg) {
                    add_unique_candidate(candidates, &count,
                                         (Mark){'L', centre, leg, old.x - target});
                    x = old.x + target;
                } else {
                    x = target - old.x - abs(centre_pos[old.centre] - centre_pos[centre]);
                }
                add_unique_candidate(candidates, &count, (Mark){'L', centre, leg, x});
            }
        if (old.kind == 'S') {
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, old.x - target});
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, old.x + target});
        } else {
            int delta = target - old.x;
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, centre_pos[old.centre] - delta});
            add_unique_candidate(candidates, &count,
                                 (Mark){'S', -1, -1, centre_pos[old.centre] + delta});
        }
    }
    return count;
}

static void try_pair(int target, Mark first, Mark second) {
    if (mark_distance(first, second) != target)
        return;
    candidate_pairs++;
    Undo first_undo, second_undo;
    if (!apply_mark(first, &first_undo))
        return;
    if (bit(target)) {
        undo_mark(&first_undo);       /* the one-mark branch already covers this */
        return;
    }
    if (!apply_mark(second, &second_undo)) {
        undo_mark(&first_undo);
        return;
    }
    if (!bit(target)) {
        fprintf(stderr, "INTERNAL pair failed to realize target\n");
        exit(2);
    }
    if (branch_feasible()) {
        legal_children++;
        legal_pair_children++;
        if (pair_probe) {
            if (paranoid)
                paranoid_check();
            pair_probe_children++;
        } else {
            dfs(target - 1);
        }
    }
    undo_mark(&second_undo);
    undo_mark(&first_undo);
}

typedef struct {
    int8_t kind;
    int8_t centre;
    int8_t leg;
    int16_t cap;
} Slot;

static int pair_slots(Slot *slots_out, const int base_legs[3]) {
    int count = 0;
    for (int centre = 0; centre < 3; centre++)
        for (int leg = 0; leg <= base_legs[centre] + 1; leg++)
            slots_out[count++] = (Slot){'L', centre, leg, leg_cap(centre, leg)};
    slots_out[count++] = (Slot){'S', -1, -1, core_total - 1};
    return count;
}

static int slot_pair_allowed(Slot first, Slot second, const int base_legs[3]) {
    for (int centre = 0; centre < 3; centre++) {
        int first_is_second_fresh = first.kind == 'L' && first.centre == centre &&
                                    first.leg == base_legs[centre] + 1;
        int second_is_second_fresh = second.kind == 'L' && second.centre == centre &&
                                     second.leg == base_legs[centre] + 1;
        if (first_is_second_fresh || second_is_second_fresh) {
            Slot other = first_is_second_fresh ? second : first;
            if (other.kind != 'L' || other.centre != centre ||
                other.leg != base_legs[centre])
                return 0;
        }
    }
    return 1;
}

static int legal_spine_coordinate(int x) {
    return x > 0 && x < core_total && x != q1;
}

static void enumerate_pair_children(int target, const int base_legs[3]) {
    Slot slots[MAXN];
    int slot_count = pair_slots(slots, base_legs);
    for (int i = 0; i < slot_count; i++) {
        for (int j = i; j < slot_count; j++) {
            Slot first_slot = slots[i], second_slot = slots[j];
            if (!slot_pair_allowed(first_slot, second_slot, base_legs))
                continue;

            if (first_slot.kind == 'L' && second_slot.kind == 'L') {
                int same_leg = first_slot.centre == second_slot.centre &&
                               first_slot.leg == second_slot.leg;
                if (same_leg) {
                    for (int x = 1; x + target <= first_slot.cap; x++)
                        try_pair(target,
                                 (Mark){'L', first_slot.centre, first_slot.leg, x},
                                 (Mark){'L', second_slot.centre, second_slot.leg,
                                        x + target});
                } else {
                    int core = abs(centre_pos[first_slot.centre] -
                                   centre_pos[second_slot.centre]);
                    int sum = target - core;
                    for (int x = 1; x <= first_slot.cap; x++) {
                        int y = sum - x;
                        if (y < 1 || y > second_slot.cap)
                            continue;
                        if (first_slot.centre == second_slot.centre &&
                            first_slot.leg == base_legs[first_slot.centre] &&
                            second_slot.leg == base_legs[first_slot.centre] + 1 &&
                            x >= y)
                            continue;
                        try_pair(target,
                                 (Mark){'L', first_slot.centre, first_slot.leg, x},
                                 (Mark){'L', second_slot.centre, second_slot.leg, y});
                    }
                }
            } else if (first_slot.kind == 'S' && second_slot.kind == 'S') {
                for (int x = 1; x + target < core_total; x++)
                    if (legal_spine_coordinate(x) && legal_spine_coordinate(x + target))
                        try_pair(target, (Mark){'S', -1, -1, x},
                                 (Mark){'S', -1, -1, x + target});
            } else {
                Slot leg_slot = first_slot.kind == 'L' ? first_slot : second_slot;
                for (int spine_x = 1; spine_x < core_total; spine_x++) {
                    if (!legal_spine_coordinate(spine_x))
                        continue;
                    int leg_x = target - abs(spine_x - centre_pos[leg_slot.centre]);
                    if (leg_x < 1 || leg_x > leg_slot.cap)
                        continue;
                    Mark leg_mark = {'L', leg_slot.centre, leg_slot.leg, leg_x};
                    Mark spine_mark = {'S', -1, -1, spine_x};
                    if (first_slot.kind == 'L')
                        try_pair(target, leg_mark, spine_mark);
                    else
                        try_pair(target, spine_mark, leg_mark);
                }
            }
        }
    }
}

static void dfs(int target) {
    if (capped)
        return;
    if (node_cap && nodes >= node_cap) {
        capped = 1;
        return;
    }
    nodes++;
    if (paranoid)
        paranoid_check();
    while (target >= 1 && bit(target))
        target--;
    int offset = N - target;
    if (offset > deepest_missing_offset)
        deepest_missing_offset = offset;
    if (nmarks > max_noncentre_marks)
        max_noncentre_marks = nmarks;
    if (target == 0) {
        if (nmarks != n - 3) {
            fprintf(stderr, "INTERNAL complete distances with %d marks\n", nmarks);
            exit(2);
        }
        report_solution();
        return;
    }
    if (window_size && N - target > window_size) {
        frontier++;
        return;
    }

    int base_legs[3] = {nlegs[0], nlegs[1], nlegs[2]};
    Mark candidates[MAXCAND];
    int candidate_count = one_mark_candidates(target, candidates);
    for (int i = 0; i < candidate_count; i++)
        try_single(target, candidates[i]);

    if (enumerate_pairs && nmarks + 2 <= n - 3) {
        enumerate_pair_children(target, base_legs);
    }
}

static int add_initial_value(int value) {
    if (value < 1 || value > N || bit(value))
        return 0;
    set_bit(value);
    return 1;
}

static void run_anchor(
    int q1_value,
    int q2_value,
    int counts[3],
    int caps[3][2],
    int fresh[3],
    Mark first_tip,
    Mark second_tip
) {
    if (capped)
        return;
    anchors_generated++;
    q1 = q1_value;
    q2 = q2_value;
    core_total = q1 + q2;
    centre_pos[0] = 0;
    centre_pos[1] = q1;
    centre_pos[2] = core_total;
    memcpy(fixed_count, counts, sizeof fixed_count);
    memcpy(fixed_caps, caps, sizeof fixed_caps);
    memcpy(fresh_caps, fresh, sizeof fresh_caps);
    memset(nlegs, 0, sizeof nlegs);
    memset(used, 0, sizeof used);
    nmarks = 0;
    if (!add_initial_value(q1) || !add_initial_value(q2) || !add_initial_value(core_total))
        return;
    Undo first_undo, second_undo;
    if (!apply_mark(first_tip, &first_undo))
        return;
    if (!apply_mark(second_tip, &second_undo)) {
        undo_mark(&first_undo);
        return;
    }
    if (!bit(N) || !branch_feasible())
        return;
    anchors++;
    dfs(N - 1);
}

static void run_AA(void) {
    active_mode = "AA";
    for (int long_tip = N / 2 + 1; long_tip < N && !capped; long_tip++) {
        if (shard_count && long_tip % shard_count != shard_index)
            continue;
        int short_tip = N - long_tip;
        for (int a = 1; a < short_tip - 1 && !capped; a++)
            for (int b = 1; b < short_tip - a && !capped; b++) {
                int fresh[3] = {short_tip - 1, short_tip - a - 1,
                                short_tip - a - b - 1};
                if (fresh[1] < 1 || fresh[2] < 1)
                    continue;
                int counts[3] = {2, 0, 0};
                int caps[3][2] = {{long_tip, short_tip}, {0, 0}, {0, 0}};
                run_anchor(a, b, counts, caps, fresh,
                           (Mark){'L', 0, 0, long_tip},
                           (Mark){'L', 0, 1, short_tip});
            }
    }
}

static void run_BB(void) {
    active_mode = "BB";
    for (int long_tip = N / 2 + 1; long_tip < N && !capped; long_tip++) {
        if (shard_count && long_tip % shard_count != shard_index)
            continue;
        int short_tip = N - long_tip;
        for (int a = 1; a < short_tip - 1 && !capped; a++)
            for (int b = a + 1; b < short_tip && !capped; b++) {
                int fresh[3] = {short_tip - a - 1, short_tip - 1,
                                short_tip - b - 1};
                if (fresh[0] < 1 || fresh[2] < 1)
                    continue;
                int counts[3] = {0, 2, 0};
                int caps[3][2] = {{0, 0}, {long_tip, short_tip}, {0, 0}};
                run_anchor(a, b, counts, caps, fresh,
                           (Mark){'L', 1, 0, long_tip},
                           (Mark){'L', 1, 1, short_tip});
            }
    }
}

static void run_AB(void) {
    active_mode = "AB";
    for (int end_tip = 1; end_tip < N - 2 && !capped; end_tip++) {
        if (shard_count && end_tip % shard_count != shard_index)
            continue;
        for (int middle_tip = 2; middle_tip < N - end_tip && !capped; middle_tip++) {
            int a = N - end_tip - middle_tip;
            if (a < 1)
                continue;
            for (int b = 1; b < middle_tip && !capped; b++) {
                int left_cap_a = end_tip - 1;
                int left_cap_b = a + middle_tip - 1;
                int middle_cap_a = middle_tip - 1;
                int middle_cap_b = end_tip + a - 1;
                int right_cap_a = middle_tip - b - 1;
                int right_cap_b = end_tip + a - b - 1;
                int fresh[3] = {
                    left_cap_a < left_cap_b ? left_cap_a : left_cap_b,
                    middle_cap_a < middle_cap_b ? middle_cap_a : middle_cap_b,
                    right_cap_a < right_cap_b ? right_cap_a : right_cap_b,
                };
                if (fresh[0] < 1 || fresh[2] < 1)
                    continue;
                int counts[3] = {1, 1, 0};
                int caps[3][2] = {{end_tip, 0}, {middle_tip, 0}, {0, 0}};
                run_anchor(a, b, counts, caps, fresh,
                           (Mark){'L', 0, 0, end_tip},
                           (Mark){'L', 1, 0, middle_tip});
            }
        }
    }
}

static void run_AC(void) {
    active_mode = "AC";
    for (int left_tip = 1; left_tip < N && !capped; left_tip++) {
        if (shard_count && left_tip % shard_count != shard_index)
            continue;
        for (int right_tip = left_tip + 1; right_tip < N - left_tip && !capped; right_tip++) {
            int total = N - left_tip - right_tip;
            if (total < 2)
                continue;
            for (int a = 1; a < total && !capped; a++) {
                int b = total - a;
                int middle_a = b + right_tip - 1;
                int middle_b = left_tip + a - 1;
                int right_a = right_tip - 1;
                int right_b = left_tip + total - 1;
                int fresh[3] = {
                    left_tip - 1,
                    middle_a < middle_b ? middle_a : middle_b,
                    right_a < right_b ? right_a : right_b,
                };
                if (fresh[0] < 1 || fresh[1] < 1 || fresh[2] < 1)
                    continue;
                int counts[3] = {1, 0, 1};
                int caps[3][2] = {{left_tip, 0}, {0, 0}, {right_tip, 0}};
                run_anchor(a, b, counts, caps, fresh,
                           (Mark){'L', 0, 0, left_tip},
                           (Mark){'L', 2, 0, right_tip});
            }
        }
    }
}

static int run_pair_probe(void) {
    /* Independent Python brute enumeration gives exactly three legal two-mark
       children for this state and target; one is c0:7 joined to c2:8. */
    n = 8;
    N = 28;
    q1 = 2;
    q2 = 3;
    core_total = 5;
    centre_pos[0] = 0;
    centre_pos[1] = 2;
    centre_pos[2] = 5;
    memset(fixed_count, 0, sizeof fixed_count);
    memset(fixed_caps, 0, sizeof fixed_caps);
    for (int centre = 0; centre < 3; centre++)
        fresh_caps[centre] = 10;
    memset(nlegs, 0, sizeof nlegs);
    memset(used, 0, sizeof used);
    nmarks = 0;
    active_mode = "PAIR_PROBE";
    if (!add_initial_value(q1) || !add_initial_value(q2) || !add_initial_value(core_total)) {
        fprintf(stderr, "pair probe failed to initialise centres\n");
        return 2;
    }
    pair_probe = 1;
    int base_legs[3] = {0, 0, 0};
    enumerate_pair_children(20, base_legs);
    pair_probe = 0;
    if (nmarks != 0 || pair_probe_children != 3) {
        fprintf(stderr, "pair probe mismatch children=%llu marks=%d\n",
                (unsigned long long)pair_probe_children, nmarks);
        return 2;
    }
    printf("{\"probe\":\"two-new-mark\",\"q1\":2,\"q2\":3,"
           "\"target\":20,\"legal_pair_children\":%llu,\"status\":\"PASS\"}\n",
           (unsigned long long)pair_probe_children);
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 2 && !strcmp(argv[1], "--pair-probe"))
        return run_pair_probe();
    if (argc < 2) {
        fprintf(stderr, "usage: %s n [AA|BB|AB|AC|all] [--fast] [--no-pairs] [--diameter-intro] "
                        "[--window W] [--shard I K] [--max-nodes K]\n", argv[0]);
        return 1;
    }
    n = atoi(argv[1]);
    if (n < 8 || n >= MAXN) {
        fprintf(stderr, "n must satisfy 8 <= n < %d\n", MAXN);
        return 1;
    }
    N = n * (n - 1) / 2;
    if (N >= 64 * NWB) {
        fprintf(stderr, "N exceeds bitset build\n");
        return 1;
    }
    const char *mode = "all";
    int index = 2;
    if (index < argc && argv[index][0] != '-')
        mode = argv[index++];
    while (index < argc) {
        if (!strcmp(argv[index], "--fast")) {
            paranoid = 0;
            index++;
        } else if (!strcmp(argv[index], "--no-pairs")) {
            enumerate_pairs = 0;
            index++;
        } else if (!strcmp(argv[index], "--diameter-intro")) {
            diameter_intro = 1;
            index++;
        } else if (!strcmp(argv[index], "--window")) {
            if (++index >= argc) {
                fprintf(stderr, "--window requires an integer\n");
                return 1;
            }
            window_size = atoi(argv[index++]);
            if (window_size < 0) {
                fprintf(stderr, "--window must be nonnegative\n");
                return 1;
            }
        } else if (!strcmp(argv[index], "--shard")) {
            if (index + 2 >= argc) {
                fprintf(stderr, "--shard requires I K\n");
                return 1;
            }
            shard_index = atoi(argv[index + 1]);
            shard_count = atoi(argv[index + 2]);
            index += 3;
            if (shard_count < 1 || shard_index < 0 || shard_index >= shard_count) {
                fprintf(stderr, "invalid shard I K\n");
                return 1;
            }
        } else if (!strcmp(argv[index], "--max-nodes")) {
            if (++index >= argc) {
                fprintf(stderr, "--max-nodes requires an integer\n");
                return 1;
            }
            node_cap = strtoull(argv[index++], NULL, 10);
        } else {
            fprintf(stderr, "unknown argument: %s\n", argv[index]);
            return 1;
        }
    }
    if (strcmp(mode, "AA") && strcmp(mode, "BB") && strcmp(mode, "AB") &&
        strcmp(mode, "AC") && strcmp(mode, "all")) {
        fprintf(stderr, "unknown mode: %s\n", mode);
        return 1;
    }

    double started = now_seconds();
    if (!strcmp(mode, "AA") || !strcmp(mode, "all")) run_AA();
    if (!strcmp(mode, "BB") || !strcmp(mode, "all")) run_BB();
    if (!strcmp(mode, "AB") || !strcmp(mode, "all")) run_AB();
    if (!strcmp(mode, "AC") || !strcmp(mode, "all")) run_AC();
    printf("{\"n\":%d,\"N\":%d,\"mode\":\"%s\",\"anchors_generated\":%llu,"
           "\"anchors\":%llu,\"nodes\":%llu,\"candidate_marks\":%llu,"
           "\"candidate_pairs\":%llu,\"legal_children\":%llu,"
           "\"legal_single_children\":%llu,\"legal_pair_children\":%llu,"
           "\"frontier\":%llu,\"nsol\":%llu,\"window\":%d,"
           "\"shard\":[%d,%d],"
           "\"deepest_missing_offset\":%d,\"max_noncentre_marks\":%d,"
           "\"paranoid\":%d,\"pair_mode\":\"%s\",\"introduction_mode\":\"%s\","
           "\"seconds\":%.3f,\"status\":\"%s\"}\n",
           n, N, mode,
           (unsigned long long)anchors_generated, (unsigned long long)anchors,
           (unsigned long long)nodes, (unsigned long long)candidate_marks,
           (unsigned long long)candidate_pairs, (unsigned long long)legal_children,
           (unsigned long long)legal_single_children,
           (unsigned long long)legal_pair_children, (unsigned long long)frontier,
           (unsigned long long)nsol, window_size, shard_index, shard_count,
           deepest_missing_offset, max_noncentre_marks,
           paranoid, enumerate_pairs ? "enumerated" : "one-vertex-lemma",
           diameter_intro ? "diameter-endpoints" : "all-selected",
           now_seconds() - started, capped ? "UNKNOWN" : "DONE");
    return 0;
}
