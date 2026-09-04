# Fable 接手包：Leech-tree 主线接手、独立审计与新路线搜索

日期：2026-09-02  
项目：FW319 exact-return-33 / Leech-tree，当前重点为 S1-279 及其后续 `delta` 分支  
项目根目录：`/Users/geoclaw/Documents/claude/projects/leech-trees`

## 0. 给 Fable 的直接任务

从本文件和 `research_state.md` 恢复工作。你不是来复述“已经完成”的，而是要：

1. 对当前主线的数学量词、代码范围、输入输出和证据等级做独立审计；
2. 查清现有有限计算的 source → binary → command → output provenance，尤其是 `delta=281,282,283`；
3. 优先寻找能够替代或显著缩小完整 forest 枚举的 sound 结构性证明；
4. 若新路线不能形成 sound 必要条件或反证，再按远程资源边界推进现有计算，并产出可独立复跑的验收材料。

最终目标仍是证明 Leech-tree 猜想；任何固定 `delta/s/shape` 的零计数只能写成有限范围结论，不能外推成全局证明。

## 1. 只读接手顺序

先不要跑长程序、不要改正式结果、不要提交或推送。按以下顺序只读检查：

1. `research_state.md`；
2. `docs/checkpoint-2026-09-01-s1-top-block-crowding.md`；
3. `docs/handoff-fable-leech-tree-audit-2026-09-01.md`；
4. `docs/s1-component-mass-dp-2026-09-02.md`；
5. `theory-lab/s1_crowding/component_mass_dp.py`；
6. 当前 git 状态、远程 scratch 目录、Hoffman2 作业状态和最近输出。

接手报告必须记录实际读取的 revision/文件哈希；不能只看文件名或聊天摘要。

## 2. 资源与安全边界

- 本地 Mac 为 24 GB 内存，禁止本地枚举、参数扫描、完整 forest、bootstrap 或长时间 Python/C++；本地只做轻量文本、diff、哈希和证明审计。
- 重计算统一放 Geo Workstation 或 Hoffman2；Geo Workstation 连接使用 `DevSpace workstation`。允许根目录以当前 DevSpace 实际授权为准；本轮已明确授权的工作副本是 `/home/geo/codex-work/leech-trees`，另有 `/home2/geo/`、`/media/geo/` 访问。不要因为根目录列表差异而自行迁移或复制 checkout。
- 每台机器最多 4 个并发 worker；长任务使用 `nice -n 15`、明确 `timeout`，开始前查残留，结束后确认没有孤儿进程。
- 不取消、重启或修改已经运行的远程作业；不删除旧证据；不读取、保存或输入密码、cookie、token。
- 正式状态和已有 checkpoint 只追加审计记录；新代码或中间结果放 scratch，避免和其他写入者冲突。

## 3. 当前基线与证据等级

### 3.1 已有的固定范围结果

- `s=154, shape=star`：62/62 参数片完成，`params_with_survivor=0`、`survivor_count=0`。这是该固定分支的 `CERTIFIED FINITE IMPOSSIBLE`，不覆盖 chain 或全局问题。
- `s=154, shape=chain` exact-10：62/62 完成，合法参数 1860，幸存者 5,201,986；这是必要子系统幸存见证，不是完整树存在性结论。
- 独立 C++ replay 的更强 canonical union：555,397 个 signature，SHA-256 为
  `81211a50c710cb3324fea47197fd0524295678dbfe08403e26d41007841567ce`。
  5,201,986 是较弱 exact-10 primary 的 raw survivor count，555,397 是后续更强
  full-21/replay union；两者不是同一对象，不能互作 mismatch 计数。
- FW303 prefilter：392,049 个 compatible rows，且都保留到 `c=14`；50-signature Python/C++ pilot 的 110 个 job keys 七项计数完全一致、survivors=0。pilot 只验证接口，不外推全域。

### 3.2 Top-block crowding 结构性结论

令 `D=L ⊔ [B,A]`，高块大小 `m=24-r`。高高点按 high-LCA 或固定 low-LCA 分类；每个分类的实际距离值域至多 `2m-3`，故全局距离单射必给出

```text
C(m,2) <= (r+1)(2m-3).
```

因此 `r=3,m=21`（`delta=279`）和 `r=4,m=20`（`delta=280`）直接矛盾。审计时不要使用错误的“high-LCA 的 q 由 y+y' 决定”说法；sound 理由是距离值域大小。

### 3.3 暂定而非完全认证的结果

Fable 报告了：

- `delta=281`：24 个 labeled / 9 个 rooted-isomorphism low shapes，depth-free 全部为零；
- `delta=282`：120 个 labeled / 20 个 rooted-isomorphism low shapes，depth-free 全部为零；
- `delta=283`：48 个 rooted shapes，其中 47 个无 depth-free 结构，chain 有 14,730 个 depth-free 结构，depth phase 为零；
- `delta=284`：115 个 shapes 中 7 个有结构，depth phase 正在 Hoffman2；
- `delta=285`：286 个 shapes 中 95 个有结构，depth phase 正在 Hoffman2。

由于 checkpoint 记录的 `abstract_class_search.cpp` 源哈希 `3a7a...` 与当前可见源哈希
`e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c` 不同，且 Hoffman2 `abstract_class_search_v4` binary SHA 为
`8e1297579d67651e0728347325a0812bf9b5680d0fc6e9d380f23dd51e74e17c`，`delta=281..283` 目前只能标为 `FABLE-REPORTED FINITE EVIDENCE / PROVENANCE PENDING`。不能把“两个运行一致”写成“两套独立算法”，除非真的核对了代码和算法独立性。

## 4. 当前远程作业（只读观察）

