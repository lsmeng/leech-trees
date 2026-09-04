# Low-decoder field audit

This is a read-only audit of
`theory-lab/topwindow/enumerate_pro_b27_p25_low_decoder_pilot.py` against the
`L-surj` requirement in
`docs/pro-b27-two-stage-projection-surjectivity.md`.  It records source-level
coverage only; it is not a new computation and does not certify a theorem.

## Field-by-field result

| projection field | source-level behavior | status for `L-surj` |
|---|---|---|
| low topology / anonymous vertices | `enumerate_pilot` rejects `max_vertices>3`; the target budget allows up to 10 vertices outside `K` | `GAP` |
| literal low edge endpoints | candidate pairs must touch an `x*` vertex; `build_rows` rejects a new component containing more than one fixed vertex | `GAP` |
| low edge weights | weights are permutations of the 14-value `H37` list only, and only for at most three added edges; arbitrary positive weights `<=37` are not in the domain | `GAP` |
| component partition | derived by `low_components` from the supplied edge list | `DERIVED` (conditional on complete input domain) |
| unique rootward port | fixed/no-new components use a hard-coded first known port; new components list local vertices because the high quotient is absent | `GAP` for arbitrary full realizations |
| outward boundary incidences | `outward_mode=all` masks only components containing `x*`; fixed components and their boundary subsets are forced empty | `GAP` |
| owner/alias marks | canonicalization renames anonymous vertices, but owner values are derived only from the bounded low pair table | `PARTIAL` |
| `5` and `21` shape | direct `5`/direct `21` edge is checked; the shared `(5,16)` / `(16,5)` realization of `21` is explicitly omitted | `GAP` |
| `32` non-L ownership | the fixed `p-q=32` edge is present, but no total-state exclusion predicate is defined for every possible realization | `PARTIAL` |
| `34--37` owner geometry | owners are recorded when a bounded low pair realizes a value; no all-state rooted path/incidence classification is provided | `GAP` |
| named/shared identities | fixed names are retained and anonymous names are permuted canonically within the pilot; arbitrary cross-component shared-incidence coverage is not proved | `PARTIAL/GAP` |

The script itself states that it does not prove P25 surjectivity, full H37
saturation, high completion, or nonexistence.  Its independent replay proves
`key -> tree` reconstruction and multiplicity accounting for the bounded pilot;
it does not regenerate the complete raw candidate domain.

## First failing implication

The earliest unconditional failure is the topology field: a genuine state with
four or more anonymous low vertices has no legal input to this pilot, even
before weights or incidence data are considered.  Therefore the current code
cannot define a total map

```text
T -> raw_key(L(T))
```

on all of `U^can_25`.  The next failures are independent (edge-weight domain,
multi-fixed attachment, fixed-component incidences, and the shared `21` shape),
so increasing only `max_vertices` would not close the gap.

## Acceptance consequence

Keep the proof-state label `GAP_L_SURJECTIVITY`.  A legitimate future closure
must either (a) prove a structural theorem reducing every genuine state to a
generator domain containing all fields in the table, or (b) implement and
independently verify a complete literal-state encoder whose inverse is the
materializer.  A larger finite pilot, even if it passes replay, is insufficient
unless its input domain is itself proved universal.

