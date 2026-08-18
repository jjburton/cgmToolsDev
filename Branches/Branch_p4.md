# Branch: p4

## 📋 Quick Info
**Status**: Active  
**Created**: August 12, 2026  
**Last Updated**: August 18, 2026 (batch export P4 context + cgmP4 revert path fix)  
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
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format reference

- **`.cursor/rules/perforce-checkout.mdc`** - Agent workflow when py3 files need P4 checkout before edit

## 🗓️ Timeline

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
- **New file in client**: confirm **Add** before `p4 add`
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

### Phase 2 — Export integration ← **preflight shipped; batch summary next**
- [x] Export preflight in **`ExportScene`** before bake — **`preflight_export_output_paths`** (entry (q))
- [ ] **`Scene.BatchExport`** — richer P4-prepare rollup in batch summary (paths attempted vs skipped)
- [ ] Structured `P4PrepareError` or extended writability error (optional)

### Phase 3 — Edge cases
- [ ] New file in depot dir → `p4 add` (binary type if required)
- [ ] Sidecar `.bak` under P4
- [ ] Lock-by-other-user actionable messaging

### Testing
- [ ] Regression: no p4 on PATH, flag off — identical to today
- [ ] Interactive save (VC=perforce): out-of-date block, checkout confirm, cancel, already-open, locked-by-other, P4 offline — poses, animFilter, mocap, skinDat, Scene Save Version, **meta `.dat`/`.bmp`** (Slice C + entry (r) verify)
- [ ] Non-P4 regression: no checkout dialogs; optional read-only depot hint only (Slice C verify)
- [x] Scene browser: P4 popup Revert/Sync/Checkout/Submit + popup Refresh + popup **Delete** — no Maya crash on column reload (deferred `_defer_ui`)
- [ ] P4-enabled export: synced read-only FBX auto-edit, new file add, batch rollup — preflight + mayapy batch checkout **Maya verified** (entries (q), (u), (v)); batch summary extensions still open
- [x] cgmP4 shelve + Shelved Files panel + Scene popup Shelve + Mv move-to-CL
- [x] cgmP4 default changelist partial submit (subset **S**) — Maya verified (entry (s))
- [x] Documentation updated for Slice B + Slice C global save + meta sidecars + session cache + scroll-list popup fix (Refresh/P4/Delete) + shelve/shelved panel + FBX export preflight + default CL submit + submit progress

---

## 🚀 PR Notes

### Perforce integration (optional layer)

#### Overview
Adds optional Perforce checkout/add before FBX export for depot users. Non-P4 users see zero behavior change.

#### Major Features

##### 1. `cgm.core.lib.perforce` — connectivity (shipped)
Read-only query API: `query_status_report()`, `connection_info`, `query_opened`, `query_file_status`.

**Files Modified:**
- `cgm/core/lib/perforce.py` - NEW

##### 2. cgmP4 tool (shipped — artist manual P4 UI)
Connectivity, opened files by changelist, **shelved files** panel, path query, checkout, sync workspace, batch revert/submit/**shelve**, shelved delete/**move**/submit. **Default CL partial submit** (checkbox subset → **S**): create numbered CL + reopen + submit. **Submit progress bar** (interruptable). Does **not** change export behavior.

**Files Modified:**
- `cgm/core/tools/p4Tool.py` - NEW/EXTENDED
- `cgm/core/tools/lib/tool_calls.py` - `cgmP4Tool()`
- `cgm/core/tools/lib/tool_chunks.py` - Help → Other → cgmP4
- `cgm/core/mrs/Scene.py` - popup Shelve

##### 3. Project save P4 prepare (shipped — Slice B + C + meta sidecars)
Global **`prepare_output_for_write(mDat=)`** and shared **`prepare_paths_for_write`** / pose / meta / Maya-scene helpers before writes when `versionControl=perforce`. Out-of-date block; checkout/add confirm on interactive save. **Paths-first:** prepare before heavy gather (mocap, skinDat, animFilter). Wired: project cfg, Scene Save Version / Save Maya here, **meta `.dat`/`.bmp`** (`prepare_meta_files_for_write`), poses, animFilter `.afs`, mocap CCL, skinDat, batch scripts (`confirm_p4=False`).

