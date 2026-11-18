---
description: Audit cgmToolsPy3 changes against the cgm rule files in .claude/rules/ (meta/strings, reload, placement, progress)
argument-hint: "[file or area, e.g. cgm/core/tools/dynFKTool.py — omit for uncommitted changes]"
---

Review cgm Maya code against the project's rule files. This is a **rules-compliance** pass, not a general
bug hunt.

**Read first** (in full, before auditing):

- [`.claude/rules/maya-cmds.md`](../rules/maya-cmds.md)
- [`.claude/rules/meta-runtime.md`](../rules/meta-runtime.md)
- [`.claude/rules/reuse-and-placement.md`](../rules/reuse-and-placement.md)
- [`.claude/rules/reload.md`](../rules/reload.md)
- [`.claude/rules/debugging.md`](../rules/debugging.md)
- [`.claude/rules/clear-code.md`](../rules/clear-code.md)
- [`.claude/rules/ui-progress.md`](../rules/ui-progress.md)
- [`.claude/rules/perforce.md`](../rules/perforce.md)

**Target:** $1 — if empty, review uncommitted changes in `cgmToolsPy3` (`git diff` / `git status`). If
`git` is "not recognized", retry with `& "C:\Program Files\Git\cmd\git.exe"`; if you still cannot get a
diff, ask the user which files to review rather than guessing.

Check the changes against each rule file and report **only actual violations**, with `file:line`, grouped
by rule file. Cover at least these:

- **`maya-cmds.md`** — `import maya.cmds as mc`; no `as cmds`, no bare `cmds.`. No `cgmMeta` / Red9
  `MetaClass` instance passed into any `mc.*` call, including inside lists, tuples, and plug format strings.
  Flag `VALID.mNodeString` results used without an `isinstance(..., str)` check.
- **`meta-runtime.md`** — runtime carried as `cgmMeta` instances, not bare node strings, through handlers,
  build/create, and multi-step pipelines. Scroll-list selection resolved by index into a parallel meta list,
  not by parsing display strings. `m*` / `ml_*` / `md_*` naming only on meta. `mc.listRelatives` / `mc.parent`
  used for parent/child intent that meta (`p_parent`, `getParent`, `msgList_get`) already models is a
  violation (allowed at the `mc.*` edge and in documented `lib/` lookups). New instance methods on a
  registered `mClass` subclass, or calls to meta methods that do not exist in `cgm/core/cgm_Meta.py`, need
  explicit user approval.
- **`reload.md`** — any `importlib.reload`, `importlib.import_module`, bare `reload()`, `imp.reload`,
  `__import__(__name__)`, or `sys.modules[...]` trick, in code, comments, or docstrings. Any reload or meta
  rebind inside a one-shot action callback (Create, bake, export). Any partial Red9 → `cgm_Meta` stack inside
  a tool's `reload_dependencies()`. Missing per-module log lines in a multi-module reload.
- **`reuse-and-placement.md`** — new general utilities outside `cgm/core/lib/`; edits to `cgm/lib/zoo/` or
  `Red9/`; shared lookup tables defined module-local instead of in `cgm/core/lib/shared_data.py`; a new
  `def` wrapping `mc.ls` / `listConnections` / `listAttr` / `keyframe` / name-string hacks that
  [`Features/Feature_CoreLibLookups.md`](../../Features/Feature_CoreLibLookups.md) already covers.
- **`ui-progress.md`** — a bake, export, batch rebuild, heavy scene walk, or many-constraint loop reachable
  from a button or menu with no visible progress feedback.
- **`clear-code.md`** and **`debugging.md`** — flag only clear violations of what those files state (for
  example, obscure patterns with no stated reason, or a pasted-log diagnosis that skips the stale-session
  check).
- **`perforce.md`** — any workaround for a read-only or not-checked-out file (shell one-liners, retries,
  edit-a-copy) instead of stopping for the user.

Then check whether the change touches a system with a design contract listed in
[`AGENTS.md`](../../AGENTS.md) (Scene export, DynSim, MRS wiring, AnimData, Project Manager, Bezier IK,
Mocap align, Perforce, MetaHuman, mesh creation, BlockCreate helpers). If so, say which `Feature_*.md`
needs updating in the same pass.

**Output:** grouped by rule file, violations only. If a section is clean, say "clean" in one line — do
not pad. End with the `Feature_*.md` update list, or "no contract touched".
