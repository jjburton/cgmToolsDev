# Google Doc Tool-Change Capture Guide

## Purpose

This guide defines how **agents and developers** turn recent cgmTools changes into **paste-ready updates** for your **user-facing Google Doc** (artist/animator/lead manual).

| Audience | Where it lives | Content style |
|----------|----------------|---------------|
| Developers | [`Branches/Branch_*.md`](../Branches/), [`NewBranch_Guide.md`](./NewBranch_Guide.md) | Timeline, files, PR notes, technical decisions |
| Artists / production | Google Doc (external) | Menus, buttons, workflows, before/after, limitations |
| Deep technical | [`NewFeature_Guide.md`](./NewFeature_Guide.md), `Docs/CursorRef/` (if used) | Architecture, APIs, testing matrices |

**When to run capture**

- After a feature slice lands (especially UI or export behavior)
- Before a release or hand-off to production
- When a branch doc timeline was updated and user-visible behavior changed
- When you need manual sections refreshed without rewriting the whole doc

**When to skip**

- Internal-only refactors with no Maya UI or workflow change
- Typo fixes in code comments
- Changes already documented in the Google Doc for that release

---

## Your Google Doc outline

Replace `[TBD]` rows with **exact section titles** from your manual (copy from the Google Doc table of contents). Agents must map every draft block to one of these sections.

| Google Doc section | What belongs here | Example tools / areas |
|--------------------|-------------------|------------------------|
| `[TBD: e.g. Scene UI]` | Buttons, columns, right-click menus, icons, file lists | Scene, Project picker |
| `[TBD: e.g. Export]` | Export modes, paths, FBX, batch, prep options | Scene export, bake/prep |
| `[TBD: e.g. MRS Build]` | Send to Build, batch rig, build window | Scene, Builder |
| `[TBD: Release notes]` | Dated summary bullets for a release | All user-visible changes |

**Cross-section changes:** If one change affects multiple sections (e.g. new export button in Scene UI + export path rule), write **separate blocks** under each section title and add a one-line cross-reference in each (e.g. “See also: Export — cutscene pathing”). Do not merge unrelated topics into one section.

---

## Agent workflow

### 1. Scope

Confirm with the user (or infer from the request):

- **Tool(s):** Scene, Project, RigBlocks, bake/prep, etc.
- **Time range:** branch name, “since [date]”, or last N commits
- **Target sections:** which rows from the outline table above

### 2. Gather sources (in order)

1. **Git** on `cgmToolsPy3` (if available):
   - `git log --oneline -N`
   - `git log --since="YYYY-MM-DD"`
   - `git diff [base]...HEAD` for touched UI modules
2. **Branch doc** in [`Branches/`](../Branches/) (e.g. `Branch_UnrealWorkflow.md`) — timeline and PR notes
3. **Code** — only for **user-visible** strings: menu labels, `ann=` tooltips, button order, export mode names. Prefer reading callers in [`Scene.py`](../../cgmToolsPy3/cgm/core/mrs/Scene.py), [`Project.py`](../../cgmToolsPy3/cgm/core/tools/Project.py), etc., not full file dumps.

**Git not on PATH:** Ask the user to paste `git log --oneline -N` or point at an updated branch doc. Do not invent commit messages.

### 3. Translate (dev to user language)

- Lead with **what the artist sees and does**, not file paths
- Use **exact UI strings** from code when possible (menu item, tooltip)
- Call out **breaking changes** and **workarounds** explicitly
- Optional **Technical reference** sub-bullet under **Source** (strip before publishing)

### 4. Draft

Produce **one block per Google Doc section** using the [output template](#output-template-google-docsfriendly) below.

### 5. Review checklist (before user pastes)

- [ ] Every block maps to an outline section title (no `[TBD]` unless user has not filled the table yet)
- [ ] Steps are actionable in Maya (open tool, click, expected result)
- [ ] No secrets, internal paths, or credentials
- [ ] Untested behavior marked “verify in Maya” or “pending QA”
- [ ] Breaking changes visible in **Summary** or **Notes / limitations**

---

## Output template (Google Docs–friendly)

Agents must emit plain structure **without markdown tables** (tables paste poorly into Google Docs). Use one block per section:

```
## [Exact Google Doc section title]

**Summary** (1–2 sentences)

**What changed**
- Bullet…

**How to use it**
1. Step…

**Before / After** (omit if not applicable)

**Notes / limitations**
- …

**Source** (optional — delete before publishing)
- Branch: … | Commits: … | Files: …
```

### Formatting rules

- In **regular prose**, use HTML entities for angle brackets: `Func&lt;string&gt;` not `Func<string>`
- Angle brackets are fine **inside code blocks**
- Spell out comparisons: “less than 1ms” not “&lt;1ms”
- Keep bullets one level deep; use numbered lists for sequences
- No emoji required (Google Doc may use its own styles)

---

## Relationship to branch docs

- **Branch docs stay the dev ledger.** Do not stop updating [`Branches/Branch_*.md`](../Branches/) when shipping code.
- **Google Doc capture is downstream:** extract **user-visible** deltas from branch timelines / commits.
- Optional branch timeline line: `Google Doc: [section title] updated (YYYY-MM-DD)`
- Related guides:
  - [`NewBranch_Guide.md`](./NewBranch_Guide.md) — how to write branch timelines
  - [`NewFeature_Guide.md`](./NewFeature_Guide.md) — long-lived feature architecture (not a substitute for the manual)
  - [`NewTesting_Guide.md`](./NewTesting_Guide.md) — QA checklists (can inform **Notes / limitations**)

---

## Prompt cheat sheet

Examples you can send in Cursor:

- “Capture Scene export changes since May 9 for the Export section of the CGM manual.”
- “Sync `Branch_UnrealWorkflow` timeline to Google Doc — Export and Scene UI sections only.”
- “Document last 10 commits on UnrealWorkflow for Google Doc; use the capture guide outline.”
- “I pasted our Google Doc section titles below — draft updates for [branch/date range].”

Invoke the **`google-doc-capture`** skill when you want the agent to load this workflow automatically.

---

## Git availability

Cursor agent shells may not have `git` on PATH even when GitHub Desktop is installed. Fallbacks:

1. User runs `git log --oneline -30` locally and pastes output into chat
2. User points at an updated [`Branches/Branch_*.md`](../Branches/) file
3. User installs [Git for Windows](https://git-scm.com/download/win) with **“Git from the command line”** and restarts Cursor

---

## Golden sample (optional appendix)

When you have a real paste that worked well, add a short example under this heading for agents to mimic tone and depth. Until then, use [`Branches/Branch_UnrealWorkflow.md`](../Branches/Branch_UnrealWorkflow.md) timeline entries as a **source**, but rewrite for artists using the template above.

---

*Last updated: 2026-05-18*
