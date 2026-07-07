# Feature: Mocap Align Snap (native mocapBakeTools)

## Status and Overview

- **Status**: Planning (July 2026)
- **Last Updated**: July 7, 2026
- **Audience**: Dev / TA — design contract for integrating skeleton→control align/snap/bake into **`mocapBakeTools`**
- **Purpose**: Replace the legacy world-vector offset bake path with the validated **parented local-TR locator** workflow (capture once, snap per frame, key controls), while preserving the existing **CCL preset format** and link-list UI artists already use. Unifies single-frame preview snap and timeline bake in one shipped cgm tool.

**Maintenance rule**: Update this doc when `mocapBakeTools` offset capture, snap, bake loop, CCL schema, or resolution rules change. Body-align workflow context and pivot learnings live in [`Feature_Metahuman.md`](Feature_Metahuman.md) (body rig alignment section).

**Related docs**

- [`Feature_Metahuman.md`](Feature_Metahuman.md) — MetaHuman pipelines; body align offset contract (`localTranslate` / `localRotate`, rotate pivot, skeleton roots)
- [`Feature_SceneExportFlow.md`](Feature_SceneExportFlow.md) — export bake/prep (orthogonal; mocap align may run **before** export in some shots)

---

## Problem

### What mocapBakeTools does today

[`cgm/core/tools/mocapBakeTools.py`](../../cgmToolsPy3/cgm/core/tools/mocapBakeTools.py) maps **source** drivers (typically mocap / MetaHuman joints) to **target** controls, then bakes keys over a frame range.

| Stage | Current behavior | Limitation |
|-------|------------------|------------|
| **Set connection pose** | `set_connection_offsets()` — world position delta + `offsetForward` / `offsetUp` in source space | Wrong or unstable on IK controls, offset pivots, and rigs where joint vs control rest frames differ |
| **Bake** | Per frame: `POS.set` + `SNAP.aim_atPoint` using stored vectors | Same math as above; does not match marking-menu locator / rotate-pivot contract |
| **Live constraints** | `pointConstraint` / `orientConstraint` `mo=True` | Preview path unrelated to bake math |
| **CCL** | Six-element JSON; stores whatever strings are in source/target lists | Often long DAG paths; no skeleton-root disambiguation |

### What we validated externally (July 2026)

A project-script prototype (documented in [`Feature_Metahuman.md`](Feature_Metahuman.md)) proved:

1. **Capture** — `doLoc()` on control at **rotate pivot**, parent to source joint, store **`localTranslate` / `localRotate`** under joint.
2. **Snap (single frame)** — rebuild parented offset locator, `movePointSnap` / `moveOrientSnap` on target.
3. **CCL** — short joint patterns + namespaced control names; resolve via **skeleton roots** + **rig namespace**.
4. **Multi-skeleton scenes** — require explicit skeleton root selection before capture/snap.

That logic must live in **cgmToolsPy3** and drive **both** preview snap and timeline bake inside mocapBakeTools.

---

## Goals

### In scope

- Factor align/snap/CCL helpers into **`cgm/core/lib/`** (no new logic in project scripts long-term)
- **Capture offsets** in mocapBakeTools UI (bind pose) using local-TR locator workflow
- **Snap** — single-frame, no keys (all links or selection); Script Editor report
- **Bake** — per-frame snap + `setKeyframe` on targets using **same** offset math as snap
- **CCL** — load/save compatible with existing six-element format; prefer short patterns; accept legacy files
- **Resolution** — skeleton joint patterns scoped to UI skeleton roots; rig controls via namespace
- Backward compatibility: load old CCLs with `positionOffset` / forward-up; warn and require re-capture for bake/snap

### Out of scope (initial ship)

- Replacing mocapBakeTools link-by-distance / link-by-name UX (keep; may auto-fill from preset)
- Facial SDK transfer ([`Feature_Metahuman.md`](Feature_Metahuman.md) — separate pipeline)
- Scene export integration hooks (future: optional pre-export bake step)
- Artist Google Doc / shelf (after UI stabilizes)
- Persisting debug locators in CCL (`alignLocator` refs remain session-only)

---

## Architecture

### Core concepts

```mermaid
flowchart LR
  subgraph preset [CCL preset]
    CCL[Short patterns\njoint + control]
  end

  subgraph resolve [Runtime resolution]
    Roots[Skeleton roots UI]
    NS[Rig namespace UI]
    CCL --> Resolve[resolve_connections]
    Roots --> Resolve
    NS --> Resolve
  end

  subgraph offset [Offset storage per link]
    Cap[Capture at bind pose]
    Loc[Parented offset locator\nlocal TR under joint]
    Cap --> Loc
    Loc --> Store[localTranslate\nlocalRotate]
  end

  subgraph exec [Execution]
    Snap[Snap current frame\nno keys]
    Bake[Bake range\nsnap + setKeyframe]
    Store --> Snap
    Store --> Bake
  end
```

