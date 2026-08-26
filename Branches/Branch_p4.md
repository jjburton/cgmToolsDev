# Branch: p4

## 📋 Quick Info
**Status**: Active  
**Created**: August 12, 2026  
**Last Updated**: August 24, 2026 (merge notes: UnrealWorkflow + Perforce)  
**PR**: Pending

## 🎯 Goals
Add an **optional** Perforce layer for depot users: audit where cgm tools write to depot paths, build `cgm.core.lib.perforce`, wire **interactive save prepare** (Slice B + C + meta sidecars shipped) and **FBX export preflight** (v1 export slice shipped). **No behavior change** when P4 is absent, disabled, or the target path is outside a client view — same code paths, errors, and logs as today.

## 📚 Related Documentation
- **[Feature_PerforceIntegration.md](../Features/Feature_PerforceIntegration.md)** - Canonical dev/TA spec: optional P4 gate, API, phases, testing
- **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)** - Superseded planning doc (kept for history)
- **[Feature_SceneExportFlow.md](../Features/Feature_SceneExportFlow.md)** - Export pipeline; v1 P4 consumer
- **[path_utils.py](../../cgmToolsPy3/cgm/core/lib/path_utils.py)** - **`prepare_output_for_write(mDat=)`** + shared **`prepare_paths_for_write`**, **`prepare_pose_files_for_write`**, **`prepare_meta_files_for_write`**, **`prepare_maya_scene_for_save`**; **paths-first** save contract; export writability pre-check, sidecar cleanup, batch non-writable path list
- **[perforce_session.py](../../cgmToolsPy3/cgm/core/lib/perforce_session.py)** - Session `_CACHE` (survives module reload; flush via Setup → Reload)
- **[perforce.py](../../cgmToolsPy3/cgm/core/lib/perforce.py)** - cgm P4 module (connectivity, write APIs, cache-first queries)
- **[zooPy perforce.py](../../cgmToolsPy3/cgm/lib/zoo/zooPy/perforce.py)** - zooPy reference only (do not import from cgm core)
- **[Feature_ProjectManager.md](../Features/Feature_ProjectManager.md)** - cgmProjectManager, project `.cfg`, paths, `dirMask`, Content/Export scroll lists
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format reference

- **`.cursor/rules/perforce-checkout.mdc`** - Agent workflow when py3 files need P4 checkout before edit

## 🗓️ Timeline

---

### August 19, 2026 (ae) - Empty asset types persist; Fill Default Asset Types menu
**What**: Project load/`fillDefaults` no longer injects `character` / `environment` / `prop` when `assetDat` is empty, so a scripts-style project stays empty after Save → Reload. Default types are opt-in: **Project Setup → Fill Default Asset Types** and **Scene File → Fill Default Asset Types** (additive; skips existing names). **Tools → Verify Asset Dirs** unchanged.  
**Files**:
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — `l_defaultAssetTypes`
- EXTENDED: `cgm/core/tools/Project.py` — `data.assetTypes_fillDefaults`; `uiAssetTypes_refill`; Setup menu item; removed auto-fill from `fillDefaults`
- EXTENDED: `cgm/core/mrs/Scene.py` — File menu item + `uiAssetTypes_fillDefaults` (refill then `uiProject_refreshDisplay`)
- EXTENDED: `Features/Feature_ProjectManager.md`, `Branches/Branch_p4.md`

**Features**:
- Empty `assetDat` is valid and persists
- Additive fill of default types with `d_dirFramework` subtypes
- Scene File menu mirrors Project Setup; Verify Asset Dirs still only creates folders from current types

**Status**: ✅ Code complete — verify empty types survive reload; Fill restores defaults; Scene categories refresh

---

### August 19, 2026 (ad) - Fstat cache keys = client-root disk path
**What**: Recursive / batch `p4 fstat` `clientFile` is mapped to the **client-root disk path** before session cache store and result matching (UNC vs `D:\p4\...` no longer miss). **`collect_unknown_files`** always unions session fstat skip with `depot_paths` so Find Unknowns **Cache** recache cannot write `notOnDepot` under Scene browser keys. Prefix map from one `p4 where` — not per file.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `_disk_path_for_fstat_client_file`; fetch store + `_query_files_status_batch`; collect cache skip union
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Code complete — verify Scene tints survive Find Unknowns Cache recache

---

### August 19, 2026 (ac) - Find Unknowns open does not flush session cache
**What**: Opening **Find Unknowns** reloads **`p4UnknownTool` only** (no `perforce_session` flush). Warm **`unknown_files`** cache fills the list; otherwise empty (no auto-scan). Toolbar **Cache** (`cache.png`) always **`warm_fstat_cache_tree`** (same as Scene P4 Cache). **Setup → Deep Scan** is disk-walk **`collect_unknown_files`** without recursive fstat. **Setup → Reload** reloads the tool + `perforce.py` but **keeps** the session cache.  
**Files**:
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `p4FindUnknownsTool()` `_reloadMod(p4UnknownTool)` only
- EXTENDED: `cgm/core/tools/p4UnknownTool.py` — `reload_tool()` no session flush; `uiFunc_cache_unknown_files`; `uiFunc_deep_scan_unknown_files`
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Code complete — verify Scene Cache → open Find Unknowns fills list; cold open stays empty; toolbar Cache prewarms; Deep Scan does not recursive fstat

---

### August 19, 2026 (ab) - Find Unknowns ext filter cell width
**What**: Extension-filter grid cells size from the **longest checkbox label** (`{ext} ({count})`) instead of a fixed 72px width, so long labels are not clipped by the next cell. `columnsResizable=False` so Maya does not squeeze columns; extra extensions wrap to the next row.  
**Files**:
- EXTENDED: `cgm/core/tools/p4UnknownTool.py` — `uiFunc_unknown_rebuild_ext_filters` cell width from max label
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Code complete — verify long ext labels fully visible in Maya

---

### August 19, 2026 (aa) - Find Unknowns per-row open folder
**What**: Each filtered file row in **Find Unknowns** has an **explorer** icon (`explorer_25.png`) that opens that file’s parent directory in Windows Explorer (Scene `OpenDirectory` / `os.startfile`). Icon strip: explorer → Add → Delete.  
**Files**:
- EXTENDED: `cgm/core/tools/p4UnknownTool.py` — `uiFunc_unknown_row_open_dir`; explorer button in `uiFunc_build_unknown_file_row`
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Code complete — verify explorer button on a filtered row in Maya

---

### August 19, 2026 (z) - Interactive save skip-add (no Add popup)
**What**: Interactive P4 prepare no longer prompts to **`p4 add`**. New Scene versions, first-time meta `.dat`/`.bmp`, poses, animFilter, mocap CCL, skinDat, and project `.cfg` write locally; artists add later via **Find Unknowns** or Scene popup **Add**. Dialogs remain for **checkout**, **locked-by-other**, and **out of date**. Export **Auto Check Out Export Files** still silently adds new FBX when that option is on (`p4_add=autoCheckoutExportFiles`).  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — default **`p4_add=False`**; confirm only on checkout; silent add when `p4_add=True`; **`p4_add`** on export prepare/preflight
- EXTENDED: `cgm/core/mrs/Scene.py` — export preflight **`p4_add=autoCheckoutExportFiles`**
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Features/Feature_SceneExportFlow.md`, `Branches/Branch_p4.md`

**Features**:
- Save Version / first-time meta: no Add popup; rows stay unknown/yellow until Add
- Existing depot file not checked out: Checkout / Cancel unchanged
- Export Auto Check Out **off**: new FBX local write (no add); existing FBX still checkout-confirm on interactive

**Decisions**:
- Interactive = edit-only; add is an explicit artist step (Find Unknowns / Scene Add) or export Auto Check Out
- Never an Add confirm dialog — `confirm_p4` applies to checkout only

**Status**: ✅ Code complete — verify Save Version + first-time meta + Auto Check Out on/off in Maya

---

### August 18, 2026 (y) - Project Content/Export scroll lists use project dirMask
**What**: **cgmProjectManager** Content and Export directory scroll lists now filter with the same merged **`dirMask`** as Scene browser navigation and Project **P4 Cache** fstat warmup — base mask (`meta`, `.mayaSwatches`, `incrementalSave`, `cgmDat`, `mayaSwatches`) plus General **`dirMask`** comma field. Editing **`dirMask`** live-refreshes both scroll lists. **`path_utils.walk_below_dir`** mask checks are case-insensitive and prune masked dirs during `os.walk`.  
**Files**:
- EXTENDED: `cgm/core/tools/Project.py` — **`project_dir_mask`**, **`uiProject_build_dir_mask`**, **`uiProject_dirMask_refresh_lists`**; scroll list **`rebuild`** passes mask; **`uiProject_p4_cache_dir_mask`** uses shared helper
- EXTENDED: `cgm/core/lib/path_utils.py` — case-insensitive **`l_mask`** + **`dirs[:]`** prune in **`walk_below_dir`**
- NEW: `Features/Feature_ProjectManager.md` — design contract for Project tool, paths, mask consumers
- EXTENDED: `Branches/Branch_p4.md`, `Guides/NewFeature_Guide.md`

**Features**:
- Mask parity: Project Content/Export trees, Scene **`l_dirMask`**, P4 fstat cache tree walk
- **`dirMask`** text field change callback → rebuild Content + Export lists without Save
- **`uiProject_fill`** builds **`self.l_dirMask`** and pushes to scroll lists before rebuild

**Decisions**:
- Single merge function **`project_dir_mask`** — avoid drift between P4 cache and UI trees
- Lowercase normalized mask entries; walk/compare case-insensitive (matches Scene **`d.lower() in l_dirMask`**)

**Status**: ✅ Code complete — verify masked folders hidden in Content/Export lists; custom **`dirMask`** token; P4 Cache skips same dirs

---

### August 18, 2026 (x) - Batch auto checkout gate + all-path export preflight
**What**: Fixed batch export checking out depot FBX files when **Auto Check Out Export Files** was **off** — `confirm_p4=False` only skipped dialogs, not `p4 edit`. Export preflight now uses **`p4_checkout = autoCheckoutExportFiles or logExportSummary`** (batch + option off → writability-only; ledger **`p4_skipped_auto_checkout_off`**). **Multi-path preflight** (cutscene / per-namespace FBX): **`preflight_export_output_paths`** checks **all** planned paths before failing; raises **`ExportPreflightFailedError`** with full failure list (each path logged; user cancel on checkout dialog still aborts immediately).  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — **`p4_checkout`** kwarg on export prepare chain; **`ExportPreflightFailedError`**; **`p4_skipped_auto_checkout_off`** ledger outcome
- EXTENDED: `cgm/core/mrs/Scene.py` — preflight gates + multi-failure logging / `_preflight_ctx['failures']`
- EXTENDED: `Features/Feature_SceneExportFlow.md`, `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Maya verified — batch with Auto Check Out off fails read-only without checkout; cutscene preflight reports all locked/not-writable paths

