# Fable 接手包：Leech-tree 主线接手、对抗审计与新路线搜索

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree  
项目根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`  
远程 checkout：Geo Workstation `/home/geo/codex-work/leech-trees`

## 给 Fable 的直接任务

请接手当前 Leech-tree 研究主线。你的首要目标不是把现有枚举继续跑大，而是：

1. 独立审计当前 frontier，找出任何错误的“已排除/已证明”表述；
2. 判断是否有比完整 `delta=284/285` depth/forest 枚举更短、更强、可写成论文引理的结构路线；
3. 只在路线 soundness 通过小例零误删后，提出一个最小的远程验证批次。

顾问结论只是候选证据，不能代替形式证明、完整 coverage 或独立复跑。

## 1. 接手前只读核对

先只读读取：

- `research_state.md`；
- `docs/handoff-fable-takeover-audit-2026-09-02.md`；
- `docs/fable-takeover-and-adversarial-audit-2026-09-02.md`；
- `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`；
- `docs/s1-component-mass-dp-2026-09-02.md`；
- `theory-lab/s1_crowding/component_mass_dp.py`；
- `theory-lab/s1_crowding/translated_sumset_csp_pilot.py`；
- `theory-lab/s1_crowding/parity_moment_audit.py`。

记录实际读取时的 Git revision、工作区状态和 SHA-256。当前参考值如下；若实际读取不同，以实际值为准：

```text
research_state.md
cf36c92da65f0ac2dc21e7984c55c2c12aa9a1e5d7e3577a8908f02d49819a1e

theory-lab/s1_crowding/translated_sumset_csp_pilot.py
93bca2c36c12baeb2361e78a438cadaf673fd250ca94971d5927d79d5783db2a

theory-lab/s1_crowding/parity_moment_audit.py
4233494c26a3504604785c55de7f855e705b5a0b7a33a7cf9e65e633a8ed3d96

docs/handoff-fable-takeover-audit-2026-09-02.md
f8f63469a87b70f829b4f31f8eecdc8e0c9ed594286421c296ee0597343225bc

docs/fable-takeover-and-adversarial-audit-2026-09-02.md
64aafe9b8b12957815cdd80cbb9342d37388f6ea13160956b81e36ff866cb046
```

正式 checkout 当前有大量既有未提交/未跟踪研究产物；不要清理、重置或提交。不要覆盖他人 scratch 或正式证书。

## 2. 目前真正知道了什么

### VERIFIED / REPRODUCED

- Top-block 值域计数给出 `C(m,2) <= (r+1)(2m-3)`，所以 `r=3,m=21`（`delta=279`）和 `r=4,m=20`（`delta=280`）直接矛盾。这个结论依赖值域容量计数，不依赖未经证明的高层 LCA 说法。
- `s=154, shape=star` 的固定分支 62/62 有限排除；只覆盖该固定分支。
- component-mass DP 小例 `m=5, lowpar=-1,0,1` 的方程检查 73/73 通过；这是接口/小例验证，不是 284/285 全局证明。
- translated-sumset 的统一树、ancestor-list LCA、BFS 复核在 order-6 genuine positive control 上通过。
- occupied 层（holes `{s+l_v}` 与固定 x-high `[B,B+m-1]`，带越界/碰撞 guard）在 genuine control 上没有误删。
- `parity_moment_audit.py` 在 order-6 genuine control 上满足：直接 BFS、edge-cut 第一矩和目标值一致。

### FINITE-EVIDENCE / PARTIAL PRODUCTION EVIDENCE

- `delta=284`：115 个 low shapes 中 7 个 structure-bearing；`delta=285`：286 个中 95 个 structure-bearing。需要核对 source/binary/input/output provenance 后才能成为完整有限证书。
- 真实 `delta=284,m=16,r=8` 单形状：occupied-v3 到 `nodes=500001` 的 node limit；`tested_s=159`，`high_high_passes=17201`，`occupied_prune_rejects=5332120`，`xhigh_out_of_range_rejects=15`，BFS pair count 120。它说明该前缀没有闭合，但不是完整排除。
- `delta=285,m=15,r=9` 的 occupied-v3 输出为空/超时，必须标为 `OUTPUT_MISSING/TIMEOUT`，不是零 survivor。
- 现有 Hoffman2 arrays（`115848`、`115912`、`115949`、`115950`）只读观察，不能取消、重启或改参数。

### 两个具体候选的独立必要条件审计

- r8 witness `s=158,L=[0,18,40,41,51,59,88,92]`：奇偶 odd-pair 数为 154 而目标为 150；第一矩为 47194 而目标为 45150。因此该具体候选可排除。
- r9 witness `s=157,L=[0,13,1,2,3,24,33,77,101]`：奇偶数 150 通过，但第一矩为 47064 而目标为 45150。因此该具体候选可排除。

以上都不能外推为 `delta=284/285` 全域结论。

## 3. 必须保持的证据边界

严格区分：

- `VERIFIED`：形式推理或完整、可复核的证书链；
- `REPRODUCED`：独立实现/独立运行得到相同结果；
- `FINITE-EVIDENCE`：固定 corpus、固定输入和完整终止范围的有限结果；
- `CANDIDATE`：必要条件、猜想或尚未闭合的路线；
- `UNKNOWN/GAP`：`NODE_LIMIT`、超时、空输出、缺 corpus、coverage 或 provenance 未闭合。

禁止把 node limit、超时、前缀计数、“没找到 survivor”、单个 shape 或 advisor 的口头结论写成全域证明。

## 4. 请优先寻找“更好的思路”

### 路线 A：把 component-mass 直接接到 depth-Hall

审计并尝试证明以下量是否对所有允许树形状成立：

```text
W = Σ C(n[v,j],2) <= 2m-3
P_v = C(M_v,2) - Σ_child C(M_child,2) - Σ_j C(n[v,j],2) <= 2m-3
W + Σ_v P_v = C(m,2)

