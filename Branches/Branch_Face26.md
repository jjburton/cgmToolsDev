# Branch: jburton/Face26

## Quick Info
**Status**: Active  
**Created**: September 1, 2026  
**Last Updated**: October 7, 2026 (TD toolbox/menu rig flags; Query distance status-line warnings; head neck ribbon; Builder scene-load; form `trackCrv`; handle proxy; puppet mesh)  
**PR**: Pending  
**py3 checkout**: `jburton/Face26` (`__BRANCH` = `FaceRigging26`, `__RELEASE` = `26.09.01.01`)

## Goals
Improve MRS facial block rigging — starting with **muzzle** lip follow/constraints and **eye** prerig parameter cleanup. Broader facial-block work (blockDat remapping when adding prerig handles, cheek controls, brow/face block parity) is in scope for this branch but not started yet. This branch also carries shared **MRS body** work used by face-adjacent rigs: **scaleSetup** dyn-parent defaults from **attachPoint**, pivot-result naming, and digit-limb ship bypass. MetaHuman solve / project-script work stays on [`Branch_UnrealWorkflow.md`](Branch_UnrealWorkflow.md) and [`Feature_Metahuman.md`](../Features/Feature_Metahuman.md) unless we deliberately factor helpers into py3.

## Related Documentation
- **[Feature_MRSMeshCreation.md](../Features/Feature_MRSMeshCreation.md)** — MRS proxy/puppet/skinned mesh contract (`meshBuild`, `proxyBuild`, batch post, geoGroup invariants)
- **[Feature_DynSimTool.md](../Features/Feature_DynSimTool.md)** — **cgmDynSimTool** dynFK / `.cgmSim*Dat` library, hair chain segment-length contract, connect/bake
- **[Feature_Metahuman.md](../Features/Feature_Metahuman.md)** — MetaHuman facial retarget / SDK transfer (Perforce `MetahumanFacial.py`; reference for facial solve patterns)
- **[Feature_MRSWiring.md](../Features/Feature_MRSWiring.md)** — module/puppet message graphs, block parent wiring
- **[Branch_Jan2026.md](Branch_Jan2026.md)** — prior muzzle handle / ribbon / face-handle work
- **[Branch_AnimData.md](Branch_AnimData.md)** — merged into Face26 (cgmAnimClip / mrsAnimClip; not Face26-native)
- **[Branch_SpringCleaning.md](Branch_SpringCleaning.md)** — merged into Face26 (`cgm.lib` → `cgm.core` migration)
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** — branch doc format
- **[muzzle.py](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/muzzle.py)** — primary iteration target
- **[eye.py](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/eye.py)** — eye / lid prerig
- **[block_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/block_utils.py)** — blockDat load/match (future non-destructive remap); **`form_segment`** (shared form + sub shapers); `block_proxy_mesh_flow`, `puppetMesh_create`, `puppetMesh_normalCheck`, `puppetMesh_colorGeo`; **`pivots_setup`** (parents **`pivotResult`** at end of pivot chain)
- **[puppet_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/puppet_utils.py)** — `proxyMesh_verify`, puppet-level `puppetMesh_create`
- **[batch_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/batch_utils.py)** — batch post rig; `resolve_build_output_path`
- **[blockShapes_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/blockShapes_utils.py)** — face handle creation (`mParent` contract)
- **[distance_utils.py](../../cgmToolsPy3/cgm/core/lib/distance_utils.py)** — `get_normalizedWeightsByDistanceToObj` (muzzle constraint weights)
- **[geo_Utils.py](../../cgmToolsPy3/cgm/core/lib/geo_Utils.py)** — `is_reversed`, `normalCheck` (proxy/puppet inside-out fix)
- **[curve_Utils.py](../../cgmToolsPy3/cgm/core/lib/curve_Utils.py)** — `polyline_length_fractions` (joint-length POC sampling on dynFK outCurve)
- **[dynamic_utils.py](../../cgmToolsPy3/cgm/core/rig/dynamic_utils.py)** — `cgmDynFK` / `chain_create_hair`, cloth attach, profile load
- **[simChain_dat.py](../../cgmToolsPy3/cgm/core/lib/simChain_dat.py)** — cgmSimHairDat / Cloth / Nucleus dat IO + dev library
- **[cgmDynFK_presets.py](../../cgmToolsPy3/cgm/core/presets/cgmDynFK_presets.py)** — `base` seed + script API (artist hair presets → `cgmDat/sim/hair/`)
- **[cgmNCloth_presets.py](../../cgmToolsPy3/cgm/core/presets/cgmNCloth_presets.py)** — `base` nc/n seed + script API (artist cloth/nucleus presets → `cgmDat/sim/`)
- **[face_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/face_utils.py)** — `fortniteMetaHuman` pose-buffer schema
- **[builder_utils.py](../../cgmToolsPy3/cgm/core/mrs/lib/builder_utils.py)** — `get_dynParentTargetsDat`, scaleSetup dyn-parent helpers
- **[handle.py](../../cgmToolsPy3/cgm/core/mrs/blocks/simple/handle.py)** — handle dyn parents; pivot result driver
- **[limb.py](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/limb.py)** — limb rigRoot / IK-FK dyn parents; digit scaleSetup bypass
- **[segment.py](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/segment.py)** — segment rigRoot scaleSetup dyn parents
- **[head.py](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/head.py)** — head rigRoot scaleSetup dyn parents; **neck form** `formAim` / `shapersAim` / `shapersAimUp`; **neck `rig_segments`** ribbon / **ribbonLive**
- **[ik_utils.py](../../cgmToolsPy3/cgm/core/rig/ik_utils.py)** — **`IK.ribbon`** arcLength squash aim-scale hookup (shared with segment blocks)

## Timeline

### October 7, 2026 — MRS body (scaleSetup dyn-parent, pivot naming)
> **Agent note:** Keep **one** `### October 7, 2026` day block. Add or extend **`####`** subsections below; do **not** replace sibling subsections or delete prior Oct 7 notes.

**Day status**: In progress — Maya verify arm/prop handle attach **end** → wrist; digit builds on temp bypass until finger attach stable.

#### scaleSetup dyn-parent — shared helpers + first rollout (head / segment / handle / limb)
**What**: With block **scaleSetup** on, improve dyn-parent defaults and parent lists on body blocks (started on **head** rigRoot vs part driver).  
**Files**: `cgm/core/mrs/lib/builder_utils.py`, `head.py`, `segment.py`, `handle.py`, `limb.py`

**Features**:
- **`scaleSetup_scaleSpacePuppetDefault`** — when scaleSetup + dyn parent scale mode **space** (and not **parentToDriver**), default **scaleSpace** to **puppet**
- **`scaleSetup_dynParentDefaultIndex`** + **`_scaleSetup_dynParentModeInt`** — set **space** / **orientTo** / **follow** from block **root_dynParentMode** / **dynParentMode** (not dyn group default alone)
- **rigRoot** (scaleSetup): default enum toward **parent-module** driver slot (index **1** after part driver) without reordering parent list; **limb** later experiment keeps rigRoot **scaleSpace** at **0** on scaleSetup
- **IK / FK / mid** (not rigRoot): **`ml_baseDynParents.append(mRoot)`** + **`LISTS.get_noDuplicates`** on composed lists; **`ml_endDynParents.insert(0, mRoot)`** unchanged pattern
- **Limb rigRoot**: extend **ml_dynParentsAbove** when **b_scaleSetupDynSpace** or **root_dynParentScaleMode == space**
- **Handle**: **scaleSetup** on **mHandle** + **rigRoot** when present; **orientTo** / **follow** use block mode attrs

**Decisions**:
- Do **not** prepend **mRoot** onto rigRoot’s own parent list (rigRoot stays part-driver-first)
- Index **1** default is **rigRoot-only**; IK/FK use **{part}_root** on base lists instead

**Status**: Code in tree — verify per block profile in Maya

#### scaleSetup dyn-parent — attachPoint-aware rigRoot / handle defaults
**What**: Default **space** / **orientTo** / **follow** from block **attachPoint** against parent-driver menu (shoulder, wrist, limb root on arm, etc.).  
**Files**: `builder_utils.py` (**`scaleSetup_dynParentDefaultIndexFromAttach`**, **`_scaleSetup_attach_driver_target`**, **`_scaleSetup_walk_parent_nondigit_driver_point`**); callers in head/segment/handle/limb **rig_cleanUp**

**Features**:
- Resolve enum index on **rebuilt** **`mDynGroup.msgList_get('dynParents')`** (not pre-dedupe Python build list)
- **Child** modules (prop **handle**, digit under arm): **`mModule.get_driverPoint`** / walk to first non-**digit** parent
- **Non-digit limb rigRoot**: own **rigJoints** base/end → **masterGroup** / **dynParentGroup** when attach maps to local chain
- **end** attach → wrist: prefer driver-point match; fallback **second** slot in **ml_dynParentsAbove** enum order (not last / limb root)
- Avoid stale **`md_dynTargetsParent['end']`** (overwritten in **`get_dynParentTargetsDat`** parent loop)

**Status**: In progress — finger **end** was defaulting to shoulder (index 1); digit path still tuning

#### Pivot result null — module naming + wiring
**What**: Pivot **result** driver nulls include module **partName**; document create/wire path for artists and agents.  
**Files**: `handle.py` (**`rig_frame`**), `segment.py`, `limb.py` (two IK paths); **`block_utils.pivots_setup`** unchanged

**Features**:
- **`cgmName`** **`{partName}_pivotResult`**, **`cgmAlias`** **`{partName}_PivotResult`**
- **Handle**: **`pivotHelper`** in prerig → result null in **`rig_frame`** → **`pivotResultDriver`** → **`pivots_setup(..., pivotResult=...)`** → parented **`mLastParent`**
- **One DAG transform** (message name “driver” is historical); limb **ball** **ikEnd** may use zero **`mPivotResultDriven`** between driver and setup
- Rebuild module for new outliner names