---

### August 18, 2026 (w) - Batch export P4 prepare summary
**What**: **`BatchExport`** end log now includes a structured **P4-prepare rollup** per export path — edit/add/already-open, skipped (VC off, offline, edit-only), and failed (out of date, locked, not writable) with optional **`sceneFile`** context from preflight. Session ledger in **`path_utils`**: **`record/get/clear_export_prepare_records`**, **`log_export_prepare_summary`**. Failed batch items may attach **`p4Outcome`** / **`p4Reason`**.  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — export prepare ledger; recording in `_prepare_p4_for_write`, `prepare_output_for_write`, `check_export_output_writable`; `prepare_context` on preflight helpers
- EXTENDED: `cgm/core/mrs/Scene.py` — `BatchExport` uses `clear_export_prepare_records` + `log_export_prepare_summary`; preflight passes `sceneFile`; batch `_resFail` P4 enrichment
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Features/Feature_SceneExportFlow.md`, `Branch_p4.md`

---

### August 18, 2026 (v) - Batch export P4 context + batch script edit-only + cgmP4 revert paths
**What**: **Mayapy batch export** now receives project + P4 connection from Scene UI so FBX preflight can **`p4 edit`** in standalone (previously failed `File is not writable` when Auto Check Out Export Files was on). Batch payload adds **`projectConfig`**, **`p4User`**, **`p4Client`**, **`autoCheckoutExportFiles`**; **`batch_export_context_from_ui`**, **`apply_batch_export_context`**, **`batch_export_setup_script_lines`** in `batch_utils`; **`BatchExport`** bootstraps before export. **Scratch batch launchers** (`mrsScene_batch.py`, `*_batch.py`, `*_MRSbatch.py`) use **`p4_add=False`** — edit depot files only, never silent **`p4 add`**. **cgmP4 revert** on opened files: **`resolve_client_disk_path`** / **`revert_opened_entry`** map `p4 opened` UNC **`clientFile`** to client-root disk path via **`p4 where`** (matches Scene popup revert, which uses browser paths under `D:\p4\...`).  
**Files**:
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — batch export context helpers; mayapy preamble; **`_batch_prepare_write_path`** → **`p4_add=False`**
- EXTENDED: `cgm/core/lib/path_utils.py` — **`p4_add`** kwarg on **`prepare_output_for_write`** / **`_prepare_p4_for_write`**
- EXTENDED: `cgm/core/lib/perforce.py` — **`resolve_client_disk_path`**, **`revert_opened_entry`**; **`revert()`** resolves client-root path
- EXTENDED: `cgm/core/tools/p4Tool.py` — row/changelist revert uses **`revert_opened_entry`**
- EXTENDED: `cgm/core/mrs/Scene.py` — batch payload wiring; **`BatchExport`** bootstrap; preflight log line
- EXTENDED: `Features/Feature_SceneExportFlow.md`, `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Maya verified — mayapy batch export with Auto Check Out Export Files + cgmP4 connected in interactive session; cgmP4 revert on added file with UNC clientFile

---

### August 17, 2026 (u) - Scene Auto Check Out Export Files
**What**: Scene **Options → Export → Auto Check Out Export Files** (`cgmVar_sceneUI_auto_checkout_export_files`, default off). When on, interactive export preflight runs silent **`p4 edit`** / **`p4 add`** on planned FBX paths (`confirm_p4=False`) instead of checkout/add confirm dialogs. Still fails on out-of-date, locked-by-other, not-in-client, P4 disconnected + read-only. Mayapy batch: see entry **(v)** — requires batch payload P4 context (regenerate `mrsScene_batch.py` after sync).  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — optionVar, Options menu, Load/SaveOptions, `ExportScene` kwarg `autoCheckoutExportFiles`, `confirm_p4` rule
- EXTENDED: `Features/Feature_SceneExportFlow.md`, `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Maya verified — interactive + mayapy batch (with entry (v) payload)

---

### August 17, 2026 (t) - cgmP4 submit progress bar
**What**: Maya **interruptable progress bar** during cgmP4 **Submit** (changelist **S** and per-row Submit). **`progress_cb`** on **`submit_paths`** / **`submit_change`** / **`_submit_default_partial`**. Default CL multi-file subset: 3 steps (create CL → reopen → submit); other submit paths: 1 step with status text. Cancel between steps logs warning (may leave empty pending CL if cancelled after create).  
**Files**: EXTENDED `cgm/core/lib/perforce.py`, `cgm/core/tools/p4Tool.py` — **`uiFunc_run_submit_*`**, **`uiFunc_p4_progress_*`**; EXTENDED `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Status**: ✅ Code complete — verify bar on default CL partial + whole-CL submit

---

### August 17, 2026 (s) - Default changelist partial submit fix
**What**: Fixed cgmP4 **subset submit** from the **default changelist** (uncheck files → **S** on remainder). Perforce limits: **`p4 submit -d`** accepts only **one** file pattern; **`submit -i` Change: default** fails (`Default change unknown`). **Shipped flow:** multi-file → **`create_pending_change`** + **`reopen_paths -c`** using **`clientFile`** from **`opened_entries`** + **`submit -c`**; single file → **`submit -d DESC clientPath`**. Path resolution: pass **`opened_entries`** from Opened Files list (not re-derived disk paths); **`_resolve_depot_submit_line`** + **`p4 where`** fallback for Scene/UNC.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — **`reopen_paths`**, **`_submit_default_partial`**, **`_depot_file_lines_for_opened_entries`**, **`_resolve_depot_submit_line`**, **`_where_depot_path`**
- EXTENDED: `cgm/core/tools/p4Tool.py` — **`uiFunc_get_cl_selection`** returns entries; **`uiFunc_run_submit_paths`**
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Fixes**:
- Multi-path `submit -d` → `Missing/wrong number of arguments`
- `submit -i` Change: default → `Default change unknown`
- `no depot path for …` on UNC / mapped workspace paths when resolving from client path alone

**Status**: ✅ Maya verified — default CL partial submit (2 of 3 files) on DDE SourceArt workspace

---

### August 17, 2026 (r) - Scene meta sidecar prepare (`.dat` + `.bmp`)
**What**: Scene version **meta** sidecars follow the PoseManager pattern: **`prepare_meta_files_for_write`** before writing `meta/<version>.dat` and optional sibling `.bmp`. **Refresh Data** prompts **Data** / **Data + Thumb** / **Cancel**; **Update Thumb** (button + thumb RMB) prepares both paths then captures 256×256 viewport thumb. **saveMetaData** / notes save prepare `.dat` and existing `.bmp` when present. Open-scene guard blocks refresh when selected version ≠ open file.  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — **`prepare_meta_files_for_write`**
- EXTENDED: `cgm/core/mrs/Scene.py` — **`_meta_paths_from_version`**, **`_meta_prepare_paths_for_write`**, **`updateMetaThumbnail`**, **`refreshMetaData`**, **`saveMetaData`**; meta details **Refresh Data** / **Update Thumb** row
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- Locked `meta/*.dat` or `meta/*.bmp` → P4 checkout dialog before gather/write (VC=perforce + in-scope + connected)
- Data-only refresh prepares `.dat` only; thumb update / Data+Thumb prepares both
- **`include_existing_thumbnail=True`** on dat save so paired bmp stays writable when only metadata changes

