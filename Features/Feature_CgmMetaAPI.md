# cgmMeta API scope (dev reference)

Living inventory of **`cgm/core/cgm_Meta.py`** (~6k lines) and closely related **`cgmMeta.*`** subclasses elsewhere. Source of truth for behavior remains the py3 module; this doc is for navigation and agent/human onboarding.

**Related rules:** **`cgm-runtime-meta-not-strings`**, **`maya-cmds-strings-only`**, draft **`cgm-meta-naming-hierarchy`** (`m*` / `ml_*` / `md_*`).

**Revision:** 2026-09-14 — initial scope pass from `cgm_Meta.py` + registry grep.

---

## Architecture

```mermaid
flowchart TB
  R9[Red9 MetaClass]
  N[cgmNode]
  O[cgmObject]
  C[cgmControl]
  subgraph core_meta [cgm_Meta.py]
    N --> O --> C
    N --> OS[cgmObjectSet]
    N --> BN[cgmBufferNode]
    N --> BS[cgmBlendShape]
    N --> CO[cgmController]
    OV[cgmOptionVar]
    CA[cgmAttr]
    NF[NameFactory]
  end
  R9 --> N
  subgraph elsewhere [registered mClass subclasses]
    DFK[cgmDynFK]
    DPG[cgmDynParentGroup]
    RB[cgmRigBlock / Puppet / Module ...]
  end
  O --> DFK
  O --> DPG
  O --> RB
```

| Layer | Role |
|--------|------|
| **Red9 `MetaClass`** | `mNode`, node cache, message graph UI, **`disconnectChild`**, **`delete`**, attr/message helpers not reimplemented in cgm |
| **`cgmNode`** | cgm attrs, messages, msgList/datList, naming, duplicate/loc, component mode |
| **`cgmObject`** | Transforms only: hierarchy via **`transform_utils`**, TRS/pivot/BB, constraints, grouping |
| **`cgmControl`** | Rig control: module/switch hooks, aim/mirror/controller tags |
| **Specialized nodes** | Sets, buffer lists, optionVars, per-attr wrapper **`cgmAttr`**, naming **`NameFactory`** |

End of file: **`r9Meta.registerMClassInheritanceMapping()`** — cgm classes join Red9’s **`mClass`** registry.

---

## Construction and validation

| Entry | Purpose |
|--------|---------|
| **`cgmMeta.cgmMetaFactory`** | **`__new__`**: create or wrap node → **`cgmObjectSet`** if objectSet, **`cgmObject`** if transform, else **`cgmNode`**. Reads **`mClass`** on node (full specialized routing still mostly “log and fall through”). |
| **`cgmMeta.asMeta(*args, sl=…)`** | List → **`validateObjListArg`**, else **`validateObjArg`**. Common UI/selection boundary. |
| **`validateObjArg` / `validateObjListArg`** | Normalize str/meta → instance; honor **`mType`**, node **`mClass`** in registry, **`default_mType`**, **`mayaType`**, **`setClass`**. Transforms default to **`cgmObject`**. |
| **`createMetaNode(mType, …)`** | Instantiate registered class by **`mClass`** string name. |
| **`reinitializeMetaClass(node)`** | Pop Red9 cache entry; re-wrap DAG node (use after reload / class change). |
| **`set_mClassInline` / registry** | Set or verify **`mClass`** attr; changing type after init → **`convertMClassType`** (Red9/cgm). |
| **`isTransform` / `getTransform`** | Thin wrappers → **`search_utils`** (not meta methods). |

**Identity on instances**

- **`mNode`** — current DAG path (Red9); use **only at `mc.*` edge**.
- **`p_nameShort` / `p_nameLong` / `p_nameBase`** — properties (aliases **`getNameShort`**, etc.).
- **`getShortName`**, **`getNameMatches`**, **`getReferencePrefix`**, **`getNameAlias`**, **`getNameDict`**, **`getCGMNameTags`** (legacy naming tags).
- **`cached`** — Red9: skip re-init when serving cached wrapper.
- **`__repr__`** — node short name + **`mClass`** when present.

**Component mode** (face/vtx-style handles): **`getComponent`**, **`isComponent`**, **`getComponents`**.

---

## `cgmNode` — all node types

Subclasses **`Red9_Meta.MetaClass`**. Network nodes, shapes used as nodes, etc. **Not** full transform hierarchy API (see **`cgmObject`**).

### Attributes and connections