**Status**: Code complete — Maya verify naming on new builds

#### Digit limb — temp skip scaleSetup dyn-space (`b_scaleSetupDynSpace`)
**What**: Ship finger/toe **digit** rigs without scaleSetup dyn-parent / scaleSpace pass while attach defaults are unstable.  
**Files**: `limb.py` — **`_LIMB_TEMP_SKIP_SCALE_SETUP_DIGIT`** (default **True**)

**Features**:
- **`rig_dataBuffer`**: **`b_scaleSetupDynSpace = False`** when **`rigSetup == digit`**; **`b_scaleSetup`** unchanged (squash/stretch, scale blend, toe/ball scale constraints)
- **rig_cleanUp** dyn-parent paths use **`b_scaleSetupDynSpace`** (not **`b_scaleSetup`**) for attach index, **mRoot** on base lists, IK/FK dedupe, scaleSetup-only rigRoot extras

**Decisions**: Set toggle **False** and remove gate when digit **attach end → wrist** is Maya-verified

**Status**: Active temp gate

#### block_utils — datList_validate `None` count guard
**What**: Builder **Edit datList** (and similar) no longer crashes when `checkAttr` (e.g. `numControls`) is missing or unset.  
**Files**: `block_utils.py` — coerce `len_needed` to `int` with fallbacks in **`datList_validate`** / **`nameList_validate`**

**Status**: Code in tree — reload MRS backend in Maya

#### Handle proxy mesh — geoOnly / geoAdd + Proxy Geo unlock
**What**: Handle **proxyType** paths for user-only vs cast+user proxy mesh; imported **Proxy Geo** duplicates unlock override attrs before proxy coloring.  
**Files**: `handle.py` (**`_handle_build_proxy_meshes`**, **`proxyGeo_add`** / **`proxyGeo_replace`**); `shared_dat.py` — **`proxyType`** **`geoAdd`** (legacy **`comboMesh`** → **`geoAdd`** via **`_handle_normalize_proxy_type`**)

**Features**:
- **`geoOnly`** / **`proxyShape` geoOnly**: mesh from **Proxy Geo** only (`proxyMeshGeo` / **`proxyGeoGroup`** / `*_proxyGeo`); skips cast loft/tessellate and **`proxyHelper`** form geo
- **`geoAdd`**: cast proxy + user Proxy Geo duplicates (replaces **`comboMesh`**)
- **`_proxy_geo_unlock_for_edit`**: DAG unlock + **`ATTR.break_connection`** + unlock **`overrideEnabled`** (and related override plugs) on transform + shapes before **`CORERIG.colorControl`** — fixes locked/connected attrs on referenced/imported geo

**Decisions**:
- Handle finalize stays **`polyCloseBorder`** after tessellate (**`_handle_proxy_finalize_mesh`**) — limb/segment Block Mesh caps use separate open-loft + end-cap helpers in **`block_utils`**

**Status**: Code in tree — Maya verify Proxy Geo add/replace on production props; **core reload** if **`proxyType`** enum changed on disk

#### Puppet / module proxy mesh — unify, normals, limb proxy return
**What**: Puppet mesh join across handle skinned geo + limb module proxies; reduce false inside-out flips on unified fingers; limb proxy list return + cap/normal ordering.  
**Files**: `block_utils.py` (**`puppetMesh_create`**, **`create_simpleLoftMesh`**, **`mesh_proxyCreate`**, **`proxy_mesh_cap_simple_loft_ends`**); `puppet_utils.py`; `limb.py` (**`build_proxyMesh`**); `geo_Utils.py`

**Features**:
- **`puppetMesh_create`**: **`polyUniteSkinned`** on handle **`ml_skinned`** + limb **`ml_proxy`**; **`polyUnite(...)[0]`** when validating unite result
- **`limb.build_proxyMesh`**: return **`ml_segProxy`** after **`msgList_connect('proxyMesh')`**
- **`mesh_proxyCreate`**: **`GEO.normalCheck`** after segment caps + **`match_transform`**
- **`GEO.is_reversed`**: unit normal via **`MATH.mag`** (not **`normalizeList`**); skip degenerate vectors; slight ray origin offset for thin tubes
- Unified puppet path: **`puppetMesh_normalCheck`** on handle skinned pre-unite only — avoid re-flipping limb pieces already checked in **`mesh_proxyCreate`** / module **`build_proxyMesh`**

**Status**: Code in tree — Maya verify full puppet mesh (fingers + handle + limbs); limb **Block Mesh** end caps

#### Form sub shaper track curves — per-block `seg_*_trackCrv` naming
**What**: Fix sub shapers on a **second** block in form (e.g. second limb) riding the **first** block’s segment track curves — wrong `pointOnCurveInfo.inputCurve` / attach behavior.  
**Files**: `limb.py` (inline form sub-shaper loop); `block_utils.py` — **`form_segment`** (used by **handle**, **head**, **segment**)

**Features**:
- Segment linear track curves renamed **`{p_nameBase}_seg_{i}_trackCrv`** (was generic **`seg_{i}_trackCrv`** on every block)
- Sub shaper attach unchanged at call site: **`BLOCKSHAPES.attachToCurve(mHandle, mLinearCurve, …)`** on the curve created for that segment

**Root cause** (debug / agent context):
- **`create_pointOnInfoNode`** connects POC via **short** shape name from **`listRelatives(..., shapes=True)`** (no **`fullPath`**)
- Duplicate short names across blocks → Maya resolves **`inputCurve`** to the first matching shape; **`getUParamOnCurve`** still used full DAG path (U could look sane while the wire was wrong)
- Not a Maya 2023 vs 2026 issue; shows when **two+** form setups with sub shapers coexist

**Decisions**:
- Ship **unique track curve names** per block (**`p_nameBase`** prefix); optional follow-up: full-path shape connect in **`curve_Utils.create_pointOnInfoNode`** or pass resolved **`mShape.mNode`** from **`attachToCurve`**

**Status**: Code in tree — Maya-verify dual limb (or limb + handle/segment) form with **`numSubShapers`**; existing scenes need **re-form** (or rebuild form null) to pick up new curve names

#### MRS Builder — scene-load block list refresh
**What**: Retained **mrsBuilder** window now refreshes the left **Rigblocks** scroll list when Maya fires **SceneOpened** (File → Open / New) without closing Builder.  
**Files**: `cgm/core/mrs/Builder.py`; doc note in [`Feature_CgmToolUI.md`](../Features/Feature_CgmToolUI.md)

**Features**:
- **`setSceneChangeCB`** in **`ui.insert_init`** (same pattern as **setTools**, **cgmDynSimTool** — zoo **`baseMelUI`** → Maya **`scriptJob`** parented to the window)
- **`uiFunc_on_scene_change`**: boundary log → **`mc.evalDeferred(..., lp=True)`** so the new scene DAG exists before **`BLOCKGEN.get_uiScollList_dat`**
- **`uiFunc_refresh_blocks_after_scene_open`**: **`uiFunc_block_clearActive()`** (clear active block, inspector, **`mActive`**) + **`BlockScrollList.rebuild()`**; fallback rebuild on error

**Decisions**:
- Clear active block + right panel on scene change (not list-only refresh) — avoids stale meta on deleted nodes
- Child windows (**blockEditor** / **picker**) out of scope; main Builder list is the file-open contract

**Status**: Code in tree — Maya verify: keep Builder open → Open/New scene → list matches new scene; relaunch Builder or reload MRS if session had old **`Builder.py`**

#### Head block — neck form shaper aim + ribbonLive segment rig
**What**: Head **neck** form setup matches **Segment** shaper aim attrs and **`block_utils.form_segment`** kwargs; neck **`rig_segments`** ribbon dict aligned with **Segment** so **ribbonLive** + squash/aim-scale no longer fails in **`IK.ribbon`** (`scaleZ` connect).  
**Files**: `head.py` (form state mask, `d_attrsToMake` / defaults, neck **`form_segment`** call, **`rig_segments`**); `ik_utils.py` — arcLength per-joint squash loop hardening

**Features**:
- **Form** (when **`neckBuild`**): block attrs **`formAim`**, **`shapersAim`**, **`shapersAimUp`** (same enums/defaults as segment: simple / chain / handle); exposed on form state + box/simple profile masks; passed into **`UTILS.form_segment`** with **`neckShapers`** / **`neckSubShapers`** and **`orientNeckHelper`**
- **`rig_segments`**: always **`settingsControl`** = **`mRigNull.settings`**; **`parentDeformTo`** = **`scaleRoot`** / **`rigRoot`**; **`driverSetup`** from **`ribbonAim`**; **`extendEnds`** from **`ribbonExtendEnds`**; explicit **`setupAimScale`** true/false from **`segmentStretchBy`**; **`ribbonConnectBy`**; guts vis on seg measure curve; **`IK`** reload before call
- **`d_squashStretch`**: **`additiveScaleEnds`** from **`scaleSetup`** commented out on head (matches segment — avoids fighting live-surface aim scale)
- **`ik_utils`**: reset **`l_argBuild`** per joint in arcLength squash loop; **`mPlug_aimResult`** fallback when extra squash on but aim scale off; guard **`scaleZ`** connect when aim plug missing

**Root cause** (ribbonLive failure):
- Neck **`form_segment`** previously used **`form_segment`** defaults (`formAim`/`shapersAim` **`toEnd`**) — no artist-facing aim enums
- Neck ribbon **`_d`** drifted from segment: conditional settings, **`mDeformNull`** parent, **`additiveScaleEnds`** on when **`scaleSetup`**, missing explicit **`setupAimScale=False`** for translate stretch → **`mPlug_aimResult`** could be **`None`** at **`doConnectOut(..., scaleZ)`**