**Status**: ✅ Code complete — verify Refresh Data, Update Thumb, notes save + P4 cancel on locked meta sidecars in Maya

---

### August 17, 2026 (q) - FBX export preflight (before bake)
**What**: **`ExportScene`** resolves planned FBX output paths and runs **`preflight_export_output_paths`** before bake/prep — fail fast on read-only depot targets. **Writability** preflight for all FBX modes; **P4** fstat/checkout only when **`versionControl=perforce`** + path in scope + cgmP4 connected (same gate as save rollout). Interactive export: checkout confirm before bake; batch: **`confirm_p4=False`**.  
**Files**:
- NEW: `cgm/core/mrs/lib/scene_export_utils.py` — **`resolve_export_fbx_paths`**, **`resolve_no_shot_export_name`**
- EXTENDED: `cgm/core/lib/path_utils.py` — **`prepare_export_output_for_write`**, **`preflight_export_output_paths`**
- EXTENDED: `cgm/core/mrs/Scene.py` — export preflight stage **`export_preflight`**; **`AnimList`** load moved before bake rename
- EXTENDED: `Features/Feature_SceneExportFlow.md`, `Features/Feature_PerforceIntegration.md`, `Branch_p4.md`

**Features**:
- Per-shot, cutscene, rig multi-root, static, and single-file anim paths resolved pre-bake
- Locked FBX → error/dialog before **`ExportScene >> Bake | start:`**
- P4 cancel on checkout → clean abort, no bake

**Status**: ✅ Code complete — verify anim/cutscene/rig/static + batch + VC=none regression in Maya

---

### August 17, 2026 (p) - Global save rollout (Slice C) + paths-first contract
**What**: Rolled **`path_utils`** save prepare across interactive depot write paths (beyond Slice B project `.cfg`). Established **paths-first** save contract: once the output path is known, call **`prepare_*`** before expensive Maya work so P4 checkout / writability dialogs appear immediately. **Hard gate:** P4 subprocess + confirm dialogs only when **`project_uses_perforce(mDat)`** and path in scope; non-P4 mode skips P4 and may show optional depot read-only hint only.  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — **`get_project_mDat`**, **`path_under_root`**, **`path_in_p4_scope`**, **`prepare_paths_for_write`**, **`prepare_pose_files_for_write`**, **`prepare_maya_scene_for_save`**, **`_maybe_warn_p4_writability_hint`**, **`_resolve_use_p4_for_path`**; paths-first module comment + docstrings
- EXTENDED: `cgm/core/mrs/Scene.py` — Save Version, Save Maya here, meta sidecars, export rig-update save
- EXTENDED: `cgm/core/mrs/PoseManager.py`, `cgm/core/mrs/Animate.py` — pose save/update/rename/duplicate/copy; path-based P4 scope (not UI mode radio)
- EXTENDED: `cgm/core/tools/animFilterTool.py` — `.afs` Save / Save As; prepare before gather
- EXTENDED: `cgm/core/tools/mocapBakeTools.py` — **Setup → Save** / **Save As…**; prepare before connection resolve; clean P4 cancel (no traceback)
- EXTENDED: `cgm/core/lib/mocap_align_utils.py` — **`save_ccl(..., skip_prepare=False)`** for UI-prepared writes
- EXTENDED: `cgm/core/lib/skinDat.py` — prepare before **`updateSourceSkinData`**
- EXTENDED: `cgm/core/tools/Project.py` — **`uiPath_MayaSaveTo`**
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py`, `cgm/core/mrs/Builder.py` — batch script writes with **`confirm_p4=False`**
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Features/Feature_MocapAlignSnap.md`, `Branches/Branch_p4.md`, `AGENTS.md`

**Features**:
- **Paths first:** resolve path → **`prepare_*`** → gather/build → write (documented in feature doc + `path_utils`)
- **mocapBakeTool:** **Save** overwrites loaded CCL path; **Save As…** file dialog; falls back to Save As when no current path
- **P4 scope:** **`path_in_p4_scope`** uses project roots / pose path / client view — not PoseManager UI mode default
- **Low-level writers:** **`skip_prepare=True`** when UI already prepared (mocap **`save_ccl`**)
- **Batch/farm:** **`confirm_p4=False`** — no interactive checkout dialogs

**Fixes**:
- mocap CCL save: 4–5 s delay before P4 popup — prepare ran after **`resolve_connections`** / validation; moved prepare to start of save
- skinDat / animFilter: same class of delay — prepare moved before skin gather / action dict sync
- mocap P4 checkout **Cancel** — duplicate errors + traceback; **`PathWritePrepareError`** handled once at UI layer

**Decisions**:
- Interactive saves: **`confirm_p4=True`** (default); batch/mayapy: **`confirm_p4=False`**
- Non-P4 projects: no P4 subprocess; optional read-only depot hint via **`_maybe_warn_p4_writability_hint`**
- FBX export prepare shipped same day — see entry **(q)** (not part of Slice C rollout commit)

**Status**: ✅ Code complete — verify Save/Save As + locked-file prompt timing on mocap, poses, animFilter, skinDat, Scene Save Version in Maya (VC=perforce)

**See also**: [`Feature_PerforceIntegration.md`](../Features/Feature_PerforceIntegration.md) (Save flow contract); [`Feature_MocapAlignSnap.md`](../Features/Feature_MocapAlignSnap.md) (CCL Save menu)

---

### August 17, 2026 (o) - Shelve workflow + cgmP4 Shelved Files panel
**What**: End-to-end **shelve** support in cgmP4 and Scene browser popups — partial files, description prompt, P4V-style revert-after-shelve, **Shelved Files** panel (query + delete/submit/move), and **Move to changelist (Mv)** via unshelve + delete source shelf. cgmP4 **Setup → Reload** aligned to standard cgm tool pattern (`reload_dependencies` + `cgmGEN._reloadMod` + `super().reload()`); section empty messages (e.g. `(no shelved changelists)`) use the same full-width centered row as **Status**. Per-changelist rows remain **animFilter-style collapsible `MelFrameLayout`** sub-sections (checkbox + labeled frame + batch buttons).  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `shelve_paths`, `shelve_change`, `query_shelved`, `iter_shelved_changelist_groups`, `delete_shelf_*`, `submit_shelved_change`, `create_pending_change`, `unshelve_*`, `move_shelf_*`; default-CL shelve via **Change: new** form; revert-after-shelve; indexed ztag parse (`depotFile0`); removed subprocess `bufsize` warning
- EXTENDED: `cgm/core/tools/p4Tool.py` — **Opened Files** **Sh** + row Shelve; **Shelved Files** section (blue-tint headers); header **D** / **Mv** / **Sub**; persistent empty-state rows; `showUI()` window reuse; standard `reload()` (dynFK/mocapBake pattern)
- EXTENDED: `cgm/core/mrs/Scene.py` — Perforce popup **Shelve**; shared submit/shelve path action; revert add on shelve failure after prepare
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `cgmP4Tool()` reloads P4UTIL + p4Tool on open
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- **Opened Files:** batch **Sh** + per-row Shelve (subset or whole CL); description via `cgmUI.uiPrompt_getValue`
- **Shelved Files:** `p4 changes -s shelved` + `p4 describe -sS`; per-CL collapsible frame; **D** delete shelf (subset/whole); **Sub** submit shelved CL; **Mv** move to target CL (`number` / `default` / `new`)
- **Mv semantics:** `unshelve -s SOURCE -c TARGET` → `shelve -d -Af` on source; target ends with **local opens** (red triangle), not shelved-only
- **Scene popup Shelve:** selected file(s) only; same description + prepare rules as Submit
- **Empty sections:** `(not loaded)`, `(no opened files)`, `(no shelved changelists)` — centered Status-style row at section level (not inside dynamic content column)

**Fixes**:
- Default changelist shelve: **Change: new** input form — filtered `p4 change -o default` caused "Default change unknown"
- Post-shelve revert (P4V default) — shelved-only blue triangle vs red triangle opens+shelf
- Shelved CL file count (0): parse `depotFile0` indexed ztag fields from `p4 describe -sS`
- Stale cgmP4 window after code reload: use **Setup → Reload** (standard `self.__class__()` rebuild), not Refresh alone

**Decisions**:
- P4 cannot move a shelved copy directly between CLs — relocate = unshelve + optional delete source shelf (Mv)
- Partial shelved submit not supported — **Sub** is whole shelved CL only (`p4 submit -e`)
- No `UI_LAYOUT_VERSION` / force-delete window loop — match other cgm tools; dev reload via Setup → Reload

**Status**: ✅ Code complete — verify shelve, Shelved panel, Mv partial/whole, Scene popup Shelve in Maya