| API | Notes |
|-----|--------|
| **`hasAttr`** | API + alias check; falls back to **`mc.objExists`**. |
| **`addAttr`** | cgm-aware create/convert; blocks referenced nodes. |
| **`doStore`**, **`doRemove`**, **`copyAttrTo`** | High-level attr storage patterns. |
| **`getMayaAttr` / `setMayaAttr` / `getMayaAttrString`** | Pass-through to attr layer. |
| **`getAttrs`**, **`resetAttrs`**, **`setAttrFlags`**, **`verifyAttrDict`** | Bulk attr ops. |
| **`doConnectIn` / `doConnectOut`** | Connection helpers with optional transfer/lock. |
| **`isAttrKeyed`**, **`isAttrConnected`**, **`getEnumValueString`** | Query helpers. |
| **`__setMessageAttr__`** | Overload: cgm **`ATTR.set_message`** unless **`ignoreOverload`**. |

### Message links (single)

| API | Notes |
|-----|--------|
| **`connectChildNode` / `connectParentNode`** | **`ATTR.set_message`**; accepts meta (uses **`.mNode`**). |
| **`connectChildrenNodes`** | Multi-child message connect. |
| **`getMessage(attr, asMeta=…, …)`** | Returns strings or meta per flag. |
| **`getMessageAsMeta(attr, asList=False)`** | Preferred rig read when you want instances. |

**Red9:** **`disconnectChild(node, attr=…)`** — not named **`disconnectChildNode`** in Red9; some rig code calls **`disconnectChildNode`** (verify at runtime / align naming with **`disconnectChild`**).

### Indexed lists on node (`msgList_*`, `datList_*`)

Parallel APIs for **message-linked lists** vs **datList** (serialized list attrs).

| Pattern | msgList | datList |
|---------|---------|---------|
| connect | **`msgList_connect`** | **`datList_connect`** |
| get | **`msgList_get`** — default **`asMeta=True`** | **`datList_get`** |
| mutate | append, index, remove, purge, clean, exists | same set |
| temp | **`msgList_getMessage`** | — |

Implementation delegates to **`attribute_utils`** on **`self.mNode`**.

### Naming

| API | Notes |
|-----|--------|
| **`doName`**, **`doTagAndName`**, **`doCopyNameTagsFromObject`** | Scene naming / cgmName tags. |
| **`uiPrompt_rename`** | Artist rename prompt. |
| **`stringModuleCall(module, func, …)`** | MEL-style dispatch into another module with **`self`** context. |

### Scene ops (any node)

| API | Notes |
|-----|--------|
| **`doLoc`**, **`doDuplicate`**, **`doOverrideColor`** | Locator, duplicate, color override. |
| **`getMayaType`** | Node type string. |
| **`getPosition` / `getPositionOLD`**, **`getDag` / `getTransform`** | Position / transform resolution (**`getDag(asMeta=True)`** → **`cgmObject`**). |
| **`getPositionOutPlug`** | World position plug; optional meta. |

### Hierarchy on `cgmNode` (limited)

| API | Notes |
|-----|--------|
| **`getParent(asMeta=False)`** | **`TRANS.parent_get`** — **read-only** property **`p_parent` / `parent`** (no setter on **`cgmNode`**). |
| **`getSiblings(asMeta=False)`** | Siblings via transform utils. |

**Important:** Parent **assignment** for transforms is on **`cgmObject.p_parent`** (**`doParent`** → **`TRANS.parent_set`**), not on bare **`cgmNode`**.

---

## `cgmObject` — transforms and joints

**`__init__`:** default transform; **`nodeType='joint'`** creates a joint. Requires **`VALID.is_transform`**.

### Hierarchy (prefer in rig/tool logic)

| API | Default / notes |
|-----|------------------|
| **`getParent(asMeta=False, fullPath=True)`** | **`cgmObject`** when **`asMeta=True`**. |
| **`p_parent` / `parent`** | **get + set** — **`doParent`** / **`TRANS.parent_set`**. |
| **`getParents`**, **`getSiblings`** | Ancestor chain / same-level siblings. |
| **`getChildren`**, **`getDescendents` / `getAllChildren`** | Filter by **`type`** (default transform). |
| **`getShapes`**, **`getListPathTo(target)`** | Shape list; path between nodes. |
| **`isParentTo`**, **`isChildTo`**, **`isVisible`** | Relationship / visibility checks. |

### Transform, pivot, bounding box

**`doSnapTo`**, **`doAim`**, **`doAimAtPoint`**, **`setPosition`**, **`getPositionAsEuclid`**, **`getOrient` / `setOrient`**, rotate axis/pivots, **`getBBSize` / `getBBCenter`**, axis vectors, world matrix, transform point/direction (incl. inverse), **`dagLock`**, **`getTransformAttrs`**, **`getPositionOutPlug(autoLoc=True)`**, **`getDeformers`**, **`doCopyPivot`**, **`doMatchTransform`**.

### Grouping and creation

**`doGroup`**, **`doCreateAt`** — null/group at self; optional **`setClass`**, connect-as patterns.

### Constraints

