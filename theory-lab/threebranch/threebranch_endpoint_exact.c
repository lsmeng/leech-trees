#define main threebranch_general_main
#include "threebranch_exact.c"
#undef main

/*
 * Exact three-centre search seeded by the outside-band high-pole a=3,4 AC
 * endpoint subcase of the singleton-pole terminal (FW134--FW137).
 *
 * Centre 0 is the classified q-arm pole root c_A, centre 1 is the old
 * singleton centre v, and centre 2 is the endpoint pivot b.  The selected
 * diameter tips are x at centre 0 and z at centre 2.  The second b-leg tip y
 * is planted at depth k, while z has depth k+qprime with 1<=qprime<=19.
 *
 * EP3 plants the complete order-three pole
 *
 *     x depth 2s, second pole leaf depth s.
 *
 * EP4 plants the complete order-four pole
 *
 *     x depth G+s, second pole path with marks at s and G,
 *     G=2*s*r_digit, r_digit>=2.
 *
 * The endpoint DFS also enforces the two rigid pieces of the reduction: the
 * pole has no further vertices, and c_A--v is the single q-edge.  The general
 * engine is included above only for its audited metric/state primitives.
 */

static int endpoint_pivot_tip;
static int endpoint_gamma;
static int endpoint_attachment_edge;
static uint64_t band_masks;
static uint64_t band_partition_nodes;
static uint64_t band_partitions;
static uint64_t partition_cap;
static uint64_t partition_node_cap;
static uint64_t endpoint_node_offsets[64];
static uint64_t endpoint_legal_offsets[64];
static int endpoint_profile;

static int pole_digit_owns(int pole_order, int s, int G, int value);

static int endpoint_qprime_allowed(int pole_order, int qprime) {
    static const int ep3[] = {1, 2, 3, 6};
    static const int ep4[] = {1, 2, 4, 5, 8};
    const int *alphabet = pole_order == 3 ? ep3 : ep4;
    int count = pole_order == 3
        ? (int)(sizeof ep3 / sizeof ep3[0])
        : (int)(sizeof ep4 / sizeof ep4[0]);
    for (int index = 0; index < count; index++)
        if (alphabet[index] == qprime)
            return 1;
    return 0;
}

static int endpoint_mark_allowed(Mark mark) {
    if (!legal_mark(mark))
        return 0;
    if (mark.kind == 'L' && mark.centre == 0)
        return 0;  /* every pole vertex was planted before the DFS */
    if (mark.kind == 'S' && mark.x < q1)
        return 0;  /* c_A--v is the original single q-edge */
    if (mark.kind == 'S' && q1 < mark.x &&
        mark.x < q1 + endpoint_attachment_edge)
        return 0;  /* v--u is the original single t-edge */
    if (mark.kind == 'L' && mark.centre == 2) {
        int reflected = endpoint_pivot_tip - mark.x;
        /* FW108: the complete owned band below gamma was planted. */
        if (0 <= reflected && reflected < endpoint_gamma)
            return 0;
    }
    return 1;
}

static void endpoint_add_unique_candidate(
    Mark *candidates,
    int *count,
    Mark mark
) {
    if (!endpoint_mark_allowed(mark))
        return;
    for (int i = 0; i < *count; i++)
        if (compare_mark(candidates[i], mark) == 0)
            return;
    if (*count >= MAXCAND) {
        fprintf(stderr, "endpoint candidate buffer exceeded\n");
        exit(2);
    }
    candidates[(*count)++] = mark;
}

/* Diameter-endpoint introduction plus the anchored one-vertex lemma: after
   x,z are selected, a first descending occurrence of a new vertex meets one
   of those two tips.  They are marks[0] and marks[1]. */
