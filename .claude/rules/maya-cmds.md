# Maya cmds: alias and argument types

Applies to every `mc.*` call in cgmToolsPy3, ProjectScripts, and other in-house Maya Python.

## Import alias

- Import as `import maya.cmds as mc`; call `mc.ls()`, `mc.objExists()`, etc.
- Never `import maya.cmds as cmds` or bare `cmds.` in new or edited code. Match nearby modules
  (`cgm/core/tools/`, `cgm/core/lib/`).
- `maya.mel as mel` is unchanged unless the file already uses a different local alias.

## Arguments are `str`, never meta

Every `mc.*` argument (and MEL run on scene nodes) that names a DAG node, shape, component, or plug must be a
`str`: a full path or unique short name Maya accepts. Never pass a `cgmMeta` / Red9 `MetaClass` instance.

- **DAG name for `mc.*` only:** use `asMeta=False` on hierarchy helpers, e.g. `mTarget.getParent(asMeta=False)`
  returns a `str` (or `False`). Pass it straight to `mc.*`; no extra `.mNode` step.
- **Meta for the next rig step:** use `asMeta=True`, work in meta, then `.mNode` (or `p_nameLong`) at the
  `mc.*` call. Prefer `.mNode` on meta you already hold.
- `mc.listRelatives(mObj.mNode, ...)` is equivalent to `getParent(asMeta=False)` when you only need the parent name.
- Don't assume `VALID.mNodeString(arg)` returned a `str` (on failure it can return the original object). Check
  `isinstance(..., str)` before `mc.*`. Use `validateArgs.mNodeString` only to produce a `str`, then pass that variable.
- Rig modules with many `mc.*` calls (e.g. `dynamic_utils`) may define a local `_dag_str(mObj)` (str or
  `.mNode`, raise if not str). Still convert at the call site; never pass meta through.

```python
# GOOD: string path when mc is next
_driver = mTarget.getParent(asMeta=False)
mc.parentConstraint(_driver, mFollicle.mNode, mo=True)

# GOOD: meta for logic, .mNode for mc
mParent = mTarget.getParent(asMeta=True)
mParent.p_parent = mGrp
mc.parentConstraint(mParent.mNode, mFollicle.mNode, mo=True)

# BAD: meta instance passed to mc (TypeError: Object (node: '...' | mClass: ...) is invalid)
mc.parentConstraint(mTarget.getParent(asMeta=True), mFollicle.mNode, mo=True)
mc.nodePreset(list=mFollicle)
```

## Lists and kwargs

- `mc.ls`, `skinCluster`, `parentConstraint`, `connectAttr`, `listConnections`, `nodePreset`, etc.: every node
  entry in a list or tuple must be `str`.
- Plug strings: `'{0}.{1}'.format(node.mNode, attr)`. The node part is `str`, not meta.
- `msgList_get` results go to `mc.*` only via `.mNode`.

See [`meta-runtime.md`](meta-runtime.md) for keeping meta everywhere except this `mc.*` edge.
