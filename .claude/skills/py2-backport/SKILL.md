---
name: py2-backport
description: >-
  Rules for a Python 2 backport session — porting or aligning cgmToolsPy3 changes into the legacy py2
  cgmTools tree. Use ONLY when the user explicitly says they are backporting to py2, opens
  cgmTools-py2-backport.code-workspace, or references Plans/PY2_BACKPORT_PLAN.md. Default sessions are
  py3-only; without this skill active, do not read, search, or edit any py2 checkout.
---

# PY2 backport session

Ported from `.cursor/rules/py2-backport-session.mdc`.

## Gate

This applies **only** when the user has explicitly opened a backport session. If they have not said so,
stop and ask — do not assume py2 paths exist, and do not go looking for them.

Default sessions are **py3-only** (`cgmToolsPy3`). See `.cursor/rules/python3-primary.mdc`.

## Setup

- The user opens [`cgmTools-py2-backport.code-workspace`](../../../cgmTools-py2-backport.code-workspace),
  or adds their local py2 checkout via **Add Folder to Workspace…**, so both trees are visible.
- That workspace file assumes the py2 checkout is at `../../repos/cgmTools` relative to `cgmToolsDev`.
  **Verify that path exists** before relying on it — adjust the workspace file if their checkout is elsewhere.
- In Claude Code, the py2 tree must be an **additional working directory** before it can be read or edited.

## Scope

- **Purpose:** port or align specific py3 changes into the legacy py2 tree — not routine feature work.
- Follow the steps and boundaries in [`Plans/PY2_BACKPORT_PLAN.md`](../../../Plans/PY2_BACKPORT_PLAN.md).
- Prefer **minimal, surgical edits** on the py2 side. Do not modernize, reformat, or refactor py2 code
  that the port does not require.
- py2 syntax constraints apply there: no f-strings, `print` conventions of that tree, `reload()` builtin
  rather than `importlib` (and `cgmGEN._reloadMod` still wraps it — see `.cursor/rules/cgm-reload-mod.mdc`).

## When finished

Tell the user to switch back to [`cgmTools.code-workspace`](../../../cgmTools.code-workspace) so py2 is not
indexed during normal py3 work.
