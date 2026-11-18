# Meta at runtime: handles, naming, hierarchy, msgLists, mClass API

Applies to new code and files you touch in `cgm/core/tools/`, `cgm/core/rig/`, `cgm/core/mrs/`, and the `lib/`
helpers they call for scene work. It is not a mandate to retrofit or rename whole tools in one pass.

## Runtime is meta, not strings

| Phase | Use |
|-------|-----|
| UI labels, scroll rows, status text | Strings (display only) |
| Saved data: optionVars, `.cgm*Dat`, CCL, presets, JSON sidecars | Strings (paths, names, enums) |
| Runtime: handlers, build/create, in-memory lists, message graphs, multi-step pipelines | `cgmMeta` instances (or typed subclasses: `cgmObject`, `cgmDynFK`, ...) |

Don't carry DAG identity as bare node strings (`mNode`, long paths, `mc.ls` results) through tool or rig logic
while the object exists in the scene. Meta resolves `p_nameLong` / `mNode` at call time and survives re-parent
and namespace changes.

**Boundaries where strings are allowed**

1. Read disk / optionVar: immediately `cgmMeta.asMeta(...)` or `validateArgs.validateObjArg`, then store on `self`
   or parallel lists as meta (`self._mDynFK`, `_ml_loaded[i]`).
2. Write disk / optionVar: serialize from meta once (`.mNode`, long path, or stable `p_nameBase` per schema), at save time only.
3. `mc.*` / MEL: convert at the call (`.mNode`, `getParent(asMeta=False)`); see [`maya-cmds.md`](maya-cmds.md).
4. Logging: strings are fine; log `mObj.p_nameShort` or `repr` of meta, not stale paths held from earlier in the function.

**Do not**

- Pass lists of node strings through create/rebuild/skin/connect pipelines when a list of meta (or an ordered
  chain such as `_hair_normalize_sim_chain`) can hold the same objects.
- Name nodes with ad-hoc `'%s_%s' % (a, b)` when meta provides `p_nameBase`, `cgmName`, or indexed naming on a `name` token.
- Call `mc.parent(string, string)` across steps when `mChild.p_parent = mParent` is available.
- Resolve selection or scroll rows by parsing display strings. Use **index -> parallel meta list**; canonical row =
  meta or wrapper with `.item` meta, and the scroll shows the `.alias` string only
  ([`Feature_CgmToolUI.md`](../../Features/Feature_CgmToolUI.md)).
- Keep the only reference to a setup as a string on `self` (`self._setupNode = '|foo|bar'`) when
  `self._mSetup = cgmMeta.asMeta(...)` is the pattern.

**Tool UI wiring**

- Load / Create / Bake / Connect handlers: resolve inputs to meta at the top of the handler (or on load into `self._m*`).
- Reload Dependencies: rebind `self._m*` from existing nodes after backend reload (see [`reload.md`](reload.md)).
- `lib/` and `rig/` functions that operate on scene objects take `mObj` / meta-list args, not "maybe string maybe
  meta", unless documented as a single boundary function that normalizes once with `cgmMeta.asMeta`.

## Naming: `m*`, `ml_*`, `md_*`

| Pattern | Meaning | Examples |
|---------|---------|----------|
| `m*` | One `cgmMeta` / Red9 `MetaClass` instance (node still in scene) | `mTarget`, `mFollicle`, `mGrp`, `mDynFK`, `mInCrv` |
| `ml_*` | list (or tuple used as ordered chain) of meta | `ml_sim`, `ml_targets`, `ml_baseTargets`, `ml_driven`, `ml_chains` |
| `md_*` | dict whose values are meta (keys: index, name token, msg label) | `md_chains`, `md_byBaseName` (not generic config dicts) |
| none of the above | Not runtime meta: UI label, plain config, path from disk, or `str` for `mc.*` | `name`, `_follDriver`, `chainMode`, optionVar strings, preset attr dict from JSON |

Never name a meta instance `target` and a string `mTarget`; the prefix marks instantiated meta, not DAG strings.
Saved data stays strings; convert with `cgmMeta.asMeta` / `validateObjArg` at load and store as `m*` / `ml_*` / `md_*`.

## Hierarchy: meta owns it

Don't maintain a parallel DAG walk (`mc.listRelatives`, `mc.parent`, path parsing) for the same parent/child
intent when `m*` / `ml_*` already model it.

| Intent | Prefer | Avoid in rig/tool logic when meta exists |
|--------|--------|------------------------------------------|
| Parent child under parent | `mChild.p_parent = mParent` | `mc.parent(...)` mid-pipeline |
| Read parent | `getParent(asMeta=True)`, or `asMeta=False` when the next step is `mc.*` only | `listRelatives` as a second way to find the parent while holding `mParent` |
| Read children / owned lists | `msgList_get` -> `ml_*`, `getMessageAsMeta`, `getChildren(asMeta=True)`, `getAllChildren` | Re-walking the DAG or `listConnections` when a msgList owns membership |
| Ordered joint chain | Ordered `ml_*` + `p_parent` / shared helpers | Bare list of path strings through create/skin/connect |

