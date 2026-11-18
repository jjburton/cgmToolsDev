# Feature: MRS Known Issues & Gotchas

## 🎯 Status & Overview
- **Status**: In Progress (living log)
- **Last Updated**: 2026-11-18
- **Owners**: Josh Burton (MRS dev/TA)
- **Purpose**: A running log of MRS build behavior that looks like a bug but is by design, or that is easy to misdiagnose. Each entry gives the symptom, the real cause with file and line references, how to confirm it, and what to check first next time. The aim is to stop debugging sessions from patching build code for behavior that is actually intended.

## 📋 Scope
- **In Scope**:
  - MRS block build steps (`form`, `prerig`, `skeleton`, `rig_*`) whose output surprises people
  - Block attribute interactions that change control orientation, position, or shapes
  - A "check this first" list for common MRS misdiagnoses
- **Out of Scope**:
  - Wiring contracts: see [`Feature_MRSWiring.md`](Feature_MRSWiring.md)
  - Mesh and proxy pipeline: see [`Feature_MRSMeshCreation.md`](Feature_MRSMeshCreation.md)
  - Artist-facing manual text (use the `google-doc-capture` skill)

## 🧩 Architecture
### Entry format
Each issue uses the same sections:

| Field | Content |
|-------|---------|
| **Block / step** | Block type and build function (for example `handle` → `rig_shapes`) |
| **Symptom** | What the user sees in Maya |
| **Looks like** | The wrong diagnosis it invites |
| **Actual cause** | Code path, file:line, and the attribute that drives it |
| **Confirm** | The quickest Maya check that tells the two apart |
| **Resolution** | Attribute change, or "by design, no code change" |

## ⚙️ Implementation Details — Issue Log

MRS-001 (handle block mirrorSetup) is written up in the mrs-handle-animation-orientation branch; merge pending.

### MRS-002: Segment bezier IK root flipped 180° on Left — FK behavior flip leaks into `ikBase = cube`
- **Block / step**: `segment` (`cgm/core/mrs/blocks/organic/segment.py`) → `rig_skeleton` / `rig_shapes` / `rig_controls` / `rig_frame`
- **Symptom**: On a Left segment with `ikSetup = bezier` and `ikBase = cube`, the IK root control (`controlIKBase`) is flipped 180° from `ikJoints[0]`. Rotating or twisting the root goes the wrong way.
- **Looks like**:
  - MRS-001's `mirrorSetup` flip. Segment has no `mirrorSetup` attr.
  - A side-dependent sign in the bezier or spline-IK code. `RIGFRAME.bezier`, `IK.bezier_spline_stretch` and `bezier_ik_block_utils` have no side terms.
- **Actual cause**: the FK behavior flip carries into the IK base.
  - On Left, `rig_skeleton` behavior-flips the FK chain (`segment.py:2804-2807` → `BUILDUTILS.joints_mirrorChainAndConnect` → `joints_flipChainForBehavior`, `builder_utils.py:2653-2675`). It sets `r{d_orientation['str'][2]} = 180` on each joint, then freezes.
  - `RIGSHAPES.ik_base`'s cube (default) branch builds the base dag with `ml_baseJoints[0].doCreateAt()` (`rigShapes_utils.py:635`), which is `fkJoints[0]`, so the root inherits the flip.
  - The flip then carries into bezier main 0, its subs (they are created at the main's orientation, `bezier_ik_block_utils.py:2113`), and the spline advanced-twist start world-up matrix (`rigFrame_utils.py:1023-1056`).
  - `rig_controls` registers `controlIKBase` with `mirrorAxis = "translateX,rotateY,rotateZ"` (`segment.py:3277-3282`), which is wrong for a flipped control.
  - This is related to MRS-001 (the same 180° on `r{str[2]}`), but it is triggered by side through the FK chain, not by the `mirrorSetup` enum. It is a bug, not by design.
- **Confirm**: Compare `controlIKBase` world orientation against `ikJoints[0]` and `fkJoints[0]`. A flipped root matches `fkJoints[0]`, with aim and up negated against the IK joint.
  - Confirmed in Maya: `ikBase = simple` builds correctly, because that branch builds from `ikStartHandle` (`rigShapes_utils.py:609-613`).
  - Not yet confirmed: Centre / Right builds with `cube` are clean (verify in Maya), and `reverseSetup = fkOnly` avoids the root flip because the flip moves to `fkBlendJoints` (verify in Maya).
- **Resolution**:
  - Workaround: set `ikBase = simple`.
  - Guard: a temporary `rig_prechecks` error (`segment.py:2149-2156`) blocks Left + bezier + cube unless `reverseSetup = fkOnly`.
  - Proposed fix (not applied): build the cube base from `ikJoints[0]` or `ikStartHandle`. Every `ik_base` cube user is affected, so test on other block types too.
- **Related findings**:
  - (a) `reverseSetup = fkOnly` with `buildEnd = joint` raised an IndexError in the `rig_shapes` reverse-control loop. `buildEnd = joint` drops the end cast target, so there is one less FK shape than reverse controls. It is fixed by reusing the last FK shape for the end reverse control (`segment.py:3029-3034`). Verify in Maya.
  - (b) Under `fkOnly`, FK and FK-reverse controls are unflipped but keep the translate-only mirrorAxis (`segment.py:3211-3238`). Verify in Maya.
  - (c) Bezier subs under the mids and end are unflipped but registered translate-only on non-Centre sides (`segment.py:3375-3385`). Verify in Maya.

## 🔧 Configuration Guide
### Check-first list for orientation complaints
1. **Segment IK root on Left**: `ikSetup = bezier` with `ikBase = cube` inherits the FK behavior flip (MRS-002).

## ✅ Testing & Validation
- MRS-002: build a Left segment with `ikSetup = bezier`, compare `controlIKBase` to `ikJoints[0]` with `ikBase = cube` (flipped, now blocked by prechecks) and `ikBase = simple` (matches; confirmed in Maya). Centre / Right and `fkOnly` cases: verify in Maya.

## 🧱 Dependencies & Integration
- `cgm/core/mrs/blocks/organic/segment.py`: `rig_prechecks`, `rig_skeleton`, `rig_shapes`, `rig_controls`, `rig_frame`
- `cgm/core/mrs/lib/rigShapes_utils.py`: `ik_base`
- `cgm/core/mrs/lib/builder_utils.py`: `joints_mirrorChainAndConnect`, `joints_flipChainForBehavior`
- `cgm/core/mrs/lib/rigFrame_utils.py`: `bezier`

## 📚 Related Documentation
- **[Feature_MRSWiring.md](Feature_MRSWiring.md)**: MRS wiring contract
- **[Feature_MRSMeshCreation.md](Feature_MRSMeshCreation.md)**: MRS mesh pipeline
- **[Feature_BezierIK.md](Feature_BezierIK.md)**: Segment bezier IK (MRS-002)
- **[Branch_Fall26.md](../Branches/Branch_Fall26.md)**: current branch timeline

## 🚀 Future Work / Ideas
- Add entries as new MRS misdiagnoses come up.

## 📝 Revision History
| Date | Author | Summary |
|------|--------|---------|
| 2026-11-18 | Josh Burton / Claude | MRS-002 segment bezier IK root Left flip (`ikBase = cube`) |