static int endpoint_one_mark_candidates(int target, Mark *candidates) {
    int count = 0;
    for (int index = 0; index < 2; index++) {
        Mark old = marks[index];
        for (int centre = 0; centre < 3; centre++)
            for (int leg = 0; leg <= nlegs[centre]; leg++) {
                int x;
                if (old.centre == centre && old.leg == leg) {
                    endpoint_add_unique_candidate(
                        candidates, &count,
                        (Mark){'L', centre, leg, old.x - target}
                    );
                    x = old.x + target;
                } else {
                    x = target - old.x
                        - abs(centre_pos[old.centre] - centre_pos[centre]);
                }
                endpoint_add_unique_candidate(
                    candidates, &count, (Mark){'L', centre, leg, x}
                );
            }
        int delta = target - old.x;
        endpoint_add_unique_candidate(
            candidates, &count,
            (Mark){'S', -1, -1, centre_pos[old.centre] - delta}
        );
        endpoint_add_unique_candidate(
            candidates, &count,
            (Mark){'S', -1, -1, centre_pos[old.centre] + delta}
        );
    }
    return count;
}

static void endpoint_dfs(int target);

static void endpoint_try_single(int target, Mark mark) {
    candidate_marks++;
    if (!endpoint_mark_allowed(mark))
        return;
    Undo undo;
    if (!apply_mark(mark, &undo))
        return;
    if (bit(target) && branch_feasible()) {
        legal_children++;
        legal_single_children++;
        int offset = N - target;
        if (offset < 64)
            endpoint_legal_offsets[offset]++;
        endpoint_dfs(target - 1);
    }
    undo_mark(&undo);
}

static void endpoint_dfs(int target) {
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
    if (offset < 64)
        endpoint_node_offsets[offset]++;
    if (offset > deepest_missing_offset)
        deepest_missing_offset = offset;
    if (nmarks > max_noncentre_marks)
        max_noncentre_marks = nmarks;
    if (target == 0) {
        if (nmarks != n - 3) {
            fprintf(stderr,
                    "INTERNAL endpoint complete distances with %d marks\n",
                    nmarks);
            exit(2);
        }
        report_solution();
        return;
    }
    if (window_size && N - target > window_size) {
        frontier++;
        return;
    }

    Mark candidates[MAXCAND];
    int candidate_count = endpoint_one_mark_candidates(target, candidates);
    for (int i = 0; i < candidate_count; i++)
        endpoint_try_single(target, candidates[i]);
}

