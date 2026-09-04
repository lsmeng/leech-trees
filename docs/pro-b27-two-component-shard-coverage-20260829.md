# FW319 b=27 two-component shard coverage (Geo Workstation)

Date: 2026-08-29

The four Geo Workstation shards reran the same restricted two-component
necessary-condition model with `max_edges=3`, `h_max=240`, and
`witness_limit=20`.  They partitioned the flat pair index into four contiguous
half-open intervals.

The independent merger
`theory-lab/topwindow/verify_pro_b27_two_component_port_states_shards.py`
returned:

```text
status=VERIFIED_SHARD_COVERAGE
coverage_exact=true
global_total_pairs=853575813
processed_pairs=853575813
survivors_found=0
shard_count=4
```

All shards report the same wrapper hash
`728adc4f26f27d5869c5f8aa18a07d3a02d5270a80b520c398b709a981d0f37d`
and semantic input hash
`8c0d82ea61cb59030614fde56e2c76e9f39b646fd3194ef0ce98ed6c7968e236`.
The pulled artifact hashes, in shard order, are:

```text
ffdd86a701ef2153252ef1963e8f8d12acbebb765567e6a86ce7784b380dedaf  shard_0_of_4.json
f6e4dfb3733059e7c5504fa83ed672d743b861d0e5b755760c0df1e04fb771f0  shard_1_of_4.json
2d437aabdf23353ca82b43edfe0e344e8896bf3ddda725d248d6eb9fe33cf2f0  shard_2_of_4.json
f58ae04401489171e0e46f1107320f78066cb2f9aea0da281d9aabd96aea3072  shard_3_of_4.json
```

This is a verified finite coverage result for the stated restricted model.
It does not cover forced L owners 5/21, other H37 components, arbitrary
LCAs/gateways, or complete-spectrum/Label-State completeness, and therefore
does not prove global Leech-tree nonexistence.
