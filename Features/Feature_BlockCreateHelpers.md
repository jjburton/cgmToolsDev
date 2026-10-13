# Feature: BlockCreate placement helpers

## Status and overview

- **Status**: Shipped (py3; Maya workflow)
- **Last Updated**: October 12, 2026
- **Audience**: Dev / TA — design contract for MRS **BlockCreate** helper geometry, persistence, sizing, and build snap (not artist Google Doc prose)
- **Purpose**: Document how placement helpers register on **`mrsHelpers`**, how **Initialize / Build** use them, and how **height baseline** + **shapeDirection** set helper pivots before blocks are created.

**Maintenance rule**: Update when changing `cgm/core/mrs/Helpers.py`, BlockCreate helper UI in `Builder.py`, or `tool_calls.mrsBlockCreate` / `blockCreate_open` reload path.

**Related docs**

- [`Feature_CgmToolUI.md`](Feature_CgmToolUI.md) — helper registered status row (animClip-style readout)
- [`Feature_MRSWiring.md`](Feature_MRSWiring.md) — block/module graph after create (orthogonal)
- [`Branches/Branch_Jan2026.md`](../Branches/Branch_Jan2026.md) — branch timeline entry

---

## Entry points

| Surface | Entry | Notes |
|---------|-------|-------|
| Toolbox / MRS menu | `tool_calls.mrsBlockCreate()` | Calls `Builder.blockCreate_open()` (reload Helpers + Builder, then UI) |
| BlockCreate UI | `Builder.ui_createBlock` | Helpers frame; **Initialize** / **Build** |
| Scene node | `mrsHelpers` (`HelperDag`) | Holds indexed **`helpers_*`** msgList |
| Backend | `cgm.core.mrs.Helpers` | msgList API, create, raycast, size, snap |

---

## Persistence (`msgList`)

Helpers are **not** rediscovered by outliner scan on every open. The **`mrsHelpers`** transform owns an indexed message list:

| Attr pattern | Holder | Child |
|--------------|--------|--------|
| `helpers_0`, `helpers_1`, … | `mrsHelpers` | Each helper transform (`block_*_helper`, raycast dupes, etc.) |

**API** (module functions on `Helpers`):

- `helpers_msglist_get(mDag)` / `helpers_msglist_set(mDag, ml_helpers)` — read/write; cleans dead slots
- `_helpers_migrate_legacy_message` — one-time move from singular `helpers` message to msgList
- `helpers_ensure_mDag(ui)` — re-bind after `cgmGEN._reloadMod(Helpers)` / stale UI `mDag`
- `helpers_mDag_valid(mDag)` — meta + `mc.objExists` guard (avoids `msgList_clean` on dead nodes)

**UI**: `helpers_ui_update_registered` syncs `self.ml_helpers`, frame label `Helpers (N)`, status button text + names, **Build** enabled when `N > 0`.

**Reload**: `Builder.reloadMRSStuff()` includes **`cgm.core.mrs.Helpers`**. `blockCreate_open()` reloads **Helpers** then **Builder** before opening BlockCreate.

---

## Helper creation

### Simple (poly cube)

1. Unit cube, `mHelper.scale = baseSize` from BlockCreate size fields.
2. `helper_apply_height_baseline(mHelper, heightBaseline, shapeDirection=…)` — pivot placement (below).
3. Append to `ml_helpers`; `helpers_msglist_set` on `mDag`.

### Raycast

`helpers_raycast` / `helperRayCaster.finalize` — same baseline + shapeDirection after placement; optional mid-point scale from cast axes.

### Initialize vs Replace

**Initialize** deletes existing registered helpers, clears msgList, creates a fresh set from current UI (count, mode, size, baseline, shapeDirection).

---

## Height baseline and shapeDirection

Baseline is **-1 / 0 / +1** (UI radio on Helpers frame). It sets **where the helper pivot sits on the unit cube** along the block profile **`shapeDirection`** axis (read from BlockCreate options at Initialize).

| Baseline | Meaning |
|----------|---------|
| **-1** | **Base** — start of the length axis (opposite the aim direction) |
| **0** | **Center** — cube center |
| **+1** | **Tip** — aim end of the length axis |

**Examples** (object-space pivot on ±0.5 unit cube):

| shapeDirection | baseline -1 (base) |
|----------------|---------------------|
| `y+` | bottom of **Y** (`y = -0.5`) |
| `y-` | top of **Y** (`y = +0.5`) |
| `z-` | **+Z** face (`z = +0.5`) |
| `z+` | **-Z** face (`z = -0.5`) |

Mesh stays centered; **`mc.xform(..., os=True, pivots=…)`** moves rotate/scale pivot only (no vtx offset).

**Stamped attrs** on each helper:

- `cgmHelperHeightBaseline` (long)
- `cgmHelperShapeDirection` (string)

**Functions**: `helper_apply_height_baseline`, `helper_get_height_baseline`, `helper_get_shape_direction`, `helper_ui_shape_direction`, `_helper_baseline_pivot_object_space`.

---

## Build from helpers

Flow: **Build** → `uiFunc_helper_build` → `uiFunc_create(count)` per helper → `helper_snap_block_to_helper`.

### Size

`helper_block_size_from_helper(mHelper, shapeDirection)`:

- Temporarily zero helper **orient**, `TRANS.bbSize_get(..., shapes=True)`, restore orient.
- Reorder to block `baseSize` tuple via `_SHAPE_DIR_TO_BB_ORDER` (`y` → `xzy`, `x` → `yzx`, `z` → `xyz`).
- Passed as `d_create['size']` before `cgmRigBlock` create; block then gets `p_orient = mHelper.p_orient`.

### Snap

`helper_snap_block_to_helper(mBlock, mHelper, shapeDirection)`:

- Block **orient** = helper orient.
- **baseline ≠ 0**: position snap **rp → rp** (pivot anchors align).
- **baseline 0**: **castNear** on inverted shape side (mid-side placement); `targetMode` flips `+`/`-` on shapeDirection.

`head` block type: copy helper position only.

---

## Session / reload

| Symptom | Fix |
|---------|-----|
| UI shows new strings, helper API errors / no msgList | **Reload MRS** from BlockCreate menu or relaunch `mrsBlockCreate()` |
| `TypeError` on `msgList_clean` after reload | Stale `mDag` — fixed by `helpers_ensure_mDag` on refresh paths |
| Wrong baseline axis after profile change | Re-**Initialize** helpers (stamped attrs + pivot from current UI) |

Do **not** call `reload_dependencies` inside Initialize/Build callbacks.

---

## Key files

| File | Role |
|------|------|
| [`cgm/core/mrs/Helpers.py`](../../cgmToolsPy3/cgm/core/mrs/Helpers.py) | msgList, baseline, size, snap, UI frame |
| [`cgm/core/mrs/Builder.py`](../../cgmToolsPy3/cgm/core/mrs/Builder.py) | `_init_helper_system`, `uiFunc_create` size/orient, `reloadMRSStuff`, `blockCreate_open` |
| [`cgm/core/tools/lib/tool_calls.py`](../../cgmToolsPy3/cgm/core/tools/lib/tool_calls.py) | `mrsBlockCreate` → `blockCreate_open` |

---

## Revision history

| Date | Summary |
|------|---------|
| 2026-10-12 | Initial doc: msgList on `mrsHelpers`, baseline pivot along shapeDirection, build size/snap, reload path |