static void run_endpoint_anchor(
    int pole_order,
    int s,
    int G,
    int qprime,
    int k,
    int q_edge,
    int vb_core,
    int attachment_edge,
    int gamma,
    int ray_count,
    const int layer_ray[20]
) {
    if (capped)
        return;
    anchors_generated++;

    int pole_tip = pole_order == 3 ? 2 * s : G + s;
    int pole_other_tip = pole_order == 3 ? s : G;
    int pivot_tip = k + qprime;

    endpoint_pivot_tip = pivot_tip;
    endpoint_gamma = gamma;
    endpoint_attachment_edge = attachment_edge;

    int high_arm = q_edge + pole_tip;
    int mu_arm = vb_core + pivot_tip;
    int lower_height = (high_arm < mu_arm ? high_arm : mu_arm) - gamma;
    if (lower_height < 1 || lower_height >= attachment_edge ||
        attachment_edge > vb_core || attachment_edge >= q_edge)
        return;

    q1 = q_edge;
    q2 = vb_core;
    core_total = q1 + q2;
    centre_pos[0] = 0;
    centre_pos[1] = q1;
    centre_pos[2] = core_total;

    memset(fixed_count, 0, sizeof fixed_count);
    memset(fixed_caps, 0, sizeof fixed_caps);
    fixed_count[0] = 2;
    fixed_caps[0][0] = pole_tip;
    fixed_caps[0][1] = pole_other_tip;
    fixed_count[1] = 1;
    fixed_caps[1][0] = lower_height;
    fixed_count[2] = 2;
    fixed_caps[2][0] = pivot_tip;
    fixed_caps[2][1] = k;

    /* Universal caps coming only from the selected AC diameter pair. */
    fresh_caps[0] = 0;  /* the classified pole has exactly two rooted arms */
    int middle_a = q2 + pivot_tip - 1;
    int middle_b = pole_tip + q1 - 1;
    int middle_diameter_cap = middle_a < middle_b ? middle_a : middle_b;
    fresh_caps[1] = lower_height - 1 < middle_diameter_cap
        ? lower_height - 1 : middle_diameter_cap;
    int pivot_a = pivot_tip - 1;
    int pivot_b = pole_tip + core_total - 1;
    fresh_caps[2] = pivot_a < pivot_b ? pivot_a : pivot_b;
    if (fresh_caps[1] < 0 || fresh_caps[2] < 1)
        return;

    memset(nlegs, 0, sizeof nlegs);
    memset(used, 0, sizeof used);
    nmarks = 0;
    if (!add_initial_value(q1) || !add_initial_value(q2) ||
        !add_initial_value(core_total))
        return;

    /* Keep x,z first: --diameter-intro relies on marks[0:2]. */
    Undo seed_undo;
    if (!apply_mark((Mark){'L', 0, 0, pole_tip}, &seed_undo))
        return;
    if (!apply_mark((Mark){'L', 2, 0, pivot_tip}, &seed_undo))
        return;
    if (!apply_mark((Mark){'L', 2, 1, k}, &seed_undo))
        return;
    if (!apply_mark((Mark){'L', 0, 1, s}, &seed_undo))
        return;
    if (pole_order == 4 &&
        !apply_mark((Mark){'L', 0, 1, G}, &seed_undo))
        return;
    if (!apply_mark((Mark){'L', 1, 0, lower_height}, &seed_undo))
        return;
    if (attachment_edge < vb_core &&
        !apply_mark(
            (Mark){'S', -1, -1, q1 + attachment_edge}, &seed_undo))
        return;

    /* FW108 supplies every receiving-arm layer below gamma.  The topology
       partition assigns each one to a b-ray; z and y already represent
       layers zero and qprime. */
    for (int ray = 0; ray < ray_count; ray++)
    for (int reflected = 1; reflected < gamma; reflected++) {
        if (reflected == qprime || layer_ray[reflected] != ray)
            continue;
        if (!pole_digit_owns(pole_order, s, G, reflected))
            return;
        if (!apply_mark(
                (Mark){'L', 2, ray, pivot_tip - reflected}, &seed_undo))
            return;
    }

    if (!bit(N) || !branch_feasible())
        return;
    anchors++;
    endpoint_dfs(N - 1);
}

static int pole_digit_owns(int pole_order, int s, int G, int value) {
    if (pole_order == 3)
        return (value / s) % 3 == 0;
    return ((value / s) % 2 == 0) && ((value / G) % 2 == 0);
}

typedef struct {
    int pole_order;
    int s;
    int G;
    int qprime;
    int minimum_q;
    int gamma;
    int pivot_tip;
    int core_distance;
    int ray_count;
    int value_count;
    int values[20];
    int value_rays[20];
    int layer_ray[20];
    uint64_t used_local_distances[NWB];
} EndpointBand;

static int endpoint_local_add(EndpointBand *band, int value) {
    if (value < 1 || value > N ||
        ((band->used_local_distances[value >> 6] >> (value & 63)) & 1ULL))
        return 0;
    band->used_local_distances[value >> 6] |= 1ULL << (value & 63);
    return 1;
}

static int endpoint_band_seed_local(EndpointBand *band) {
    int depths[3], legs[3], count;
    if (band->pole_order == 3) {
        depths[0] = 2 * band->s; legs[0] = 0;
        depths[1] = band->s; legs[1] = 1;
        count = 2;
    } else {
        depths[0] = band->G + band->s; legs[0] = 0;
        depths[1] = band->s; legs[1] = 1;
        depths[2] = band->G; legs[2] = 1;
        count = 3;
    }
    if (!endpoint_local_add(band, band->core_distance))
        return 0;
    for (int index = 0; index < count; index++) {
        if (!endpoint_local_add(band, depths[index]) ||
            !endpoint_local_add(
                band, band->core_distance + depths[index]))
            return 0;
        for (int other = 0; other < index; other++) {
            int distance = legs[index] == legs[other]
                ? abs(depths[index] - depths[other])
                : depths[index] + depths[other];
            if (!endpoint_local_add(band, distance))
                return 0;
        }
    }
    return 1;
}

