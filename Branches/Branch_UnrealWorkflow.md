# Branch: jburton/UnrealWorkflow

## 📋 Quick Info
**Status**: Active  
**Created**: April 23, 2026  
**Last Updated**: June 5, 2026 (MetaHuman facial skeleton prune; Maya Be Odd cascade UI windows)  
**PR**: Pending

## 🎯 Goals
Harden Scene export behavior so Unreal-oriented exports are consistent, repeatable, and predictable for animation and rig workflows. Track export issues and fixes in one place, with explicit validation criteria and PR-ready notes.

## 📚 Related Documentation
- **[Scene.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Scene.py)** - Main Scene UI, `RunExportCommand`, `ExportScene`, `BatchExport`, `SendToBuild`
- **[Builder.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Builder.py)** - `ui_toStandAlone` (MRS Build), `uiFunc_process` batch / logging
- **[Project.py](../../../repos/cgmToolsPy3/cgm/core/tools/Project.py)** - `Project.data`, `fillDefaults` (project picker / version menus)
- **[RigBlocks.py](../../../repos/cgmToolsPy3/cgm/core/mrs/RigBlocks.py)** - `cgmRigMaster.rebuildMasterShapes` (batch rig / master controls)
- **[bakeAndPrep.py](../../../repos/cgmToolsPy3/cgm/core/tools/bakeAndPrep.py)** - Bake, Prep, `ProcessDeleteSet`, `resolve_td_set_for_asset`, texture breaking
- **[path_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/path_utils.py)** - Export output writability check, `.bak` sidecar cleanup, `ExportOutputNotWritableError`, non-writable path session list
- **[batch_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/batch_utils.py)** - Mayapy batch preflight (`ensure_fbx_plugin` before Scene import)
- **[project_utils.py](../../../repos/cgmToolsPy3/cgm/core/tools/lib/project_utils.py)** - Lazy `get_fbx_versions()` (no import-time FBX MEL probe)
- **[animFilterTool.py](../../../repos/cgmToolsPy3/cgm/core/tools/animFilterTool.py)** - Anim post filters UI (`VERIFY_CLOSE` / `confirmClose`)
- **[baseMelUI.py](../../../repos/cgmToolsPy3/cgm/core/lib/zoo/baseMelUI.py)** - `BaseMelWindow` close hooks (`VERIFY_CLOSE`, `restoreAfterCloseCancelled`)
- **[cgm_General.py](../../../repos/cgmToolsPy3/cgm/core/cgm_General.py)** - Shared helpers (`playback_stop`, logging); `ensure_fbx_plugin`, FBX export preamble/selection helpers
- **[PostBake.py](../../../repos/cgmToolsPy3/cgm/core/classes/PostBake.py)** - Post filters bake loop (AnimFilter dragger/spring/etc.)
- **[locinator.py](../../../repos/cgmToolsPy3/cgm/core/tools/locinator.py)** - `bake_match` timeline bake
- **[curve_Utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/curve_Utils.py)** - `align_eps_by_lane_projection`, `distribute`
- **[shape_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/shape_utils.py)** - `get_nonintermediate` (canonical live shape resolution)
- **[toolbox.py](../../../repos/cgmToolsPy3/cgm/core/tools/toolbox.py)** - Snap **Ratio** row; Controls **tweak** row (`buildRow_tweakCurve`)
- **[snapTools.py](../../../repos/cgmToolsPy3/cgm/core/tools/snapTools.py)** - Snap **Ratio** row (shared with toolbox)
- **[joint_utils.py](../../../repos/cgmToolsPy3/cgm/core/rig/joint_utils.py)** - `pruneSkeletonToJoints` (MetaHuman / facial skeleton strip to keep-list + root chain)
- **[mayaBeOdd_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/mayaBeOdd_utils.py)** - Maya Be Odd helpers (`cascade_mc_windows`, outliner/panel cleanup)
- **[tool_chunks.py](../../../repos/cgmToolsPy3/cgm/core/tools/lib/tool_chunks.py)** - Snap/marking menu **Arrange → Ratio**; **Point Special → Ground**; Loc **Ground Pos**; `buildRows_ratio_arrange`; **Maya Be Odd → Cascade UI Windows**
- **[snap_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/snap_utils.py)** - `to_ground`, `ground_position_get`
- **[snap_calls.py](../../../repos/cgmToolsPy3/cgm/core/tools/lib/snap_calls.py)** - `get_special_pos` (`groundPos`), `snap_action` ground mode
- **[position_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/position_utils.py)** - `scene_up_axis_get`, `ground_plane_up_index`, `position_project_to_ground_plane`, scene-up **bottom**/**top** in `get_bb_pos`
- **[transform_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/transform_utils.py)** - `ground_position_get` re-export
- **[mayaSettings_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/mayaSettings_utils.py)** - `sceneUp_get()` (Maya `upAxis`)
- **[arrange_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/arrange_utils.py)** - `alongRatio`, `alongRatio_prompt`, golden/finger presets
- **[general_utils.py](../../../repos/cgmToolsPy3/cgm/core/rig/general_utils.py)** - `ratio()` shim to `alongRatio`
- **[block_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/block_utils.py)** - `prerig_handlesLayoutRatio`, `prerig_arrangeRatio_menuDict`
- **[ml_breakdown.py](../../../repos/cgmToolsPy3/cgm/core/lib/ml_tools/ml_breakdown.py)** - Optional diagnostics touchpoint
- **[NewBranch_Guide.md](./NewBranch_Guide.md)** - Branch documentation format reference
- **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)** - P4 checkout/add for FBX export (planning)

## 🗓️ Timeline

### June 5, 2026 - MetaHuman facial skeleton prune + Maya Be Odd cascade UI windows
**What**: Added a joint-prune helper for MetaHuman facial prep (keep listed joints plus parent chain to root; delete all other joints under that hierarchy) and a dev toolbox action to cascade visible `mc.window` UIs onscreen when many tool windows pile up during rig/export debugging.  
**Files**:
- EXTENDED: `cgm/core/rig/joint_utils.py` — `pruneSkeletonToJoints(jointsToKeep, delete=True, report=True)`; walks up joint parents to root into keep set; deletes other joints under root(s) deepest-first; dry-run via `delete=False`
- EXTENDED: `cgm/core/lib/mayaBeOdd_utils.py` — `cascade_mc_windows(start_x, start_y, step_x, step_y, skip, verbose)`; moves visible Maya UI windows in a screen cascade (skips `MayaWindow` by default)
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — **Maya Be Odd → Cascade UI Windows** menu item

**Features**:
- **Facial skeleton strip**: pass joints to keep (facial set); spine/neck path to root preserved; side branches (body, extra facial) pruned — supports MetaHuman facial wiring workflows (`TechAnimation/Maya/ProjectScripts/MetahumanFacial.py` usage pattern)
- **Cascade UI Windows**: cgmToolbox **Maya Be Odd:** submenu; logs moved window names to Script Editor

**Decisions**:
- Skeleton prune lives in **`joint_utils`** (rig joint IO), not `face_utils` — general keep-list + root-chain behavior, reusable beyond one facial script
- `pruneSkeletonToJoints` does **not** clean skin clusters or other joint connections; run on dup or expect skin/bind fixes
- Cascade helper in **`mayaBeOdd_utils`** with toolbox wiring only (no artist manual / Google Doc scope)

**Status**: ✅ Complete (Maya runtime verification user-side for prune; cascade is dev ergonomics)

---

### June 4, 2026 - Scene-up-aware ground snap (unified groundPos / to_ground)
**What**: Fixed ground snap math for **Z-up** Maya scenes. Previously `to_ground` and `groundPos` assumed Y-up (ymin BB bottom, force `Y=0`). Centralized scene-up plane logic in `position_utils` and routed snap UI, loc creation, and master-block selection snap through shared helpers.  
**Files**:
- EXTENDED: `cgm/core/lib/position_utils.py` — `scene_up_axis_get()` (wraps `MAYASET.sceneUp_get`), `ground_plane_up_index()`, `position_project_to_ground_plane()`, `ground_bottom_position_get()`; `get_bb_pos` **bottom**/**top** use min/max along scene up (Y or Z)
- EXTENDED: `cgm/core/lib/snap_utils.py` — `ground_position_get(obj, mode='pivot'|'bottom')` (query); `to_ground()` uses up index + `ground_bottom_position_get`
- EXTENDED: `cgm/core/lib/transform_utils.py` — `ground_position_get = SNAP.ground_position_get`
- EXTENDED: `cgm/core/tools/lib/snap_calls.py` — `groundPos` branch calls `SNAP.ground_position_get` (was hardcoded `[x,0,z]`)
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — Point Special menu **Ground** (removed WIP label)
- UNCHANGED API (benefit from fix): `cgm/core/mrs/RigBlocks.py` master create `targetPivot='groundPos'`; `cgm/core/mrs/lib/blockShapes_utils.py` `SNAP.to_ground`