- Hoffman2 array `115848`：`depth_r8`，64 个 task 仍在运行；当前只见 `.tmp`，无最终 `.txt`。
- Hoffman2 array `115912`：`depth_r9`，36 个 task 运行、1 个 pending（其余受 QOS 限制）；当前只见 `.tmp`，无最终 `.txt`。
- `depth_r7chain` 已完成 64/64，`leaves=14730`、`depth_survivors=0`，汇总 SHA 为
  `b1bce6b547ac84acf94aaa63a901f51472ea06569e82f32d8dac54e62de18c97`。
- Geo Workstation 上的 component-mass DP `m=16` 原始未压缩单形状探针已按单进程、`nice -n 15`、`timeout 600` 退出 `RC=124`；这是性能 `UNKNOWN`，不是数学排除。压缩实现的同形状探针已完成（见第 11 节），不要重复启动旧探针，也不要删除其 `.tmp`、`.time` 或状态码。

## 5. 首要审计问题

### A. 数学量词与 top-block 证明

1. 重写并核对 high-LCA / low-LCA 的完整分区，确保每一对 high vertices 恰好归入一类；
2. 明确 `m=24-r`、`D=L ⊔ [B,A]`、`B=delta+1-s` 等定义的适用范围；
3. 检查 singleton final-cap、低树连通性和 LCA 分类是否已由前置引理真正保证；
4. 找出任何把必要条件误写成充分条件、把有限范围外推成全局结论的地方。

### B. 代码与 provenance

1. 搜索 `_s154`、`abstract_class_search_v4` 和 depth checker 中残留的 `s=152`、`B=128`、`d2<128`、`c<=13`；
2. 检查 Class B/C 的 fixed LH/LL edges 是否重复安装，root set 是否恰为 `c`，high partition 是否两两不交；
3. 为每次接受的运行保存 exact source hash、compiler/build 命令、binary hash、输入 hash、完整命令行、退出码、output hash；
4. 区分“同一代码重复运行”“独立实现 replay”“独立数学检查器”，不要混用术语。

## 6. 必须优先评估的更好路线

### 6.1 Component-mass DP（当前首选）

对 low vertex `v`，令直接挂在 `v` 上的 high components 大小为 `n[v,j]`，low 子树中的 high 总质量为 `M_v`，`C0=2m-3`。必须有

```text
W   = sum_{v,j} C(n[v,j],2) <= C0
P_v = C(M_v,2) - sum_{u child v} C(M_u,2) - sum_j C(n[v,j],2) <= C0
W + sum_v P_v = C(m,2)
```

这只是 sound 必要条件过滤器，不是完整求解器。脚本和公式见 `theory-lab/s1_crowding/component_mass_dp.py` 与 `docs/s1-component-mass-dp-2026-09-02.md`。Geo Workstation 的小规模 smoke test 已验证：`m=5, lowpar=-1,0,1` 时 108 个质量模式、73 个通过必要条件，独立方程检查 73/73。

要求 Fable：

- 先审计公式和枚举量词，再检查当前 `m=16,r=8` 探针；
- 若扩展，只能在 Geo Workstation/Hoffman2 运行，并保存被过滤模式的 `lowpar`、质量分拆、`W`、全部 `P_v` 和阈值；
- 用小规模 relaxed-target 或独立实现做差分，证明不误删已知可行结构；
- 统计它对 `delta=284,285` 的预期 workload 缩减；若缩减很小，立即回退到现有 depth checker。

### 6.2 Depth interval / Hall 传播

在质量过滤后评估

```text
l_i >= ceil((delta + 2 - 2s + M_i^sum)/2)
```

并检查 root-class 对 `s` 的下界、颜色容量和区间 Hall 不可行性。必须给出完整的必要性证明和小规模差分验证；不能假定存在安全的 `delta` 单调递推（目前没有）。

### 6.3 分层或组合替代

可评估但不可直接当结论：

- 先按总 component 数、`(m,c,W,P-vector)` 分层，寻找容量反证。旧 FW303 的
  Class A/B/C 是 `delta=279` 特定 core/embedding 下的分类，不能未经重新推导
  直接套到 `delta=284,285`；若要重用，必须另证新的 gate/class interface；
- 把 root-coloring、边拥有者和容量约束改写成精确覆盖/小型整数规划或生成函数；
- 找跨-signature 不变量，避免逐一跑 555,397 个完整 forest。

任何新路线都必须写出：形式化必要条件、soundness 证明、独立小例验证、预计节省、失败时的回退方案。

## 7.1 顾问补充：把质量需求直接接到 depth-Hall

对一个已通过 mass DP 的模式，先用 `P_v` 而不是泛化的 class 最大 sum 做
更便宜的下界：根节点必须有 `P_0` 个不同正整数 sums，故

```text
s >= ceil((delta + 2 + P_0) / 2)
LB_v(s) = max(1, ceil((delta + 2 - 2s + P_v) / 2))
```

沿 low-tree 的 parent 顺序传播 `E_v=max(LB_v,E_parent+1)`，再检查
`[E_v,B-1]` 是否能给非根 low vertices 分配互异槽位。Hall 失败是严格的
必要性排除；Hall 通过不代表存在。下一次 pilot 应先在已验证小例上做这个
`P_v→depth-Hall` 差分，再考虑 global distance-slot flow；不要先增加
high-parent DFS 的复杂度。

## 8. 建议的执行顺序

1. 只读审计当前文件、作业和 provenance；
2. 等待并核对正在运行的 `delta=284,285` 输出，不重复提交；
3. 完成 component-mass DP 代码审计和远程探针验收；
4. 对一个 structure-bearing shape 做“质量过滤 → depth checker”的小片差分；
5. 只有过滤器 sound 且确有实质缩减时，才提交最多 4-worker 的远程批次；
6. 每个里程碑追加 checkpoint，明确 `VERIFIED / REPRODUCED / FINITE-EVIDENCE / CANDIDATE / UNKNOWN / GAP`；
7. 在正式接受任何零结果前，先完成 provenance 闭合和独立复跑。

## 9. Fable 返回格式（简短但可审计）