s >= ceil((delta + 2 + P_root)/2)
LB_v(s) = max(1, ceil((delta + 2 - 2s + P_v)/2))
E_v = max(LB_v, E_parent + 1)
```

重点不是再加一层 DFS，而是找出统一的 Hall/capacity 矛盾，能否一次性压掉许多 shape 或所有 `r=8/9` 情形。每个式子都要给出精确量词、边界条件和最小反例。

一个比逐点 suffix-Hall 更强、仍可直接审计的候选是“需求跨度”不等式。令
`C0=2m-3`，对每个 low-LCA 类记 `S_v` 为其未平移的和集合，`P_v=|S_v|`，
并令
`T_v=2B-2l_v+S_v`。由于不同 LCA 类的距离必须互异，对任意 low-class
子集 `Q` 都必须有

```text
Σ_{v∈Q} P_v <= C0 + 2(max_{v∈Q} l_v - min_{v∈Q} l_v).
```

证明只用区间包络：每个 `T_v` 都包含在长度为 `C0`、平移量为 `-2l_v`
的区间内，所有这些区间的并包含在两端区间的跨度内；真实 `T_v` 彼此
不交，所以总基数不能超过该跨度。与 high-LCA 类合并还给出

```text
W + P_v <= C0 + min(C0, 2*(B-l_v)).
```

这些式子只是必要条件：通过不代表存在；接入 production 前仍需检查
`W+ΣP_v=C(m,2)`、深度顺序、边界截断和 occupied 槽位，并在 genuine
positive controls 上做 zero-false-reject differential。若出现反例，记录
最小 `(m, lowpar, P, L)`，不要把不等式当作定理外推。

### 路线 B：全局必要条件，不依赖完整 forest

检查 parity 与 Wiener 第一矩是否能同 `(m,c,W,P-vector)` 或 root-coloring signature 联立，形成对整个 shape 类的整数不等式。目标形式例如：

```text
O(25-O)=150,  O∈{10,15}
Σ_e a_e(25-a_e) w_e = 45150
```

如果能把 edge-cut 贡献、低/高层 owner 和 component mass 消去，优先尝试写成可人工审计的 lemma，而不是仅作为程序 presolver。

### 路线 C：增强 translated-sumset，但必须证明 sound

逐项检查：

- `|H| + Σ|S_v| = C(m,2)` 是否严格成立；
- H 与每个 `S_v` 内部重复、跨 `S_v` raw-sum 重复的量词是否正确；
- holes、x-high、L 的 owner 是否互异；
- high-parent/low-root 顺序和所有越界 guard；
- BFS 权重是否与原距离公式逐项一致。

可以考虑 exact low-low、全局 distance-slot flow、跨 `S_v` 联合 Hall、按 signature 分层、生成函数或小型 ILP/SAT；但任何新剪枝必须先在 order-6 genuine positive control 和人工可行双-low/三-low 小例上做 zero-false-reject differential。没有这个门槛，不得接入 production。

### 路线 D：直接找结构性不变量

尝试寻找一个短命题，能同时处理 7 个 `delta=284` 或 95 个 `delta=285` structure-bearing shape，例如：

- 模类/区间容量不变量；
- high-high slot 总和与 component mass 的统一上界；
- root-coloring、edge owner、LCA class 的精确覆盖；
- 把 parity、第一矩、第二矩组合成对 shape signature 的不可满足条件。

不要把旧 FW303 的 Class A/B/C 不加证明地套用到当前 frontier。

## 5. 计算与机器边界

- 本机 24 GB：只允许文本、diff、哈希和轻量审计；禁止本机枚举、参数扫描或长 Python/C++。
- 重计算只能提交 Geo Workstation 或 Hoffman2。Geo 使用 `DevSpace workstation`，checkout `/home/geo/codex-work/leech-trees`，允许根目录 `/home2/geo/` 与 `/media/geo/`。
- 新任务最多 4 workers，统一 `nice -n 15`，长任务必须有明确 timeout；开始前查残留，结束后查孤儿。
- 现有远程作业只读观察，不取消、不重启、不改参数。
- 所有新输出放 scratch，保存脚本、输入、命令、机器、revision、SHA-256 和终止状态；不要提交或推送。

## 6. 最小接手交付

请在 `docs/` 新增带日期的结果，或追加到研究状态，回答：

```text
实际读取 revision / git 状态：
实际文件与 SHA-256：
远程作业是否修改：