**Status**: Code in tree — Maya verify: head with **`neckBuild`**, **`segmentType`** **ribbonLive**, squash on; re-form neck then full rig rebuild; reload **`ik_utils`** + head block module (or core reload) if session stale

#### TD shell — rig attr flags (toolbox + cgm menu)
**What**: Quick **dagLock** / **dagUnlock** and standard transform **hide/unhide** on selection via existing **`cgmObject.dagLock`** and **`setAttrFlags`** — surfaced in **cgmToolbox** and **cgm → Rigging Utils**.  
**Files**: `cgm/core/lib/rigging_utils.py` — **`dag_lock`**, **`standard_attrs_hide`**, **`standard_attrs_unhide`**; `cgm/core/tools/toolbox.py` — Rigging **Flags:** row; `cgm/core/tools/lib/tool_chunks.py` — **`uiSection_riggingUtils`** **Flags** submenu

**Features**:
- **dagLock** / **dagUnlock** — **`cgmObject.dagLock(True/False)`** on tx–sz + v (TD context **`each`**)
- **Hide Std** — **`setAttrFlags()`** defaults (lock + hide standard transforms)
- **Unhide Std** — **`setAttrFlags(lock=False, visible=True, keyable=True)`**
- Toolbox layout: **Flags:** row directly under **Group:** (before **Attr:**)
- Menu: **Rigging Utils → Flags →** same four items

**Status**: Code in tree — relaunch toolbox / rebuild cgm menu to pick up UI

#### TD shell — Query distance results on status line
**What**: **cgm → Query → Distance** measurement readouts use **`log.warning`** instead of **`print`** so results show on Maya’s status line (e.g. **`|Arc length.each| >> 45.42…`**).  
**Files**: `cgm/core/tools/markingMenus/lib/contextual_utils.py` — **`func_process`** **`resultWarning`** kwarg (popped before backend call); `tool_chunks.py` — **`uiSection_distance`** passes **`resultWarning=True`** on Sum, Ordered, Arc length, Near/Far queries (not **Surface Nodes** create)

**Decisions**:
- Opt-in per menu callback — other **`func_process`** callers unchanged
- Same message format as prior **`print`** lines; only logging channel changes

**Status**: Code in tree — rebuild cgm menu or reload **`contextual_utils`** + **`tool_chunks`** in session

---

### September 1, 2026 - Eye prerig fix + muzzle constraint weights
**What**: First Face26 commit — eye prerig uses the shared `mParent` handle contract; muzzle drops stale nostril influence target and normalizes pointConstraint weights by distance before corner bias.  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/organic/eye.py` — `create_lidHandle`: `mStateNull` → `mParent`; remove unused `numLidLwrShapers` / `numLidUprShapers` defaults; blendshape weight attrs via `mc.listAttr(..., '.weight')` (no `cgm.lib.deformers`)
- EXTENDED: `cgm/core/mrs/blocks/organic/muzzle.py` — remove `nostril` from lip-corner influence target loop; `DIST.get_normalizedWeightsByDistanceToObj` before hardcoded corner weight tweak

**Features**:
- Eye lid handle creation matches `blockShapes_utils` parent kw (`mParent`)
- Muzzle lip-corner pointConstraint weights distance-normalized, then corner bias (`targetWeights[0] = 1.25`)

**Decisions**:
- Nostril removed from automatic lip-corner influence list (was pulling unrelated targets)
- Weight normalization lives in rig build (not a shared constraint helper yet)

**Status**: Code complete — Maya verify: eye prerig lid handles parent correctly; muzzle rebuild with lip-corner influences

---

### September 1, 2026 - Merge jburton/AnimData
**What**: Brought AnimData branch into Face26 for shared release (`26.09.01.01`). AnimClip / mrsAnimClip work is tracked on [`Branch_AnimData.md`](Branch_AnimData.md), not duplicated here.  
**Status**: Merge complete

---

### September 2, 2026 - prntConstraint lip mid-follow mode
**What**: Dedicated `lipMidFollowSetup == 'prntConstraint'` path on muzzle; default enum extended with `pntConstraint`; fallback path splits parentConstraint into point+orient; lip-aim block moved under prntConstraint branch (deduped).  
**Files**:
- EXTENDED: `cgm/core/cgm_General.py` — `__BRANCH` = `FaceRigging26`
- EXTENDED: `cgm/core/mrs/blocks/organic/muzzle.py` — `lipMidFollowSetup` enum `ribbon:prntConstraint:pntConstraint:parent`; new `prntConstraint` rig path (corner/center influences + parentConstraint + aim); else path uses `pointConstraint` + `orientConstraint`

**Features**:
- **prntConstraint**: mid lip handles parent to follow null, constrained to two of three influences (left vs right chain), plus per-joint aim along lip chain
- **pntConstraint** (default fallback when not ribbon/parent/prntConstraint): point + orient split instead of parentConstraint
- Enum order documents available modes for artists/TAs

**Decisions**:
- prntConstraint keeps aim setup inside its branch; pntConstraint path no longer duplicates aim block
- Debug `pprint` left in prntConstraint loop (remove when Maya-verified)

**Status**: Code complete — Maya verify: rebuild muzzle with `lipMidFollowSetup` = `prntConstraint` vs `pntConstraint` vs `ribbon`

---

### September 2, 2026 - Merge origin/jburton/SpringCleaning
**What**: Pulled lib→core migration into Face26 so facial blocks build on current `cgm.core` APIs (no live `cgm.lib` in touched paths). Full migration timeline: [`Branch_SpringCleaning.md`](Branch_SpringCleaning.md).  
**Notable for facial callers**: `ModuleControlFactory` / `ModuleShapeCaster` use `CORERIG.group_me` and `CORERIG.shapeParent_in_place`; eye blendshape queries use `mc.listAttr`.  
**Status**: Merge complete

---

### September 2, 2026 - Face proxy / puppet mesh pipeline
**What**: Configurable face-block mesh pipeline — `proxyBuild` toggles colored proxy mesh vs skinned puppet mesh; batch and puppet utils route per block instead of forcing all face blocks through unskinned proxy dupes. Muzzle/brow/eye `build_proxyMesh` refactored with `simpleMeshMode` / `puppetMeshMode`; puppet duplicates copy skin. Build output path helper + Scene send-to-build P4 prepare. Brow final mesh respects `numSplit_u` / `numSplit_v`.  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/organic/muzzle.py` — `meshBuild` / `proxyBuild` attrs; `create_simpleMesh`; `build_proxyMesh` puppet/module/simpleMeshMode split; skin copy on puppet dup
- EXTENDED: `cgm/core/mrs/blocks/organic/brow.py` — same proxy attrs + mesh refactor; `get_meshFromNurbs` `mode='general'` (uses `numSplit_u` / `numSplit_v`)
- EXTENDED: `cgm/core/mrs/blocks/organic/eye.py` — same proxy attrs + mesh refactor; `create_simpleMesh` calls module `build_proxyMesh` (not `self.build_proxyMesh`)
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — `block_proxy_mesh_flow`; `puppetMesh_create` separates skinned vs proxy unify paths
- EXTENDED: `cgm/core/mrs/lib/puppet_utils.py` — `proxyMesh_verify` skips face blocks when `proxyBuild` off; matching `puppetMesh_create` routing
- EXTENDED: `cgm/core/mrs/lib/shared_dat.py` — `proxyBuild` in proxySurface UI group
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — `resolve_build_output_path` (`*_BUILD.mb` beside version file)
- EXTENDED: `cgm/core/mrs/Scene.py` — `SendToBuild`: `PATHUTIL.prepare_maya_scene_for_save` on existing BUILD output before opening MRS Build

**Features**:
- **`proxyBuild` off** (default on muzzle/brow/eye): batch step 1 skips module proxy; step 2 builds **skinned puppet mesh** via `create_simpleMesh`
- **`proxyBuild` on**: module `proxyMesh` + puppet `puppetProxyMesh` (skin copied to dupes)
- **`meshBuild`**: master on/off for any mesh on the block (default on for face blocks)
- Mixed puppet unify: skinned pieces `polyUniteSkinned`, proxy pieces `polyUnite` (no global `skin=False` override on batch `proxy=True`)
- Brow tessellation: form preview and final mesh both driven by block `numSplit_u` / `numSplit_v` (was hardcoded 3×3 via `get_meshFromNurbs` default mode)

**Decisions**:
- Face blocks follow limb-style `proxyBuild` gate on module proxy; puppet skinned path is the default artist workflow
- Eye `create_simpleMesh` must call module-level `build_proxyMesh(self, …)` — Red9 meta has no `build_proxyMesh` attr on the block node
- Eye lid tessellation uses `get_meshFromNurbs` `mode='general'` (`numLidSplit_u` / `numLidSplit_v`) — matched brow

**Status**: Code complete — Maya verify: Edna muzzle/brow batch post with `proxyBuild` off; brow density via `numSplit_u` / `numSplit_v`

---

