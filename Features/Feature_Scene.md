# Feature: Scene (mrsScene browser)

## 🎯 Status & Overview
- **Status**: Shipped (living contract — browser navigation and file actions keep evolving on `Branch_Fall26`)
- **Last Updated**: 2026-11-12
- **Owners**: Josh Burton (dev / TA); artists use it daily for open / save / export
- **Purpose**: `mrsScene` (`cgm/core/mrs/Scene.py`, `ui` class) is the project content browser: pick a category, asset, subtype, set, variation and version file from the project content tree; open / reference / import / replace / save versions; send to build, queue and export. This doc is the contract for **how the columns map to folders on disk** and **how file-row actions write files** (including Perforce). Export internals live in [`Feature_SceneExportFlow.md`](Feature_SceneExportFlow.md); list widget styling lives in [`Feature_CgmToolUI.md`](Feature_CgmToolUI.md).

## 📋 Scope
- **In Scope**:
  - Column navigation (category → asset → subtype → sets → variation → version) and the filesystem rules that drive it
  - Subtype resolution, including the `<asset root>` entry for mixed asset folders
  - File-row / directory RMB actions (Open, Reference, Import, Replace, Save Version, Save Maya here, Send To Build / Project / Queue, Delete)
  - Where Scene calls the shared write-prepare / P4 helpers
- **Out of Scope**:
  - FBX export modes, bake/prep, tdSets, rig naming → [`Feature_SceneExportFlow.md`](Feature_SceneExportFlow.md)
  - Scroll-list display (dir/file tint, `+ name/` alias, P4 row colors) → [`Feature_CgmToolUI.md`](Feature_CgmToolUI.md) § Scene
  - P4 API, preflight, `prepare_*` semantics → [`Feature_PerforceIntegration.md`](Feature_PerforceIntegration.md)
  - Project `.cfg` schema, `dirMask`, asset-type templates → [`Feature_ProjectManager.md`](Feature_ProjectManager.md)

## 🧩 Architecture

### Core concepts

| Column / control | Widget | Disk path property |
|------------------|--------|--------------------|
| Category button | `categoryBtn` | `path_dir_category` = `content/<category>` |
| Asset list | `assetList` | `path_asset` = `.../<asset>` |
| Type (subtype) button + menu | `subTypeBtn` / `subTypeMenu` | `path_subType` via `_resolve_subType_container_path` |
| Panel 2 — Sets | `subTypeSearchList` | `path_set` (folder row) **or** version files when `not hasSub` |
| Variation | `variationList` | `path_variationDirectory` |
| Version | `versionList` | `path_versionDirectory` / `versionFile` |

**Runtime vs saved**: column contents are display strings over real paths; selection resolves through the path properties above, not by parsing alias text (`+ rig/`). Last selection persists via optionVars (`SaveCurrentSelection` / `LoadPreviousSelection`, e.g. `var_lastSubtype`, `var_lastVersion`).

### Subtype resolution

- **Base subtypes** come from the project asset type: `mDat.assetType_get(category)['content']` → `l_subTypesBase` (`SetCategory`).
- **On asset select** (`uiFunc_assetList_select`) the subtype list is rebuilt from the asset folder's **child directories**: names matching a base subtype (plural / singular / case variants via `_resolveSubTypeLabelFromPathToken`) first, then any other folders under an "Extras.." divider.
- **Folder name ↔ label**: `_resolve_subType_container_path(assetPath, subType)` picks the existing folder from `PU.subtype_dir_candidates` (plural preferred when `usePluralSubdirs`); warns and offers `_fix_subType_directory_discrepancy` when both plural and legacy folders exist.
- **File token**: `_subtype_file_token()` → `PU.subtype_file_token` (singular, lowercase) for basenames such as `bob_rig_01.mb`.
- **Config index alignment**: `hasVariant` reads `assetType_get(...)['content'][subTypeIndex]` — extras and `<asset root>` are appended **after** base subtypes so these indices stay valid for config rows.

### `<asset root>` (mixed asset folder)

Because every asset subfolder becomes a subtype, loose `.ma` / `.mb` directly under `content/<category>/<asset>/` had no column. When the asset folder has **subfolders and loose Maya files**, the Type menu adds a last entry **`<asset root>`** (`_SUBTYPE_ASSET_ROOT`, "Asset level.." divider):

| Behavior | Rule |
|----------|------|
| Path | `_resolve_subType_container_path` → `path_asset` |
| Layout | `hasSub` forced `False` → files list in panel 2 (type-only layout), no version column |
| Filename filter | `_version_list_include_filename` does not require an `{asset}_{subtype}_` prefix |
| Names | `_subtype_file_token()` → `''`: Save Version `{asset}_01.mb`, SubType Ref `{asset}Ref.mb`, `exportFileName` `{asset}.fbx` |
| Export dir | `_exportSubTypeDirName` → `''` (batch export lands in the asset export folder) |
| Guards | Not renameable (`rename_below('subtype')`); skipped by Create Asset subtype `mkdir`; skipped by plural/legacy dir fix-up |