**Files Modified:**
- `cgm/core/lib/path_utils.py` - prepare helpers, `PathWritePrepareError`, paths-first contract
- `cgm/core/tools/Project.py`, `cgm/core/cgm_Dat.py` - write hooks
- `cgm/core/mrs/Scene.py`, `PoseManager.py`, `Animate.py` - Maya/pose/meta saves
- `cgm/core/tools/animFilterTool.py`, `mocapBakeTools.py`, `mocap_align_utils.py`, `skinDat.py`
- `cgm/core/mrs/lib/batch_utils.py`, `Builder.py` - batch writes

##### 4. Session status cache (shipped)
**Files Modified:**
- `cgm/core/lib/perforce_session.py` - NEW
- `cgm/core/lib/perforce.py`, `cgm/core/tools/p4Tool.py`, `cgm/core/tools/lib/tool_calls.py`

##### 5. FBX export preflight (shipped)
- `scene_export_utils.resolve_export_fbx_paths` + `path_utils.preflight_export_output_paths` before bake in ExportScene
- Scene **Options → Auto Check Out Export Files** — silent P4 checkout/add on export when enabled (entry (u))
- **Mayapy batch** — payload carries **`projectConfig`**, **`p4User`**, **`p4Client`**, **`autoCheckoutExportFiles`**; bootstrap before `BatchExport` (entry (v)). **Regenerate batch file** after sync when P4 context changes.

##### 5b. Batch scratch scripts (shipped — edit-only)
- **`batch_utils._batch_prepare_write_path`** — **`p4_add=False`**: **`p4 edit`** when on depot; skip **`p4 add`** for local-only scratch (`mrsScene_batch.py`, etc.)

##### 6. Export-only P4 flag + batch summary (next)
- `cgm/core/tools/lib/project_utils.py` / Project UI — **`useP4OnExport`** (default off)
- `cgm/core/mrs/Scene.py` — batch export P4-prepare rollup in summary
- Optional: queue-time batch preflight without opening scene

**Configuration:**
- `useP4OnExport`: False (default)
- `CGM_EXPORT_P4`: env override for farm batch

#### Architecture Decisions

1. **Optional layer**: Triple gate before any p4 subprocess; skip silently otherwise
2. **No zooPy import**: Reference vendored code only; own module under cgm/core/lib/
3. **FBX export preflight shipped**: `preflight_export_output_paths` before bake (entry (q)); defense-in-depth writability remains in `fbx_export_selection`
4. **Paths first**: Interactive saves call **`prepare_*`** before expensive Maya work — immediate P4 UX; **`skip_prepare`** on low-level writers when UI prepared
5. **Meta sidecars mirror poses**: **`prepare_meta_files_for_write`** — dat-only vs dat+bmp via `store_thumbnail` / `include_existing_thumbnail`
6. **Default CL partial submit**: never **`submit -i` Change: default**; multi-file uses **`reopen`** to numbered CL (entry (s)); **`opened_entries`** not disk path re-resolve
7. **Mayapy batch P4**: copy interactive cgmP4 user/client + project cfg into batch payload — standalone has no Scene session (entry (v))
8. **Batch scratch scripts**: never auto **`p4 add`** — edit-only prepare (entry (v))
9. **cgmP4 revert paths**: use client-root disk path from **`p4 where`**, not raw UNC **`clientFile`** from **`p4 opened`** (entry (v))

#### Breaking Changes
None — P4 off by default; existing export behavior preserved.

#### Next Steps
1. **`useP4OnExport`** flag (default off) — export-only opt-in separate from `versionControl`
2. **Batch export** — richer P4-prepare rollup in batch summary
3. **Phase 0 audit:** Resolve open questions (FBX binary type, changelist policy, P4 error strings) before wide studio rollout

---

**Active** — Slice A/B/C + FBX export preflight + Scene auto checkout export + mayapy batch P4 context + cgmP4 revert path fix + Scene meta sidecars + cgmP4 default CL partial submit shipped; **`useP4OnExport`** optional next.

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

*Last Updated: August 18, 2026 (batch export P4 context + cgmP4 revert path fix)*  
*Branch Status: Active — useP4OnExport optional next*