```text
接手日期：
实际 revision / source hashes：
读取文件：
当前运行与是否修改：

VERIFIED：
REPRODUCED：
FINITE-EVIDENCE：
CANDIDATE：
UNKNOWN / GAP：

量词或实现问题：
更好路线：形式化必要条件 + soundness + 小例验证 + 预计节省
对 delta=284/285 的建议：继续 / 缩片 / 暂停 / 改路线
实际修改文件：
实际命令与退出码：
独立验证命令与结果：
仍未闭合的最小命题：
下一步：
```

## 10. 绝对停止条件

只有遇到真实凭据/MFA/CAPTCHA、破坏性或不可逆动作、公开发布/提交推送、缺少无法推断的实质决定，或所有安全路径都无法继续时才停下来询问。若用户说“暂停/停下来”，立即停止新消息、计算、编辑和重试，只保存状态。

## 11. 最新增量（2026-09-02）

旧的完整 local-partition 探针在 Geo Workstation 上对
`lowpar=-1,0,0,1,3,4,5,6`、`m=16` 按 `nice -n 15 timeout 600` 退出，
`RC=124`；该结果仅为算法性能 `UNKNOWN`，绝不是 zero-survivor 结论。

为此新增压缩实现
`theory-lab/s1_crowding/component_mass_dp_compressed.py`。它把局部整数分拆
按 `(a,w)` 合并，并在每个 low 子树只保留 `(M,W)` 状态；Geo Workstation
同一形状 `m=16` 的压缩探针以 `RC=0`、`0.08s`、`MAXRSS=12568 KB`
完成，根节点 `W=0..29` 全可达，`root_possible=true`。这说明必要条件层
可快速执行，但没有排除该形状，也不构成存在性证据。

远程/本地脚本 SHA-256：
`7ed764d97ff45e9eca16e79c48d2d6328f32c3cc99c35a3b58f902587473d162`。
远程压缩 summary SHA-256：
`46a13ff99aa4ae32d1613374c86b598ca0fc1e9ac80820234cc29a257cc63766`。

Fable 接手时应先做一个独立 relaxed-target 差分，确认压缩状态不会误删
已知可行的小例；若 shape-level 缩减不显著，回退现有 depth checker，
不要直接实现高风险 partial residual 剪枝。Hoffman2 arrays `115848`
（64 RUNNING）和 `115912`（36 RUNNING + 1 PENDING）保持原样，不得重启、
取消或修改。

最新只读观察：`depth_r8` 64 个 `.tmp` 已写出 384 行 `EXHAUSTED`（6 个
lowpar 记录各重复 64 次），中间汇总 `leaves=23332646`、
`depth_survivors=0`；`depth_r9` 36 个 `.tmp` 已写出 216 行 `EXHAUSTED`
（6 个 lowpar 记录各重复 36 次），中间汇总 `leaves=111759`、
`depth_survivors=0`。这些不是最终数组结果：仍有形状未覆盖，文件仍为
`.tmp`，必须等任务收尾并核对完整 coverage 后才能接受。

新增的候选增强层是
`theory-lab/s1_crowding/global_distance_slot_flow_pilot.py`：将 `W/P_v`
需求与放宽的全局 distance slots 做最大流。只有 flow 不足时才可 sound
排除；flow 通过不表示存在。该工具已在 Geo Workstation toy 案例中与
独立回溯匹配对照一致。Fable 应先用小规模 relaxed-target 验证，再决定
是否对实际 `delta=284,285` depth structures 做 post-processing；不要
把它直接当成完整 proof。

压缩 DP 的额外证据：在 Geo Workstation 上用未压缩版本作 oracle，对
`m=4..7,r=1..5` 的全部 136 个 rooted lowpar shapes 做根状态集合差分，
`mismatch_count=0`（`RC=0`，2.38s）。这支持压缩在 root reachable-state
必要判定上的完备性，但它仍丢弃具体 `P_v` 向量；Fable 做 depth/Hall 时
必须保留 witness/profile 或重新展开 mass patterns。

顾问审计补充的 flow 生产门槛：接入必须独立提供完整结构的
`W/P_v/(s,L)/lowpar`，核对 `W+ΣP_v=C(m,2)`，并逐项证明 occupied
槽位确实由不同 pair 占用；重复 occupied 值应报告为上游碰撞，不能静默
集合去重。当前 flow 仍仅为 `LOGIC-AUDITED / CANDIDATE NECESSARY FILTER`。

## 12. 请主动寻找“比当前路线更好”的方案

不要默认继续把 `delta=284,285` 的完整 depth/forest 枚举做大。接手后的第一项实质工作，是对下面路线做一次有结论的比较，并明确指出是否存在更短、更强或更容易认证的路线：

### 路线 A：把 top-block crowding 推到 `r=5,6,...`

尝试在不依赖具体树形的前提下，把 high-LCA / low-LCA 的容量计数、低树连通性、singleton final-cap 和 component 质量约束合并，得到对 `r=5`（`delta=281`）及以后仍有效的统一不等式。若失败，要给出失败的最小反例，而不是只说“计数不够”。

### 路线 B：`(W,P_v)` 直接接深度与 Hall

对每个 low-tree shape 和每个质量 profile，保留可追溯的 `P_v` witness；先用

```text
s >= ceil((delta + 2 + P_0)/2)
LB_v(s) = max(1, ceil((delta + 2 - 2s + P_v)/2))
```

做 parent-order 传播和区间 Hall。必须报告：过滤掉多少 shape/profile、是否误删小例、与现有 depth checker 相比节省多少。Hall 通过只能记为“未排除”，不能记为存在。

### 路线 C：全局 distance-slot / matching / ILP

把高高 pair 的距离槽、low-LCA 类和 occupied slots 组成精确的 matching/flow/ILP。先证明这是原问题的 sound 必要松弛，再用小规模完整回溯做 differential test。若能产生 unsat core 或可读的容量证书，优先把它整理成数学引理；若只能得到 flow pass，就不要把它包装成证明。