**See also**: [`Feature_PerforceIntegration.md`](../Features/Feature_PerforceIntegration.md) (shelve/Mv API + cgmP4 UI); [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md) (collapsible CL header pattern)

---

### August 17, 2026 (n) - Scene browser popup Delete crash fix
**What**: Maya **ACCESS_VIOLATION** when deleting a file from Scene browser scroll-list popups (asset / sets / variation / version). Same Qt reentrancy class as entry (l): popup **Delete** rebuilt the owning `iconTextScrollList` synchronously (`LoadVersionList` → `select_last` → `selectIndexedItem`) while `QMenu::exec` was still active. **Refresh** and P4 post-write were already deferred; **Delete** was not.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `_defer_list_reload_after_delete(mode)`, `_reload_lists_after_asset_delete()`; all five popup **Delete** menu items use `_defer_ui(cgmGEN.Callback(uiFunc_deleteSelectedInList, …))`; bulk + single delete paths defer column reload; single version delete aligned to `LoadVersionList` (was `LoadVariationList`)
- EXTENDED: `Features/Feature_CgmToolUI.md`, `Features/Feature_PerforceIntegration.md`, `Branch_p4.md`

**Symptoms fixed**:
- Clean Maya session → Scene → version column RMB → **Delete** → confirm → crash in `Qt5Core.dll` / `QItemSelectionModel::select` (Python stack: `uiFunc_deleteSelectedInList` → `LoadVersionList` → `select_last`)

**Fix**:
- Defer popup Delete handler and post-delete reload (`_defer_ui` + `_defer_list_reload_after_delete`) — menu closes before confirm dialog and `ra=True` / selection restore
- Defense in depth: reload deferred inside `uiFunc_deleteSelectedInList` even if called outside popup

**Status**: ✅ Shipped — code complete; verify Delete on version / sets / variation columns in Maya

**See also**: entry (l); [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md) (popup + `ra=True` pitfall)

---

### August 13, 2026 (m) - P4 + Scene Script Editor log noise cleanup
**What**: Removed high-chatter **info/warning** lines that fired on normal Scene browser use (P4 column gates, asset popup build). Cache hits and lightweight status probes stay silent at default log level.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `query_project_p4_status` / `query_connection` cache hit + fetch messages → `log.debug` (doc already said project probe has no logging)
- EXTENDED: `cgm/core/mrs/Scene.py` — removed leftover debug `log.warning` in `HasSub` (called once per subtype in asset popup loop)
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branch_p4.md`

**Symptoms fixed**:
- Repeated `# cgm.core.lib.perforce : Using cached Perforce status (project)` on column load / P4 tint pass
- Repeated `# Warning: cgm.core.mrs.Scene : HasSub ||||||||| laksj;flaksjdfkl; >> …` when opening asset list popup

**Decisions**:
- Session cache working as intended is **not** artist-visible — reserve `log.info` for user-initiated reports (`query_status_report`, Print Log, path query)
- Hot-path helpers (`query_project_p4_status`, `scene_list_p4_enabled`) must not warn/info per call

**Status**: ✅ Shipped

---

