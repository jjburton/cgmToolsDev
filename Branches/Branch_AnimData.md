# Branch: jburton/animData

## Quick Info
**Status**: Active  
**Created**: August 25, 2026  
**Last Updated**: September 1, 2026 (capture/dest wrap to meta)  
**PR**: Pending

## Goals
Ship lossless Maya animation clips as `cgmAnimClip` (cgmDat JSON): nested clip → object → channel → curve → key, then capture, apply, and match in later phases. **Phase 0** is the Dat window stub. **Phase 1** is the curve round-trip gate. **Phase 2a/2b/2c** capture range + relative times + unkeyed boundary samples. **Phase 3** Paste Clip writes Replace/Merge/Insert. **Phase 4** Pose mapping. Dest list is the Maya selection, or global Name when empty. **mrsAnimClip** is the MRS context tool (PoseManager chrome; capture and paste dests). **Phase 5** clip file is the clipboard (File Save/Load). **Phase 6** paste onto Base or a specified animLayer. Trim / retime / clip-math mirror, library, and Animate time context are Later.

Canonical contract: [`Feature_AnimData.md`](../Features/Feature_AnimData.md).

## Related Documentation
- **[Feature_AnimData.md](../Features/Feature_AnimData.md)** - Canonical design contract (phases, schema, Phase 1 gate, Phase 2a capture)
- **[animClip_dat.py](../../repos/cgmToolsPy3/cgm/core/lib/animClip_dat.py)** - `AnimClip` + Dat UI
- **[animClip_curve.py](../../repos/cgmToolsPy3/cgm/core/lib/animClip_curve.py)** - curve snapshot / rebuild / capture helpers
- **[cgm_Dat.py](../../repos/cgmToolsPy3/cgm/core/cgm_Dat.py)** - `CGMDAT.data` / `CGMDAT.ui` base
- **[MRSDat.py](../../repos/cgmToolsPy3/cgm/core/mrs/MRSDat.py)** - Dat subclass pattern
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format
- **[Feature_MRSWiring.md](../Features/Feature_MRSWiring.md)** - puppet/module `controls_get` (used via `animate_utils.context_get`)
- **[mrsAnimClip.py](../../repos/cgmToolsPy3/cgm/core/mrs/mrsAnimClip.py)** - MRS subclass of `animClip_dat.ui`
- **[Feature_CgmToolUI.md](../Features/Feature_CgmToolUI.md)** - pinned chrome above scroll
- **[NewFeature_Guide.md](../Guides/NewFeature_Guide.md)** - Feature documentation format

## Timeline

### September 1, 2026 - Wrap capture/dest nodes as meta
**What**: Capture and dest lists wrap via `cgmMeta.validateObjArg`. Long names are `mObj.p_nameLong`. Selected shapes use `mObj.getParent(asMeta=True)` instead of `mc.ls` / `listRelatives`.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `_as_transform_meta`, `_normalize_nodes`, `_selected_transforms`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip / mrsAnimClip; capture a control (and a shape) to confirm longs

---

### August 31, 2026 - mrsAnimClip (MRS context wrapper)
**What**: Separate tool — PoseManager context chrome pinned above inherited cgmAnimClip UI. Context fills capture nodes and paste dests. Same `_ext` / `_startDir`. Empty context warns (no global Name). Do not add a Dest dropdown to cgmAnimClip. Context **mirror** = extra controls in the pool, not clip-math mirror. `animClip_dat.py` still must not import `Animate.py`.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `get(nodes=)`, `apply(dests=)`, `_clip_*` hooks, `uiBuild_pinned_chrome`
- NEW: `cgm/core/mrs/mrsAnimClip.py`
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `mrsANIMCLIP`
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — Toolbox MRS next to mrsPoser
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — `get(nodes=)` / `apply(dests=)` / `dests=[]`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Maya-verified — context Capture/Paste; empty context warns; cgmAnimClip still selection/Name; shared clip files

