# Feature: Core lib lookups

Agent / dev index — **not** a product feature. Need → existing `cgm.core.lib` call. Do not list every `def`. Add a row when a search-first miss happens.

**Read this before** adding a helper that uses `mc.ls`, `listConnections`, `listAttr`, `keyframe`, or name-string hacks.

Old `cgm.lib` → `cgm.core` names live in [`Feature_LibToCore.md`](Feature_LibToCore.md). P4 write policy: [`Feature_PerforceIntegration.md`](Feature_PerforceIntegration.md).

**Aliases** (match nearby callers): `ATTR` `attribute_utils`, `NAMES` `name_utils`, `SEARCH` `search_utils`, `TRANS` `transform_utils`, `POS` `position_utils`, `SNAP` `snap_utils`, `SKIN` `skin_utils`, `CONSTRAINT` / `CONSTRAINTS` `constraint_utils`, `PATHUTIL` `path_utils`, `TEXTURE` `texture_utils`.

Do **not** wrap these with names like `curve_from_plug` or `_candidate_attrs`.

---

### Attr / anim

| Need | Use |
|------|-----|
| Keyed attrs on a node | `ATTR.get_keyed` / `ATTR.is_keyed` |
| Driver of a plug (past `unitConversion`) | `ATTR.get_driver(..., skipConversionNodes=True)` |
| Driven plugs | `ATTR.get_driven` |
| Plug connected | `ATTR.is_connected` |
| Get / set attr | `ATTR.get` / `ATTR.set` |
| Attr exists | `ATTR.has_attr` |
| Set a key | `ATTR.set_keyframe` |

### Names

| Need | Use |
|------|-----|
| Short / long / base DAG name | `NAMES.get_short` / `get_long` / `get_base` |
| Namespace on a live DAG node | `NAMES.get_short` vs `get_base` (not `get_refPrefix` unless it is a reference) |
| On a cgm object | `mObj.p_nameShort` / `p_nameLong` / `p_nameBase` — wrap with `cgmMeta.validateObjArg` / `validateObjListArg` |

### Time / search

| Need | Use |
|------|-----|
| Slider / selected / scene / current time | `SEARCH.get_time` |
| Key times on a node | `SEARCH.get_key_indices_from` |
| Channel Box selection | `SEARCH.get_selectedFromChannelBox` |
| Selected animLayers | `SEARCH.animLayers_getSelected` |
| All scene animLayers | `SEARCH.animLayers_get` (root + children; `includeBase` for BaseAnimation) |
| Object / plug on an animLayer | `SEARCH.animLayer_contains` |
| Parent chain | `SEARCH.parents_get` / `SEARCH.get_all_parents` |

### DAG

| Need | Use |
|------|-----|
| Parent get / set | `TRANS.parent_get` / `parent_set` — on meta: `mObj.getParent(asMeta=True)` |
| Is a transform | `SEARCH.is_transform` |
| Shapes | `TRANS.shapes_get` |
| Children / descendents | `TRANS.children_get` / `descendents_get` |

### Xform

| Need | Use |
|------|-----|
| World / local position | `POS.get` / `POS.get_local` |
| Rotate / orient | `TRANS.rotate_get` / `orient_get` |
| Rotate order | `TRANS.rotateOrder_get` |
| World RP snap without rotateOrder convert | `SNAP.move_point_snap` / `move_orient_snap` — **not** `SNAP.go` |

### Constraints

| Need | Use |
|------|-----|
| Constraints on a node | `CONSTRAINT.get_constraintsTo` |
| Constraints from a node | `CONSTRAINT.get_constraintsFrom` |
| Constraint targets | `CONSTRAINT.get_targets` |

### Skin

| Need | Use |
|------|-----|
| First skinCluster on a mesh | `SKIN.get_cluster` |
| Copy closest-point weights source → target(s) | `SKIN.transfer_fromTo` — owns old zoo `transferSkinning`; do not import `cgm.lib.zoo.zooPyMaya.skinWeights` (Phase 2, Maya-verified) |

### Paths / P4 writes

| Need | Use |
|------|-----|
| Prepare a path for write | `PATHUTIL.prepare_path_for_write` |
| Scene meta sidecars | `PATHUTIL.prepare_meta_files_for_write` |
| FBX / export preflight | `PATHUTIL.preflight_export_output_paths` |
| Remap missing `file` texture paths onto project content/export | `TEXTURE.remap_missing` |
| Copy off-project textures next to the scene | `TEXTURE.localize` |

### Clip curves

Payload IO only: `animClip_curve.snapshot` / `rebuild` / `slice_keys` / `offset_keys` / `ensure_boundary_keys` / `apply_to_plug`. Capture uses `ATTR.get_keyed` + `ATTR.get_driver` in the caller (`AnimClip.get()`). `ensure_boundary_keys` runs only when clip option `keyStartEnd` is on. Boundary samples evaluate the curve already in hand (`getAttr(curve.output, time=)`); skip Start in the pre-infinity region when `preInfinity` is not `constant`, skip End in the post-infinity region when `postInfinity` is not `constant`. Do not use `SEARCH.get_anim_value_by_time` (it `listConnections` type animCurve and misses `unitConversion`). Apply matches the dest object, then keys `dest.attr` — do not resolve stored curve `nodeName`. Pose mapping (`base` / `stripPrefix` / `metaData` / `mirrorIndex`) is `r9Core.matchNodeLists`. Dest list is the Maya selection as-is, or a global Name map (`_scene_node_by_name`) when nothing is selected, unless `get(nodes=)` / `apply(dests=)` pass a list (empty dests = nothing). Capture and dest lists wrap via `cgmMeta.validateObjArg`; longs are `mObj.p_nameLong`; shapes use `mObj.getParent(asMeta=True)`. `Name` with a selection keeps hits only if they are in that list. No `TRANS.descendents_get` and no puppet `controls_get` inside `animClip_dat` — mrsAnimClip fills those lists via `animate_utils.dat.context_get`. `mirrorIndex_ID` is `MirrorHierarchy.getMirrorIndex` (PoseSaver) — `matchNodeLists` has no `_ID` path. `metaData` also compares stored Red9 `getNodeConnectionMetaDataMap` to dest wires, then stripPrefix (PoseSaver). Insert shifts later keys on that same plug with `mc.keyframe(..., relative=True, timeChange=)` — not a new lookup. Skip if `get_driver` is a non-time-curve (layers/blends) unless pasting onto a specified animLayer (`animBlend*` is allowed then). `apply_to_plug(..., animLayer=)` prefers that Maya layer (create if missing) so keys hit it instead of Base. No new plug→curve lookup.