### August 13, 2026 (l) - Scene browser scroll-list popup crash fix
**What**: Intermittent Maya **ACCESS_VIOLATION** when P4 popup actions (Revert/Sync/etc.) or column **Refresh** rebuilt the owning `iconTextScrollList` synchronously — `ra=True` → `QTreeWidget::clear()` while Qt popup menu still active. Fixed with deferred column reload + Builder-style refresh guard.  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` — `_defer_ui()` (`mc.evalDeferred` + `cgmGEN.Callback`); `_refresh_searchable_display` disables `b_selCommandOn`, `deselectAll` before `ra=True`; P4 post-write + popup/column Refresh wired through `_defer_ui`
- EXTENDED: `Features/Feature_CgmToolUI.md`, `Features/Feature_PerforceIntegration.md`, `Branch_p4.md`

**Root cause**:
- P4 menu callback → `_scene_p4_after_write()` → `LoadVersionList()` → `_refresh_searchable_display()` → `sl(e=True, ra=True)` on the **same widget** that owns the right-click popup, during `QMenu::exec` — Qt selection-model reentrancy crash (not a Python logic bug)

**Fix**:
- Defer list reload to next idle tick: `_scene_p4_after_write`, popup **Refresh**, popup **Delete** (see entry (n)), column refresh icon, asset-list popup Refresh
- Harden `_refresh_searchable_display`: temp `b_selCommandOn=False`, `deselectAll` before `ra=True`, restore in `finally` (match `BlockScrollList.rebuild`)

**Status**: ✅ Shipped — user verified Revert path no longer crashes

**See also**: [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md) (popup + `ra=True` pitfall)

---

### August 13, 2026 (f) - Scene browser scroll list display (phases 1–3)
**What**: Scene asset-browser columns distinguish folders vs files without polluting canonical selection. Parallel `SceneListRow` model (`.item` vs `.alias`); folders-first sort; dir alias `name/`; row tint via `itc`; Builder-style append+itc refresh. **No per-row icons yet** (phase 2 deferred). Complements July mixed-level button work — display layer only; path resolution and `b_subFile` / `b_varFile` unchanged.  
**Files**:
- NEW helpers: `cgm/core/mrs/lib/scene_utils.py` — `SceneListRow`, `scene_list_sort_rows`, `scene_list_filter_rows`
- EXTENDED: `cgm/core/classes/GuiFactory.py` — `cgmScrollList.setRows`, canonical `getSelectedItem()` / `selectByValue()` via `_ml_rows`; `clear()` widget-only (Builder-aligned)
- EXTENDED: `cgm/core/mrs/Scene.py` — `_refresh_searchable_display`, `_push_searchable_rows`; LoadCategory/SubType/Variation/Version loaders; filter/clear filter; **Show all files** refreshes all affected columns
- EXTENDED: `Features/Feature_CgmToolUI.md` — Scene browser list section

**Features**:
- Dirs show as `rig/` with cool row tint; files unchanged basename; dirs listed before files in mixed columns
- Search matches canonical name and alias; optionVar restore uses `.item` only
- **Pitfall fixed**: blank lists when `setRows` called `clear()` before append loop — follow `BlockScrollList.update_display` (ra → append → itc per display index)

**Decisions**:
- Display-only decoration in `.alias`; never strip suffixes from saved paths
- Reuse existing `iconTextScrollList` widget — row icons not available from cmds; dir alias `+ name/` instead
- P4 file status on rows — `itc` tint + alias suffix via `.data['p4Status']` (see entries (i)–(j))

**Status**: ✅ Shipped — user verified in Maya

**See also**: [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md) (pattern contract)

---

### August 13, 2026 (m) - Scene browser P4 fstat session cache
**What**: Scene navigation in P4 mode caches `p4 fstat` results per `(user, client, path)` in `perforce_session._CACHE`. Navigation reuses cache (no subprocess when revisiting a folder). Column **Refresh** icon / popup **Refresh** invalidates **that column's directory only** (`invalidate_fstat_directory`) then reloads. P4 popup writes invalidate affected paths only; full `flush_status_cache()` reserved for cgmP4 global Refresh / connection change. Deduped duplicate `LoadVersionList` on set→variation navigation.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce_session.py` — `fstat_by_path` in `_CACHE`
- EXTENDED: `cgm/core/lib/perforce.py` — cache-first `query_files_status` / `query_file_status` (chunked misses); `invalidate_fstat_paths`, `invalidate_fstat_directory`; write APIs invalidate fstat selectively
- EXTENDED: `cgm/core/mrs/Scene.py` — `_refreshSubTypeList` / `_refreshVariationList` / `_refreshVersionList`, `_invalidate_p4_directory_for_column`, `_scene_p4_after_write(list_key=)`; `_version_list_refreshed` dedupe
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Features/Feature_CgmToolUI.md`

**Decisions**:
- Stale P4 colors after external depot changes (P4V, other user) until artist hits column Refresh — no background polling in v1
- Navigation does not invalidate cache; Refresh explicitly drops directory entries then re-fstats

**Status**: ✅ Code complete — verify revisit speed + per-column Refresh scope

---

### August 13, 2026 (k1) - Scene browser P4 menu: Checkout + Add
**What**: Perforce popup gains **Checkout** (`p4 edit`) and **Add** (`p4 add`) before Revert/Sync/Submit; fstat validation + confirm (out-of-date blocks checkout; on-depot blocks add).  
**Files**: `Scene.py`, `Feature_CgmToolUI.md`, `Feature_PerforceIntegration.md`  
**Status**: ✅ Shipped

---

### August 13, 2026 (k) - Scene browser P4 right-click menu
**What**: Perforce section on file scroll-list popups (SubType, Variation, Version): **Revert**, **Sync** (selected file), **Submit**. Built only when `versionControl=perforce`; items disabled when P4 not connected; enabled for file rows when connected.  
**Files**:
- NEW: `sync_file` in `cgm/core/lib/perforce.py`
- EXTENDED: `cgm/core/mrs/Scene.py` — `_append_p4_file_menu`, `uiFunc_p4_*`, select-handler enable refresh
- EXTENDED: `Features/Feature_CgmToolUI.md`, `Features/Feature_PerforceIntegration.md`

**Decisions**:
- Sync = `p4 sync <path>` not whole workspace (artist out-of-date fix on selected row)
- Submit uses `submit_paths([path])` with changelist confirm (match cgmP4)
- Post-action: `flush_status_cache()` + **deferred** column reload via `_defer_ui` (P4 row colors refresh; avoids popup reentrancy crash — see entry (l))

**Status**: ✅ Code complete — verify Maya checklist in plan

---

### August 13, 2026 (j) - Scene browser P4 alias suffix + locked tint
**What**: Shipped polish on (i): alias suffix `(status)` after file basename (display-only); **`locked_by_other`** red tint + `(locked-by-other)` / `(open-elsewhere)`; unknown changed from gray to **yellow** for contrast vs synced off-white. User verified in Maya.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `file_status_ui_suffix`; `classify_file_status_ui` priority adds `locked_by_other`
- EXTENDED: `cgm/core/mrs/lib/scene_utils.py` — `SCENE_LIST_ITC_P4_LOCKED`, `scene_list_file_alias`; apply resets plain alias when no status
- EXTENDED: `Features/Feature_CgmToolUI.md`, `Features/Feature_PerforceIntegration.md`, `Branch_p4.md`

**Decisions**:
- Classification priority: locked → checked out / add → out of sync → unknown (not on depot)
- Synced at head: no suffix, default off-white; query errors / not-in-client: no suffix, default tint
- Search filter matches suffix text (e.g. `locked` finds `(locked-by-other)` rows)

**Status**: ✅ Shipped — user verified

---

### August 13, 2026 (i) - Scene browser P4 file-row colors
**What**: File rows in SubType / Variation / Version columns tint by Perforce status when project `versionControl=perforce` **and** P4 connected. Batch `p4 fstat` per column load; dirs unchanged (blue). Status keys: checked out (blue), marked for add (green), out of sync (orange), unknown / not on depot (yellow), locked by other (red); synced files stay default off-white.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `query_files_status`, `classify_file_status_ui`
- EXTENDED: `cgm/core/mrs/lib/scene_utils.py` — `SCENE_LIST_ITC_P4_*`, `scene_list_apply_p4_file_itc`, `SceneListRow.data`
- EXTENDED: `cgm/core/mrs/Scene.py` — `_apply_p4_file_row_colors` in LoadSubType/Variation/VersionList
- EXTENDED: `Features/Feature_CgmToolUI.md`, `Features/Feature_PerforceIntegration.md`

**Decisions**:
- Gate on `project_uses_perforce` + `query_project_p4_status()['connected']` — no fstat when offline or versionControl none
- Colors on row at load time; column Refresh re-queries; search filter preserves stored row `itc` / alias
- Query errors / not-in-client → default file tint (no P4 suffix)

**Status**: ✅ Shipped — extended by (j)

**See also**: [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md) (pattern contract)

---

### August 13, 2026 (h) - Scene browser selection highlight (`itc` / `hlc`)
**What**: Selected scroll rows stay readable — match Builder `BlockScrollList.setHLC`. Maya inverts the selection row; light pastels / white `itc` copied straight to `hlc` wash out. Scene dirs/files now use **saturated base `itc`** + **dimmed `hlc`** (`itc × 0.7`) on every select and after list refresh.  
**Files**:
- EXTENDED: `cgm/core/mrs/lib/scene_utils.py` — `SCENE_LIST_HLC_DIM`, darker `SCENE_LIST_ITC_DIR` / `SCENE_LIST_ITC_FILE`
- EXTENDED: `cgm/core/classes/GuiFactory.py` — `cgmScrollList._syncHLCFromSelection(dim=0.7)`; wired from `selCommand`, `selectByValue`, `selectByIdx`
- EXTENDED: `cgm/core/mrs/Scene.py` — `_refresh_searchable_display` calls `_syncHLCFromSelection` after repopulate
- EXTENDED: `Features/Feature_CgmToolUI.md` — `itc`/`hlc` table + tuning constants

**Decisions**:
- Same hue on select (blue folder → darker blue highlight), not gray fallback — gray only as widget default before first pick (Builder create-time `hlc=[.5,.5,.5]`)
- Tune colors in `scene_utils.py` only; do not parse alias strings for color

**Status**: ✅ Shipped — user verified readability

---

### August 13, 2026 (g) - Scene browser row icons — not supported; alias prefix instead
**What**: Attempted per-row icons on Scene `iconTextScrollList` columns (`appendDisplayRow`, cgm PNG paths, `numberOfIcons=1`). **Maya cmds API does not display row icons** on this control (behaves as text-only; icon gutter may appear empty). Reverted to **text markers**: dir alias `+ name/` + trailing `/`, folder-first sort, dir `itc` tint. Removed `numberOfIcons=1`.  
**Files**:
- EXTENDED: `cgm/core/mrs/lib/scene_utils.py` — `scene_list_row_alias`, `SCENE_LIST_DIR_ALIAS_PREFIX`; removed unused `scene_list_row_icon`
- EXTENDED: `cgm/core/classes/GuiFactory.py` — `appendDisplayRow` text+itc only
- EXTENDED: `cgm/core/mrs/Scene.py` — no `numberOfIcons` on searchable lists
- EXTENDED: `Features/Feature_CgmToolUI.md` — document Maya limitation + prefix convention

**Status**: ✅ Shipped — user verified text lists; icons N/A on Mel scroll list

---

### August 13, 2026 (e) - Session status cache + cgmP4 open performance
**What**: P4 status queries cached in **`perforce_session._CACHE`** so module reload and cgmP4 re-open do not re-run full `p4 info` / opened / fstat on every open. cgmP4 **reuses existing window**; cache-first Project P4 status row.  
**Files**:
- NEW: `cgm/core/lib/perforce_session.py` — `_CACHE`, `clear()`
- EXTENDED: `cgm/core/lib/perforce.py` — cache-first `query_connection`, `query_project_p4_status`; `flush_status_cache()`, `reload_session_cache()`
- EXTENDED: `cgm/core/tools/p4Tool.py` — `showUI()` window reuse; `uiFunc_refresh(force=False)`; Setup → Reload via `cgmGEN._reloadMod`
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `cgmP4Tool()` no reload on open
- EXTENDED: `cgm/core/tools/Project.py` — P4 status row cache-first refresh

**Behavior**:
- Warm cache: cgmP4 open + Project General P4 row near instant (no subprocess)
- **Refresh** / P4 writes: `force=True` or `flush_status_cache()` re-query
- **Setup → Reload**: `cgmGEN._reloadMod(perforce_session)` + perforce + p4Tool

**Status**: ✅ Code complete — verify cgmP4 re-open speed + Refresh still updates

---

### August 13, 2026 (d) - Project config save P4 prepare (Slice B)
**What**: Scene **File → Save** / dat save runs global `path_utils.prepare_output_for_write()` when project `versionControl` is `perforce` — fstat + confirm + `p4 edit` / `p4 add` before write. Wired in `Project.data.write()` and `cgm_Dat.data.write()`.  
**Files**:
- EXTENDED: `cgm/core/lib/path_utils.py` — `prepare_output_for_write()`, `_prepare_p4_for_write()`, `PathWritePrepareError`
- EXTENDED: `cgm/core/tools/Project.py` — `data.write()` via global prepare (`mDat=self`)
- EXTENDED: `cgm/core/cgm_Dat.py` — `data.write()` global prepare hook
- EXTENDED: `cgm/core/mrs/Scene.py` — `uiProject_saveAndRefresh` aborts on failed save

**Status**: ✅ Code complete — verify Scene File → Save scenarios below

**Behavior**:
- **Out of date** (haveRev < headRev): block save + dialog; sync first
- **Synced read-only on depot**: confirm **Checkout** before `p4 edit` (Cancel → no write)
- **New file in client**: no Add prompt — local write (skip-add; see entry (z))
- **Already checked out** by you: no prompt; save proceeds
- **Locked by other** / not in client: error, no write
- **P4 offline**: skip P4 silently; fail only if file still read-only locally

---

### August 13, 2026 (c) - Project versionControl + P4 status (Slice A)
**What**: Project General `versionControl` (`none`|`perforce`); live P4 status row (green connected / orange not connected); `project_uses_perforce()`, `query_project_p4_status()`.  
**Files**:
- EXTENDED: `cgm/core/tools/lib/project_utils.py` — schema + `project_uses_perforce()`
- EXTENDED: `cgm/core/lib/perforce.py` — `query_project_p4_status()`
- EXTENDED: `cgm/core/tools/Project.py` — General UI
- EXTENDED: `Features/Feature_PerforceIntegration.md`

**Status**: ✅ Code complete — verify in Project tool General section

---

### August 13, 2026 (b) - cgmP4 changelist UI + status buffer
**What**: Opened Files grouped by changelist (animFilter-style header rows); batch **R** / **S** with per-file checkboxes; Print Log uses buffered status (no re-query); status panel full-width layout; batch revert/submit APIs.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `iter_opened_changelist_groups`, `log_status_report`, `revert_change`, `submit_paths`; `CREATE_NO_WINDOW` on Windows
- EXTENDED: `cgm/core/tools/p4Tool.py` — changelist sections, `_p4_status_dat` buffer, `uiFunc_changelist_revert` / `uiFunc_changelist_submit`
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_p4.md`

