#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

namespace {

#ifndef REPLAY_D1
#define REPLAY_D1 18
#endif
constexpr int S=152, B=128, D1=REPLAY_D1, YN=21, ROOTS=10, MAXV=279;

struct Root { int y; int color; };

struct Replay {
    int d2=0;
    std::array<unsigned char,MAXV+1> owner{};
    std::array<unsigned char,YN> local_mask{};
    std::array<unsigned char,YN> selected{};
    std::vector<Root> roots;
    std::uint64_t params_total=0, params_valid=0, params_with_survivor=0;
    std::uint64_t survivors=0, dfs_calls=0, extension_invocations=0, extension_calls=0;
    std::map<std::tuple<int,int,int>,std::uint64_t> histogram;
    std::vector<std::string> signatures;

    bool hole(int v) const { return v==S || v==S+D1 || v==S+d2; }
    bool allowed(int v) const { return 1<=v && v<=MAXV && !hole(v); }

    int low_depth(int color) const {
        return color==0?0:(color==1?D1:d2);
    }

    int low_high(int low,int y,int color) const {
        const int h=B+y;
        if(low==1) return color==0?h+D1:h-D1;
        if(color==0) return h+d2;
        if(color==1) return h+d2-2*D1;
        return h-d2;
    }

    int lca(int a,int b) const {
        if(a==0 || b==0) return 0;
        if(a==2 && b==2) return d2;
        return D1;
    }

    bool background_add(int v){
        if(!allowed(v) || owner[v]) return false;
        owner[v]=1; return true;
    }

    bool setup(int candidate_d2){
        d2=candidate_d2;
        owner.fill(0); local_mask.fill(0); selected.fill(0); roots.clear();
        if(!(D1<d2 && d2<B && (d2%2)==0)) return false;
        const int gap=d2-D1;
        if(!(D1<S && gap<S) || gap==D1) return false;
        if(!background_add(D1) || !background_add(d2)) return false;
        for(int y=0;y<YN;++y) if(!background_add(B+y)) return false;
        if(!background_add(gap)) return false;

        for(int y=0;y<YN;++y){
            unsigned char mask=0;
            for(int color=0;color<3;++color){
                const int att=B+y-low_depth(color);
                if(!(0<att && att<S)) continue;
                if(color==0 && att!=B+y) continue;
                const int a=low_high(1,y,color), b=low_high(2,y,color);
                if(a==b || !allowed(a) || !allowed(b)) continue;
                if(owner[a] || owner[b]) continue;
                mask|=static_cast<unsigned char>(1u<<color);
            }
            local_mask[y]=mask;
        }
        return true;
    }

    bool propose(int v,const std::vector<int>& pending) const {
        if(!allowed(v) || owner[v]) return false;
        return std::find(pending.begin(),pending.end(),v)==pending.end();
    }

    bool add_root(int y,int color,std::vector<int>& added){
        if(!(local_mask[y]&(1u<<color))) return false;
        std::vector<int> pending;
        const int a=low_high(1,y,color), b=low_high(2,y,color);
        if(!propose(a,pending)) return false; pending.push_back(a);
        if(!propose(b,pending)) return false; pending.push_back(b);
        const int att=B+y-low_depth(color);
        if(color==0 && att!=B+y) return false;
        if(color==1 && att!=a) return false;
        if(color==2 && att!=b) return false;
        for(const Root& r:roots){
            const int dist=2*B+y+r.y-2*lca(color,r.color);
            if(!propose(dist,pending)) return false;
            pending.push_back(dist);
        }
        for(int v:pending) owner[v]=1;
        added=std::move(pending);
        return true;
    }

    void undo(const std::vector<int>& added){ for(int v:added) owner[v]=0; }

