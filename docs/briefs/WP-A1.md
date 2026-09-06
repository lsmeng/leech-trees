# WP-A1 — 把两条线性矩方程接进 abstract_class_search 深度阶段（Opus）

背景（够用即可）：n=25 Leech 树，N=300。normal form：删掉锚 a 后的 24 点根树 K，低点 r=9 个深度
L 自由、高点 m=15 个深度固定；引擎按 (split,shape) 枚举低深度并检查 276 个距离互异。
对任何正整数权树、任选根 o、σ_v=(−1)^{d(o,v)}、S=Σσ_v：
  (W)  Σ_e w_e·|A_e|·(25−|A_e|) = 45150            （Wiener，已在 presolver 用）
  (M)  Σ_e w_e·q_e·(S−q_e) = 150，q_e=Σ_{v∈A_e}σ_v   （带符号一阶矩，新）
奇偶模式（lowpar/hpar 及各深度奇偶）固定后，|A_e|、q_e 是常数，w_e 是深度的仿射函数，两式是深度的整数线性方程。

文件：theory-lab/s1_crowding/abstract_class_search.cpp（483 行）。入口 solve_depths_for_structure() L189；
逐槽 csp_dfs L92 / csp_take L85；split 参数 main L382。参考：colored_moment_hall_presolve.py（Python 版 (W)），
Astra 的实现 ~/Documents/Codex/leech-ideas-2026-09-04/check_signed_moment.py（(M) 的割边形式，可照抄公式）。

要做：
1. 在奇偶模式固定、深度未放时：把 (W)(M) 化为 Σ c_i·x_i = 常数（x=深度变量），检查 mod 8 与 gcd 整除可解性，
   不可解则跳过整支。
2. 深度阶段只剩两个自由深度时：联立 (W)(M) 直接解（系数行独立时），验证取值范围与父子深度顺序，再走原有距离检查；
   系数行相关时退回枚举。
3. 完整候选：两式作为精确终检（应与原距离检查一致，只是早拒绝）。
4. 加 --no-moment 开关回退；输出 token 与 (split,shape) 记录格式不变。

验收（写进 result）：
- order-6 genuine 正控（现有用法见 colored_moment_hall_presolve.py 顶部注释的 L6 参数）：新旧引擎 survivors 相同。
- theory-lab/s1_crowding/certificates/depthv7_r8/ 中任取 10 条 (split,shape)：新旧 survivors=0 相同，新 leaves ≤ 旧。
- 本机只做 n=6 与 ≤60 秒的小样；r8 差分在 geo-ws 上跑（nice -n 15，≤4 进程，先 pgrep -af abstract_class）。

禁读：research_state.md、paper/、THEORY.md。
回传：docs/briefs/WP-A1-result.md ≤60 行：改动摘要、差分表、新旧二进制 SHA-256、JSON
{status: done|blocked, speedup_smoke: x, blocking: "..."}。不要粘贴代码到 result。
