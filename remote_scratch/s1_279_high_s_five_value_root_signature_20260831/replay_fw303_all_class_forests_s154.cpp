#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using i64 = std::int64_t;

static const std::array<int, 6> W = {4, 5, 16, 18, 19, 20};
static const std::array<std::string, 6> NAMES = {"z", "b1", "b2", "c", "d6", "a"};

struct Signature {
    std::string raw;
    int s = 0;
    std::string shape;
    int d1 = 0;
    int d2 = 0;
    std::array<int, 21> selected{};
};

struct RowSpec {
    int gate = -1;
    int q = 0;
    char cls = '?';
};

struct Descriptor {
    bool compatible = false;
    char cls = '?';
    int gate = -1;
    int q = 0;
    std::array<int, 21> fixed_parent{};
    std::array<int, 21> forced_color{};
    std::vector<int> possible_c;
};

struct Counters {
    i64 root_sets = 0;
    i64 root_colorings = 0;
    i64 root_edge_legal = 0;
    i64 capacity_rejects = 0;
    i64 weight_assignments = 0;
    i64 parent_legal = 0;
    i64 spectrum_survivors = 0;
};

static std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string part;
    while (std::getline(ss, part, delim)) out.push_back(part);
    return out;
}

static std::vector<int> parse_group(const std::string &s) {
    std::vector<int> out;
    if (s.empty()) return out;
    for (const auto &part : split(s, ',')) out.push_back(std::stoi(part));
    return out;
}

static Signature parse_signature(const std::string &raw) {
    auto parts = split(raw, '|');
    if (parts.size() < 7) throw std::runtime_error("bad signature");
    Signature sig;
    sig.raw = raw;
    sig.s = std::stoi(parts[0]);
    sig.shape = parts[1];
    sig.d1 = std::stoi(parts[2]);
    sig.d2 = std::stoi(parts[3]);
    sig.selected.fill(-1);
    int count = 0;
    for (int color = 0; color < 3; ++color) {
        for (int y : parse_group(parts[4 + color])) {
            if (y < 0 || y > 20 || sig.selected[y] != -1) {
                throw std::runtime_error("bad selected root");
            }
            sig.selected[y] = color;
            ++count;
        }
    }
    if (count != 10) throw std::runtime_error("signature is not exact-10");
    return sig;
}

