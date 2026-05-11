# PY2 backport plan

Use this document when porting or aligning changes between **`cgmToolsPy3`** (Python 3, primary) and the legacy **`cgmTools`** Python 2 tree.

## When to use

- You intend to **apply the same fix or feature** (or deliberate parity) on **both** py3 and py2, **or**
- You are **auditing** differences for a controlled backport.

For **new py3-only development**, do **not** add the py2 repo to your workspace; use **`cgmTools.code-workspace`** only.

## Session setup

1. Open **`cgmTools-py2-backport.code-workspace`** from `cgmToolsDev`, **or** start from **`cgmTools.code-workspace`** and **Add Folder to Workspace…** for your local py2 checkout.
2. If the default py2 path does not exist on disk, edit the fourth folder entry in **`cgmTools-py2-backport.code-workspace`** to match your **`cgmTools`** (py2) clone.
3. Confirm both **`cgmToolsPy3`** and py2 roots appear in the Explorer sidebar.

## Workflow (fill in specifics per task)

1. Identify the **py3 change set** (commits, files, or behavior).
2. Map to the **equivalent modules/paths** under py2 (path names may differ).
3. Apply **minimal** py2 edits; preserve py2 compatibility (syntax, imports, Maya APIs available on your supported versions).
4. **Test** in the environment that consumes py2, if applicable.
5. Document any **intentional non-parity** (deprecated on py2, etc.).

## Session teardown

Close the backport workspace when done and return to **`cgmTools.code-workspace`** so py2 is **not** indexed during routine py3 development.
