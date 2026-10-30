# CLAUDE.md — cgmTools

Entry point for Claude Code. Read this with [`AGENTS.md`](AGENTS.md) (repo layout, workspace setup, and
the numbered **design contracts** in `Features/`).

## Two repos, one session

| Repo | Role | Claude may write |
|------|------|------------------|
| `cgmToolsDev` (this one) | Bridge: docs, rules, plans, branch notes | Yes — docs, rules, config |
| `cgmToolsPy3` (additional working dir) | **Ship tree** artists sync into Maya `scripts/` | Yes — **code only** |

**Never** create `.claude/`, `.cursor/`, `CLAUDE.md`, `AGENTS.md`, `*.code-workspace`, or bridge docs
inside `cgmToolsPy3`. Dev-workflow assets live here. (`cgmToolsPy3/.gitignore` enforces this as a backstop.)

**Python 3 only.** Do not read, search, or edit a legacy py2 `cgmTools` checkout unless a PY2 backport
session is explicitly active — see the `py2-backport` skill.

## Iron rules (always on)

These are condensed from `.cursor/rules/*.mdc`, which stay the source of truth. When a rule matters to the
change at hand, **open the named `.mdc`** for the full contract and examples.

### 1. Maya `cmds` — alias and types
- Import `import maya.cmds as mc`. Never `as cmds`, never bare `cmds.`. (`maya-cmds-import`)
- Every `mc.*` argument naming a node, shape, component, or plug must be a **`str`**. Never pass a
  `cgmMeta` / Red9 `MetaClass` instance into `mc.*`. Use `getParent(asMeta=False)` when `mc.*` is next,
  or `.mNode` on meta you already hold. Don't trust `VALID.mNodeString` to have returned a `str` —
  `isinstance(..., str)` first. (`maya-cmds-strings-only`)

### 2. Runtime is meta, not strings
- **UI labels and saved data** (optionVars, `.cgm*Dat`, CCL, presets, JSON) → strings.
- **Runtime** (handlers, build/create, in-memory lists, message graphs, pipelines) → `cgmMeta` instances.
- Convert once at the load/save boundary; `str` only at the `mc.*` edge.
- Resolve scroll-list selection by **index → parallel meta list**, never by parsing display strings.
  (`cgm-runtime-meta-not-strings`, `Features/Feature_CgmToolUI.md`)

### 3. Meta naming and hierarchy
- `m*` = one meta instance · `ml_*` = list of meta · `md_*` = dict with meta values. No prefix ⇒ not meta.
- Meta owns hierarchy: `mChild.p_parent = mParent`, `getParent(asMeta=True)`, `msgList_get` → `ml_*`.
  Don't run a parallel `mc.listRelatives` / `mc.parent` walk for the same intent.
- Scope: new code and files you touch — not a mandate to retrofit whole tools.
  (`cgm-meta-naming-hierarchy`, `cgm-msglist-patterns`)

### 4. Search before you write
- Before any new `def` using `mc.ls`, `listConnections`, `listAttr`, `keyframe`, or name-string hacks:
  read [`Features/Feature_CoreLibLookups.md`](Features/Feature_CoreLibLookups.md) and call what's there.
- Before new helpers, grep `cgmToolsPy3` for the problem already solved. A new lib function needs a real gap.
- Shared lookup tables / alias maps / enums → `cgm/core/lib/shared_data.py` (as `SHARED`), not module-local
  dicts. (`cgm-meta-and-existing-patterns`, `cgm-shared-lookup-data`)

### 5. Module placement
| Kind | Home |
|------|------|
| General utilities (paths, math, P4, file IO, non-meta Maya) | `cgm/core/lib/` |
| Meta, blocks, Scene, rig build | `cgm/core/mrs/`, `cgm/core/rig/`, `mrs/lib/` |
| Artist tool windows / shelves | `cgm/core/tools/` (+ `tools/lib/`) |

**Do not modify** `cgm/lib/zoo/` (zooPy) or `Red9/` without explicit user clearance — fix or wrap in
`cgm/core/`. Red9 edits that do happen must be recorded in
[`Patches/Red9/manifest.json`](Patches/Red9/manifest.json). (`cgm-module-placement`, `Feature_Red9Patches.md`)

### 6. `mClass` / meta API changes need approval
- **Do not add new instance methods** on registered `mClass` subclasses, or call methods you just invented.
  Default is a `lib/` / `rig/` **module function** taking `mObj` as first arg.
- If the user approves an `mClass` change, **tell them to run `import cgm.core as CGM; CGM._reload()`**
  before expecting new behavior. (`cgm-meta-and-existing-patterns`, `Feature_CgmMetaAPI.md`)

