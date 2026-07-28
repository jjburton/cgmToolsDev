# Branch: jburton/UnrealWorkflow

## 📋 Quick Info
**Status**: Active  
**Created**: April 23, 2026  
**Last Updated**: July 28, 2026 (mocapBakeTools local-TR align/snap/bake + `mocap_align_utils`)  
**PR**: Pending

## 🎯 Goals
Harden Scene export behavior so Unreal-oriented exports are consistent, repeatable, and predictable for animation and rig workflows. **Also:** MetaHuman / Fortnite facial solve — joint matching, control→bridge mapping, SDK transfer onto source rigs, and lightweight target-follow constraints (`ProjectScripts/MetahumanFacial.py`); **body rig align** via native `mocapBakeTools` local-TR capture/snap/bake (`mocap_align_utils`). Track export and facial/align issues in one place, with explicit validation criteria and PR-ready notes.

## 📚 Related Documentation
- **[Feature_SceneExportFlow.md](../Features/Feature_SceneExportFlow.md)** - Canonical dev/TA spec: export modes, tdSet contract, prep order, namespace/path rules, troubleshooting
- **[Feature_SimChain.md](../Features/Feature_SimChain.md)** - Canonical dev/TA spec: cgmSimChain / cgmDynFK hair + cloth attach, nCloth presets, connect/bake, Query Settings
- **[Feature_MRSWiring.md](../Features/Feature_MRSWiring.md)** - Module/puppet message graphs, `mirror_get` tag-matching contract, control rewire consumers
- **[Feature_Metahuman.md](../Features/Feature_Metahuman.md)** - MetaHuman facial solve + body align workflow (mocapBakeTools is canonical align/bake home)
- **[Feature_MocapAlignSnap.md](../Features/Feature_MocapAlignSnap.md)** - Native mocapBakeTools local-TR align/snap/bake dual-path contract
- **MetahumanFacial.py** - `SourceArt-DDE/TechAnimation/Maya/ProjectScripts/MetahumanFacial.py` (Perforce) — facial SDK transfer / constrain (iteration home until core factors to py3)
- **[mocapBakeTools.py](../../cgmToolsPy3/cgm/core/tools/mocapBakeTools.py)** - Mocap / MetaHuman body align UI; dual-path bake (local TR when captured, legacy vector otherwise)
- **[mocap_align_utils.py](../../cgmToolsPy3/cgm/core/lib/mocap_align_utils.py)** - CCL IO, skeleton-root resolve, local-TR capture/snap/bake orchestration
- **[face_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/face_utils.py)** - `fortniteMetaHuman` pose-buffer schema
- **[sdk_utils.py](../../cgmToolsPy3/cgm/core/lib/sdk_utils.py)** - Existing SDK patterns; candidate merge target when factoring facial helpers from ProjectScripts
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
- **[nCloth_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/nCloth_utils.py)** - nCloth preset apply (`profile_load` layered fabric/solver/wind), `query_settings` / `query_settings_selection`, scene-up nucleus gravity remap, skip list (`isDynamic`, collision attrs), `get_out_mesh_shape` / `get_out_mesh_transform` for cloth attach
- **[node_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/node_utils.py)** - `create_UVPin`, `create_UVPinOnMesh`, `createRivetOnMesh` (Constraints-menu Rivet API + classic edge-loft fallback; no `mel createRivet`)
- **[constraint_utils.py](../../../repos/cgmToolsPy3/cgm/core/rig/constraint_utils.py)** — `attach_toShape(..., surfaceTrack=)` (follicle | rivet | uvPin); Rigging Utils **Attach by** surface-track items
- **[dynamic_utils.py](../../../repos/cgmToolsPy3/cgm/core/rig/dynamic_utils.py)** — `map_cloth_surface`, `get_mapped_cloth`, `attach_to_cloth_dynFK`, `setup_sim_dynFK`, `cgmDynFK.bake_nodes`, `set_base_name`, `chainMode='clothAttach'`
- **[dynFKTool.py](../../../repos/cgmToolsPy3/cgm/core/tools/dynFKTool.py)** (`cgmSimChain`) - **Init Sim Setup**, Details **Cloth** `>>` + **Fabric** / **Solver** menus (explicit apply only), **Cloth track**, **Attach to Cloth**, editable **Base Name**, **Tools → Query Settings**, target bake + post-bake `targets_disconnect`, `reload_dependencies()`
- **[tool_calls.py](../../../repos/cgmToolsPy3/cgm/core/tools/lib/tool_calls.py)** — `cgmSimChain()` reloads backend modules via `cgmGEN._reloadMod` before opening UI
- **[module_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/module_utils.py)** — `mirror_get`, `siblings_get`, module parent/children wiring
- **[animate_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/animate_utils.py)** — Animate context cache (`module_get`, `context_get`, mirror module expansion)
- **[cgmNCloth_presets.py](../../../repos/cgmToolsPy3/cgm/core/presets/cgmNCloth_presets.py)** - Layered profiles: **fabric** (`silk`, `cotton`, `denim`, …), **solver** (`solver_balanced`, `solver_quality`, `solver_high`, …), **wind** (`wind_calm`, `wind_flag`); `d_profileKind` registry
- **[transform_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/transform_utils.py)** - `ground_position_get` re-export
- **[mayaSettings_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/mayaSettings_utils.py)** - `sceneUp_get()` (Maya `upAxis`)
- **[arrange_utils.py](../../../repos/cgmToolsPy3/cgm/core/lib/arrange_utils.py)** - `alongRatio`, `alongRatio_prompt`, golden/finger presets
- **[general_utils.py](../../../repos/cgmToolsPy3/cgm/core/rig/general_utils.py)** - `ratio()` shim to `alongRatio`
- **[block_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/block_utils.py)** - `prerig_handlesLayoutRatio`, `prerig_arrangeRatio_menuDict`
- **[ml_breakdown.py](../../../repos/cgmToolsPy3/cgm/core/lib/ml_tools/ml_breakdown.py)** - Optional diagnostics touchpoint
- **[NewBranch_Guide.md](./NewBranch_Guide.md)** - Branch documentation format reference
- **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)** - P4 checkout/add for FBX export (planning)

