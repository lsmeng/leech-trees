# Fable 接手任务单：Leech-tree 主线与更好路线对抗审计

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree  
项目根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`

这是一份可直接交给 Fable 的自包含接手单。目标不是复述已有工作，而是独立检查当前 frontier，并优先判断是否存在比“完整 depth/forest 枚举”更短、更强、可写成论文引理的路线。

## 1. 先读与当前基线

请先只读打开：

1. `research_state.md`；
2. `docs/handoff-fable-takeover-audit-2026-09-02.md`（长版历史、公式、旧产物哈希）；
3. `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`；
4. `docs/s1-component-mass-dp-2026-09-02.md`；
5. `theory-lab/s1_crowding/component_mass_dp.py`；
6. `theory-lab/s1_crowding/translated_sumset_csp_pilot.py`；
7. 本文件所列远程 scratch 和 Hoffman2 状态。

开始报告中记录实际 revision、文件 SHA-256、Git 状态以及远程作业状态。不要只相信聊天摘要或“已完成”字样。

当前可复核的本地脚本 SHA-256（含可选 `--include-low-low` 剪枝，默认关闭）：

```text
theory-lab/s1_crowding/translated_sumset_csp_pilot.py
93bca2c36c12baeb2361e78a438cadaf673fd250ca94971d5927d79d5783db2a
```

正式长版接手文档当前 SHA-256：

```text
docs/handoff-fable-takeover-audit-2026-09-02.md
a148cf82d39f58a2674918be1427b321142c7f022f2e1bb4fcedb05d68393c2d
```

若文件在你读取后发生变化，以实际读取的 SHA 为准，并把差异写进审计结果。

## 2. 目标与严格证据边界

最终目标仍是证明或否定 Leech-tree 猜想。当前关键未闭合区域是 `delta=284` 和 `delta=285` 的结构/深度阶段，而不是已经完成的 toy 例。

证据标签必须严格区分：

- `VERIFIED`：形式化推理或可复核的完整证书链；
- `REPRODUCED`：独立复跑得到相同结果；
- `FINITE-EVIDENCE`：明确固定参数、shape、输入 corpus 和完整终止范围的有限结果；
- `CANDIDATE`：必要条件过滤器、猜想、尚未闭合的结构路线；
- `UNKNOWN/GAP`：超时、`NODE_LIMIT`、`.tmp`、缺失 corpus、provenance 未闭合。

特别禁止：

- 把 `NODE_LIMIT`、超时、前缀计数或“没有见到 survivor”写成完整排除；
- 把同一程序的重复运行叫作独立算法；
- 把 `delta=281..283` 的 Fable 报告越过 source/binary/input provenance 缺口直接升级为证明；
- 从单个 `delta=284/285` shape 外推全域；
- 在本机做枚举、参数扫描或长 Python/C++。

## 3. 已有 frontier（只接受经核对的部分）

### 已验证或可独立核对

1. Top-block 值域计数给出
   `C(m,2) <= (r+1)(2m-3)`；因此 `r=3,m=21`（`delta=279`）和 `r=4,m=20`（`delta=280`）直接矛盾。理由是距离值域大小，不是“high-LCA 的 q 由 y+y' 决定”。
2. `s=154, shape=star` 的 62/62 固定分支有限排除；只覆盖该固定分支。
3. `s=154, shape=chain` exact-10 有大量必要子系统 survivor；它们不是完整树存在性证明。
4. component-mass DP 小例 smoke test：`m=5, lowpar=-1,0,1`，108 个质量模式、73 个通过必要条件，独立方程检查 73/73。
5. translated-sumset 的 unified-tree + ancestor-list LCA 在 order-6 genuine positive control 上通过 BFS；`bfs_check.ok=true`。
6. occupied 层（holes `{s+l_v}` 加固定 x-high `[B,B+m-1]`，含越界/碰撞 guard）在 order-6 genuine control 上没有误删。

### 仅为有限/前缀证据，不能升级

1. Fable 报告的 `delta=281,282,283` 结果仍有 source/binary/input provenance 缺口；先审计，不能直接称 certified。
2. `delta=284`：115 个 low shapes 中 7 个 structure-bearing；`delta=285`：286 个中 95 个 structure-bearing。这是现有结构阶段报告，完整 depth 证据仍待闭合。
3. Hoffman2：array `115848`（r8/depth）64 个 task 运行；`115912`（r9/depth）36 个运行、其余受 QOS pending；`115949/115950`（s1abs）pending。不得取消、重启、改参数。
4. 首个真实 structure-bearing 单形状控制：
   - `delta=284,m=16,r=8`：`lowpar=0,0,1,3,4,5,6`，C++ `RC=0, leaves=1, nodes=12346`，BFS 覆盖 120 个 high pairs；occupied v3 在 500000 node limit 下 `occupied_prune_rejects=5332120`、`high_high_passes=17201`、`status=NODE_LIMIT`。
   - `delta=285,m=15,r=9`：`lowpar=0,0,0,0,1,5,6,7`，C++ `RC=0, leaves=1, nodes=7687`，BFS 覆盖 105 个 high pairs；occupied v3 当前没有可用完整输出（文件为空/运行超时），不得填入统计。
5. 因而当前 production 状态仍是：`PRODUCTION EFFECTIVENESS GAP — no immutable complete 284/285 hpar/depth corpus and no zero-false-reject differential`。

## 4. Fable 的首要任务：先找更好的思路

请按以下优先级做“反证式”路线搜索，每条路线都必须给出形式化量词和失败条件：

### A. 把 component-mass 接到 depth-Hall

检查并尝试加强：

```text
W = Σ C(n[v,j],2) <= 2m-3
P_v = C(M_v,2) - Σ_child C(M_child,2) - Σ_j C(n[v,j],2) <= 2m-3
W + Σ_v P_v = C(m,2)