Asset folders with **only** files keep the no-subtype layout (`not self.subTypes` → version list under `path_asset`).

### Navigation depth (filesystem walk)

Column count follows **immediate children** of the current browse path (after `dirMask`, ignoring `_` / `.` names), not project `hasSub` / `hasVariant` flags — except explicit **`hasVariant: false`** on project content, which disables the variation tier.

| On-disk layout under selected type (`path_subType`) | Visible columns (after asset) |
|---------------------------------------------------|-------------------------------|
| Only `.ma`/`.mb` (no child folders) | **Type** + **panel 2** (files). Version column off — files are not duplicated into column 4. |
| Child folders (with or without loose files at type root) | **Type** + **Sets** (dirs and files in one list). **Version** when a folder row is selected. Mixed type root: no auto-select. |
| Set folder with only scenes | **Sets** + **Version** (no variation). |
| Set folder with child folders (with or without loose scenes) | **Sets** + **Variation** (folders, plus files when mixed) + **Version**. |

**Properties** (evaluated per current selection):

- **`hasSub`** — `path_subType` has filtered child directories (`_dir_children_dirs`). Always `False` for `<asset root>`. `False` → `LoadVersionList` fills **panel 2**.
- **`hasVariant`** — selected set (`path_set`) has filtered child directories; `False` at the subtype root.
- **`_version_column_should_show`** — hidden when the selected sets/variation row is a file (`b_subFile` / `b_varFile`) or layout is type-only.
- **`_dir_is_mixed(path)`** — both child dirs and Maya files; mixed levels skip auto-selection so the user picks a dir or a file.

**Navigation API** (call after disk changes / saves): `_republish_navigation_lists(from_level, focus_path)`, `_navigate_to_scene_file`, `_navigate_to_scene_parts`, `_navigate_to_scene_entry` (queue / batch dicts), `_navigation_tokens_from_focus_path`.

## ⚙️ Implementation Details

### Files & Responsibilities