### 路线 D：压缩与跨 signature 不变量

尝试按 `(m,c,W,P-vector,lowpar)` 或更强的 occupancy profile 合并 555,397 个 canonical signatures，寻找对所有 signature 同时成立的容量/奇偶/距离和不变量。任何复用旧 FW303 Class A/B/C 的做法，都必须重新证明它适用于 `delta=284,285`；不能把旧分类名称当作新定理。

### 路线 E：有限结果到全局结果的桥

可以研究 `delta` 单调性、递推或嵌入，但必须先写出完整的映射（树、标签、距离槽和 root condition 逐项保持），并给出反例搜索。当前没有已接受的安全单调递推；在证明前一律标 `OPEN`。

## 13. 更好路线的统一验收门槛

Fable 选择任何新路线，都必须返回以下五件东西：

1. **形式化命题**：明确量词、输入域、必要/充分方向和适用的 `delta,s,r,m` 范围；
2. **soundness 证明**：说明为什么不会排除真实解，并指出所有使用到的前置引理；
3. **最小独立小例**：在 `m<=7` 的全部 rooted lowpar shapes（或同等覆盖）上，与旧枚举/独立回溯逐项比对；
4. **实际收益**：对 `delta=284,285` 给出 shape、profile、节点或运行时间的前后数量，不能只给“应该更快”；
5. **失败回退**：如果收益不显著或 soundness 无法闭合，明确回退到哪个现有脚本和远程作业，不擅自扩大计算。

优先级判断规则：

- 能产出跨 shape 的数学反证或可读容量证书的路线，优先级最高；
- 只有必要过滤、但能把 workload 降低至少一个数量级的路线，才值得提交新的远程批次；
- 只减少常数、不能改善证明量词或 provenance 的改动，暂不做；
- 任何新脚本先放 scratch，先做小例 differential，再申请最多 4-worker 的远程运行。

## 14. 交接时请特别回答的三个问题

1. 当前最早未闭合的**数学**缺口到底是哪一个（不是“程序还没跑完”）？
2. 在不依赖完整 forest 枚举的情况下，你认为最有希望的单一新思路是什么？请给出一页以内的推导或反例；
3. 如果继续计算，为什么它比路线 A--D 更值得，预计何时能产生可审计的 `VERIFIED` 或 `FINITE-EVIDENCE` 结果？

没有这三个回答，不要启动新的大批次，也不要把中间 `.tmp` 或 flow/Hall 通过误写成证明。

## 15. 最新顾问结果：联合区间 Hall（2026-09-02）

`CONSULT-20260902-009` 的只读审查给出了一个比逐点 `P_v` 下界更强的候选层。
固定合法 `(s,L)` 后，令 `C0=2m-3`、`B=delta+1-s`，则 high-LCA 类的距离
落在 `[1,C0]`，low-LCA 类 `v` 的距离落在

```text
I_v = [2B-2*l_v+1, 2B-2*l_v+C0] ∩ [1,delta].
```

对任意 class 子集 `Q`，真实距离单射必然给出

```text
sum(demand_i for i in Q) <= |union(I_i for i in Q) minus occupied|.
```

违反它即可 sound 排除；通过仍不是存在性证明。顾问同时给出 `r=5,m=19,C0=35`
的质量 counterprofile：low-chain 上直接质量为
`(1,1),(1,1),(1,1),(1,1),(7,1,1,1,1)`，得到
`M=(19,17,15,13,11)`、`W=21`、`P=(35,31,27,23,34)`，说明单纯总容量
路线在 `r=5` 已经不够强。

为验证实现，新增：

- `theory-lab/s1_crowding/joint_interval_hall_pilot.py`
- `theory-lab/s1_crowding/joint_interval_hall_differential.py`

Geo Workstation scratch 运行 `nice -n 15 timeout 120`，对 `m=5,delta=10`
的 chain3、star3、branch4 做逐槽位回溯 matching differential，结果分别为
`151/91/0`、`188/132/0`、`184/120/0`（格式为
`exact_depth_assignments / hall_rejects / matching_mismatches`），总计
`matching_mismatches=0`、`soundness_ok=true`、`RC=0`。脚本哈希为
`f2fd8e642707df5f3549505b6cc3839316ffdba30944128037554306df9b8c1f`，差分脚本
哈希为 `abbb102a09219758d6afef6511c5de738bcd57e8688493fc94e8f58db4072109`，
结果哈希为 `d33c718a721ccc266c39572d2030a108b61cf156cf181af7052b1e1cfa6cac9f`。

注意：一版早期对照把“depth-only 可行”误当成完整解，出现的 false-reject 计数
已作废，不能引用。Fable 下一步应把联合 Hall 接到真实完整 `(structure,s,L)`
记录上，量化它对 `delta=284,285` 的排除率；在此之前不要把它称为 production
verified，也不要重启现有 Hoffman2 arrays。

## 16. 最新独立顾问审计（CONSULT-20260902-010）

普通 Chat 顾问对联合区间 Hall 的实现和差分脚本做了只读复核，结论如下：

- **公式 soundness：VERIFIED。** 对固定 `(m,delta,s,L)`，high 类使用
  `[1,C0]`，low 类使用
  `[2B-2l_v+1,2B-2l_v+C0]∩[1,delta]`；任意 class 子集的需求总数超过
  区间并集容量时，必然违反距离单射，因此可以安全排除。
- **按 class 检查足够。** 同一 class 的 demand copies 具有相同邻域，故不必
  再拆成 individual pair clones。
- **clipping sound；occupied 有条件 sound。** `[1,delta]` 裁剪不会误删真实
  距离；只有在 occupied 值已经由其它不同 unordered pairs 确定占用时才能删除，
  重复 occupied 必须作为上游碰撞拒绝，不能静默 `set()` 去重。