static int endpoint_band_add(EndpointBand *band, int value, int ray) {
    uint64_t local[NWB];
    memset(local, 0, sizeof local);
#define ADD_LOCAL(value_expression) do {                                        \
        int distance_ = (value_expression);                                    \
        if (distance_ < 1 || distance_ > N ||                                  \
            ((band->used_local_distances[distance_ >> 6] >>                    \
              (distance_ & 63)) & 1ULL) ||                                     \
            ((local[distance_ >> 6] >> (distance_ & 63)) & 1ULL))              \
            return 0;                                                          \
        local[distance_ >> 6] |= 1ULL << (distance_ & 63);                     \
    } while (0)

    int depth = band->pivot_tip - value;
    ADD_LOCAL(depth);                         /* b to this band vertex */
    ADD_LOCAL(band->core_distance + depth);  /* c_A to this band vertex */
    if (band->pole_order == 3) {
        ADD_LOCAL(band->core_distance + depth + 2 * band->s);
        ADD_LOCAL(band->core_distance + depth + band->s);
    } else {
        ADD_LOCAL(band->core_distance + depth + band->G + band->s);
        ADD_LOCAL(band->core_distance + depth + band->s);
        ADD_LOCAL(band->core_distance + depth + band->G);
    }
    for (int index = 0; index < band->value_count; index++) {
        int same_ray = band->value_rays[index] == ray;
        int distance = same_ray
            ? abs(value - band->values[index])
            : 2 * band->pivot_tip - value - band->values[index];
        ADD_LOCAL(distance);
    }
    for (int word = 0; word < NWB; word++)
        band->used_local_distances[word] |= local[word];
#undef ADD_LOCAL
    band->values[band->value_count] = value;
    band->value_rays[band->value_count] = ray;
    band->value_count++;
    band->layer_ray[value] = ray;
    return 1;
}

static void endpoint_band_search(EndpointBand band, int next_value) {
    if (partition_node_cap && band_partition_nodes >= partition_node_cap) {
        capped = 1;
        return;
    }
    band_partition_nodes++;
    while (next_value > band.qprime &&
           !pole_digit_owns(band.pole_order, band.s, band.G, next_value))
        next_value--;
    if (next_value <= band.qprime) {
        int pole_marks = band.pole_order == 3 ? 2 : 3;
        if (band.value_count + pole_marks + 1 > n - 3)
            return;
        if (partition_cap && band_partitions >= partition_cap) {
            capped = 1;
            return;
        }
        uint64_t partition_ordinal = band_partitions++;
        int k = band.pivot_tip - band.qprime;
        for (int q_edge = band.minimum_q;
             q_edge < band.core_distance && !capped; q_edge++) {
            int vb_core = band.core_distance - q_edge;
            int pivot_diameter = 2 * k + band.qprime;
            if (pivot_diameter >= q_edge || pivot_diameter >= vb_core)
                continue;
            int maximum_t = q_edge - 1 < vb_core
                ? q_edge - 1 : vb_core;
            for (int attachment_edge = pivot_diameter + 1;
                 attachment_edge <= maximum_t && !capped;
                 attachment_edge++) {
                uint64_t shard_key = partition_ordinal * 0x9e3779b97f4a7c15ULL;
                shard_key ^= (uint64_t)q_edge * 0xbf58476d1ce4e5b9ULL;
                shard_key ^= (uint64_t)attachment_edge * 0x94d049bb133111ebULL;
                if (shard_count && shard_key % (uint64_t)shard_count !=
                    (uint64_t)shard_index)
                    continue;
                run_endpoint_anchor(
                    band.pole_order,
                    band.s,
                    band.G,
                    band.qprime,
                    k,
                    q_edge,
                    vb_core,
                    attachment_edge,
                    band.gamma,
                    band.ray_count,
                    band.layer_ray
                );
            }
        }
        return;
    }

    for (int ray = 0; ray <= band.ray_count; ray++) {
        EndpointBand child = band;
        if (!endpoint_band_add(&child, next_value, ray))
            continue;
        if (ray == child.ray_count)
            child.ray_count++;
        endpoint_band_search(child, next_value - 1);
    }
}

