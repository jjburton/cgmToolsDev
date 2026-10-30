---
name: google-doc-capture
description: >-
  Captures cgmTools Maya tool changes as paste-ready Google Doc section updates mapped to the team's
  artist manual outline. Use when the user mentions Google Doc, artist manual, user-facing documentation,
  "capture changes for documentation", "sync branch work to the manual", or release notes for artists.
---

# Google Doc capture

Ported from `.cursor/skills/google-doc-capture/SKILL.md` and `.cursor/rules/google-doc-capture.mdc`.

## When to use

- User asks to document tool changes for **Google Docs** or the **artist manual**
- User wants branch/commit work turned into **manual section updates**
- User says "capture for documentation", "sync to Google Doc", "what should I paste in the manual"

## Instructions

1. **Read** [`Guides/GoogleDoc_Capture_Guide.md`](../../../Guides/GoogleDoc_Capture_Guide.md) — especially
   the outline table and output template. If the outline table is still `[TBD]`, ask the user for exact
   section titles from the manual before drafting.

2. **Confirm scope** (ask if unclear):
   - Tool(s): Scene, Project, export, MRS Build, etc.
   - Range: branch name, date, or commit count
   - Target **Google Doc section titles** (from the guide's outline table; if all `[TBD]`, ask the user to
     paste TOC headings)

3. **Gather sources**, in order:
   - `git log` / `git diff` in `cgmToolsPy3`
   - If `git` is "not recognized", the session has a stale PATH — retry once with
     `& "C:\Program Files\Git\cmd\git.exe"` before falling back
   - User-pasted log, or [`Branches/Branch_*.md`](../../../Branches/)
   - Code skim **only** for user-visible strings (`ann=`, menu labels, button order) in relevant UI modules

4. **Draft** one block per section — no markdown tables:

   ```
   ## [Exact Google Doc section title]

   **Summary** (1–2 sentences)

   **What changed**
   - …

   **How to use it**
   1. …

   **Before / After** (if applicable)

   **Notes / limitations**
   - …

   **Source** (optional — user deletes before publish)
   - Branch: … | Commits: … | Files: …
   ```

5. **Finish** with **Suggested placement**: a bullet list mapping each block → section title.

## Do not

- Edit the Google Doc directly (no API) — produce copy-paste-ready text only
- Write capture output into `cgmToolsPy3`
- Replace branch docs — only consume them as sources
- Use developer jargon as the primary wording (file paths, internal function names)
- Write long essays — prefer **one section block per Google Doc heading**

## Translation rules

- Prefer menu paths, tooltip text, and workflow order from the UI
- Flag breaking changes and "verify in Maya" for untested paths
- Cross-reference other manual sections with one line when a change spans topics

## Example request

> Sync Branch_UnrealWorkflow to Google Doc — Scene UI and Export sections only.

**Response shape:** two section blocks (Scene UI, Export) + Suggested placement list.
