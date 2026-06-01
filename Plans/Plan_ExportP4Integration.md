# Plan: Export Perforce (P4) Integration

## Purpose

Plan automatic Perforce checkout (`p4 edit`) and add (`p4 add`) for Scene FBX export targets so batch and standalone exports succeed against synced depot files without manual checkout. This doc is the **planning source of truth** until implementation ships; then promote or mirror to `Features/Feature_ExportP4Integration.md` per [`Guides/NewFeature_Guide.md`](../Guides/NewFeature_Guide.md).

## 🎯 Status & Overview

| Field | Value |
|-------|-------|
| **Status** | Planning |
| **Last Updated** | May 28, 2026 (`cgm.core.lib.perforce`; no zooPy) |
| **Owners** | TBD |
| **Branch** | [`Branch_UnrealWorkflow.md`](../Branches/Branch_UnrealWorkflow.md) |
| **Trigger** | Read-only synced FBX in depot caused opaque FBX I/O failures; May 2026 pass added pre-check + batch reporting only |

**Summary:** Export writability checks live in `path_utils` today (no P4 API). New work adds **`cgm.core.lib.perforce`** — our own P4 wrapper under **`cgm/core/lib/`** — wired into export prepare. **Do not import or modify** vendored zooPy (`cgm.lib.zoo.zooPy.perforce`); zooPy and Red9 docs are **reference only** when reimplementing patterns.

---

## 📋 Scope

### In scope (v1 target)

- **FBX export output paths** from Scene `ExportScene` / `BatchExport` (anim, cutscene, rig, static as configured)
- **Pre-export prepare:** attempt checkout or add so `check_export_output_writable()` passes
- **Existing sidecars:** continue best-effort `.bak` cleanup; extend if P4 state blocks deletion
- **Batch reporting:** extend non-writable summary with P4 action attempted / reason (edit failed, not under client, offline)
- **Graceful fallback:** if P4 unavailable or path outside workspace, behave like today (fail on read-only with clear message)

### Out of scope (v1)

- Maya `.ma` / `.mb` save-here / Save Version (separate workflow; may share helpers later)
- Texture / image export paths
- Submitting changelists (`p4 submit`) — export opens files only
- Revert-on-failed-export rollback (optional v2)
- Modifying **`cgm.lib.zoo.zooPy.perforce`** — third-party vendored code; not ours
- Modifying **`Red9/`** modules — requires **explicit user clearance** (including bug fixes); fix in cgm.core first
- Full depot policy (branch specs, file types, `p4 typemap`) — studio ops owns

### Non-goals

- Require P4 for all cgmTools sessions
- Silent overwrite of another user's open-for-edit file without error

---

## 🧩 Current state (baseline)

### What exists today

| Component | Behavior |
|-----------|----------|
| `path_utils.check_export_output_writable()` | mkdir parent, remove editable `.bak` sidecars, `os.access(W_OK)` fail-fast |
| `path_utils.ExportOutputNotWritableError` | Message suggests manual `p4 edit` |
| `path_utils` session list | `record/get/clear_non_writable_export_paths()` for batch summary |
| `cgm_General.fbx_export_selection()` | Calls writability check before `FBXExport` |
| `Scene.BatchExport` | Clears path list at start; logs non-writable rollup at end |
| `cgm.core.lib.perforce` | **Does not exist yet** — planned new module under `cgm/core/lib/` |
| `cgm.lib.zoo.zooPy.perforce` | Vendored zooPy; **reference only** — never import from cgm core export path |

### Failure modes observed (Unreal workflow branch)

1. Synced FBX on disk is read-only → FBX plugin I/O error (fixed UX: fail before export with path listed)
2. Stale `.fbx.bak` from prior failed export → blocks overwrite when deletable locally
3. Nested namespace / bake set issues — **separate** from P4; already fixed in branch

### Hook point (proposed)

```
ExportScene / fbx_export_selection
  → path_utils.prepare_export_output_for_write()   ← NEW
       → cgm.core.lib.perforce.edit_or_add(diskPath)   ← NEW module
       → path_utils.cleanup_fbx_export_sidecars()
       → path_utils.check_export_output_writable()  (os.access)
  → FBXExport MEL
```

**Module split:** P4 subprocess logic in **`cgm/core/lib/perforce.py`**; export-specific sidecars + writability + batch path list stay in **`path_utils`**.

---

## 🧩 Architecture

### Decision: `cgm.core.lib.perforce` (ours)

New first-party module at **`cgm/core/lib/perforce.py`** (`import cgm.core.lib.perforce as P4UTIL` or project alias). Subprocess-based `p4` CLI wrapper scoped to what export needs — no zooPy `Path` monkey-patching.

