# Branch: jburton/animData

## Quick Info
**Status**: Active  
**Created**: August 25, 2026  
**Last Updated**: August 26, 2026 (Phase 2a range capture)  
**PR**: Pending

## Goals
Ship lossless Maya animation clips as `cgmAnimClip` (cgmDat JSON): nested clip → object → channel → curve → key, then capture, apply, and match in later phases. **Phase 0** is the Dat window stub. **Phase 1** is the curve round-trip gate. **Phase 2a** captures direct time-based curves over Start/End (absolute times). Relative time, boundary samples, apply, and pose matching stay later.

Canonical contract: [`Feature_AnimData.md`](../Features/Feature_AnimData.md).

## Related Documentation
- **[Feature_AnimData.md](../Features/Feature_AnimData.md)** - Canonical design contract (phases, schema, Phase 1 gate, Phase 2a capture)
- **[animClip_dat.py](../../repos/cgmToolsPy3/cgm/core/lib/animClip_dat.py)** - `AnimClip` + Dat UI
- **[animClip_curve.py](../../repos/cgmToolsPy3/cgm/core/lib/animClip_curve.py)** - curve snapshot / rebuild / capture helpers
- **[cgm_Dat.py](../../repos/cgmToolsPy3/cgm/core/cgm_Dat.py)** - `CGMDAT.data` / `CGMDAT.ui` base
- **[MRSDat.py](../../repos/cgmToolsPy3/cgm/core/mrs/MRSDat.py)** - Dat subclass pattern
- **[NewBranch_Guide.md](../Guides/NewBranch_Guide.md)** - Branch documentation format
- **[NewFeature_Guide.md](../Guides/NewFeature_Guide.md)** - Feature documentation format

## Timeline

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
- [x] Selection + frame range (2a: absolute times, drop keys outside Start/End)
- [ ] Relative / normalized times
- [ ] Evaluate start/end if unkeyed (boundary motion)

### Phase 3 — Apply
- [ ] Apply at destination frame
- [ ] Replace / merge / insert

### Phase 4 — Matching
- [ ] Reuse PoseManager match methods

### Phase 5 — Copy/paste
- [ ] Cross-scene copy/paste (clip as clipboard)

### Later
- [ ] Trim / retime / mirror
- [ ] Library / browser
- [ ] Additive / layers / retarget

### Testing
- [x] Phase 1 Maya round-trip gate
- [x] Documentation updated
- [ ] Maya testing complete

---

## PR Notes

### TBD (Phase 2b relative time)

#### Overview
Phase 0 Dat UI + Phase 1 curve round-trip + Phase 2a absolute range capture. Relative times and unkeyed boundary samples are next.

#### Architecture Decisions
- Nested clip → object → channel → curve → key
- JSON Dat, not ConfigObj
- UI with the Dat class (`animClip_dat.py`), launched from Toolbox Anim
- File bar = path; Status row = operations
- Absolute times through Phase 2a
- Curve node is source of truth; `ATTR.get_driver(skipConversionNodes=True)`; skip layers / blends
- Pose matching deferred to Phase 4

#### Testing
- Phase 0 UI stub: open AnimClip, Capture, Save/Load JSON, Paste Clip warns
- Phase 1 tests passed in Maya (ANIMCLIP), including weighted after spline→fixed fix
- Phase 2a: locator tx capture, range slice, unitConversion hop (ANIMCLIP)

#### Documentation Updated
- `Feature_AnimData.md` — Phase 2a capture contract
- `Branch_AnimData.md` — this pass
- `AGENTS.md` — contract pointer

#### Breaking Changes
None

#### Next Steps
- Phase 2b: normalize clip times relative to Start
- Phase 2c: sample unkeyed start/end so motion at the clip edges is preserved
- Phase 3: Paste Clip writes keys (replace / merge / insert)

---

**Ready for Review** - Not yet. Relative time and apply still open.

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

*Last Updated: August 26, 2026*  
*Branch Status: Active*
