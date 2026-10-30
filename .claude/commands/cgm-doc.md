---
description: Create or update a Feature_*.md design contract or Branch_*.md timeline in cgmToolsDev
argument-hint: "feature <Name> | branch <Name> — e.g. 'feature BezierIK' or 'branch Jan2026'"
---

Write or update cgmToolsDev documentation. **Never** write any of this into `cgmToolsPy3`.

**Request:** $ARGUMENTS

## Routing

| Kind | Goes in | Follow |
|------|---------|--------|
| `feature <Name>` | `Features/Feature_<Name>.md` | [`Guides/NewFeature_Guide.md`](../../Guides/NewFeature_Guide.md) |
| `branch <Name>` | `Branches/Branch_<Name>.md` | [`Guides/NewBranch_Guide.md`](../../Guides/NewBranch_Guide.md) |
| testing checklist | per [`Guides/NewTesting_Guide.md`](../../Guides/NewTesting_Guide.md) | that guide |
| artist-facing manual text | nowhere in a repo — paste blocks only | the `google-doc-capture` skill |

If the request is ambiguous, ask which one before writing.

## Steps

1. **Read the matching guide first** — use its template verbatim, including the status/overview header.
   Respect `NewBranch_Guide.md`'s formatting rules: HTML entities for angle brackets in regular text,
   spelled-out comparisons ("less than 1ms"), no backticks for attributes in timeline entries.
2. **If the file already exists, update it in place** — append timeline entries or revise sections. Do not
   rewrite a living document from scratch, and do not drop existing sections you did not research.
3. **Gather facts before writing.** Use `git log` / `git diff` in `cgmToolsPy3`; if `git` is "not
   recognized", retry with `& "C:\Program Files\Git\cmd\git.exe"`. If history is still unavailable, ask the
   user for pasted `git log --oneline -N` or point to the relevant `Branches/Branch_*.md`. Read the actual
   `cgmToolsPy3` code for behavior rather than inferring it. Mark anything unverified in Maya as such —
   do not state untested behavior as working.
4. **Cross-link**: a new or substantially changed `Feature_*.md` needs a numbered entry in the design
   contract list in [`AGENTS.md`](../../AGENTS.md), and a `Branch_*.md` reference for its timeline. Add or
   update that entry in the same pass and say that you did.
5. Set **Last Updated** to today's date.
