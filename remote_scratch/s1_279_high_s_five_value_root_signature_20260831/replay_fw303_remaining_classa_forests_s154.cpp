#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int S = 152;
constexpr int D1 = 18;
constexpr int B = 128;
constexpr std::array<int,6> W{{4,5,16,18,19,20}};
constexpr std::array<int,5> CORE_W{{1,2,6,7,10}};

struct Case {
    const char* name;
    int d2;
    std::array<int,21> selected_color;
    std::array<int,21> fixed_parent;
};

struct Counts {
    std::uint64_t root_sets = 0;
    std::uint64_t root_colorings = 0;
    std::uint64_t root_edge_legal = 0;
    std::uint64_t weight_assignments = 0;
    std::uint64_t parent_legal = 0;
    std::uint64_t spectrum_survivors = 0;
};

Case make_case(
    const char* name,
    int d2,
    const std::array<std::vector<int>,3>& roots,
    const std::vector<std::pair<int,int>>& fixed
) {
    Case out{name,d2,{},{}};
    out.selected_color.fill(-1);
    out.fixed_parent.fill(-1);
    for (int color=0;color<3;++color)
        for (int y: roots[color]) out.selected_color[y]=color;
    for (auto [y,p]: fixed) out.fixed_parent[y]=p;
    return out;
}

std::vector<Case> cases() {
    return {
        make_case("sig3-z-q14",102,
            {{{4},{0,6,17},{1,2,3,5,10,15}}},
            {{7,6},{8,6},{13,6},{16,6},{19,13}}),
        make_case("sig5-b1-q14",106,
            {{{4},{0,8,16},{1,6,11,12,13,15}}},
            {{7,6},{9,7},{14,7},{17,7},{20,14}}),
        make_case("sig9-c-q17",108,
            {{{3,7},{0,16},{2,5,8,13,14,15}}},
            {{9,3},{10,3},{11,10},{12,10},{20,10}}),
        make_case("sig13-z-q14",108,
            {{{5},{1,2,17},{0,3,6,10,12,14}}},
            {{7,6},{8,6},{13,6},{16,6},{19,13}}),
    };
}

int attachment_weight(int d2,int y,int color) {
    const int low_depth[3]={0,D1,d2};
    return B+y-low_depth[color];
}

bool full_spectrum(
    int d2,
    const std::array<int,21>& root_color,
    const std::array<int,21>& parent
) {
    std::array<std::vector<std::pair<int,int>>,24> adj;
    auto add=[&](int a,int b,int w){
        adj[a].push_back({b,w});
        adj[b].push_back({a,w});
    };
    add(0,1,D1);
    add(1,2,d2-D1);
    for(int y=0;y<21;++y){
        if(root_color[y]>=0)
            add(root_color[y],3+y,attachment_weight(d2,y,root_color[y]));
        else
            add(3+parent[y],3+y,y-parent[y]);
    }

    std::vector<int> got;
    got.reserve(276);
    for(int src=0;src<24;++src){
        std::array<int,24> dist;
        dist.fill(-1);
        dist[src]=0;
        std::vector<int> stack{src};
        while(!stack.empty()){
            int v=stack.back(); stack.pop_back();
            for(auto [u,w]:adj[v]) if(dist[u]<0){
                dist[u]=dist[v]+w;
                stack.push_back(u);
            }
        }
        for(int v=src+1;v<24;++v){
            if(dist[v]<0) return false;
            got.push_back(dist[v]);
        }
    }
    std::sort(got.begin(),got.end());
    std::vector<int> target;
    for(int v=1;v<=279;++v)
        if(v!=S && v!=S+D1 && v!=S+d2) target.push_back(v);
    return got==target;
}

struct Search {
    const Case& tc;
    int c;
    int extra_count;
    int e;
    Counts counts;
    std::vector<int> eligible;
    std::vector<int> chosen;

    Search(const Case& tc_,int c_):tc(tc_),c(c_),extra_count(c_-10),e(16-c_){
        for(int y=0;y<21;++y)
            if(tc.selected_color[y]<0 && tc.fixed_parent[y]<0) eligible.push_back(y);
    }