- **小例差分：VERIFIED（仅对测试域）。** 独立逐槽位回溯 matching 与 Hall
  逐例一致：chain3 `151/91/0`、star3 `188/132/0`、branch4 `184/120/0`，
  `matching_mismatches=0`、`soundness_ok=true`、远程 `RC=0`。
- **生产接入：GAP。** 尚未对真实 order-9 或 `delta=284,285` 完整
  `(structure,s,L)` survivor 做 zero-false-reject differential；因此当前等级仍是
  `LOGIC-AUDITED + SMALL EXACT MATCHING DIFFERENTIAL`，不是 production verified。

顾问还指出，比区间 Hall 更强的下一条路线是从完整 abstract structure 中直接取
`within_vals=H` 与 `class_sums[v]=S_v`，检查精确平移集合
`T_v=2B-2l_v+S_v` 的落界、两两不交以及避开 `H`。其中
`2(l_i-l_j) notin S_i-S_j` 是 low-class 的精确深度差禁止条件；这仍只覆盖
high-high subsystem，必须把 LL/LH/holes 单独纳入后才能用于完整树。

**因此给 Fable 的优先级：**

1. 先对 genuine relaxed survivor 做 `occupied=()` 的零误删差分；
2. 再在不触碰现有 Hoffman2 arrays 的前提下，对少量已冻结的 `delta=284/285`
   完整结构做只读 post-processing，统计实际排除率；
3. 若精确 translated-sumset CSP 能减少至少一个数量级，再考虑实现生产层；否则
   回退现有 depth checker，不扩大远程批次。

本轮顾问依赖哈希：

```text
joint_interval_hall_pilot.py        f2fd8e642707df5f3549505b6cc3839316ffdba30944128037554306df9b8c1f
joint_interval_hall_differential.py abbb102a09219758d6afef6511c5de738bcd57e8688493fc94e8f58db4072109
differential_v2.json                d33c718a721ccc266c39572d2030a108b61cf156cf181af7052b1e1cfa6cac9f
```

## 17. 新增远程正向控制：STRUCT → H/S 重建（2026-09-02）

为验证 translated-sumset 路线的输入链条，而不是直接假定 `STRUCT` 已包含
`within_vals/class_sums`，在 Geo Workstation 上对已有 r7 chain 结构做了一个
单进程、`nice -n 15`、`timeout 120` 的正向控制：

```text
binary: abstract_class_search_v4
input:  --m 17 --lowpar 0,1,2,3,4,5 --xcap 1000 --stop-first --emit
STRUCT: -1 -2 -3 -4 -5 -6 -7 -7 6 6 6 -6 -5 -4 -3 -2 -1
delta:  283
source SHA-256: e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c
binary SHA-256: 38e3c2a5c0d58864809056699e84176d461ba4a70ba5ad141e52ca173cd9ebad
```

独立 Python post-processor 从 `lowpar + hpar` 重建 high forest、high LCA、
`H=within_vals` 和 `S_v=class_sums[v]`，然后只检查 exact high-high translated
sets。结果：`RC=0`，`tested_s=158`，在 `node-limit=500000` 时得到
`high_high_passes=474290`，最后状态为 `NODE_LIMIT`（不是完整 census）。这证明
重建链路能处理真实 `STRUCT` 输出，并明确显示该层在 r7 positive control 上仍然
大量通过，不能单独关闭问题。

产物及哈希（均在 `remote_scratch/translated_sumset_positive_control_20260902/`）：

```text
translated_sumset_csp_pilot.py   0b1e700038d8aaa91c9a81149ab8c0b3702bd65b6d47231ff7abb54cb38dbf61
struct_r7_chain.txt              4f59c070ed78bb3b2fe7d467f811ab25b98d80a1b6626c52d4b0fc0f839a449d
translated_sumset_result_v2.json c7d91c53d909000257ff8a290e5a2029c6c7b64633c0c8a27e17587005c569c7
translated_sumset_run_v2.stderr 5962f3cf8b2dca06f2e382685039396b96ad5a8ab5d51ec4341de966ae77c845
```

证据等级：`REMOTE REPRODUCED INPUT-RECONSTRUCTION PILOT`；不是 `VERIFIED`
全局排除，也不是存在性证据。Fable 接手时应先把节点上限改成可完成的小例或
固定一个 `s` 做完整差分，并与现有 C++ 的 `DEPTH_SURVIVOR`/拒绝结果对照；
若没有真实 `delta=284/285` 的完整 `STRUCT` 输出，必须明确标记
`GAP: production translated-sumset integration`。

随后在同一 Geo Workstation 结构上固定 `s=158`，用现有 C++ checker 做了独立
对照（同样 `nice -n 15`、`timeout 120`）：`RC=0`、`leaves=1`、
`depth_survivors=0`、`csp_nodes=24`。这与 translated-sumset 层在节点上限前
已有大量 `high_high_passes` 的结果相符：新层只是较早的必要过滤，仍会把大量
候选交给 LL/LH/holes 检查；该对照不是“两个独立完整算法”，不能扩大成全局
零计数结论。

对照产物：

```text
cpp_fixs158.txt    04ffe728009db725909bc5a554ea9300d5d858c5312dcdc0686f8ff63c32b8d2
cpp_fixs158.stderr e321fd66e43908c3ec255c752ac518d47c383da51140731add2e65b0adc7930d
```

## 18. Genuine positive control：order-6

为做真正的零误删控制，在 Geo Workstation 上运行了极小的
`m=4,r=1,order=6,delta=11` 搜索（单进程、`nice -n 15`、`timeout 30`）。
现有 C++ checker 返回 `RC=0`，`leaves=9`，并产生 genuine
`DEPTH_SURVIVOR s=8, L=0, hpar=-1,-1,1,1`。

