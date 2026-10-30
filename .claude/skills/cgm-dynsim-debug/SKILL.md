---
name: cgm-dynsim-debug
description: >-
  Debug contract for cgmDynSimTool / cgmDynFK (formerly cgmSimChain) — hair chain count vocabulary
  (sim joints vs follow locs vs inCurve CVs), addEndJoint, curve extendEnd, advanced twist, and the
  Create Chain debug log sequence. Use when touching dynFKTool.py, dynamic_utils.py, simChain_dat.py,
  Feature_DynSimTool.md, or when the user reports wrong joint/locator/CV counts, a chain that won't
  build, or "only N joints" in the dyn sim tool.
---

# cgmDynSimTool debug contract

Ported from `.cursor/rules/cgm-simchain-debug-contract.mdc`.
Canonical detail: [`Features/Feature_DynSimTool.md`](../../../Features/Feature_DynSimTool.md) (Dev debug section).

## Count vocabulary — do not conflate

| Term | Typical count for N target controls |
|------|--------------------------------------|
| **Target controls** (`mBaseTargets` / item list) | N |
| **Sim joints** (`mObjJointChain` under follicle) | N, or **N+1** when **Add end joint** is on — serial `p_parent` chain under root |
| **Driven joints** (spline IK) | Same as sim after `_hair_reparent_sim_chain_ordered`; duplicate sim **root** + child hierarchy; `ik_utils.spline` needs **≥ 3** |
| **Follow locs** (`mLocs`, spline or legacy) | **N** (one per target — *not* N+1) |
| **inCurve CVs** | **N** (or **N+1** sim joints) + optional **+1** when **Extend end** (`extendEnd`) is on — extra CV past tip sim joint (add end on) or last target (add end off); tip CVs skin to last sim joint |
| **Curve extendEnd** | Separate from add end joint — grp attr `extendEnd` when `addEndJoint` attr exists (pre-split chains: legacy `extendEnd` on grp = joint only) |

When the user says "only 4 joints," **clarify sim chain vs follow locs vs CV count before changing code.**

## Add end joint

- UI / grp attr: `addEndJoint` (legacy: chain grp `extendEnd` only when `addEndJoint` attr is absent).
- **On**: expect **N+1** sim joints; tip joint extends past last target by distance (numeric attr, e.g. `2.0`).
- `requireAddEndJoint`: validation can run when the checkbox is on even if numeric parse fails — coerce a
  default distance in the backend.

## Curve extend end

- UI / grp attr: `extendEnd` (default off; distance default **1.0** when enabled).
- **On**: one extra inCurve CV — does **not** add sim joints or follow locs.

## Advanced twist (spline IK only)

- UI / grp attr: `advancedTwist` (default off); setup dat `options.advancedTwist`.
- **On**: after `ik_utils.spline`, `_apply_hair_spline_ik_advanced_twist` — `dWorldUpType` 4;
  `dForwardAxis` / `dWorldUpAxis` from chain fwd/up (**different Maya enums** — do not share an integer map;
  skip `closest*` on world up).
- World-up drivers: `dWorldUpMatrix` / `dWorldUpMatrixEnd` ← sim joint `worldMatrix[0]` (first sim + last
  **base** sim, not the add-end tip). Vectors: `up` axis `p_vector`.
- **Rebuild Chain** reapplies; the checkbox on Details stores to grp only (no live IK patch).
- Sim naming on rebuild: `{name}_sim_##_jnt`; driven `{name}_driven_##_jnt` — not sim.

## Debug log contract (Create Chain, hair)

After **Setup → Reload Dependencies**, three checks in the Script Editor:

1. `uiFunc_make_dynamic_chain` — add-end checkbox/distance, resolved `addEndJoint` and `extendEnd`.
2. `chain_create_hair` **entry** — `addEndJoint`, `extendEnd`, `requireAddEndJoint`, target count.
3. **After ensure** — `simJoints` count and `l_pos` CV count.

If (1) is correct and (2) is **missing**, treat it as a **stale session** — see the stale-session rule in
[`CLAUDE.md`](../../../CLAUDE.md) §8 and `.cursor/rules/cgm-stale-session-diagnosis.mdc`. Do **not** chase
kwargs wiring.

## Reload paths

- **Reload Dependencies** = backend `reload_dependencies` + `_dynfk_rebind_loaded_mDynFK`
- **Relaunch Tool** / shelf = also reloads `dynFKTool`
- **`mClass` edits** (`cgmDynFK` class body) = user runs `import cgm.core as CGM; CGM._reload()`

See `.cursor/rules/cgm-reload-mod.mdc`.