### September 3, 2026 - Proxy/puppet mesh normals, shaders, skin-unify routing, timing logs
**What**: Harden face proxy/puppet mesh output — flip inside-out tessellation via `GEO.normalCheck`, apply limb-style proxy shaders through shared helpers, and skip per-block proxy flow when batch skin-unify is active. Centralize human-readable elapsed-time formatting for batch/rig logs.  
**Files**:
- EXTENDED: `cgm/core/cgm_General.py` — `get_timeString`, `get_timeLogString` (e.g. `21m 9.9s`; raw seconds appended when ≥ 1 min)
- EXTENDED: `cgm/core/mrs/lib/batch_utils.py` — post-process time reports + total time use `get_timeString` / `get_timeLogString`
- EXTENDED: `cgm/core/mrs/RigBlocks.py` — contextual rig timing via `get_timeString`
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — `puppetMesh_normalCheck`, `puppetMesh_colorGeo` (`get_side` + `CORERIG.color_mesh`, `'center'` when side is `none`/empty); `GEO` / `TRANS` imports; `puppetMesh_create` calls helpers after `create_simpleMesh`; `_blockProxyFlow` gated with `and not _skinUnify`; `create_simpleMesh` runs `GEO.normalCheck` on loft output
- EXTENDED: `cgm/core/mrs/lib/puppet_utils.py` — same helper usage + skin-unify proxy skip (mirrors `block_utils`)
- EXTENDED: `cgm/core/mrs/blocks/organic/muzzle.py` — `GEO.normalCheck` after `nurbsToPoly`; proxy vis uses `CORERIG.color_mesh` (not `colorControl`)
- EXTENDED: `cgm/core/mrs/blocks/organic/brow.py` — proxy vis `_wireProxyVis`: `CORERIG.color_mesh` + `'center'` side fallback
- EXTENDED: `cgm/core/mrs/blocks/organic/eye.py` — lid proxy mesh shader via `CORERIG.color_mesh` + `'center'` side fallback

**Features**:
- **`puppetMesh_normalCheck`**: per-shape `GEO.normalCheck` after puppet/simple mesh creation (inside-out nurbs tessellation fix)
- **`puppetMesh_colorGeo`**: shared proxy shader path — `CORERIG.color_mesh(..., proxy=True)` with block side (or `'center'`)
- **Skin-unify**: `block_proxy_mesh_flow` / `verify_proxyMesh` skipped when `skin=True` (unified skinned puppet path only)
- **Timing logs**: batch post-process step reports and totals use human-readable durations

**Decisions**:
- Proxy/puppet display shaders match limb/segment — `color_mesh` + `proxy=True`, not `colorControl`
- Unknown / empty block `side` → `'center'` for shader lookup (same pattern as `_wireProxyVis` on face blocks)
- Skin-unify and per-block proxy dup are mutually exclusive in `puppetMesh_create`

**Status**: Code complete — Maya verify: batch post skin-unify puppet mesh (normals + side-colored geo); proxyBuild on path still uses `color_mesh`; batch timing log readability

---