| Concept | Role |
|---------|------|
| **Connection dict** | One source→target pair: patterns, resolved nodes, follow flags, offsets |
| **Follow mode** | `setPosition` + `setRotation` → legacy `constraintType` `po` / `o` in CCL target data |
| **Offset locator** | Temporary or persistent debug loc; parented to **source** joint with saved local TR; world pose drives snap |
| **Resolution** | Patterns in CCL; long paths only in memory after resolve |

### Offset contract (normative)

Inherited from [`Feature_Metahuman.md`](Feature_Metahuman.md) — **do not diverge**:

| Step | Rule |
|------|------|
| Locator creation | `cgmObject.doLoc()` on **target** control; **rotate pivot** placement |
| Parent | To **source** joint; preserve world transform |
| Storage | `localTranslate`, `localRotate` on locator under joint |
| Snap position | `cgm.lib.position.movePointSnap` (rotate pivot) |
| Snap rotation | `cgm.lib.position.moveOrientSnap` |
| Meta wrap | `cgmObject(longName)` only — not `validateObjArg(setClass=True)` on anim controls |

### CCL schema (extended, backward compatible)

Existing six-element array unchanged:

```
[source_items, source_data, target_items, target_data, links, connection_data]
```

**connection_data[]** entries — supported keys:

| Key | Required | Notes |
|-----|----------|-------|
| `source`, `target` | Yes | Short patterns in saved files |
| `setPosition`, `setRotation` | Yes | Bake/snap flags |
| `localTranslate`, `localRotate` | Preferred | New capture output |
| `positionOffset`, `offsetForward`, `offsetUp` | Legacy | Load OK; snap/bake warns until re-captured |

On save: emit short patterns only (see MetaHuman feature doc CCL conventions).

---

## Module placement

Per [`cgm-module-placement`](../../.cursor/rules/cgm-module-placement.mdc):

| Module | Responsibility |
|--------|----------------|
| **`cgm/core/lib/mocap_align_utils.py`** (new) | CCL load/save/normalize, pattern resolution, capture, single-frame snap, **per-frame bake sample**, connection dict helpers |
| **`cgm/core/tools/mocapBakeTools.py`** | UI, link lists, calls into lib; thin `set_connection_offsets` / `bake` wrappers |
| **Project scripts** | Deprecate duplicate align UI once parity reached; may keep Scene menu entry that opens mocapBakeTools |

Do **not** put resolution or offset math in `cgm_General` or vendored trees.

### Proposed public API (`mocap_align_utils.py`)

| Function | Purpose |
|----------|---------|
| `load_ccl(path)` / `save_ccl(path, data)` | JSON six-element IO |
| `ccl_to_connections(data, rig_ns, skel_roots, skel_ns)` | Normalize + resolve |
| `connections_to_ccl(connections, rig_ns)` | Short-pattern export |
| `resolve_skeleton_joint(pattern, skel_roots, skel_ns)` | Scoped joint lookup |
| `resolve_rig_control(pattern, rig_ns)` | Namespaced control lookup |
| `capture_alignment_offsets(connections)` | Bind-pose capture in place |
| `snap_connections(connections, indices=None)` | Single frame; returns result dict |
| `bake_connections(connections, start, end)` | Timeline loop: snap + keyframe |
| `_align_ccl_source_pattern` / `_align_ccl_target_pattern` | Short-name helpers (may be module-private) |

Project-script implementations become the reference port; behavior should match unless noted in PR.

---

## mocapBakeTools UI plan

Keep existing **source / target lists**, **link**, **bake range**, and **CCL load/save**. Add:

| UI block | Control | Behavior |
|----------|---------|----------|
| **Resolution** | Rig namespace field | Default from selection or last used optionVar |
| **Resolution** | Skeleton roots field + “Set from selection” | Semicolon-separated long paths; required when >1 skeleton |
| **Offsets** | **Capture offsets** | Replaces or supplements “Set connection pose”; writes `localTranslate` / `localRotate` |
| **Preview** | **Snap all** / **Snap selected** | No keys; report to Script Editor |
| **Debug** | **Create locs** / **Delete locs** (optional) | Persistent offset locators per link |
| **Bake** | Existing bake button | Calls `bake_connections()` using locator snap |

OptionVar candidates: `mocap_rig_namespace`, `mocap_skel_roots`, `mocap_use_local_offsets` (default 1).

**“Set connection pose”** — either:

- **A (recommended):** Remove from default UI; keep legacy function as deprecated alias that warns and calls old vector math only if a “legacy offsets” debug flag is on.
- **B:** Rename to “Capture offsets (legacy)” hidden under Tools menu for old scenes.

---

## Bake loop design

Replace inner loop of `bake()`:

```python
# Current (legacy)
POS.set(target, source_pos + positionOffset)
SNAP.aim_atPoint(target, ..., vectorUp=offsetUp)

# Target (locator-based)
for frame in bake_range:
    mc.currentTime(frame)
    for conn in connection_data:
        snap_connection_pair(conn)  # same as single-frame snap
        if conn['setPosition']:
            mc.setKeyframe(target + '.translate')
        if conn['setRotation']:
            mc.setKeyframe(target + '.rotate')
```

Notes:

