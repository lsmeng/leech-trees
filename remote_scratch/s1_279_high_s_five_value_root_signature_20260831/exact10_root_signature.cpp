#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int MAXV = 279;
constexpr int YMAX = 20;
constexpr int ROOTS = 10;

enum class Shape { Star, Chain };

struct Root {
    int y;
    int color;
};

uint64_t fnv1a64(const std::string& s) {
    uint64_t h = 1469598103934665603ULL;
    for (unsigned char ch : s) {
        h ^= static_cast<uint64_t>(ch);
        h *= 1099511628211ULL;
    }
    return h;
}

std::string hex64(uint64_t x) {
    std::ostringstream out;
    out << std::hex << std::setw(16) << std::setfill('0') << x;
    return out.str();
}

std::string shape_name(Shape s) {
    return s == Shape::Star ? "star" : "chain";
}

Shape parse_shape(const std::string& s) {
    if (s == "star") return Shape::Star;
    if (s == "chain") return Shape::Chain;
    throw std::runtime_error("shape must be star or chain");
}

bool allowed_s(int s) {
    return s == 152 || s == 154 || s == 156 || s == 158 || s == 160;
}

struct Search {
    int s;
    int B;
    Shape shape;
    int only_d1;
    int d1 = 0;
    int d2 = 0;

    std::bitset<MAXV + 1> owner;
    std::array<unsigned, YMAX + 1> local_color_mask{};
    std::vector<Root> roots;

    uint64_t params_total = 0;
    uint64_t params_valid = 0;
    uint64_t params_with_survivor = 0;
    uint64_t dfs_calls = 0;
    uint64_t candidate_attempts = 0;
    uint64_t survivor_count = 0;
    uint64_t survivor_xor = 0;
    uint64_t survivor_sum = 0;

    std::map<std::tuple<int,int,int>, uint64_t> color_counts;
    std::vector<std::string> examples;
    size_t max_examples = 50;

    Search(int s_, Shape sh, int only_d1_)
        : s(s_), B(280 - s_), shape(sh), only_d1(only_d1_) {}

    bool is_hole(int v) const {
        return v == s || v == s + d1 || v == s + d2;
    }

    bool pair_value_allowed(int v) const {
        return 1 <= v && v <= MAXV && !is_hole(v);
    }

    int low_parent_depth(int color) const {
        if (color == 0) return 0;
        if (color == 1) return d1;
        if (color == 2) return d2;
        throw std::runtime_error("bad color");
    }

    int lca_depth(int c1, int c2) const {
        if (shape == Shape::Star) {
            if (c1 == 1 && c2 == 1) return d1;
            if (c1 == 2 && c2 == 2) return d2;
            return 0;
        }
        if (c1 == 0 || c2 == 0) return 0;
        if (c1 == 2 && c2 == 2) return d2;
        return d1;
    }

    bool add_background_value(int v) {
        if (!pair_value_allowed(v) || owner.test(v)) return false;
        owner.set(v);
        return true;
    }

    bool setup_parameter(int a, int b) {
        d1 = a;
        d2 = b;
        owner.reset();

        if (!(0 < d1 && d1 < d2 && d2 < B)) return false;
        if ((d1 & 1) || (d2 & 1)) return false;

        int lowlow = 0;
        if (shape == Shape::Star) {
            if (!(d1 < s && d2 < s)) return false;
            lowlow = d1 + d2;
        } else {
            int g = d2 - d1;
            if (!(d1 < s && g < s)) return false;
            if (d1 == g) return false;
            lowlow = g;
        }

        if (!add_background_value(d1)) return false;
        if (!add_background_value(d2)) return false;
        for (int y = 0; y <= YMAX; ++y)
            if (!add_background_value(B + y)) return false;
        if (!add_background_value(lowlow)) return false;

        for (int y = 0; y <= YMAX; ++y) {
            unsigned mask = 0;
            for (int c = 0; c < 3; ++c) {
                int att = B + y - low_parent_depth(c);
                if (!(0 < att && att < s)) continue;
                if (c == 0) {
                    if (att == B + y && owner.test(att)) mask |= 1u;
                } else if (pair_value_allowed(att) && !owner.test(att)) {
                    mask |= (1u << c);
                }
            }
            local_color_mask[y] = mask;
        }
        return true;
    }

    bool propose_new_owner(int v, const std::vector<int>& pending) const {
        if (!pair_value_allowed(v) || owner.test(v)) return false;
        return std::find(pending.begin(), pending.end(), v) == pending.end();
    }

    bool try_add_root(int y, int color, std::vector<int>& added) {
        ++candidate_attempts;
        if ((local_color_mask[y] & (1u << color)) == 0) return false;

        std::vector<int> pending;
        int att = B + y - low_parent_depth(color);
        if (!(0 < att && att < s)) return false;
        if (color == 0) {
            if (att != B + y || !owner.test(att)) return false;
        } else {
            if (!propose_new_owner(att, pending)) return false;
            pending.push_back(att);
        }

        // Compare actual tree distances, never raw y-sums across LCA classes.
        for (const Root& r : roots) {
            int ell = lca_depth(color, r.color);
            int dist = 2 * B + y + r.y - 2 * ell;
            if (!propose_new_owner(dist, pending)) return false;
            pending.push_back(dist);
        }

        for (int v : pending) owner.set(v);
        added.swap(pending);
        return true;
    }

    void undo_added(const std::vector<int>& added) {
        for (int v : added) owner.reset(v);
    }

