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

5. **Export pipeline design contract**: [`Features/Feature_SceneExportFlow.md`](Features/Feature_SceneExportFlow.md) — canonical dev/TA reference for Scene export behavior (modes, tdSets, prep invariants). Update when changing `ExportScene` or `bakeAndPrep`.

6. **cgmSimChain design contract**: [`Features/Feature_SimChain.md`](Features/Feature_SimChain.md) — hair vs cloth attach chains, nCloth preset layering, connect/bake invariants, Query Settings. Update when changing `cgmDynFK`, `dynFKTool`, or `nCloth_utils`.

7. **MetaHuman facial solve design contract**: [`Features/Feature_Metahuman.md`](Features/Feature_Metahuman.md) — joint matching, bridge mapping, `transfer_rig` / `constrain_rig`, rest-pose invariants. Timeline on [`Branches/Branch_UnrealWorkflow.md`](Branches/Branch_UnrealWorkflow.md). Primary code in Perforce `ProjectScripts/MetahumanFacial.py` (factor core to cgm when API stabilizes).

8. **Mocap align snap / bake design contract**: [`Features/Feature_MocapAlignSnap.md`](Features/Feature_MocapAlignSnap.md) — **implemented and Maya-verified** local-TR locator align, single-frame snap, and dual-path timeline bake in `mocapBakeTools` (`mocap_align_utils`). Snap/bake must rebuild locators via `doLoc` on target (rotateAxis invariant). Reload align lib on tool open (`tool_calls.mocapBakeTool`). Update when changing offset capture, CCL schema, or bake loop. Timeline: [`Branches/Branch_UnrealWorkflow.md`](Branches/Branch_UnrealWorkflow.md).

9. **MRS module wiring design contract**: [`Features/Feature_MRSWiring.md`](Features/Feature_MRSWiring.md) — block/module/puppet message graphs, build sync, control rewire, attach points. Update when changing `puppet_utils`, `module_utils`, or `moduleTarget_wire_from_blockParent`.

10. **cgm tool UI design contract**: [`Features/Feature_CgmToolUI.md`](Features/Feature_CgmToolUI.md) — parallel list data vs scroll display, selection by index, CCL/preset save rules, scroll-list pitfalls. Living doc — extend when establishing list/UI patterns in tools. See also [`Feature_MocapAlignSnap.md`](Feature_MocapAlignSnap.md) for link-list + CCL example.

11. **Perforce integration design contract**: [`Features/Feature_PerforceIntegration.md`](Features/Feature_PerforceIntegration.md) — optional P4 layer; **`path_utils.prepare_*`** for saves (including **`prepare_meta_files_for_write`** for Scene meta sidecars); **`preflight_export_output_paths`** before FBX bake when VC=perforce. Timeline on [`Branches/Branch_p4.md`](Branches/Branch_p4.md).

12. **cgm Project Manager design contract**: [`Features/Feature_ProjectManager.md`](Features/Feature_ProjectManager.md) — project `.cfg` schema, path authority, **`dirMask`** (Content/Export scroll lists, Scene, P4 cache), asset structure, Project-tool P4 row. Update when changing `Project.py`, `project_utils`, or shared mask/walk behavior.

## Python 2 backport (exceptional)

1. Use **[`cgmTools-py2-backport.code-workspace`](cgmTools-py2-backport.code-workspace)** so the legacy **py2** tree is a workspace folder, **or** add your py2 checkout via **Add Folder to Workspace…**.
2. Edit the **py2 folder path** in that workspace file if your checkout is not `../../repos/cgmTools` relative to this repo.
3. Follow **[`Plans/PY2_BACKPORT_PLAN.md`](Plans/PY2_BACKPORT_PLAN.md)**.
4. When finished, switch back to **`cgmTools.code-workspace`** so py2 is not indexed during normal py3 work.

## Repo layout

| Path | Purpose |
|------|---------|
| `cgmToolsDev/` | Bridge: rules, workspaces, `Plans/`, `Features/`, `guides/` |
| `cgmToolsPy3/` (separate clone) | Ship-only Maya tools (Python 3) |
