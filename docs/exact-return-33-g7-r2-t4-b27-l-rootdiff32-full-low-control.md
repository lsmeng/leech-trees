# FW319 `b=27`: full Tail-5 local control with an L ancestor edge `32`

The L alternative also survives the complete local Tail-5 pressure test.
Keep the fixed L factor, choose `w=98`, and use named J depths `34,37`.  Add
an L ancestor--descendant edge of weight `32` at `P_0`, followed by L edges
of weights `35` and `36`.

The resulting 14-vertex tree has all `91` pair distances distinct, with

```text
32: (P0,x32)              L ancestor edge
34: (u,y0)                J
35: (x32,v35)             L
36: (P0,v36)              L
37: (u,y3)                J
```

It satisfies

```text
w=98>=38,  r=34>=16,  t=w+r=132>=54.
```

Its maximum distance is `229`, above the order-14 cap `91`, so this is an
`OBSERVED_CONTROL`, not a Leech tree.  It shows that the L ancestor branch
also cannot be removed by the fixed factor, the carrier/endpoint floors, and
complete local ownership of `32,...,37` alone.  At the first open Taylor
order, however, `229 < binom(25,2)=300`; therefore the order-25 global cap
also does not remove this control (margin `71`).

Replay:

```bash
.venv/bin/python theory-lab/topwindow/verify_exact_return_33_g7_r2_t4_b27_l_rootdiff32_full_low_control.py
```

The remaining exclusion must use the full exact-return spectrum, the final
cap, least-remote minimality, or a genuine inherited descent.
