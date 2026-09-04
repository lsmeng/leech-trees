# Pro 顾问建议：`J` 单边 `32` 的低支撑闭合义务

## 顾问输出

在当前 `b=27` 的 `VERIFIED_FRONTIER` 下，GPT Pro 将下一步收窄为一个
**完整穿孔低前缀**的有限义务，而不是继续只试若干方便的 owner：

```text
H37 = {5,16,18,19,20,21,24,25,26,32,34,35,36,37}
```

若 `32` 的 owner 是 `J` 中的单边，则应枚举十四个 `H37` owner paths
的最小加权森林 `F`，同时满足：

1. 每个 `H37` 值有且只有一个实际 owner pair；
2. `F` 中所有不超过 `37` 的 pair distance 恰为固定 `L` 前缀、
   `H37` 与唯一穿孔值 `4` 的补集；
3. 所有 pair distances 无重复、没有距离 `4`，新 edge weights 互异；
4. `J` edge weights 避开固定 `L` rooted-depth difference set
   `Delta(B0)`，且 `J` 中总长不超过 `37` 的连续路径避开
   `S0 union {4}`；
5. `5` 的 `L` owner 是单边，`21` 的 `L` owner 是 `(21)` 或复用
   `5` 后接一个 `16`（两种方向）。

所有 owner paths 的总长不超过 `37`，所以其新 edge weight 也不超过
`37`；通过大于 `37` 的 gateway 接入的远端部分不会改变低前缀。顾问
建议至少用一个加权树枚举器和一个 SAT/CP 编码独立复核：零模型才可
提升为 `J-32` 的有限排除；有模型则必须输出完整 owner endpoints、edge
weights、低距离表和固定 pair reuse witness。

## 独立审计边界

目前已核对 `H37` 与仓库中的固定前缀一致，且“低 owner path 不会经过
大于 `37` 的 edge”这一有限化理由成立。但这仍不是 `VERIFIED` 定理：
尚未完成森林枚举，尤其没有覆盖任意远端 `L` attachment gate、`34--37`
在 `L/J` 之间的全部分配，以及一个独立的 SAT/CP 复核。

已建立的控制脚本
`theory-lab/topwindow/verify_pro_b27_j32_isolated_l521_minimal.py` 只做
顾问建议的一个窄化模型（`34` 固定在 `b2`、`5` 从 `b2` 远接、六个孤立
`t` 行、三种 `J-32` gate）。它的默认全枚举比短检查大，已停止本地运行，
避免增加工作机负载；脚本保留给 Hoffman2 的低优先级运行。该停止本身不
产生 `NONE` 或非存在性结论。

## 当前推荐的远端步骤

在 Hoffman2 有可用节点时，先只运行这个窄化模型并保存完整计数；若结果
为零，再将同一低前缀义务改写成独立的 CP-SAT/树枚举双实现。Geo
Workstation 当前负载过高，不应再投递新的搜索。

## 第二轮 adversarial 审计

随后要求 Pro 审计这个有限化本身。它的结论是：`H37` 森林是必要条件，
但尚不能直接作为充分封闭。真正缺少的不是更多 owner shape，而是每个
low-support component 的 attachment port。建议的最小 canonical state 为

```text
(L0, F, pi, rho)
```

其中 `L0` 是完整固定 core 的实际图，`F` 是所有新边权不超过 37 的
support forest，`pi` 记录每个 component 的固定顶点或已证明完备的
attachment cell，`rho` 记录 J-component 指向 carrier/root 的方向。LCA
由真实树拓扑自动决定，无需另存；但若只保留抽象 owner graph，就会漏掉
fixed-pair collision、cross distance 和 rooted provenance。

为防止把该义务误当成充分条件，
`theory-lab/topwindow/verify_pro_b27_h37_abstract_port_gap.py` 给出了一个
抽象 witness：固定 `L` core 外，再用 13 个独立的 L 低边承载
`{5,16,18,19,20,21,24,25,26,34,35,36,37}`，用一个独立 J 边承载
`32`。低前缀恰好覆盖 `S0 union H37` 且没有 `4` 或低距离重复；这些
component 之间的连接被有意留作未建模的 `>37` gateway。它不是连通树，
但证明了“没有 attachment-port 条件的 H37 枚举”必然会留下抽象 survivor。

Pro 给出的安全计数是：新 edge 至多 `|H37|=14` 条；若 component 数为
`C<=14`，则新顶点满足 `V_new=E+C<=28`。同时必须检查所有 pair，而不
只是检查新 edge weight 是否落在固定谱之外。

这部分已独立固化为
`theory-lab/topwindow/verify_pro_b27_h37_support_bound.py`，运行状态为
`VERIFIED_LEMMA`。它只验证集合、边/顶点上界和 `>37` gateway 隔离，
没有把 attachment-port 完备性偷偷当成已证事实。