    void weight_rec(
        const std::vector<int>& unknown,
        const std::vector<int>& available,
        int idx,
        unsigned used,
        std::array<int,21>& parent,
        const std::array<int,21>& root_color
    ) {
        if(idx==e){
            ++counts.weight_assignments;
            for(int i=0;i<e;++i) if(parent[unknown[i]]<0) return;
            ++counts.parent_legal;
            if(full_spectrum(tc.d2,root_color,parent)) ++counts.spectrum_survivors;
            return;
        }
        for(std::size_t j=0;j<available.size();++j){
            if(used&(1u<<j)) continue;
            int child=unknown[idx];
            int p=child-available[j];
            parent[child]=p;
            weight_rec(unknown,available,idx+1,used|(1u<<j),parent,root_color);
            parent[child]=-1;
        }
    }

    void evaluate_colors(const std::vector<int>& colors){
        ++counts.root_colorings;
        std::array<int,21> root_color=tc.selected_color;
        for(int i=0;i<extra_count;++i) root_color[chosen[i]]=colors[i];

        std::array<bool,280> used{};
        auto add_edge_weight=[&](int w){
            if(w<=0 || w>=S || used[w]) return false;
            used[w]=true;
            return true;
        };
        if(!add_edge_weight(D1) || !add_edge_weight(tc.d2-D1)) return;
        for(int w:CORE_W) if(!add_edge_weight(w)) return;
        for(int y=0;y<21;++y) if(root_color[y]>=0)
            if(!add_edge_weight(attachment_weight(tc.d2,y,root_color[y]))) return;
        ++counts.root_edge_legal;

        std::vector<int> unknown;
        std::array<int,21> parent=tc.fixed_parent;
        for(int y=0;y<21;++y)
            if(root_color[y]<0 && parent[y]<0) unknown.push_back(y);
        if(static_cast<int>(unknown.size())!=e) return;
        std::vector<int> available;
        for(int w:W) if(!used[w]) available.push_back(w);
        if(static_cast<int>(available.size())<e) return;
        weight_rec(unknown,available,0,0,parent,root_color);
    }

    void color_rec(int idx,std::vector<int>& colors){
        if(idx==extra_count){evaluate_colors(colors);return;}
        for(int color=0;color<3;++color){
            colors[idx]=color;
            color_rec(idx+1,colors);
        }
    }

    void combination_rec(int start,int need){
        if(need==0){
            ++counts.root_sets;
            std::vector<int> colors(extra_count,0);
            color_rec(0,colors);
            return;
        }
        for(int i=start;i<=static_cast<int>(eligible.size())-need;++i){
            chosen.push_back(eligible[i]);
            combination_rec(i+1,need-1);
            chosen.pop_back();
        }
    }

    Counts run(){combination_rec(0,extra_count);return counts;}
};

} // namespace

int main(){
    auto all=cases();
    std::uint64_t total_survivors=0;
    std::cout << "{\n  \"status\":\"INDEPENDENT_FW303_CLASSA_FOREST_REPLAY\",\n  \"results\":[\n";
    bool first=true;
    for(const Case& tc:all){
        for(int c=10;c<=13;++c){
            Counts x=Search(tc,c).run();
            total_survivors+=x.spectrum_survivors;
            if(!first) std::cout << ",\n";
            first=false;
            std::cout << "    {\"case\":\""<<tc.name<<"\",\"c\":"<<c
                      <<",\"root_sets\":"<<x.root_sets
                      <<",\"root_colorings\":"<<x.root_colorings
                      <<",\"root_edge_legal\":"<<x.root_edge_legal
                      <<",\"weight_assignments\":"<<x.weight_assignments
                      <<",\"parent_legal\":"<<x.parent_legal
                      <<",\"spectrum_survivors\":"<<x.spectrum_survivors<<"}";
        }
    }
    std::cout << "\n  ],\n  \"total_full_spectrum_survivors\":"<<total_survivors<<"\n}\n";
    return total_survivors==0?0:1;
}