**Features**:
- **Point Special → Ground**: moves selection so shape BB **bottom** sits on ground plane (`scene up = 0`)
- **Loc → Ground Pos** / **`groundPos` snap pivot**: projects rotate pivot onto ground plane (keeps other axes)
- **Master block + selection size**: placement snap uses same `groundPos` query (via `get_special_pos`)
- **Y-up and Z-up**: ground plane component is index 1 or 2 per `mc.upAxis`

**Decisions**:
- Two behaviors kept: **query** (pivot projection) vs **action** (BB-bottom move) — only axis math is shared
- Low-level helpers in **`position_utils`** (imports `mayaSettings_utils`); snap API in **`snap_utils`**; public query alias on **`transform_utils`** (avoids SNAP↔TRANS import cycle)
- `get_bb_pos` front/back/left/right modes unchanged (out of scope)

**Status**: ✅ Complete (Maya Y-up / Z-up runtime verification user-side)

---

### June 1, 2026 - Export prep/bake tdSets, FBX bootstrap, writable paths, export summary
**What**: Hardened batch/standalone export for nested reference namespaces (e.g. `M_MED_Base_APose:M_MED_Base_Head:root`), fixed mayapy FBX MEL spam at import, fail-fast on read-only depot FBX targets with batch reporting, and added end-of-run export summaries (shots + UP axis). Full Perforce `p4 edit` integration deferred.  
**Files**:
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `resolve_td_set_for_asset()` walks namespace prefixes outer→inner for `bake_tdSet` / `export_tdSet` / `delete_tdSet`; `Bake()` uses it; `Prep()` resolves export/delete sets after outer namespace merge, optional missing delete set, namespace merge instead of per-DAG rename loop
- EXTENDED: `cgm/core/lib/path_utils.py` — `ExportOutputNotWritableError`, `check_export_output_writable()`, `cleanup_fbx_export_sidecars()`, session list `clear/record/get_non_writable_export_paths()`
- EXTENDED: `cgm/core/cgm_General.py` — `ensure_fbx_plugin()` (reload + MEL source fallback); `fbx_export_preamble` / `fbx_export_shot_time_range` / `fbx_export_selection` (delegates writability to `path_utils`); `get_mayaFBXVersionsAvailable()` no longer probes 2010–2050 at import
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — lazy `get_fbx_versions()`; removed import-time `get_mayaFBXVersionsAvailable()` call
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — mayapy `l_pre`: `ensure_fbx_plugin` **before** `import Scene` (avoids `FBXExportFileVersion` spam from `project_utils` import)
- EXTENDED: `cgm/core/mrs/Scene.py` — FBX export paths use `cgmGEN` helpers; `_finalize_fbx_export_error` for `ExportOutputNotWritableError`; `BatchExport` clears/lists non-writable paths; `log_export_results_summary()` + `logExportSummary` flag (batch suppresses per-scene duplicate); records per-shot exports with frame ranges + **UP axis** query

**Features**:
- **Bake set**: finds `RefNamespace:bake_tdSet` when export root is `Ref:Inner:root` (not only full nested prefix)
- **Prep**: export set at root after APose merge; missing delete set is warning-only; final namespace via `mergeNamespaceWithRoot`
- **Writable check**: fails before `FBXExport` with checkout hint; removes editable `.bak` sidecars only
- **Batch summary**: non-writable paths block at end; successful exports listed once (`Batch export summary`) with shot name, frames, path, UP axis
- **Standalone export**: same summary via `logExportSummary=True` (default)

**Decisions**:
- Path/write helpers live in **`path_utils`**, not `cgm_General` (keeps General Maya/FBX-only)
- No `p4 edit` / auto `p4 add` in this pass — artists checkout manually; clearer errors replace opaque FBX I/O failures
- Batch runs one summary at end, not per-scene + batch duplicate

**Status**: ✅ Complete (user verified Crate per-shot export + writable-path behavior)

---

### May 27, 2026 - Prerig ratio arrange (golden / finger / custom prompt)
**What**: Generalized proportional handle spacing for snap arrange and MRS prerig workflows. Replaced rigid 4-node finger `ratio()` with `alongRatio` (N controls, first/last fixed). Golden preset uses a true geometric φ chain (not equal weights). Custom entries prompt for one ratio or comma-separated segment weights.  
**Files**:
- EXTENDED: `cgm/core/lib/arrange_utils.py` — `PHI`, `_ratio_weights`, `_ratio_cumulative_fractions`, `_ratio_parse_weights_input`, `alongRatio` (linear + cubic/arc/target curves), `alongRatio_prompt`; `_d_arrangeRatio_ann`
- EXTENDED: `cgm/core/rig/general_utils.py` — `ratio()` delegates to `ARRANGE.alongRatio` (no 4-node assert)
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — `_ui_arrange_ratio` (Snap → Arrange submenu); `buildRows_ratio_arrange` (toolbox + snapTools)
- EXTENDED: `cgm/core/tools/toolbox.py`, `cgm/core/tools/snapTools.py` — Snap section **Ratio** / **Ratio custom** button rows via `UICHUNKS.buildRows_ratio_arrange`
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — `prerig_handlesLayout_getHandles`, `prerig_handlesLayoutRatio`, `prerig_arrangeRatio_menuDict`; refactored `prerig_handlesLayout` to shared handle resolver
- EXTENDED: `cgm/core/mrs/Builder.py` — block menu **Prerig** (picker, editor, context): `**BLOCKUTILS.prerig_arrangeRatio_menuDict(...)` after existing Linear/Cubic arrange items

**Features**:
- **Presets (no prompt)**: Golden, Golden | Curve, Finger, Finger | Curve
- **Custom (prompt)**: Custom, Custom | Curve — one number → geometric chain; comma list → explicit per-segment weights (root → tip)
- Span preserved along straight A→D (linear) or rebuilt/reference curve (cubic); middle prerig/snap controls move only
- MRS block menu uses same ratios on prerig handle index range as `prerig_handlesLayout`

**Decisions**:
- `golden_all` weights are `ratio^(n-1)…ratio^0` per segment — equal `[φ,φ,φ]` was removed (normalized to even spacing)
- No **Custom | Finger** menu entry (finger preset covers one-click; custom defaults to φ)
- Ratio UI centralized in `tool_chunks.buildRows_ratio_arrange` / `prerig_arrangeRatio_menuDict` to avoid drift across toolbox, snapTools, and Builder

**Status**: ✅ Complete (Maya runtime verification user-side)

---