`mc.listRelatives` / `mc.parent` remain fine (a) in `lib/` or `shared_data` + lookup helpers implementing a
documented query per [`Feature_CoreLibLookups.md`](../../Features/Feature_CoreLibLookups.md), with callers
consuming meta after that boundary, or (b) immediately at the `mc.*` edge, resolving `str` once.

`asMeta` on `cgmMeta` query methods (default varies by method):

- `asMeta=True`: meta instance(s). `cgmObject` / `cgmNode` hierarchy getters (`getParent`, `getParents`,
  `getSiblings`, `getChildren`, `getDescendents` / `getAllChildren`, `getShapes`, `getListPathTo`) always query
  Maya with `fullPath=True` via `_hierarchyQueryFullPath`; don't pass `fullPath=True` just for meta resolve.
- `asMeta=False`: DAG `str`; the `fullPath` kw controls short vs long (e.g. `getAllChildren` defaults short,
  `getChildren` long).

Meta in the middle; `str` only at `mc.*` / MEL.

## msgList patterns

Use message lists on meta for ordered, persistent collections of scene nodes. Canonical API:
[`Feature_CgmMetaAPI.md`](../../Features/Feature_CgmMetaAPI.md) (Indexed lists, `msgList_*`); implementation in
`cgm_Meta.py` -> `attribute_utils`.

| Use msgList for | Instead of |
|-----------------|------------|
| Setup owns N chains, hair systems, targets, locs, follicles | `chain_0`...`chain_N` name parsing, outliner scans, `self._chains = ['\|foo', ...]` |
| Ordered pipeline (connect/bake/rebuild by index) | Unordered set / dict without index attr |
| Back-link from child to owner (setup, segment curve, block) | Guessing parent from the DAG |

Single optional link -> `getMessage` / `getMessageAsMeta` / `connectChildNode`. Serialized list attrs without
live messages -> `datList_*`.

- **Read:** `ml_* = mOwner.msgList_get('chain') or []` (default `asMeta=True`).
- **Write:** `msgList_connect`, `msgList_append`, `msgList_remove`, `msgList_purge`, `msgList_clean` on the holder
  meta (or `ATTR.msgList_*` with `.mNode` when only a `str` is available at a thin lib edge).
- **Index:** `msgList_index(attr, mChild)`; store `chainIndex` (or equivalent) on the child when UI needs it. See
  `chain_connect_to_setup` / `chain_sync_chain_index_attrs` in `dynamic_utils`.
- **connectBack:** when the child must know its owner, pass it on append. Match existing child attr names
  (`owner`, `puppet`, `block`, ...); grep callers before inventing one.

```python
mSetup.msgList_append('chain', mGrp.mNode, connectBack='owner')
mSegmentCurve.msgList_append('ikHandles', mIKHandle.mNode, connectBack='segmentCurve')
```

- **Rebuild / artist deletes:** call `msgList_clean(attr)` on the holder (drops dead slots) before
  `msgList_append` / `msgList_connect`. Indices may not be dense after outliner deletes
  (`chain_connect_to_setup` cleans `chain` before re-wiring).
- Don't keep a second Python-only list beside a msgList (e.g. `mHairSystems`) that can drift, and don't use
  `listRelatives` / `listConnections` to discover members a msgList already stores.

Examples in tree: `chain` on a `cgmDynFK` setup (per-chain grp, `connectBack='owner'`); `mHairSystems` (registered
hairSystem shapes); `mTargets` / `mLocs` / `mObjJointChain` on a chain grp; `mMeshFollicles` / `mRivets` /
`mUvPins` on a cloth-attach chain grp.

## Meta API reference and mClass approval

- Inventory: [`Feature_CgmMetaAPI.md`](../../Features/Feature_CgmMetaAPI.md); source: `cgm/core/cgm_Meta.py`.
  `cgmNode` is for non-transform nodes (shapes, networks); `cgmObject` is the transform default (joints, groups,
  rig DAG). Shared: `p_nameShort` / `p_nameLong`, messages, `msgList_*`, `getMessageAsMeta`, `connectChildNode`;
  hierarchy / `p_parent` on `cgmObject` only. When unsure a capability exists, read that file and nearby callers
  instead of assuming.
- **Do not add new methods on registered `mClass` subclasses** (`cgmDynFK`, `cgmRigBlock`, `cgmObject`
  subclasses in `mrs/`, `rig/`, ...) or call new `mObj.<method>()` you just invented, unless the user explicitly
  asked for that meta-class API. Using existing methods (`p_parent`, `msgList_get`, `getMessageAsMeta`, ...) is
  required practice.
- Default for new behavior: a `lib/` or `rig/` module function whose first arg is `mObj` / `mDynFK`
  (e.g. `RIGDYN.chain_set_name(mDynFK, ...)`).
- If the user approves an `mClass` change, tell them to run `import cgm.core as CGM; CGM._reload()` before
  expecting new behavior (reload mechanics: [`reload.md`](reload.md)).
- Detail: [`Feature_CgmMetaAPI.md`](../../Features/Feature_CgmMetaAPI.md) (Session reload and agent policy).
