# Feature: MRS Pivots (addPivot / pivotHelper / ballRotate)

## 🎯 Status & Overview
- **Status**: In Progress (overview + ballRotate fix, Fall26)
- **Last Updated**: November 10, 2026
- **Owners**: Josh Burton
- **Purpose**: MRS blocks (Handle, Segment, Limb) can add a pivot rig above the main control — foot-style
  roll/bank/spin pivots, a wobble/tilt, or a rolling ball. Prerig places helpers; rig build duplicates them into
  pivot controls, chains them under the driving control, and ends the chain in a **`pivotResult`** null that the
  rest of the module follows. This doc is the agent-facing overview of that pipeline and its frame invariants.

## 📋 Scope
- **In Scope**:
  - Block attr **`addPivot`** (`none:simple:wobbleAdd:wobbleOnly:ballRotate`) and **`pivotDriverSetup`** (`default:dynParent`)
  - Prerig helper build (`BLOCKSHAPES.pivotHelper` + block-specific tilt/spin/ball helpers)
  - Rig shapes (`RIGSHAPES.pivotShapes`), control registration, and `BLOCKUTILS.pivots_setup`
  - **ballRotate** auto-roll (`RIGUTILS.add_ball_auto_roll`)
- **Out of Scope**:
  - Limb IK foot roll specifics (`limb.py` uses `pivots_setup` with `rollSetup='human'` etc.) beyond noting the shared entry
  - Scale pivot (`addScalePivot`) and space pivots (`numSpacePivots`)

## 🧩 Architecture

### Pipeline
```
prerig                         rig_shapes                      rig_controls          rig_frame
──────                         ──────────                      ────────────          ─────────
pivotHelper (base_pivotHelper) RIGSHAPES.pivotShapes           MODULECONTROL.register pivotResult = <driver>.doCreateAt()
 ├ pivotCenter / front / …      dup each prerig pivot           each 'pivot*' on       BLOCKUTILS.pivots_setup(
 ├ pivotTilt  (ballRotate,      → mRigNull.pivot<Name>          rigNull (masterGroup)    mControl, mRigNull,
 │   wobble*)                   tilt/spin: dup of pivotCenter                            pivotResult, setup, …)
 ├ pivotSpin                     (front for wobble tilt) with                          → pivotResult.parent = mLastParent
 └ pivotBall  (ballRotate)       the helper's shape parented in
```

- **`pivots_setup`** walks **`l_pivotOrder`**, parents each pivot's `masterGroup` under the previous pivot's
  **`drivenGroup`** (first one under **`mDag`** = `mControl`, or `mDeformNull` for `pivotDriverSetup=dynParent`),
  wires setup-specific attrs, and finally parents **`pivotResult`** under **`mLastParent`** (keeps its world transform).
- **`pivotResult`** is the module's downstream driver: Handle parents the direct joint's `masterGroup` under it
  (`pivotDriverSetup=default`); Segment uses it as the new root (`mRoot`). Message: `rigNull.pivotResultDriver`.

### Pivot orders by `addPivot`
| `addPivot` | `l_pivotOrder` | `setup` | Notes |
|------------|----------------|---------|-------|
| `simple` | `center, front, back, left, right` (shared default) | `default` | roll / bank / spin attrs on `mControl` |
| `wobbleAdd` | `center, back, front, left, right, spin, tilt` | `default` + `setupWobble` | no per-pivot spin |
| `wobbleOnly` | `spin, tilt, center` | `wobble` + `setupWobble` | tilt counter-spins spin |
| `ballRotate` | `spin, tilt` | `ballRotate` | auto-roll, see below |

### Frames (the part that bites)
- **`base_pivotHelper`** (`block.pivotHelper`) defines the **ground plane**: its Y is up for the setup, and the
  artist may rotate it to any plane.
- Prerig sub-pivots (`pivotCenter`, …) are created at the block's orientation and follow the base through a
  `track` group parentConstrained to a child of the base, so they keep the base's frame.
- Rig `tilt` / `spin` are **duplicates of `pivotCenter`**, so their rotate axes are the ground frame.
- `pivotResult` is created at the **driving control** (Handle: `mHandle`; Segment: first FK joint), so its own
  orientation is the control's — *not* the ground frame.

### ballRotate
Prerig (Handle `prerig`, Segment `prerig`): `ball_pivotHelper` (`pivotBall`) is a scaled sphere that defines the
ball **center and size**; `pivotTilt` / `pivotSpin` live under the base.

Rig (`pivots_setup`, `setup == 'ballRotate'`):
```
spin.drivenGroup
 └ tilt.masterGroup … tilt               (animator rotates tilt; sits on the ground contact)
 └ <tilt parent>
    └ ballRoll   (at tilt, tilt orient)   ← tx/tz from tilt rx/rz (rad × radius); identity rest transform
       └ ballSpin (at ball center, tilt orient, tilt rotateOrder) ← tilt.rotate
          └ pivotResult                    (keeps handle-space offset/orient)
```
- `tilt.ballRollGroup` / `tilt.ballSpinGroup` messages point at the two groups.
- Radius = half the world bbox of `pivotBall` → stored on `tilt.radius`; `tilt.translateDrive`,
  `invertRotX_to_Z` (default on), `invertRotZ_to_X` (default off) are added by `add_ball_auto_roll`.