    bool extend(int y){
        ++extension_calls;
        if(y==YN) return true;
        if(selected[y]) return extend(y+1);
#ifdef REPLAY_EXTENSION_ORDER_MATCH_PRIMARY
        // Audit mode: align only the short-circuit traversal order with the
        // primary implementation.  The feasible color set is unchanged.
        const int order[3]={0,1,2};
#else
        const int order[3]={1,2,0};
#endif
        for(int color:order){
            const int a=low_high(1,y,color), b=low_high(2,y,color);
            if(a==b || !allowed(a) || !allowed(b) || owner[a] || owner[b]) continue;
            owner[a]=owner[b]=1;
            const bool ok=extend(y+1);
            owner[b]=owner[a]=0;
            if(ok) return true;
        }
        return false;
    }

    std::string signature() const {
        std::array<std::vector<int>,3> ys;
        for(const Root& r:roots) ys[r.color].push_back(r.y);
        std::ostringstream out; out<<S<<"|chain|"<<D1<<'|'<<d2;
        for(const auto& group:ys){
            out<<'|';
            for(std::size_t i=0;i<group.size();++i){if(i)out<<',';out<<group[i];}
        }
        return out.str();
    }

    void record(){
        ++survivors;
        int count[3]={0,0,0}; for(const Root& r:roots) ++count[r.color];
        ++histogram[{count[0],count[1],count[2]}];
        signatures.push_back(signature());
    }

    int available_positions(int start) const {
        int n=0; for(int y=start;y<YN;++y) if(local_mask[y]) ++n; return n;
    }

    void dfs(int start,int need){
        ++dfs_calls;
        if(need==0){ ++extension_invocations; if(extend(0)) record(); return; }
        if(YN-start<need || available_positions(start)<need) return;
        const int last=YN-need;
        const int order[3]={2,0,1};
        for(int y=start;y<=last;++y){
            if(!local_mask[y]) continue;
            for(int color:order){
                if(!(local_mask[y]&(1u<<color))) continue;
                std::vector<int> added;
                if(!add_root(y,color,added)) continue;
                roots.push_back({y,color}); selected[y]=1;
                dfs(y+1,need-1);
                selected[y]=0; roots.pop_back(); undo(added);
            }
        }
    }

    void run(){
        for(int candidate_d2=D1+2;candidate_d2<B;candidate_d2+=2){
            ++params_total;
            if(!setup(candidate_d2)) continue;
            ++params_valid;
            const auto before=survivors;
            dfs(0,ROOTS);
            if(survivors!=before) ++params_with_survivor;
        }
        std::sort(signatures.begin(),signatures.end());
    }

    void print() const {
        std::cout<<"{\n  \"status\":\"INDEPENDENT_EXACT10_FULL21_D1_REPLAY\",\n"
                 <<"  \"s\":"<<S<<",\n  \"B\":"<<B<<",\n  \"shape\":\"chain\",\n"
                 <<"  \"d1\":"<<D1<<",\n  \"params_total\":"<<params_total
                 <<",\n  \"params_valid\":"<<params_valid
                 <<",\n  \"params_with_survivor\":"<<params_with_survivor
                 <<",\n  \"dfs_calls\":"<<dfs_calls
                 <<",\n  \"extension_invocations\":"<<extension_invocations
                 <<",\n  \"extension_calls\":"<<extension_calls
                 <<",\n  \"survivor_count\":"<<survivors<<",\n"
                 <<"  \"color_count_histogram\":{";
        bool first=true;
        for(const auto& kv:histogram){
            if(!first) std::cout<<','; first=false;
            auto [a,b,c]=kv.first;
            std::cout<<'\"'<<a<<','<<b<<','<<c<<"\":"<<kv.second;
        }
        std::cout<<"},\n  \"canonical_root_signatures\":[";
        for(std::size_t i=0;i<signatures.size();++i){
            if(i) std::cout<<','; std::cout<<'\"'<<signatures[i]<<'\"';
        }
        std::cout<<"]\n}\n";
    }
};

} // namespace

int main(){ Replay r; r.run(); r.print(); return 0; }