### May 27, 2026 - Curve EP lane alignment + distribute (toolbox Controls tweak row)
**What**: Added lane-projection EP alignment for middle curves between start/end guides, exposed it and existing `distribute` on the toolbox **Controls → tweak** row, and unified duplicate `get_nonintermediate` helpers without introducing a `distance_utils` ↔ `shape_utils` import cycle.  
**Files**:
- EXTENDED: `cgm/core/lib/curve_Utils.py` — `_nurbs_curve_shape_for_closest`, `_get_edit_point_count`, `_closest_point_between_line_and_curve`, `align_eps_by_lane_projection` (shape-level EP read/write, solve-then-apply; reuses `_closestPointOnShape`, `DIST`, `MATH.Vector3.Lerp`, `POS`, `TRANS`, `SHAPES`)
- EXTENDED: `cgm/core/lib/search_utils.py` — `get_nonintermediateShape` delegates to `SHAPES.get_nonintermediate` (lazy import)
- EXTENDED: `cgm/core/tools/toolbox.py` — `buildRow_tweakCurve` after mirror row: **Align EPs (lane)** (`func_process` `all`) and **Distribute EPs** (`func_process` `each`)

**Features**:
- **Align EPs (lane)**: selection order start → middle(s) → end; per-EP lane from start/end EP positions; closest point on each middle curve to that segment
- **Distribute EPs**: even arc-length spacing of edit points on selected curve(s); closed curves keep first/last EP fixed
- Single `nurbsCurve` shape per transform (fail-fast); `SHAPES.get_nonintermediate` for deformer/Orig-safe closest-point and EP IO

**Decisions**:
- No `maya.api.OpenMaya`; closest point via existing `_closestPointOnShape` (`nearestPointOnCurve` DG node)
- `distance_utils` keeps calling `SEARCH.get_nonintermediateShape` (not a top-level `SHAPES` import) to avoid circular import through `transform_utils` → `distance_utils` → `shape_utils` → `rigging_utils`
- Lane align uses `func_process` mode `all` (ordered list passed as `curves`); distribute uses `each`

**Status**: ✅ Complete (Maya runtime verification user-side)

---

### May 19, 2026 - AnimFilter verify-close on window close
**What**: Added optional close confirmation for AnimFilter so clicking the window **X** prompts before the tool hides (`RETAIN=True`). Cancel re-shows the window; Close hides as before. Implemented via shared `BaseMelWindow` hooks in `baseMelUI` (cmds/MEL only — no Qt).  
**Files**:
- EXTENDED: `cgm/core/lib/zoo/baseMelUI.py` — `BaseMelWindow.VERIFY_CLOSE`, `confirmClose()`, `restoreAfterCloseCancelled()` (`scriptJob` idle + `evalDeferred` fallback), `Close()` calls confirm before `visible=False`
- EXTENDED: `cgm/core/tools/animFilterTool.py` — `VERIFY_CLOSE = True`; `confirmClose()` uses `confirmDialog` (`Close` / `Cancel`, default **Cancel**)

**Features**:
- **X** on AnimFilter shows “Close AnimFilter?”; **Cancel** keeps the window open; **Close** hides it
- Other cgm tools can opt in by setting `VERIFY_CLOSE = True` and overriding `confirmClose()` (e.g. only when actions are loaded)

**Decisions**:
- Maya `closeCommand` runs after the window is already hidden; cancel path must re-show via deferred restore, not synchronous `showWindow` alone
- Do not use `cgmGEN.Callback` for `closeCommand` (one-shot `del self` breaks repeat closes)
- Qt `closeEvent` was tried and reverted (set `closeCommand` to `doNothing` when hook failed, which closed with no prompt)

**Status**: ✅ Complete

---

### May 19, 2026 - Global playback stop before frame-scrub bakes
**What**: Timeline playback could fight `currentTime` loops when users started a bake while Maya was playing (reported on AnimFilter). Added `cgmGEN.playback_is_playing()` / `playback_stop()` and wired it at shared bake entry points. **Stop only** — does not resume playback after bake.  
**Files**:
- EXTENDED: `cgm/core/cgm_General.py` — `playback_is_playing()`, `playback_stop(log=True)`
- EXTENDED: `cgm/core/classes/PostBake.py` — `playback_stop()` at start of `bake()` (AnimFilter, dragger, spring, designer spring, trajectory aim, keyframe-to-motion-curve)
- EXTENDED: `cgm/core/tools/locinator.py` — `bake_match()`
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `Bake()`
- EXTENDED: `cgm/core/tools/mocapBakeTools.py` — `bake()`
- EXTENDED: `cgm/core/tools/funcIterTime.py` — `fOverTimeBAK.run()`, `run_frames()`

**Features**:
- Starting any wired bake while the timeline is playing stops playback first
- Opening bake UIs alone does not stop playback (only bake execution)

**Decisions**:
- Central helper in `cgm_General` rather than per-tool copies; no auto-resume after bake

**Status**: ✅ Complete

---

### May 14, 2026 - Version list path parity (`_version_files_parent_directory`)
**What**: Fixed Save here / Export / Save version when the version column is the second column (e.g. subtype is `version`, no `hasSub`, or no subtype tabs). `LoadVersionList` already searched `path_asset` in those layouts, but `SaveVersion`, save-here dialogs, and `path_versionDirectory` used `path_subType` / `hasNested` logic and could pass `False` into `os.path.join`.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `_version_files_parent_directory()` mirrors `LoadVersionList` `searchDir` (no subtypes → `path_asset`; `hasVariant` → variation dir; `hasSub` → `path_set`; else → `path_subType`); `path_versionDirectory` property delegates to it; `SaveVersion`, `CreateSubTypeRef`, and `uiPath_mayaSaveTo_version` use it; `OpenVersionDirectory` guards missing path; removed stray `cgmUI` token in `LoadVersionList` no-`hasSub` filter branch

**Features**:
- Version-column icon row and RMB **Save Maya here** target the same folder the version list is built from
- No more `TypeError: ... not bool` on **Save version** when `path_subType` is unset
- **Export** / **Save here** no longer warn "Version path doesn't exist" while files still list correctly

**Status**: ✅ Complete

---

### May 10–13, 2026 - Scene column icon rows, save-here stub, `ExportSelection` sets mode
**What**: Replaced cramped text rows with icon strips on the version column and no-subtype sets row (matching explorer icon styling). Wired the same behaviors as RMB **Save Maya here** / **Export Here** / **Save Version**, added sets-column **Export Here**, fixed Maya `MelButton` extra-callback `*args` issues, and pre-filled save dialogs with a version-stub basename (no trailing version digits, no `.ma`/`.mb`).  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `mRow_versionButtons` and no-`hasSub` `mRow_setButtons` icon rows (order: **save here** → **export** → **save version**); `ExportSelection(mode='sets')` + `ExportSelection_sets()`; sets list RMB **Export Here**; `_compute_next_version_save_basename()` shared with `SaveVersion`; `_save_here_suggested_stub()` for save-here dialog; `uiPath_mayaSaveTo(..., defaultFilename=)` via `fileDialog2` `startingDirectory`; `uiPath_mayaSaveTo_*` accept `*args` for Maya callbacks; `variationButton` / **New {subtype}** / **Add Set** / **Add Variation** on dedicated icons
- ADDED: `cgm/images/icons/new_set.png`, `new_dir.png`, `new_version.png`, `new_variation.png`, `export_file.png`; updated `new_file.png`

**Features**:
- Version column: `new_file` (save here), `export_file` (export selection), `new_version` (`SaveVersion`)
- No-subtype sets row: `new_dir` (add set) + same three action icons
- Has-subtype row: `new_set` (new subtype), `new_variation` (add variation), `new_dir` (add set when applicable)
- Save-here suggests e.g. `bird_wing_mdl` while **Save version** still increments to `bird_wing_mdl_12.mb`

**Status**: ✅ Complete

---