独立 post-processor 对该 survivor 完整枚举 `s=1..11`，得到
`H=[1,2,3]`、`S_0=[1,2,3]`、`high_high_passes=3`、`status=COMPLETE`，并保留
`s=8,L=[0]` witness。这是目前第一条 genuine-positive-control：重建和
translated-sumset 层没有误删已知 C++ survivor；它只验证小例接口，不覆盖
`delta=284/285`。

产物哈希：

```text
order6_genuine.txt             ac530b6a13d7c718a3f26da6f8b30eab0f01c9d564614447905658d95365b270
order6_genuine.stderr          ac148848dd5934439bb7dabf6eae3bce3ec40974ded29a3d32a9d64386347ab6
order6_translated_result_v3.json 66beae67306c3f993f2424f5eb5ac85b9d62013439716398d6255d8efeb7c83a
order6_translated_v3.stderr       7df576a0964a5d85c4251642a04b3d709cf6a65522c42b6684d1c38fbba512ea
```

该 v3 结果还通过统一加权树的 BFS 逐对距离核对：`bfs_check.ok=true`、
`pair_count=6`，重建的 H/S 与 BFS 归一化结果完全相同。因而小例接口可标为
`SMALL-EXACT-DIFFERENTIAL`；生产 `delta=284/285` 接入仍是 GAP。

补充复跑（同一 r7 结构，脚本加入 BFS 后）：`RC=0`、`bfs_check.ok=true`、
`pair_count=136`、`high_high_passes=474290`、`status=NODE_LIMIT`。结果文件
`translated_sumset_result_v3.json` 的 SHA-256 为
`12df3fb35bcca3bb59aac89015d0bd9e329fa967f9d738e347294349572c3c6a`，计时/错误
文件 `translated_sumset_run_v3.stderr` 的 SHA-256 为
`fab979ad8e4eb9bce2773eb8e18f6daa30bffa0ee75b5b1fc1a53a44ee046680`；脚本当前
SHA-256 为 `0b1e700038d8aaa91c9a81149ab8c0b3702bd65b6d47231ff7abb54cb38dbf61`。

## 19. 顾问 011 的最终接手建议

顾问确认：从 `lowpar+hpar` 建立统一 rooted tree，再用 generic ancestor-list
LCA，是最小且不易错的 H/S 重建；必须检查 high parent 的“只能指向更早节点”、
负 parent 的 low-root 范围、
`|H|+Σ|S_v|=C(m,2)`、H 和每个 S_v 内部无重复。跨不同 `S_v` 出现相同 raw sum
是允许的，不能误报。

建议 Fable 在正式接入前再执行一次独立 BFS 复核：给 low-low、low-high、
high-high 边赋与当前公式一致的权重，逐 pair 计算距离，并核对它是否恰为
`H` 或 `2B-2l_v+S_v`。order-6 genuine control 已通过该检查；这应成为生产
post-processor 的输入验收门槛。

在真实 `delta=284/285` `STRUCT` 尚不可得时，正式标记应为
`PRODUCTION EFFECTIVENESS GAP — no immutable 284/285 hpar corpus available`，
不能从 `.tmp`、aggregate counters、toy differential 或 r7 单结构推导排除率。
更强的安全增强顺序是：先加 holes，再加固定 `[B,B+m-1]` x-high owners，再加
exact LL；每一层都必须先通过 genuine-positive-control 零误删，避免退化成另一
份未经审计的完整 depth solver。

## 20. occupied 增强层的远程小例

按顾问 011 的建议，post-processor 增加了可选的已知 occupied 集合：固定
x-high 槽位 `[B,B+m-1]` 与 holes `{s+l_v≤delta}`。这些值只在 pair owner
已确定且彼此不同的条件下加入；与 H/S 或彼此碰撞时拒绝，绝不静默去重。

- order-6 genuine survivor（`s=8,L=0`）仍通过：`high_high_passes=1`、
  `occupied_rejects=2`、`bfs_check.ok=true`。这是 occupied 层的零误删控制。
- r7 frozen STRUCT 在 `node-limit=500000` 下有 `occupied_rejects=474290`、
  `high_high_passes=0`，但状态仍为 `NODE_LIMIT`；只能说已访问节点全部被
  occupied 层拒绝，不能说该结构完整搜索为零。

当前实现脚本 SHA-256 为
`c993dec61b6ecd2d5797b4774d9aaacf5487f784319047ab10a2104d88ffc5d3`；结果文件：

```text
order6_translated_occupied.json bf0bfba31315ca618de714ad4c2a4226a3cb8cf7fcf9be1775310a1f2667f980
r7_translated_occupied.json     fd58e739a51e5f285c68d6d35be899135b4f18e0427cc58b6f29414063f02156
```

该层仍属于 `SMALL-EXACT-DIFFERENTIAL / CANDIDATE NECESSARY FILTER`，尚未接入
真实 `delta=284/285` corpus。

## 23. 首个 delta=285 structure-bearing 单形状控制

对一个已知 r9 shape 做了同样的 Geo Workstation 单进程控制：

```text
lowpar = 0,0,0,0,1,5,6,7
STRUCT = -1 -2 -6 -7 -8 -9 -9 5 5 5 -8 -7 -6 -2 -1
abstract leaves=1, nodes=7687, RC=0
```

独立 H/S+BFS 对全部 `C(15,2)=105` 个 high pairs 给出 `bfs_check.ok=true`。
普通 translated-sumset 层在 500000 节点上限内得到
`high_high_passes=481494`、`status=NODE_LIMIT`；加入 occupied 后得到
`occupied_rejects=481471`、`high_high_passes=23`、
`xhigh_out_of_range_rejects=14`，仍是 `NODE_LIMIT`。这是真实 `delta=285`
结构输入的可复现剪枝测量，但不是该 shape 的完整排除。

产物哈希：

```text
struct.txt               bd6186f7b9afa58818e5aa3f0434ae9119399670758a0c3b7ca84268d935f0d5
translated.json          ba85cd3a12df17dfa63d3c5e0b5bf9edd0d0a35fe47edbd3e0460f6d95d85642
translated_occupied.json 9027d6a6be8bd6487a67cc8ce1dc2c7972a610116bc819339a185f3e0913571c
```