**Features**:
- Per-changelist collapsible sub-section: master checkbox, compact **R** / **S** buttons, per-file checkbox + row Revert/Submit
- **R**: subset checked → per-file `p4 revert`; all/none checked → `p4 revert -c`
- **S**: subset checked → `p4 submit -c CL path…`; all/none checked → whole changelist submit
- **Refresh** queries once → UI + `_p4_status_dat`; **Print Log** → `log_status_report(buffer)` only
- Status block: `MelHSingleStretchLayout` + `column_adj=True` (see `Feature_CgmToolUI.md`)

**Decisions**:
- cgmP4 submit/revert is artist manual workflow — **export v1 still open-for-edit only** (no auto-submit)
- Dynamic changelist sub-sections do not persist collapse state in optionVars (rebuilt on Refresh)

**Status**: ✅ Code complete — verify in Maya

---

### August 13, 2026 - cgmP4 UI polish + P4 write actions
**What**: Restyled cgmP4 (BlockConfig-style frames, margins, scroll); collapsible Opened Files list with Revert/Submit rows; top-level Sync Workspace; path Checkout; write APIs in perforce.py.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `edit`, `add`, `edit_or_add`, `revert`, `sync_workspace`, `submit_change`, `flatten_opened_entries`
- EXTENDED: `cgm/core/tools/p4Tool.py` — full UI restyle
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- Collapsible sections: Connection, Status, Opened Files, Path Query
- Alternating grayscale opened-file rows with Revert / Submit (multi-file CL confirm)
- Sync Workspace on Connection toolbar (`p4 sync` client root)
- Path Checkout (`edit_or_add`)

**Decisions**:
- Sync is workspace-wide only — not per opened-file row
- Submit submits changelist scope with confirm when CL has multiple files

**Status**: ✅ Code complete — verify in Maya

---

### August 12, 2026 (e) - cgmP4 tool + shared optionVars
**What**: Simple cgmUI window to save Perforce user/client to Maya optionVars; `resolve_connection()` reads prefs for all tools.  
**Files**:
- NEW: `cgm/core/tools/p4Tool.py`
- EXTENDED: `cgm/core/lib/perforce.py` — `get_connection_prefs`, `save_connection_prefs`, optionVar constants
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `cgmP4Tool()`
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — Help → Other → cgmP4
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- OptionVars: `cgmVar_p4_user`, `cgmVar_p4_client`
- User/client text fields, Save, Refresh, Print Log; status labels (connection, root, stream)
- Refresh queries and updates UI; Print Log prints buffered report (later refined Aug 13)

**Decisions**:
- OptionVars after explicit args, before env — artists set once in cgmP4; export and other tools inherit via `resolve_connection()`

**Status**: ✅ Code complete — verify in Maya (Help → Other → cgmP4)

---

### August 12, 2026 (d) - Explicit p4 -u / -c / -ztag connection
**What**: Reworked all server p4 calls to use explicit `-u USER -c CLIENT -ztag` (studio-solved pattern); removed registry/cwd/P4CONFIG discovery and p4 set identity diagnostics.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py`
- EXTENDED: `Features/Feature_PerforceIntegration.md`

**Features**:
- `query_status_report(p4_user=, p4_client=)` or env `CGM_P4USER` / `CGM_P4CLIENT`
- `p4 -ztag opened` / `fstat` / `info` parsing

**Decisions**:
- Required args: Perforce username + client workspace — no implicit hostname client

**Status**: ✅ Code complete — verify in Maya Script Editor

---

### August 12, 2026 (c) - P4 identity and environment diagnostics
**What**: Extended connectivity report with `p4 set`, process env comparison, P4CONFIG root walk, and identity warnings when effective user differs from expected depot username.  
**Files**:
- EXTENDED: `cgm/core/lib/perforce.py` — `query_p4_env`, `query_identity`, P4CONFIG-aware cwd, `expected_user` on report
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- P4 Environment section: `p4 set` values/sources, Maya process env, OS user, P4CONFIG roots
- Identity warnings: OS user fallback, p4 set vs p4 info mismatch, unset P4CLIENT / hostname client
- Optional `expected_user='josh.burton'` arg on `query_status_report()`

**Decisions**:
- Report only — no auto `p4 set` or env mutation from cgmTools
- P4CONFIG walk implements zooPy getDefaultWorkingDir intent without importing zooPy

**Status**: ✅ Code complete — re-run in Maya Script Editor with `expected_user='josh.burton', force=True`

---

### August 12, 2026 (b) - P4 connectivity query module
**What**: Read-only Perforce probe — connection info, opened files, pending changelists, scene fstat; Script Editor entry only.  
**Files**:
- NEW: `cgm/core/lib/perforce.py`
- EXTENDED: `Features/Feature_PerforceIntegration.md`, `Branches/Branch_p4.md`

**Features**:
- `query_status_report()` logs user, client, server, stream, opened files by changelist, pending CLs, scene depot status
- Subprocess cwd tries scene dir, project path optionVar, then getcwd; caches first working `p4 info`
- Graceful offline: `connected: False` with reason; no impact on export or other tools

**Decisions**:
- Script Editor only for v0 (no toolbox menu)
- Read-only queries do not require export opt-in flag
- `p4 -s` subprocess without shell=True

**Status**: ✅ Code complete — Maya Script Editor verify recommended

---

### August 12, 2026 - Branch + feature documentation
**What**: Started p4 branch; created feature design contract and branch timeline doc. Scoped v1 to FBX export with optional-layer principle (no P4 = no change).  
**Files**:
- NEW: `Features/Feature_PerforceIntegration.md`
- NEW: `Branches/Branch_p4.md`
- EXTENDED: `AGENTS.md`, `Features/Feature_SceneExportFlow.md`, `Plans/Plan_ExportP4Integration.md`, `Branches/Branch_UnrealWorkflow.md` (cross-links)

**Features**:
- Feature doc: optional triple gate (opt-in + is_available + is_under_client), phased plan, API sketch, audit checklist, testing
- Branch doc: deliverables checklist for Phase 0–3
- Active P4 work ownership moved from UnrealWorkflow branch to p4 branch

**Decisions**:
- P4 is purely optional — default off; no subprocess or behavior change without explicit enable + available P4 + path under client
- v1 integration target: FBX export only (`ExportScene` / `BatchExport` / `fbx_export_selection`)
- New module at `cgm/core/lib/perforce.py`; never import zooPy perforce from cgm core
- Export paths from cgm Project + Scene only (not Red9 pathing)

**Status**: ✅ Complete — docs ready; Phase 0 audit next

---

## 📦 Deliverables

### Phase 0 — Incorporation audit
- [x] Map project `.cfg` save path — **`prepare_output_for_write(mDat=)`** (Slice B)
- [x] Map interactive depot write paths — Scene Maya/meta, poses, animFilter, mocap CCL, skinDat, batch scripts, **FBX export preflight** (Slice C + export, Aug 2026)
- [x] Confirm studio `p4 info` / client root / `P4CONFIG` from Maya and mayapy — cwd probe in `perforce.py`; shell verified `p4 info`; Maya verify pending
- [ ] List P4 error strings to surface in export UX
- [ ] Skim zooPy editoradd / Red9 push_file edge cases for reimplementation
- [ ] Confirm depot rule for new `.fbx` (binary type?)
- [ ] Resolve open questions in feature doc before export Phase 1

### Phase 1 — `cgm.core.lib.perforce` + prepare helper
- [x] NEW: `cgm/core/lib/perforce.py` — subprocess p4 wrapper (connectivity queries)
- [x] Shared prefs: `cgmVar_p4_user` / `cgmVar_p4_client` + cgmP4 tool
- [x] Write slice: `edit`, `add`, `edit_or_add`, `revert`, `revert_change`, `sync_workspace`, `submit_change`, `submit_paths`, **`reopen_paths`**, **`_submit_default_partial`**, **`shelve_*`**, **`delete_shelf_*`**, **`submit_shelved_change`**, **`move_shelf_*`**, **`query_shelved`** (cgmP4 + Scene)
- [x] Scene **Auto Check Out Export Files** option — silent export P4 checkout (entry (u)); mayapy batch context (entry (v))
- [x] Batch mayapy P4 bootstrap — **`projectConfig`**, **`p4User`**, **`p4Client`** in batch payload (entry (v))
- [x] Batch scratch scripts **`p4_add=False`** — edit-only, no auto **`p4 add`** on `mrsScene_batch.py` (entry (v))
- [x] cgmP4 revert UNC **`clientFile`** fix — **`resolve_client_disk_path`** / **`revert_opened_entry`** (entry (v))
- [x] cgmP4 default CL partial submit: **`opened_entries`** + create/reopen/submit (entry (s)); submit progress bar (entry (t))
- [x] cgmP4 UI: Connection / Status / **Opened Files** / **Shelved Files** / Path Query; buffered status; batch R/S/**Sh**; shelved D/**Mv**/Sub; window reuse; standard Setup → Reload
- [x] Session cache: `perforce_session._CACHE`; cache-first queries; flush on writes / Setup → Reload
- [x] Project save prepare: **`prepare_output_for_write(mDat=)`** with confirm + out-of-date gate (Slice B)
- [x] Global save helpers: **`prepare_paths_for_write`**, **`prepare_pose_files_for_write`**, **`prepare_meta_files_for_write`**, **`prepare_maya_scene_for_save`**, **`path_in_p4_scope`**, **`get_project_mDat`** (Slice C + meta sidecars)
- [x] Interactive save wiring: Scene, PoseManager, Animate, animFilter, mocap CCL, skinDat, Project Maya save-to (Slice C)
- [x] Batch save wiring: **`batch_utils`**, **`Builder`** with **`confirm_p4=False`** (Slice C)
- [x] Save flow contract: **paths first** — prepare before heavy gather/build (documented + applied to mocap, skinDat, animFilter)
- [x] **`path_utils.prepare_export_output_for_write()`** + **`preflight_export_output_paths`** wired in ExportScene ← **shipped**
- [ ] **`useP4OnExport`** project flag (default off) in Project / export options
- [x] Subprocess cwd strategy (scene / project / getcwd) — implemented for queries
- [x] Windows: hide p4 subprocess console windows (`CREATE_NO_WINDOW`)

### Phase 2 — Export integration ← **preflight + batch summary shipped**
- [x] Export preflight in **`ExportScene`** before bake — **`preflight_export_output_paths`** (entry (q))
- [x] **`Scene.BatchExport`** — richer P4-prepare rollup in batch summary (paths attempted vs skipped) (entry (w))
- [ ] Structured `P4PrepareError` or extended writability error (optional; deferred — ledger dicts sufficient)

### Phase 3 — Edge cases
- [ ] New file in depot dir → `p4 add` (binary type if required)
- [ ] Sidecar `.bak` under P4
- [ ] Lock-by-other-user actionable messaging

### Testing
- [ ] Regression: no p4 on PATH, flag off — identical to today
- [ ] Interactive save (VC=perforce): out-of-date block, checkout confirm, cancel, already-open, locked-by-other, P4 offline, **no Add popup on new files** — poses, animFilter, mocap, skinDat, Scene Save Version, **meta `.dat`/`.bmp`** (Slice C + entry (r) + skip-add entry (z))
- [ ] Non-P4 regression: no checkout dialogs; optional read-only depot hint only (Slice C verify)
- [x] Scene browser: P4 popup Revert/Sync/Checkout/Submit + popup Refresh + popup **Delete** — no Maya crash on column reload (deferred `_defer_ui`)
- [x] Batch export P4 prepare summary — ledger + rollup (entry (w)); **Maya verified** (entry (w))
- [x] Batch auto checkout gate — **`p4_checkout`** separate from **`confirm_p4`**; option off = no batch checkout (entry (x))
- [x] Export preflight all-path check — **`ExportPreflightFailedError`** before bake (entry (x)); **Maya verified** cutscene multi-FBX
- [ ] P4-enabled export: synced read-only FBX auto-edit when Auto Check Out **on**; new file silent add only when Auto Check Out **on**
- [x] cgmP4 shelve + Shelved Files panel + Scene popup Shelve + Mv move-to-CL
- [x] cgmP4 default changelist partial submit (subset **S**) — Maya verified (entry (s))
- [x] Documentation updated for Slice B + Slice C global save + meta sidecars + session cache + scroll-list popup fix (Refresh/P4/Delete) + shelve/shelved panel + FBX export preflight + default CL submit + submit progress + **interactive skip-add** (entry (z))

---

## 🚀 PR Notes

```markdown
# Merge notes: UnrealWorkflow + Perforce