VERIFIED：
REPRODUCED：
FINITE-EVIDENCE：
CANDIDATE：
UNKNOWN / GAP：

translated-sumset soundness verdict：
occupied / low-low verdict：
component-mass / depth-Hall verdict：
parity + Wiener verdict：

更好路线：命题、证明草图、最小反例或零误删验证：
若失败，失败证据：
唯一推荐下一步及完成标准：
```

## 7. 唯一优先下一步

先不要放大 284/285 的 node limit。最高价值的下一步是：

1. 在冻结的真实 structure corpus 上，为 parity + Wiener 第一矩建立低成本 presolver；
2. 用 order-6 genuine、人工双-low/三-low 小例做 zero-false-reject differential；
3. 若 sound 且确有大幅削减，再在 Geo Workstation 上对 284/285 做最多 4-worker、有界的最小批次；
4. 若 presolver 没有统一收益，停止堆剪枝，优先把路线 A/B/D 中最有希望的一条写成精确 lemma 或给出最小反例。

真正的生产缺口仍是：完整 immutable 的 `delta=284/285` structure/depth corpus、可复跑 provenance、完整 coverage，以及真实 survivor 的 zero-false-reject differential。

## 8. 停止条件

只有遇到密码/MFA/CAPTCHA、破坏性动作、提交/推送/公开发布、写冲突，或远程资源确实不可用且无安全替代时才暂停并报告。普通 timeout、一个过滤器不够强或 advisor 没有立即回复，都不构成全项目停止理由。

## 9. 最新只读补充：Hoffman2 `delta=286` 结构层

Hoffman2 已完成的 `s1abs` 批次产生了 `m=14,r=10` 的 abstract 层结果。按源码
`delta=C(24,2)+r`，这是 `delta=286`，不是当前 `delta=284/285` 的最终 depth
问题。聚合文件已复制为：

```text
remote_scratch/hoffman_abstract_20260902/all_sorted.txt
SHA-256: 2f91a166a5ca9adfbbac0445782358c0ec7b9149e49e3d30aacef40ffac21723
```

轻量独立检查得到：719 个唯一 abstract shape，317 个 `EXISTS`，402 个
`EXHAUSTED`；32 个 shard summary 覆盖 `0..31`；每个 summary 的
`shapes_run + skipped_other_shards = 719`，且加上 `skipped_iso` 后为
`362880=9!`。这可暂记为 `FINITE-EVIDENCE / STRUCTURE-ONLY`，但因尚未独立
取得所有原始分片、提交命令和编译二进制哈希，仍是 `PROVENANCE-INCOMPLETE`。
请把它作为寻找跨 `r` 层不变量的线索，不要把它当作 `delta=284/285` 的证明。

随后新增轻量文本审计器
`theory-lab/s1_crowding/audit_abstract_aggregate.py`（SHA-256
`b0f4be3ba27173fbbd39c01081625746bbbb26bd8fbc2293b66ed397bdbda7ef`），对上述
聚合文件生成 `remote_scratch/hoffman_abstract_20260902/audit.json`，其
`all_checks_ok=true`。检查覆盖记录唯一性、状态分割、32 个 shard 编号、每个
summary 的 coverage、`9!` 原始计数和 leaves 一致性；它明确是文本一致性审计，
不是深度证书。接手时请先复核该 JSON，再决定是否值得向 `delta=284/285` 回溯
同类 coverage/provenance。

## 10. 最新顾问意见与冻结 r10 pilot（2026-09-02）

`Leech tree chat2` 已完成一次有界审阅（`CONSULT-20260902-014`）。请优先
考虑它提出的 **colored moment-Hall completion lemma**：固定 abstract structure
后，联合保留 `H`、每个 low-LCA 类的 raw-sum 集合 `S_v`、差集 `S_i-S_j`、深度
平移、parity 和 Wiener 第一矩；对任意类子集使用 Hall 与 moment-Hall。这个方向
比单纯增加 DFS node limit 更有希望，但目前仍是候选路线。顾问的负面审计同样
重要：没有证据表明所有 `r=8/9/10` 结构都 UNSAT；仅用 component mass 或
`(W,P)` 会丢失差集信息，不能当作 sound 全局剪枝。

已在 Geo Workstation 冻结并审计一个真实 r10 结构：

```text
lowpar = 0,0,0,0,0,1,6,7,8
STRUCT = -1 -2 -7 -8 -9 -10 -10 -10 5 -9 -8 -7 -2 -1
binary sha256 = 5270bd212a93e786549c1fd6f1e9da399b7c94b0d6f582042f8e278be949799e
struct sha256 = 97cf0a8a656ebbb25b41de745dbb4bb5790c4bbe228ab4c6012d28ed8417e9e5
RC = 0, leaves = 1, nodes = 7173
```

结构-only 审计器
`theory-lab/s1_crowding/colored_moment_hall_audit.py`（SHA-256
`dde5c4cebdf62cff40e97c0313f225efb69fdbf58c343cbe913e390ba755fd8a`）生成
`remote_scratch/demand_span_r10_20260902/colored_audit_v1/colored_audit.json`
（SHA-256 `3ea46c2c7dc74c7167947fbd49c3c586be9222d0b39908d35ca5ffb3754d6a38`）。
它验证了 `pair_total=91`、`H_unique=true`、全部 `S_v` 内部唯一、
`W=1`、`P=[25,21,0,0,0,0,17,13,9,5]` 及固定结构的 Wiener 仿射式。该文件
只支持 **VERIFIED structure-only necessary audit**，不支持深度存在性结论。

旧 translated-sumset 全搜索基线在同一结构上以 120 秒上限超时（`RC=124`，
输出 JSON 为空；无残留进程）。请把它登记为 `TIMEOUT / OUTPUT_MISSING`，不要
误读成“零 survivor”，也不要重复这条慢路径。

### 给 Fable 的接手任务

1. 先只读复核本文件、`research_state.md`、上述 `colored_audit.json` 以及
   `docs/demand-span-lemma-audit-2026-09-02.md`；确认结构、哈希和证据等级。
2. 提出一个更好的、可人工审计的统一 lemma，优先覆盖
   `S_i-S_j`、parity-colored Hall、moment-Hall 和 Wiener 仿射约束；明确量词、
   owner 去重、holes/occupied 删除规则和边界条件。
3. 如需实现 presolver，只能先放 scratch；先在 genuine positive control 与
   人工双-low/三-low 小例上做 zero-false-reject differential，不得直接替换
   production DFS。
4. 只有 sound 且有明确削减收益后，才拟定 Geo Workstation 上最多 4 workers、
   `nice -n 15`、有界 timeout 的最小 r8/r9 批次；不碰现有远程作业。

请返回：更好的命题/证明草图或最小反例、对现有路线的接受/拒绝理由、实际改动
文件与命令、验证结果、未闭合缺口，以及下一步是否值得投入远程算力。

## 11. `CONSULT-20260902-016` 的补充规格与边界修正

普通 Chat 顾问的短重试已返回完整审阅。最值得实现的是一个只生成 structure
certificate 的 `translated_difference_domains` 模块，而不是继续扩大 `(s,L)`
DFS。输入 `lowpar,hpar,delta`，输出 `H`、`S_v`、`P_v`、raw-sum/parity 统计、
`S_i-S_j` 的 forbidden depth differences 以及 Wiener 仿射系数。该模块不搜索
深度，因此容易逐项人工审计。

固定 `(s,L)` 后可安全判 `UNSAT` 的情况包括：H/S 内部碰撞、pair partition 错误、
平移越界、exact difference collision、H/T 或已确认 occupied owner 碰撞、Hall/
colored Hall、moment-Hall、全局 parity 或 Wiener equality 失败。所有这些条件
通过时只能记作 `NOT-EXCLUDED`，因为 LL、LH 和完整 owner ledger 尚未覆盖。

最小 zero-false-reject 验收集应包含：

1. 已知 order-6 genuine `s=8,L=[0]` 正例；
2. 人工核过的双-low 正例，用于检查差集符号、平移和 parity 颜色；
3. 人工三-low 负例，分别制造 exact-difference、Hall 和 moment-Hall 失败。

另外修正了
`theory-lab/s1_crowding/translated_sumset_csp_pilot.py`：启用 occupied 时，
hole owner 的距离 `s+l` 超出 `[1,delta]` 现在明确拒绝，并记录
`hole_out_of_range_rejects`。这是补足漏剪枝，不是放宽条件；本轮只做语法检查和
`git diff --check`，未运行搜索。修正后脚本 SHA-256 为
`4e14150bf84817a448f419e76a385fa52e2c9891397a83eab2755ce662ed28d0`。

## 12. 结构证书最小模块已落地

新增
`theory-lab/s1_crowding/translated_difference_domains.py`（SHA-256
`98aefed17c6f104dec8254946aa3d8bfa9963a37ec83c9304b456c4fcfe0d007`）。它只做
结构层工作：输出 `H`、`S_v`、`P_v`、raw-sum 差集、对应的偶数深度禁配值和
Wiener 仿射系数，不枚举 `(s,L)`，不替换 production DFS。一个重要实现细节是
禁配字段存储 `d/2`（其中 `d∈S_i-S_j` 为偶数），即直接对应
`l_i-l_j`，不是 raw difference 本身。

对冻结 r10 structure 的轻量复核已经通过：`pair_total=91`、`W=1`、
`P=[25,21,0,0,0,0,17,13,9,5]`、H/S 内部唯一且结构证书状态为
`STRUCTURE_CERT_OK`。这只验证接口和结构分割，仍不代表任何 `(s,L)` 存在或
全局非存在。

该结构证书工具随后在 Geo Workstation scratch 上以单 worker、`nice -n 15`、
30 秒上限实际运行一次，约 0.05 秒完成；输出
`remote_scratch/demand_span_r10_20260902/colored_audit_v1/translated_difference_domains.remote.json`
已回收，SHA-256 为
`96aca92b8f4c22a11134034c6ddf84b7ba7cd9a08b27e7a9374fdd40d27ab0a1`。远程输出的
91-pair 结构断言与本地一致，且没有遗留 pilot 进程。该结果只加强结构证书的
可复现性，不改变“尚未完成 `(s,L)` 或全局证明”的证据等级。

## 13. r8/r9 真实单结构证书回放

复查远程 scratch 发现，已有的 r8 `delta=284` 和 r9 `delta=285` 单结构搜索结果
均停在 `NODE_LIMIT`，所以不构成排除。随后仅对它们的固定结构做了结构证书回放，
没有重跑深度搜索：

```text
delta=284, m=16, r=8: pair_total=120, W=1,
P=[29,25,0,21,17,13,9,5]
remote SHA-256: 6c31fa385a75d9292a7a4d06dbfd039738cfcbcc84e1c05c54c6f9f75abf9a8c

delta=285, m=15, r=9: pair_total=105, W=6,
P=[27,23,0,0,0,19,15,11,4]
remote SHA-256: c3a7914bdc95f95ec3dfeeb0c973f2b88fb8f32460b5a733383c64e1bc331578
```

两份远程证书都通过 H/S 分割与内部唯一性断言。它们只证明结构数据可复现，
不能把原来的 `NODE_LIMIT` 升级为 `UNSAT`，也不能外推到完整 284/285 corpus。