static std::vector<Signature> read_signatures(const std::string &path) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("cannot open signature input");
    std::string text((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    const std::string key = "\"canonical_root_signatures\"";
    auto key_pos = text.find(key);
    if (key_pos == std::string::npos) throw std::runtime_error("signature key missing");
    auto begin = text.find('[', key_pos + key.size());
    auto end = text.find(']', begin);
    if (begin == std::string::npos || end == std::string::npos) {
        throw std::runtime_error("malformed signature array");
    }
    std::vector<Signature> out;
    std::size_t pos = begin + 1;
    while (pos < end) {
        auto first = text.find('"', pos);
        if (first == std::string::npos || first >= end) break;
        auto last = text.find('"', first + 1);
        if (last == std::string::npos || last > end) {
            throw std::runtime_error("unterminated signature string");
        }
        std::string raw = text.substr(first + 1, last - first - 1);
        if (raw.find('|') == std::string::npos) throw std::runtime_error("bad signature entry");
        out.push_back(parse_signature(raw));
        pos = last + 1;
    }
    if (out.empty()) throw std::runtime_error("no canonical signatures parsed");
    return out;
}

static int vertex_id(const std::string &name) {
    for (int i = 0; i < 6; ++i) if (NAMES[i] == name) return i;
    throw std::runtime_error("unknown core vertex");
}

static std::array<std::vector<std::pair<int, int>>, 6> core_adj() {
    std::array<std::vector<std::pair<int, int>>, 6> adj;
    const std::array<std::tuple<const char *, const char *, int>, 5> edges = {{
        {"z", "b1", 1}, {"z", "b2", 2}, {"c", "d6", 6},
        {"c", "z", 7}, {"z", "a", 10}
    }};
    for (const auto &[a_name, b_name, w] : edges) {
        int a = vertex_id(a_name), b = vertex_id(b_name);
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    return adj;
}

static std::vector<RowSpec> all_rows() {
    std::vector<RowSpec> out;
    auto add_range = [&](const char *gate, int lo, int hi, char cls) {
        for (int q = lo; q <= hi; ++q) out.push_back({vertex_id(gate), q, cls});
    };
    add_range("z", 13, 20, 'A');
    add_range("b1", 14, 20, 'A');
    add_range("b2", 15, 20, 'A');
    add_range("c", 17, 20, 'A');
    out.push_back({vertex_id("b2"), 22, 'B'});
    for (int q : {22, 24, 26}) out.push_back({vertex_id("c"), q, 'C'});
    for (int q : {24, 26, 28, 30}) out.push_back({vertex_id("a"), q, 'B'});
    for (int q : {24, 26}) out.push_back({vertex_id("d6"), q, 'B'});
    for (int q : {28, 30, 32}) out.push_back({vertex_id("d6"), q, 'C'});
    if (out.size() != 38) throw std::runtime_error("row catalogue is not 38");
    return out;
}

static Descriptor assess(const Signature &sig, const RowSpec &spec) {
    const auto adj = core_adj();
    std::array<int, 6> offset, parent_vertex;
    offset.fill(-1);
    parent_vertex.fill(-1);
    offset[spec.gate] = 0;
    std::queue<int> qv;
    qv.push(spec.gate);
    while (!qv.empty()) {
        int v = qv.front(); qv.pop();
        for (auto [u, w] : adj[v]) {
            if (offset[u] != -1) continue;
            offset[u] = offset[v] + w;
            parent_vertex[u] = v;
            qv.push(u);
        }
    }

    Descriptor d;
    d.cls = spec.cls;
    d.gate = spec.gate;
    d.q = spec.q;
    d.fixed_parent.fill(-1);
    d.forced_color.fill(-1);
    const int B = 280 - sig.s;
    const int A = B + 20;
    const int t = A - spec.q;
    std::array<int, 6> kind, ident; // kind 1=HIGH, 0=LOW
    for (int v = 0; v < 6; ++v) {
        int depth = t + offset[v];
        if (B <= depth && depth <= A) {
            kind[v] = 1;
            ident[v] = depth - B;
        } else if (depth == 0) {
            kind[v] = 0; ident[v] = 0;
        } else if (depth == sig.d1) {
            kind[v] = 0; ident[v] = 1;
        } else if (depth == sig.d2) {
            kind[v] = 0; ident[v] = 2;
        } else {
            return d;
        }
    }

    int f_c = 0;
    for (int child = 0; child < 6; ++child) {
        int par = parent_vertex[child];
        if (par == -1) continue;
        if (kind[child] == 0) {
            if (kind[par] != 0) throw std::runtime_error("core depth decreased");
            continue; // low-low core edge is already a chain edge
        }
        int y = ident[child];
        if (kind[par] == 1) {
            d.fixed_parent[y] = ident[par];
            ++f_c;
        } else {
            d.forced_color[y] = ident[par];
        }
    }
    int expected = spec.cls == 'A' ? 5 : (spec.cls == 'B' ? 4 : 3);
    if (f_c != expected) throw std::runtime_error("row class/f_C mismatch");
    for (int y = 0; y < 21; ++y) {
        if (d.fixed_parent[y] != -1 && sig.selected[y] != -1) return d;
        if (d.forced_color[y] != -1 && sig.selected[y] != -1 &&
            d.forced_color[y] != sig.selected[y]) return d;
    }
    int missing_forced = 0;
    for (int y = 0; y < 21; ++y) {
        if (d.forced_color[y] != -1 && sig.selected[y] == -1) ++missing_forced;
    }
    int min_c = spec.cls == 'A' ? 10 : (spec.cls == 'B' ? 11 : 12);
    // s=154 chain admits c=14; include the endpoint in the exact forest domain.
    for (int c = min_c; c <= 14; ++c) {
        if (c - 10 >= missing_forced) d.possible_c.push_back(c);
    }
    if (d.possible_c.empty()) return d;
    d.compatible = true;
    return d;
}

static int attachment_weight(const Signature &sig, int y, int color) {
    const int B = 280 - sig.s;
    const std::array<int, 3> low_depth = {0, sig.d1, sig.d2};
    return B + y - low_depth[color];
}

static std::vector<int> distance_multiset(
    const Signature &sig,
    const std::array<int, 21> &root_color,
    const std::array<int, 21> &parent
) {
    std::array<std::vector<std::pair<int, int>>, 24> adj;
    auto add = [&](int a, int b, int w) {
        if (w <= 0) throw std::runtime_error("nonpositive edge");
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    };
    add(0, 1, sig.d1);
    add(1, 2, sig.d2 - sig.d1);
    for (int y = 0; y < 21; ++y) {
        if (root_color[y] != -1) {
            add(root_color[y], 3 + y, attachment_weight(sig, y, root_color[y]));
        } else {
            if (parent[y] < 0) throw std::runtime_error("missing high parent");
            add(3 + parent[y], 3 + y, y - parent[y]);
        }
    }
    std::vector<int> out;
    out.reserve(276);
    for (int src = 0; src < 24; ++src) {
        std::array<int, 24> dist;
        dist.fill(-1);
        dist[src] = 0;
        std::vector<int> stack = {src};
        while (!stack.empty()) {
            int v = stack.back(); stack.pop_back();
            for (auto [u, w] : adj[v]) {
                if (dist[u] != -1) continue;
                dist[u] = dist[v] + w;
                stack.push_back(u);
            }
        }
        for (int v = src + 1; v < 24; ++v) {
            if (dist[v] < 0) throw std::runtime_error("disconnected tree");
            out.push_back(dist[v]);
        }
    }
    std::sort(out.begin(), out.end());
    return out;
}

static std::vector<std::vector<int>> combinations(const std::vector<int> &items, int k) {
    std::vector<std::vector<int>> out;
    std::vector<int> cur;
    std::function<void(int, int)> rec = [&](int pos, int need) {
        if (need == 0) { out.push_back(cur); return; }
        if ((int)items.size() - pos < need) return;
        for (int i = pos; i <= (int)items.size() - need; ++i) {
            cur.push_back(items[i]);
            rec(i + 1, need - 1);
            cur.pop_back();
        }
    };
    if (k >= 0) rec(0, k);
    return out;
}

static Counters search(const Signature &sig, const Descriptor &d, int c) {
    Counters ctr;
    std::array<int, 21> base_roots = sig.selected;
    int f_c = 0;
    for (int y = 0; y < 21; ++y) {
        if (d.fixed_parent[y] != -1) ++f_c;
        if (d.forced_color[y] != -1) {
            if (base_roots[y] != -1 && base_roots[y] != d.forced_color[y]) {
                throw std::runtime_error("forced root color mismatch");
            }
            base_roots[y] = d.forced_color[y];
        }
    }
    int base_root_count = std::count_if(base_roots.begin(), base_roots.end(), [](int x){return x != -1;});
    int free_count = c - base_root_count;
    int e = 21 - c - f_c;
    if (free_count < 0 || e < 0) return ctr;
    std::vector<int> eligible;
    for (int y = 0; y < 21; ++y) {
        if (base_roots[y] == -1 && d.fixed_parent[y] == -1) eligible.push_back(y);
    }
    auto root_subsets = combinations(eligible, free_count);
    std::vector<int> target;
    for (int v = 1; v < 280; ++v) {
        if (v != sig.s && v != sig.s + sig.d1 && v != sig.s + sig.d2) target.push_back(v);
    }
    for (const auto &free_roots : root_subsets) {
        ++ctr.root_sets;
        int colorings = 1;
        for (int i = 0; i < free_count; ++i) colorings *= 3;
        for (int code = 0; code < colorings; ++code) {
            ++ctr.root_colorings;
            auto roots = base_roots;
            int x = code;
            for (int y : free_roots) { roots[y] = x % 3; x /= 3; }
            std::vector<int> edge_weights = {sig.d1, sig.d2 - sig.d1};
            for (int y = 0; y < 21; ++y) {
                if (d.fixed_parent[y] != -1) edge_weights.push_back(y - d.fixed_parent[y]);
            }
            for (int y = 0; y < 21; ++y) {
                if (roots[y] != -1) edge_weights.push_back(attachment_weight(sig, y, roots[y]));
            }
            bool legal_edges = true;
            std::set<int> used;
            for (int w : edge_weights) {
                if (!(0 < w && w < sig.s) || !used.insert(w).second) {
                    legal_edges = false; break;
                }
            }
            if (!legal_edges) continue;
            ++ctr.root_edge_legal;
            std::vector<int> children;
            for (int y = 0; y < 21; ++y) {
                if (roots[y] == -1 && d.fixed_parent[y] == -1) children.push_back(y);
            }
            if ((int)children.size() != e) throw std::runtime_error("high-edge ledger mismatch");
            std::vector<int> available;
            for (int w : W) if (!used.count(w)) available.push_back(w);
            if ((int)available.size() < e) { ++ctr.capacity_rejects; continue; }

            std::vector<int> chosen;
            std::vector<bool> taken(available.size(), false);
            std::function<void()> assign = [&]() {
                if ((int)chosen.size() == e) {
                    ++ctr.weight_assignments;
                    auto parent = d.fixed_parent;
                    for (int i = 0; i < e; ++i) {
                        int p = children[i] - chosen[i];
                        if (p < 0) return;
                        parent[children[i]] = p;
                    }
                    ++ctr.parent_legal;
                    if (distance_multiset(sig, roots, parent) == target) {
                        ++ctr.spectrum_survivors;
                    }
                    return;
                }
                for (int i = 0; i < (int)available.size(); ++i) {
                    if (taken[i]) continue;
                    taken[i] = true;
                    chosen.push_back(available[i]);
                    assign();
                    chosen.pop_back();
                    taken[i] = false;
                }
            };
            assign();
        }
    }
    return ctr;
}

int main(int argc, char **argv) {
    if (argc != 4) {
        std::cerr << "usage: replay INPUT.json JOBS.tsv SUMMARY.json\n";
        return 2;
    }
    try {
        auto signatures = read_signatures(argv[1]);
        auto rows = all_rows();
#ifndef ALLOW_MIXED_D1
        const int expected_d1 = signatures.front().d1;
        if (expected_d1 <= 0 || (expected_d1 & 1)) {
            throw std::runtime_error("unexpected replay d1");
        }
#endif
        std::ofstream jobs(argv[2]);
        if (!jobs) throw std::runtime_error("cannot open jobs output");
        jobs << "signature_index\tgate\tq\tclass\tc\troot_sets\troot_colorings\troot_edge_legal\tcapacity_rejects\tweight_assignments\tparent_legal\tspectrum_survivors\n";
        i64 gate_rows_tested = 0, compatible = 0, row_c_jobs = 0, total_survivors = 0;
        std::map<char, i64> by_class = {{'A', 0}, {'B', 0}, {'C', 0}};
        Counters totals;
        for (int si = 0; si < (int)signatures.size(); ++si) {
            const auto &sig = signatures[si];
            if (sig.s != 154 || sig.shape != "chain"
#ifndef ALLOW_MIXED_D1
                || sig.d1 != expected_d1
#else
                || sig.d1 <= 0 || (sig.d1 & 1) || sig.d2 <= sig.d1 || sig.d2 >= 126
#endif
            ) {
                throw std::runtime_error("unexpected replay scope");
            }
            for (const auto &spec : rows) {
                ++gate_rows_tested;
                auto d = assess(sig, spec);
                if (!d.compatible) continue;
                ++compatible;
                ++by_class[d.cls];
                for (int c : d.possible_c) {
                    ++row_c_jobs;
                    auto x = search(sig, d, c);
                    totals.root_sets += x.root_sets;
                    totals.root_colorings += x.root_colorings;
                    totals.root_edge_legal += x.root_edge_legal;
                    totals.capacity_rejects += x.capacity_rejects;
                    totals.weight_assignments += x.weight_assignments;
                    totals.parent_legal += x.parent_legal;
                    totals.spectrum_survivors += x.spectrum_survivors;
                    total_survivors += x.spectrum_survivors;
                    jobs << si << '\t' << NAMES[d.gate] << '\t' << d.q << '\t' << d.cls << '\t' << c
                         << '\t' << x.root_sets << '\t' << x.root_colorings << '\t' << x.root_edge_legal
                         << '\t' << x.capacity_rejects << '\t' << x.weight_assignments
                         << '\t' << x.parent_legal << '\t' << x.spectrum_survivors << '\n';
                }
            }
        }
        jobs.close();
        std::ofstream summary(argv[3]);
        if (!summary) throw std::runtime_error("cannot open summary output");
        summary << "{\n"
                << "  \"status\": \"INDEPENDENT_FW303_ALL_CLASS_REPLAY\",\n"
#ifndef ALLOW_MIXED_D1
                << "  \"d1\": " << expected_d1 << ",\n"
#else
                << "  \"d1_min\": 2,\n"
                << "  \"d1_max\": 124,\n"
#endif
                << "  \"signatures\": " << signatures.size() << ",\n"
                << "  \"gate_rows_per_signature\": 38,\n"
                << "  \"gate_rows_tested\": " << gate_rows_tested << ",\n"
                << "  \"compatible_rows\": " << compatible << ",\n"
                << "  \"compatible_A\": " << by_class['A'] << ",\n"
                << "  \"compatible_B\": " << by_class['B'] << ",\n"
                << "  \"compatible_C\": " << by_class['C'] << ",\n"
                << "  \"row_c_jobs\": " << row_c_jobs << ",\n"
                << "  \"root_sets\": " << totals.root_sets << ",\n"
                << "  \"root_colorings\": " << totals.root_colorings << ",\n"
                << "  \"root_edge_legal\": " << totals.root_edge_legal << ",\n"
                << "  \"capacity_rejects\": " << totals.capacity_rejects << ",\n"
                << "  \"weight_assignments\": " << totals.weight_assignments << ",\n"
                << "  \"parent_legal\": " << totals.parent_legal << ",\n"
                << "  \"full_spectrum_survivors\": " << total_survivors << "\n"
                << "}\n";
        return 0;
    } catch (const std::exception &e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