Optional Perforce for depot users. Scene export hardened for Unreal. mocapBakeTools is the body-align home. cgmSimChain supports cloth attach. Non-P4 users should see no P4 behavior.

---

## Scene

### Features

**Export**
- Rig mode always single-file (`{asset}_rig.fbx`); no per-shot split
- Stage-tagged failures on `ExportScene` / `RunExportCommand` / `BatchExport`
- Nested-ref tdSet resolution (`bake` / `export` / `delete` sets from outer namespace)
- Writability pre-check before FBX; `.bak` sidecar cleanup; export summary (shots, frames, paths, UP axis)
- Batch honors per-item `worldUp`; mayapy FBX plugin bootstrap
- Project options: **Delete mesh** (anim/cutscene, default off) and **Fix rotation** (post-euler bake, default off)
- Export queue: Ctrl/Shift multi-select + toolbar bulk enqueue (RMB still one item)
- Sets-column **Export Here**
- FBX **preflight before bake** (P4 checkout confirm; cancel = no bake)
- **Auto Check Out Export Files** (default off) — silent `p4 edit`/`p4 add` when on
- Mayapy batch carries project + P4 user/client (regenerate `mrsScene_batch.py` after sync)
- Batch end log includes P4-prepare rollup; all planned FBX paths checked before fail

**Browser**
- Icon rows: Save Maya here / Export / Save Version; save-here stub basename
- Mixed dir+file browse levels (dir and file buttons independently)
- Folder vs file display (`name/`, folders-first, dir tint); readable selection highlight
- P4 row tints + status suffix (checked out / add / out of sync / unknown / locked)
- File popup: Checkout, Add, Revert, Sync, Submit, Shelve
- **Utils → Switch Up** (Y↔Z scene up + ViewCube-safe home; does not write project `worldUp`)
- Meta sidecar prepare (`.dat` / `.bmp`) on Refresh Data, Update Thumb, notes save
- **File → Fill Default Asset Types** (mirrors Project Setup)
- `usePluralSubDirs`: plural folders, singular filename tokens (`bob_rig_01`); mixed-folder Fix Now
- Quieter startup logs

### Bugs

- Non-ref exports skipped delete sets, used the wrong bake set, or failed with `No object exists: master`
- Multi-ref cutscene could pick another rig’s `delete_tdSet`; mesh strip left stale names in selection
- Empty AnimList + per-shot = false batch success, no FBX
- Shot bake treated length as a frame (`min/max` of `[start, end, length]`)
- Version Save/Export could join `False`; metadata did not refresh from column select
- Empty/missing `rig/` folder hid Save/Export/Save Version
- Popup Refresh / P4 / Delete crashed Maya (Qt reentrancy — deferred list reload)
- Batch with Auto Check Out **off** still checked out depot FBX
- Script Editor spam from P4 cache hits and `HasSub`

---

## Project Manager

### Features

- General **versionControl** (`none` | `perforce`) + live P4 status row
- `usePluralSubDirs` checkbox; legacy configs default missing keys on project switch
- Content/Export scroll lists use the same **dirMask** as Scene and P4 Cache (live refresh)
- **Setup → Fill Default Asset Types** — opt-in additive fill
- Project `.cfg` save runs P4 prepare when VC=perforce

### Bugs

- Empty `assetDat` was refilled with character/environment/prop on Save → Reload
- `fillDefaults` flooded the Script Editor at DEBUG unless `CGM_VERBOSE_FILL_DEFAULTS`
- `usePluralSubDirs` leaked into filenames (`*_templates_01`)

---

## cgmP4 (new)

### Features

- Connection prefs (`cgmVar_p4_user` / `cgmVar_p4_client`); Help → Other → cgmP4
- Opened Files grouped by changelist; batch Revert / Submit / Shelve
- **Shelved Files** panel: delete, submit, move to changelist
- Sync Workspace; Path Checkout
- Session cache so re-open does not re-run full `p4 info`
- Interruptable submit progress bar
- Default changelist **partial submit** (checked subset → numbered CL + reopen + submit)

### Bugs

- Partial submit from default CL failed (`submit -d` / `Change: default`)
- Revert missed UNC `clientFile` paths (now `p4 where` → client-root disk path)

---

## Find Unknowns

### Features

- Per-row Open folder
- Ext-filter cells size to the longest `{ext} (count)` label
- Open does not flush session cache; toolbar Cache = fstat warmup; Setup → Deep Scan = disk walk (no recursive fstat)

### Bugs

- Cache recache could mark Scene-browser files `notOnDepot` (UNC vs `D:\p4\...` fstat keys)

---

## mocapBakeTools

### Features

- Native local-TR capture / snap / bake (`mocap_align_utils`); dual-path legacy vector bake when offsets unset
- Align UI: Rig NS, Skel Roots, Capture, Snap All/Sel; Tools → Mapping Report + debug locs
- CCL uniqueness under Skel Roots (not MetaHuman-only); sources can be driver **transforms**, not joints-only
- Target RMB reorder + `[n]` index labels; Setup → Show short names
- Last CCL autoload, status bar, Setup → Recent
- Save / Save As: P4 prepare before connection resolve

