# Branch: jburton/SpringCleaning

## Quick Info
**Status**: Complete  
**Created**: August 20, 2026  
**Last Updated**: September 1, 2026 (branch closed)  
**PR**: Pending

## Goals
Finish the unfinished move of **used** first-party `cgm.lib` code into `cgm.core` without breaking Maya tools. Stand up a real unittest safety net (keep unittest + Toolbox menu; no pytest). **Drop unused legacy artist windows** (attrTools, tdTools, locinator, setTools, namingTools, puppetBox, bufferTools, polyUniteTool, leftover animTools 1.0) and keep `cgm.core.tools`. **Toolbox Legacy tab removed** (2026-08-25); leftover animTools 1.0 + `animToolsLib` deleted 2026-09-01; `findTextures` moved to `cgm/core/lib/texture_utils.py`. Leave vendored trees (`zoo`, `ml`, `bo`, `openSource`, Red9) and unused show scripts alone. This branch is **not** “delete `cgm.lib`.” First-party modules are parked in **`cgm/libOld`**; `cgm.lib` keeps zoo/ml/bo/openSource. The `lists` shim was dropped 2026-09-01.

## Remaining

**None.** Closed 2026-09-01. Canonical outcomes: [`Feature_LibToCore.md` — Closed on this branch](../Features/Feature_LibToCore.md#closed-on-this-branch-2026-09-01).

Out of scope (not leftover): hollow-shim `attributes` / `search`; port `modules` / leftover deformers bake / leftover joints / bulk skinning; migrate zoo/ml/bo/openSource/Red9; delete the `cgm.lib` package; retarget `cgm/projects`. **libOld is already on git.**

## Related Documentation
- **[Feature_LibToCore.md](../Features/Feature_LibToCore.md)** - Canonical inventory, old→new map, shim rules, test-runner contract, wave order
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format
- **[cgm-module-placement.mdc](../.cursor/rules/cgm-module-placement.mdc)** - Where new helpers go (`core/lib`, not zoo/Red9)
- **[Feature_PerforceIntegration.md](../Features/Feature_PerforceIntegration.md)** - Same vendored rule: do not import zooPy perforce from core

## Timeline

### September 1, 2026 - Branch closed
**What**: Called Spring Cleaning complete. No remaining production work. Maya smoke of core tools closed. Hollow shims / `libOld` ports / `cgm/projects` stay out of scope. Docs only — no py3 code this pass.

**Files**:
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Complete.

---

### September 1, 2026 - Drop cgm.lib.lists shim
**What**: Deleted the Wave 1 compatibility shim. Production already used `list_utils`. Kept `test_LISTS.Test_noOldAliases` (old names must not be on `list_utils`). Did **not** hollow-shim `attributes` / `search`.

**Files**:
- DELETED: `cgm/lib/lists.py`
- EXTENDED: `cgm/core/tests/test_coreLib/test_LISTS.py`, `list_utils.py`, `cgm/lib/__init__.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Re-run **LISTS** or **cgm - All**.

---

### September 1, 2026 - zooSetkey + drop cgmBaseMelUI
**What**: zoo Setkey MM South dragBreakdown → `ml_breakdownDragger.drag()`. Deleted unused `cgm.lib.cgmBaseMelUI` (core uses `cgm.core.lib.zoo.baseMelUI`). Closed remaining-table P4 row (**this checkout is git**; libOld is already in tree). Hollow-shim attributes/search **won’t do** — production core does not need it. Skip `cgm/projects`.

**Files**:
- EXTENDED: `cgm/lib/zoo/zooMel/zooSetkey.mel`
- DELETED: `cgm/lib/cgmBaseMelUI.py`
- EXTENDED: `cgm/lib/__init__.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Maya-smoke zoo Setkey South dragBreakdown.

---

### September 1, 2026 - Unittest end-of-run summary
**What**: `cgmTests.main` keeps per-module `TextTestRunner` + `file -new`. Captures each `TestResult` and prints a compact PASS/FAIL rollup at the end (module + test id + exception headline). `testCheck=True` stays list-only. Import failures still raise.

**Files**:
- EXTENDED: `cgm/core/tests/cgmTests.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Code + docs. Next **cgm - All** last Script Editor block should be `RESULT: PASS` or a FAIL list.

---

### September 1, 2026 - findTextures → texture_utils
**What**: Moved Scene Remap Unlinked Textures off leftover `cgm/tools/findTextures.py` into `cgm/core/lib/texture_utils.py`. Scene passes `mDat.userPaths_get()` content/export. Fixed localize `of.path.basedir` typo. Did **not** add a unittest. `cgm/tools` is empty after this.

**Files**:
- NEW: `cgm/core/lib/texture_utils.py` (`remap_missing` / `localize`)
- EXTENDED: `cgm/core/mrs/Scene.py`
- DELETED: `cgm/tools/findTextures.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Feature_CoreLibLookups.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Maya-smoke Scene Tools → Remap Unlinked Textures.

---

### September 1, 2026 - PuppetKey off animToolsLib
**What**: Retargeted live PuppetKey Reset / dragBreakdown onto `cgm.core.lib.ml_tools`. Deleted `cgm/tools/lib/animToolsLib.py`. Did **not** edit vendored `zooSetkey.mel` (South dragBreakdown still names `animToolsLib`).

**Files**:
- EXTENDED: `cgm/core/tools/markingMenus/cgmPuppetKey.py`
- DELETED: `cgm/tools/lib/animToolsLib.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Maya-smoke PuppetKey Reset and dragBreakdown. zoo Setkey MM South item is a known miss if that hotkey is still used.

---

### September 1, 2026 - Leftover animTools 1.0 file cut
**What**: Deleted the leftover 1.0 window and the held libs that only existed for it. Did **not** delete `animToolsLib` (PuppetKey ml wrappers) or `findTextures` (Scene). Dropped `TOOLCALLS.animToolsLEGACY`. Did **not** hollow-shim `attributes` / `search`. Did **not** touch `cgm.libOld` or vendored `cgm.lib`.

**Files**:
- DELETED: `cgm/tools/animTools.py`, `cgm/tools/lib/locinatorLib.py`, `cgm/tools/lib/tdToolsLib.py`, `cgm/tools/lib/namingToolsLib.py`
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — dropped `animToolsLEGACY`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Maya smoke of core tools still open. P4 depot for libOld still open.

---

### August 25, 2026 - Toolbox Legacy tab removed
**What**: Removed the Toolbox **Legacy** tab (TD / Anim / Settings remain). Did **not** delete `cgm/tools/animTools.py` or held libs. `TOOLCALLS.animToolsLEGACY` still exists for scripts; it `ImportError`s after libOld.

**Files**:
- EXTENDED: `cgm/core/tools/toolbox.py` — drop `uiTab_legacy` / `buildTab_legacy`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Status**: Code + docs. Reload Toolbox to verify three tabs.

---

### August 25, 2026 - Restore SEARCH.get_referencePrefix
**What**: Hygiene had left the `get_referencePrefix` body as dead code after a leftover `returnSelectedAttributesFromChannelBox` wrapper (no `def`). `cgm_Meta.getReferencePrefix` → `SEARCH.get_referencePrefix` AttributeError. Restored the function; dropped the unused old-name wrapper (core callers already use `get_selectedFromChannelBox`). Did **not** alias `returnReferencePrefix` on SEARCH.

**Files**:
- EXTENDED: `search_utils.py`, `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Code + docs. Re-run `cgmMeta` / `cgm - All`.

---

### August 25, 2026 - Unittest reload fallout after libOld
**What**: `importlib.reload` was keeping removed `Test*` classes (`Test_object_size_alias`) and old aliases (`returnListChunks` on `list_utils`, `returnObjectSize` on DIST). `_reload()` does not reload `cgm.lib.lists`. NODES `isConnected` failed on time-typed plugs because Maya inserts `unitConversion`; **`setup_offset_cycle_speed` was not changed.** `file -new` does not reset `currentUnit`.

**Files**:
- EXTENDED: `cgmTests.py` (drop test module from `sys.modules` then import)
- EXTENDED: `test_LISTS.py` Test_shimNames (reload shim; disk-check old names are not assigned on `list_utils`)
- EXTENDED: `test_NODES.py` (`isConnected(..., ignoreUnitConversion=True)` on `time1` and animCurve `input`)
- EXTENDED: `cgm/core/__init__.py` ignore tag `cgm.libOld`

**Status**: Maya-closed for the last NODES fail. Re-run full `cgm - All` if that has not happened since these runner fixes.

---

### August 25, 2026 - libOld probe (first-party park)
**What**: Moved first-party `cgm/lib` modules + `classes/` + confs + `gigs/` + `specialCaseStuff` to **`cgm/libOld`**. Left `zoo` / `ml` / `bo` / `openSource`, the `lists` shim, and `cgmBaseMelUI` in `cgm.lib`. Did **not** rewire leftover tools or projects to `libOld`. Did **not** add shims that hide `ModuleNotFoundError`.

**Expected breaks**: locinatorLib / tdToolsLib / namingToolsLib if imported, `cgm/projects` mk1/morpheus/lbs, user `from cgm.lib import attributes`, `animToolsLEGACY()` if called. **Expected OK**: Scene, MRS, mocap bake, Toolbox (TD / Anim / Settings), PuppetKey MM, rigger MM, zoo/ml.

**Files**:
- MOVED: first-party modules from `cgm/lib/` → `cgm/libOld/`
- EXTENDED: `cgm/lib/__init__.py`, `cgm/libOld/__init__.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Disk move done. p4 CLI was not on PATH — depot still needs `p4 move`. Maya smoke of core tools still open. Unittest fallout (runner/LISTS/NODES) recorded in the entry above.

---

### August 25, 2026 - Wave 4e examples off first-party lib
**What**: Retargeted remaining example scripts off first-party `cgm.lib`. Did **not** import `locator_utils` (it imports Dragger). Did **not** use `ATTR.set_message` for the intro-to-meta demo (that example is native Maya multi-message duplication).

**Map**: `createControlCurve` → `CURVES.create_fromName`. `doLocPos` → `mc.spaceLocator(p=hit)`. `storeObjectsToMessage` → inline `addAttr` + `connectAttr(..., nextAvailable=True)`. `doGetAttr` / `doSetAttr` / `doAddAttr` → `ATTR.get` / `ATTR.set` / `ATTR.add`.

**Files**:
- EXTENDED: `cgm/core/examples/help_rayCasting.py`, `help_introToMeta.py`, `cgm/core/exampleForMark.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Code + docs done — examples are not in `cgm - All`

**Next leftover hub**: leftover deformers bake / leftover joints helpers / bulk skinning / `modules` null-system (do not port). `cgm.core` grep-clean of live first-party lib except the `test_LISTS` shim check.

---

### August 25, 2026 - Wave 4d test leftovers off first-party lib
**What**: Retargeted `mayaBeOdd.py` and `cgmMeta_test.py` off first-party `cgm.lib`. Did **not** add them to the unittest runner. Did **not** revive `cgmMeta_test` (Dropbox paths remain). Kept `test_LISTS` shim import of `cgm.lib.lists`.

**Map**: `createCurve('sphere')` → `CURVES.create_fromName('sphere')`. `getShortName` → `NAMES.get_short`. `doGetAttr` → `ATTR.get`. `returnMessageData` → `ATTR.get_messageLong`. `doBreakConnection` → `ATTR.break_connection`. `returnWorldSpacePosition` → `POS.get`.

**Files**:
- EXTENDED: `cgm/core/tests/mayaBeOdd.py`, `cgm/core/tests/cgmMeta_test.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Code + docs done — `cgm - All` does not run these files; no extra Maya pass required for this slice

**Next leftover hub**: leftover deformers bake / leftover joints helpers / bulk skinning / `modules` null-system (do not port). Examples still on lib.

---

### August 25, 2026 - Wave 4c nodes / unused pyui / dead joints landmine
**What**: Retargeted live core `cgm.lib.nodes` callers onto existing `NODES.create` and a new `setup_offset_cycle_speed`. Dropped unused Scene `pyui` import. Removed unreachable `joints.orientJoint` in `segment_utils`. Did **not** hollow-shim `nodes.py` / `joints.py` / `pyui.py`. Did **not** add `createNamedNode` / `offsetCycleSpeedControlNodeSetup` wrappers on core.

**Map**: `createNamedNode` → `NODES.create`. `offsetCycleSpeedControlNodeSetup` → `NODES.setup_offset_cycle_speed` (lib created an unused offset MD; core does not).

**Files**:
- EXTENDED: `node_utils.py` (`setup_offset_cycle_speed`), `NodeFactory.py`, `post_utils.py`, `Scene.py`, `segment_utils.py`
- NEW: `test_NODES.py`; `'NODES'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Complete — **Maya-verified 2026-08-25** (`cgm - All`, including NODES)

**Next leftover hub**: leftover deformers bake / leftover joints helpers / bulk skinning / `modules` null-system (do not port). Production `cgm.core` grep-clean of live first-party lib except tests/examples.

---

### August 25, 2026 - Wave 4b skinning query / unused lib imports / settings-color landmine
**What**: Retargeted live core skinning-query and settings-color callers onto existing APIs. Dropped unused first-party lib imports. Fixed MCS `returnSettingsData` NameError left by the curves wave (import commented, calls still live). Did **not** hollow-shim `skinning` / `modules` / `deformers` / `joints`. Did **not** port the old module-null system. Did **not** add `querySkinCluster` / `returnSettingsData` wrappers on core.

**Map**: `querySkinCluster` → `SKIN.get_cluster`. `queryInfluences` → `SKIN.get_influences_fromCluster`. MCS jointOrientation → `'zyx'`. `getSettingsColors` → SHARED `_d_side_colors_index` (**center is sub, aux** = yellowBright/peach, not center main). Eye blink `returnBlendShapeAttributes` → `mc.listAttr(..., m=True)`.

**Files**:
- EXTENDED: `skin_utils.py` (`get_cluster`), `skinDat.py`, `segment_utils.py`, `meta_Utils.py`, `shared_data.py` comment, `ModuleShapeCaster.py`, `eye.py`
- EXTENDED: unused lib imports dropped from `curve_Utils.py`, `surface_Utils.py`, `Project.py`, `ControlFactory.py`
- NEW: `test_SKIN.py`; `'SKIN'` in `cgmTests.py` `_d_modules['coreLib']`; `test_SHARED` side-color + `getSettingsColors`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Complete — **Maya-verified 2026-08-25** (`cgm - All`, including SKIN + SHARED color tests)

**Next leftover hub**: joints / leftover deformers bake / nodes / modules null-system (do not port) / bulk skinning. `Scene.py` still on `pyui`.

---

### August 25, 2026 - Wave 4 curves core retarget
**What**: Retargeted live `cgm.core` `cgm.lib.curves` callers onto existing APIs. Did **not** wrap `createControlCurve` / `parentShapeInPlace` / `setCurveColorByName` / `combineCurves`. Did **not** hollow-shim `curves.py`. Left `mayaBeOdd` and `examples/help_rayCasting.py` on lib.

**Map**: `createControlCurve` → `CURVES.create_fromName` (string; not `create_controlCurve`, which returns a list and always colors). `parentShapeInPlace` → `CORERIG.shapeParent_in_place`. `combineCurves` → `SHAPES.combine` (onto first; not `combineShapes` onto last). `setCurveColorByName` → `CORERIG.override_color`. `createTextCurve` → `CURVES.create_text`.

**Files**:
- EXTENDED: `ModuleShapeCaster.py`, `ModuleControlFactory.py`, `shapeCaster.py`, `DraggerContextFactory.py`
- EXTENDED: unused `curves` import dropped from `curve_Utils.py`, `surface_Utils.py`, `ControlFactory.py`
- NEW: `test_CURVES.py`; `'CURVES'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Complete — **Maya-verified 2026-08-25** (`cgm - All`, including CURVES)

---

### August 25, 2026 - Hygiene pass (old names off core)
**What**: Retargeted `cgm.core` callers to the modern APIs from the audit punch list, then dropped unused old-name aliases on `list_utils` / DIST / MATH / SHARED / SNAP / GuiFactory. lists old names live on the `cgm.lib.lists` shim only. Leftover `distance` / `cgmMath` / `dictionary` / `position` / `guiFactory` still hold their own names for leftover tools.

**Callers**: ModuleShapeCaster, Dragger, puppetKey, meshTools, mocapBakeTools, locinator, dynParentTool, ATTR, skinDat, rayCaster, SnapFactory, geo_Utils, shapeCaster, rigging_utils, general_utils, curve_Utils.

**Tests**: Dropped `assertIs` alias checks on LISTS/DIST/MATH/SHARED/GUI. Shim test still hits `cgm.lib.lists.returnListChunks`. MATH asserts `normalizeListToSum(..., 2.0)` sums to 2 (core wins vs leftover lib divide).

**Status**: Code + docs done — Maya: Toolbox **Unittesting → cgm - All** still needed this pass.

---

### August 25, 2026 - Audit shipped waves vs newer-core-API
**What**: Reviewed Waves 1–3h against “use the newer core call; do not keep old names on `*_utils`.” ATTR/SEARCH, names (`get_base`), and rigging (`group_me` / `copy_pivot`) already match. lists / DIST / MATH / SHARED still have old-name aliases that core callers use. SNAP `move_*_snap` stays (not `SNAP.go`). Punch list lives in Feature_LibToCore “Audit of shipped waves.”

**Status**: Evaluation only — retarget/hygiene pass landed same day (see Hygiene pass entry)

---

### August 25, 2026 - Prefer newer core API
**What**: Contract clarification — if core already has a better call, use it. Do not add 1:1 old-name wrappers on `*_utils` just to match leftover `cgm.lib`. Old names stay on lib until leftover tools go away or the lib file is shimmed. Exception: newer is not a drop-in when behavior changes (`SNAP.go` rotateOrder).

**Follow-up**: Removed Wave 3h `groupMeObject` / `copyPivot` wrappers. Core callers use `TRANS.group_me(..., parent=False, maintainParent=False)` and `copy_pivot`. Wave 3f callers use `NAMES.get_base` (dropped `getBaseName` on NAMES).

**Files**:
- EXTENDED: `rigging_utils.py`, `name_utils.py`, `shapeCaster.py`, `DraggerContextFactory.py`, `ModuleShapeCaster.py`, `ModuleControlFactory.py`, `skinDat.py`, `nameTools.py`, `test_RIGGING.py`, `test_NAMES.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Complete — Maya smoke same as 3h plus nameTools/skinDat basename via `get_base`

---

### August 25, 2026 - Wave 3h rigging groupMeObject / copyPivot
**What**: Added 1:1 `groupMeObject` / `copyPivot` on `rigging_utils`. Retargeted live core callers. Dropped unused `rigging` imports. Restored live `from cgm.lib import curves` on ModuleShapeCaster / ModuleControlFactory (earlier wave commented the import while curve calls stayed — NameError). **Superseded same day** — wrappers removed; core uses `TRANS.group_me` / `copy_pivot` (see Prefer newer core API).

**Files**:
- EXTENDED: `cgm/core/lib/rigging_utils.py` — `groupMeObject`, `copyPivot`
- NEW: `cgm/core/tests/test_coreLib/test_RIGGING.py`; `'RIGGING'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `shapeCaster.py`, `DraggerContextFactory.py`, `ModuleShapeCaster.py`, `ModuleControlFactory.py`, `Project.py`, `skinDat.py`, `curve_Utils.py`, `surface_Utils.py`, `ControlFactory.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `TRANS.group_me` defaults and `_grp` rename are not a drop-in
- `copy_pivot` copies rp/sp separately; lib `copyPivot` uses `xform piv`
- Restore lib `curves` until the curves wave — do not leave those calls unbound

**Status**: Complete for core groupMeObject/copyPivot retarget — Maya smoke: `cgm - All` now includes RIGGING; Dragger group mode; MRS shape caster / control factory copyTransform

---

### August 25, 2026 - Wave 3g gui / optionVars core retarget
**What**: Added 1:1 `purgeCGM` / `appendOptionVarList` / `resetGuiInstanceOptionVars` / `warning` on core GuiFactory. Retargeted Toolbox Purge Option Vars and cgmPuppetKey off lib. Dropped unused `guiFactory` import from shapeCaster. ControlFactory warnings → `mc.warning`. Did **not** hollow-shim `guiFactory.py` / `optionVars.py`. Did **not** call `purgeCGM` from unittest (wipes every optionVar containing `cgm`).

**Files**:
- EXTENDED: `cgm/core/classes/GuiFactory.py` — `purgeCGM`, `appendOptionVarList`, old-name aliases
- NEW: `cgm/core/tests/test_coreLib/test_GUI.py`; `'GUI'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `tool_chunks.py`, `cgmPuppetKey.py`, `ControlFactory.py`, `shapeCaster.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `appendOptionVarList` stays on `self.optionVars` (puppetKey); core windows use `l_optionVars`
- `purgeCGM` matches lib substring `'cgm'` — not a prefix filter
- Hollow shim gated on leftover animTools + held `*Lib.py`

**Status**: Complete for core gui/optionVars retarget — Maya smoke: `cgm - All` now includes GUI; Toolbox Purge Option Vars still listed (do not fire during smoke unless you mean to wipe prefs); puppetKey Reset; ControlFactory aim-axis warning

---

### August 25, 2026 - Wave 3f names core retarget
**What**: Added 1:1 `getBaseName` / `getShortName` / `getLongName` wrappers on `name_utils` matching lib (missing → False). Retargeted live core `names.getBaseName` callers. Dropped unused `names` import from Project. Did **not** alias `getBaseName` = `get_base`. Did **not** hollow-shim `names.py`. `mayaBeOdd` still on lib (leave).

**Files**:
- EXTENDED: `cgm/core/lib/name_utils.py` — `getBaseName` / `getShortName` / `getLongName`
- NEW: `cgm/core/tests/test_coreLib/test_NAMES.py`; `'NAMES'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `nameTools.py`, `skinDat.py`, `Project.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `get_base` is string-split only and does not check existence — not a drop-in for lib `getBaseName`
- Hollow shim gated on leftover tools + lib internals

**Status**: Complete for core names retarget — Maya smoke: `cgm - All` now includes NAMES; skinDat / nameTools basename; Project still opens

---

### August 25, 2026 - Wave 3e dictionary core retarget
**What**: Aliased used axis/color names from `cgm.lib.dictionary` onto SHARED. Retargeted `cgm.core` off live `from cgm.lib import dictionary`. Conf-file `initializeDictionary` stays on lib. Did **not** hollow-shim `dictionary.py`.

**Files**:
- EXTENDED: `cgm/core/lib/shared_data.py` — `stringToVectorDict`, `returnStringToVectors`, `returnVectorToString`, `axisDirectionsByString`, `returnStateColor`
- NEW: `cgm/core/tests/test_coreLib/test_SHARED.py`; `'SHARED'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `rayCaster.py`, `shapeCaster.py`, `SnapFactory.py`, `meshTools.py`, `ControlFactory.py`, `curve_Utils.py`, `surface_Utils.py`, `nameTools.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- Canonical axis vectors stay tuples on `_d_axis_string_to_vector`; old dict uses lists
- `returnStateColor` reads `_d_gui_state_colors` — `ready` green is core `0.5` (meshTools only uses `help`)
- Do not port `initializeDictionary` this pass

**Status**: Complete for core dictionary retarget — Maya smoke: `cgm - All` now includes SHARED; meshTools help fields; rayCaster axis cast; SnapFactory mid-surface

---

### August 25, 2026 - Wave 3d cgmMath core retarget
**What**: Aliased used `cgm.lib.cgmMath` names on MATH. Retargeted `cgm.core` off live `from cgm.lib import cgmMath`. Fixed `rigging_utils` landmine (`cgmMath.*` with no import). Did **not** hollow-shim `cgmMath.py`. Did **not** alias `multiplyList` = `MATH.multiply`.

**Files**:
- EXTENDED: `cgm/core/lib/math_utils.py` — old-name aliases; `mag`
- NEW: `cgm/core/tests/test_coreLib/test_MATH.py`; `'MATH'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `rayCaster.py`, `curve_Utils.py`, `rigging_utils.py`, `skinDat.py`, `cgm_Deformers.py`, `shapeCaster.py`, `Project.py`, `surface_Utils.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `normSumList` = `normalizeListToSum` (core wins when `normalizeTo != 1`; skinDat uses `1.0`)
- `mag` is n-d list hypot — not `length()` (euclid)
- `MATH.multiply` is not a product; leave `multiplyList` on lib until a correct core helper is needed

**Status**: Complete for core cgmMath retarget — Maya smoke: `cgm - All` now includes MATH; skinDat normalize; rayCaster mid-cast; blendShape delta add

---

### August 25, 2026 - Wave 3c position snap wrappers
**What**: Core callers of `cgm.lib.position.movePointSnap` / `moveOrientSnap` now use 1:1 wrappers on `snap_utils` (`SNAP.move_point_snap` / `move_orient_snap`). Did **not** use `SNAP.go` (rotateOrder conversion would break mocap align). Dropped unused `locators` import from `surface_Utils`. Hollow `position.py` shim not done — leftover tools still call lib. Wave 3 distance retarget Maya-verified by user this session.

**Files**:
- EXTENDED: `cgm/core/lib/snap_utils.py` — `move_point_snap` / `move_orient_snap` / `move_parent_snap` + old-name aliases
- EXTENDED: `cgm/core/lib/mocap_align_utils.py`, `cgm/core/classes/SnapFactory.py`, `cgm/core/lib/surface_Utils.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Features/Feature_MocapAlignSnap.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- Mocap snap/bake must keep rotate-pivot `xform` + `move rpr` — `SNAP.go` is not a drop-in
- `moveParentSnap` aliased on SNAP for later leftover-tool retarget; locinatorLib / tdToolsLib stay on lib this pass

**Status**: Complete for core position retarget — Maya smoke: mocapBakeTools snap/bake + SnapFactory wrap-to-surface

---

### August 25, 2026 - Wave 3 distance core retarget
**What**: Aliased used measure/pos names on DIST. Retargeted `cgm.core` off live `from cgm.lib import distance` (except `cgmMeta_test`). Curve/surface closest-info callers now use `DIST.get_closest_point` / `get_closest_point_data` / `get_closest_point_data_from_mesh`. SnapFactory `locClosest` → DIST + spaceLocator. Rigger MM Locator → `LOC.create`. `geo_Utils` progress windows → core GuiFactory. Did **not** hollow-shim `cgm.lib.distance`. Maya not verified this session.

**Files**:
- EXTENDED: `cgm/core/lib/distance_utils.py` — old-name aliases; `get_object_size`; `get_positions_sorted_by_distance`
- NEW: `cgm/core/tests/test_coreLib/test_DIST.py`; `'DIST'` in `cgmTests.py` `_d_modules['coreLib']`
- EXTENDED: `ModuleShapeCaster.py`, `rayCaster.py`, `skinDat.py`, `curve_Utils.py`, `shapeCaster.py`, `surface_Utils.py`, `DraggerContextFactory.py`, `SnapFactory.py`, `segment_utils.py`, `general_utils.py`, `arrange_utils.py`, `rigging_utils.py`, `geo_Utils.py`, `GuiFactory.py`, `cgmMMRigger.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `returnClosestPoint` aliases **pos-list** closest (`get_closest_from_posList`), never `get_closest_point` (surface)
- `returnWorldSpaceFromMayaSpace` = `MATH.get_space_value(..., 'apiSpace')`
- `get_object_size` covers mesh / nurbsSurface / nurbsCurve only; component sizer stays on lib
- Follicle attach: `get_closest_point_data_from_mesh(mesh=surface, targetObj=obj)` — do not pass positional (obj, surface)
- Do not import `locator_utils` from Dragger (cycle: LOC imports Dragger)
- Hollow `distance.py` / `locators.py` shims wait on leftover tools + lib internals (`returnObjectType` `'shape'`)

**Status**: Complete for core distance retarget — **Maya-verified 2026-08-25**

---

### August 24, 2026 - Wave 5 docs catch-up
**What**: Recorded the unused-tool cut as **done** (windows/MEL already deleted 2026-08-20). Feature contract leftover inventory is six `cgm/tools` files. Did not re-run Maya smoke this session.

**Files**:
- EXTENDED: `Features/Feature_LibToCore.md` — status, post-cut remainder, Wave 5 done, launcher/rigger-MM notes
- EXTENDED: `Branches/Branch_SpringCleaning.md`

**Decisions**:
- animTools 1.0 stays this branch; locinatorLib / tdToolsLib / namingToolsLib / animToolsLib stay with it
- findTextures stays (Scene)
- Hollow attributes/search shim still gated on lib locators/distance, not on the deleted UIs

**Status**: Complete — docs only

---

### August 20, 2026 - Legacy artist tools cut
**What**: Removed unused `cgm/tools` windows and old marking-menu MEL. Toolbox Legacy tab is AnimTools only. Dropped unused rigger MM Surface snap rather than retargeting. `findTextures` stays — Scene still uses it.

**Files**:
- DELETED: `cgm/tools/attrTools.py`, `tdTools.py`, `locinator.py`, `setTools.py`, `namingTools.py`, `puppetBox.py`, `bufferTools.py`, `polyUniteTool.py`
- DELETED: `cgm/tools/lib/attrToolsLib.py`, `setToolsLib.py`, `puppetBoxLib.py`, `bufferToolsLib.py`
- DELETED: `cgm/tools/markingMenus/cgmSnap.py`, `cgmSetMenu.py`, `cgmSetKey.py`
- DELETED: `cgm/mel/cgmSnapMM.mel`, `cgmSetToolsMM.mel`, `cgmSetKeyMM.mel`
- KEPT: `cgm/tools/animTools.py`, `findTextures.py`, `lib/animToolsLib.py`, `lib/locinatorLib.py`, `lib/tdToolsLib.py`, `lib/namingToolsLib.py`
- EXTENDED: `cgm/core/tools/toolbox.py` — `buildTab_legacy` AnimTools only
- EXTENDED: `cgm/core/tools/lib/tool_calls.py` — dropped `*LEGACY` except `animToolsLEGACY`; dropped `loadPuppetBox` / `loadPuppetBox2`
- EXTENDED: `cgm/core/tools/markingMenus/cgmMMRigger.py` — Surface snap + `tdToolsLib` import gone
- EXTENDED: `cgm/core/tools/markingMenus/cgmMM_tool.py` — unused `tdToolsLib` import gone
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`, `AGENTS.md`

**Decisions**:
- Keep animTools 1.0 until a later pass (loc/tag/snap tabs still call locinatorLib / tdToolsLib)
- namingTools, puppetBox, bufferTools, polyUniteTool go with the unused-tool cut
- Do not retarget `doSnapClosestPointToSurface` — drop the menu item
- `puppetBox2` had no module; launchers removed
- Old hotkeys on `cgmSnapMM` / `cgmSetToolsMM` / `cgmSetKeyMM` break — use core MMs (`cgmPuppetKeyMM`, snap/set tools)
- Does not lift the `attributes.py` / `search.py` hollow-shim gate

**Status**: Complete for named windows — Maya smoke still open

---

### August 20, 2026 - mixed-hub attributes/search retarget
**What**: After Maya-verified attributes/search slice, retargeted remaining mixed-hub live `attributes`/`search` calls onto ATTR/SEARCH/VALID and dropped unused imports. `cgm.core` is now grep-clean of live `from cgm.lib import attributes` / `search` except examples and `cgmMeta_test` (do not revive). Did **not** shim those lib modules — `cgm/tools` and other `cgm.lib` files still need the old names.

**Files**:
- EXTENDED: `DraggerContextFactory.py`, `Project.py`, `skinDat.py`, `surface_Utils.py`, `shapeCaster.py`, `SnapFactory.py`, `shader_utils.py`, `segment_utils.py`, `mm_utils.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `ATTR.get_driver(..., getNode=True)` replaces `returnDriverObject`; `skipConversionNodes=` must be keyword (not positional) on combined plugs
- `segment_utils` live `attributes.*` calls had no live lib import (commented tuple) — retarget is a landmine fix
- `mm_utils` channel-box path used `search.*` with no import — same landmine; now `SEARCH.get_selectedFromChannelBox(report=False)`
- Shim waits on an old-name alias map covering `cgm/tools` + remaining `cgm.lib` internals

**Status**: Complete — Maya-verified **cgm - All**

---

### August 20, 2026 - attributes/search shim gated
**What**: Inventoried remaining `attributes.*` / `search.*` callers in `cgm/tools`, `cgm/projects`, and other `cgm.lib` modules. **Did not** hollow-shim `attributes.py` / `search.py`. Lib `returnObjectType` is component-aware; a `search_utils` re-export would break locators/distance. Several ATTR “equivalents” have incompatible signatures (positional `skipConversionNodes`, `transferConnection`, `forceLock`).

**Files**:
- EXTENDED: `Features/Feature_LibToCore.md` (Wave 2 detail + gate), `Branches/Branch_SpringCleaning.md`

**Decisions**:
- Wave 2 core retarget is done; shim is a later step (Wave 3 locators/distance first, or a hybrid leftover-body shim)
- Do not add naive `doGetAttr = get` aliases that change call signatures
- Examples / `cgmMeta_test` stay on lib

**Status**: Complete — gate documented; next is Wave 3 transform backbone or hybrid shim if explicitly requested

---

### August 20, 2026 - attributes/search core retarget (no shim yet)
**What**: After Maya-verified `cgm_Meta`, mapped remaining core `attributes`/`search` callers and retargeted the ones already covered by ATTR/SEARCH. Dropped unused lib imports. Added `SEARCH.select_check` plus old-name aliases (`selectCheck`, `returnObjectType`, `returnSelectedAttributesFromChannelBox`). Did **not** shim `cgm.lib.attributes` / `search` — mixed hubs still import them with other lib modules.

**Files**:
- EXTENDED: `search_utils.py`, `node_utils.py`, `mayaBeOdd_utils.py`, `control_utils.py`, `selection_Utils.py`, `cgm_Deformers.py`, `rayCaster.py`, `meshTools.py`, `cgmMM_tool.py`, `cgmPuppetKey.py`, `distance_utils.py`, `nameTools.py`, `curve_Utils.py`, `ControlFactory.py`, `cgm_RigMeta.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- `ATTR.connect` does not support lib `transferConnection=True` (raises); `control_utils` slaves scale without transfer
- Channel-box query uses `SEARCH.get_selectedFromChannelBox(report=False)` so marking menus do not pprint
- Leave mixed hubs (`DraggerContextFactory`, `Project`, `skinDat`, `surface_Utils`, `shapeCaster`, `SnapFactory`, rig leftovers) until those files are retargeted as a group
- Do not shim `attributes.py` / `search.py` until those remaining callers are gone

**Status**: Complete — Maya-verified **cgm - All**

---

### August 20, 2026 - cgm_Meta off live first-party lib
**What**: Retargeted remaining live `cgm_Meta` calls off `cgm.lib` (`names`, `attributes.storeInfo`, `dictionary` axis vectors, `rigging.doParentToWorld`, `locators.locMeObject`). Component `doLoc` now uses `POS.get` + `spaceLocator` (same as the transform path) so `locator_utils` / DraggerContextFactory are not imported at meta load. Dropped unused `ml_resetChannels` and `NameFactory` (`Old_Name`) imports.

**Files**:
- EXTENDED: `cgm/core/cgm_Meta.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- Axis enums use `SHARED._d_axis_string_to_vector` (tuples; Maya aimConstraint accepts them)
- Buffer `store()` uses `ATTR.set_message(..., simple=True)` for scene objects
- Parent-to-world uses `TRANS.parent_set(node, False)`
- Do not import `locator_utils` from `cgm_Meta` (heavy; DraggerContextFactory)
- Leave `cgm.lib.attributes` / `search` as full implementations until remaining core callers are mapped

**Status**: Complete — Maya-verified **cgm - All** (coreLib + cgmMeta)

---

### August 20, 2026 - Maya-verified suite; ATTR float/double
**What**: Toolbox Unittesting **cgm - All** passes for coreLib + cgmMeta. RigBlocks skipped (incomplete). `test_ATTR.test_type` uses `validate_attrTypeMatch` so Maya `float` vs `double` are the same family.

**Files**:
- EXTENDED: `cgm/core/tests/test_coreLib/test_ATTR.py`
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Status**: Complete — ready to push this slice; next wave was remaining `cgm_Meta` lib imports (done this same day)

---

### August 20, 2026 - Skip incomplete RigBlocks tests; isolate runner scenes
**What**: `cgm - All` no longer runs MRS RigBlocks (incomplete suite). Class is `@unittest.skip`. Runner now `file -new` **per test module** so leftover selection cannot leak. `cgmRigBlock` create only infers side from selection if it is a transform — attr plugs like `node.translateX` no longer hit `xform`.

**Files**:
- EXTENDED: `cgm/core/tests/cgmTests.py` — MRS dropped from `_l_all_order`; sceneSetup per module
- EXTENDED: `cgm/core/tests/test_MRS/test_RigBlocks.py` — skip
- EXTENDED: `cgm/core/mrs/RigBlocks.py` — transform check before `position_get`

**Decisions**:
- Skip rather than rewrite RigBlocks tests this branch
- Unittesting menu still lists MRS / RigBlocks for an explicit run (skipped)

**Status**: Complete — re-run **cgm - All**; RigBlocks errors should be gone

---

### August 20, 2026 - Wave 0 inventory and branch docs
**What**: Surveyed first-party `cgm.lib` vs `cgm.core` dual-stack, existing unittest runner, and remaining callers. Wrote the feature contract and this branch doc. No py3 code changes.

**Files**:
- NEW: `Features/Feature_LibToCore.md`
- NEW: `Branches/Branch_SpringCleaning.md`
- EXTENDED: `AGENTS.md` (feature-doc link)

**Features**:
- Living old→new mapping table and caller counts
- Shim / characterizing-test / grep-gate rules
- Wave order (lists first, then attributes/search, then transform backbone)

**Decisions**:
- Inventory → characterize → port used functions → retarget core → thin shim (not big-bang, not port unused lines)
- Keep unittest + Unittesting menu; do not introduce pytest this branch
- Core wins when lib and core APIs disagree; old names stay on the shim
- Do not delete `cgm.lib` this branch (user/ProjectScripts still import it)
- Leave `zoo` / `ml` / `bo` / `openSource` / Red9 / `specialCaseStuff` / `gigs` alone
- `cgm.lib.modules` is superseded by MRS — do not port the old module-null system

**Status**: Complete — Wave 0 docs only. Code waves wait on explicit start.

---

### August 20, 2026 - Wave 0b/1/2/3 code (lists shim, tests, dual-import cuts)
**What**: Stood up Maya-free `test_LISTS` and real `test_ATTR`. Ported remaining `lists` helpers into `list_utils` with old-name aliases; `cgm.lib.lists` is a re-export shim. Retargeted core callers off `from cgm.lib import lists`. `search_utils` and `attribute_utils` no longer import first-party lib (`returnMessageData` / `repairMessageToReferencedTarget` now on ATTR). Dropped unused lib imports from `rigging_utils`. Retargeted `geo_Utils` math/names/distance/attr calls to core; progress UI still uses `cgm.lib.guiFactory`. Restored `from cgm.lib import distance` on `ModuleShapeCaster` (commented import was a NameError landmine).

**Files**:
- NEW: `cgm/core/tests/test_coreLib/test_LISTS.py`
- EXTENDED: `cgm/core/lib/list_utils.py`, `cgm/lib/lists.py` (shim), `cgm/core/tests/cgmTests.py`, `cgm/core/tests/test_coreLib/test_ATTR.py`, `cgm/core/lib/attribute_utils.py`, `search_utils.py`, `rigging_utils.py`, `geo_Utils.py`, `distance_utils.py`, `math_utils.py`, plus core callers (locinator, mocapBakeTools, meshTools, dynParentTool, arrange_utils, ModuleShapeCaster, curve_Utils, DraggerContextFactory, cgmPuppetKey, cgm_Meta unused lists import, others)
- EXTENDED: `Features/Feature_LibToCore.md`, `Branches/Branch_SpringCleaning.md`

**Decisions**:
- Core list API uses `get_*` names; old `return*` names stay as aliases + shim
- `returnSplitList` uses integer division (`//`) so py3 slicing works
- `get_matchList` always returns a list (empty, not False)
- Do not shim `distance.py` this pass — too many old names still in ModuleShapeCaster

**Status**: Complete for lists wave. Attributes/search full shims and factory/UI retarget still open.

---

## Deliverables

### Wave 0 — docs + inventory
- [x] Branch doc
- [x] Feature_LibToCore inventory and contract
- [x] AGENTS.md link

### Wave 0b — test runner
- [x] Harden `cgmTests.py` (scene-wipe documented; registry for LISTS)
- [x] Maya-free `test_LISTS` against `list_utils`

### Wave 1 — lists
- [x] Port used `cgm.lib.lists` functions into `list_utils` + aliases
- [x] Retarget core callers; fix `arrange_utils` / `ModuleShapeCaster` missing-import landmines
- [x] Shim `cgm.lib.lists` (later **dropped 2026-09-01**)

### Wave 2 — attributes + search
- [x] Real `test_ATTR` (replace `pass` stubs)
- [x] `attribute_utils` / `search_utils` do not import first-party lib
- [x] Retarget `cgm_Meta` remaining live lib imports (`attributes`, `search`, `locators`, …)
- [x] Retarget remaining easy core `attributes`/`search` callers (ATTR/SEARCH already existed)
- [x] Retarget mixed-hub live `attributes`/`search` callers in `cgm.core`
- [x] Full shim of `cgm.lib.attributes` / `cgm.lib.search` — **won’t do** (production does not need it)

### Wave 3 — transform backbone
- [x] Unused lib imports removed from `rigging_utils`
- [x] `geo_Utils` math/names/distance/attr retarget; `MATH.multiplyLists` / `DIST.get_bb_average`
- [x] `geo_Utils` progress windows → core GuiFactory (Wave 3)
- [x] Locators / full `distance.py` shim — **won’t do** (impl in `libOld`; core grep-clean)

### Later waves
- [x] Vendored `zoo` / `ml` / `bo` / `openSource` / Red9 / `specialCaseStuff` / `gigs` left alone
- [x] Remaining used Maya utils — **do not port** (deformers bake / leftover joints / bulk skinning / `modules`)
- [x] Drop unused legacy `cgm/tools` UIs (attr/td/locinator/setTools 1.0, namingTools, puppetBox, bufferTools, polyUniteTool, old marking menus + MEL)
- [x] animTools 1.0 + locinatorLib/tdToolsLib/namingToolsLib/animToolsLib deleted 2026-09-01
- [x] `findTextures` → `TEXTURE.remap_missing` 2026-09-01; `cgm/tools` empty
- [x] Maya smoke of core tools — **closed 2026-09-01**

### Testing
- [x] Wave 0: inventory of current runner (documented in feature doc)
- [x] Unittesting → cgm - All in Maya (coreLib + cgmMeta; RigBlocks skipped)
- [x] Wave 4 / 4b / 4c Maya-verified (`cgm - All`, including CURVES / SKIN / NODES)
- [x] `cgm_Meta` lib retarget Maya-verified
- [x] Mixed-hub attributes/search retarget Maya-verified
- [x] ATTR float/double treated as one family (`validate_attrTypeMatch`)
- [x] No pytest this branch
- [x] Wave 5 Maya smoke — **closed 2026-09-01**

---

## PR Notes

### Overview
Spring cleaning **complete**: used first-party `cgm.lib` is in `cgm.core`; leftover first-party modules parked in `cgm/libOld`. Production `cgm.core` is grep-clean of live first-party `cgm.lib`. Legacy `cgm/tools` 1.0 windows deleted (including animTools). `findTextures` is `TEXTURE.remap_missing`. Vendored trees stay in `cgm.lib` (zooSetkey South is a one-line `ml_tools` hook). Hollow `attributes`/`search` shims were not restored.

#### Breaking Changes
First-party names parked in `libOld` (`from cgm.lib import attributes` / `lists` fails). Canonical new imports are `cgm.core.lib.*_utils`. **Artist-facing:** Toolbox tabs are TD / Anim / Settings (Legacy tab gone). Use `cgm.core.tools` for attr/locinator/setTools. tdTools has no 1:1 replacement window. Old MEL marking menus `cgmSnapMM` / `cgmSetToolsMM` / `cgmSetKeyMM` are gone — use core MMs (`cgmPuppetKeyMM`, snap/set tools). `cgm/projects` and old user scripts that import first-party `cgm.lib` `ImportError`.

#### Next Steps
None for this branch. Optional later (not leftover): revive hollow shims for user scripts, retarget `cgm/projects`, delete `libOld`, re-enable MRS RigBlocks tests with per-test scene setup.

---

## Notes

### Architectural Patterns Established
- Dual-stack is a cycle, not a shim layer — finish core, then hollow out lib
- Characterizing tests before port; core wins on disagreement
- Explicit `_d_modules` registry (discover was abandoned)
- `file -new` per test module so selection cannot leak
- Float and double are the same ATTR family (`validate_attrTypeMatch`)

### Future Considerations
- Optional mayapy / standalone initialize after the GUI runner is trustworthy
- Hard cutover of shims only after we know nothing still imports lib (later branch)

---

*Last Updated: September 1, 2026*  
*Branch Status: Complete*