### May 9, 2026 - Cutscene export: `deleteMesh` selection recovery + strict per-rig delete sets
**What**: After multi-ref cutscene debugging: Prep no longer resolves another rig’s `delete_tdSet` when DAG paths include `|`; cutscene `deleteMesh` no longer leaves stale transform names in `exportTransforms` for `mc.select`.  
**Files**:
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `Prep` parses namespace from `_topShort = topNode.mNode.split('|')[-1]` (matches `Bake`); `_ns_hint = ns.rstrip(':')`; `resolve_delete_set` with `namespace_prefix` tries only explicit prefixed candidates (no global `*:delete_tdSet` scan); `ProcessDeleteSet(..., resolved_set=)` when `mc.objExists(deleteSet)` in Prep
- EXTENDED: `cgm/core/mrs/Scene.py` — module helper `_export_transforms_after_mesh_strip()` filters deleted mesh transforms after `deleteMesh`, falls back to export root `obj`; used on referenced and rig multi-root export paths; fails with stage `select` if no DAG remains

**Features**:
- Multi-reference cutscene Prep uses `CrateBase:delete_tdSet` when prepping `CrateBase:master`, not the first `*:delete_tdSet` in the scene
- Cutscene export survives mesh strip when Prep selection included geo transforms

**Status**: ✅ Complete

---

### May 8, 2026 - Export refinements: rig/cutscene paths, mesh-strip transform recovery, namespaced delete-set + `zUpRoot` helper
**What**: Hardened FBX export pathing/naming for rig and cutscene modes, recovered transforms after mesh-strip steps so `deleteMesh`-driven exports do not silently lose targets, made delete-set resolution namespace-aware, and added a root-motion utility (`zUpRoot`).  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — added `_export_transforms_after_mesh_strip` for post-strip DAG recovery; abort export when `deleteMesh` removes all export DAGs; animation folder/name logic uses selected set or leaf token, treats `none`/`null` as no animation; only appends animation name for non-static/non-rig exports; `exportAnimPath` resolution simplified (rigs use asset path); rig filenames produced as `{assetName}_rig.fbx`; cutscenes collapse per-shot output into a single anim folder with asset disambiguation; rig exports skip per-shot splitting and unnecessary directory creation
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — initial namespace-aware `resolve_delete_set` / `ProcessDeleteSet` (strict per-rig resolution completed May 9)
- EXTENDED: `cgm/core/mrs/lib/post_utils.py` — new `zUpRoot` helper (validates selection, defaults `rootMotion_jnt`/`rootMotion_anim`, removes existing root constraints, temporarily unparents children, sets master `rx=90`, applies point/orient constraints with `maintainOffset=True`, reparents children, early returns on invalid input)

**Features**:
- Rig exports always single-file (`{assetName}_rig.fbx`); no shot folder/file fragmentation
- Cutscene exports collapse per-shot output into one anim folder with asset-disambiguated names
- Non-anim modes no longer append stray animation tokens to filenames
- Delete-set resolution survives namespace differences for non-referenced rigs

**Status**: ✅ Complete

---

### May 6, 2026 - Subtype invariants registry + Arnold plugin guard + minor robustness + `baseFemale_gameToon` config
**What**: Centralized subtype directory invariants (single canonical on-disk basename), guarded the `mtoa` plugin load with a `pluginInfo` registered-check, hardened `is_rigged` against a missing `moduleTarget`, and added the `baseFemale_gameToon` block configuration.  
**Files**:
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — `d_subtype_dir_invariants` and `_subtype_invariant_by_lower` to centralize tokens with single on-disk basenames (`geo`, `audio`, `source`); `_pluralize_token` and `subtype_dir_candidates` use the lookup so legacy plural variants are accepted but canonical form is used for filenames/dirs
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — `create_Scene_batchFile` and `create_MRS_batchFile` now check `mc.pluginInfo('mtoa', q=True, registered=True)` before inserting `mc.loadPlugin('mtoa')`
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — `is_rigged` falls back when `moduleTarget` is missing (treats `blockState=='rigged'` as positive, otherwise `False`); preserves prior behavior when `moduleTarget` exists
- ADDED: `cgm/cgmDat/mrs/human/baseFemale/baseFemale_gameToon.cgmBlockConfig` — serialized rig setup for the base female toon (master + spine segment with prerig/define/form/shape/proxy data, version `3.3.2.20`)

**Features**:
- Adding new subtype invariants no longer requires touching ad-hoc `geo` checks
- Batch jobs no longer error when `mtoa` is unavailable on the host
- `is_rigged` no longer raises when block setup is partial

**Status**: ✅ Complete

---

### May 3, 2026 - Exception logging revamp + Arnold load for Maya >2020
**What**: Restructured the shared exception/traceback path to produce clearer, deduplicated output with concise frame summaries, and inserted a conditional `mtoa` plugin load into MRS batch pre-commands for Maya versions newer than 2020 (later guarded by registered-check on May 6).  
**Files**:
- EXTENDED: `cgm/core/cgm_General.py` — replaced ad-hoc prints with structured messages; compact args/kwargs summaries; suppressed duplicate tracebacks; new `_normalize_exc_info` and `_summarize_frame_locals` helpers; `log_tb` now uses `traceback.format_exception` and avoids re-printing the same exception instance, handling missing `tb`/`value` robustly; `cgmException` accepts an exception instance (`cgmException(err)`) and prints an innermost-frame summary before delegating to `log_tb`; removed older verbose/local-dump code
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — `create_MRS_batchFile` adds `mc.loadPlugin('mtoa')` to `l_pre` when `cgmGEN.__mayaVersionInt__ > 2020`

**Features**:
- Exception output consistently single-traceback with locals summary at the innermost frame
- Arnold renderer plugin loads automatically for newer Maya versions in batch jobs

**Status**: ✅ Complete

---

### May 1, 2026 - Batch export honors per-item `worldUp`
**What**: `BatchExport` now reads a `worldUp` entry from export payloads and applies it once at the start of the batch, syncing Maya's scene up axis to the requested setting before processing items.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — export payloads include `worldUp`; `BatchExport` queries the current scene up axis and, if needed, calls `mayaSettings_utils.sceneUp_set` (logs the change); leaves the axis unchanged when `worldUp` is absent; debug print of the up axis at the end of `ExportScene`

**Status**: ✅ Complete

---