## 22. occupied guard 修正与 delta=284 回归

顾问 012 发现 occupied 模式还应显式拒绝超出 `[1,delta]` 的 x-high 槽位，
并单独记录 `xhigh_out_of_range_rejects`。该 guard 已加入脚本；它只增加必要
剪枝，不会造成 false rejection。

回归结果：

- order-6 genuine：`status=COMPLETE`、`high_high_passes=1`、
  `occupied_rejects=2`、`xhigh_out_of_range_rejects=3`、`bfs_check.ok=true`；
- 首个 `delta=284` 单形状：`status=NODE_LIMIT`、访问 500000 节点，
  `occupied_rejects=477145`、`high_high_passes=0`、
  `xhigh_out_of_range_rejects=15`。这仍只是限额前缀证据。

当前脚本 SHA-256：
`a157174be591c65e8cab7d005ed2df871466386042542cb500ce6a3839c02df0`。
order-6 occupied 结果 SHA-256：
`e7a549e164f8e58a7645830db8a43e2852e3a4c5f154f6f0139b66a0601a121e`；
delta-284 occupied 结果 SHA-256：
`e9e820776bf5864240d5c7db837156ad737c50310da8fd91c3161ddfe2869d28`。

## 21. 首个 delta=284 structure-bearing 单形状控制

为避免只在 r7/toy 上测试，Geo Workstation 又对一个现有 r8
(`delta=284,m=16,r=8`) structure-bearing shape 做了单形状、单进程
`nice -n 15 timeout 120` 运行：

```text
lowpar = 0,0,1,3,4,5,6
STRUCT = -1 -2 -4 -5 -6 -7 -8 -8 -8 6 -7 -6 -5 -4 -2 -1
abstract leaves=1, nodes=12346, RC=0
```

独立 H/S+BFS 重建对全部 `C(16,2)=120` 个 high pairs 校验 `bfs_check.ok=true`。
未加入 occupied 时，在 500000 节点上限内有 `high_high_passes=477145`；加入
holes 与固定 x-high 槽位后，访问节点中的 `occupied_rejects=477145`、
`high_high_passes=0`，但两个结果都为 `NODE_LIMIT`，所以不能称该 shape 已完整
排除。它证明了新层已经能处理真实 `delta=284` 的结构输入，并量化了 occupied
增强的即时剪枝效果；生产结论仍需完整终止和 zero-false-reject differential。

source SHA-256 为 `e72d39e673671f0a7fe6a9a66986d3075277a9dd4e7e6ce2a4d7e63d53ab987c`，
Geo binary SHA-256 为 `38e3c2a5c0d58864809056699e84176d461ba4a70ba5ad141e52ca173cd9ebad`。
产物哈希：

```text
struct.txt               0c7541bb1dadd9f40a9d7064cd158044b5c84b1097fc934c36537b7b453fcf7d
translated.json          c0cc7172378d19165fed665d880f20527ef445ffa5b99562dc06b0587702087b
translated_occupied.json 83523c618649c5e9dfb23d07d03b82910c691492bd60b30772c1bb6c520f0afa
```

## 24. early-prune 修订后的最新远程观测（2026-09-02）

当前本地与 Geo Workstation 应使用的 `translated_sumset_csp_pilot.py` SHA-256 为
`005f506ac32fa77d2aa7da37a60c37fbb6c637802b281ca010f75aad81acfac8`。本版本把
known occupied 的碰撞和 x-high 越界检查提前到 DFS 层；因此新版计数应看
`occupied_prune_rejects`，不能与旧版 `occupied_rejects` 直接比较。
Geo scratch 中实际用于回归的副本
`remote_scratch/translated_sumset_positive_control_20260902/translated_sumset_csp_pilot.py`
也核对为同一 SHA；正式 checkout 根目录下没有该脚本的独立副本，后续远程运行必须
把脚本副本和 hash 一起记录。

对同一个真实 `delta=284,m=16,r=8` structure-bearing shape 的 Geo Workstation
回归结果如下：

```text
status=NODE_LIMIT
nodes=500001
tested_s=159
occupied_prune_rejects=5332120
occupied_rejects=0
high_high_passes=17201
xhigh_out_of_range_rejects=15
bfs_check.ok=true
pair_count=120
result SHA-256=13972f40ba78216367c3389e0d3e9723def965acafbb2611360334c9ff594502
```

这是“前缀内的必要条件剪枝测量”，不是该 shape 的完整排除；`NODE_LIMIT` 仍是
`UNKNOWN/GAP`。BFS 只说明已经产生的 witness 的 H/S 距离重建自洽。

同一批次的 `delta=285,m=15,r=9` occupied-v3 输出文件为空，不能读取任何统计，
记为 `OUTPUT_MISSING/TIMEOUT`，不把它写成零结果，也不因该空文件重启批次。
Hoffman2 arrays `115848/115912/115949/115950` 的只读状态未改变。

因此当前 production 缺口仍然是：完整且不可变的 `delta=284/285` structure/depth
corpus、可复跑 provenance，以及针对真实 survivor 的 zero-false-reject differential。

## 25. 可选 exact low-low 剪枝（2026-09-02）

在不改变默认 high-high/occupied 行为的前提下，post-processor 新增
`--include-low-low` 选项。对 DFS 每次新加入的低深度 `l_i`，它计算与所有已加入
低点的真实距离 `l_i+l_j-2l_lca(i,j)`；若该距离越界、撞上已有 H/T/occupied 值，
或与本次新生成的 low-low 距离重复，就立即拒绝该分支。这是“距离单射”的直接
必要条件，默认关闭，尚未宣称 production 过滤收益。