**Hard rule:** cgm core **must not** `import` from `cgm.lib.zoo.zooPy.perforce`. When implementing, read zooPy / Red9 docs only to redo behavior in our module.

### Planned API (v1 sketch)

| Function | Responsibility |
|----------|----------------|
| `is_available(force=False)` | `p4 info` succeeds; cache per session |
| `connection_info()` | client name, user, client root (from `p4 info`) |
| `is_under_client(disk_path)` | `p4 fstat` — path in workspace view |
| `file_status(disk_path)` | Redo Red9-style strings: `checkout_other`, `on_sync`, `not_on_p4`, etc. |
| `edit(disk_path, changelist=None)` | `p4 edit`; return success + stderr |
| `add(disk_path, file_type=None)` | `p4 add` (`binary` for `.fbx` if required) |
| `edit_or_add(disk_path, **kw)` | edit if managed exists, else add — export main entry |
| `P4PrepareError` | Structured failure (path, action, p4_message) for batch summary |

Optional later: `create_changelist(description)`, `revert(disk_path)`, sync-before-edit.

### Reference material (read-only)

| Source | Use |
|--------|-----|
| zooPy [`perforce.py`](../../cgmToolsPy3/cgm/lib/zoo/zooPy/perforce.py) | Reference for `p4run`, `fstat`, `editoradd`, `isUnderClient`, binary add — **do not call** |
| Red9 [`Red9_Pro_perforce.html`](../../cgmToolsPy3/Red9/docs/html/red9pro_templates/Red9_Pro_perforce.html) | Reference for `push_file`, `status()` strings, exception handling — **do not depend at runtime** |

### Path authority

Export disk paths come from **Scene + cgm Project**. **`cgm.core.lib.perforce`** receives **absolute paths only**.

### Subprocess cwd

Implement inside **`cgm.core.lib.perforce`**, not zooPy `getDefaultWorkingDir()`.

### Phase 0 audit (before coding)

- [ ] List P4 error strings export must surface (locked by other user, not in client view, etc.)
- [ ] Confirm depot rule for new `.fbx` (`p4 add -t binary` vs default)
- [ ] Skim zooPy `P4File.editoradd` / Red9 `push_file` for edge cases to reimplement in cgm module

---

## ⚙️ Implementation plan (phased)

### Phase 0 — Decisions (this doc)

- [ ] Answer open questions below
- [ ] Confirm cgm Project export roots align with P4 client mappings (anim FBX depot paths under `path_export` / Scene builders)
- [ ] Confirm opt-in mechanism (project flag vs env vs always-on in batch)

### Phase 1 — `cgm.core.lib.perforce` + prepare helper

- [ ] **NEW:** `cgm/core/lib/perforce.py` — subprocess `p4` wrapper (info, fstat, edit, add, edit_or_add, file_status)
- [ ] **NEW:** `path_utils.prepare_export_output_for_write(finalPath, *, use_p4=True)` — calls `P4.edit_or_add`, then sidecar cleanup + writability check
- [ ] Subprocess cwd from cgm `pathProject` when configured
- [ ] Unit-testable: mock subprocess; paths under/over client boundary

### Phase 2 — Scene / batch integration

- [ ] Wire from `fbx_export_selection()` before FBX MEL
- [ ] Extend `ExportOutputNotWritableError` or new `ExportP4PrepareError` with `p4_attempted`, `p4_message`
- [ ] Batch summary: group "P4 edit failed" vs "not writable (no P4)"

### Phase 3 — Edge cases

- [ ] New file in existing depot directory → `p4 add` (binary type for `.fbx` if required)
- [ ] Temp-then-replace: if edit fails on locked file, export to `%TEMP%` then copy? (**needs decision**)
- [ ] Sidecar `.bak` under P4: revert/delete policy

### Phase 4 — Docs & validation

- [ ] Update `Branch_UnrealWorkflow.md` timeline
- [ ] Artist-facing note in Google Doc Export section (manual checkout no longer required when P4 enabled)
- [ ] Promote to `Features/Feature_ExportP4Integration.md` when shipped

---

## 🔧 Configuration (draft)

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| `useP4OnExport` | project JSON / Scene export option | `False` | Opt-in until validated studio-wide |
| `CGM_EXPORT_P4` | env `1`/`true`/`yes` | unset | Override for batch farm |
| P4 session cache | `cgm.core.lib.perforce` | — | `is_available()` caches `p4 info` per export session |
| P4 offline | — | fallback | Skip P4; `path_utils` writability check only |

**Open:** Should batch mayapy **always** attempt P4 when `p4 info` works, regardless of UI checkbox?

---

## ✅ Testing & validation

### Manual checklist