## 🗓️ Timeline

### July 26–28, 2026 - mocapBakeTools local-TR align / snap / bake (`mocap_align_utils`)
**What**: Shipped native body-align workflow in `mocapBakeTools`: capture parented local-TR offsets (`doLoc` at rotate pivot), single-frame snap, and timeline bake using the same locator math. Dual-path — when `localTranslate` / `localRotate` are unset, Manual Set / Set On Bake / vector bake behave as before. Snap skips missing local offsets and prints a full Script Editor missing-data report.  
**Files**:
- NEW: `cgm/core/lib/mocap_align_utils.py` — CCL load/save, skeleton-root / rig-NS resolve, `capture_alignment_offsets`, `snap_connections`, `bake_connections`
- EXTENDED: `cgm/core/tools/mocapBakeTools.py` — Align UI (Rig NS, Skel Roots, Capture, Snap All/Sel); Tools menu debug locs; dual-path `bake()`; CCL via lib helpers
- EXTENDED: `cgmToolsDev/Features/Feature_MocapAlignSnap.md`, `Feature_Metahuman.md` — implemented status; mocapBakeTools as canonical align/bake home

**Features**:
- Capture at bind pose → store `localTranslate` / `localRotate`; Snap all/selected (no keys)
- Bake uses local-TR snap when offsets present; legacy `POS.set` + `SNAP.aim_atPoint` otherwise
- Multi-skeleton: set Skel Roots (auto-fill when exactly one MH-style `root` detected); Capture/Snap blocked when >1 root and unset
- CCL short-pattern save; load resolves under roots + namespace

**Decisions**:
- Keep Set Connection Pose UI; do not overwrite local TR with vector Manual Set / Set On Bake
- Snap does **not** fall back to vector aim — full missing-data report instead
- Orchestration only in `mocap_align_utils` — reuses `doLoc`, `movePointSnap` / `moveOrientSnap`, `TRANS.parent_set`, `NAMES`

**Status**: ✅ Complete (Maya verification checklist in Feature_MocapAlignSnap — user runtime pass)

---

### July 25, 2026 - mirror_get cgmDirectionModifier matching (FRNT vs none)
**What**: Fixed bilateral module mirror lookup when a puppet has multiple same-name modules on one side differing only by **`cgmDirectionModifier`** (e.g. `L_coat_segment_part` vs `L_FRNT_coat_segment_part`). `mirror_get` previously omitted absent modifier tags from the match dict, so `L_coat_segment_part` matched both `R_coat_segment_part` and `R_FRNT_coat_segment_part` and raised `"Shouldn't have found more than one mirror module!"`. Animate marking-menu context then crashed with `'NoneType' object is not subscriptable` when `module_get` failed.  
**Files**:
- EXTENDED: `cgm/core/mrs/lib/module_utils.py` — `mirror_get` always compares `cgmPosition`, `cgmPositionModifier`, `cgmDirectionModifier` via `getCGMNameTags(['cgmDirection'])` (absent tags = `False`); child loop uses same tag source for modifier plugs
- EXTENDED: `cgm/core/mrs/lib/animate_utils.py` — `context_get` uses `module_get(...) or {}` and `.get('mControls', [])` when building control lists
- EXTENDED: `Features/Feature_MRSWiring.md` — **Module mirror lookup (`mirror_get`)** pattern + maintenance rule cross-ref

**Features**:
- **`L_coat_segment_part` → `R_coat_segment_part`** (no FRNT modifier on either side)
- **`L_FRNT_coat_segment_part` → `R_FRNT_coat_segment_part`** (FRNT modifier preserved)
- Marking-menu / Animate mirror context no longer hard-fails on ambiguous coat modules

**Decisions**:
- Module mirror pairing follows the same tag contract as control pairing in **`mirror_verify`** — do not match on name/type/direction alone when position/modifier tags differ
- Keep the `"more than one mirror module"` guard; disambiguation is via tags, not tie-break heuristics

**Status**: ✅ Code complete — user verify: Hondo (or similar) coat modules + normal limb mirror spot-check in Animate marking menu

---

### July 25, 2026 - cgmSimChain bake constraint cleanup + preset menu fix
**What**: Fixed two cloth-workflow regressions: **Bake All Targets** left loc→target `parentConstraint` nodes live after simulation bake, and **Attach to Cloth** / Details rebuild could re-apply nCloth presets because Fabric/Solver menus defaulted to `cotton` / `solver_balanced` and fired `changeCommand` on UI rebuild. Added canonical **`Feature_SimChain.md`** design contract (July 14 doc; branch cross-link maintained).  
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `bake_nodes` calls **`targets_disconnect`** after `bakeResults` for any chain whose `mTargets` were baked (explicit `parentConstraint` cleanup; `disableImplicitControl` alone was unreliable)
- EXTENDED: `cgm/core/tools/dynFKTool.py` — Fabric/Solver menus default to **`Fabric`** / **`Solver`** placeholders; **`_suppressClothPresetApply`** while wiring menus on Details rebuild; presets apply **only** on explicit menu change (not attach/map/rebuild); remembers last menu selection for display without re-apply
- NEW: `Features/Feature_SimChain.md` — dev/TA spec: hair vs `clothAttach`, connect/bake contract, layered presets, Query Settings, verification checklist
- EXTENDED: `Features/Feature_SimChain.md` — bake contract documents post-bake `targets_disconnect`; anti-pattern for preset auto-apply on rebuild

**Features**:
- **Bake All Targets**: keys from sim bake, then constraints removed on baked target chains
- **Presets**: selecting **Fabric** / **Solver** from Details menus applies; attach and chain creation do **not** touch cloth attrs

