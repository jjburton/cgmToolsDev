# Branch: jburton/Fall26

## 📋 Quick Info
**Status**: Active  
**Created**: November 10, 2026  
**Last Updated**: November 10, 2026  
**PR**: Pending  
**py3 checkout**: `jburton/Fall26` (cut from `main` at `86b4b39`, after the Face26 merge — `__BRANCH` = `Fall26`, `__RELEASE` = `26.11.06.01` in `cgm_General.py`)

## 🎯 Goals
[2-3 sentence summary of what this branch accomplishes — TBD. Fall 2026 working branch following the Face26 and BezierIK merges.]

## 📚 Related Documentation
- **[Branch_Face26.md](Branch_Face26.md)** - Previous branch (merged via PR #19); facial block, Segment, and cgmMeta hierarchy work
- **[Branch_BezierIK.md](Branch_BezierIK.md)** - Previous branch (merged via PR #18); Bezier/spline IK and ShotList UI
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch doc format
- **[Feature_MRSPivots.md](../Features/Feature_MRSPivots.md)** - MRS pivot pipeline, ballRotate frames

## 🗓️ Timeline

### November 10, 2026 - Branch Created
**What**: Created `jburton/Fall26` in cgmToolsPy3 from `main` after the Face26 merge; started this branch doc  
**Files**: 
- NEW: `Branches/Branch_Fall26.md` (cgmToolsDev)
- EXTENDED: `cgm/core/cgm_General.py` (`__BRANCH` = `Fall26`)

**Features**:
- Release metadata branch string set to Fall26

**Decisions**:
- Branch starts from a clean `main` (no commits ahead yet)

**Status**: ✅ Complete

### November 10, 2026 - ballRotate pivot on rotated ground plane
**What**: Handle/Segment `addPivot = ballRotate` rolled wrong when the base pivot wasn't world-aligned, and sank into the ground at 45°.  
**Files**: 
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` (`pivots_setup`, ballRotate branch)
- NEW: `Features/Feature_MRSPivots.md` (cgmToolsDev)

**Features**:
- `ballRoll` group (zeroed in tilt frame, parented before wiring) receives roll translate; `ballSpin` child at ball center receives rotation; `pivotResult` parents under `ballSpin`
- Radius = half `pivotBall` bbox (was full diameter)

**Decisions**:
- Ground plane = `base_pivotHelper` frame (artist-rotatable); ball center/size = `ball_pivotHelper`
- Handle with `rotPivotPlace = jointHelper` needs the joint helper aligned to the base pivot space — documented, not enforced (no helper yet)

**Status**: ✅ Verified in Maya (user, with joint helper aligned)

---

### November 16, 2026 - Prerig-authored bezier (`ikSplineBezierMode=prerig`)
**What**: Auto-generated bezier curves didn't follow joint flow. New `ikSplineBezierMode` value `prerig` builds an editable bezier at prerig that places the joints and is the curve the rig's bezier IK uses. Sub-branch `jburton/Fall26_bezierPrerig` (cgmToolsPy3).  
**Files**: 
- EXTENDED: `cgm/core/mrs/lib/shared_dat.py` (`ikSplineBezierMode` enum adds `prerig`)
- EXTENDED: `cgm/core/mrs/lib/bezier_ik_block_utils.py` (`block_bezier_prerig_curve_active` gate, `bezier_prerig_curve_copy_for_rig`, shared prerig build: `prerig_bezier_curve_build`, `prerig_bezier_handles_ride`, `prerig_attach_to_curve_fraction`, `prerig_parent_world_space`)
- EXTENDED: `cgm/core/mrs/blocks/organic/head.py`, `segment.py` (`prerig`, `create_jointHelpers`)
- EXTENDED: `cgm/core/mrs/lib/rigFrame_utils.py` (`bezier` → `useBezierCurve`), `cgm/core/rig/ik_utils.py` (`bezier_spline(driverMatchBezier=)`)
- EXTENDED: `cgm/core/lib/curve_Utils.py` (`getPercentPointOnCurve` accepts bezierCurve; `create_bezier_nurbs_curve(bezier=)`), `cgm/core/mrs/lib/block_utils.py` (`controls_get` appends tangent handles last)
- UPDATED: `Features/Feature_BezierIK.md` (§ Prerig-authored bezier)

**Features**:
- Bezier anchors = first prerig handle, ikMid helpers, last prerig handle; tangent handles per anchor (decomposeMatrix → CVs), anchor → tangent lines, bezier-order pickwalk
- Interior prerig handles and joint helpers ride the bezier by arc length (motionPath fractionMode)
- Rig copies the prerig curve; spline IK driver is an exact nurbs copy of the bezier (`driverMatchBezier`)

**Decisions**:
- Hard gate: Head `neckIK=bezier` / Segment `ikSetup=bezier` **and** mode `prerig` — everything else unchanged
- Joints ride the bezier, not `drivenCurve` — measured up to ~2 units off, caused the IK-on jump
- ikMid anchors follow the form-only track curve to avoid a DG cycle

**Status**: ✅ Head verified in Maya (joints + IK driver 0.0 off the bezier at rest) · ⏳ Segment port — verify in Maya

---

## 📦 Deliverables

### [Phase/Feature Name]
- [ ] Task 1
- [ ] Task 2

### Testing
- [ ] Code implementation complete
- [ ] No linter errors
- [ ] Documentation updated
- [ ] Maya testing complete

---

## 🚀 PR Notes

**IMPORTANT**: Use HTML entities for angle brackets in regular text: Func&lt;string&gt; not `Func<string>`. Code blocks are fine.

### [PR Title]

#### Overview
[Brief overview of the PR]

#### Major Features

##### 1. [Feature Name] ✨
[Description]

**Files Modified:**
- `File1.py` - Description

#### Technical Details

##### [Feature Name] Implementation

Use 4-space indented code blocks for code examples (not triple backticks):

    def example(mObj):
        # Key code example
        pass

#### Architecture Decisions

1. **Decision 1**: Rationale

#### Testing

##### [Feature Name]
- ⏳ Verify in Maya

#### Documentation Updated
- ✅ `Branch_Fall26.md` - Created

#### Breaking Changes
None

#### Next Steps
- [TBD]

---

**Ready for Review** - Not yet

---

## 📝 Notes

### Architectural Patterns Established
- [TBD]

### Lessons Learned
- [TBD]

### Future Considerations
- [TBD]

---

*Last Updated: November 10, 2026*  
*Branch Status: Active*