s >= ceil((delta + 2 + P_root)/2)
LB_v(s) = max(1, ceil((delta + 2 - 2s + P_v)/2))
E_v = max(LB_v, E_parent + 1)
```

审计这些式子的必要性、边界条件和是否真正减少 `(structure,s,L)` workload。优先寻找可直接导致 Hall 失败的统一不等式，而不是再加一层未经证明的 DFS。

### B. 审计并加强 translated-sumset CSP

当前脚本重建 `H`、每个 `S_v`、`T_v=2B-2l_v+S_v`，并可做 BFS 距离复核与 occupied 必要条件。请检查：

- high parent 只能指向更早节点；负 parent 的 low-root 范围；
- `|H| + Σ|S_v| = C(m,2)`；H 与每个 S_v 内无重复；不同 S_v 的 raw sum 重复是否被错误禁止；
- holes、x-high、L 的固定 owner 是否真的互异；越界 guard 是否 sound；
- BFS 权重是否与原距离公式完全一致。

然后评估更强但仍 sound 的层：exact LL、全局 distance-slot flow、跨 `S_v` 的联合 Hall/匹配、按 `(m,c,W,P-vector)` 分层、生成函数或小型 ILP/SAT。任何“更强”都必须先在 order-6 genuine positive control 和至少一个人工可行小例上零误删，再谈生产接入。

### C. 寻找不依赖完整 forest 的结构性不变量

请特别检查是否存在：

- 对所有低树形状同时成立的容量/模类/区间不变量；
- 将 high-high distance slots 与 component mass 直接联立的总和界；
- 对 root-coloring、edge owner、LCA class 的精确覆盖或生成函数反证；
- 能把 95 个 `delta=285` 或 7 个 `delta=284` structure-bearing shape 一次性分层排除的 lemma。

不要把旧 FW303 的 Class A/B/C 直接套用到 `delta=284/285`；必须重新证明 interface 和适用量词。

## 5. 计算与机器边界

- 本机 24 GB：只做文本、diff、哈希和轻量证明审计；禁止本机枚举或长脚本。
- 重活只能放 Geo Workstation 或 Hoffman2。Geo 连接使用 `DevSpace workstation`，checkout 为 `/home/geo/codex-work/leech-trees`，允许根目录为 `/home2/geo/` 与 `/media/geo/`。
- 每台机器最多 4 个 worker；统一 `nice -n 15`，长任务加明确 `timeout`；开始前查残留，结束后查孤儿进程。
- 现有 Hoffman2 arrays 只读观察，不取消、不重启、不改参数。
- 新计算优先 scratch；不要覆盖正式证书或和其他写入者同时改同一文件；不要提交或推送。

## 6. 接手后的最小交付

请在 `docs/` 新增一个带日期的审计结果，或在 `research_state.md` 追加一节，至少包含：

1. 实际读取的 revision、源/二进制/输入/输出 SHA-256；
2. 哪些结论升为 `VERIFIED/REPRODUCED/FINITE-EVIDENCE`，哪些仍是 `CANDIDATE/UNKNOWN/GAP`；
3. 对现有 translated-sumset、occupied、mass-DP、depth-Hall 的 soundness verdict；
4. 至少一个“更好路线”候选：形式化命题、证明草图、最小反例搜索或零误删差分、预期节省；
5. 若没有更好路线，明确说明失败原因，并给出最小生产计算批次；
6. 下一步只保留一个最高价值任务和明确的完成标准。

### 建议的返回格式

```text
Fable 接手日期 / revision：
实际读取文件与 hashes：
远程作业是否修改：

VERIFIED：
REPRODUCED：
FINITE-EVIDENCE：
CANDIDATE：
UNKNOWN / GAP：

translated-sumset 审计：
occupied 层审计：
mass-DP / depth-Hall 审计：

更好路线（命题 + soundness + 最小验证）：
若路线失败，失败证据：
唯一推荐下一步：
```

## 7. 停止条件

只有以下情况暂停并报告：需要密码/MFA/CAPTCHA；需要破坏性动作、提交/推送或外部发布；发现工作区写冲突；或远程资源确实不可用且没有安全替代。普通 timeout、缺失顾问回复或一个过滤器不够强，不是停止整个项目的理由；应保存状态并转向另一个可验证的小任务。

## 最新补充：优先审计 parity + Wiener first moment

独立检查器 `theory-lab/s1_crowding/parity_moment_audit.py` 已在 Geo Workstation
通过 order-6 genuine 正控，并对一个 r8 与一个 r9 translated witness 做了直接
BFS 交叉核对。r8 witness 同时违反奇偶计数和第一矩；r9 witness 通过奇偶计数但
违反第一矩。它们只排除这两个具体 `(structure,s,L)`，不构成全域结论。

接手后的最高价值小任务是：在冻结的真实 structure corpus 上，把 parity 与第一矩
作为低成本 presolver 接入 bounded DFS，先做 zero-false-reject differential；不要
先放大 translated node limit，也不要把 `NODE_LIMIT` 当完整排除。
