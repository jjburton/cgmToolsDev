# Reuse first, shared data, and module placement

Applies whenever you add a helper, lookup, table, or new module in cgmToolsPy3.

## Search before you write

- Before any new `def` using `mc.ls`, `listConnections`, `listAttr`, `keyframe`, or name-string hacks, read
  [`Feature_CoreLibLookups.md`](../../Features/Feature_CoreLibLookups.md) and call the names listed there.
- Don't add a wrapper whose only job is that query. A new lib function needs a real gap shown by search, not a
  type-check or log line on top of an existing call.
- Before new helpers (extra `mc.ls`, string hacks, duplicate logic), grep the cgmToolsPy3 tree, `cgm/core/lib/`
  and `mrs/lib/` for the problem already solved. Reuse or extend unless there is a clear gap and a deliberate
  reason to diverge.
- When unsure what meta can do, read `cgm/core/cgm_Meta.py` ([`meta-runtime.md`](meta-runtime.md)).

### MRS block build (`rig_*` + `lib/*_block_utils`)

- `rig_dataBuffer` / `rig_frame` store build state on `self` (`self.ml_*`, `self.d_*`). Grep sibling `rig_*` steps and
  `BEZIERIKBLOCK` / `RIGFRAME` callers before new wiring.
- Lib helpers called from blocks take the block build instance (`self`) first when peers do
  (`squash_ik_fk_blend_segment_scale_compensate(self, ...)`, `RIGFRAME.bezier(self, ...)`). Set `self.ml_*` inside
  the helper (see [`clear-code.md`](clear-code.md)).

## Shared lookup and static data

Put reusable lookup tables, alias maps, enums, and version-compat data in `cgm/core/lib/shared_data.py`, imported
as `SHARED`. Examples: Maya node-type aliases (`d_mayaNodeType_canonical`), naming suffix maps, axis/color tables,
rotate-order maps, project-wide option lists and type vocab. Callers read from `SHARED`; never copy the dict.

Don't add module-level dicts/constants in implementation files when the data is compared in more than one place,
is Maya-version/API-compat normalization (e.g. `addDL` -> `addDoubleLinear`), or is vocabulary other tools or
tests might need. Constants private to one file and not project vocabulary are fine.

```python
# BAD: local alias table in validateArgs.py
_MAYA_NODE_TYPE_CANONICAL = {'addDL': 'addDoubleLinear'}

# GOOD: shared_data.py
d_mayaNodeType_canonical = {'addDL': 'addDoubleLinear'}

# GOOD: caller
return SHARED.d_mayaNodeType_canonical.get(_intialCheck, _intialCheck)
```

Before adding data: (1) search `shared_data.py` and nearby `lib/*_utils.py`; (2) tables live in `shared_data`,
lookup functions live in `lib/` (don't duplicate lookup logic there; see Feature_CoreLibLookups.md); (3) extend an
existing `d_*` / `_d_*` table when the category exists, else add a new named section.

## Where new code lives

| Kind of code | Home |
|--------------|------|
| General utilities (paths, math, P4, file IO, non-meta Maya cmds) | `cgm/core/lib/`: extend an existing `*_utils.py` or add a module (e.g. `lib/perforce.py`) |
| Meta, blocks, Scene, rig build logic | `cgm/core/mrs/`, `cgm/core/rig/`, `mrs/lib/` |
| Artist tool windows / shelves | `cgm/core/tools/` (+ `tools/lib/` for shared UI chunks) |
| Truly global cross-cutting helpers (logging, callbacks) | `cgm/core/cgm_General.py`, sparingly; prefer `lib/` |

Match the import style of nearby callers (e.g. `import cgm.core.lib.path_utils as PATHUTIL`).

## Keep modules focused

- Don't bolt unrelated features onto a module because it is already imported (P4 belongs in `lib/perforce.py`, not
  `cgm_General` or zooPy).
- Callers (`Scene.py`, `bakeAndPrep.py`, ...) stay thin: import a `lib/` helper, orchestrate, return.

## Do not modify vendored trees

- `cgm/lib/zoo/` (zooPy) is not ours: no edits, and no wiring `cgm.core` through it.
- `Red9/` (vendored core / docs; Pro Pack if on disk): do not modify without explicit user clearance, including for
  bug fixes. Default: fix or work around in `cgm/core/` (`lib/`, `mrs/`, `tools/`). If a bug truly lives in Red9,
  ask first. Red9 edits that do happen must be recorded in
  [`Patches/Red9/manifest.json`](../../Patches/Red9/manifest.json) (see
  [`Feature_Red9Patches.md`](../../Features/Feature_Red9Patches.md)).
- Useful vendored patterns: reimplement or wrap under `cgm/core/lib/`; don't import/patch upstream.