这也修正了本文件上一节的措辞：通过 `>37` edge 接入的部分不会改变
`<=37` 的内部距离，这个隔离事实成立；但若不先证明允许的 attachment
port 集合完备，独立低组件可能产生平凡的低前缀模型。因而 H37 枚举的
`survivors=[]` 才能推出 J-32 排除；出现任何 survivor 时，只能把它当作
pressure control，并继续做 cross-translate、cap 和 inherited-descent
审计。

## 第三轮 Pro 建议：port-complete 状态（2026-08-28）

在抽象断开 survivor 之后，Pro 将最小状态进一步指定为

```text
(T_C, p(C), sigma(C), H(C))
```

其中 `T_C` 是一个 low-support component 的内部加权树，`p(C)` 是它朝
固定 core 的唯一 attachment port，`sigma(C)` 是 `L/J` carrier，`H(C)`
是该 port 的全局 `d6` 深度；component 内部的 LCA 由
`(T_C,p(C))` 的真实拓扑自动决定。这个状态比仅记录 owner paths 更强，
因为它保留了 cross-translate 和 fixed-pair reuse 所需的端口信息。

Pro 还提出候选深度上界：若 `E_C=max_x d(p(C),x)`，则在 J-side 情形
应有

```text
H(C) + E_C + 28 <= N,
```

从而 `38 <= H(C) <= N-28-E_C`。目前只能确认固定 L rooted-depth
集合为 `{0,6,13,14,15,23,27,28}`，所以其最大值 `28` 已由
`verify_exact_return_33_g7_r2_t4_b27_endpoint_depth_floor.py` 的
`VERIFIED` replay 间接固定；**上述含 `N` 的不等式尚未证明**。它需要
先明确 `N` 的定义、J component 到 `d6` 的路径分解，以及为什么固定
L 深度 `28` 必然进入同一个全局 cap。故当前状态标为
`CANDIDATE_BOUND`，不能用来排除任何 attachment port。

最小的第一 falsification check 是：对每个候选 `(T_C,p(C))` 先计算
`R_p={d(p(C),x)}`，再逐一枚举允许的 `H`，检查
`B0+(H+r)` 是否避开固定 `S0`、已命名 J translates 和彼此重复；若某
port 没有可行 `H` 才能删除该 port。不能先枚举 gateway weight，也不能
把 `H37` 的断开模型当作连通 Leech tree 证据。

该安全审计已固化为
`theory-lab/topwindow/verify_pro_b27_port_depth_candidate.py`。它复核
固定 L 深度包及最大值 `28`，并只输出 `CANDIDATE_BOUND`，明确列出尚未
证明的三项前提；它不是 J-32 排除器。

端口优先的第一版枚举器已写入
`theory-lab/topwindow/scan_pro_b27_j32_port_profiles.py`。它枚举根保持的
小型加权树 profile，再检查每个 `H` 的固定-L/J translate；两条边的本机
smoke test 找到 41 个必要条件 profile、并保留 5 个 witness。这个结果
只能作为 `OBSERVED_PORT_PROFILE_SCAN`，三条及以上边的完整扫描应放到
Hoffman2，不能在当前工作机继续扩展。
对应的低优先级 SLURM 包装器是
`/Users/geoclaw/Documents/claude/projects/leech-trees/scripts/hoffman2_port_profile_slurm.sh`；
Hoffman 登录恢复后再投递，当前不提交。

## Hoffman2 端口 profile 扫描结果（job 98652）

Hoffman2 `login2 -> n1182` 以单 CPU、2 GB、低优先级完成了
`max_edges=3, h_max=220` 的扫描，SLURM 状态为 `COMPLETED`、退出码
`0`、耗时约 6 秒。结果为 1 个、40 个、952 个（按边数 1/2/3）的
合格 rooted profiles，共 993 个；检查了 `1,090,314` 个 `H` 候选，
其中 `288,144` 个通过当前必要 translate 条件，保留前 1000 个 witness。

结果文件为
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98652.json`
（SHA-256 `b2a2231e051399da3e692e94d0ce94b4214124f9dca75ae539783e92d277cc9b`），
独立审计为
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98652_audit.json`。
这不是 J-32 的存在性证明；它反而证明当前 translate 筛选远不够强，必须
把多个 component 的 H37 覆盖、port 互相作用、complete spectrum 和 cap
一起纳入。

随后补入已命名 J 的全局低值/边权约束 `16,19,35`，以同样参数重跑
Hoffman2 job `98653`（`n1182`，`COMPLETED`，约 3 秒）。合格 profile
降为 533 个（边数 1/2/3 为 1/28/504），`H` 候选降为 `585,234`，但
仍有 `127,629` 个必要条件 survivor；保留前 1000 个 witness。原始结果
和独立审计分别为
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98653.json`
和
`theory-lab/topwindow/results/pro_b27_j32_port_profiles_e3_h220_98653_audit.json`。
因此约束确实收缩了搜索，但尚未触及完整 H37/port/cap 闭合。