### April 30, 2026 - Ribbon attach kwargs + module child traversal hardening + `setup_shapes` docstring
**What**: Renamed ribbon IK kwargs to match expected key names for start/end attachments, switched batch error handling to delegate via `cgmException`, and rewrote `moduleChildren` flattening as BFS using `collections.deque` with a step cap so traversal cannot loop or run away. Documented `setup_shapes` runtime contract.  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/organic/head.py`, `cgm/core/mrs/blocks/organic/segment.py` — `attachStartToInfluences` → `attachStartToInfluence`, `attachEndToInfluences` → `attachEndToInfluence`
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — error path now calls `cgmGEN.cgmException(Exception, err)` instead of raising directly
- EXTENDED: `cgm/core/mrs/lib/module_utils.py` — `moduleChildren_get` rewritten as BFS via `collections.deque`, no in-place list mutation while iterating, large step cap with clearer error message
- EXTENDED: `cgm/core/mrs/lib/post_utils.py` — added `setup_shapes` docstring (keys: `shape`, `size`, `mirror`, `moveOffsetAim`, `setAttr`, `replaceShape`; mirror recipe behavior for `L_`/`R_`; first-existing-shape RGB carry; missing-object collection)

**Status**: ✅ Complete

---

### April 29, 2026 - moduleTarget wiring on block parent change + eyeLook resolution hardening
**What**: Consolidated `moduleTarget` wiring when a block's parent changes, added cleanup of stale `moduleParent.moduleChildren` links, and hardened the eyeLook control resolution path to handle siblings, puppets, ambiguity, and duplicates.  
**Files**:
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — added `moduleTarget_wire_from_blockParent` (handles master/puppet wiring and detaches previous moduleParent); `parentModule_detach` and `parentModule_set` now scrub stale `moduleParent.moduleChildren`; `blockParent_set` calls the helper but skips already-rigged blocks or blocks in `rig` state
- EXTENDED: `cgm/core/mrs/RigBlocks.py` — rigFactory consolidated through the new helper
- EXTENDED: `cgm/core/mrs/lib/module_utils.py` — supporting plumbing for parentModule changes
- EXTENDED: `cgm/core/mrs/blocks/organic/eye.py` — `msgList_append` replaced with guarded add (checks `msgList_index` first to avoid duplicates)
- EXTENDED: `cgm/core/mrs/lib/builder_utils.py`, `cgm/core/mrs/lib/rigBits.py` — `eyeLook_get` rewritten: checks module + moduleParent, searches sibling block children for an `eyeMain` `moduleTarget` (via `getMessageAsMeta` and attribute access), prefers `puppet.getMessageAsMeta` over attribute access, maps msgList entries by `p_nameLong`, errors on unresolved or ambiguous controls, falls back to `eyeLook_verify` when `autoBuild` is requested

**Features**:
- Block parent changes no longer leave stale child references on prior parents
- eyeLook resolution surfaces clear errors instead of silent failure on ambiguous setups
- Duplicate eyeLook msgList connections prevented

**Status**: ✅ Complete

---

### April 28, 2026 - Legacy config defaulting + subtype canonicalization hardening + export-dir alignment
**What**: Finalized plural-subdir behavior so legacy project switches, subtype UI state, filename stems, and export directory paths all follow a consistent policy split: plural for directory containers (when enabled), singular canonical for naming tokens.  
**Files**:
- EXTENDED: `cgm/core/tools/Project.py` — `data.read()` now calls `fillDefaults()` after config load to backfill missing keys from code defaults; bool UI fill handling for legacy/missing values (`usePluralSubDirs`, `mayaVersionCheck`) to avoid stale carryover on project switch
- EXTENDED: `cgm/core/mrs/Scene.py` — subtype list loading normalizes folder tokens to canonical subtype labels; metadata `subType` capture writes canonical subtype token; set-token filename normalization handles embedded plural subtype fragments (e.g. `full_templates` → `full_template`)
- EXTENDED: `cgm/core/mrs/Scene.py` — export path builders now resolve subtype export directory via policy-aware helper so `usePluralSubDirs` applies deterministically in export path construction paths

**Features**:
- Switching from a project with `usePluralSubDirs=True` to legacy configs now defaults missing key to `False` instead of retaining stale UI state
- Save New Version basename canonicalization now handles nested/set tokens containing plural subtype fragments
- Subtype action labels/prompts remain singular canonical (`New Template`)
- Export directories now consistently follow plural-subdir policy where Scene builds export subtype paths

**Status**: ✅ Complete

---

### April 28, 2026 - Final subtype filename token singularization + UI label cleanup
**What**: Closed remaining plural-token leakage in Save New Version naming (for example `*_test_templates_01`) by making subtype file token normalization generic, and updated subtype action labels to display singular canonical tokens.  
**Files**:
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — generalized `subtype_file_token` singularization rules (`s`/`es`/`ies`) with `geo` special-case preserved
- EXTENDED: `cgm/core/mrs/Scene.py` — SaveVersion/CreateSubTypeRef basename token normalization now resolves plural subtype fragments to canonical singular tokens; subtype action labels/prompts use singular display token (`New Template`)

**Features**:
- Save naming now prefers canonical singular subtype tokens even when directory containers remain plural
- Example correction path: `character_test_templates_01` → `character_test_template_01`
- Subtype UI action text aligned with naming policy (`New Template` instead of `New Templates`)

**Status**: ✅ Complete

---

### April 27, 2026 - Scene/Project startup log-noise reduction (Script Editor spam pass)
**What**: Reduced non-actionable startup/load logging noise when opening Scene and loading a project, while preserving meaningful warnings/errors and opt-in verbose diagnostics.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — downgraded high-chatter startup/state reporting and non-critical scriptUI-path messages to debug; reduced repeated list/dir-mask spam; avoided stale-selection “item not found” spam in previous-selection restores
- EXTENDED: `cgm/core/tools/Project.py` — `uiProject_fill` per-field fill chatter moved to debug/verbose-only; additional startup/path display chatter downgraded to debug

**Features**:
- Significantly quieter Script Editor output on Scene init + project load
- Added safer selection restore helper behavior to suppress avoidable “Item not found” chatter for stale remembered entries
- Kept error paths and actionable warnings intact; verbose fill diagnostics remain opt-in

**Status**: ✅ Complete

---

### April 27, 2026 - Scene metadata refresh reliability from directory/file column selections
**What**: Fixed cases where selecting paths in Scene columns did not refresh metadata details even when `.dat` metadata existed for the selected version file.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — selection flows now trigger metadata refresh after list-driven version resolution; subtype path-token mapping normalized for plural/singular folder tokens during path-based selection

**Features**:
- Added internal selection refresh helper to load metadata from the selected version file and rebuild details UI
- `uiFunc_subTypeList_select` / `uiFunc_variationList_select` now refresh metadata after `LoadVersionList` auto-selection paths
- Path-based open/select flows now resolve subtype labels from folder tokens (plural/singular aware) before subtype lookup

**Status**: ✅ Complete

---

### April 27, 2026 - Project `usePluralSubDirs` + subtype-only naming policy refinement
**What**: Added project-level control for plural subtype directories, kept behavior scoped to subtype UI/pathing, added mixed-state warning/fixer action, and corrected file naming so rig saves remain singular token (`rig`) even when subtype containers are plural (`Rigs`).  
**Files**:
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — `usePluralSubDirs` defaults/schema entry; subtype directory candidate policy (`s`/`es`) and canonical subtype file token helper
- EXTENDED: `cgm/core/tools/Project.py` — General UI checkbox support for `usePluralSubDirs`
- EXTENDED: `cgm/core/mrs/Scene.py` — project-option-aware subtype path resolution, `Fix Now` dialog action, subtype-only scope for pathing, canonical file-token naming in save/export paths

**Features**:
- New project general option: `usePluralSubDirs` (default `False`)
- `Scene` subtype container resolution is policy-aware:
  - OFF: singular-first, plural fallback
  - ON: plural-first, singular fallback
- Mixed singular/plural subtype folder states warn and offer `Fix Now`
- Fixer remains constrained to subtype folders under the selected asset directory only
- `geo` is handled as a special-case subtype folder token (`geo` only, no pluralization)
- Save/export filename stems use canonical subtype tokens (for example, `bob_rig_01` not `bob_rigs_01`)

**Decisions**:
- Scope intentionally limited to subtype naming/pathing UI behavior; asset/category naming is unchanged
- Directory container naming policy is separated from filename token policy to keep export/version names deterministic

**Status**: ✅ Complete

---

### April 23, 2026 - Branch Setup, Baseline, and First Export Fix
**What**: Created Unreal workflow branch guide, defined Unreal export success criteria, triaged current Scene export risks, and implemented first high-priority export fix  
**Files**:
- NEW: `py3/branches/Branch_UnrealWorkflow.md`
- EXTENDED: `cgm/core/mrs/Scene.py`

**Features**:
- Added branch-scoped workflow doc for Unreal export hardening
- Added explicit Unreal export acceptance criteria and validation matrix
- Added issue triage list with priority and resolution state
- Fixed rig export behavior so per-shot file splitting cannot run in rig mode

**Decisions**:
- Keep branch execution tracking in `Branch_UnrealWorkflow.md`; split to `py3/Dev/Features` only if implementation details become too large
- Prioritize stability fixes that remove behavior ambiguity before polishing UI/ergonomics
- Treat rig exports as always single-file by design; this aligns with expected rig delivery and prevents accidental shot-fragment outputs

**Status**: ✅ Complete

---

### April 23, 2026 - Export error reporting, RunExportCommand guards, batch summaries
**What**: Stage-tagged context logging, safer path token handling, stronger batch failure traces, `ExportScene` failure summary blocks  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` (`RunExportCommand`, `ExportScene`, `BatchExport`)

