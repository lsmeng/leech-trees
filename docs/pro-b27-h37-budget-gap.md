# Ten-vertex budget is not a closure by itself

The replay
`theory-lab/topwindow/verify_pro_b27_h37_budget_gap.py` constructs an abstract
low forest for the canonical `J32` branch.  The fixed 15-vertex packet already
realizes the low values

```text
S0_low ∪ {16,19,32,34,35,36,37}.
```

Only seven low values remain: `{5,18,20,21,24,25,26}`.  They can be realized
by eight new vertices: a four-vertex component with edge weights `5,20,21`
(whose internal low pair values include `25=5+20` and `26=5+21`), plus separate
two-vertex edges of weights `18` and `24`.  The resulting disconnected forest
covers all 36 non-punctured values below 38 and uses fewer than the ten
remaining vertices.

The verifier returns `OBSERVED_BUDGET_GAP_ABSTRACT_WITNESS`.  This is not a
connected tree: all `>37` gateways and cross-component distances are omitted
intentionally.  Its role is negative: it proves that the vertex budget and the
low-prefix owner set alone cannot close the `J32` branch.  Attachment ports,
carrier orientation, and the full spectrum remain indispensable.
