# Agent / developer workflow (cgmTools)

## Keep `cgmToolsPy3` clean

Others sync the **py3** repo into Maya’s `scripts` path. Do **not** commit Cursor config, workspace files, or bridge-only docs **inside `cgmToolsPy3`**. Those belong in **`cgmToolsDev`** only.

## Daily py3 development

1. **Open the multi-root workspace from this repo:**  
   **File → Open Workspace from File…** → [`cgmTools.code-workspace`](cgmTools.code-workspace)  
   That loads **`cgmToolsDev`**, **`cgmToolsPy3`**, and **`cgmDocs`** so Cursor rules under `.cursor/rules/` apply while you edit py3 code.

2. **Do not** rely on opening only the py3 folder if you want bridge rules active—the rules live here, not in py3.

3. **Module placement:** new general utilities → **`cgm/core/lib/`**; meta/MRS/rig logic → **`mrs/`**, **`rig/`**; do not edit **zooPy** or **Red9** without clearance — see **`.cursor/rules/cgm-module-placement.mdc`**.

4. **User-facing Google Doc updates** (artist manual): follow [`Guides/GoogleDoc_Capture_Guide.md`](Guides/GoogleDoc_Capture_Guide.md) and the **`google-doc-capture`** skill (`.cursor/skills/google-doc-capture/`). Branch docs in `Branches/` are the dev source; the guide produces paste-ready section blocks for your Google Doc.

## Python 2 backport (exceptional)

1. Use **[`cgmTools-py2-backport.code-workspace`](cgmTools-py2-backport.code-workspace)** so the legacy **py2** tree is a workspace folder, **or** add your py2 checkout via **Add Folder to Workspace…**.
2. Edit the **py2 folder path** in that workspace file if your checkout is not `../../repos/cgmTools` relative to this repo.
3. Follow **[`Plans/PY2_BACKPORT_PLAN.md`](Plans/PY2_BACKPORT_PLAN.md)**.
4. When finished, switch back to **`cgmTools.code-workspace`** so py2 is not indexed during normal py3 work.

## Repo layout

| Path | Purpose |
|------|---------|
| `cgmToolsDev/` | Bridge: rules, workspaces, `Plans/`, `guides/` |
| `cgmToolsPy3/` (separate clone) | Ship-only Maya tools (Python 3) |