**Decisions**:
- Do not rely on Maya **`disableImplicitControl`** alone for loc→target cleanup — always **`targets_disconnect`** after target bake
- nCloth preset apply is **opt-in** from menus — never side-effect of UI rebuild or attach

**Status**: ✅ Code complete — user verify: attach chain → tuned cloth unchanged; connect → bake → no `parentConstraint` on targets

---

### July 20, 2026 - Scene export queue multi-select + file-list popup rebuild
**What**: Artists can Ctrl/Shift multi-select Maya files in Sets, Variation, and Version scroll lists and enqueue them in one action from the bottom toolbar. Right-click file menus stay single-selection only; multi-select suppresses the popup using the same delete-and-rebuild pattern as MRS Builder block scroll lists.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `build_searchable_list(..., allowMultiSelect=)`; `AddSelectedToExportQueue` + `_collectExportQueueEntries` / `_exportQueueEntryFor*` helpers; toolbar **Add to queue as** wired to bulk path; RMB **To Queue as** still uses `AddToExportQueue` (one item); `_wireFileListScrollSelect`, `_fileListSelectCommand`, `_clearFileListPopupMenu`, `buildSubTypeListPopup` / `buildVariationListPopup` / `buildVersionListPopup` (Builder pattern: delete popup on selection change, skip rebuild when multi-select); `button=3` popups; init guard so wire-up does not run select handlers before sibling lists exist
- EXTENDED: `Features/Feature_SceneExportFlow.md` — export queue UI section + revision note

**Features**:
- **Multi-select** on Sets / Variation / Version file scroll lists (Asset list remains single-select)
- **Toolbar bulk queue**: **Add to queue as: Anim / Cutscene / Rig** → `AddSelectedToExportQueue` appends one queue entry per selected file (active list prefers multi-selection, else Version → Variation → Sets)
- **Right-click unchanged for queue**: popup **To Queue as:** still queues primary selection only via `AddToExportQueue`
- **Multi-select + RMB**: no context menu (popup deleted, not rebuilt — matches `Builder.uiScrollList_block_select`)
- **Batch unchanged**: `batch_buildFile` / `BatchExport` consume same `batchExportItems` dict shape

**Decisions**:
- Bulk queue is **toolbar-only** — no multi-mode right-click queue submenu
- Popup suppression follows **Builder** (rebuild on select, omit menu when `len(selected) > 1`), not enable/vis toggles on a static popup (those did not reliably hide Maya menus)
- Do not call list select handlers during initial UI wire when downstream columns are not built yet (`variationList` guard)

**Status**: ✅ Code complete — user verified bulk queue; reload Scene UI after sync

---

### July 14, 2026 - cgmSimChain polish: bake, presets, query, base name
**What**: Hardened cloth workflow UX after surface-track attach: nucleus-only **Init Sim Setup**, layered nCloth **Fabric** + **Solver** menus, simulation bake for targets (cloth + hair), preset query tool, editable setup base name, and preset hygiene (`isDynamic` is not profile data).  
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `setup_sim_dynFK` / `cgmDynFK.setup_sim`; `ensure_nucleus` + `_wire_time1_current_time`; `map_cloth_surface` rewires mapped nCloth to setup nucleus; `attach_to_cloth_dynFK` sets `cgmMatchTarget` → paired `mLoc`; `targets_connect` sets match target + `parentConstraint(loc, target)`; `cgmDynFK.bake_nodes` (`mc.bakeResults`, `simulation=True`, `disableImplicitControl=True`); `set_base_name`; load existing setup reads `cgmName` / `_dynFK` suffix
- EXTENDED: `cgm/core/lib/nCloth_utils.py` — layered `profile_load(fabric, solver=, wind=)`; `profile_kind` / `d_profileKind`; `query_settings`, `query_nucleus_settings`, `query_settings_selection`, `profile_format_paste`; `l_skipPresetAttrs` adds **`isDynamic`**; removed `isDynamic` from `base` nc in presets file
- EXTENDED: `cgm/core/presets/cgmNCloth_presets.py` — split **fabric** / **solver** / **wind** profiles; `solver_high` (20 substeps, 50 max collision iters); `preview` → `solver_preview` alias in utils
- EXTENDED: `cgm/core/tools/dynFKTool.py` — **Init Sim Setup**; Details **Fabric** + **Solver** option menus on Cloth row (`uiFunc_apply_ncloth_profiles`); editable **Base Name** (Details + Options); **Tools → Query Settings**; bake calls `bake_nodes` only (no manual snap loop)
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — dynFK nucleus `profile_load` remaps gravity via `NCLOTH._remap_nucleus_scene_axes`

**Features**:
- **Init Sim Setup**: `cgmDynFK` + nucleus + `time1.outTime → currentTime` without `makeCurvesDynamic` — required before **Cloth `>>`** when no hair chain exists
- **Map cloth**: links `mCloth` transform; if setup nucleus exists, reconnects nCloth sim to that nucleus
- **Presets in UI**: `NCLOTH.profile_load(fabric, solver=solver, applyNucleus=True)` — fabric feel independent of solver speed
- **Bake All Targets**: `bakeResults` simulation bake; **`targets_disconnect`** after bake removes loc→target constraints (July 25 — `disableImplicitControl` alone was insufficient)
- **Connect Targets**: `mLocs` drive targets; `cgmMatchTarget` points at loc for snap/bake workflows
- **Base Name**: editable on loaded setup; renames `{baseName}_dynFK` + updates `cgmName`
- **Tools → Query Settings**: selection → preset-shaped `profile` dict (diff from `base`), paste-ready Python block, Script Editor output; supports nCloth, nucleus, cgmDynFK mapped cloth, hair/nucleus dynFK nodes

