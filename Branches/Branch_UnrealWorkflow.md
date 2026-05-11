# Branch: jburton/UnrealWorkflow

## 📋 Quick Info
**Status**: Active  
**Created**: April 23, 2026  
**Last Updated**: May 9, 2026 (Save/export icon buttons + file dialog defaults, rig/cutscene export refinements + mesh-strip transform recovery, namespace-aware delete-set, `zUpRoot` helper, subtype invariants registry, Arnold plugin load guard, exception logging revamp, batch `worldUp`, ribbon attach kwargs + module child traversal hardening, moduleTarget wiring on parent change, eyeLook resolution hardening)  
**PR**: Pending

## 🎯 Goals
Harden Scene export behavior so Unreal-oriented exports are consistent, repeatable, and predictable for animation and rig workflows. Track export issues and fixes in one place, with explicit validation criteria and PR-ready notes.

## 📚 Related Documentation
- **[Scene.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Scene.py)** - Main Scene UI, `RunExportCommand`, `ExportScene`, `BatchExport`, `SendToBuild`
- **[Builder.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Builder.py)** - `ui_toStandAlone` (MRS Build), `uiFunc_process` batch / logging
- **[Project.py](../../../repos/cgmToolsPy3/cgm/core/tools/Project.py)** - `Project.data`, `fillDefaults` (project picker / version menus)
- **[RigBlocks.py](../../../repos/cgmToolsPy3/cgm/core/mrs/RigBlocks.py)** - `cgmRigMaster.rebuildMasterShapes` (batch rig / master controls)
- **[bakeAndPrep.py](../../../repos/cgmToolsPy3/cgm/core/tools/bakeAndPrep.py)** - Bake, Prep, `ProcessDeleteSet`, texture breaking
- **[cgm_General.py](../../../repos/cgmToolsPy3/cgm/core/cgm_General.py)** - Shared logging helpers
- **[ml_breakdown.py](../../../repos/cgmToolsPy3/cgm/core/lib/ml_tools/ml_breakdown.py)** - Optional diagnostics touchpoint
- **[NewBranch_Guide.md](./NewBranch_Guide.md)** - Branch documentation format reference

## 🗓️ Timeline

### May 9, 2026 - Scene UI: save/export icon buttons + file dialog defaults
**What**: Replaced text MelButton controls with `MelIconButton` icon buttons for set/subset/variation/version actions, added explicit Save/New Version/Export icon buttons in the version and sets rows, added an "Export Here" menu item, and pre-filled Maya save/export dialog filenames/paths via reusable helpers. Also corrected swapped icon/callback assignments so the version row uses Save/New Version + Export semantics consistently.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `SaveVersion` extracted helpers `_compute_next_version_save_basename` / `_save_here_suggested_stub`; `uiPath_mayaSaveTo` accepts a `defaultFilename` and uses it as `fileDialog2` startingDirectory; `uiPath_mayaSaveTo_sets/variant/version` pass suggested names; new `ExportSelection` `sets` mode + `ExportSelection_sets` wrapper; icon buttons wired to correct save/export callbacks (icon-only, 25x25, `cgmUI.guiButtonColor`)
- ADDED: `cgm/images/icons/new_set.png`, `cgm/images/icons/new_dir.png`, `cgm/images/icons/new_version.png`, `cgm/images/icons/export_file.png`; updated `cgm/images/icons/new_file.png`

**Features**:
- "Save new version" → `new_version.png` calling `SaveVersion()`
- "Export selected objects…" → `export_file.png` calling `ExportSelection(mode='version')` and `ExportSelection_sets()` for the version and sets rows respectively
- New "Export Here" menu item alongside save/new-version/export icon buttons
- File dialog now pre-fills suggested filename and starts in the resolved directory

**Status**: ✅ Complete

---

