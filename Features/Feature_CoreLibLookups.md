# Feature: Core lib lookups

Agent / dev index — **not** a product feature. Need → existing `cgm.core.lib` call. Do not list every `def`. Add a row when a search-first miss happens.

**Read this before** adding a helper that uses `mc.ls`, `listConnections`, `listAttr`, `keyframe`, or name-string hacks.

Old `cgm.lib` → `cgm.core` names live in [`Feature_LibToCore.md`](Feature_LibToCore.md). P4 write policy: [`Feature_PerforceIntegration.md`](Feature_PerforceIntegration.md).

**Aliases** (match nearby callers): `ATTR` `attribute_utils`, `NAMES` `name_utils`, `SEARCH` `search_utils`, `TRANS` `transform_utils`, `POS` `position_utils`, `CONSTRAINT` / `CONSTRAINTS` `constraint_utils`, `PATHUTIL` `path_utils`.

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
| Set a key | `ATTR.set_keyframe` |

### Names

| Need | Use |
|------|-----|
| Short / long / base DAG name | `NAMES.get_short` / `get_long` / `get_base` |
| On a cgm object | `mObj.p_nameShort` / `p_nameLong` |

### Time / search

| Need | Use |
|------|-----|
| Slider / selected / scene / current time | `SEARCH.get_time` |
| Key times on a node | `SEARCH.get_key_indices_from` |
| Channel Box selection | `SEARCH.get_selectedFromChannelBox` |
| Parent chain | `SEARCH.parents_get` / `SEARCH.get_all_parents` |

### DAG

| Need | Use |
|------|-----|
| Parent get / set | `TRANS.parent_get` / `parent_set` |
| Shapes | `TRANS.shapes_get` |
| Children / descendents | `TRANS.children_get` / `descendents_get` |

### Xform

| Need | Use |
|------|-----|
| World / local position | `POS.get` / `POS.get_local` |
| Rotate / orient | `TRANS.rotate_get` / `orient_get` |
| Rotate order | `TRANS.rotateOrder_get` |

### Constraints

| Need | Use |
|------|-----|
| Constraints on a node | `CONSTRAINT.get_constraintsTo` |
| Constraints from a node | `CONSTRAINT.get_constraintsFrom` |
| Constraint targets | `CONSTRAINT.get_targets` |

### Paths / P4 writes

| Need | Use |
|------|-----|
| Prepare a path for write | `PATHUTIL.prepare_path_for_write` |
| Scene meta sidecars | `PATHUTIL.prepare_meta_files_for_write` |
| FBX / export preflight | `PATHUTIL.preflight_export_output_paths` |

### Clip curves

Payload IO only: `animClip_curve.snapshot` / `rebuild` / `slice_keys`. Capture uses `ATTR.get_keyed` + `ATTR.get_driver` in the caller (`AnimClip.get()`). No new plug→curve lookup.