**Decisions**:
- **`isDynamic`** is a runtime sim on/off switch — never apply or capture in presets (same class as collision flags)
- Target bake uses Maya **simulation bake**, not per-frame `doSnapTo` + `setKeyframe`
- Fabric and solver are **layered profiles**, not combined monolithic presets (`denim` + `solver_high`, etc.)
- Query output is **diff from `base`** so artists can paste deltas into new fabric/solver entries

**Status**: ✅ Code complete — Maya verify: Init Sim → map cloth → cotton + solver_high → attach → connect → bake targets; Query Settings on tuned cloth

---

### July 13, 2026 - nCloth preset profiles + apply helper
**What**: Added script-editor nCloth preset library and applier for cloth sim testing (capes, apparel, flags). Profiles set fabric dynamics + nucleus solver attrs; scene **Z-up** gravity is detected automatically; collision setup on the nCloth is left untouched.  
**Files**:
- NEW: `cgm/core/presets/cgmNCloth_presets.py` — `base` + initial monolithic profiles (`silk`, `cotton`, …); **July 14** refactor split fabric / solver / wind — see timeline entry above
- NEW: `cgm/core/lib/nCloth_utils.py` — `get_nCloth` / `get_nCloths` (shape, transform, or mesh); `profile_list`, `profile_load`, `apply`; `scene_up_get`, `gravity_direction_get`; `_remap_nucleus_scene_axes` via `position_utils.scene_up_axis_get`
- EXTENDED: `cgm/core/lib/nCloth_utils.py` — `pointMass` alias (`mass` → `pointMass`); skip compound/array attrs; `l_skipPresetAttrs` for collision attrs + **`isDynamic`** (July 14)

**Features**:
- **Script editor**: `import cgm.core.lib.nCloth_utils as NCLOTH` → `NCLOTH.profile_load('stable')` on selected nCloth / mesh
- **Scene up**: nucleus `gravityDirection` remapped at apply (Y-up `[0,-1,0]`, Z-up `[0,0,-1]`); ground `planeNormal` when `usePlane` is on
- **Collision preserved**: presets do not overwrite self-collide, collision flags, or thickness — artist/scene collision setup stays as-is
- **Profiles**: `stable` for character apparel first pass; `silk` / `flag` for light/windy cloth; `preview` for fast scrubbing

**Decisions**:
- Presets live under **`cgm/core/presets/`** (same pattern as `cgmDynFK_presets`); applier in **`lib/nCloth_utils.py`**
- Fabric dynamics only from presets — collision attrs filtered at apply time even if re-added to preset data later
- Nucleus `spaceScale` default `0.01` (cm scenes); artists on meters bump manually for now

**Status**: ✅ Code complete — Maya nCloth runtime verification user-side (Z-up gravity + stable/silk profiles)

---

### July 13, 2026 - cgmSimChain cloth attach + surface tracks (follicle / rivet / uvPin)
**What**: Extended **cgmSimChain** (`dynFKTool` / `cgmDynFK`) with mapped cloth surface, nCloth preset loading in Details, a distinct **Attach to Cloth** action (mesh trackers on linked nCloth **outMesh**), and artist-selectable **surface track** mode. **Make Dynamic Chain** (hair / `makeCurvesDynamic`) unchanged. nCloth **creation** stays outside the tool — artists map an existing nCloth to setup `mCloth`.  
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `map_cloth_surface()`, `get_mapped_cloth()`; `attach_to_cloth_dynFK()` calls `RIGCONSTRAINTS.attach_toShape` per joint on nCloth outMesh; `chainMode='clothAttach'`; per-chain `surfaceTrack` attr; msgLists `mLocs`, `mMeshFollicles`, `mRivets`, `mUvPins`; `chain_create` dispatches `hair` vs `clothAttach`; `chain_create_hair` (extracted, behavior unchanged); `get_dat()` adds `mCloth`, `mClothOutMesh`, per-chain track lists
- EXTENDED: `cgm/core/rig/constraint_utils.py` — `attach_toShape(..., surfaceTrack='follicle'|'rivet'|'uvPin')`; rivet via `NODES.createRivetOnMesh`; uvPin via `NODES.create_UVPinOnMesh`
- EXTENDED: `cgm/core/lib/node_utils.py` — `createRivetOnMesh` (Maya **Constraints → Rivet** internal API when available, else classic `curveFromMeshEdge` + `loft` + `pointOnSurfaceInfo` network — **not** `mel createRivet`, which is absent in current Maya/py3 builds); `create_UVPinOnMesh` wrapper around existing `create_UVPin`
- EXTENDED: `cgm/core/lib/nCloth_utils.py` — `get_out_mesh_shape`, `get_out_mesh_transform` (sim output mesh for attach)
- EXTENDED: `cgm/core/tools/dynFKTool.py` — Details **Cloth** row: status label + single **`>>`** (map selected nCloth; no separate Map Cloth button); `cgmNCloth_presets` menu when mapped; Create panel **Cloth track** menu + **Attach to Cloth** (gated on `mCloth`); per-chain UI branches on `chainMode` / `surfaceTrack`; `reload_dependencies()` + **Setup → Reload** via `cgmGEN._reloadMod`
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — Rigging Utils **Attach by → Surface track** items (`track:follicle`, `track:rivet`, `track:uvPin`)
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `cgmSimChain()` reloads `dynamic_utils`, `constraint_utils`, `node_utils`, nCloth presets before UI open

**Features**:
- **Map cloth**: select nCloth → Details **Cloth** row **`>>`** → `map_cloth_surface()` links setup `mCloth` (nCloth **transform**, not shape — reliable readback via `listConnections`)
- **nCloth presets in tool**: Details Cloth row **Fabric** + **Solver** menus → `NCLOTH.profile_load(fabric, solver=, applyNucleus=True)` (July 14 split; was single menu July 13)
- **Cloth track** (Create panel): `follicle` | `rivet` | `uvPin` before **Attach to Cloth**
- **Attach to Cloth**: fails fast if `mCloth` unset; places mesh tracker on **outMesh** per joint; **loc per target** parented under track (`mLocs` drive Connect Targets / bake — not follicle/rivet/uvPin xform directly)
- **Surface track behavior**:
  - **follicle** — follicle on closest UV (`mMeshFollicles`)
  - **rivet** — Constraints-menu rivet or classic edge-loft rivet (`mRivets`)
  - **uvPin** — `uvPin` node + locator on closest UV; one shared `uvPin` per mesh shape when possible (`mUvPins`)
