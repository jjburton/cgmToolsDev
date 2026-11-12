# Branch: jburton/Fall26

## 📋 Quick Info
**Status**: Active  
**Created**: November 10, 2026  
**Last Updated**: November 11, 2026  
**PR**: Pending  
**py3 checkout**: `jburton/Fall26` (cut from `main` at `86b4b39`, after the Face26 merge — `__BRANCH` = `Fall26`, `__RELEASE` = `26.11.06.01` in `cgm_General.py`)

## 🎯 Goals
[2-3 sentence summary of what this branch accomplishes — TBD. Fall 2026 working branch following the Face26 and BezierIK merges.]

## 📚 Related Documentation
- **[Branch_Face26.md](Branch_Face26.md)** - Previous branch (merged via PR #19); facial block, Segment, and cgmMeta hierarchy work
- **[Branch_BezierIK.md](Branch_BezierIK.md)** - Previous branch (merged via PR #18); Bezier/spline IK and ShotList UI
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch doc format
- **[Feature_MRSPivots.md](../Features/Feature_MRSPivots.md)** - MRS pivot pipeline, ballRotate frames
- **[Feature_SceneExportFlow.md](../Features/Feature_SceneExportFlow.md)** - Scene export pipeline; rig naming / unbaked rig options

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

### November 11, 2026 - Shot list refreshes on scene open
**What**: Open Shot list (`Shots.ShotUI`, "Sub Animation List") now reloads its rows on Maya **SceneOpened** (File → Open / New) — same pattern as Builder, setTools, cgmDynSimTool.  
**Files**: 
- EXTENDED: `cgm/core/mrs/Shots.py` (`CreateWindow` scriptJob, `uiFunc_on_scene_change`, `uiFunc_refresh_after_scene_open`, `LoadAnimList` reset)

**Features**:
- `SceneOpened` scriptJob parented to the window → `mc.evalDeferred(..., lp=True)` → `RefreshShotListUI()`
- `LoadAnimList` clears `animDict` / `animList` / `animListNode` first, so a scene with no `AnimListNode` shows an empty list instead of the previous scene's shots

**Decisions**:
- `ShotUI` is a raw `mc.window`, not a zoo `BaseMelWindow`, so it calls `mc.scriptJob(event=('SceneOpened', ...), parent=self.window)` directly instead of `setSceneChangeCB`

**Status**: 🔄 Verify in Maya (open scene with shots → open scene without → File → New)

### November 11, 2026 - Scene rig export naming + unbaked rig export
**What**: Two new project export options for Scene rig export (mode 3): pick the rig FBX name source, and skip bake/animation on rig export.  
**Files**: 
- EXTENDED: `cgm/core/mrs/lib/scene_export_utils.py` (`rig_export_file_name`, `resolve_rig_export_file_name`; `sub_asset` / `variation` / `rig_export_name` on `resolve_export_fbx_paths`)
- EXTENDED: `cgm/core/mrs/Scene.py` (`ExportScene` kwargs `rigExportName`, `bakeRigExport`, `variation`; `RunExportCommand`, `batch_buildFile`, `BatchExport` wiring)
- EXTENDED: `cgm/core/tools/lib/project_utils.py` (`_exportOptionSettings`: `rigExportName`, `bakeRigExport`)
- EXTENDED: `cgm/core/cgm_General.py` (`fbx_export_preamble(include_animation=)`)
- EXTENDED: `cgm/assets/example_project.cfg`
- EXTENDED: `Features/Feature_SceneExportFlow.md` (cgmToolsDev)

**Features**:
- **Rig export naming** (`rigExportName`): `namespace` (default, legacy `{refNamespace}_rig.fbx`) or `generated` (`{asset}_{subAsset}_{variation}_rig.fbx`, e.g. `Crate_Hero_red_rig.fbx`; `rig` always last, missing tokens dropped)
- **Bake rig export** (`bakeRigExport`, default **off**): rig export skips `Bake()` and writes FBX with the Animation group off; prep + FBX still run. On = legacy bake
- Preflight and `ExportScene` share one name resolver, so planned path = written path

**Decisions**:
- Asset token for `generated` = `exportAssetPath` leaf (browser asset), so interactive and batch agree without a new kwarg
- Sub asset / variation are Sets / Variation list **folders** only (version files in those lists are ignored)
- Fixed batch payload key mismatch: RunExportCommand wrote `subSet`, BatchExport read `set` — now reads `subSet` with `set` fallback; batch queue now sends `subSet` + `variation`
- Multi-root rig (combined FBX) still uses browser `exportName` — not changed

**Status**: ✅ Verified in Maya (user)

### November 12, 2026 - Scene Replace File prompts P4 checkout
**What**: Scene file-row right-click **Replace File** now runs the normal P4 checkout / writability prompt before overwriting, instead of failing on a read-only (not checked out) file.  
**Files**: 
- EXTENDED: `cgm/core/mrs/Scene.py` (`file_replace`)
- EXTENDED: `Features/Feature_PerforceIntegration.md` (cgmToolsDev — Replace File added to wired callers)

**Features**:
- After the "Replacing : …" confirm, calls `PATHUTIL.prepare_maya_scene_for_save(filePath, mDat=self.mDat)` — same path as Save As / Save Version; cancel or checkout failure logs and aborts before `mc.file(s=True)`
- Refreshes browser lists (`_republish_navigation_lists`) after save so the row's P4 status updates

**Decisions**:
- Kept the existing overwrite confirm; the checkout prompt follows it (two dialogs: overwrite intent, then P4)

**Status**: ✅ Verified in Maya (user)

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