### September 4, 2026 - geoGroup stability + Feature_MRSMeshCreation doc
**What**: Intermittent loss of puppet `geoGroup` during `puppetMesh_create` when head `neckBuild` ran internal `polyUniteSkinned` on meshes parented under geoGroup. Safe puppet mesh delete/unite filters; `puppet_geoGroup_get`; head keeps intermediate geo at world until final parent. Feature doc captures full mesh contract.  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/organic/head.py` — `create_simpleMesh`: no intermediate parent to geoGroup; cleanup guards
- EXTENDED: `cgm/core/mrs/lib/block_utils.py` — `puppet_geoGroup_get`, `puppet_mesh_filter_nodes`, `puppet_mesh_delete_existing`
- EXTENDED: `cgm/core/mrs/lib/puppet_utils.py` — same helpers via `BLOCKUTILS`
- ADDED: `Features/Feature_MRSMeshCreation.md` — design contract for proxy/puppet/skinned mesh

**Status**: Maya-verified — geoGroup stable on repeat puppet mesh create with `neckBuild`

---

---

---

### September 9, 2026 - cgmSimChain setup dat (Phase 2)
**What**: **`SimChainSetup`** (`.cgmSimChainSetup`) captures a full cgmDynFK recipe (mapped nucleus/cloth/hair, chain targets, options, optional `presetRefs`) and re-wires the setup when scene nodes still exist.  
**Files**:
- EXTENDED: `cgm/core/lib/simChain_dat.py` — `SimChainSetup`, `resolve_library_filepath`, `apply_preset_ref`, setup library scan
- EXTENDED: `cgm/core/tools/dynFKTool.py` — **Presets → Setups**, **File → Capture Setup Dat**, **Tools → Apply Setup Dat**
- EXTENDED: `cgm/core/tests/test_coreLib/test_SIMCHAIN.py` — setup schema + library resolve tests
- EXTENDED: `Features/Feature_DynSimTool.md` — Phase 2 setup contract

**Features**:
- **Capture**: loaded cgmDynFK → JSON under `cgmDat/sim/setups/`
- **Apply**: find/create setup → map nodes → rebuild hair/clothAttach chains → apply `presetRefs`
- **Library**: **Presets → Setups** dev scan (parallel to preset Library)

**Status**: Code complete — Maya verify: capture setup on production rig → reload scene → Apply Setup Dat

---

### September 9, 2026 - cgmSimChain dat presets (Phase 1)
**What**: cgmSimChain preset **file** transport — `SimHairDat` / `SimClothDat` / `SimNucleusDat` under `cgm/cgmDat/sim/`. Library scan + Save/Load in dynFKTool; dict apply via `profile_apply_section`. *(Artist menu cutover to library-only: September 10, 2026.)*  
**Files**:
- ADDED: `cgm/core/lib/simChain_dat.py` — dat classes, capture/apply, library scan, `seed_dev_library()`
- EXTENDED: `cgm/core/lib/nCloth_utils.py` — `profile_apply_section()` for nc/n dict apply
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `profile_apply_section()` for hs/n dict apply
- EXTENDED: `cgm/core/tools/dynFKTool.py` — Presets → Library, File Load/Save/Apply Dat; Library submenu rebuild fix (no `MelMenuItem.clear`)
- ADDED: `cgm/cgmDat/sim/{hair,cloth,nucleus}/*.cgmSim*Dat` — seed presets (bob, bangs_firm, cotton, solver_balanced, wind_calm)
- ADDED: `cgm/core/tests/test_coreLib/test_SIMCHAIN.py` — seed read, module export, JSON round-trip
- EXTENDED: `Features/Feature_DynSimTool.md` — dat preset contract + Phase 2 setup stub

**Features**:
- **Library**: dev scan of `cgmDat/sim` (BlockConfig-style keys e.g. `hair.bob`)
- **Capture/Save**: selection → dat file under kind folder
- **Apply**: reuses skip-list, base seed, gravity remap from Feature_DynSimTool preset contract

**Decisions**:
- Phase 1 = preset attrs only; Phase 2 = `.cgmSimChainSetup` full setup re-wire (schema stub in feature doc)
- Layered fabric+solver remains two dat applies (cloth dat, nucleus dat)
- Library menu populates when **Presets** opens; fresh `MelMenuItem` submenu — never `.clear()` on submenu items

**Status**: Maya-verified — Library load/apply, File Save/Load, capture round-trip; parity with Python Presets menu on test setups

---

### September 9, 2026 - cgmSimChain dynFK segment length + hair/cloth presets
**What**: Hair dynamic chains now match joint spacing on inCurve/outCurve; new **`bob`** / **`bangs_firm`** hair-feel presets and nCloth fabric **`bangs_firm`** for firm short-panel / cage cloth attach. Introduced **`CURVES.polyline_length_fractions`** for chord-length POC placement.  
**Files**:
- EXTENDED: `cgm/core/lib/curve_Utils.py` — **`polyline_length_fractions`**: 0–1 cumulative fractions along a polyline (joint spacing → `turnOnPercentage` POC params)
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — **`chain_create_hair`**: **`curveLinear`** inCurve (was cubic EP); POC nodes use **`parameter` + `turnOnPercentage`** from joint fractions (not `getUParamOnCurve` on extended curve); **`skinCluster`** on full joint chain (was root-only **`bindSkin`**); **`extendEnd` default `False`**; **`extendStart` / `extendEnd`** use explicit `None` handling (falsy `False` no longer overridden by instance defaults); manual **`upSetup`** no longer appends extend CV when **`extendEnd`** is off
- EXTENDED: `cgm/core/presets/cgmDynFK_presets.py` — presets **`bob`**, **`bangs_firm`**; **`d_profileKind`** entries (`hair`)
- EXTENDED: `cgm/core/presets/cgmNCloth_presets.py` — fabric preset **`bangs_firm`** (high stretch/compression, soft bend, moderate damp, subtle **`inputMeshAttract`**); **`d_profileKind`** entry (`fabric`)
- EXTENDED: `Features/Feature_DynSimTool.md` — hair **segment length** contract; bob / bangs / firm-cloth attach patterns; nCloth input-attract anti-pattern

**Features**:
- **Segment length**: linear inCurve through joint CVs; full-chain skin; locators sample outCurve at joint-length ratios
- **Hair feel**: **`bob`** (chin-length volume); **`bangs_firm`** (forehead fringe — root-heavy attract/stiffness)
- **Cloth feel**: **`bangs_firm`** nc — stretch 120 / compression 80 / bend 0.25 / damp 1.0 / mass 0.6 / input attract 0.08 (head-follow panels; not high input lock)

**Decisions**:
- Firm short cloth / hair cages: stretch+compression high, bend relatively low, damp moderate, **`inputMeshAttract` subtle** — high input attract locks rest mesh and kills head follow
- Ponytail-style tip overshoot remains opt-in via **`extendEnd=True`** (script/API); not default on **`chain_create_hair`**

**Status**: Code complete — Maya verify: dynFK chain joint spacing vs inCurve; add chain to **existing** hairSys; **Presets → Hair** `bob` / `bangs_firm`; **Presets → Cloth** `bangs_firm` + nucleus solver on head-follow cage

---

### September 11, 2026 - Hair bind order, post-MCD rebuild, follicle sampling options
**What**: Fixes **Make Dynamic Chain** when adding a hair chain to an **existing** `cgmDynFK` / hairSys (Edna bang + hairTip). Skins inCurve **before** `makeCurvesDynamic`; post-MCD **rebuilds** linear inCurve from joint positions, wires **`follicle.startPosition`**, rebinds skin, **syncs outCurve at rest**. Default follicle **`sampleDensity=1`** (CV-matched collision segments); optional **Fixed segment length** in Create **Options**. Create panel separates hair vs cloth attach with **Cloth Options** header row.
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — ... **last-joint forward tangent aim** when **`extendEnd=False`** (tip **`+fwd`**, aim = tip + tangent × segment length)
- EXTENDED: `cgm/core/tools/dynFKTool.py` — Create layout (hair first, **Cloth Options** header); **Options → Fixed segment length** + segment length field (readable inactive styling per **Feature_CgmToolUI**)
- EXTENDED: `cgm/core/lib/simChain_dat.py` — capture/apply **`fixedSegmentLength`**, **`follicleSegmentLength`**, **`surfaceTrack`** for `clothAttach` only
- EXTENDED: `Features/Feature_DynSimTool.md` — bind-order contract, follicle sampling default vs optional, outCurve rest sync, troubleshooting + verification checklist
- EXTENDED: `Features/Feature_CgmToolUI.md` — disabled **`MelTextField`** anti-pattern on dark template rows

**Features**:
- **Add-to-existing hairSys**: no `inCrv.worldSpace` / skinCluster failure; frame-0 **inCrv** / **outCrv** match joint chain after rebuild
- **Follicle sampling default**: **`fixedSegmentLength=off`**, **`sampleDensity=1`** — one collision segment per inCurve CV / joint span
- **Follicle sampling optional**: Create **Options → Fixed segment length** → **`fixedSegmentLength=on`**, **`segmentLength=1.0`** (scene units)
- **Collision viz finer than joints**: shared hairSystem **`extraBendLinks`** / **`subSegments`** (e.g. **`bob`** preset) — expected; tune on hairSystem AE

**Decisions**:
- **`startPosition`** reads inCurve **`worldSpace`** — inCrv must remain on **chain grp**, not reparented under follicle with **`relative=True`**
- Follicle placement follows rig via **`parentConstraint(mo=True)`** after root joint → follicle parent; no manual follicle snap to root joint
- Fixed 1-unit collision sampling is **opt-in** at build time (not default)
- **Last-joint aim**: when **`extendEnd=False`**, tip **`+fwd`** aim null = tip POC + outCurve tangent × last segment length (same aim axis as interior joints)

**Status**: Code complete — Maya verify: fresh chain + add chain to existing Edna hair setup; frame 0 curve/joint alignment; optional fixed segment length toggle

---

### September 14, 2026 - Hair follow: Spline IK default + Legacy POC
**What**: New default **Spline IK** hair follow (follicle-driven **outCrv**, duplicate **driven** joint chain + **`ik_utils.spline`**, locators parented under driven joints). **Legacy** POC/aim on **outCrv** remains opt-in (**Create Options → Follow mode → Legacy**); chains without **`hairFollowMode`** still rebuild as legacy. Create **Options** add **In curve degree** / **Out curve degree**; spline rebuild uses **`follicle_set_input_curve`** and **`follicle_regenerate_out_curve`** (no forced in→out CV match).
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — follicle I/O helpers, **`chain_rebuild_spline_follow`**, **`chain_rebuild_hair`**, spline follow build/teardown
- EXTENDED: `cgm/core/tools/dynFKTool.py` — Create Options follow mode + degrees; Details **Rebuild Chain** vs **Rebuild Locators**
- EXTENDED: `cgm/core/lib/simChain_dat.py` — capture/apply **`hairFollowMode`**, **`inCurveDegree`**, **`outCurveDegree`**
- EXTENDED: `Features/Feature_DynSimTool.md` — **Hair follow modes** section

**Status**: Code complete — Maya verify per Feature doc checklist (spline default, degrees, rebuild chain, legacy parity)

---

### September 15, 2026 - cgmSimChain Details UX (refresh, rename, nested lists)
**What**: cgmSimChain header **refresh** re-reads the loaded setup from scene; per-chain **Name** field renames `chain_*_grp` and hair infrastructure via **`chain_set_name`**; Targets/Locators/Joints use zebra sub-header collapsibles under each chain frame.  
**Files**:
- EXTENDED: `cgm/core/tools/dynFKTool.py` — refresh icon (`refresh.png`), `uiFunc_refresh_loaded_setup`, chain Name row, nested list chrome
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `chain_cgm_name`, module `chain_set_name(mDynFK, …)`, `_chain_rename_hair_infrastructure`
- EXTENDED: `Features/Feature_DynSimTool.md` — UI surface rows

**Status**: Code complete — Maya verify: refresh after scene edit; rename hair chain; collapse chain hides sub-lists; **Reload Dependencies** logs Red9 + **`cgm_Meta`** + **`dynamic_utils`**

**Docs**: **`Feature_CgmMetaAPI.md`** § Session reload (core **`CGM._reload`** for **`mClass`**); **`cgm-reload-mod.mdc`** — no partial meta reload in tools

---

### September 15, 2026 - Multi hairSystem + Details dat presets
**What**: Per-chain **`mHairSysShape`** and setup **`msgList mHairSystems`**; Create **Hair system** (New / Default / registered); Details **Hair systems** block with per-shape **Load Dat** / **Save Hair Dat…** (same **`.cgmSimHairDat`** library as top **Presets** menu — Maya **`nodePreset`** removed from **`dynFKTool`**). Nucleus connect dedupe for playback perf when re-registering hair systems.  
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — hair registry, `chain_create_hair` modes, `hair_system_resolve_for_chain`, nucleus dedupe on register
- EXTENDED: `cgm/core/tools/dynFKTool.py` — hair system rows, `uiFunc_sim_dat_capture_save_for_target`, library-only preset option menus
- EXTENDED: `cgm/core/lib/simChain_dat.py` — `SimHairDat` per-target apply/capture; setup dat `hairSystems[]`
- EXTENDED: `Features/Feature_DynSimTool.md` — multi-hair patterns, UI surface, verification #25–28

**Status**: Code complete — Maya verify: two chains, two hairSystems, independent **Load Dat** per row; **Presets → Hair** still default-only

---

### September 18, 2026 - cgmDynSimTool load UX + Create/chain UI polish
**What**: **Load progress bar** on autoload (**LastDynFK**) and header **load selected** while **`uiFunc_update_details`** rebuilds (sync → **`get_dat()`** → setup/baking UI → per chain; cancel supported). **Create → Hair** layout aligned with chain **Build** rows; **Follicle** / **Hair system** use Project-style centered sub-headers (not nested frames). Per-chain **Targets** action row label (was Connect). Removed redundant per-chain **HairShape** collapsible (shape presets stay on **Details → Hair systems** menus).  
**Files**:
- EXTENDED: `cgm/core/tools/dynFKTool.py` — `_dynfk_progress_*`, **`with_progress`** on load/details; Create Hair + empty Details chrome
- EXTENDED: `Features/Feature_DynSimTool.md`, `Features/Feature_CgmToolUI.md`, `.cursor/rules/cgm-long-running-ui-progress.mdc`

**Status**: Code complete — Maya verify: multi-chain autoload shows progress; refresh without bar; HairShape only on hair-system rows

---

### September 17, 2026 - cgmSimChain Details layout + File menu
**What**: Polish **cgmSimChain** Details/header UI to match **Project → Paths** row chrome: pinned AnimClip-style **status row** (help **`MelButton`** setup name + **set_25** load selected); map rows use **set_25** / **select** + read-only help status buttons (not `<<` or disabled text fields). Reorganize **Baking** (label + stretch separator: **All Inputs** / **All Targets**, **Connect All** / **Disconnect All**) and per-chain rows (**Build** + **Push Settings to Build Menu**; **Advanced twist** + end-joint on one row; **Input** / **Connect** / **Chain** action rows). **File** menu: load applies on pick, save captures setup; **Setup** menu removed (dock + relaunch under **File → Tool**); duplicate **Tools → Apply Setup Dat** removed.  
**Files**:
- EXTENDED: `cgm/core/tools/dynFKTool.py` — `uiBuild_setup_status_row`, `uiFunc_make_load_row`, baking + chain action layout, `uiFunc_chain_push_build_to_create_options` on Build row
- EXTENDED: `Features/Feature_DynSimTool.md` — UI surface table, layout chrome note, changelog

**Features**:
- Header **Dynamic Chain System** label + icon cluster (refresh, load selected, select, clear)
- Details nucleus/cloth/hair/register rows: `MelSeparator` h=3, padding 5, help status + map/select icons
- Per-chain **Rebuild** / **Delete** on **Chain** row; hair **Input → Bake**; **Connect** bake/connect/disconnect trio

**Decisions**:
- Map **values** = non-interactive help **`MelButton`** (same bgc family as header status), not `MelTextField` or instruction-template stretch labels
- **Push build → Create** folded into **Build** row as **Push Settings to Build Menu** (no separate push row)

**Status**: Code complete — Maya verify: map row spacing/icons; cloth status label refresh; baking + chain actions; push-to-create after **Reload Dependencies**

---

### September 14, 2026 - cgmSimChain hair create hardening (Maya-verified)
**What**: Face26 bang/fringe **Make Dynamic Chain** path stabilized after spline-default rollout: **`addEndJoint`** through ensure/skin/MCD; sim joints parented **root→tip**; spline **driven** chain from **duplicate sim root**; incomplete chains surfaced in Details; dev reload split (backend vs tool UI); **`mc.*`** accepts DAG **strings** only at API edge.  
**Files**:
- EXTENDED: `cgm/core/rig/dynamic_utils.py` — `_hair_reparent_sim_chain_ordered`, sim **`p_parent`** create, `_hair_chain_integrity_missing`, `_dag_str` / follicle constraint driver strings, driven duplicate-root contract
- EXTENDED: `cgm/core/tools/dynFKTool.py` — broken-chain UI, **Push build → Create**, **Reload Dependencies** vs **Relaunch Tool**, **`getMessageAsMeta('mFollicle')`** on load
- EXTENDED: `Features/Feature_DynSimTool.md` — sim/driven contract, reload, broken chain, anti-patterns, checklist #21–22
- EXTENDED: `.cursor/rules/maya-cmds-strings-only.mdc`, **`cgm-runtime-meta-not-strings`** — **`asMeta=False`** / **`.mNode`** at **`mc.*`**

**Status**: ✅ Maya-verified — Edna 4-target bang + add end; spline IK past 3-joint gate; broken partial chain delete/recreate

---

### September 10, 2026 - cgmSimChain dat library (artist presets)
**What**: Shipped and tuned **`.cgmSim*Dat`** preset library under `cgm/cgmDat/sim/`; **Presets → Hair / Cloth / Nucleus** in dynFK now loads library files only (Python module menus removed). Capture fix for cloth/hair/nucleus from loaded setup **`mCloth`** / hair / nucleus messages. Hair and nucleus presets Maya-tuned on Edna test hair.  
**Files**:
- EXTENDED: `cgm/core/tools/dynFKTool.py` — library-first Presets menu; **Reset → Base**; `uiFunc_library_apply_by_name` (Details per-hair row dat menus added later — see Sept 15 multi hairSystem entry)
- EXTENDED: `cgm/core/lib/simChain_dat.py` — capture resolves mapped nodes from loaded cgmDynFK
- ADDED/EXTENDED: `cgm/cgmDat/sim/hair/*.cgmSimHairDat` — `bob`, **`bob_hold`**, `bangs_firm`, `shoulder`, `ponytail`, `long_flow`, `ribbon`, `tail`, **`tail_firm`**, `limb`, `rope` (+ user `bobTest` capture on disk)
- ADDED/EXTENDED: `cgm/cgmDat/sim/cloth/*.cgmSimClothDat` — Autodesk seeds: silk, chiffon, cotton, denim, leather, burlap; user `bangs_firm`, `bangs_2`
- ADDED/EXTENDED: `cgm/cgmDat/sim/nucleus/*.cgmSimNucleusDat` — `solver_balanced`, `solver_quality`, **`solver_high`**, `wind_calm`
- EXTENDED: `cgm/core/presets/cgmDynFK_presets.py` — synced **`bob`**, **`bob_hold`**, **`tail_firm`**, **`ponytail`** tuning; module header notes library is artist source
- EXTENDED: `cgm/core/tests/test_coreLib/test_SIMCHAIN.py` — library seed list + scan asserts
- EXTENDED: `Features/Feature_DynSimTool.md` — library-first UI, bob/bob_hold, solver tiers, verification checklist

**Features**:
- **Hair feel** (`.cgmSimHairDat`, `hs` only): **`bob`** = lively + blended hold; **`bob_hold`** = bobTest rest-shape; **`tail_firm`** vs legacy **`tail`**; retuned **`ponytail`**, **`ribbon`**
- **Cloth feel** (`.cgmSimClothDat`, `nc` only): material seeds + user bangs cloth dats
- **Nucleus sim** (`.cgmSimNucleusDat`, `n` only): **`solver_balanced`** → **`solver_quality`** → **`solver_high`**
- **Presets → Save * Dat…** — capture to library; **Query Settings** paste block for dat authoring
- **Section isolation**: hair dat never writes nucleus; cloth dat never writes nucleus; nucleus dat never writes hair/cloth

**Decisions**:
- Artist menu = dat library only; **`cgmDynFK_presets` / `cgmNCloth_presets`** kept for **`base`** seed + script `profile_load` / Query Settings diffs
- **`bobTest.cgmSimHairDat`** left as user capture; shipped equivalent is **`bob_hold`**
- Collision / `isDynamic` attrs omitted from library seeds — set in AE per scene

**Status**: Code complete — Maya verify: Edna **`bob`** / **`bob_hold`**; ponytail/ribbon/tail_firm on test chains; cloth + **`solver_high`** layered apply

---

## Deliverables

### Muzzle lip follow (in progress)
- [x] Distance-normalized lip-corner pointConstraint weights
- [x] Remove nostril from lip-corner influence targets
- [x] `prntConstraint` lip mid-follow rig path
- [x] `pntConstraint` split (point + orient) for default mid-follow
- [ ] Maya-verify prntConstraint vs ribbon vs parent on production muzzle profile
- [ ] Remove debug `pprint` from prntConstraint loop

### Eye block cleanup
- [x] `mParent` kw on lid handle creation (matches blockShapes_utils)
- [x] Drop unused lid shaper count defaults
- [x] Blendshape weight query without `cgm.lib.deformers`
- [x] `proxyBuild` / puppet mesh routing; `create_simpleMesh` module call fix
- [x] Eye lid tessellation — `get_meshFromNurbs` `general` mode (`numLidSplit_u` / `numLidSplit_v`)
- [ ] Broader eye rig constraint audit (if issues surface in production)

### Handle proxy geo + puppet unify (Oct 7)
- [x] **`geoOnly`** / **`geoAdd`** handle proxy paths; **`comboMesh`** → **`geoAdd`** normalize
- [x] **`_proxy_geo_unlock_for_edit`** before proxy geo **`colorControl`**
- [x] **`puppetMesh_create`** skinned + proxy **`polyUniteSkinned`**; unite result **`[0]`** fix
- [x] **`GEO.is_reversed`** mag-based normal (no **`normalizeList`** ZeroDivisionError)
- [x] Puppet normal-check routing on unified mesh (handle pre-unite; skip limb over-flip)
- [x] **`limb.build_proxyMesh`** returns **`ml_segProxy`**
- [ ] Maya-verify prop/handle **geoOnly** + **geoAdd** on production assets
- [ ] Maya-verify unified puppet mesh finger normals vs per-module proxy

### Face proxy / puppet mesh (in progress)
- [x] `meshBuild` + `proxyBuild` attrs on muzzle, brow, eye
- [x] `block_proxy_mesh_flow` + split skinned/proxy paths in `puppetMesh_create`
- [x] Muzzle `create_simpleMesh` (skinned puppet path)
- [x] Skin copy to puppet proxy dupes (muzzle, brow, eye)
- [x] Brow `numSplit_u` / `numSplit_v` on final mesh (`get_meshFromNurbs` general mode)
- [x] Eye lid tessellation parity with brow
- [x] `GEO.normalCheck` after mesh creation; `puppetMesh_normalCheck` / `puppetMesh_colorGeo` helpers
- [x] Proxy/puppet shaders via `CORERIG.color_mesh` (`'center'` fallback); skin-unify skips proxy mesh flow
- [x] Human-readable batch/rig timing (`get_timeString` / `get_timeLogString`)
- [ ] Maya-verify `proxyBuild` on (two skinned sets) vs off (single puppet mesh) on production face rigs
- [ ] Maya-verify inside-out normals fixed on muzzle lip nurbs tessellation + unified puppet mesh
- [x] Document face mesh contract — [`Feature_MRSMeshCreation.md`](../Features/Feature_MRSMeshCreation.md)

### Build / Scene (Face26)
- [x] `resolve_build_output_path` in batch utils
- [x] `SendToBuild` P4 prepare on existing BUILD output path

### MRS form — sub shaper track curves (Oct 7)
- [x] **`{p_nameBase}_seg_{i}_trackCrv`** rename in **`limb.py`** form sub-shaper loop
- [x] Same rename in **`block_utils.form_segment`** (handle / head / segment)
- [ ] Maya-verify two limbs in form with sub shapers (POC **`inputCurve`** on correct block curves)
- [ ] Optional: harden **`create_pointOnInfoNode`** / **`attachToCurve`** with full-path shape plugs

### Head neck — form aim + ribbon segment (Oct 7)
- [x] **`formAim`** / **`shapersAim`** / **`shapersAimUp`** on head block + neck **`form_segment`** wiring
- [x] Neck **`rig_segments`** ribbon **`_d`** parity with segment (**ribbonLive**, settings, **`parentDeformTo`**, **`setupAimScale`**, no **`additiveScaleEnds`** on squash dict)
- [x] **`IK.ribbon`** arcLength squash loop guards (**`ik_utils.py`**)
- [ ] Maya-verify head **`neckBuild`** + **ribbonLive** + squash/aim-scale rig build end-to-end
- [ ] Maya-verify neck form shaper loft aim with **`shapersAim`** / **`formAim`** enums vs segment feel

### TD toolbox / cgm menu (Oct 7)
- [x] **`rigging_utils`** — **`dag_lock`**, **`standard_attrs_hide`**, **`standard_attrs_unhide`**
- [x] **cgmToolbox** Rigging **Flags:** row (under **Group:**) — dagLock, dagUnlock, Hide Std, Unhide Std
- [x] **cgm menu** **Rigging Utils → Flags** — same four actions
- [x] **Query → Distance** — **`resultWarning`** on **`func_process`** for status-line readouts
- [ ] Optional: toolbox Near/Far distance buttons — same **`resultWarning`** if artists want parity with menu

### MRS scaleSetup dyn-parent + pivot naming (Face26)
- [x] Pivot result **`{partName}_pivotResult`** / **`{partName}_PivotResult`** (handle **`rig_frame`**, segment, limb ×2)
- [x] Document pivot result = **`pivotResultDriver`** message + **`pivots_setup`** **`pivotResult`** (same DAG null)
- [x] **`builder_utils`** attachPoint → dyn-parent default index + scaleSpace puppet helper
- [x] Wire head, segment, handle, limb rigRoot (+ handle main control)
- [x] IK/FK/mid **`{part}_root`** on base dyn parents when scaleSetup
- [x] TEMP digit bypass **`b_scaleSetupDynSpace`** (`_LIMB_TEMP_SKIP_SCALE_SETUP_DIGIT`)
- [ ] Maya-verify attach **end** → wrist (arm + prop handle)
- [ ] Maya-verify digit with temp flag off; remove temp when stable
- [ ] Maya-verify handle/segment with **addPivot** — outliner **`{partName}_pivotResult_*`** after module rebuild

### cgmSimChain / dynFK (Face26)
- [x] **`polyline_length_fractions`** + linear inCurve + joint-length POC sampling
- [x] Full-chain **`skinCluster`**; **`extendEnd=False`** default; extend arg **`None`** handling
- [x] Hair library **`bob`**, **`bob_hold`**, **`bangs_firm`**, full `.cgmSimHairDat` seed set
- [x] Cloth library seeds (silk–burlap) + user **`bangs_firm`** / **`bangs_2`** dats
- [x] Nucleus **`solver_balanced`**, **`solver_quality`**, **`solver_high`**
- [x] **`Feature_DynSimTool.md`** — segment-length contract + library preset patterns + Sept 11 bind/rebuild/sampling
- [x] **Hair bind-before-MCD** + post-MCD inCurve rebuild + outCurve rest sync
- [x] **Add-to-existing hairSys** — skinCluster + outCurve POC path (Edna bang/hairTip)
- [x] Create **Options → Fixed segment length** (default CV-matched sampling)
- [x] Create panel — **Cloth Options** header row; **Mesh track** cloth-only gating
- [x] **cgmSim*Dat** — `simChain_dat.py`; **Presets → Hair/Cloth/Nucleus** library-only UI
- [x] **cgmSimChainSetup** Phase 2 — capture/apply setup dat, **Presets → Setups**
- [x] Details UX — status row, Project-style map rows (**set_25** / **select**), Baking + per-chain **Input** / **Connect** / **Chain** action rows (Sept 17)
- [x] **File** menu load/save setup dat; dock + relaunch under **File → Tool**
- [x] **SimClothDat.capture** — resolves **`mCloth`** from loaded setup
- [x] Maya-verify dat capture Save/Load round-trip
- [ ] Maya-verify **`bob`** vs **`bob_hold`** on Edna production hair sim
- [ ] Maya-verify setup dat capture → reload scene → Apply Setup Dat on production rig
- [ ] Maya-verify cloth attach + **`bangs_firm`** on production hair cage / fringe panels

### BlockDat / facial blocks (planned)
- [ ] Non-destructive blockDat remap when adding prerig handles (e.g. cheek on muzzle) — ordered-list match today shifts indices
- [ ] Keyed / tagged handle identity instead of pure list order (design TBD)
- [ ] Document facial blockDat contract in a Feature doc when API stabilizes

### MetaHuman / export (out of scope unless pulled in)
- [ ] Factor stable facial helpers from `MetahumanFacial.py` into `face_utils` / `sdk_utils` (see Feature_Metahuman)

### Testing
- [ ] Muzzle rebuild — lipMidFollowSetup modes
- [ ] Eye prerig — lid handles with `mParent`
- [ ] Face batch post — `proxyBuild` off (skinned puppet mesh) on muzzle/brow/eye
- [ ] Face batch post — `proxyBuild` on (module + puppet proxy, skinned)
- [ ] Face batch post — skin-unify path (no per-block proxy dup; normals + `color_mesh` on unified geo)
- [ ] Brow mesh density — `numSplit_u` / `numSplit_v` on final geo
- [ ] Regression: existing muzzle blockDat load + rig on shipped character
- [x] cgmSimChain — **Presets → Hair → bob** / **bob_hold** on test hair rig; Save Dat round-trip
- [x] cgmSimChain — add hair chain to **existing** hairSys; frame 0 inCrv/outCrv on joints (Edna verify)
- [ ] cgmSimChain — cloth attach + nCloth **`bangs_firm`** on head-follow cage
- [ ] cgmSimChain — setup dat capture + **File → Load Dat** (apply on pick) on production cloth attach rig
- [x] cgmDynSimTool — Details map/baking/chain action rows + load progress (Sept 18 polish)

---

## PR Notes

### Face26 — MRS facial block improvements (muzzle, brow, eye)

#### Overview
Face26 work hardens muzzle lip mid-follow (new `prntConstraint` mode, distance-weighted corner influences), aligns eye prerig with the shared `mParent` face-handle contract, adds a configurable face proxy/puppet mesh pipeline for muzzle/brow/eye (normals, `color_mesh` shaders, skin-unify routing), and extends **cgmSimChain** with dynFK hair-chain segment matching, a shipped **`.cgmSim*Dat` preset library** (hair/cloth/nucleus), and Edna-tuned **`bob`** / **`bob_hold`** hair presets. Branch includes merges from AnimData and SpringCleaning.

#### Major changes

##### 1. Muzzle lip mid-follow
- New `lipMidFollowSetup` mode: **prntConstraint** (parentConstraint + aim along chain)
- Default fallback path uses **pointConstraint + orientConstraint** instead of parentConstraint
- Lip-corner influences: distance-normalized weights via `distance_utils.get_normalizedWeightsByDistanceToObj`; `nostril` removed from target list

**Files**: `cgm/core/mrs/blocks/organic/muzzle.py`, `cgm/core/lib/distance_utils.py` (caller only)

##### 2. Eye prerig parameter fix
- `create_lidHandle`: `mStateNull` → `mParent`
- Removed dead `numLid*Shapers` defaults; blendshape attrs via `mc.listAttr`

**Files**: `cgm/core/mrs/blocks/organic/eye.py`

##### 3. Face proxy / puppet mesh pipeline
- **`proxyBuild`** on muzzle/brow/eye: proxy mesh workflow when on; skinned puppet mesh (`create_simpleMesh`) when off (default)
- **`block_proxy_mesh_flow`** in `block_utils`; `puppetMesh_create` / `proxyMesh_verify` honor per-block routing
- `build_proxyMesh`: `simpleMeshMode`, `puppetMeshMode`, skin copy on puppet dupes
- Brow final mesh uses `get_meshFromNurbs` **general** mode (`numSplit_u` / `numSplit_v`)
- **`puppetMesh_normalCheck`** / **`puppetMesh_colorGeo`**: shared post-create normal fix + `CORERIG.color_mesh` proxy shaders (`'center'` when side unknown)
- **`GEO.normalCheck`** after muzzle nurbs tessellation and `create_simpleMesh` loft output
- Skin-unify (`skin=True`): proxy mesh flow disabled — unified skinned puppet path only

**Files**: `muzzle.py`, `brow.py`, `eye.py`, `block_utils.py`, `puppet_utils.py`, `shared_dat.py`

##### 4. Timing log formatting
- **`get_timeString`** / **`get_timeLogString`** in `cgm_General` — human-readable elapsed time in batch post-process reports and rig timing

**Files**: `cgm_General.py`, `batch_utils.py`, `RigBlocks.py`

##### 5. Build output path + Scene send-to-build
- `batch_utils.resolve_build_output_path` — version file → `*_BUILD.mb` sibling
- `Scene.SendToBuild` — `PATHUTIL.prepare_maya_scene_for_save` on existing BUILD output before MRS Build

**Files**: `batch_utils.py`, `Scene.py`

##### 6. cgmSimChain — dynFK segment length + presets
- **`CURVES.polyline_length_fractions`**: chord-length 0–1 fractions for polyline joint spacing
- **`chain_create_hair`**: **`curveLinear`** inCurve; POC **`turnOnPercentage`** from joint fractions; full-chain **`skinCluster`**; **`extendEnd=False`** default; explicit **`None`** handling for extend args
- **`cgmDynFK_presets`**: **`bob`**, **`bangs_firm`** (hair feel); **`d_profileKind`** mappings
- **`cgmNCloth_presets`**: fabric **`bangs_firm`** (stretch/compression firm, soft bend, damp 1.0, subtle input attract); **`d_profileKind`** mapping
- **`Feature_DynSimTool.md`**: segment-length contract, preset patterns, cloth input-attract anti-pattern

**Files**: `curve_Utils.py`, `dynamic_utils.py`, `cgmDynFK_presets.py`, `cgmNCloth_presets.py`, `Features/Feature_DynSimTool.md`

##### 7. cgmSimChain — cgmSim*Dat preset library (Phase 1 + artist cutover)
- **`simChain_dat.py`**: `SimHairDat` / `SimClothDat` / `SimNucleusDat` JSON under `cgm/cgmDat/sim/`
- **`profile_apply_section`**: dict apply on hairSystem / nCloth / nucleus (section-isolated; same skip/base/gravity contract as module presets)
- **dynFKTool**: **Presets → Hair / Cloth / Nucleus** = library scan + apply; **Save * Dat…** capture; **Reset → Base**; Python preset submenus removed (Sep 10)
- **Shipped seeds**: hair (`bob`, `bob_hold`, `bangs_firm`, `ponytail`, `ribbon`, `tail_firm`, …); cloth (silk–burlap); nucleus (`solver_balanced`, `solver_quality`, `solver_high`, `wind_calm`)
- **Capture fix**: `SimClothDat` / hair / nucleus capture uses loaded setup mapped nodes

**Files**: `simChain_dat.py`, `nCloth_utils.py`, `dynamic_utils.py`, `dynFKTool.py`, `cgm/cgmDat/sim/**`, `test_SIMCHAIN.py`, `Features/Feature_DynSimTool.md`

##### 8. cgmSimChain — hair preset tuning (Edna test hair)
- **`bob`**: lively (low drag/mass) + blended rest-shape hold from bobTest comparison
- **`bob_hold`**: bobTest capture values — max return-to-form when **`bob`** drifts
- **`ponytail`**, **`ribbon`**, **`tail_firm`**: retuned from legacy module seeds (underwater / anti-gravity / appendage defaults)

**Files**: `cgm/cgmDat/sim/hair/*.cgmSimHairDat`, `cgmDynFK_presets.py`, `Features/Feature_DynSimTool.md`

##### 9. cgmSimChain — hair bind/rebuild + add-to-existing hairSys (Sept 11)
- **`chain_create_hair`**: skin inCurve **before** `makeCurvesDynamic`; post-MCD **`_consolidate_hair_incurve_after_mcd`** (rebuild linear inCurve, wire **`startPosition`**, 1:1 CV skinPercent)
- **outCurve rest**: **`restPose`** Same As Start + **`CURVES.match`** inCurve → outCurve at frame 0
- **Follicle sampling**: default **`sampleDensity=1`**, **`fixedSegmentLength=off`**; optional Create **Options → Fixed segment length** (`segmentLength` default 1.0)
- **Existing hairSys**: up/aim POC on **outCurve** (inCurve loses transform **`worldSpace`** after MCD); **`get_dat` `mInCrv`** from chain grp
- **Hierarchy contract**: inCrv on **chain grp**; root sim joint → follicle; **`parentConstraint`** to rig — no follicle snap + relative inCrv reparent

**Files**: `dynamic_utils.py`, `dynFKTool.py`, `simChain_dat.py`, `Features/Feature_DynSimTool.md`, `Features/Feature_CgmToolUI.md`

##### 10. cgmSimChain — Details / Baking UI layout (Sept 17)
- Pinned header status row; map rows aligned with **Project** paths pattern (**set_25**, help status button, **select**)
- Setup **Baking** and per-chain connect/bake/rebuild/delete as label + separator button rows
- **File** menu owns setup dat load/save + tool dock/relaunch

**Files**: `dynFKTool.py`, `Features/Feature_DynSimTool.md`

##### 11. MRS scaleSetup dyn-parent + pivot naming (Oct 7)
- See timeline **October 7, 2026** — amend **`####`** subsections there (shared helpers, attachPoint, pivot naming, digit temp bypass)
- **Files**: `builder_utils.py`, `head.py`, `segment.py`, `handle.py`, `limb.py`, `block_utils.py` (`pivots_setup`)

##### 12. Form sub shaper track curves — per-block naming (Oct 7)
- See timeline **October 7, 2026** — **`#### Form sub shaper track curves`**
- **Files**: `limb.py`, `block_utils.py` (`form_segment`); related **`blockShapes_utils.attachToCurve`**, **`curve_Utils.create_pointOnInfoNode`**

#### Merged dependencies (separate PR notes)
- **AnimData** — see [`Branch_AnimData.md`](Branch_AnimData.md)
- **SpringCleaning** — see [`Branch_SpringCleaning.md`](Branch_SpringCleaning.md)

#### Breaking changes
None intended — new enum values and rig paths are opt-in via block attrs. Existing face blocks without `proxyBuild` attr behave as puppet mesh path (off).

#### Next steps
- Maya-verify prntConstraint on production characters
- Maya-verify eye lid mesh density via `numLidSplit_u` / `numLidSplit_v`
- Maya-verify skin-unify puppet mesh normals + side-colored shaders on production face rigs
- Design blockDat key-based remap for new prerig handles (cheek, etc.)
- Maya-verify cgmSimChain **`bob`** vs **`bob_hold`** on Edna production hair sim
- Maya-verify cgmSimChain **`bangs_firm`** hair + nCloth on production fringe / hair-cage rigs
- Phase 2: **`cgmSimChainSetup`** — shipped; production rig verify pending
- Consider Feature doc for facial MRS blocks when blockDat / mesh contract is settled
- Maya-verify scaleSetup dyn-parent **attachPoint** on limb/handle; remove **`_LIMB_TEMP_SKIP_SCALE_SETUP_DIGIT`** when digit stable

---

## Notes

### Context from prior exploration
Facial blocks store blockDat by **ordered lists**; adding a prerig handle (e.g. cheek) shifts indices and breaks non-destructive load. A keyed remap layer in `block_utils` / per-block `blockDat_load_state` is the likely fix — deferred until after lip-follow stabilization.

### Architectural patterns
- Face handle parent kw is **`mParent`** (not `mStateNull`) — match `blockShapes_utils`
- Lip mid-follow modes: `ribbon` | `prntConstraint` | `pntConstraint` | `parent`
- Face mesh: **`meshBuild`** (any mesh) + **`proxyBuild`** (proxy vs skinned puppet path); default `proxyBuild=False` on muzzle/brow/eye
- Batch post: `proxyMesh_verify` (module proxy) then `puppetMesh_create(unified=True, skin=True, proxy=True)` — face blocks with `proxyBuild` off skip step 1 and use `create_simpleMesh` in step 2
- Puppet mesh post-create: **`puppetMesh_normalCheck`** → **`puppetMesh_colorGeo`** (`CORERIG.color_mesh`, side or `'center'`)
- Skin-unify: `block_proxy_mesh_flow` skipped when `skin=True` in `puppetMesh_create` (no proxy dup during unified skin path)
- Elapsed-time logs: **`cgmGEN.get_timeString`** / **`get_timeLogString`** (batch totals append raw seconds when ≥ 1 min)
- Brow/eye tessellation: `RIGCREATE.get_meshFromNurbs` — **`mode='general'`** respects `uNumber`/`vNumber`; **`mode='default'`** hardcodes 3×3
- Constraint weight queries: `mc.parentConstraint` / `mc.pointConstraint` with `q=True, weightAliasList=True` only (no invalid query flags)
- **cgmSimChain hair chain**: linear **`curveLinear`** inCurve; bind **before** MCD; post-MCD rebuild + **`startPosition`** wire; outCurve rest sync; inCrv on **chain grp**
- **Follicle sampling default**: **`fixedSegmentLength=off`**, **`sampleDensity=1`** (CV-matched); optional Create **Options → Fixed segment length**
- **Add-to-existing hairSys**: POC / up-aim on **outCurve**; full-chain **`skinCluster`** before MCD
- **Last-joint aim default**: forward tangent offset at tip (**`+fwd`**) when **`extendEnd=False`**
- **cgmSim*Dat library**: `.cgmSimHairDat` / `.cgmSimClothDat` / `.cgmSimNucleusDat` under **`cgm/cgmDat/sim/`**; **Presets → Hair / Cloth / Nucleus** + **File** Save/Load (Maya-verified)
- **cgmSimChainSetup Phase 2**: `.cgmSimChainSetup` under **`cgm/cgmDat/sim/setups/`**; **File → Load / Save Dat** (load applies on pick), **Presets → Setups**
- **dynFK Details UI**: help status **`MelButton`** + **set_25** / **select** map rows; **Baking** + per-chain **Input** / **Connect** / **Chain** label rows — see **`Feature_DynSimTool.md`** UI Surface
- **dynFK hair feel**: **`bob`** (lively volume), **`bob_hold`** (rest-shape), **`bangs_firm`** (fringe) — **Presets → Hair**
- **Nucleus solver tiers**: **`solver_balanced`** → **`solver_quality`** → **`solver_high`** — **Presets → Nucleus** (never bundled into hair/cloth dats)
- **nCloth short panels**: fabric **`bangs_firm`** — high stretch/compression, low bend, moderate damp; **`inputMeshAttract` ≤ ~0.08** on head-follow cages (not **`inputAttract`** preset)
- **scaleSetup dyn-parent**: default enum from block **attachPoint** on rebuilt **`dynParents`**; digit limbs gated by **`_LIMB_TEMP_SKIP_SCALE_SETUP_DIGIT`** until finger attach verified
- **Pivot result naming**: **`{partName}_pivotResult`** on the same DAG null as **`pivotResultDriver`**; created in handle **`rig_frame`** (not prerig); **`pivots_setup`** parents that null at end of pivot chain — rebuild module for new names
- **Handle proxyType**: **`geoOnly`** = Proxy Geo only; **`geoAdd`** = cast + Proxy Geo (legacy **`comboMesh`**); **`proxyGeo_add`** unlocks override attrs before **`color_mesh`** / **`colorControl`**
- **Puppet unify**: handle skinned + limb proxies via **`polyUniteSkinned`**; **`puppetMesh_normalCheck`** scoped on unified path to avoid double-flipping limb proxy geo
- **Form sub shaper track curves**: rename **`{p_nameBase}_seg_{i}_trackCrv`** so POC **`inputCurve`** does not collide when multiple blocks are in form; shared path **`UTILS.form_segment`** + limb inline form
- **Head neck form aim**: same **`formAim`** / **`shapersAim`** / **`shapersAimUp`** contract as segment — wired through **`form_segment`** when **`neckBuild`**
- **Head neck segment ribbon**: **`rig_segments`** **`IK.ribbon`** kwargs match segment; **`additiveScaleEnds`** not tied to **`scaleSetup`** on head squash dict (live surface + aim **`scaleZ`**)
- **TD rig flags**: **`RIGGING.dag_lock`** / **`standard_attrs_*`** → **`cgmObject`**; toolbox + **Rigging Utils → Flags**
- **Query distance UX**: **`func_process(..., resultWarning=True)`** → **`log.warning`** for **Query → Distance** (not **Surface Nodes**)

---

*Last Updated: October 7, 2026 (TD toolbox/menu rig flags; Query distance warnings; head neck ribbon; Builder scene-load; form trackCrv; scaleSetup; handle proxy; puppet mesh)*  
*Branch Status: Active*