static void enumerate_endpoint_bands(
    int pole_order,
    int s,
    int G,
    int qprime,
    int minimum_q
) {
    int gamma_cap = pole_order == 3 ? 13 : 20;
    for (int gamma = qprime + 1;
         gamma <= gamma_cap && !capped;
         gamma++) {
        band_masks++;
        int pole_tip = pole_order == 3 ? 2 * s : G + s;
        for (int k = qprime + 1; !capped; k++) {
            int endpoint_r = N - 2 * k - qprime;
            if (endpoint_r < 1)
                break;
            if (endpoint_r < n - 1 || endpoint_r == qprime)
                continue;
            int pivot_tip = k + qprime;
            /* FW130--FW131: the unique B-branch b is outside S_gamma. */
            if (pivot_tip < gamma)
                continue;
            int core_distance = N - pole_tip - pivot_tip;
            if (core_distance <= minimum_q)
                continue;

            EndpointBand band;
            memset(&band, 0, sizeof band);
            band.pole_order = pole_order;
            band.s = s;
            band.G = G;
            band.qprime = qprime;
            band.minimum_q = minimum_q;
            band.gamma = gamma;
            band.pivot_tip = pivot_tip;
            band.core_distance = core_distance;
            band.ray_count = 2;
            for (int value = 0; value < 20; value++)
                band.layer_ray[value] = -1;
            int fixed_ok = endpoint_band_seed_local(&band);
            for (int value = 0; value <= qprime && fixed_ok; value++) {
                if (!pole_digit_owns(pole_order, s, G, value))
                    continue;
                int ray = value < qprime ? 0 : 1;
                if (!endpoint_band_add(&band, value, ray))
                    fixed_ok = 0;
            }
            if (fixed_ok)
                endpoint_band_search(band, gamma - 1);
        }
    }
}