### Bugs

- Snap used a plain locator instead of `doLoc` on the target (wrong world offset with `rotateAxis`)
- CCL save blocked ArtSpine / joint-named drivers unique under Skel Roots
- P4 Cancel on save produced duplicate errors + traceback

---

## cgmSimChain

### Features

- Cloth attach + surface tracks (follicle / rivet / uvPin); map existing nCloth; hair chain unchanged
- Layered nCloth presets (fabric / solver / wind); Presets menu (Cloth / Hair / Nucleus)
- Init Sim Setup; Query Settings; editable Base Name; simulation bake of targets
- Details `<<` loads nucleus/cloth/hair from selection

### Bugs

- Bake All Targets left loc→target `parentConstraint` nodes
- Fabric/Solver menus reapplied presets on Details rebuild / attach
- Fabric apply reset `localSpaceOutput` (output-space setup treated as fabric)

---

## AnimFilter / bake tools

### Features

- Confirm on window **X**
- Playback stops before frame-scrub bake (AnimFilter, Locinator, mocap, bakeAndPrep)
- `.afs` Save / Save As: P4 prepare before gather

### Bugs

- Bake while the timeline was playing fought `currentTime`

---

## cgmToolbox / Snap / Arrange

### Features

- **Fix Rotation** Current / Animation (Anim Utils + marking menu)
- **Rotate Order** Current / Animation + enum
- **To Curve** Even / Spaced / Ratio; Ratio slide + Stack slide (Linear / Curve / To Curve)
- Ratio arrange (golden / finger / custom) on Snap, toolbox, and MRS prerig
- Align EPs (lane) + Distribute EPs on Controls tweak row
- Select* / marking-menu lists sorted by DAG hierarchy
- Maya Be Odd → Cascade UI Windows

### Bugs

- Ground snap / `groundPos` assumed Y-up (Z-up forced `Y=0`)

---

## MRS Builder / Rig

### Features

- Send to Build / MRS Build logging + window placed on screen
- `moduleTarget` rewire on block parent change; eyeLook resolution with clear errors
- Exception logging: one report per failure; `proxyMesh_verify` fail-fast; structured `connectAttr` errors
- Arnold `mtoa` loaded in batch only if the plugin is registered

### Bugs

- Missing prerig vis/settings messages → `False.doDuplicate()` crash on batch rig
- `mirror_get` mixed FRNT / non-FRNT coat modules; Animate marking menu crash
- Jonesy-class batch printed the same incomplete-settings exception once per finger
- `is_rigged` raised when `moduleTarget` was missing
- Batch `loadPlugin('mtoa')` failed on hosts without Arnold

---

## PoseManager / Animate / skinDat

P4 prepare on pose save/update/rename/duplicate and before skinDat gather. Checkout dialogs appear before expensive Maya work; new files write locally (no Add popup).

---

## MetaHuman facial (ProjectScripts)

- `transfer_rig` (SDK transfer, rest-pose invariants) and `constrain_rig` (target follow)
- `get_driven_data`, control→bridge map, joint pairing
- `pruneSkeletonToJoints` in cgm `joint_utils` (keep-list + parent chain)
- `deleteUnused` does not delete unmapped ancestors of matched targets

---

## MRS / Fortnite skeleton (ProjectScripts)

- Maps + `connect_fn_skeleton_to_mrs` in `mrs_fortnite_utils.py` (`biped.py` re-exports)
- Point + orient constraints (MRS drives FN); remapped scale `connectAttr` (not scaleConstraint)
- Upperarm twist driver mapping corrected

---

## Shared / cleanup

- New `cgm.core.lib.perforce` + `perforce_session` (optional; explicit `-u/-c/-ztag`)
- `path_utils` prepare contract: checkout existing depot files; skip add on new files; batch/farm = no dialogs
- Interactive skip-add: Save Version / first-time meta stay unknown until Find Unknowns or Scene Add
- Subtype invariants registry (`geo` / `audio` / `source`); `baseFemale_gameToon` block config
- Removed unused `Scene2.py` (external importers must use `Scene`)

---

## Still open (do not claim)

- `useP4OnExport` flag (P4 still gated by `versionControl=perforce`)
- Full Maya + Unreal ingest pass
- MetaHuman facial: no shelf UI; core not in cgm; full-face regression scenes
- mocap: deprecate duplicate project-script align UI; optional `cgmDat/mocap/` preset browser
- FN connect: full-body Maya regression; face map unused on connect
```

---

## 📝 Notes

### Architectural Patterns Established
- Optional triple gate: explicit opt-in AND is_available AND is_under_client (export)
- Project save gate: `versionControl=perforce` on project General (interactive confirm)
- **Paths-first save:** resolve path → **`prepare_paths_for_write`** / **`prepare_output_for_write`** → gather/build → write
- Module split: `perforce.py` (P4 subprocess) vs `perforce_session.py` (cache) vs `path_utils` (prepare + sidecars + writability)

### Lessons Learned
- `MelColumnLayout adj=False` shrinks row width, not height — use `MelHSingleStretchLayout` for full-width centered status (see `Feature_CgmToolUI.md`)
- Print Log should log buffered `query_connection` data, not re-query on every click
- Session cache module must **not** reload on cgmP4 open — use **Setup → Reload** (`reload_dependencies` + `cgmGEN._reloadMod` + `super().reload()`) after py edits; do not rely on Refresh alone for layout/API changes
- Section empty messages (no shelved changelists, etc.) must live in the **collapse-frame inner column** (Status stretch-row pattern), not inside the dynamic `uiFrame_*` content column — otherwise `align='center'` has no width
- Per-changelist UI stays **one header row**: checkbox + **collapsible `MelFrameLayout` (label = CL name)** + batch buttons — do not split label and frame for centering
- Perforce batch submit/revert maps cleanly to changelist sections with animFilter-style checkbox rows
- Scene browser scroll lists: **`iconTextScrollList` display must use Builder `append` + per-row `itc`** — not raw `append=` + `clear()` that wipes `_ml_rows` before populate (see `Feature_CgmToolUI.md` Scene browser section)
- **Never `ra=True` on a scroll list synchronously from its own popup menu** — defer reload with `mc.evalDeferred(..., lp=True)`; disable `b_selCommandOn` + `deselectAll` before clear (Maya/Qt crash in `QItemSelectionModel::clear` / `selectIndexedItem`). Applies to **Refresh**, **Delete**, and P4 write actions — not only P4 (see entries (l), (n))
- P4 session cache hits (`query_project_p4_status`, `query_connection`) → **`log.debug` only** — Scene column P4 gates call these many times per refresh; `log.info` spam is not actionable
- **Do not run heavy save work before `prepare_*`** — connection resolve, pose capture, skin gather, etc. delay P4 checkout dialogs (fixed mocap/skinDat/animFilter Aug 2026)
- **Meta sidecars = pose pattern** — `prepare_meta_files_for_write` for `meta/<version>.dat` + optional `.bmp`; thumb capture runs **after** prepare (same as PoseManager Update thumb)
- **Default CL partial submit** — P4 rejects multi-arg `submit -d` and `submit -i` Change: default; use **`reopen`** + numbered **`submit -c`**; pass **`opened_entries`** with **`clientFile`** (UNC paths break fstat re-resolve)
- **cgmP4 submit progress** — Maya progress bar via **`progress_cb`**; 3 steps for default CL multi-file subset; cancel between steps only (not mid-subprocess)
- **Interactive skip-add** — Save Version / first-time meta must not prompt `p4 add`; add is Find Unknowns / Scene Add (or export Auto Check Out)

### Future Considerations
- Scene browser list row icons — **not supported** on Maya `iconTextScrollList`; use `+ name/` alias prefix + tint (see `Feature_CgmToolUI.md`)
- Scene browser selection — **`itc` ≠ `hlc`**: saturated unselected text + dimmed `hlc` on select (`itc × 0.7`); Maya inverts selection row (see `Feature_CgmToolUI.md`, Builder `setHLC`)
- Scene browser P4 file rows — batch fstat, tints + alias suffix (entries (i)–(j)); **right-click Revert/Sync/Submit** (entry (k)); popup reload deferred (entries (l), (n) — Refresh, Delete, P4)
- Unknown / not-on-depot uses **yellow** not gray — off-white synced files too similar to gray
- ~~Scene Save Maya here / Save Version~~ — wired via **`prepare_maya_scene_for_save`** (Slice C)
- ~~MRS batch `_batch.py` writability~~ — **`batch_utils`** / **`Builder`** with **`confirm_p4=False`** (Slice C)
- UI toggle for export P4 opt-in
- Artist Google Doc update when validated studio-wide
- ~~Artist prefs UI for P4 user/client~~ — cgmP4 tool shipped

---

*Last Updated: August 24, 2026 (merge notes: UnrealWorkflow + Perforce)*  
*Branch Status: Active — useP4OnExport optional next*