- **Coexistence**: hair (`chainMode='hair'`) and cloth attach chains on one setup (shared nucleus)
- **Reload**: **Setup → Reload** or toolbox `cgmSimChain()` picks up backend changes without Maya restart

**Decisions**:
- **Extend cgmSimChain**, not a separate cloth-only tool — shared nucleus, joint list, bake/connect UX
- Cloth chains do **not** use `makeCurvesDynamic` or per-chain hairSystem — follow simmed cloth mesh only
- Reuse **`RIGCONSTRAINTS.attach_toShape`** (Rigging Utils **Attach by**) — no parallel `dynamic_mesh_follow` module
- Do **not** merge `cgmNCloth_presets` into `cgmDynFK_presets` (`nc` vs `hs` sections)
- Presets still skip collision attrs at apply (unchanged)
- Details **Cloth** row uses **`>>` only** for map (no duplicate Map Cloth button)

**Status**: ✅ Code complete — Maya verify: map cloth (`>>`) → preset → pick surface track → attach joint chain → connect/bake targets (all three track modes)

---

### July 13, 2026 - Scene mixed-level scroll list buttons
**What**: Fixed Scene asset-browser columns treating a browse level as **either** directories **or** files. When set folders and loose `.ma/.mb` files coexist at the same level (e.g. `Animations/` with set subdirs + loose scenes), the sets/variation rows now show **both** directory actions (New Subtype / Add Set / Add Variation) **and** file actions (Save Maya here / Export / Save Version). Version column visibility is driven by level content and selection type, not `hasSub`/`hasNested` alone.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `_dir_children_dirs`, `_dir_maya_files`, `_dir_is_mixed`, `_subtype_level_has_content`, `_level_show_dir_actions`, `_level_show_file_actions`, `_version_column_should_show`; shared `_append_set_*` / `_append_variation_*` button builders; refactored `uiUpdate_setsButtons` + new `uiUpdate_variationButtons`; `mRow_variationButtons` replaces static `variationButton`; `b_varFile` parallel to `b_subFile`; `LoadVariationList` includes loose Maya files; select handlers refresh buttons + version column; `versionFile` resolves when `path_variationDirectory` is a file; `SetSubType` / `buildAssetForm` use content-based version-column gates

**Features**:
- **Mixed subtype level**: sets row shows dir + file icon buttons together; folder select keeps version column; file select hides version column but keeps file buttons on sets row
- **Mixed set + variants**: variation row shows Add Variation + file buttons when variant subdirs and loose files coexist under `path_set`
- **Files-only / dirs-only**: prior single-mode behavior preserved (file buttons only vs dir buttons only)
- **Metadata on loose variation files**: file select in variation list drives `getMetaDataFromFile` via `versionFile` file-path resolution

**Decisions**:
- Dir and file button visibility composed independently from **immediate children** of the browse directory — do not infer file actions from `hasSub` alone
- Hide version column only when parent-list selection is itself a file (`b_subFile` / `b_varFile`), or when the resolved version parent has neither child dirs nor Maya files
- Variation column uses same dynamic row pattern as sets (`mRow_variationButtons` + `uiUpdate_variationButtons`)

**Status**: ✅ Complete — user verified in Maya

---

### July 2, 2026 - Empty shot list anim export fallback
**What**: Fixed silent no-op when `exportShotsToIndividualFiles` (or cutscene per-shot branch) was enabled but the scene had no `AnimList` shots — prep completed, batch reported success, no FBX written.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `_export_single_anim_fbx` helper; empty `shotList` falls back to single file at `exportName`; fail `fbx_export` if `exportFBXFile` and zero `_export_results`
- EXTENDED: `Features/Feature_SceneExportFlow.md` — path rule + anti-pattern + failure stage

**Features**:
- **Anim export, no shots**: writes `exportName` FBX with warning log instead of skipping FBX
- **Safety**: `No FBX files written` prevents false batch success

**Status**: ✅ Code complete — Maya verify Chr_0V_C no-shot + per-shot regression

---

### June 22, 2026 - MetaHuman feature doc + constrain_rig deleteUnused safety
**What**: Captured facial solve design contract in `Feature_Metahuman.md`; hardened `constrain_rig` so unmapped target joints that are **ancestors** of matched targets are never deleted (`protected_unused` vs `deletable_unused`).  
**Files**:
- NEW: `cgmToolsDev/Features/Feature_Metahuman.md`
- EXTENDED: `cgmToolsDev/AGENTS.md` — MetaHuman feature doc cross-link
- EXTENDED: `ProjectScripts/MetahumanFacial.py` — `_protected_target_ancestors`, `_deletable_unused_target_joints`; constrain_rig check_only reports both buckets

**Features**:
- **deleteUnused safety**: structural unmapped parents of matched joints kept even when unmapped
- **Dev docs**: feature spec; timeline tracked on this branch (UnrealWorkflow)

**Decisions**:
- ProjectScripts remains iteration home; **factor reusable core into cgm proper** when API stabilizes (see Deliverables + Notes)
- `transfer_rig` REST POSE block frozen unless explicitly requested — invariants in feature doc

**Status**: ✅ Complete

---

### June 2026 - MetaHuman transfer_rig (SDK transfer pipeline)
**What**: Full facial SDK transfer from target hierarchy onto source: rest capture, bridge.rest base SDK, offset locators, target curve cache, snap-sampled control pose SDKs.  
**Files**:
- EXTENDED: `ProjectScripts/MetahumanFacial.py` — `transfer_rig` and helpers (rest TR, offset locators, movement cache, channel transfer, audit)

