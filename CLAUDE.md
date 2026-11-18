# CLAUDE.md — cgmTools

Entry point for Claude Code. Read this with [`AGENTS.md`](AGENTS.md) (repo layout, workspace setup, and
the numbered **design contracts** in `Features/`).

## Rule 0 — Delegate to the cheapest capable subagent (HARD RULE, checked first every turn)

- The main session plans, synthesizes, reviews diffs, and answers. It does **not** search, explore, run git ops, resolve conflicts, or edit files itself.
- **Inline budget: ≤2 tool calls for the whole turn**, against a known path (one `Read`, one `git show <sha>`). Plan/wrap-up bookkeeping calls don't count; everything else does — including "just checking" commands (`git status`, `git fetch`, `git log`, `ls`, `grep`).
- **Decide before the first tool call.** If the job will plausibly take >2 calls, the first real tool call is `Agent`. No "let me look first, then delegate."
- **Tripwire:** the moment a 3rd inline call would be needed, stop and hand the remainder to a subagent with what you know so far. Never finish "since I'm already here."
- No exemption for task type: git merges, conflict resolution, commits, doc edits, and multi-file reads are all delegated (Haiku when the plan is written; Sonnet when judgment is needed).
- Always pass `model` explicitly:
  - **Haiku** — searches, `git log`/`blame`/history digs, merges/commits/conflict fixes with a written plan, file/symbol lookups, edits with a written plan.
  - **Sonnet** — work needing judgment: locating a cause across files, log diagnosis, non-trivial edits, conflict resolution needing content decisions.
  - **Opus** — only deep MRS/rig build, meta graph, or DynSim design work.
- Choose the model by scope and depth, not domain (Maya vs engine work): Opus also covers engine/systems/perf work and many-file refactors. Why delegate even small, already-diagnosed edits: it keeps expensive-model tokens off simple work, and the user can address that specific agent about its result (`SendMessage` / its diff).
- Brief tightly: goal, exact paths/repos, what's ruled out, and the return shape (conclusion + `file:line` / sha refs, no file dumps).
- Follow-ups go to the same agent via `SendMessage`; never redo a subagent's work inline. Review its diff, not whole files.
- Parallel independent lookups go out in one message, each on the cheapest model that fits.
- **Accountability:** the turn's wrap-up recap names which subagents ran (model + job), or states "inline (≤2 calls)". Exceeding the budget without delegating is a rule violation — say so plainly if it happens.

## Two repos, one session

| Repo | Role | Claude may write |
|------|------|------------------|
| `cgmToolsDev` (this one) | Bridge: docs, rules, plans, branch notes | Yes — docs, rules, config |
| `cgmToolsPy3` (additional working dir) | **Ship tree** artists sync into Maya `scripts/` | Yes — **code only** |

`cgmToolsDev` holds **developer-workflow** assets: Claude config, workspace files, `Plans/` (backport and
coordination docs, e.g. `PY2_BACKPORT_PLAN.md`), `Guides/`, `Features/`, `Branches/`. It is **not** the Maya
scripts tree. `cgmToolsPy3` is the **runtime library**; don't confuse folders here with its package modules.

**Never** create `.claude/`, `.cursor/`, `CLAUDE.md`, `AGENTS.md`, `*.code-workspace`, or bridge docs
inside `cgmToolsPy3`. Dev-workflow assets live here. (`cgmToolsPy3/.gitignore` enforces this as a backstop.)

**Python 3 only.** `cgmToolsPy3` is the default target for edits and suggestions. Do not read, search, propose
changes to, or assume paths in a legacy py2 `cgmTools` checkout unless a PY2 backport session is explicitly
active — see the `py2-backport` skill and `Plans/PY2_BACKPORT_PLAN.md`.

## Iron rules (always loaded from .claude/rules/)

Every file in [`.claude/rules/`](.claude/rules/) loads at session start, like this file. They govern code in
`cgmToolsPy3`; open the named file for the full contract and examples.

- [`maya-cmds.md`](.claude/rules/maya-cmds.md) — `import maya.cmds as mc`; every `mc.*` node argument is a `str`, never meta.
- [`meta-runtime.md`](.claude/rules/meta-runtime.md) — meta at runtime, strings at edges; `m*`/`ml_*`/`md_*`; msgLists; no new mClass methods.
- [`reuse-and-placement.md`](.claude/rules/reuse-and-placement.md) — search before writing; `SHARED` data; module homes; no zoo/Red9 edits.
- [`reload.md`](.claude/rules/reload.md) — only `cgmGEN._reloadMod`; banned reload APIs; never reload in action callbacks.
- [`debugging.md`](.claude/rules/debugging.md) — stale session first, boundary logs, one root cause per turn, minimal diffs.
- [`clear-code.md`](.claude/rules/clear-code.md) — explicit names, `self`-passing helpers; obscurity needs a stated reason.
- [`ui-progress.md`](.claude/rules/ui-progress.md) — long-running buttons show a cancellable Maya progress bar.
- [`perforce.md`](.claude/rules/perforce.md) — blocked by checkout: stop, name the file, wait; no workarounds.

## Skills and commands

Skills (`.claude/skills/`): `google-doc-capture` (artist-manual paste blocks) · `cgm-dynsim-debug` (DynSim
count vocabulary and debug log contract) · `py2-backport` (only in an explicit py2 backport session).
Commands (`.claude/commands/`): `/cgm-doc` (create/update a Feature or Branch doc) · `/cgm-review` (audit
cgmToolsPy3 changes against the iron rules).

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