- [ ] Export over existing synced FBX (read-only) → auto edit → export succeeds
- [ ] Export new FBX under depot path → auto add → file visible in `p4 opened`
- [ ] Export to local non-P4 folder → no P4 calls; unchanged behavior
- [ ] P4 not installed / `p4 info` fails → clear log; fail only if still read-only
- [ ] Batch multi-shot: each path edited; summary shows no non-writable paths
- [ ] Another user's lock → fail with actionable message (not FBX I/O)
- [ ] `.bak` sidecar present + read-only target → prepare clears/adds/edits as expected

### Regression

- [ ] Writable local export without P4 unchanged
- [ ] `logExportSummary` / batch rollup still single summary
- [ ] mayapy batch: no return of FBX MEL spam at import (keep `ensure_fbx_plugin` order)

---

## 🧱 Dependencies & integration

| System | Relationship |
|--------|----------------|
| [`path_utils.py`](../../cgmToolsPy3/cgm/core/lib/path_utils.py) | Sidecars, writability, batch path list, `prepare_export_output_for_write` |
| **`cgm/core/lib/perforce.py`** (new) | **Our** P4 CLI wrapper — only module that spawns `p4` for export |
| [`cgm_General.fbx_export_selection`](../../cgmToolsPy3/cgm/core/cgm_General.py) | Caller |
| [`Scene.py` ExportScene / BatchExport](../../cgmToolsPy3/cgm/core/mrs/Scene.py) | UX + batch summaries |
| [`Project.py`](../../cgmToolsPy3/cgm/core/tools/Project.py) / [`project_utils.py`](../../cgmToolsPy3/cgm/core/tools/lib/project_utils.py) | **Path authority** — export roots |
| Perforce server / workspace | Studio infrastructure |
| zooPy / Red9 P4 code | **Reference only** — not imported |

---

## ❓ Open questions (need answers before Phase 1)

Record decisions in the **Decisions log** as they are resolved.

1. **Opt-in vs default-on:** Should P4 run automatically whenever `p4 info` succeeds and the path is under the client, or only when a project flag / env var is set?
2. ~~**Red9 / zooPy runtime**~~ — **Resolved:** own **`cgm.core.lib.perforce`**; zooPy/Red9 reference only.
3. **`getDefaultWorkingDir`:** Does the studio use `P4CONFIG` in repo roots? Should cgm set cwd to **cgm project root** (`pathProject`) before `p4` subprocesses?
4. **New files:** Always `p4 add` on first export to a depot path, or only when parent dir is mapped?
5. **FBX file type:** Does depot require `p4 add -t binary` (or `binary+F`) for `.fbx`?
6. **Temp-then-replace:** If `p4 edit` fails (exclusive lock), should we export to temp and instruct manual reconcile, or hard-fail?
7. **Changelist:** Default changelist only, or auto-create described changelist per batch run?
8. **Scope creep:** Same helper for **Save Maya here** / version saves in v1 or strictly FBX?
9. **Farm batch:** Mayapy on render farm — is P4 available with same client as artist workstations?
10. **Revert policy:** On export failure after edit, leave open for edit or `p4 revert`?

---

## 📋 Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-28 | Pre-check without P4 shipped first | Avoid opaque FBX I/O; no P4 API until plan approved |
| 2026-05-28 | **cgm Project pathing only — not Red9 pathing** | Export paths from Scene + cgm Project |
| 2026-05-28 | **`cgm.core.lib.perforce` — no zooPy** | New module under `cgm/core/lib/`; subprocess `p4` CLI; never import or edit zooPy |

---

## 🚀 Future work (post-v1)

- Shared prepare helper for Maya save paths
- `p4 reconcile` for orphaned `.bak` / `.fbx` pairs
- UI: export option "Checkout in P4" with tooltip when disabled
- Integration test with mock `p4` in CI (if feasible)

---

## 📚 Related documentation

- **[Branch_UnrealWorkflow.md](../Branches/Branch_UnrealWorkflow.md)** — export hardening timeline; deferred P4 note
- **[NewFeature_Guide.md](../Guides/NewFeature_Guide.md)** — template for post-ship feature doc
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** — branch timeline when implementation starts
- **[PY2_BACKPORT_PLAN.md](./PY2_BACKPORT_PLAN.md)** — if P4 helpers must port to py2 (unlikely for export)

---

## 📝 Revision history

| Date | Author | Summary |
|------|----------|-----------|
| 2026-05-28 | — | Initial plan from UnrealWorkflow export branch context |
| 2026-05-28 | — | Decision: cgm Project roots only; Red9 pathing rejected |
| 2026-05-28 | — | Decision: `cgm.core.lib.perforce`; aligns with `cgm-module-placement` rule |
