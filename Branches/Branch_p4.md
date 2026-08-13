# Branch: p4

## 📋 Quick Info
**Status**: Active  
**Created**: August 12, 2026  
**Last Updated**: August 13, 2026 (Scene browser P4 suffix + locked; export wire next)  
**PR**: Pending

## 🎯 Goals
Add an **optional** Perforce layer for depot users: audit where cgm tools write to depot paths, build `cgm.core.lib.perforce`, and wire FBX export checkout/add as v1. **No behavior change** when P4 is absent, disabled, or the target path is outside a client view — same code paths, errors, and logs as today.

## 📚 Related Documentation
- **[Feature_PerforceIntegration.md](../Features/Feature_PerforceIntegration.md)** - Canonical dev/TA spec: optional P4 gate, API, phases, testing
- **[Plan_ExportP4Integration.md](../Plans/Plan_ExportP4Integration.md)** - Superseded planning doc (kept for history)
- **[Feature_SceneExportFlow.md](../Features/Feature_SceneExportFlow.md)** - Export pipeline; v1 P4 consumer
- **[path_utils.py](../../cgmToolsPy3/cgm/core/lib/path_utils.py)** - **`prepare_output_for_write(mDat=)`** global save prepare; export writability pre-check, sidecar cleanup, batch non-writable path list
- **[perforce_session.py](../../cgmToolsPy3/cgm/core/lib/perforce_session.py)** - Session `_CACHE` (survives module reload; flush via Setup → Reload)
- **[perforce.py](../../cgmToolsPy3/cgm/core/lib/perforce.py)** - cgm P4 module (connectivity, write APIs, cache-first queries; export prepare planned)
- **[zooPy perforce.py](../../cgmToolsPy3/cgm/lib/zoo/zooPy/perforce.py)** - zooPy reference only (do not import from cgm core)
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format reference

- **`.cursor/rules/perforce-checkout.mdc`** - Agent workflow when py3 files need P4 checkout before edit

## 🗓️ Timeline

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
- [ ] Map remaining cgm write paths that hit depot (FBX export primary; Scene save/version `.ma`/`.mb`, batch `_batch.py` as future)
- [x] Confirm studio `p4 info` / client root / `P4CONFIG` from Maya and mayapy — cwd probe in `perforce.py`; shell verified `p4 info`; Maya verify pending
- [ ] List P4 error strings to surface in export UX
- [ ] Skim zooPy editoradd / Red9 push_file edge cases for reimplementation
- [ ] Confirm depot rule for new `.fbx` (binary type?)
- [ ] Resolve open questions in feature doc before export Phase 1

### Phase 1 — `cgm.core.lib.perforce` + prepare helper
- [x] NEW: `cgm/core/lib/perforce.py` — subprocess p4 wrapper (connectivity queries)
- [x] Shared prefs: `cgmVar_p4_user` / `cgmVar_p4_client` + cgmP4 tool
- [x] Write slice: `edit`, `add`, `edit_or_add`, `revert`, `revert_change`, `sync_workspace`, `submit_change`, `submit_paths` (cgmP4 UI test)
- [x] cgmP4 UI: Connection / Status / Opened Files (by changelist) / Path Query; buffered status; batch R/S; window reuse
- [x] Session cache: `perforce_session._CACHE`; cache-first queries; flush on writes / Setup → Reload
- [x] Project save prepare: **`prepare_output_for_write(mDat=)`** with confirm + out-of-date gate (Slice B)
- [ ] **`path_utils.prepare_export_output_for_write()`** wrapping global prepare + export triple-gate ← **next**
- [ ] `useP4OnExport` project flag (default off) in Project / export options
- [x] Subprocess cwd strategy (scene / project / getcwd) — implemented for queries
- [x] Windows: hide p4 subprocess console windows (`CREATE_NO_WINDOW`)

### Phase 2 — Export integration ← **after Phase 1 prepare helper**
- [ ] Wire from `fbx_export_selection()` before FBX MEL
- [ ] Extend batch summary: P4 attempted vs not writable (no P4)
- [ ] Structured `P4PrepareError` or extended writability error

### Phase 3 — Edge cases
- [ ] New file in depot dir → `p4 add` (binary type if required)
- [ ] Sidecar `.bak` under P4
- [ ] Lock-by-other-user actionable messaging

### Testing
- [ ] Regression: no p4 on PATH, flag off — identical to today
- [ ] Project save (VC=perforce): out-of-date block, checkout confirm, cancel, already-open, locked-by-other, P4 offline
- [ ] P4-enabled export: synced read-only FBX auto-edit, new file add, batch rollup (after export wire)
- [x] Documentation updated for Slice B + session cache

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
Connectivity, opened files by changelist, path query, checkout, sync workspace, batch revert/submit. Does **not** change export behavior.