### 7. Reload
- Reload only via `cgmGEN._reloadMod(module)` after `import cgm.core.cgm_General as cgmGEN`.
- **Banned:** `importlib.reload`, `importlib.import_module`, bare `reload()`, `imp.reload`,
  `__import__(__name__)`, `sys.modules[...]` tricks — in code, comments, docs, and Script Editor snippets.
- Dependencies first, consumer last; tool module last. Log each module name as it reloads.
- **Never** reload or rebind inside one-shot action callbacks (Create, bake, export).
- **Never** build a partial Red9 → `cgm_Meta` → `cgm_RigMeta` stack inside a tool's `reload_dependencies()`
  — it breaks other metaclasses. (`cgm-reload-mod`)

### 8. Debugging order
1. **Stale session first.** New `log.info` from the tool module but none from the backend module ⇒ stale
   import / cached meta, not broken wiring. Fix is Reload Dependencies, shelf relaunch, or Maya restart.
2. **Log at boundaries** (UI handler → public API kwargs → first backend branch) before adding validation,
   coercion, or rig logic.
3. **One root cause per turn.** Don't stack fixes without Maya confirmation between them.
4. **Stop condition:** after one change that doesn't move Maya output and backend entry logs are still
   absent — stop patching build logic, document reload steps only.
5. Never interpret a count without naming *which* object (sim joints vs follow locs vs inCurve CVs).
   (`cgm-stale-session-diagnosis`, `cgm-debug-order`, `cgm-simchain-debug-contract`)

### 9. Working with pasted Maya logs
- Quote what is **present vs absent** (specific module/function lines), then state **one** inference before
  editing. Prefer minimal diff until session freshness is proven. Don't re-explain the same root cause
  across turns without a new log or user confirmation. (`cgm-agent-token-discipline`)

### 10. Clear code
- Names match scene nodes/attrs/buffer fields (`m_ik_orient_frame`, not `mSpan`). Return what callers need.
- Pass the block build instance (`self`) into helpers; set `self.ml_*` **inside** the helper, not by
  assigning a return value at the call site.
- Obscure patterns only with a stated one-line reason (design / engineering / performance). (`cgm-clear-code`)

### 11. Long-running UI work needs progress
- Any button or menu that can keep Maya busy — multi-frame bake, timeline export, batch rebuild, heavy
  scene walks, many constraints/duplicates — must show **visible progress** and support cancel where it can.
  (`cgm-long-running-ui-progress`)

### 12. Perforce
- If an edit is blocked by read-only / not-checked-out: **stop**, name the full path and the intended change,
  wait for the user. No shell one-liners, patch scripts, retries, or edit-a-copy workarounds.
  (`perforce-checkout`, `Feature_PerforceIntegration.md`)

## Rule index (`.cursor/rules/` — full text)

Always on: `python3-primary` · `maya-cmds-import` · `maya-cmds-strings-only` · `cgm-runtime-meta-not-strings`
· `cgm-meta-naming-hierarchy` · `cgm-msglist-patterns` · `cgm-meta-and-existing-patterns`
· `cgm-shared-lookup-data` · `cgm-module-placement` · `cgm-reload-mod` · `cgm-stale-session-diagnosis`
· `cgm-debug-order` · `cgm-agent-token-discipline` · `cgm-clear-code` · `cgm-long-running-ui-progress`
· `perforce-checkout`

Conditional (ported to `.claude/skills/`): `google-doc-capture` · `cgm-simchain-debug-contract`
· `py2-backport-session` · `bridge-repo-context`

## Where docs go

| Writing… | Goes in |
|----------|---------|
| Long-lived architecture / design contract | `Features/Feature_*.md` — see [`Guides/NewFeature_Guide.md`](Guides/NewFeature_Guide.md) |
| Branch timeline, what landed when | `Branches/Branch_*.md` — see [`Guides/NewBranch_Guide.md`](Guides/NewBranch_Guide.md) |
| QA / validation checklist | per [`Guides/NewTesting_Guide.md`](Guides/NewTesting_Guide.md) |
| Artist-facing manual text | paste blocks only — `google-doc-capture` skill. **Never** into `cgmToolsPy3`. |

When you change code covered by a design contract in `AGENTS.md` (Scene export, DynSim, MRS wiring,
AnimData, Project Manager, …), **update that `Feature_*.md` in the same pass**.

## Environment notes

- Shell is **PowerShell 5.1** — no `&&`, no `?:`, no `??`. Chain with `;` or `if ($?) { }`.
- **`git`** is Git for Windows at `C:\Program Files\Git\cmd` (on the machine PATH). If `git` comes back
  "not recognized", the session inherited a stale environment — use the full path
  `& "C:\Program Files\Git\cmd\git.exe"` for that session and tell the user a restart will fix it.
  GitHub Desktop also bundles its own git; prefer the Program Files one.
- Maya code here is **not runnable from this shell**. Behavior claims need Maya verification by the user —
  mark untested paths "verify in Maya" rather than reporting them as done.
