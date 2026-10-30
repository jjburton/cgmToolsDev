---
description: Audit cgmToolsPy3 changes against the cgm iron rules (meta/strings, reload, placement, progress)
argument-hint: "[file or area, e.g. cgm/core/tools/dynFKTool.py — omit for uncommitted changes]"
---

Review cgm Maya code against the project's iron rules in [`CLAUDE.md`](../../CLAUDE.md). This is a
**rules-compliance** pass, not a general bug hunt.

**Target:** $1 — if empty, review uncommitted changes in `cgmToolsPy3` (`git diff` / `git status`). If
`git` is "not recognized", retry with `& "C:\Program Files\Git\cmd\git.exe"`; if you still cannot get a
diff, ask the user which files to review rather than guessing.

Check each of these and report **only actual violations**, with `file:line`:

1. **`mc` alias** — `import maya.cmds as mc`; no `as cmds`, no bare `cmds.`
2. **Strings at the `mc` edge** — no `cgmMeta` / Red9 `MetaClass` instance passed into any `mc.*` call,
   including inside lists, tuples, and plug format strings. Flag `VALID.mNodeString` results used without
   an `isinstance(..., str)` check.
3. **Runtime meta** — DAG identity carried as bare node strings through handlers, build/create, or
   multi-step pipelines when the node still exists. Scroll-list selection resolved by parsing display
   strings instead of index → parallel meta list.
4. **Naming** — meta instances without `m*` / `ml_*` / `md_*`; those prefixes on things that are not meta.
5. **Parallel hierarchy** — `mc.listRelatives` / `mc.parent` used for parent/child intent that meta
   (`p_parent`, `getParent`, `msgList_get`) already models. Allowed at the `mc.*` edge and in documented
   `lib/` lookups.
6. **Reload** — any `importlib.reload`, `importlib.import_module`, bare `reload()`, `imp.reload`,
   `__import__(__name__)`, or `sys.modules[...]` trick, in code *or* comments *or* docstrings. Any reload
   or meta rebind inside a one-shot action callback (Create, bake, export). Any partial Red9 → `cgm_Meta`
   stack inside a tool's `reload_dependencies()`. Missing per-module log lines in a multi-module reload.
7. **New `mClass` instance methods** — flag any added method on a registered `mClass` subclass, or any call
   to a meta method that does not exist in `cgm/core/cgm_Meta.py`. These need explicit user approval.
8. **Placement** — new general utilities outside `cgm/core/lib/`; edits to `cgm/lib/zoo/` or `Red9/`;
   shared lookup tables defined module-local instead of in `cgm/core/lib/shared_data.py`.
9. **Reinvented lookups** — a new `def` wrapping `mc.ls` / `listConnections` / `listAttr` / `keyframe` /
   name-string hacks that [`Features/Feature_CoreLibLookups.md`](../../Features/Feature_CoreLibLookups.md)
   already covers.
10. **Long-running UI** — a bake, export, batch rebuild, heavy scene walk, or many-constraint loop reachable
    from a button or menu with no visible progress feedback.

Then check whether the change touches a system with a design contract listed in
[`AGENTS.md`](../../AGENTS.md) (Scene export, DynSim, MRS wiring, AnimData, Project Manager, Bezier IK,
Mocap align, Perforce, MetaHuman, mesh creation, BlockCreate helpers). If so, say which `Feature_*.md`
needs updating in the same pass.

**Output:** grouped by rule number, violations only. If a section is clean, say "clean" in one line — do
not pad. End with the `Feature_*.md` update list, or "no contract touched".