### May 8, 2026 - Export refinements: rig/cutscene paths, mesh-strip transform recovery, namespaced delete-set + `zUpRoot` helper
**What**: Hardened FBX export pathing/naming for rig and cutscene modes, recovered transforms after mesh-strip steps so `deleteMesh`-driven exports do not silently lose targets, made delete-set resolution namespace-aware, and added a root-motion utility (`zUpRoot`).  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — added `_export_transforms_after_mesh_strip` for post-strip DAG recovery; abort export when `deleteMesh` removes all export DAGs; animation folder/name logic uses selected set or leaf token, treats `none`/`null` as no animation; only appends animation name for non-static/non-rig exports; `exportAnimPath` resolution simplified (rigs use asset path); rig filenames produced as `{assetName}_rig.fbx`; cutscenes collapse per-shot output into a single anim folder with asset disambiguation; rig exports skip per-shot splitting and unnecessary directory creation
- EXTENDED: `cgm/core/tools/bakeAndPrep.py` — `resolve_delete_set` is now namespace-aware; `ProcessDeleteSet` accepts an optional `resolved_set` param to force per-rig resolution; namespace parsing/handling fixed in `Prep`
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

### Low
- [x] Structured export / batch / delete-set logging for triage (log-based; UI summary optional later)
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
- **Anim/Cutscene shot split behavior**: ⚠️ Not changed in this pass; requires runtime verification.
- **Static export + texture-link option behavior**: ⚠️ Not changed in this pass; requires runtime verification.
- **Cross-mode path consistency**: ⚠️ Requires runtime verification with project data variants.

### Residual Risk
- Runtime behavior in Maya + Unreal ingest still needs a manual verification pass for full confidence.

---

## 🚀 PR Notes

```markdown
# Scene Export: Unreal workflow (rig stability, logging, bake/delete, MRS Build)

## Overview
Improves Scene export reliability for Unreal-oriented workflows: rig single-file behavior, clearer errors, non-referenced namespace and bake/delete parity with referenced `Prep`, structured logging for batch and delete-set cleanup, Send to Build / MRS Build observability and window placement, quieter project `fillDefaults`, batch rig master control when prerig helper messages are missing, and removal of unused `Scene2.py`.

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

## Files Modified
- `cgm/core/mrs/Scene.py`
- `cgm/core/mrs/Builder.py`
- `cgm/core/tools/Project.py`
- `cgm/core/mrs/RigBlocks.py`
- `cgm/core/tools/bakeAndPrep.py`
- REMOVED: `cgm/core/mrs/Scene2.py`

## Testing
- ✅ Static / lint checks on touched files
- ⏳ Full Maya batch rig export + Unreal ingest (user runtime)

## Breaking Changes
- **External only**: anything that imported `cgm.core.mrs.Scene2` must use `Scene`.

## Next Steps
- Runtime pass: batch rig, non-referenced + namespaced root, verify bake member count and delete-set logs
- Unreal ingest spot-check on exported FBX
```

---

## 📝 Notes

### Architectural Patterns Established
- Export mode should strictly govern whether optional export toggles are applicable.
- Mode-incompatible options must be ignored rather than partially honored.
- Shared helpers (`ProcessDeleteSet`, bake set resolution) keep referenced vs non-referenced paths consistent.
- Parse DAG nodes with `split('|')[-1]` before inferring namespace/bake/delete set names.

### Lessons Learned
- A small conditional guard can remove high-impact ambiguity in file-output behavior.
- Capturing triage + validation criteria up front helps keep export fixes measurable.
- Anything that only ran inside `Prep()` never ran for non-referenced exports until explicitly duplicated or shared.
- `cgmMeta.getMessageAsMeta` returns **`False`** when a message is missing; do not chain meta-only APIs on that return without a truthiness check.
- `log.debug` still prints when the effective logger level is DEBUG; opt-in env flags are safer than `log.debug` alone for very hot paths like `fillDefaults`.

### Future Considerations
- Optional lightweight UI toast or summary line after export when `RunExportCommand` / batch returns failure (logs remain source of truth).
- Consider a UI hint/disable state for options not applicable to selected mode.

---

*Last Updated: May 9, 2026 (Save/export icon buttons + file dialog defaults, rig/cutscene export refinements + mesh-strip transform recovery, namespace-aware delete-set, `zUpRoot` helper, subtype invariants registry, Arnold plugin load guard, exception logging revamp, batch `worldUp`, ribbon attach kwargs + module child traversal hardening, moduleTarget wiring on parent change, eyeLook resolution hardening)*  
*Branch Status: Active*
