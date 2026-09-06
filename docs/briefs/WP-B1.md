# WP-B1 — forest engine 跑完 n=19、n=20，测增长因子（Sonnet）

目的：决定 n=25 直接搜索战役是否可行。已知 n=17：7.88e9 节点、1.7 CPU-h；n=18：约 6e10 节点、几 CPU-h；
每点增长因子 5.71→7.59（n=12..18）在上升。预期 n=19≈5e11 节点（~40 CPU-h）、n=20≈4e12（~350 CPU-h）。

工具：src/forest_search.cpp，分片脚本 src/run_cpp_shard.py，验收 src/verify_forest_run.py。
用法先看这三个文件顶部注释和 results/ 里 n=18 的分片布局（照抄参数，只改 n）。

规则：全部在 Hoffman2（campus/qos campus24，23:50 墙）或 geo-ws（≤4 进程，nice -n 15）跑；起跑前
pgrep -af forest_search 查残留；不动任何已有作业；分片数按 n=18 的做法放大 8 倍以留出墙钟余量。

回传：docs/briefs/WP-B1-result.md ≤60 行：n=19、20 各自的总节点数、CPU-h、survivors（必须 0）、
verify_forest_run 输出 token、结果文件 SHA-256、增长因子 g(19)=N19/N18、g(20)=N20/N19，
JSON {status, nodes19, nodes20, cpuh19, cpuh20, g19, g20, blocking}。中途被墙杀死就报告已完成分片数，不自行重投。
禁读：research_state.md、paper/。