---

### August 31, 2026 - Layer picker New + Override/Additive
**What**: Layer menu includes **New** (prompt for a name; do not store New in the optionVar). **Override / Additive** enum is applied only when `ensure_anim_layer` creates the layer. Existing layers keep their mode. Not clip additive math.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `ensure_anim_layer(..., override=)`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — New + kind menus; `AnimClip.apply(layerOverride=)`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_AnimData.md`

**Status**: Maya-verified — New prompts; Override vs Additive on create; paste onto that layer

---

### August 31, 2026 - Layer paste: add dests then key preferred layer
**What**: Paste onto a named animLayer was succeeding without putting dest controls on the layer, so keys did not drive the rig. Apply now adds dests (`addSelectedObjects`), verifies membership (`SEARCH.animLayer_contains`), prefers the layer, and keys it. Do not use `setKeyframe -animLayer`.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `anim_layer_add_nodes`, `anim_layer_ensure_plug`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.apply` adds dests before keying
- EXTENDED: `cgm/core/lib/search_utils.py` — `animLayer_contains` (optional attr)
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Maya-verified — dests are layer members and keys drive the rig when the layer is unmuted

---

### August 31, 2026 - Phase 6 paste to animLayer
**What**: Apply **Layer** is `Base` or a scene animLayer. Named layers are created if missing. `apply_to_plug(..., animLayer=)` prefers that layer so Replace/Merge/Insert hit it. Dest list / Mapping unchanged. Blend drivers are allowed when pasting onto a layer.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `ensure_anim_layer`, `apply_to_plug` `animLayer`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.apply(layer=)`; Apply Layer menu
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Maya-verified — Layer menu; Paste onto a named layer vs Base

---

### August 31, 2026 - Phase 5 done: clip file is the clipboard
**What**: Cross-scene copy/paste is File Save / Load / Recent. Capture in one scene, Load in another, Paste. No separate in-memory copy buffer. Dedicated Copy button is optional Later UX.
**Files**:
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Maya-verified — Phase 6 is next

---

### August 31, 2026 - Plan Phase 6 paste to animLayer
**What**: After Phase 5, Apply can target **Base** (current) or a **specified Maya animLayer**. Dest list / Mapping unchanged. Not flatten-on-capture, not additive mix, not retarget.
**Files**:
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Plan only — Phase 5 clipboard is trusted (File Save/Load). Implement when starting Phase 6.

---

### August 31, 2026 - Maya verify dest list and Check Mapping
**What**: Dest list (selection vs empty-sel Name) and Check Mapping `[x]` on misses verified in Maya.
**Status**: Maya-verified

---

### August 31, 2026 - Check Mapping miss prefix
**What**: Unmatched CLIP CONTENTS object frames prefix `[x]` (`[x] src  →  --`). Hits stay `src → dest`. Display-only — do not parse the prefix back to data. Status still reports `N/M matched | missed`.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `uiUpdate_clip`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; Check Mapping with some dests missing

---

### August 31, 2026 - Dest list: selection or global Name
**What**: Dest list is the Maya selection as-is (no DAG descendents). Empty selection falls back to global Name. `Name` with a selection only matches among those dests. Removed Dest dropdown, `destMode`, and MRS puppet walk (Later context). Pose pairing stays Red9.
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Code complete — reopen cgmAnimClip; select dests or deselect for Name map; Check Mapping

---

### August 31, 2026 - Dest Selection vs MRS
**What**: Puppet walk is no longer silent inside Red9 mapping. Apply **Dest** is `Selection` (sel + DAG kids) or `MRS` (`controls_get` + `moduleSet`). `metaData` / `stripPrefix` / `mirrorIndex` stay Red9 on that list.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; Dest MRS + dest master for root-select; Dest Selection + dest controls for Red9-only

---

### August 30, 2026 - MRS dest pool from root; mirrorIndex_ID
**What**: Dest pool adds MRS puppet controls from a selected master/root (`puppet` / `rigNull` → `controls_get` + each `moduleSet.getList()`, same as Animate puppet context). DAG descendents stay as well. `mirrorIndex_ID` uses `MirrorHierarchy.getMirrorIndex` (slot only); `matchNodeLists` never implemented `_ID`.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; Check Mapping with dest master/root; mirrorIndex_ID with dest selected

---

### August 30, 2026 - Plan MRS Animate context (4b / Later)
**What**: After Phase 4 Maya verify, **4b** is dest-pool only (selected node → puppet/module → `controls_get`; `mrs/lib`, not `Animate.py` into `animClip_dat`). Not Phase 5. **Later** is the full Animate context row (control / part / puppet / scene + children / siblings / mirror) and capture-from-context. Context is runtime — no `mPuppet` on the clip JSON. DAG descendents stay the stand-in until 4b.  
**Files**:
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Status**: Plan only — do not implement until Phase 4 Check Mapping is trusted

---

### August 30, 2026 - metaData maps dest roots and leftover controls
**What**: Pose dest pool is the selection plus `TRANS.descendents_get` (select a puppet/root). `metaData` matches stored Red9 `{metaAttr, metaNodeID}`, then live wires if the source is still in the scene, then stripPrefix for leftover controls (PoseSaver). Capture stores that map plus `cgmDirection`.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; Check Mapping with dest root or dest controls

---

### August 28, 2026 - CLIP CONTENTS full-width rows and lighter zebra
**What**: Object frames parent directly to the CLIP CONTENTS inner column (`adj=True`) so they stretch full width. Zebra is even `guiButtonColor` / odd `guiBackgroundColor` — both lighter than the CLIP CONTENTS `guiHeaderColor` bar.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip

---

### August 28, 2026 - CLIP CONTENTS collapsible
**What**: CLIP CONTENTS is its own collapsible frame inside Current Clip (`animClip_contentsFrameCollapse`). Header shows `CLIP CONTENTS (N)`. Rebuild clears the inner column only so collapse state is kept.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip

---

### August 28, 2026 - ANIMCLIP unittest fixes
**What**: `AnimClip.__init__` uses `super()` so a module reload does not break `test_json_file_roundtrip`. Infinity skip tests set `preInfinity` / `postInfinity` on the curve with `setAttr` (`setInfinity` on a driven curve was a no-op, so Start/End still sampled).  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — rerun Toolbox Unittesting → coreLib → ANIMCLIP

---

### August 28, 2026 - Check Mapping preview
**What**: Apply **Check Mapping** runs the current Mapping through `_match_destinations` and shows clip → dest without writing keys. Status reports matched/missed. CLIP CONTENTS labels stamp `src → dest` (or `--`). Per-row Sel is still the captured node in the scene. Preview is UI-only (cleared on Capture / Load / Clear).  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `_preview_mapping`; Check Mapping button
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — preview does not paste
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; select dest; Check Mapping

---

### August 28, 2026 - Capture and paste progress bar
**What**: `AnimClip.get` / `apply` drive Maya’s main progress bar (`CGMUI.doStartMayaProgressBar`). Capture steps per selected object; paste per clip channel. Esc cancels; partial results stay. No bar when `$gMainProgressBar` is missing (batch / tests).  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip

---

### August 28, 2026 - Set Slider and clip contents zebra
**What**: Current Clip **Set Slider** sets the playback range to Paste at frame plus clip duration (`sourceEnd − sourceStart`). Duration 0 stays a single frame. Scene range expands if needed. CLIP CONTENTS object frames alternate `guiBackgroundColor` / `guiHeaderColor` (`MATH.is_even`), same even/odd gray as AnimFilters.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CgmToolUI.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip

---

### August 28, 2026 - Clip header namespace
**What**: Captured object `shortName` / `longName` are stored without Maya namespace (`NAMES.get_base`). Clip header `namespace` holds the source ns (`;`-joined if mixed). Name mapping tries `ns:short` then unique short. Per-object `namespace` is no longer written.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip; capture a namespaced control

---

### August 26, 2026 - Phase 4 Pose matching
**What**: Mapping menu adds PoseManager methods. `base` / `stripPrefix` / `metaData` / `mirrorIndex` / `mirrorIndex_ID` call `r9Core.matchNodeLists` against the current selection. Auto / Name / Index unchanged. No new matcher; Red9 files untouched. metaData and mirror methods need captured nodes still in the scene.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `_match_pose_destinations`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — stripPrefix paste
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Dest pool is the selection (same as Pose load onto chosen nodes)
- Our Index stays selection-order zip, not Red9 poseDict ID index

**Status**: Code complete — reopen cgmAnimClip; select dest; Mapping stripPrefix

---

### August 26, 2026 - Paste at frame defaults to slider start
**What**: Apply **Paste at frame** field (and `AnimClip.apply` when `atFrame` is omitted) uses the playback slider min, not current time. Same `SEARCH.get_time('slider')` as Capture Start.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Status**: Code complete — reopen cgmAnimClip

---

### August 26, 2026 - Key start/end capture option
**What**: Boundary samples are no longer always on. Capture checkbox **Key start/end** (optionVar, off by default) passes `keyStartEnd` into `AnimClip.get()`. Clip stores the flag. Infinity skip still applies when the option is on.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `get(keyStartEnd=)`; Capture checkbox
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — default off; existing 2c tests pass `keyStartEnd=True`
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Decisions**:
- Opt-in so a range with no keys in Start/End stays empty unless requested

**Status**: Code complete — reopen cgmAnimClip

---

### August 26, 2026 - Phase 3 Insert
**What**: Insert paste opens a gap on dest.attr: keys strictly after the first pasted time shift by the clip span (`max–min` dest times), then clip keys write in. Merge-like (no cut, no infinity change). Replace/Merge unchanged.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `apply_to_plug` Insert; `_shift_keys_after`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.apply` no longer stubs Insert
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — insert at 20 shifts dest 30 → 40
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Ripple is per attribute on the dest object, not a named curve node
- Key at the insert time is not shifted (clip overwrites it); later keys move
- Do not wrap `ml_copyAnim` / `pasteKey`

