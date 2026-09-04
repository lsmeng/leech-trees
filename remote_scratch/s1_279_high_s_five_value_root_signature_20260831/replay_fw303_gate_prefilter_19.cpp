#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>

struct Case {
    int index;
    int d2;
    std::set<int> roots;
    std::array<int,21> color;
};

Case make_case(int index,int d2,
               std::initializer_list<int> y0,
               std::initializer_list<int> y1,
               std::initializer_list<int> y2){
    Case c{index,d2,{},{}}; c.color.fill(-1);
    int col=0;
    for(auto group:{y0,y1,y2}){
        for(int y:group){c.roots.insert(y);c.color[y]=col;}
        ++col;
    }
    return c;
}

struct Profile { const char* gate; int q0; std::vector<int> positive; };

int main(){
    const std::vector<Case> cases{
        make_case(1,100,{5},{0,8,16},{2,3,4,6,9,15}),
        make_case(2,100,{5},{1,2,14},{0,3,6,8,10,17}),
        make_case(3,102,{4},{0,6,17},{1,2,3,5,10,15}),
        make_case(4,104,{3},{0,8,16},{2,4,5,6,11,17}),
        make_case(5,106,{4},{0,8,16},{1,6,11,12,13,15}),
        make_case(6,106,{5},{0,8,16},{1,7,10,12,13,14}),
        make_case(7,106,{7},{0,8,16},{2,3,4,6,9,15}),
        make_case(8,106,{5},{1,9,17},{0,3,7,12,13,14}),
        make_case(9,108,{3,7},{0,16},{2,5,8,13,14,15}),
        make_case(10,108,{5},{0,8,16},{2,3,4,6,9,15}),
        make_case(11,108,{5},{0,11,17},{2,7,12,14,15,16}),
        make_case(12,108,{5},{1,2,14},{0,3,6,8,10,17}),
        make_case(13,108,{5},{1,2,17},{0,3,6,10,12,14}),
        make_case(14,108,{5},{8,12,16},{0,1,2,7,14,17}),
        make_case(15,108,{5},{8,12,16},{0,1,2,11,14,17}),
        make_case(16,108,{5},{3,15,16},{0,7,9,11,14,17}),
        make_case(17,108,{4},{1,9,17},{2,7,12,13,14,16}),
        make_case(18,108,{5},{1,9,17},{2,8,11,13,14,15}),
        make_case(19,118,{4},{0,7,14},{1,9,11,12,13,17}),
    };
    const std::array<Profile,4> profiles{{
        {"z",13,{1,2,7,10,13}},
        {"b1",14,{1,3,8,11,14}},
        {"b2",15,{2,3,9,12,15}},
        {"c",17,{6,7,8,9,17}},
    }};

    int total=0;
    std::cout<<"{\n  \"status\":\"INDEPENDENT_FW303_GATE_PREFILTER_19\",\n  \"results\":[\n";
    bool first=true;
    for(const Case& tc:cases){
        int a_count=0,b_count=0,c_count=0;
        std::vector<std::string> a_rows;
        for(const auto& p:profiles){
            for(int q=p.q0;q<=20;++q){
                const int gate_y=20-q;
                bool conflict=false;
                for(int off:p.positive)
                    if(tc.roots.count(gate_y+off)) conflict=true;
                if(!conflict){
                    ++a_count;
                    a_rows.push_back(std::string(p.gate)+":"+std::to_string(q));
                }
            }
        }

        // For these 19 inputs, exact low depths are {0,18,d2}.  A mixed
        // one-low row requires gate depth 148-q to equal d2.  The only match
        // is d2=118, gate a, q=30.  It forces high z at y=0 to attach to u2
        // (color 2); signature 19 instead declares y=0 color 1.
        if(tc.d2==118){
            const bool forced_root_compatible=(tc.color[0]<0 || tc.color[0]==2);
            if(forced_root_compatible) ++b_count;
        }
        // Two-low d6 rows would require both t and t+6 to equal {18,d2};
        // here t>=116, so none is compatible.  No Class-C row remains.

        total+=a_count+b_count+c_count;
        if(!first) std::cout<<",\n"; first=false;
        std::cout<<"    {\"index\":"<<tc.index<<",\"d2\":"<<tc.d2
                 <<",\"A\":"<<a_count<<",\"B\":"<<b_count
                 <<",\"C\":"<<c_count<<",\"A_rows\":[";
        for(std::size_t i=0;i<a_rows.size();++i){
            if(i) std::cout<<',';
            std::cout<<'\"'<<a_rows[i]<<'\"';
        }
        std::cout<<"]}";
    }
    std::cout<<"\n  ],\n  \"total_compatible_signature_rows\":"<<total<<"\n}\n";
    return total==4?0:1;
}
