# Clear code by default

Applies to refactors and new rig/tool code. Write so the next reader (artist, TD, or agent) sees what and why
without decoding indirection. Prefer clarity over cleverness.

- **Names** match scene nodes, attrs, and data-buffer fields (`m_ik_orient_frame`, `ml_ikBlendUse`, not `mSpan` /
  `d_buff`). Meta prefixes: [`meta-runtime.md`](meta-runtime.md).
- **Return values** are what callers need, not opaque dicts unless several distinct outputs are required.
- **Block build helpers:** pass the build instance (`self`) in and set `self.ml_*` / `self.*` inside the helper once
  a legible local exists (e.g. `m_ik_orient_frame`). Don't assign a return value at the call site just to fill buffer fields.
- **Avoid** vague aliases (`ml_ikForFkIkBlend = x or y`), mystery kwargs, and jargon from a different code path
  unless that path is the actual contract.

## When unclear code is OK

Only with a stated reason, in a one-line comment or docstring naming the constraint (not an essay):

| Reason | Example |
|--------|---------|
| Design | Shared API (`blendChainsBy` chain order), framework hook, stable public surface |
| Engineering | Maya constraint needs three distinct transforms; match an existing cgm helper signature |
| Performance | Hot loop, batch `mc.*`, avoiding redundant meta wrap; comment the tradeoff |