**Status**: Code complete — reopen cgmAnimClip; Mode Insert; paste into a curve that has keys after paste-at

---

### August 26, 2026 - 2c skip non-constant infinity bounds
**What**: Do not bake a Start sample when the capture start is before the first key and `preInfinity` is not Maya `constant`. Same for End vs `postInfinity`. Interior unkeyed bounds still sample. Infinity stays on the curve payload.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `ensure_boundary_keys`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — pre/post infinity skip; interior cycle still samples
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`

**Decisions**:
- `constant` is Maya's default / "normal". Linear, cycle, cycleRelative, oscillate are not sampled in the extrapolation region.

**Status**: Code complete — reopen cgmAnimClip

---

### August 26, 2026 - Phase 2c unkeyed boundary samples
**What**: Capture inserts evaluated keys when Start/End are not already keyed, so a range of in-betweens still holds the motion at the clip edges. Samples use `getAttr(curve.output, time=)` on the curve already in hand (linear tangents). Does not `listConnections` or move `currentTime`.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `ensure_boundary_keys`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `get()` samples then slices
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — unkeyed 5–15 on a 0–20 linear curve
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Evaluate the capture curve node, not `SEARCH.get_anim_value_by_time` (that lookup misses `unitConversion`)
- Already-keyed bounds are left alone; `includeStatic` stays a later flag

**Status**: Code complete — reopen cgmAnimClip; capture a range with no keys on Start/End; paste should hold those values

---

### August 26, 2026 - Paste keys dest.attr (not named curves)
**What**: Paste Clip was writing onto captured animCurve node names (`pSphere1_translateX`). Maya `cutKey`/`setKeyframe` treat those as DAG objects and fail. Apply now matches the dest transform, then keys each stored attr on that object.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `apply_to_plug` replaces `apply_to_curve`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.apply` keys dest.attr
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — paste onto unkeyed other object
- EXTENDED: `Features/Feature_AnimData.md`, `Features/Feature_CoreLibLookups.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Capture still snapshots the curve node (past unitConversion). Apply never looks up `curve.nodeName`.
- Layers/blends still skipped via `ATTR.get_driver` on the dest plug.

**Status**: Code complete — reopen cgmAnimClip; Capture; Paste Clip onto the same or another object

---

### August 26, 2026 - Phase 3 Replace/Merge paste
**What**: Paste Clip writes keys at Paste at frame. Relative clips add `atFrame` to stored times. Replace cuts the dest window; Merge keeps other keys. Mapping is Name / Index / Auto (selection-count). Insert and Pose matching are not in this slice.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `apply_to_curve`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.apply`; File Paste Clip
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — paste at frame 50
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Tangents set by time so merge onto existing curves stays lossless
- Missing dest curve: `ATTR.set_keyframe` then `get_driver`
- Skip 2c so capture can be verified in Maya

