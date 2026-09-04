#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>

struct Profile {
    const char* gate;
    int q0;
    std::vector<int> positive_offsets;
};

int main() {
    // Independent table-form replay: use the four all-high rooted profiles
    // directly, rather than reconstructing the FW303 core graph.
    const std::set<int> selected_roots{0,2,3,4,5,6,8,9,15,16};
    const std::array<Profile,4> profiles{{
        {"z",  13, {1,2,7,10,13}},
        {"b1", 14, {1,3,8,11,14}},
        {"b2", 15, {2,3,9,12,15}},
        {"c",  17, {6,7,8,9,17}},
    }};

    int rows = 0;
    int conflicting = 0;
    std::cout << "{\n  \"status\":\"INDEPENDENT_CLASSA_GATE_ROOT_CONFLICT_REPLAY\",\n"
              << "  \"rows\":[\n";
    bool first_row = true;
    for (const Profile& p : profiles) {
        for (int q = p.q0; q <= 20; ++q) {
            ++rows;
            const int gate_y = 20 - q;
            std::vector<int> hits;
            for (int off : p.positive_offsets) {
                const int y = gate_y + off;
                if (selected_roots.count(y)) hits.push_back(y);
            }
            if (!hits.empty()) ++conflicting;
            if (!first_row) std::cout << ",\n";
            first_row = false;
            std::cout << "    {\"gate\":\"" << p.gate << "\",\"q\":" << q
                      << ",\"gate_y\":" << gate_y << ",\"conflicts\":[";
            for (std::size_t i = 0; i < hits.size(); ++i) {
                if (i) std::cout << ',';
                std::cout << hits[i];
            }
            std::cout << "]}";
        }
    }
    std::cout << "\n  ],\n  \"rows_total\":" << rows
              << ",\n  \"rows_with_conflict\":" << conflicting
              << ",\n  \"compatible_rows\":" << (rows-conflicting) << "\n}\n";
    return (rows == 25 && conflicting == 25) ? 0 : 1;
}