- Invariants:
  1. `add_ball_auto_roll` connects **local** channels. The node receiving translate must have an identity rest
     transform in the tilt frame, and must be parented **before** wiring (connected channels can't compensate
     on reparent).
  2. Rotation happens at the **ball center**, translation on the **ground plane** — rotating at the contact point
     sinks the ball (center drops to r·cos θ).
  3. Rotate order of the rotation receiver matches the tilt (`pivots_setup` sets pivots to `rotateOrder = 2`).

## ⚙️ Implementation Details

### Files & Responsibilities
| File | Responsibility |
|------|----------------|
| [`mrs/blocks/simple/handle.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/simple/handle.py) | `addPivot` attrs; prerig helpers (~`if self.addPivot`); `rig_shapes` → `pivotShapes`; `rig_controls` registers `pivot*`; `rig_frame` creates `pivotResult` and calls `pivots_setup` |
| [`mrs/blocks/organic/segment.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/segment.py) | Same prerig helpers; pivot setup in the IK/frame pass; `pivotResultDriver` becomes `mRoot` for ballRotate |
| [`mrs/blocks/organic/limb.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/limb.py) | Foot pivots via the same `pivots_setup` (human/ik roll) |
| [`mrs/lib/blockShapes_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/blockShapes_utils.py) | `pivotHelper` — base + sub-pivot prerig helpers, track constraints |
| [`mrs/lib/rigShapes_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/rigShapes_utils.py) | `pivotShapes` — duplicate prerig pivots into rig pivots on `rigNull` |
| [`mrs/lib/block_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/block_utils.py) | `pivots_setup` — chain, attrs, wobble, ballRotate groups, `pivotResult` parent |
| [`lib/rigging_utils.py`](../../cgmToolsPy3/cgm/core/lib/rigging_utils.py) | `add_ball_auto_roll` — generic rotate→translate rolling wiring |
| [`mrs/lib/shared_dat.py`](../../cgmToolsPy3/cgm/core/mrs/lib/shared_dat.py) | `_l_pivotOrder`, `_d_pivotBankNames` |

## 🔧 Configuration Guide
- **`addPivot`** — choose the pivot rig. **`pivotDriverSetup`** — `default` hangs pivots under the control;
  `dynParent` hangs them under `mDeformNull` (parentConstrained to the driver point) and adds `pivotResult` as a dyn parent.
- **ballRotate prerig setup**:
  1. Rotate/position **`base_pivotHelper`** to define the ground plane (its Y = up).
  2. Position and scale **`ball_pivotHelper`** for ball center and size.
  3. **Handle with `rotPivotPlace = jointHelper`: align the joint helper's orientation to the base pivot's space.**
     The main control and direct joint take their frame from the joint helper; if it doesn't match the ground
     frame, the roll reads wrong even though the ball wiring is correct. Not enforced in code yet.

## ✅ Testing & Validation
Manual, in Maya (rebuild rig after `cgmGEN._reloadMod` of `block_utils`):
- [ ] ballRotate, base pivot at world: tilt rx / rz roll the ball; contact stays on the ground at 45° and 90°
- [ ] ballRotate, base pivot rotated + joint helper aligned: same, along the rotated plane
- [ ] Move/rotate root and main control, then tilt: ball rolls on the carried ground plane, no pop at rest
- [ ] 360° tilt ≈ one circumference (2πr) of travel
- [ ] Segment ballRotate builds (`pivotResultDriver` as root)
- [ ] `simple` / `wobble*` unchanged

## 🧱 Dependencies & Integration
- Control registration (`MODULECONTROL.register`) supplies `masterGroup`; `pivots_setup` errors per pivot without it.
- Handle `rig_cleanUp` adds `pivotResultDriver` to dyn parents when `pivotDriverSetup = dynParent`.
- See [`Feature_MRSWiring.md`](Feature_MRSWiring.md) for module/attach wiring around the pivot result.

## 📚 Related Documentation
- **[Branch_Fall26.md](../Branches/Branch_Fall26.md)** – ballRotate fix timeline
- **[Branch_Face26.md](../Branches/Branch_Face26.md)** – `pivotResult` naming / `pivotResultDriver` message history

## 🚀 Future Work / Ideas
- Warn (or auto-align) at rig build when Handle's joint helper orientation doesn't match `base_pivotHelper` for ballRotate.
- Take the ground frame straight from `base_pivotHelper` instead of via `pivotCenter`.
- Radius from the ball's local shape size × scale instead of the world bbox (rotated / non-uniform ball).
- Euler mapping (rx→tz, rz→tx) is exact per axis only; combined rolls are an approximation.

## 📝 Revision History
| Date | Author | Summary |
|------|--------|---------|
| 2026-11-10 | Josh Burton / Claude | Initial overview; ballRotate `ballRoll` / `ballSpin` groups, radius fix, joint-helper alignment note |