**Files Modified:**
- `cgm/core/tools/p4Tool.py` - NEW/EXTENDED
- `cgm/core/tools/lib/tool_calls.py` - `cgmP4Tool()`
- `cgm/core/tools/lib/tool_chunks.py` - Help → Other → cgmP4

##### 3. Project save P4 prepare (shipped — Slice B)
Global **`prepare_output_for_write(mDat=)`** before project cfg / dat writes when `versionControl=perforce`. Out-of-date block; checkout/add confirm on interactive save.

**Files Modified:**
- `cgm/core/lib/path_utils.py` - `prepare_output_for_write`, `PathWritePrepareError`
- `cgm/core/tools/Project.py`, `cgm/core/cgm_Dat.py` - write hooks
- `cgm/core/mrs/Scene.py` - save abort on prepare failure

##### 4. Session status cache (shipped)
**Files Modified:**
- `cgm/core/lib/perforce_session.py` - NEW
- `cgm/core/lib/perforce.py`, `cgm/core/tools/p4Tool.py`, `cgm/core/tools/lib/tool_calls.py`

##### 5. Export prepare (next phase)
- `cgm/core/lib/path_utils.py` - prepare_export_output_for_write
- `cgm/core/cgm_General.py` - fbx_export_selection hook
- `cgm/core/mrs/Scene.py` - batch summary extensions (if needed)

**Configuration:**
- `useP4OnExport`: False (default)
- `CGM_EXPORT_P4`: env override for farm batch

#### Architecture Decisions

1. **Optional layer**: Triple gate before any p4 subprocess; skip silently otherwise
2. **No zooPy import**: Reference vendored code only; own module under cgm/core/lib/
3. **FBX v1 only**: Maya save / batch script paths deferred

#### Breaking Changes
None — P4 off by default; existing export behavior preserved.

#### Next Steps
1. **Phase 1 finish:** `path_utils.prepare_export_output_for_write()` + `useP4OnExport` flag (default off)
2. **Phase 2:** Wire `fbx_export_selection()` before FBX MEL; batch summary extensions
3. **Phase 0 audit:** Resolve open questions (FBX binary type, changelist policy, P4 error strings) before wide studio rollout

---

**Active** — Slice A/B + session cache shipped; **export prepare hook is next implementation target**.

---

## 📝 Notes

### Architectural Patterns Established
- Optional triple gate: explicit opt-in AND is_available AND is_under_client (export)
- Project save gate: `versionControl=perforce` on project General (interactive confirm)
- Module split: `perforce.py` (P4 subprocess) vs `perforce_session.py` (cache) vs `path_utils` (prepare + sidecars + writability)

### Lessons Learned
- `MelColumnLayout adj=False` shrinks row width, not height — use `MelHSingleStretchLayout` for full-width centered status (see `Feature_CgmToolUI.md`)
- Print Log should log buffered `query_connection` data, not re-query on every click
- Session cache module must **not** reload on cgmP4 open — use `cgmGEN._reloadMod(perforce_session)` only for dev flush
- Perforce batch submit/revert maps cleanly to changelist sections with animFilter-style checkbox rows
- Scene browser scroll lists: **`iconTextScrollList` display must use Builder `append` + per-row `itc`** — not raw `append=` + `clear()` that wipes `_ml_rows` before populate (see `Feature_CgmToolUI.md` Scene browser section)

### Future Considerations
- Scene browser list row icons — **not supported** on Maya `iconTextScrollList`; use `+ name/` alias prefix + tint (see `Feature_CgmToolUI.md`)
- Scene browser selection — **`itc` ≠ `hlc`**: saturated unselected text + dimmed `hlc` on select (`itc × 0.7`); Maya inverts selection row (see `Feature_CgmToolUI.md`, Builder `setHLC`)
- Scene browser P4 file rows — batch `query_files_status`; five status tints + alias suffix when versionControl + connected (see entries (i)–(j), `Feature_CgmToolUI.md`)
- Unknown / not-on-depot uses **yellow** not gray — off-white synced files too similar to gray
- Scene Save Maya here / Save Version
- MRS batch `_batch.py` writability (`batch_utils.py`)
- UI toggle for export P4 opt-in
- Artist Google Doc update when validated studio-wide
- ~~Artist prefs UI for P4 user/client~~ — cgmP4 tool shipped

---

*Last Updated: August 13, 2026 (Scene browser P4 suffix + locked; export wire next)*  
*Branch Status: Active — export prepare next*