- Rebuild or update offset locators **once** before bake chunk; update parent if source moved (joint animation).
- Locator local TR stays constant; joint motion drives world locator pose.
- Single `undoInfo` open/close around full bake (existing pattern).
- `cgmGEN.playback_stop()` before bake (existing).

Performance: ~N links × M frames locators — acceptable for typical body (~50×1000); profile before optimizing (pool locators, avoid recreate per frame).

---

## Migration and compatibility

| Scenario | Behavior |
|----------|----------|
| Old CCL with long DAG paths | Load OK; normalize to short on save; resolve if nodes exist |
| Old CCL with vector offsets only | Load OK; snap/bake warn “re-capture offsets”; optional one-time “legacy bake” menu for old scenes |
| New CCL with local TR | Full snap + bake |
| Mixed skeletons in scene | User must set skeleton roots (same as MetaHuman align doc) |
| `doLoc` pivot fix in cgm core | Required dependency — rotate pivot default (July 2026) |

Character presets (e.g. per-project `.ccl` under `cgmDat/mocap/`) ship short names; mocapBakeTools default file dialog can point at project dat path via optionVar later.

---

## Implementation phases

### Phase 1 — Library extraction (py3 only)

1. Create `cgm/core/lib/mocap_align_utils.py` from validated project-script logic.
2. Unit-test pure helpers where possible (pattern parsing, CCL round-trip without Maya).
3. Maya dev tests: capture → snap → compare control to manual locator check (foot IK, one finger).

**Exit criteria:** Lib imports from Maya; one body pair passes capture/snap.

### Phase 2 — mocapBakeTools capture + snap (no bake change yet)

1. Wire UI: namespace, skeleton roots, Capture offsets, Snap all/selected.
2. On CCL load: `ccl_to_connections` + populate lists from patterns (or merge with existing list UI).
3. Script Editor reporting for snap.
4. Keep legacy `bake()` unchanged; warn if local offsets missing.

**Exit criteria:** Load preset, capture, scrub skeleton, snap — matches project prototype.

### Phase 3 — Bake integration

1. Implement `bake_connections()` in lib.
2. Replace `bake()` body to call lib when `localTranslate` present on all active links (or per-link fallback with warning).
3. OptionVar “set connection at bake” → auto-capture if missing (discourage for production; prefer explicit capture).

**Exit criteria:** Bake range on test scene matches single-frame snap at each frame; keys on targets only.

### Phase 4 — Polish and deprecation

1. Short-name save by default; mapping list or alias refresh shows resolved short names.
2. Document in [`Feature_Metahuman.md`](Feature_Metahuman.md) that mocapBakeTools is the canonical align/bake home.
3. Thin or remove duplicate project align UI; Scene menu opens mocapBakeTools or preloads preset path.
4. Google Doc capture for artists (optional).

---

## Testing checklist

### Dev (Maya)

1. Load short-name CCL; set skeleton roots + rig NS; all links resolve.
2. Capture at bind pose; spot-check local TR on foot IK and one finger.
3. Snap all — Script Editor report; controls match debug locators.
4. Scrub skeleton; repeat snap on single frame — stable.
5. Bake 10-frame range; keys only on targets; motion matches live snap.
6. Load **legacy** CCL (vector offsets); warnings; re-capture; bake succeeds.
7. Two skeletons in scene; without roots — capture/snap blocked or warns; with roots — correct hierarchy.
8. CCL save/reload round-trip; file stays short; offsets preserved.

### Regression

- Existing mocapBakeTools link-by-name / link-by-distance still works for ad-hoc sessions without preset.
- Old CCL files from shipped characters still load (may need re-capture, not crash).

---

## Risks and open questions

| Item | Notes |
|------|-------|
| **Bake performance** | Many links × long ranges; may need locator pooling |
| **Orient-only pairs** | Bake rotation keys only — verify no stray translate keys |
| **Referenced rigs** | Snap/bake on referenced anim controls — test lock/reference edits |
| **Constraint conflicts** | Targets with existing constraints may not move; report in unchanged_details (reuse snap result pattern) |
| **Auto “set connection at bake”** | Legacy behavior re-captures with **wrong** math if left on — default off when local-offset mode enabled |
| **UI complexity** | mocapBakeTools already dense; consider collapsible “MetaHuman align” frame |

**Open decisions (resolve before Phase 2):**

1. Remove vs hide legacy “Set connection pose”?
2. Should link lists store **patterns** or resolved long names internally after load?
3. Default skeleton roots from selection on CCL load if exactly one MH root detected?

---

## Future work (post-ship)

- [ ] Scene export hook: optional “bake mocap align before export” on tdSet rigs
- [ ] Preset browser tied to `cgmDat/mocap/` per character
- [ ] mayapy batch bake for overnight retarget passes
- [ ] Merge with mocapBakeTools “attach point” / raycast loc workflows (shared `LOC.create` pivot rules)

---

## Revision history

| Date | Summary |
|------|---------|
| 2026-07-07 | Initial plan — problem statement, lib factoring, UI/bake design, phases, migration, testing |
