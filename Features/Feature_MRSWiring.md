# Feature: MRS Module Wiring

## Status and Overview

- **Status**: Shipped (core MRS; ongoing maintenance)
- **Last Updated**: October 9, 2026
- **Audience**: Dev / TA — design contract for block/module/puppet message graphs and build sync (not artist manual prose)
- **Purpose**: Canonical reference for how `cgmRigBlock`, `cgmRigModule`, and `cgmRigPuppet` stay linked via message attributes, DAG parenting, and cached lists. Use when debugging build regressions, mirror/controller passes, module hierarchy bugs, or attach-point failures.

**Maintenance rule**: Update this doc whenever `puppet_utils.module_connect`, `module_utils.parentModule_set`, `module_utils.mirror_get`, `block_utils.moduleTarget_wire_from_blockParent` / `puppet_verify`, `controls_getDat` rewire behavior, or message attr names on `cgmRigPuppet` / `cgmRigModule` change.

**Related docs**

- [`Feature_SceneExportFlow.md`](Feature_SceneExportFlow.md) — export uses puppet/module sets (orthogonal)
- [`Feature_DynSimTool.md`](Feature_DynSimTool.md) — dyn drivers collected to puppet space groups

---

## Scope

### In scope

- Three-layer graph: **Block** (`moduleTarget`) → **Module** (`moduleParent` / `moduleChildren` / `modulePuppet`) → **Puppet** (`moduleChildren`, caches)
- Build-time wiring: `module_verify`, `puppet_verify`, `connect_module`, `gather_modules`, `moduleTarget_wire_from_blockParent`
- Query + **rewire** caches: `mModulesAll`, `mControlsAll`, `mControlsCore`, `mControlsCoreAll`
- Spatial attachment: `get_attachPoint`, `get_driverPoint`, `skeleton_connectToParent`
- Rig live/deform wiring: `rig_connect` / `rig_disconnect` (skin joints → rig joints)
- Dispatch pattern: `atUtils`, `atRigModule`, `atRigPuppet` on meta classes

### Out of scope

- Block **state** message wiring (`d_wiring_form`, `d_wiring_prerig`, `msgDat_check`) — brief cross-ref only; detail stays in block build docs
- Face control **attribute** wiring (`face_utils` `wiringDict`) — separate system
- Mirror index assignment / controller graph (`mirror_verify`, `controller_verify`) — documented here as **consumers** of control rewire, not full mirror spec
- Artist Google Doc / shelf wording (this doc can seed that later)

---

## Entry Points and Call Graph

| Surface | Entry | Notes |
|---------|-------|-------|
| Block build | `block_utils.puppet_verify` | Non-master blocks attach module to puppet |
| Meta API | `cgmRigPuppet.connect_module` / `gather_modules` | Delegates to `puppet_utils` |
| Block parent change | `block_utils.moduleTarget_wire_from_blockParent` | Syncs block tree → module tree |
| Module hierarchy | `module_utils.parentModule_set` / `parentModule_detach` | Bidirectional `moduleParent` / `moduleChildren` |
| String dispatch | `cgmRigBlock.atRigModule('set_parentModule', …)` | `RigBlocks.py` |
| Control repair | `controls_getDat(..., rewire=True)` | Puppet + module level |

```mermaid
flowchart TD
  Build[block build / state change] --> MV[module_verify]
  MV --> PV[puppet_verify]
  PV --> CM[connect_module]
  CM --> GM[gather_modules]
  BP[blockParent_set] --> MTW[moduleTarget_wire_from_blockParent]
  MTW --> PMS[parentModule_set or modulePuppet]
  Mirror[mirror_verify / controller_verify] --> RW[controls_get rewire=True]
  RW --> Cache[mControlsAll caches]
```

### Key files

| File | Responsibility |
|------|----------------|
| [`cgm/core/mrs/lib/puppet_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/puppet_utils.py) | Puppet↔module connect, module enumeration, puppet control aggregation, `rig_connectAll` |
| [`cgm/core/mrs/lib/module_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/module_utils.py) | Module hierarchy, attach/driver points, module control rewire, rig connect per module |
| [`cgm/core/mrs/lib/block_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/block_utils.py) | `puppet_verify`, `module_verify`, `moduleTarget_wire_from_blockParent`, `blockParent_set` |
| [`cgm/core/mrs/RigBlocks.py`](../../cgmToolsPy3/cgm/core/mrs/RigBlocks.py) | `cgmRigPuppet`, `cgmRigModule` meta classes, `atUtils` / `atRigModule` dispatch |
| [`cgm/core/mrs/lib/general_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/general_utils.py) | `get_puppet_heirarchy_context` (hierarchical module order) |
| [`cgm/core/mrs/lib/shared_dat.py`](../../cgmToolsPy3/cgm/core/mrs/lib/shared_dat.py) | `_l_controlOrder`, block wiring UI keys |