**`getConstraintsTo` / `From`**, **`getConstrainingObjects`**, **`getConstraintsByDrivingObject`**, **`isConstrainedBy`**.

---

## Other classes in `cgm_Meta.py`

| Class | Base | Purpose (summary) |
|--------|------|-------------------|
| **`cgmController`** | **`cgmNode`** | Controller network; **`parent_set` / `parent_get`**, **`purge`**, **`pickWalk`**, **`index_get`**. Factory helper **`controller_get`**. |
| **`cgmControl`** | **`cgmObject`** | Rig control: **`_hasModule`**, **`_hasSwitch`**, **`controller_get`**, group locks, **`doAim`**, mirror tags (**`_verifyMirrorable`**, **`doMirrorMe`**, push to mirror), **`controlTags_*`**. |
| **`cgmObjectSet`** | **`cgmNode`** | Maya set as meta: QSS, set type, **`getList` / `getMetaList`**, **`append` / `remove` / `extend`**, selection helpers, key/reset on members. |
| **`cgmOptionVar`** | (standalone) | Maya **`optionVar`** wrapper: get/set, type, append/remove, UI prompt, recent list helpers. |
| **`cgmBufferNode`** | **`cgmNode`** | Sequential **`item_N`** message/string storage: **`store`**, **`value`**, **`updateData`**, **`rebuild`**, purge/remove by index. |
| **`cgmAttr`** | (standalone) | Rich wrapper for one attr on a **`cgmNode`**: value, min/max, enum, connections, rename — large API (~1.2k lines). |
| **`NameFactory`** | (standalone) | Scene-wide cgm naming iteration (**`doNameObject`**, fast iterate, tag dict). |
| **`cgmBlendShape`** | **`cgmNode`** | Blend shape helper (also a duplicate class name in **`cgm_Deformers.py`** — use the one your caller imports). |
| **`pathList`** | (standalone) | OptionVar-backed path list UI helper. |
| **`cgmTest`** | **`MetaClass`** | Internal/test hook. |
| **`ModuleFunc`** | **`cgmFuncCls`** | Validates **`moduleInstance`** for module-scoped func wrappers. |

---

## Registered subclasses (outside this file)

These use **`mClass`** on the node and **`createMetaNode` / `validateObjArg(mType=…)`**:

| Module | Classes (sample) |
|--------|-------------------|
| **`cgm/core/cgm_RigMeta.py`** | **`cgmDynamicSwitch`**, **`cgmDynamicMatch`**, **`cgmDynParentGroup`** |
| **`cgm/core/rig/dynamic_utils.py`** | **`cgmDynFK`** |
| **`cgm/core/mrs/RigBlocks.py`** | **`cgmRigBlock`**, **`cgmRigBlockHandle`**, **`cgmRigPuppet`**, **`cgmRigMaster`**, **`cgmMasterNull`**, **`cgmRigModule`** |
| **`cgm/core/tools/lightLoomLite.py`** | **`cgmLight`**, **`cgmLightShape`** |

Extend this table when adding new **`mClass`** types.

---

## Red9 inherited behavior (not duplicated in cgm docstrings)

Use **`Red9/core/Red9_Meta.py`** for full detail. Typical calls in cgm codebases:

- **`delete()`**, **`deleteCall`**
- **`disconnectChild(node, attr=…)`** — message unlink
- Message / meta rig UI, **`getChildren`** meta rig walks (Red9 meta rig — distinct from **`cgmObject.getChildren`** DAG walk)
- Cache: **`RED9_META_NODECACHE`**, **`cached`**, dead-node cleanup in **`cgmNode.__repr__`**

Attr **get/set** on nodes often uses **`mObj.attrName`** or **`ATTR.get(mObj.mNode, …)`** patterns rather than a single **`getAttr`** on **`cgmNode`**.

---

## `asMeta` defaults cheat sheet

| Call | Typical default |
|------|------------------|
| **`msgList_get`** | **`asMeta=True`** |
| **`getMessage`** | check call — often string unless **`asMeta=True`** |
| **`getParent`** on **`cgmObject`** | **`asMeta=False`** (explicit **`True`** for rig steps) |
| **`getChildren` / descendents** | **`asMeta=False`** unless requested |

At **`mc.*`**: **`asMeta=False`**, **`.mNode`**, or **`p_nameLong`** — never pass meta instances into commands.

---

## Gaps and maintenance

- **`cgmMetaFactory`** does not fully branch on every **`mClass`** value yet (logs “specialized processing not implemented” in places).
- **`cgmNode.p_parent`** is read-only; assigning parent requires **`cgmObject`** (or **`TRANS.parent_set`** at lib boundary).
- When adding public meta methods, update this doc and any **`Feature_*`** contract that depends on the behavior.

**Primary code path:** `d:\Repos\cgmToolsPy3\cgm\core\cgm_Meta.py`