static void run_endpoint_order(int pole_order) {
    active_mode = pole_order == 3 ? "EP3" : "EP4";
    for (int s = 1; !capped; s++) {
        /* pole tip + least q-edge + least pivot tip + least v--b core */
        int minimum_pole_mass = pole_order == 3
            ? 5 * s + 5
            : 14 * s + 5;  /* G=4s, lambda=5s, q>=9s+1 */
        if (minimum_pole_mass > N)
            break;

        int digit_start = 2;
        int digit_end = pole_order == 3 ? 3 : N;
        for (int r_digit = digit_start; r_digit < digit_end && !capped; r_digit++) {
            int G = pole_order == 3 ? 0 : 2 * s * r_digit;
            int pole_tip = pole_order == 3 ? 2 * s : G + s;
            int minimum_q = pole_order == 3 ? 3 * s + 1 : 2 * G + s + 1;
            if (pole_order == 4 && pole_tip + minimum_q + 4 > N)
                break;

            /* EP3 has no higher digit parameter. */
            if (pole_order == 3 && r_digit > digit_start)
                break;

            for (int qprime = 1; qprime <= 19 && !capped; qprime++) {
                if (!endpoint_qprime_allowed(pole_order, qprime))
                    continue;
                if (!pole_digit_owns(pole_order, s, G, qprime))
                    continue;
                enumerate_endpoint_bands(
                    pole_order, s, G, qprime, minimum_q
                );
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr,
                "usage: %s n [EP3|EP4|all] [--fast] [--no-pairs] "
                "[--diameter-intro] [--window W] [--shard I K] "
                "[--max-nodes K] [--max-partitions K] "
                "[--max-partition-nodes K] [--profile]\n", argv[0]);
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
            if (shard_count < 1 || shard_index < 0 ||
                shard_index >= shard_count) {
                fprintf(stderr, "invalid shard I K\n");
                return 1;
            }
        } else if (!strcmp(argv[index], "--max-nodes")) {
            if (++index >= argc) {
                fprintf(stderr, "--max-nodes requires an integer\n");
                return 1;
            }
            node_cap = strtoull(argv[index++], NULL, 10);
        } else if (!strcmp(argv[index], "--max-partitions")) {
            if (++index >= argc) {
                fprintf(stderr, "--max-partitions requires an integer\n");
                return 1;
            }
            partition_cap = strtoull(argv[index++], NULL, 10);
        } else if (!strcmp(argv[index], "--max-partition-nodes")) {
            if (++index >= argc) {
                fprintf(stderr, "--max-partition-nodes requires an integer\n");
                return 1;
            }
            partition_node_cap = strtoull(argv[index++], NULL, 10);
        } else if (!strcmp(argv[index], "--profile")) {
            endpoint_profile = 1;
            index++;
        } else {
            fprintf(stderr, "unknown argument: %s\n", argv[index]);
            return 1;
        }
    }
    if (strcmp(mode, "EP3") && strcmp(mode, "EP4") && strcmp(mode, "all")) {
        fprintf(stderr, "unknown mode: %s\n", mode);
        return 1;
    }

    /* Both restrictions are proved theorems, not optional heuristics here. */
    enumerate_pairs = 0;
    diameter_intro = 1;

    double started = now_seconds();
    if (!strcmp(mode, "EP3") || !strcmp(mode, "all"))
        run_endpoint_order(3);
    if (!strcmp(mode, "EP4") || !strcmp(mode, "all"))
        run_endpoint_order(4);
    printf("{\"n\":%d,\"N\":%d,\"mode\":\"%s\",\"anchors_generated\":%llu,"
           "\"anchors\":%llu,\"nodes\":%llu,\"candidate_marks\":%llu,"
           "\"candidate_pairs\":%llu,\"legal_children\":%llu,"
           "\"legal_single_children\":%llu,\"legal_pair_children\":%llu,"
           "\"frontier\":%llu,\"nsol\":%llu,\"window\":%d,"
           "\"shard\":[%d,%d],\"deepest_missing_offset\":%d,"
           "\"max_noncentre_marks\":%d,\"paranoid\":%d,"
           "\"band_masks\":%llu,\"band_partition_nodes\":%llu,"
           "\"band_partitions\":%llu,"
           "\"pair_mode\":\"%s\",\"introduction_mode\":\"%s\","
           "\"seconds\":%.3f,\"status\":\"%s\"}\n",
           n, N, mode,
           (unsigned long long)anchors_generated,
           (unsigned long long)anchors,
           (unsigned long long)nodes,
           (unsigned long long)candidate_marks,
           (unsigned long long)candidate_pairs,
           (unsigned long long)legal_children,
           (unsigned long long)legal_single_children,
           (unsigned long long)legal_pair_children,
           (unsigned long long)frontier,
           (unsigned long long)nsol,
           window_size, shard_index, shard_count,
           deepest_missing_offset, max_noncentre_marks,
           paranoid,
           (unsigned long long)band_masks,
           (unsigned long long)band_partition_nodes,
           (unsigned long long)band_partitions,
           enumerate_pairs ? "enumerated" : "one-vertex-lemma",
           diameter_intro ? "diameter-endpoints" : "all-selected",
           now_seconds() - started,
           capped ? "UNKNOWN" : "DONE");
    if (endpoint_profile) {
        fprintf(stderr, "endpoint-offset-profile");
        for (int offset = 0; offset < 64; offset++)
            if (endpoint_node_offsets[offset] || endpoint_legal_offsets[offset])
                fprintf(stderr, " %d:%llu/%llu", offset,
                        (unsigned long long)endpoint_node_offsets[offset],
                        (unsigned long long)endpoint_legal_offsets[offset]);
        fprintf(stderr, "\n");
    }
    return 0;
}