---

## Core Concepts

### Three meta layers

MRS maintains **two parallel hierarchies** that must stay aligned:

1. **Block tree** — `blockParent` on `cgmRigBlock` (authoring / build order)
2. **Module tree** — `moduleParent` / `moduleChildren` on `cgmRigModule` (runtime part graph)

Each non-master block owns a **`moduleTarget`** (`cgmRigModule`). All modules roll up to a single **`cgmRigPuppet`** (the master block's `moduleTarget`).

```mermaid
flowchart TB
  subgraph blockLayer [Block layer]
    RB[cgmRigBlock]
    BP[blockParent]
  end
  subgraph moduleLayer [Module layer]
    RM[cgmRigModule]
    MP[moduleParent]
    MC[moduleChildren]
  end
  subgraph puppetLayer [Puppet layer]
    RP[cgmRigPuppet]
    MCH[moduleChildren]
    MA[mModulesAll cache]
  end
  RB -->|moduleTarget| RM
  BP -->|moduleTarget_wire_from_blockParent| MP
  RP -->|module_connect| RM
  RM -->|modulePuppet| RP
  MCH --> RM
  MP --> MC
```

**Sync point**: when `blockParent_set` runs, it calls `moduleTarget_wire_from_blockParent` so the module tree reflects the block tree.

### Message attribute contract

| Object | Attribute | Direction | Role |
|--------|-----------|-----------|------|
| `cgmRigBlock` | `moduleTarget` | block → module | Built module instance |
| `cgmRigModule` | `rigBlock` | module → block | Source block |
| `cgmRigModule` | `modulePuppet` | module → puppet | Owning puppet |
| `cgmRigModule` | `moduleParent` | module → module | Parent part |
| `cgmRigModule` | `moduleChildren` | module → module[] | Child parts |
| `cgmRigPuppet` | `moduleChildren` | puppet → module[] | Top-level modules only |
| `cgmRigPuppet` | `mModulesAll` | cache | Flat module list (`rewire=True` rebuilds) |
| `cgmRigModule` | `mControlsAll`, `mControlsCore` | cache | Per-module control lists |
| `cgmRigPuppet` | `mControlsAll`, `mControlsCoreAll` | cache | Aggregated control lists |

### Manual list maintenance invariant

`moduleChildren` on puppet and modules is updated by **explicit append/remove** (`__setMessageAttr__`, list reassignment) — not only `connectChildNode`. This is intentional: simple message attrs stay predictable and list order is controlled by the utils.

Always use **`parentModule_set`** / **`parentModule_detach`** for module-to-module links; do not set `moduleParent` alone without updating the parent's `moduleChildren`.

### Block state wiring (related, separate)

Per-block-type **`d_wiring_{state}`** dicts (e.g. `d_wiring_form`, `d_wiring_prerig`) declare which message links must exist for `is_form`, `is_prerig`, etc. Resolved via `block_utils.get_stateLinks` and checked by `msgDat_check`. This is **block null wiring**, not the module part graph — do not conflate the two when debugging.

---

## Normative Wiring Sequences

### A. Build attach (non-master block)

Inside `puppet_verify` (`block_utils.py`):

1. **`module_verify`** — create or find `moduleTarget` on the block
2. **Resolve puppet** — from existing `modulePuppet`, or walk block parents to master `moduleTarget`, or create new puppet
3. **`connect_module(mi_module)`** — append to puppet `moduleChildren`, set `modulePuppet`, parent module DAG under `masterNull.partsGroup`
4. **`gather_modules()`** — iterate all modules and re-run `module_connect` on each

`module_connect` (`puppet_utils.py`) in order:

- Append module to puppet `moduleChildren` if not present
- Set `mModule.modulePuppet = self.mNode`
- Set `mModule.parent = self.masterNull.partsGroup.mNode`

### B. Block parent → module parent sync

`moduleTarget_wire_from_blockParent` runs from `blockParent_set` whenever block parenting changes:

| Block parent | Module action |
|--------------|---------------|
| Master block | `modulePuppet = parentModuleTarget` (top-level under puppet) |
| Non-master block | `set_parentModule(parentModuleTarget)` |
| No block parent | `parentModule_detach`, then `modulePuppet = puppet_get(self)` |

`parentModule_set` (`module_utils.py`) maintains bidirectional links:

1. Remove self from old parent's `moduleChildren` (if any)
2. Append self to new parent's `moduleChildren`
3. Set `moduleParent` message on self
4. Copy new parent's DAG parent: `self.parent = mModuleParent.parent`

```mermaid
sequenceDiagram
  participant Block as cgmRigBlock
  participant BU as block_utils
  participant Mod as cgmRigModule
  participant MU as module_utils

  Block->>BU: blockParent_set
  BU->>BU: moduleTarget_wire_from_blockParent
  BU->>Mod: parentModule_detach
  alt parent is master
    BU->>Mod: modulePuppet = parentModuleTarget
  else parent is part block
    BU->>MU: set_parentModule(parentModuleTarget)
    MU->>Mod: update moduleParent + moduleChildren both ways
  end
```

### C. Module enumeration

| Function | Behavior |
|----------|----------|
| `modules_get(rewire=False)` | Start from puppet `moduleChildren`; recursively extend via `get_allModuleChildren` → `moduleChildren_get` (BFS deque) |
| `modules_getHeirarchal(rewire=True)` | Ordered list via `get_puppet_heirarchy_context` |
| `rewire=True` | Writes `mModulesAll` on puppet |

**Referenced assets**: all rewire paths skip writes when `isReferenced()` is true.

### D. Control discovery and rewire

Two-level aggregation:

**Module** — `controls_getDat(..., rewire=True)` in `module_utils.py`:

1. Walk `d_controlLinks` keys against `rigNull` message/msgList plugs (merge block-module overrides from `d_controlDat_links`)
2. Second pass: reconcile against `rigNull.moduleSet` members; tag via `cgmControlDat` / `cgmTypeModifier`
3. On rewire: purge/rebuild `moduleSet`, repair broken `rigNull` parent links on controls, write `mControlsAll` and `mControlsCore`

**Puppet** — `controls_get(..., rewire=True)` in `puppet_utils.py`:

1. Collect puppet-level controls via puppet `d_controlLinks` (`root`, `settings`, `motionHandle`, etc.)
2. Extend with each module's `atUtils('controls_get', rewire=rewire)`
3. On rewire: repair broken `cgmOwner` links, write `mControlsAll` and `mControlsCoreAll`

**Control category maps**: puppet `d_controlLinks` adds puppet-only keys (`root` → `masterControl`, `cog`, …). Module `d_controlLinks` follows `BLOCKSHARE._l_controlOrder` (`fk`, `ik`, `direct`, …). Block modules may extend via `d_controlDat_links`.

**Downstream consumers**: `mirror_verify` and `controller_verify` call `controls_get(..., rewire=True)` before processing — stale caches break mirror pairing and controller parenting.

### E. Spatial attachment (rig build)

Used when a child module must attach to its parent's skeleton or controls:

| Function | Returns | Notes |
|----------|---------|-------|
| `get_attachPoint(mode)` | Parent skeleton joint | Reads parent `moduleJoints` or `rigJoints` (head/end special case); modes: `end`, `base`, `closest`, `index` |
| `get_driverPoint(mode)` | Constraint driver transform | Often `masterGroup` or `dynParentGroup` off rig joint; root modules get puppet `masterControl`; default mode from block `attachPoint` enum |
| `skeleton_connectToParent` | — | Parents first `moduleJoint` under resolved attach joint; block-parent aware |

### F. Rig connect (deform layer)

Separate from message wiring — connects **skin joints to rig joints** for live deformation:

| Module type | Constraints |
|-------------|-------------|
| Face modules | `parentConstraint` (rig → skin) |
| Body/limb | `pointConstraint` + `orientConstraint` + `scaleConstraint` |

- **`rig_connect`** / **`rig_disconnect`** — per module
- **`rig_connectAll`** on puppet — walks `[self] + modules_get(self)` and calls each `rig_connect` or `rig_disconnect`

Puppet-level **`rig_connect`** (master) connects `rootJoint` to `rootMotionHandle` via `RIGCONSTRAINT.driven_connect`.

---

## Dispatch API

Meta classes route string calls to lib utils:

| Caller | Method | Resolves to |
|--------|--------|-------------|
| `cgmRigPuppet` | `atUtils(func, …)` | `puppet_utils.{func}(self, …)` |
| `cgmRigModule` | `atUtils(func, …)` | `module_utils.{func}(self, …)` |
| `cgmRigBlock` | `atRigModule(func, …)` | `block.moduleTarget.atUtils(func, …)` |
| `cgmRigBlock` (master) | `atRigPuppet(func, …)` | `block.moduleTarget.atUtils(func, …)` |
| `cgmRigBlock` (non-master) | `atRigPuppet(func, …)` | `block.moduleTarget.modulePuppet.atUtils(func, …)` |

Convenience wrappers on `cgmRigPuppet`: `connect_module`, `get_modules`, `gather_modules` → direct `PUPPETUTILS` calls.

---

## Common Rig Patterns

### Pattern: Master + two part blocks

| Item | Value |
|------|-------|
| **Setup** | Master block + spine block + limb block; limb `blockParent` = spine |
| **Expected** | Master `moduleTarget` = puppet; spine and limb modules in puppet `moduleChildren`; limb `moduleParent` = spine module |
| **DAG** | All module transforms under `masterNull.partsGroup` |
| **Verify** | `puppet.atUtils('modules_get', rewire=True)` returns 2+ modules |

### Pattern: Reparent block in form state

| Item | Value |
|------|-------|
| **Setup** | Change limb `blockParent` from spine to master |
| **Expected** | `moduleTarget_wire_from_blockParent` detaches old parent, sets `modulePuppet` or new `moduleParent` |
| **Regression** | `get_driverPoint` / `get_attachPoint` must resolve against new parent |

### Pattern: Mirror verify after rig build

| Item | Value |
|------|-------|
| **Setup** | Built bilateral limbs with mirror blocks |
| **Expected** | `mirror_verify` runs `controls_get(..., rewire=True)` then pairs controls by tag/name |
| **Failure** | Stale `mControlsAll` → missing controls in mirror pass |

### Pattern: Module mirror lookup (`mirror_get`)

| Item | Value |
|------|-------|
| **Setup** | Puppet with multiple same-name modules on one side (e.g. `L_coat_segment_part` and `L_FRNT_coat_segment_part`) |
| **Expected** | `module_utils.mirror_get` resolves the opposite-side module with flipped `cgmDirection` **and** matching CGM name tags (`cgmPosition`, `cgmPositionModifier`, `cgmDirectionModifier`); absent tags compare as `False` |
| **Contract** | Same tag-matching contract as control pairing in `mirror_verify` — do not match only on `cgmName` + `moduleType` + direction when modifiers differ |
| **Failure** | Ambiguous match → `"Shouldn't have found more than one mirror module!"`; animate context may fail downstream if uncaught |

### Pattern: Referenced rig asset

| Item | Value |
|------|-------|
| **Setup** | Puppet/module from referenced file |
| **Expected** | Query functions work; `rewire=True` is no-op (no message writes) |
| **Contract** | Do not expect rewire to repair referenced assets in-place |

---

## Anti-Patterns and Failure Modes

| Anti-pattern | Symptom | Contract |
|--------------|---------|----------|
| Stale `mModulesAll` / `mControlsAll` | Mirror/UI misses modules or controls | Run query with `rewire=True` on non-referenced assets |
| Block parent changed but module tree stale | Wrong attach parent / driver | `blockParent_set` must call `moduleTarget_wire_from_blockParent` |
| Only set `moduleParent` without updating parent's `moduleChildren` | Orphan or duplicate in hierarchy | Always use `parentModule_set` / `parentModule_detach` |
| Iterate+mutate same list in module children walk | Infinite loop / "Max count reached" | Use BFS deque in `moduleChildren_get` (do not regress) |
| Confuse block wiring with module wiring | `is_prerig` fails vs module not on puppet | Block `d_wiring_*` = state null links; module wiring = part graph |
| Rewire on referenced puppet | Unexpected message writes | `rewire` skips when `isReferenced()` |
| Manual `mc.parent` on module without message sync | DAG and module graph diverge | Use utils; `parentModule_set` copies DAG parent from module parent |

---

## Verification Checklist (dev)

Run in Maya after wiring changes:

1. **Master + child blocks** — build spine → limb; verify `modulePuppet`, `moduleParent`, puppet `moduleChildren`, DAG under `partsGroup`
2. **Reparent block** — change `blockParent`; verify `moduleTarget_wire_from_blockParent` updates module tree and attach points
3. **Module cache** — `puppet.atUtils('modules_get', rewire=True)`; `mModulesAll` count matches scene modules
4. **Control rewire** — `mirror_verify` or `controls_get(..., rewire=True)`; no broken `rigNull` / `cgmOwner` links in log
5. **Rig connect** — `rig_connectAll(mode='connect')` constrains skin joints; `rig_disconnect` clears constraints
6. **Referenced asset** — confirm rewire does not write messages; queries still return expected lists

---

## Related Documentation

- **[Feature_SceneExportFlow.md](Feature_SceneExportFlow.md)** — export bake/prep uses puppet/module qss sets (orthogonal)
- **[Feature_DynSimTool.md](Feature_DynSimTool.md)** — dyn drivers collected to puppet `worldSpaceObjects` / `puppetSpaceObjects` groups
- **[Guides/NewFeature_Guide.md](../Guides/NewFeature_Guide.md)** — feature doc conventions

### Code references (py3)

- [`cgm/core/mrs/lib/puppet_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/puppet_utils.py) — `module_connect`, `modules_get`, `controls_get`
- [`cgm/core/mrs/lib/module_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/module_utils.py) — `parentModule_set`, `controls_getDat`, `get_attachPoint`, `rig_connect`
- [`cgm/core/mrs/lib/block_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/block_utils.py) — `puppet_verify`, `moduleTarget_wire_from_blockParent`
- [`cgm/core/mrs/RigBlocks.py`](../../cgmToolsPy3/cgm/core/mrs/RigBlocks.py) — `cgmRigPuppet`, `cgmRigModule`, dispatch methods

---

## Limb segment mid IK (`segmentMidIKSetup`)

Limb **roll** segments (per `numRoll` / `md_roll` index) can expose a mid IK control **`controlSegMidIK_{rollIndex}`**. Spine/neck mids on **Segment** / **Head** still use **`ikMidSetup`** + prerig **`ikMidHelpers`** and **`RIGFRAME.segment_mid`** (full handle chain). **Limb only** uses **`segmentMidIKSetup`** and **`RIGFRAME.limb_segment_mid`** (localized to that roll’s segment handles).

### Block attrs (Limb)

| Attr | Role |
|------|------|
| **`segmentMidIKControl`** | When on (and roll joint count allows): create mid control + **`segmentMidHandles_*`**, shapes, aim on helpers; **always** insert mid into roll segment ribbon **`influences`** when the control exists. |
| **`segmentMidIKSetup`** | How the mid **follows** along the segment span. **`none`** = no extra follow rig (mid still affects segment deformation via influences + aim on seg mid handles). |

**`segmentMidIKSetup`** enum: `none` | `ribbon` | `ribbonLive` | `prntConstraint` | `linearTrack` | `cubicTrack`. Default **`ribbon`** (legacy per-segment mid `IK.ribbon`).

### Follow modes (`limb_segment_mid`)

| Mode | Behavior |
|------|----------|
| **`none`** | Skip **`limb_segment_mid`**; mid remains in **`ml_influences`** and aim constraints on **`segmentMidHandles_*`**. |
| **`ribbon`** | Per-segment `IK.ribbon` on joint list start + mid + end; **`influences`** = **`ml_segHandles`** (seg duplicate handles). |
| **`ribbonLive`** | Same as ribbon but **`liveSurface=True`**, **`extendEnds=True`**, **`sectionSpans`** from **`d_squashStretchIK`** (default **2**). Live loft drivers = **seg end handles only** (mid rides via **`jointList`**, not live influence rails). |
| **`prntConstraint`** | **`mainDriver`** on mid + parentConstraint to **`ml_segHandles`**. |
| **`linearTrack`** / **`cubicTrack`** | **`CORERIG.create_at`** track through ordered **`ml_handleJoints[i:i+2]`** (segment boundary handles, no mid controls); **`BLOCKSHAPES.attachToCurve`** on mid **`masterGroup`** with **`param`** (segment prerig pattern). |

Parent mid **`masterGroup`** to **`mRoot`** only for **`ribbon`** / **`ribbonLive`**; track modes keep **`rig_controls`** parent (blend at roll index).

### Roll segment squash / aim (Limb)

Per-roll **`IK.curve`** / **`IK.ribbon`** in **`limb.rig_segments`** now matches Segment/Head:

- **`skipAim`**: block bool **`squashSkipAim`** (default **True** on Limb, same as Segment).
- **`setupAimScale`**: **True** when **`segmentStretchBy == 'scale'`**, else **False** on ribbon path; curve path sets **`setupAim = 1`** + **`setupAimScale`** when scale stretch.
- **`liveSurface`**: **`segmentType == ribbonLive`** on main roll ribbon build.

**Files**: [`limb.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/limb.py) (`rig_dataBuffer`, `rig_segments`); [`rigFrame_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/rigFrame_utils.py) (`limb_segment_mid`); [`block_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/block_utils.py) (`segmentMidIKSetup` in rig-state vis list); [`shared_dat.py`](../../cgmToolsPy3/cgm/core/mrs/lib/shared_dat.py) (rig + squash UI lists).

**Not in scope**: no **`ikMidDynParentMode`** / extra seg-mid dyn-parent rebuild in **`rig_cleanUp`** (unlike Segment spine mids); pole **`controlIKMid`** is separate from roll seg mids.

---

## Segment `followParentBank`

Organic **Segment** blocks support the same parent-bank rig as **Limb** digits: block bool **`followParentBank`**, rigNull plugs **`followParentBankJoints`**, **`controlFollowParentBank`**, **`bankParentFKDriver`**, **`bankParentIKDriver`**, settings **`visParentBank`** on the bank control shape.

### Defaults

| Block | `followParentBank` default |
|-------|----------------------------|
| **Segment** (`segment.py`) | **`False`** — opt in per block (rig UI / attr). |
| **Limb** (`limb.py`) | **`True`** on digit-style profiles (unchanged). |

Existing Segment blocks keep whatever value is already stored on the node; only **new** blocks pick up the Segment default.

### When it runs

1. Block attr **`followParentBank`** is on.
2. **Parent module** `rigNull` has a live **`pivotResultDriver`** message (typical foot/hand pivot from parent Limb pivot setup).

If (2) fails, build sets **`b_followParentBank`** false and skips bank nodes (same as Limb).

### Build (Segment)

| Step | Role |
|------|------|
| `rig_dataBuffer` | Sets `b_followParentBank`; pushes parent **`pivotResultDriver`** into **`ml_dynParentsAbove`** for space lists. |
| `rig_skeleton` | `followParentBankJoints` chain. |
| `rig_shapes` / `rig_controls` | `controlFollowParentBank`, `visParentBank`. |
| `rig_frame` | Local FK/IK groups (unchanged). |
| **`rig_followParentBankSetup`** | SC IK bank, parent FK/IK blend dags, aim — bank root = **`rigRoot`** (not `limbRoot`). |
| `rig_cleanUp` | Dyn parents: **`followParentBank`** on rig root, first FK, **`controlIK`**, **`controlIKBase`** when drivers exist. |

Works with **FK-only or IK** Segment (`ikSetup` not required for the bank path).

Parent FK/IK blending still reads **parent** `settings.result_FKon` / `result_IKon`; if those attrs are missing on the parent, blend drivers are not created (parent pivot may still appear in space lists via `ml_dynParentsAbove`).

### Space / follow UI (artist-facing)

Dyn-parent menus use each target’s **`cgmAlias`**, not rigNull plug names.

| What you want | What appears in space / orient lists |
|---------------|--------------------------------------|
| Parent foot/hand pivot | Parent pivot’s alias (e.g. `*_PivotResult`) — from **`ml_dynParentsAbove`**. |
| Parent-bank follow (FK/IK switch) | **`followParentBank`** — from **`bankParentFKDriver`** / **`bankParentIKDriver`**. |

Implementation: [`segment.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/segment.py) (`rig_followParentBankSetup`, `rig_cleanUp`). Limb reference: [`limb.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/limb.py) (`rig_pivotSetup`).

---

## Revision History

| Date | Summary |
|------|---------|
| 2026-10-09 | Limb roll seg mid IK: track modes via `attachToCurve`; `squashSkipAim` on roll ribbons; `segmentMidIKControl` vs setup enum contract |
| 2026-10-09 | Segment `followParentBank`: docs (default off, space UI, build table); `rigRoot` bank; parent pivot in `ml_dynParentsAbove` |
| 2026-10-08 | Limb roll seg mid IK: `segmentMidIKSetup` (segment/head keep `ikMidSetup`) |
| 2026-07-21 | Initial feature doc — block/module/puppet message contract, build sync, control rewire, attach points, anti-patterns |