**Features**:
- `RunExportCommand`: validates open-file tokens and export directory before indexing; top-level `log.exception` with context
- `ExportScene`: `_finalize_failure` lists stage/reason troubleshooting summary on failure paths (workspace, bake, prep, FBX, cleanup)
- `BatchExport`: per-item `log.exception`, structured failure records, attempted/succeeded/failed summary line

**Status**: ✅ Complete

---

### April 23, 2026 - Non-referenced namespace removal + bake set resolution
**What**: `removeNamespace` for non-referenced exports; bake all members of `bake_tdSet` when DAG path vs short name mismatched namespaced bake set  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — non-ref branch merges namespaces and strips root name for export selection
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `Bake()` uses short node name for namespace; tries `namespace:bake_tdSet` then plain `bake_tdSet`; logs missing sets and empty bake sets

**Decisions**:
- Parse namespace from `asset.split('|')[-1]` so `|group|ns:root` does not produce invalid bake set names

**Status**: ✅ Complete

---

### April 23, 2026 - Delete set for non-referenced exports (`ProcessDeleteSet`)
**What**: Delete-set cleanup lived only in `Prep()` (referenced assets). Batch/rig exports with a non-referenced rig never called `Prep`, so delete sets were never processed and no delete logs appeared.  
**Files**:
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `resolve_delete_set`, `ProcessDeleteSet` (shared); `Prep` delegates to it; added `cgmGEN` import for warning banners
- EXTENDED: `cgm/core/mrs/Scene.py` — non-referenced branch: `delete_pre_ns` (if root has namespace) then `delete_post_ns` after namespace strip

**Features**:
- Resolves delete set via `ns:delete_tdSet`, plain `delete_tdSet`, or `*:delete_tdSet` pattern
- Logs resolved set name, target count, failures, survivors

**Status**: ✅ Complete

---

### April 23, 2026 - Send to Build observability, MRS Build window placement, project `fillDefaults` noise
**What**: Scene “Send to Build” and MRS Build batch path easier to debug; MRS Build window reliably on-screen; `Project.data.fillDefaults` no longer floods the Script Editor when log level is DEBUG.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `SendToBuild`: `log.info` stages, `try`/`except` around `ui_toStandAlone`
- EXTENDED: `cgm/core/mrs/Builder.py` — `uiFunc_process`: INFO/WARNING for prechecks, file list, skip reasons (missing path, dirty cancel), empty batch summary; `_mrs_build_window_place_on_screen` + `post_init` on `ui_toStandAlone`; `RETAIN = False`; optional `CGM_MRS_BUILD_AT_CURSOR` for cursor placement; clear stale `windowPref` for the build window name
- EXTENDED: `cgm/core/tools/Project.py` — `fillDefaults`: no routine logging unless env `CGM_VERBOSE_FILL_DEFAULTS` is `1`/`true`/`yes` (avoids noise even when loggers are DEBUG)

**Decisions**:
- MRS Build still queues files for the **Build** button; logs state that explicitly so it is not mistaken for a one-shot action.
- Rig-block **prechecks run on the current scene** before batch file generation; failure logs now say queued files were not processed.

**Status**: ✅ Complete

---

### April 23, 2026 - Batch rig: master vis/settings when prerig messages are missing (`doDuplicate` on `False`)
**What**: `rebuildMasterShapes` assumed `prerigNull.getMessageAsMeta('controlVis'|'controlSettings')` always returned a meta node; `getMessageAsMeta` returns **`False`** when the message is unset, which caused `AttributeError: 'bool' object has no attribute 'doDuplicate'` during `process_blocks_rig` / Send to Build batch runs.  
**Files**:
- EXTENDED: `cgm/core/mrs/RigBlocks.py` — `cgmRigMaster.rebuildMasterShapes`: if prerig helper message is missing, **warning** + **procedural** helper build (same pattern as the no-prerig-null branch) instead of calling `.doDuplicate` on `False`.

**Status**: ✅ Complete

---

### April 23, 2026 - Remove unused `Scene2.py` backup
**What**: Confirmed no repo references to `cgm.core.mrs.Scene2`; entry points use `Scene` only (`tool_calls.py`, `Project.py`). Removed duplicate backup module to avoid drift and duplicate maintenance (e.g. parallel `SendToBuild` edits).  
**Files**:
- REMOVED: `cgm/core/mrs/Scene2.py`

**Note**: If any **external** shelf or script imported `Scene2`, repoint it to `cgm.core.mrs.Scene`.

**Status**: ✅ Complete

---

## 📦 Deliverables

### Branch Doc Foundation
- [x] Create branch-specific doc using branch template conventions
- [x] Add branch metadata, goals, related docs, and timeline structure
- [x] Add dedicated Unreal export working sections

### Unreal Success Criteria + Baseline Repro
- [x] Define expected output behavior for Anim, Cutscene, Rig, and Static export modes
- [x] Define deterministic naming/path expectations for generated FBX files
- [x] Define baseline repro checklist for regression comparison

### Triage and Fixes
- [x] Triage Scene export issues into blocking/high/medium priorities
- [x] Resolve at least one high-priority behavior bug in `Scene.py`
- [x] Capture fix rationale and impact in branch timeline and notes

### Validation Matrix
- [x] Build repeatable matrix for fresh export, re-export, and multi-mode runs
- [x] Record current results and confidence level per matrix entry
- [x] Call out residual risk/remaining manual Unreal ingest checks

### PR Readiness
- [x] Draft PR notes with overview, changed files, behavior changes, and testing summary
- [x] Document non-breaking behavior intent
- [x] List next steps and known limitations

### Testing
- [x] Static code-path validation for first fix completed
- [ ] Full Maya + Unreal ingest verification pass (manual runtime pass pending)
- [x] Documentation updated and PR notes drafted

---

## Unreal Export Success Criteria

1. **Mode correctness**
   - `Anim`/`Cutscene`: support shot/take workflows as configured.
   - `Rig`: always produce a single rig export file (no per-shot splitting).
   - `Static`: export selected/static targets with expected texture-link behavior.
2. **Path correctness**
   - Export path resolves to expected asset/subtype locations for each mode.
   - No unexpected nested folders unless explicitly part of shot-split mode.
3. **Naming correctness**
   - Output filenames are deterministic and consistent across repeated exports.
   - No accidental namespace pollution in final export names when removal is enabled.
4. **Repeatability**
   - Running export twice with identical config produces equivalent structure and expected files.
5. **Safety**
   - Options that are irrelevant to a mode do not create side effects (for example, shot splitting in rig mode).

## Baseline Repro Checklist

- Open representative scene with exportable asset setup.
- Confirm export mode selection and option state.
- Export in `Anim`, `Cutscene`, `Rig`, and `Static` modes.
- Re-run export with same settings and compare output structure.
- Validate that resulting files and directories match mode expectations.

---

## Issue Triage (Current)

### Blocking
- None currently identified after first pass.

### High
- [x] **Rig mode honoring shot-splitting option**
  - **Problem**: Rig export could enter per-shot split branch when `exportShotsToIndividualFiles` was enabled.
  - **Fix**: Guarded split branch to run only when `not exportAsRig`.
  - **File**: `cgm/core/mrs/Scene.py`
  - **Impact**: Rig mode now reliably exports as a single file.

### Medium
- [ ] Validate mode/path combinations against project directory configurations.
- [ ] Validate re-export overwrite behavior across all modes.
- [x] Namespace + bake set behavior for non-referenced namespaced rigs (short-name bake set resolution)
- [x] Delete set runs for non-referenced export path (`ProcessDeleteSet` pre/post namespace)
- [x] Multi-reference cutscene Prep picks correct rig `delete_tdSet` (strict `resolve_delete_set` + `resolved_set`)
- [x] Cutscene `deleteMesh` + stale `exportTransforms` after Prep (`_export_transforms_after_mesh_strip`)
- [x] Version-column save/export when versions live under `path_asset` (`_version_files_parent_directory`)