| File | Responsibility |
|------|----------------|
| [`cgm/core/mrs/Scene.py`](../../cgmToolsPy3/cgm/core/mrs/Scene.py) | `ui` window: columns, path properties, RMB menus, save/replace/version, P4 menu actions, export UI → `ExportScene` |
| [`cgm/core/mrs/lib/scene_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/scene_utils.py) | List row building / sort (`scene_list_rows_from_entries`, `scene_list_sort_rows`), tint constants, annotations |
| [`cgm/core/mrs/lib/scene_export_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/scene_export_utils.py) | Export path / name resolution (see SceneExportFlow) |
| [`cgm/core/tools/lib/project_utils.py`](../../cgmToolsPy3/cgm/core/tools/lib/project_utils.py) | `subtype_file_token`, `subtype_dir_candidates`, `project_uses_perforce` |
| [`cgm/core/lib/path_utils.py`](../../cgmToolsPy3/cgm/core/lib/path_utils.py) | `prepare_maya_scene_for_save`, `prepare_meta_files_for_write`, `PathWritePrepareError` |
| [`cgm/core/mrs/lib/batch_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/batch_utils.py) | Batch files / build output path helpers (`resolve_build_output_path`, `is_mrs_build_output_scene`) |

### File-row actions

RMB menus are built per column (`Sets` / `Variant` / `Version` sections): **Selected** (Rename, Reference, Import, Replace, Export Here, Send To Project, Send To Build, Send Last To Queue / To Queue as, Create SubTypeRef), **Directory** (Explorer, Open Maya here, Save Maya here, Refresh, Delete), and **Perforce** (Get, Checkout, Add, Revert, Submit, Shelve; Get Latest Revision on dirs).

| Action | Method | Write path |
|--------|--------|-----------|
| Save Version | `SaveVersion` | `prepare_maya_scene_for_save` → rename + save → `_republish_navigation_lists` |
| Save Maya here / Save As | `uiPath_mayaSaveTo*` | `prepare_maya_scene_for_save` → rename + save → republish |
| **Replace** | `file_replace` | Overwrite confirm → `prepare_maya_scene_for_save` (P4 checkout prompt) → rename + save → republish |
| Send To Build | `SendToBuild` | Prepares the `*_BUILD` output path first (`confirm_p4 = not autoCheckoutExportFiles`), then opens MRS Build |
| Meta sidecars | `saveMetaData`, `refreshMetaData`, `updateMetaThumbnail` | `prepare_meta_files_for_write` (`.dat` + `.bmp`) |
| Delete | `uiFunc_deleteSelectedInList` | Local delete (multi-select confirm, or `uiPrompt_removeDir`) → deferred list reload. No P4 delete. |

**Rule**: any Scene action that writes a Maya scene calls **`PATHUTIL.prepare_maya_scene_for_save(path, mDat=self.mDat)` before `mc.file(rename=…)`**, and aborts on `PathWritePrepareError`. That is what gives the "check out?" prompt on P4 projects and the writability check everywhere else. Do not call `mc.file(s=True)` on a known path without it.

### Perforce hooks

- P4 menu items appear only when `_scene_p4_menu_active()` (project `versionControl` = perforce) and enable when `_scene_p4_connected()`.
- Single and multi-file Checkout / Add / Revert / Get loop with `_scene_p4_multi_file_progress_*` (progress + cancel).
- Submit / Shelve classify paths first (`_scene_p4_classify_open_paths`) and add/checkout what's needed before the changelist prompt.
- After P4 writes: `_scene_p4_after_write` / `_scene_p4_after_sync_directory` reload the affected lists so row colors update.
- Export preflight and the **Auto Check Out Export Files** option (`cgmVar_sceneUI_auto_checkout_export_files`) are documented in [`Feature_PerforceIntegration.md`](Feature_PerforceIntegration.md) and [`Feature_SceneExportFlow.md`](Feature_SceneExportFlow.md).

### Lifecycle

- `SetCategory` → reload asset list, reset subtypes from config.
- `uiFunc_assetList_select` → rebuild subtypes from disk (+ `<asset root>`), restore previous selection, `buildAssetForm` (column visibility).
- `SetSubType` → `LoadSubTypeList` → `LoadVariationList` / `LoadVersionList` cascade.
- Category / subtype menu callbacks are **deferred** (`_defer_ui`) — direct calls from the popup crash Maya. Do not rebuild a file-list popup from its own `pmc`.

## 🔧 Configuration Guide

| Source | Field | Effect |
|--------|-------|--------|
| Project `assetDat` | category `content[].n` | Base subtypes (menu order) |
| Project `assetDat` | `content[].hasVariant: false` | Disables the variation tier for that subtype |
| Project | `usePluralSubdirs` | Preferred subtype folder form (`Rigs` vs `Rig`) |
| Project | `dirMask` | Folders hidden from every column |
| Project | `versionControl` | P4 menus, checkout prompts, row colors |
| Scene options | Show all files | Lists every file, not just `.ma`/`.mb` |
| Scene options | Auto Check Out Export Files | Silent p4 edit/add for export outputs |

## ✅ Testing & Validation

Manual, in Maya (Scene is not runnable outside Maya):

- [ ] Asset with only subtype folders — subtypes listed, no `<asset root>`
- [ ] Asset with subfolders **and** loose `.ma` — `<asset root>` last in the Type menu; selecting it lists the loose files in panel 2; Open / Reference / Replace work; switching back to a real subtype restores its sets
- [ ] Save Version under `<asset root>` → `{asset}_01.mb` (no subtype token) in the asset folder
- [ ] Rename on `<asset root>` warns and does nothing
- [ ] Type-only files layout, mixed type root, set with variations — columns per the navigation table
- [ ] P4 project, file not checked out: Replace / Save Version / Save Maya here → checkout prompt; cancel aborts without writing
- [ ] Non-P4 project, read-only file → writability prompt, no P4 calls

**Verified in Maya**: Replace File checkout prompt (2026-11-12). `<asset root>` — **not yet verified**.

## 🧱 Dependencies & Integration
- `ExportScene` / batch export consume `subType`, `subSet`, `variation` from this UI — see SceneExportFlow.
- MRS Build (`Builder.ui_toStandAlone`) via Send To Build.
- Shots (`Shots.py`) via the shot list / Copy ShotList on meta.

## 📚 Related Documentation
- **[Feature_SceneExportFlow.md](Feature_SceneExportFlow.md)** – export modes, preflight, naming
- **[Feature_CgmToolUI.md](Feature_CgmToolUI.md)** – Scene list widgets, tint, P4 row colors
- **[Feature_PerforceIntegration.md](Feature_PerforceIntegration.md)** – `prepare_*` helpers, checkout policy
- **[Feature_ProjectManager.md](Feature_ProjectManager.md)** – project schema, `dirMask`, asset types
- **[Branch_Fall26.md](../Branches/Branch_Fall26.md)** – timeline (Replace File checkout, `<asset root>`)

## 🚀 Future Work / Ideas
- Interactive **Export** from a scene opened at asset root fails: `RunExportCommand` needs at least 3 path tokens (category / asset / subtype) from `uiFunc_getOpenFilePathTokens`.
- `ExportScene` builds `exportAnimPath` from `subType` when none is passed; `<asset root>` callers rely on `_exportSubTypeDirName` returning `''` before that point.
- Delete is local only — no `p4 delete` for depot files.

## 📝 Revision History
| Date | Author | Summary |
|------|--------|---------|
| 2026-11-12 | Josh Burton | Initial contract: navigation columns (moved from Feature_CgmToolUI), subtype resolution + `<asset root>`, file-row write rule, P4 hooks |