**Features**:
- **check_only** + **testControl** filter for incremental validation
- **REST POSE INVARIANTS**: attr-based rest (`getAttr` tx–rz), never xform; bridge.rest @ 0 holds base pose; control SDK @ 0 is always 0
- **Offset locators** (`MH_offset_*`): parentConstraint target sdk → locator; snap source sdk to locator per pose key
- **Movement cache**: skip static joints per channel; **pose_baseline** restore between channels
- Undo chunk + full plug restore at end

**Decisions**:
- Replicate target SDK topology on source; control→bridge assumed wired on scene
- Pose keys: set **control only**, snap sdk → locator, `setDrivenKeyframe` **without** explicit `value=`
- Rejected: xform rest, bridge driving during sample, locator differential math without snap, per-pose SDK disconnect loops

**Status**: ✅ Code complete — full-face Maya verification ongoing

---

### June 2026 - MetaHuman constrain_rig + get_driven_data + joint/bridge foundation
**What**: Lightweight target-follow (`constrain_rig`), SDK curve introspection (`get_driven_data`), joint pairing (`snap_source_to_target`), control→bridge probe (`map_controls_to_bridge`), mirror helpers, manual Fortnite `d_wire` map.  
**Files**:
- EXTENDED: `ProjectScripts/MetahumanFacial.py` — `constrain_rig`, `get_driven_data`, `snap_source_to_target`, `map_controls_to_bridge`, `mirror_face_joints`

**Features**:
- **constrain_rig**: parentConstraint target sdk → source sdk; optional deleteUnused (deepest-first, ancestor-safe after June 22)
- **get_driven_data**: read SDK animCurve keys on bridge/joint plugs for audit + transfer cache
- **map_controls_to_bridge**: axis probe with baseline restore; overlaps conceptually with `sdk_utils` — factor later

**Status**: ✅ Code complete — Maya verification ongoing

---

### June 15, 2026 - Non-ref export post-delete selection (master in delete_tdSet)
**What**: Fixed non-referenced `ExportScene` failing with `No object exists: master` when `master` is intentionally in `delete_tdSet`. Non-ref prep now mirrors referenced `Prep()`: constraints cleared on export set members before delete, per-rig delete sets via `resolve_td_set_for_asset`, and FBX selection from surviving `export_tdSet` members — not the export context hint (`master`).  
**Files**:
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `export_select_targets_resolve`, `export_constraints_clear_on_members`, `export_prep_non_referenced`; `Prep()` final selection uses shared helper
- EXTENDED: `cgm/core/mrs/Scene.py` — non-ref single + multi-root prep call `export_prep_non_referenced`; `_export_transforms_after_mesh_strip` falls back to export set members; export root discovery logs clarify context-hint vs post-delete DAG

**Features**:
- **Crate non-ref export**: `master` in `delete_tdSet`, `export_tdSet` = geo + `rootMotion_jnt` → batch/export selects export members after delete (including re-run on `*_baked.mb`)
- **Multi-rig namespaced**: namespace on hint drives tdSet resolution; no global `*:delete_tdSet` bleed on post-ns delete

**Decisions**:
- `exportObjs` entries remain bake/orchestration hints only — never assumed to exist after `ProcessDeleteSet`
- Shared prep logic lives in `bakeAndPrep` so referenced and non-ref paths stay aligned

**Status**: ✅ Code complete — Maya runtime verification user-side (Crate non-ref + baked file re-export; referenced export smoke test)

---

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

### MetaHuman Facial Solve (ongoing — ProjectScripts)
- [x] `snap_source_to_target`, `map_controls_to_bridge`, `get_driven_data`
- [x] `transfer_rig` with REST POSE invariants and offset-locator sampling
- [x] `constrain_rig` with safe deleteUnused (protected ancestors)
- [x] Dev feature spec (`Feature_Metahuman.md`)
- [ ] Shelf / UI wrapper for probe → transfer → constrain
- [ ] Persisted `bridgeMapping` per character variant
- [ ] Full-face Maya regression scenes + batch/mayapy smoke
- [ ] **Factor facial SDK core into cgm proper** — see Notes (target: `sdk_utils`, `mrs/lib/face_utils`; keep `d_wire` in ProjectScripts)

### MetaHuman Body Align (mocapBakeTools)
- [x] `mocap_align_utils` — CCL, resolve, local-TR capture / snap / bake
- [x] mocapBakeTools Align UI + dual-path bake (legacy vector when offsets unset)
- [x] Feature contracts (`Feature_MocapAlignSnap.md`, body-align section in `Feature_Metahuman.md`)
- [ ] Maya verification checklist pass (foot IK + finger; multi-skeleton; legacy CCL)
- [ ] Deprecate duplicate project-script align UI once parity confirmed
- [ ] Optional Google Doc artist section / preset browser under `cgmDat/mocap/`

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
- [x] Mixed browse levels (dirs + loose `.ma/.mb` at same path): sets/variation icon rows and version column visibility (`uiUpdate_setsButtons`, `uiUpdate_variationButtons`, `_version_column_should_show`)
- [x] Export queue bulk add from multi-selected Sets/Variation/Version files (toolbar **Add to queue as**; RMB queue single-file only)
- [x] Animate mirror context on rigs with duplicate module names + direction modifiers (`mirror_get` tag matching; `animate_utils.context_get` guard)