### Low
- [x] Playback stopped before frame-scrub bakes (`cgmGEN.playback_stop` + PostBake / Locinator / bakeAndPrep / mocap / funcIterTime)
- [x] AnimFilter close confirmation on window **X** (`BaseMelWindow.VERIFY_CLOSE` + `animFilterTool.confirmClose`)
- [x] Structured export / batch / delete-set logging for triage (log-based; UI summary optional later)
- [x] End-of-export summary: per-shot list, frame ranges, paths, UP axis (`log_export_results_summary`; batch rollup)
- [x] Read-only depot FBX fail-fast + non-writable path batch report (`path_utils`; P4 checkout deferred)
- [x] Nested-ref bake/export/delete tdSet resolution (`resolve_td_set_for_asset`)
- [x] Mayapy FBX import order + lazy FBX version probe (no `FBXExportFileVersion` spam at batch start)
- [x] Ground snap / `groundPos` respect Maya scene up (Y-up and Z-up; unified helpers in `position_utils` / `snap_utils`)
- [x] MetaHuman facial skeleton prune to keep-list + root chain (`joint_utils.pruneSkeletonToJoints`)
- [x] Maya Be Odd **Cascade UI Windows** dev menu action (`mayaBeOdd_utils` / `tool_chunks`)
- [x] Send to Build / MRS Build path: stage logging, window placement, `fillDefaults` opt-in verbosity (`CGM_VERBOSE_FILL_DEFAULTS`)
- [x] Batch rig master rebuild when prerig vis/settings messages are absent (`RigBlocks` / `getMessageAsMeta` vs `False`)

---

## Validation Matrix (Current Pass)

### Matrix Definition
- **Scenarios**: Fresh export, re-export, mode-switch export
- **Modes**: Anim, Cutscene, Rig, Static
- **Checks**: Path, naming, file count/shape, option side effects

### Results Snapshot
- **Rig + shot-splitting option ON**: ✅ Code-path validated; split branch blocked for rig exports.
- **Multi-ref cutscene + deleteMesh**: ✅ Code-path validated; per-rig delete set + post-strip selection refresh.
- **Version column (no subtype tabs / version in column 2)**: ✅ Save/export paths aligned with `LoadVersionList`.
- **Per-shot individual FBX (exportShotsToIndividualFiles)**: ✅ User verified (Crate closed/opening/open/closing); export summary at batch end.
- **Read-only synced FBX in depot**: ✅ Fail before FBX with path listed; `.bak` cleanup when deletable (manual `p4 edit` still required).
- **Static export + texture-link option behavior**: ⚠️ Not changed in this pass; requires runtime verification.
- **Cross-mode path consistency**: ⚠️ Requires runtime verification with project data variants.

### Residual Risk
- Runtime behavior in Maya + Unreal ingest still needs a manual verification pass for full confidence.

---

## 🚀 PR Notes

```markdown
# Scene Export: Unreal workflow (rig stability, logging, bake/delete, MRS Build)

## Overview
Improves Scene export reliability for Unreal-oriented workflows: rig single-file behavior, clearer errors, non-referenced namespace and bake/delete parity with referenced `Prep`, nested-ref tdSet resolution (`resolve_td_set_for_asset`), writable-path pre-check and batch non-writable reporting (P4 checkout deferred), FBX plugin bootstrap for mayapy batch, export success summary (shots, frames, paths, UP axis), multi-reference cutscene delete-set isolation and post-`deleteMesh` selection recovery, Scene column save/export icon rows with save-here filename stubs and version-directory parity, global `playback_stop` before frame-scrub bakes, AnimFilter verify-close on window **X**, structured logging for batch and delete-set cleanup, Send to Build / MRS Build observability, quieter project `fillDefaults`, batch rig master control when prerig helper messages are missing, prerig ratio arrange + curve EP lane tools, scene-up-aware ground snap (Z-up fix for Point Special **Ground**, `groundPos`, master-block placement), MetaHuman facial skeleton prune (`pruneSkeletonToJoints`), Maya Be Odd cascade UI windows dev action, and removal of unused `Scene2.py`.

## Major Changes

### 1. Rig mode single-file enforcement
`exportShotsToIndividualFiles` does not apply per-shot splitting when exporting as rig (`exportAsRig`).

### 2. Export error reporting
- `RunExportCommand`: token/path guards; exception context
- `ExportScene`: stage-tagged failures and end-of-failure troubleshooting summary
- `BatchExport`: per-item tracebacks and batch summary counts

### 3. Non-referenced export path
- Namespace stripping for `removeNamespace` when asset is not referenced
- `ProcessDeleteSet` before/after namespace merge so delete sets are found and logged (matches prior `Prep`-only behavior)

### 4. Bake (`bakeAndPrep.Bake`)
- Namespace parsed from short node name (fixes wrong bake set when DAG path contains `|`)
- Tries namespaced then plain bake set name; warns on missing/empty sets

### 5. Send to Build / MRS Build (`Scene`, `Builder`)
- `SendToBuild`: INFO logs, exception if UI fails to open
- `uiFunc_process`: clearer precheck / skip / empty-batch messages
- MRS Build window: centered on `MayaWindow` by default; optional `CGM_MRS_BUILD_AT_CURSOR`; `RETAIN = False` + placement helper

### 6. Project data (`Project.py`)
- `fillDefaults`: silent unless `CGM_VERBOSE_FILL_DEFAULTS` is set

### 7. Batch rig master (`RigBlocks.py`)
- Missing prerig `controlVis` / `controlSettings` messages: procedural helper instead of `False.doDuplicate()`

### 8. Cleanup
- Removed `cgm/core/mrs/Scene2.py` (unused backup; no in-repo imports)

### 9. Multi-reference cutscene Prep (`bakeAndPrep`)
- `Prep` namespace from DAG leaf (`split('|')[-1]`); strict `resolve_delete_set` when prefix is known; `resolved_set` when delete set already exists

### 10. Cutscene mesh strip (`Scene`)
- `_export_transforms_after_mesh_strip` refreshes selection after `deleteMesh` removes geo transforms from Prep selection

### 11. Scene column UI (`Scene`)
- Icon rows: save here / export / save version; `_save_here_suggested_stub` + `fileDialog2` prefill; `_version_files_parent_directory` for list/save path parity

### 12. AnimFilter close confirm (`baseMelUI`, `animFilterTool`)
- `BaseMelWindow.VERIFY_CLOSE` + `confirmClose()` / `restoreAfterCloseCancelled()`; AnimFilter always confirms on **X** (cmds `closeCommand` path)

### 13. Playback stop before bakes (`cgm_General`, PostBake, bake tools)
- `playback_stop()` at frame-scrub bake entry points; fixes playback-during-bake conflicts (AnimFilter and Locinator-class tools)

### 14. Curve tweak tools (`curve_Utils`, `toolbox`, `search_utils`)
- `align_eps_by_lane_projection`: middle curves snap EPs to lanes between start/end curves (ordered selection)
- Toolbox **Controls → tweak**: **Align EPs (lane)** + **Distribute EPs**
- `get_nonintermediate` canonical in `shape_utils`; `search_utils.get_nonintermediateShape` delegates (lazy import)

### 15. Ratio arrange (`arrange_utils`, snap/toolbox, MRS prerig block menu)
- `alongRatio` / `alongRatio_prompt`: proportional spacing, endpoints fixed, N≥3 controls
- Golden geometric chain; finger preset; custom prompt (φ default or comma weights)
- Snap **Arrange → Ratio** submenu; cgmToolbox/snapTools **Ratio** button rows
- MRS Builder block **Prerig**: **Arrange | Ratio *** menu items via `prerig_arrangeRatio_menuDict`

### 16. Export tdSet resolution + Prep namespace (`bakeAndPrep`)
- `resolve_td_set_for_asset`: outer→inner namespace candidates for bake/export/delete sets
- `Prep`: resolved export set after ref merge; optional delete set; `mergeNamespaceWithRoot` for remaining NS

### 17. Writable export paths + FBX bootstrap (`path_utils`, `cgm_General`, `Scene`, `batch_utils`, `project_utils`)
- Pre-export writability check; `ExportOutputNotWritableError`; editable `.bak` sidecar cleanup
- `ensure_fbx_plugin` before Scene import in mayapy batch; lazy FBX version list (no import probe loop)
- Batch non-writable path summary; export success summary (shots, frames, paths, UP axis)

### 18. Scene-up-aware ground snap (`position_utils`, `snap_utils`, `snap_calls`, `tool_chunks`, `transform_utils`)
- `ground_position_get` / `position_project_to_ground_plane` / `ground_bottom_position_get` — single source for plane math via `sceneUp_get`
- Point Special **Ground** + `groundPos` loc/snap/master-block placement fixed in Z-up (no hardcoded `Y=0` / ymin)
- `to_ground` preserves pivot offset along scene up; BB bottom/top in `get_bb_pos` respect up axis

### 19. MetaHuman facial skeleton prune (`joint_utils`)
- `pruneSkeletonToJoints`: keep listed joints + parent chain to joint root; delete all other joints under that hierarchy (deepest first)
- Dry run: `delete=False`; returns `kept` / `deleted` / `roots` dict
- Does not strip skin or other joint connections — artist dup or post-fix expected

### 20. Maya Be Odd cascade UI windows (`mayaBeOdd_utils`, `tool_chunks`)
- **Maya Be Odd → Cascade UI Windows** in cgmToolbox; dev ergonomics when many tool windows are open during export/rig debugging

## Files Modified
- `cgm/core/mrs/Scene.py`
- `cgm/core/mrs/lib/batch_utils.py`
- `cgm/core/mrs/Builder.py`
- `cgm/core/tools/Project.py`
- `cgm/core/tools/lib/project_utils.py`
- `cgm/core/mrs/RigBlocks.py`
- `cgm/core/tools/bakeAndPrep.py`
- `cgm/core/lib/path_utils.py`
- `cgm/core/cgm_General.py`
- `cgm/core/classes/PostBake.py`
- `cgm/core/tools/locinator.py`
- `cgm/core/tools/mocapBakeTools.py`
- `cgm/core/tools/funcIterTime.py`
- `cgm/core/lib/zoo/baseMelUI.py`
- `cgm/core/tools/animFilterTool.py`
- `cgm/core/lib/curve_Utils.py`
- `cgm/core/lib/search_utils.py`
- `cgm/core/tools/toolbox.py`
- `cgm/core/tools/snapTools.py`
- `cgm/core/tools/lib/tool_chunks.py`
- `cgm/core/lib/arrange_utils.py`
- `cgm/core/rig/general_utils.py`
- `cgm/core/mrs/lib/block_utils.py`
- `cgm/core/lib/position_utils.py`
- `cgm/core/lib/snap_utils.py`
- `cgm/core/lib/transform_utils.py`
- `cgm/core/tools/lib/snap_calls.py`
- `cgm/core/rig/joint_utils.py`
- `cgm/core/lib/mayaBeOdd_utils.py`
- REMOVED: `cgm/core/mrs/Scene2.py`
- ADDED: `cgm/images/icons/new_set.png`, `new_dir.png`, `new_version.png`, `new_variation.png`, `export_file.png` (and updated `new_file.png`)

## Testing
- ✅ Static / lint checks on touched files
- ⏳ Full Maya batch rig export + Unreal ingest (user runtime)

## Breaking Changes
- **External only**: anything that imported `cgm.core.mrs.Scene2` must use `Scene`.

## Next Steps
- Optional `p4 edit` integration at export writability check
- Unreal ingest spot-check on exported FBX (UP axis in summary for troubleshooting)
```