    std::string canonical_signature() const {
        std::array<std::vector<int>, 3> ys;
        for (const Root& r : roots) ys[r.color].push_back(r.y);
        std::ostringstream out;
        out << s << '|' << shape_name(shape) << '|' << d1 << '|' << d2;
        for (int c = 0; c < 3; ++c) {
            out << '|';
            for (size_t i = 0; i < ys[c].size(); ++i) {
                if (i) out << ',';
                out << ys[c][i];
            }
        }
        return out.str();
    }

    void record_survivor() {
        ++survivor_count;
        int n[3] = {0,0,0};
        for (const Root& r : roots) ++n[r.color];
        color_counts[{n[0],n[1],n[2]}]++;
        std::string sig = canonical_signature();
        uint64_t h = fnv1a64(sig);
        survivor_xor ^= h;
        survivor_sum += h;
        if (examples.size() < max_examples) examples.push_back(sig);
    }

    int locally_available_positions(int start) const {
        int count = 0;
        for (int y = start; y <= YMAX; ++y)
            if (local_color_mask[y]) ++count;
        return count;
    }

    void dfs(int start_y, int need) {
        ++dfs_calls;
        if (need == 0) { record_survivor(); return; }
        if (start_y > YMAX || YMAX - start_y + 1 < need) return;
        if (locally_available_positions(start_y) < need) return;

        int last_y = YMAX - need + 1;
        for (int y = start_y; y <= last_y; ++y) {
            unsigned mask = local_color_mask[y];
            if (!mask) continue;
            for (int color = 0; color < 3; ++color) {
                if ((mask & (1u << color)) == 0) continue;
                std::vector<int> added;
                if (!try_add_root(y, color, added)) continue;
                roots.push_back({y,color});
                dfs(y + 1, need - 1);
                roots.pop_back();
                undo_added(added);
            }
        }
    }

    void run() {
        for (int a = 2; a < B; a += 2) {
            if (only_d1 >= 0 && a != only_d1) continue;
            for (int b = a + 2; b < B; b += 2) {
                ++params_total;
                if (!setup_parameter(a, b)) continue;
                ++params_valid;
                uint64_t before = survivor_count;
                roots.clear();
                dfs(0, ROOTS);
                if (survivor_count != before) ++params_with_survivor;
            }
        }
    }

    void print_json() const {
        std::string input_tag =
            "S1-279-HIGH-S-EXACT10-ROOT-SUBSYSTEM-v2"
            "|s=" + std::to_string(s) +
            "|shape=" + shape_name(shape) +
            "|d1=" + (only_d1 < 0 ? std::string("all") : std::to_string(only_d1)) +
            "|d1,d2=even,0<d1<d2<B"
            "|background=Dminus0+lowlow"
            "|newowners=color1or2-attachments+all-rootroot"
            "|color0-attachment=same-owner-exception"
            "|exact-roots=10|actual-distance-comparison=yes";

        std::cout << "{\n"
                  << "  \"status\":\"EXACT10_ROOT_SUBSYSTEM_EXHAUSTED\",\n"
                  << "  \"s\":" << s << ",\n"
                  << "  \"B\":" << B << ",\n"
                  << "  \"shape\":\"" << shape_name(shape) << "\",\n"
                  << "  \"d1_shard\":" << only_d1 << ",\n"
                  << "  \"input_tag\":\"" << input_tag << "\",\n"
                  << "  \"input_tag_fnv1a64\":\"" << hex64(fnv1a64(input_tag)) << "\",\n"
                  << "  \"params_total\":" << params_total << ",\n"
                  << "  \"params_valid\":" << params_valid << ",\n"
                  << "  \"params_with_survivor\":" << params_with_survivor << ",\n"
                  << "  \"dfs_calls\":" << dfs_calls << ",\n"
                  << "  \"candidate_attempts\":" << candidate_attempts << ",\n"
                  << "  \"survivor_count\":" << survivor_count << ",\n"
                  << "  \"survivor_xor_fnv1a64\":\"" << hex64(survivor_xor) << "\",\n"
                  << "  \"survivor_sum_fnv1a64\":\"" << hex64(survivor_sum) << "\",\n"
                  << "  \"color_count_histogram\":{";
        bool first = true;
        for (const auto& kv : color_counts) {
            if (!first) std::cout << ',';
            first = false;
            auto [n0,n1,n2] = kv.first;
            std::cout << '\"' << n0 << ',' << n1 << ',' << n2 << "\":" << kv.second;
        }
        std::cout << "},\n  \"first_examples\":[";
        for (size_t i = 0; i < examples.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << '\"' << examples[i] << '\"';
        }
        std::cout << "]\n}\n";
    }
};

} // namespace

int main(int argc, char** argv) {
    try {
        int s = -1;
        int only_d1 = -1;
        std::string shape_s;
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--s" && i + 1 < argc) s = std::stoi(argv[++i]);
            else if (arg == "--shape" && i + 1 < argc) shape_s = argv[++i];
            else if (arg == "--d1" && i + 1 < argc) only_d1 = std::stoi(argv[++i]);
            else throw std::runtime_error("unknown/incomplete argument: " + arg);
        }
        if (!allowed_s(s))
            throw std::runtime_error("--s must be one of 152,154,156,158,160");
        if (shape_s.empty()) throw std::runtime_error("--shape star|chain is required");
        if (only_d1 >= 0 && (only_d1 <= 0 || (only_d1 & 1)))
            throw std::runtime_error("--d1 must be a positive even integer");

        Search search(s, parse_shape(shape_s), only_d1);
        search.run();
        search.print_json();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 2;
    }
}