### Low
- [x] Playback stopped before frame-scrub bakes (`cgmGEN.playback_stop` + PostBake / Locinator / bakeAndPrep / mocap / funcIterTime)
- [x] AnimFilter close confirmation on window **X** (`BaseMelWindow.VERIFY_CLOSE` + `animFilterTool.confirmClose`)
- [x] Structured export / batch / delete-set logging for triage (log-based; UI summary optional later)
- [x] End-of-export summary: per-shot list, frame ranges, paths, UP axis (`log_export_results_summary`; batch rollup)
- [x] Read-only depot FBX fail-fast + non-writable path batch report (`path_utils`; P4 checkout deferred)
- [x] Nested-ref bake/export/delete tdSet resolution (`resolve_td_set_for_asset`)
- [x] Mayapy FBX import order + lazy FBX version probe (no `FBXExportFileVersion` spam at batch start)
- [x] Ground snap / `groundPos` respect Maya scene up (Y-up and Z-up; unified helpers in `position_utils` / `snap_utils`)
- [x] nCloth preset profiles + apply helper with scene-up nucleus gravity (`nCloth_utils`, `cgmNCloth_presets`)
- [x] cgmSimChain cloth map + attach (`attach_to_cloth_dynFK` / `attach_toShape` surface tracks, `dynFKTool` Cloth `>>` / Attach to Cloth, follicle / rivet / uvPin)
- [x] cgmSimChain Init Sim + layered nCloth Fabric/Solver presets + `solver_high` (`setup_sim_dynFK`, split menus, `profile_load` layering)
- [x] cgmSimChain target bake via `bake_nodes` / `bakeResults(simulation=True)` + post-bake **`targets_disconnect`**
- [x] cgmSimChain Fabric/Solver menus — explicit preset apply only (no auto-apply on attach/Details rebuild)
- [x] **Feature_SimChain.md** design contract (canonical dev/TA reference)
- [x] cgmSimChain **Tools → Query Settings** (`query_settings_selection`, preset diff from `base`)
- [x] nCloth presets exclude `isDynamic` (runtime switch, not fabric profile)
- [x] cgmSimChain editable base name on loaded setup (`set_base_name`)
- [x] `mirror_get` disambiguates modules with same name/type/direction but different `cgmDirectionModifier` (FRNT vs none); animate `context_get` guard when `module_get` fails
- [x] mocapBakeTools local-TR align/snap/bake (`mocap_align_utils`); dual-path legacy vector bake when offsets unset
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
- **Mixed browse level (set folders + loose `.ma/.mb`)**: ✅ User verified — dir + file buttons together; version column follows folder vs file selection.
- **Export queue multi-select (toolbar Add to queue as)**: ✅ User verified — multiple version files enqueue in one action; RMB suppressed on multi-select.
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
Improves Scene export reliability for Unreal-oriented workflows: rig single-file behavior, clearer errors, non-referenced namespace and bake/delete parity with referenced `Prep`, nested-ref tdSet resolution (`resolve_td_set_for_asset`), writable-path pre-check and batch non-writable reporting (P4 checkout deferred), FBX plugin bootstrap for mayapy batch, export success summary (shots, frames, paths, UP axis), multi-reference cutscene delete-set isolation and post-`deleteMesh` selection recovery, Scene column save/export icon rows with save-here filename stubs and version-directory parity, **export queue multi-select bulk enqueue (toolbar) with Builder-style file-list popup rebuild**, global `playback_stop` before frame-scrub bakes, AnimFilter verify-close on window **X**, structured logging for batch and delete-set cleanup, Send to Build / MRS Build observability, quieter project `fillDefaults`, batch rig master control when prerig helper messages are missing, prerig ratio arrange + curve EP lane tools, scene-up-aware ground snap (Z-up fix for Point Special **Ground**, `groundPos`, master-block placement), MetaHuman facial skeleton prune (`pruneSkeletonToJoints`), **mocapBakeTools local-TR body align/snap/bake (`mocap_align_utils`, dual-path legacy vector bake)**, Maya Be Odd cascade UI windows dev action, and removal of unused `Scene2.py`.

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
- Mixed browse levels: dir + file icon buttons composed independently on sets/variation rows; `_version_column_should_show` + `b_subFile` / `b_varFile` for version column visibility
- Export queue: multi-select on Sets/Variation/Version lists; toolbar **Add to queue as** → `AddSelectedToExportQueue`; RMB **To Queue as** → `AddToExportQueue` (single item); file-list popups rebuilt via Builder pattern (`_wireFileListScrollSelect`, no menu when multi-select)

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