当前脚本 SHA-256 已变为
`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`；仅完成无副作用
语法检查，尚未在 Geo Workstation 运行 genuine control。接手者的最小验收是：先将
同一脚本副本复制到 Geo scratch，以该 SHA 在 order-6 genuine control 上运行
`--include-low-low`，必须保留已知 witness 且 `bfs_check.ok=true`，否则撤回该层。

## 26. exact low-low genuine-control 回归（2026-09-02）

已按上述门槛在 Geo Workstation 完成单进程回归；没有在本机运行枚举，也未触碰
Hoffman2 arrays。远程命令为：

```text
nice -n 15 timeout 30 python3 translated_sumset_csp_pilot.py \
  --delta 11 --lowpar= --struct=-1,-1,1,1 --node-limit 100000 \
  --include-known-occupied --include-low-low
```

脚本 SHA-256：`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`。
输出 `result.json` SHA-256：
`1a206bcfc3814fe13e1d0224e353dc8cd809feed7231f5907df7f905c2c387cb`。
结果为 `RC=0,status=COMPLETE,nodes=1,tested_s=11,high_high_passes=1`，已知
`s=8,L=0` witness 保留；`low_low_prune_rejects=0`、
`occupied_prune_rejects=2`、`xhigh_out_of_range_rejects=3`，且
`bfs_check.ok=true,pair_count=6`。这是 `VERIFIED GENUINE POSITIVE CONTROL /
INTERFACE CHECK`，不能外推为 284/285 的生产收益或全局证明。

## 27. low-low 双低点人工接口控制（2026-09-02）

由于 order-6 genuine control 只有一个 low 点，另做了一个极小的双 low 点
人工可行接口控制，以确保新代码确实执行了 low-low 距离计算。Geo Workstation
单进程命令为：

```text
nice -n 15 timeout 30 python3 translated_sumset_csp_pilot.py \
  --delta 10 --lowpar=0 --struct=-1,-1,-2 --node-limit 100000 \
  --include-known-occupied --include-low-low
```

脚本 SHA-256 仍为
`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`；
`result.json` SHA-256 为
`2e2d6a07bbd837e2ca9b35f8cd2741cee440ed8b4a2b6e2d7b0dd045e7eeb5e2`。
结果 `RC=0,status=COMPLETE,nodes=2,tested_s=9,high_high_passes=1`，保留
`witnesses=[{s:9,L:[0,1]}]`；`low_low_prune_rejects=0` 且
`bfs_check.ok=true,pair_count=3`。这是人工接口正控（不是 Leech-tree 全局
结论），说明 low-low 层在实际产生一个 low-low pair 时没有误删。

## 28. low-low 负向碰撞控制（2026-09-02）

为验证新层确实会拒绝 low-low 重复距离，Geo Workstation 又运行了一个极小的
三 low 点路径控制（不含 known occupied）：

```text
nice -n 15 timeout 30 python3 translated_sumset_csp_pilot.py \
  --delta 10 --lowpar=0,1 --struct=-1 --node-limit 100000 \
  --include-low-low
```

脚本 SHA-256 为
`f5b91b5f36106d94b79f0d964104717d8e441988f6a93482811636b1667c1b4d`；
`result.json` SHA-256 为
`16a494516c769a9d3acdcbb4b711d73eefc2437fb95d8a5e100ccc2c332a93f3`。
结果 `RC=0,status=COMPLETE,nodes=152,tested_s=8,high_high_passes=100`，
`low_low_prune_rejects=20`，说明重复/冲突的 low-low 分支确实被拒绝；保留的
witness 均通过 `bfs_check.ok=true,pair_count=0`。这是剪枝行为的负向接口控制，
不是关于 Leech-tree 的有限或全局结论。

## 29. parity + Wiener first-moment 三对象远程小批次（2026-09-02）

独立检查器 `theory-lab/s1_crowding/parity_moment_audit.py` 从
`lowpar+hpar+(s,L)` 建立完整加权树，同时计算顶点深度奇偶计数、cut identity
第一矩和直接 BFS 的全 pair 距离和。Geo Workstation 使用的脚本 SHA-256 为
`4233494c26a3504604785c55de7f855e705b5a0b7a33a7cf9e65e633a8ed3d96`。

单进程 `nice -n 15 timeout 120` 结果：

```text
order-6 genuine (delta=11, s=8, L=[0]):
  all_checks_ok=true, cut=direct=target=120, parity_ok=true
  result SHA=5c8fabd00ef2efc449f4fab1761d51831728f7aeab266616fece1422246f2cdd

delta=284 r8 translated witness (s=158, L=[0,18,40,41,51,59,88,92]):
  parity_ok=false (odd_pairs=154 vs target=150)
  cut_identity_ok=true, first moment 47194 != 45150
  result SHA=d50ef4f291e9831cc498e0f398d8086e871257e414d3ba2ea73655f44c271451

delta=285 r9 translated witness (s=157, L=[0,13,1,2,3,24,33,77,101]):
  parity_ok=true (odd_pairs=150), first moment 47064 != 45150
  cut_identity_ok=true
  result SHA=eefefa59e95b0993a24ab3f94b0f23f6cef6ae6041b7a7f7504aefc4ad51272b
```

对 r8/r9 的含义仅是：上述两个具体 `(structure,s,L)` 候选分别被 parity 或
第一矩这个 sound 必要条件拒绝；不能外推到整个 `delta`。生产接入仍需冻结
structure corpus、bounded-DFS 计数及 zero-false-reject differential。

## 30. 当前脚本 hash 更新说明（2026-09-02）

随后仅修正 `translated_sumset_csp_pilot.py` 顶部 docstring，使其不再声称
occupied/low-low 选项被省略；算法逻辑未变。当前脚本 SHA-256 为
`93bca2c36c12baeb2361e78a438cadaf673fd250ca94971d5927d79d5783db2a`。
§25--§28 的历史输出仍对应各自记录的 `f5b91b…` 版本；后续新运行必须记录
新的 source hash，不得混合 provenance。