---

## 📝 Notes

### Architectural Patterns Established
- Export mode should strictly govern whether optional export toggles are applicable.
- Mode-incompatible options must be ignored rather than partially honored.
- Shared helpers (`ProcessDeleteSet`, `resolve_td_set_for_asset`) keep referenced vs non-referenced paths consistent.
- Parse DAG nodes with `split('|')[-1]` before inferring namespace/bake/delete set names.

### Lessons Learned
- A small conditional guard can remove high-impact ambiguity in file-output behavior.
- Capturing triage + validation criteria up front helps keep export fixes measurable.
- Anything that only ran inside `Prep()` never ran for non-referenced exports until explicitly duplicated or shared.
- `cgmMeta.getMessageAsMeta` returns **`False`** when a message is missing; do not chain meta-only APIs on that return without a truthiness check.
- `log.debug` still prints when the effective logger level is DEBUG; opt-in env flags are safer than `log.debug` alone for very hot paths like `fillDefaults`.
- `topNode.mNode.split(':')` on a full DAG path leaves `|` in the namespace token; use `split('|')[-1]` before `:` parsing (same as `Bake`).
- `LoadVersionList` search directory and save/export helpers must share one resolver when subtype tabs are absent.
- Retained Maya windows (`RETAIN=True`) need deferred re-show on cancelled close; overriding `closeCommand` alone is not enough to veto the **X** button.
- Shared UI close policy belongs on `BaseMelWindow` in `baseMelUI`, not per-tool Qt hooks.
- Frame-scrub bakes must call `cgmGEN.playback_stop()` before driving `currentTime`; opening the tool UI is not enough.
- Do not add top-level `shape_utils` imports in `distance_utils`; use `SEARCH.get_nonintermediateShape` or lazy import inside functions to avoid `transform_utils` circular init.
- Curve lane alignment: shape-level `.ep[i]` + `SHAPES.get_nonintermediate` keeps closest-point and EP edits on visible geometry, not Orig.
- Ratio presets: equal segment weights normalize to even spacing — geometric chains need descending powers per segment, not repeated constants.
- Shared menu builders (`buildRows_ratio_arrange`, `prerig_arrangeRatio_menuDict`) keep snap, toolbox, and MRS block menus aligned.
- Nested ref export roots need **outer** namespace on tdSets (`Blurrg:bake_tdSet` not `Blurrg:Inner:bake_tdSet`); use prefix walk, not full DAG namespace string.
- `project_utils` must not call FBX MEL at import — lazy `get_fbx_versions()` and batch must load FBX **before** importing Scene.
- Read-only depot FBX fails as opaque FBX I/O; pre-check + batch path list is enough until optional `p4 edit` pass.
- Export path helpers belong in **`path_utils`**, not `cgm_General`.
- Ground snap must use **`MAYASET.sceneUp_get()`** (or `POS.scene_up_axis_get`) — never hardcode `pos[1]=0` or ymin for “ground” in Z-up pipelines.
- **`groundPos`** (pivot on plane) and **`to_ground`** (BB bottom on plane) are different tools; share projection/BB helpers only.
- **`pruneSkeletonToJoints`**: keep set = explicit list ∪ parent chains to joint root only; does not retain unlisted **children** of kept joints — list every joint you need or they are pruned.
- MetaHuman facial wiring scripts should call **`JNTUTIL.pruneSkeletonToJoints`** after building the keep list; preview with `delete=False` first.

### Future Considerations
- AnimFilter: conditional confirm (e.g. only when `_actionList` is non-empty or file dirty) via `confirmClose()` override.
- Optional **`p4 edit`** before export — see **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)**
- Rig FBX: confirm `_rig_fbx_export_to_path` no-takes path on same builds as anim export.
- Consider a UI hint/disable state for options not applicable to selected mode.
- Curve tweak row: optional `rebuild` toggle for distribute; lane-align `samples` / `refine_steps` exposed in UI if artists need tuning.
- Ratio arrange: optional `cubicRebuild` / target-curve entries on toolbox row; store last custom ratio in optionVar.
- Optional skin-cluster / bind preflight before `pruneSkeletonToJoints` (or auto-detach helper) if facial strip becomes a one-click artist tool.

---

*Last Updated: June 5, 2026 (MetaHuman facial skeleton prune; Maya Be Odd cascade UI windows)*  
*Branch Status: Active*
