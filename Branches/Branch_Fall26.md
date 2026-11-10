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