**Status**: Code complete — Capture, Paste at a later frame, scrub to check values

---

### August 26, 2026 - Phase 2b relative time
**What**: After slicing to Start/End, capture subtracts Start from each key time so the clip starts at 0. `sourceStart` / `sourceEnd` stay the original Maya range. `relative` is True on captured clips. Phase 1 `from_curve` fixtures stay absolute. Boundary samples are not in this slice.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `offset_keys`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `get()` offsets after slice
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — relative times vs source range
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Decisions**:
- Clip-dict math next to `slice_keys`; not a new Maya lookup
- Apply (Phase 3) will add the paste-at frame to relative times

**Status**: Code complete — run ANIMCLIP unittests in Maya

---

### August 26, 2026 - Phase 2a range capture
**What**: Capture Animation / `AnimClip.get()` snapshots time-based curves on the selection over Start/End via `ATTR.get_keyed` + `ATTR.get_driver(skipConversionNodes=True)`. Keys outside the range are dropped. Layers and blends are skipped with a warning. Times stay absolute. Relative normalize and unkeyed boundary samples are not in this slice.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_curve.py` — `slice_keys`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `get()` fills `channels`; `reload_dependencies()`
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `ANIMCLIPDATui` reloads curve + dat, then `reload_dependencies()`
- EXTENDED: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py` — locator capture, range slice, unitConversion via get_driver
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`, `AGENTS.md`

**Features**:
- Selected transforms → identity + channels with curve dicts
- Start/End inclusive filter; no boundary samples
- CLIP CONTENTS shows per-channel key counts

**Decisions**:
- Reuse `ATTR.get_keyed` and `ATTR.get_driver(..., skipConversionNodes=True)` — no new channel/curve lookup
- Snapshot the curve node; skip layers / blends / any other non-time-curve driver
- `includeStatic` remains a clip flag; unkeyed values not stored yet
- Split Phase 2: 2a absolute capture now; 2b relative; 2c boundary samples

**Status**: Code complete — run ANIMCLIP unittests in Maya; Capture Animation on a keyed translate control

---

### August 26, 2026 - Phase 1 curve snapshot / rebuild
**What**: Time-based `animCurve*` ↔ dict ↔ new node, plus JSON fixture wrap. Capture still identity-only. Tests registered on the Toolbox Unittesting menu.  
**Files**:
- NEW: `cgm/core/lib/animClip_curve.py`
- EXTENDED: `cgm/core/lib/animClip_dat.py` — `AnimClip.from_curve`
- NEW: `cgm/core/tests/test_coreLib/test_ANIMCLIP.py`
- EXTENDED: `cgm/core/tests/cgmTests.py` — coreLib ANIMCLIP
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Features**:
- `snapshot` / `rebuild` / `compare` for TL/TA/TU/TT
- Absolute times; curve node is the source of truth
- One-curve clip JSON write/read in tests

**Decisions**:
- New lib module, not `anim_utils.py` and not `cgm_Dat.py`
- Rebuild does not connect to a plug
- Capture does not pull curves yet (Phase 2)
- Run tests: Toolbox Unittesting → Test Modules → coreLib → ANIMCLIP

**Status**: Code complete — run ANIMCLIP unittests in Maya

---

### August 26, 2026 - Phase 0 UI stub settled
**What**: Maya-iterated AnimClip Dat window is the Phase 0 stub. File bar is path-only; operational messages live on a Status row. Capture / Current Clip / Apply frames, mocap-style range, Bake Range-style Paste row. No footer Get/Apply. Horizontal scroll fixed without changing frame header chrome.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Features**:
- Capture: Set Timeline Range (Start/End + Slider / Sel / Scene), include static, Capture Animation (identity + range)
- Current Clip: summary + CLIP CONTENTS identity rows (0 curves)
- Apply: Paste at frame, Mode (Replace / Merge / Insert), Mapping (Auto / Name / Index), Paste Clip stub
- File Save / Load / Recent unchanged; Load/Save not duplicated in Apply
- Default window 560×700; keep larger `windowPref`

**Decisions**:
- Dat top bar is the loaded file, same as other cgmDat UIs
- Status row in the scroll is for Capture / Get / Paste text
- Range matches mocap bake (`uiFunc_updateTimeRange` + `SEARCH.get_time`); no Custom enum
- Apply row matches Bake Range (label | stretch | fields | action)
- Scroll children sit in one adjustable `CGMUITemplate` column (first-child `childResizable`; header text stays Dat chrome)
- Curves and Paste behavior wait for Phase 1 / 3

**Status**: Complete — Phase 0 UI stub; next is Phase 1 curve round-trip

---

### August 26, 2026 - Mocap range + Save/Load stretch
**What**: Capture range matches mocap bake (Set Timeline Range: Slider / Sel / Scene). Apply Save Clip / Load Clip stretch across the row like the old Get/Apply footer. CLIP CONTENTS still identity-only — curves are Phase 1.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Features**:
- `uiFunc_updateTimeRange` (same as mocap bake)
- Save/Load `MelHLayout` equal stretch
- CLIP CONTENTS header shows object count; nested frames rebuilt on capture

**Decisions**:
- No Custom range mode — edit Start/End directly, same as mocap
- Sel does not fall back to slider if the timeline has no highlight
- Per-control curve lists wait for Phase 1

**Status**: Code complete — reopen cgmAnimClip

---

### August 26, 2026 - Apply stub + range radios
**What**: Capture Range is radios (same on-change as the old option menu). Footer Get/Apply removed. New collapsible **Apply** section matching the paste-clip layout (Paste at frame, Mode, Mapping, Paste Clip; Save/Load + Ready.). Paste Clip is a Phase 3 stub.  
**Files**:
- EXTENDED: `cgm/core/lib/animClip_dat.py`
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Features**:
- Range radios: Timeline / Playback / Scene / Custom → `uiFunc_capture_range_changed`
- Apply frame: optionVars for mode/mapping; Paste Clip warns only
- Save Clip… / Load Clip… in Apply call existing Dat saveAs/load

**Decisions**:
- Get lives on Capture Animation (status row still Get)
- Scroll attaches to cgm footer like other Dat windows (no bottom button row)
- Mode / Mapping stay option menus; only Range switched to radios

**Status**: Code complete — reopen cgmAnimClip; radios fill Start/End; Paste Clip logs Phase 3

---

### August 25, 2026 - Phase 0 cgmDat UI stub
**What**: Stubbed AnimClip Dat window on the same chrome as other cgmDat UIs (status row, File Save/Load/Recent, CLIP kv rows, OBJECTS list, footer). Get stores identity stubs only. Capture/Apply disabled.  
**Files**:
- NEW: `cgm/core/lib/animClip_dat.py` — `AnimClip` JSON Dat + `ui(CGMDAT.ui)`
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — `ANIMCLIPDATui`
- EXTENDED: `cgm/core/tools/toolbox.py` — Anim tab **cgmAnimClip**
- EXTENDED: `cgm/core/tools/lib/tool_chunks.py` — **cgm → Anim → cgmAnimClip**
- EXTENDED: `Features/Feature_AnimData.md`, `Branches/Branch_AnimData.md`

**Features**:
- JSON Dat shell (`cgmAnimClip`, `_startDir` `cgmDat/anim`)
- CLIP section: labeled stretch rows (version, scene, units, range, includeStatic, counts)
- CAPTURE / Current Clip: collapsible frames; clip summary + CLIP CONTENTS expand rows
- OBJECTS section: index + name + channel count; Select Source / Sel by list index
- Get from selection → object identity, empty channels
- File IO inherited from `CGMDAT.ui`

**Decisions**:
- UI lives with the Dat class (same as `MRSDat.uiBlockDat`)
- Launch from Toolbox **Anim** and Maya **cgm → Anim** (not WIP Tools; not merging until ready)
- Empty `__init__` does not fill a clip dict so last-file auto-load still works
- Do not inherit base `uiUpdate_data` pprint-key buttons

**Status**: Code complete — open Toolbox Anim → cgmAnimClip; Get selection; Save/Load JSON

---

### August 25, 2026 - Phase 1 contract (planning pass)
**What**: Reviewed the AnimClip vision and shrank Phase 1 so schema, Maya curve IO, and clip capture/apply are not mixed. Docs only; no Python.  
**Files**:
- EXTENDED: `Features/Feature_AnimData.md` — purpose, phases, schema sketch, metadata vs required, round-trip gate
- EXTENDED: `Branches/Branch_AnimData.md`
- EXTENDED: `AGENTS.md` — item 14 points at the contract (no longer TBD)

**Features**:
- Frozen nested schema; Phase 1 implements one `animCurve*` ↔ dict ↔ node
- JSON Dat (`cgmAnimClip`), not ConfigObj
- Absolute Maya times in Phase 1; relative time is Phase 2

**Decisions**:
- Capture the curve node, not the plug (unitConversion / layers)
- Identity fields as stubs; Red9 `matchMethod` is Phase 4
- Boundary motion is Phase 2 capture policy
- Do not grow `cgm_Dat.py`; curve IO in `cgm/core/lib/`; Dat subclass `animClip_dat.py` (or `AnimDat.py`)
- Do not wrap `ml_copyAnim` or Maya `.anim`

**Status**: Complete — contract in feature doc; code still TBD

---

### August 25, 2026 - Branch and feature stubs
**What**: Stood up empty branch and feature docs so later planning has a home. No code.  
**Files**:
- NEW: `Branches/Branch_AnimData.md`
- NEW: `Features/Feature_AnimData.md`
- EXTENDED: `AGENTS.md` — item 14 AnimData design contract

**Features**:
- Planning stubs only

**Decisions**:
- Feature filename `Feature_AnimData.md`; git branch `jburton/animData`
- No `Plans/` doc this pass

**Status**: Complete — stubs in place; superseded by Phase 1 contract entry above

---

## Deliverables

### Planning
- [x] Flesh out AnimData goals and scope
- [x] Fill feature architecture, files, and testing sections
- [x] Break work into phases on this branch

### Phase 0 — cgmDat UI stub
- [x] `AnimClip` JSON Dat shell + `CGMDAT.ui` subclass
- [x] Get from selection (identity stubs, no curves)
- [x] Toolbox Anim → cgmAnimClip launcher
- [x] Maya: open UI, Capture Animation, Save/Load, Paste Clip stub warns

### Phase 1 — Data model + curve foundation
- [x] `AnimClip` Dat subclass (`_ext` `cgmAnimClip`, `_dataFormat` `json`) — shell in Phase 0
- [x] Curve + key dict snapshot / rebuild (time-based `animCurve*` only)
- [x] Identity field stubs on object records (no matching) — Get in Phase 0
- [x] Maya round-trip tests (linear/spline/stepped/auto, weighted, breakdown, infinity, TL+TA, single key)
- [x] JSON file round-trip of a fixture clip

### Phase 2 — Clip capture
- [x] Selection + frame range (2a: drop keys outside Start/End)
- [x] Relative / normalized times
- [x] Evaluate start/end if unkeyed (boundary motion)

### Phase 3 — Apply
- [x] Apply at destination frame (Replace / Merge)
- [x] Insert

### Phase 4 — Matching
- [x] Reuse PoseManager match methods

### Phase 4b — Dest list
- [x] Dest list = Maya selection, or global Name when empty (no Dest menu, no DAG/MRS walk)
- [x] Check Mapping: unmatched CLIP CONTENTS rows prefix `[x]`

### Phase 5 — Copy/paste
- [x] Cross-scene copy/paste (clip file is the clipboard — File Save / Load / Recent)

### Phase 6 — Paste to animLayer
- [x] Apply **Layer**: Base (current) or a specified Maya animLayer
- [x] Replace / Merge / Insert write that layer’s curves; dest list / mapping unchanged
- [x] Create layer if missing; not flatten-on-capture; not additive mix math; not retarget

### mrsAnimClip
- [x] PoseManager context chrome pinned above inherited Capture / Clip / Apply
- [x] Context for capture and paste dests; empty warns (no global Name)
- [x] Shared `_ext` / `_startDir`; Toolbox MRS next to mrsPoser

### Later
- [ ] Trim / retime / clip-math mirror
- [ ] Library / browser
- [ ] Animate time context (back / next / bookEnd)
- [ ] Additive / retarget
- [ ] `includeStatic` capture of unkeyed static values
- [ ] Anim-layer flatten on capture (if ever)

### Testing
- [x] Phase 1 Maya round-trip gate
- [x] Documentation updated
- [x] Maya testing complete (dest list + Check Mapping `[x]`)
- [x] Maya testing complete (mrsAnimClip context capture/paste vs cgmAnimClip sel/Name)

---

## PR Notes

### TBD (Later)

#### Overview
Phase 0–6 + mrsAnimClip ship. **cgmAnimClip** dest list is selection or global Name. **mrsAnimClip** uses PoseManager context for capture and paste dests (shared clip files). Clip file is the clipboard (File Save/Load). Paste targets Base or a specified animLayer. Trim / retime / clip-math mirror, library, and Animate time context are Later. Capture still skips layer/blend drivers until flatten-on-capture (Later).

#### Next Steps
- Later: trim / retime / clip-math mirror; library; Animate time; `includeStatic`; optional Copy button

---

**Ready for Review** - Not yet. Later trim / library / Animate time still open.

---

## Notes

### Architectural Patterns Established
- Schema frozen early; behavior phased
- Dat subclass + UI in `cgm/core/lib/animClip_dat.py`
- File bar vs Status row; mocap Set Timeline Range; Bake Range Apply row
- Scroll: one adjustable column on `CGMUITemplate` so frames keep header chrome and do not force a horizontal bar

### Lessons Learned
- Mixing capture/apply into the first curve round-trip would make tests dishonest
- `scrollLayout` `childResizable` only sizes the first child; extra frames as siblings cause a horizontal scrollbar
- Parenting those frames under `cgmUISubTemplate` changes collapsible header text color; keep the wrap on `CGMUITemplate`

### Future Considerations
- See feature doc Later phase

---

*Last Updated: August 31, 2026*  
*Branch Status: Active*