### 21. mocapBakeTools local-TR align / snap / bake (`mocap_align_utils`, `mocapBakeTools`)
- NEW `mocap_align_utils`: CCL IO, skeleton-root / rig-NS resolve, capture (`doLoc` + local TR), snap (`movePointSnap` / `moveOrientSnap`), `bake_connections`
- Align UI: Rig NS, Skel Roots, Capture, Snap All/Sel; Tools → debug locs
- Dual-path `bake()`: local TR when present; else legacy `POS.set` + `aim_atPoint` unchanged
- Snap without local offsets: skip + full Script Editor missing-data report

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
- ADDED: `cgm/core/lib/mocap_align_utils.py`
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
- MetaHuman **rest pose**: capture sdk node rest via **`getAttr` tx–rz** only — never `xform`; `jointOrient` breaks xform-based rest reads.
- MetaHuman **pose SDK transfer**: set control only during sampling; snap sdk → offset locator; omit `value=` on `setDrivenKeyframe` so snapped attrs drive keys.
- MetaHuman **constrain_rig deleteUnused**: unmapped joints on the parent chain of matched targets are structural — protect, do not delete.
- Scene scroll-list **bottom buttons** and **version column visibility** must be derived from **level content** (child dirs + Maya files) and **selection type** (`b_subFile` / `b_varFile`) — `hasSub` / `hasNested` mean “any child dir exists” and must not gate file actions or hide the version column when loose files are present.
- **File-list context menus** (Sets/Variation/Version): use **Builder** pattern — `delete()` popup on each selection change, rebuild only for single-select; static popups + enable/vis toggles do not reliably suppress Maya RMB on `iconTextScrollList`.
- **Export queue bulk add** is toolbar-only; RMB queue stays one primary item. Re-bind `sc` on the scroll list after replacing `selCommand` so popup sync runs on Ctrl/Shift multi-select (`cgmScrollList` registers callback at create time).
- **`_wireFileListScrollSelect`**: do not invoke select handlers during initial UI build before sibling columns exist (`variationList` may still be `None`).
- nCloth **`mass`** in the Attribute Editor maps to plug **`pointMass`** on the shape; parent `mass` is compound — preset applier aliases and skips non-scalar attrs.
- nCloth presets intentionally **do not** set collision thickness / self-collide / collision flags — cloth collision is scene-specific (character body, layers, thickness).
- Nucleus **`gravityDirection`** for nCloth presets must follow **`scene_up_axis_get()`** — same Z-up lesson as ground snap; do not hardcode Y-down in apply paths.
- **cgmSimChain cloth attach** uses nCloth **outputMesh**, not input mesh — resolve via `get_out_mesh_shape` before tracker placement.
- **Attach to Cloth** requires setup-level **`mCloth`** — no silent fallback to selection; gate UI until mapped.
- **`mCloth`** links the nCloth **transform** (not shape) — shape `viewName` breaks `get_message` readback; use plain `listConnections` in `get_mapped_cloth`.
- **`mel createRivet`** is not available in current Maya/py3 builds — rivet path uses Constraints-menu internal API or classic edge-loft node network in **`node_utils.createRivetOnMesh`**.
- **Cloth surface tracks**: `follicle` (follicle UV), `rivet` (face/edge rivet), `uvPin` (`create_UVPin` + locator) — all via `attach_toShape(..., surfaceTrack=)`; locators under track for connect/bake.
- **cgmSimChain reload**: `reload_dependencies()` + `cgmGEN._reloadMod` on toolbox launch and **Setup → Reload** — required after editing `dynamic_utils` / `constraint_utils` / `node_utils` during dev.
- **Init Sim Setup** creates nucleus without hair — map cloth (`>>`) expects this path when artists have nCloth but no dynamic curve chain; `time1 → currentTime` must be wired on nucleus and nCloth after map.
- **nCloth preset layering**: fabric profiles touch **`nc`** only; solver profiles touch **`n`** only — pair in UI (`cotton` + `solver_high`), not one monolithic preset.
- **`isDynamic`** is not preset data — sim enable/disable is artist workflow; Query Settings and `profile_load` skip it.
- **Target bake**: `mc.bakeResults(..., simulation=True)` then **`targets_disconnect`** on baked target chains — do not rely on `disableImplicitControl` alone for loc→target cleanup.
- **Cloth preset menus**: default **`Fabric`** / **`Solver`** placeholders; apply only when artist picks a profile — Details rebuild (attach/map) must not call `profile_load`.
- **Query Settings** returns **diff from `base`** + paste-ready block — use **Tools → Query Settings** or `NCLOTH.query_settings_selection()` when capturing tuned cloth for new presets.
- **`mc.ls(..., long=True)`** — not `longPath` (Maya cmds flag name).
- **`mirror_get`**: always match **`cgmPosition` / `cgmPositionModifier` / `cgmDirectionModifier`** via `getCGMNameTags(['cgmDirection'])` — absent tags are **`False`**, not “ignore in comparison”. Omitting unset attrs caused duplicate matches (e.g. `L_coat` matching both `R_coat` and `R_FRNT_coat`).
- Animate **`context_get`**: treat failed **`module_get`** as `{}` when collecting controls — `mirror_get` exceptions must not cascade to `'NoneType' object is not subscriptable`.
- **Body align offsets**: capture with **`doLoc` at rotate pivot**, parent to source joint, store **`localTranslate` / `localRotate`** — do not mix with legacy world-vector `positionOffset` / forward-up for the same links.
- **mocapBakeTools dual-path**: no local TR → keep Manual Set / vector bake; with local TR → locator snap/bake. Snap never falls back to vector aim — report every skipped pair.
- **Multi-MH scenes**: set **Skel Roots** before Capture/Snap; short CCL patterns alone are ambiguous without roots.

### Future Considerations
- AnimFilter: conditional confirm (e.g. only when `_actionList` is non-empty or file dirty) via `confirmClose()` override.
- Optional **`p4 edit`** before export — see **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)**
- Rig FBX: confirm `_rig_fbx_export_to_path` no-takes path on same builds as anim export.
- Consider a UI hint/disable state for options not applicable to selected mode.
- Curve tweak row: optional `rebuild` toggle for distribute; lane-align `samples` / `refine_steps` exposed in UI if artists need tuning.
- Ratio arrange: optional `cubicRebuild` / target-curve entries on toolbox row; store last custom ratio in optionVar.
- Optional skin-cluster / bind preflight before `pruneSkeletonToJoints` (or auto-detach helper) if facial strip becomes a one-click artist tool.
- Cloth attach: optional manual UV / face placement override (closest-point is default for all three surface tracks); chain rebuild parity for `clothAttach` chains.
- Query Settings: optional copy-to-clipboard; full-profile export toggle (not only diff from `base`).
- nCloth: `cotton_static` or similar only if artists need a documented “sim off” utility — still must not use `isDynamic` in fabric presets.
- **Factor MetaHuman facial core into cgm proper** when API stabilizes: `get_driven_data` / SDK helpers → **`sdk_utils`**; joint match, bridge probe, rest/transfer helpers → **`mrs/lib/face_utils`**; thin **`tools/`** or ProjectScripts caller for orchestration; character **`d_wire`** maps stay project-specific. Do not split REST POSE + offset-locator sampling prematurely.
- **Body align**: deprecate duplicate project-script align UI after Maya parity; optional Scene menu → mocapBakeTools; preset browser under `cgmDat/mocap/`; optional pre-export align bake hook.

---

*Last Updated: July 28, 2026 (mocapBakeTools local-TR align/snap/bake + `mocap_align_utils`)*  
*Branch Status: Active*
