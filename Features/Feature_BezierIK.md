# Feature: Bezier IK (MRS Segment)

## Status and Overview

- **Status**: In progress — **Maya-verified** for Segment `ikSetup=bezier`, `segmentType=parent`, `scaleSetup` + squash **simple**, `segmentStretchBy` **translate** and **scale**; Segment **`ikSetup=bezier`** + **`ikBase=hips`** spine-style (hip/chest IK + separate chain bezier mains — see § Hips parent bezier); Segment **`segmentType=bezier`** in py3 (bezier CV **handle** shapes + `controlsSegmentBezier`; segment ribbon + **`rig_frame`** like ribbon — **not** coupled to `ikSetup=bezier`)
- **Last Updated**: October 29, 2026 — Module IK **`bezier_spline_stretch`** split by **`segmentType`** (**`segment_bezier_module_ik_spline_stretch_profile`**: parent = block stretch + volume; non-parent = **translate** + arcLength on **`ikJoints`**, full squash/stretch on **`segmentJoints`**); Head **`neckIK=bezier`** parity + precheck unlock for non-parent segment
- **Audience**: Dev / TA — design contract for Bezier spline IK on MRS Segment (not artist manual prose)
- **Branch timeline**: [`Branches/Branch_BezierIK.md`](../Branches/Branch_BezierIK.md)

**Maintenance rule**: Update when changing `IK.bezier_spline`, `IK.bezier_spline_stretch` (incl. **`volumeSquashInflateOnly`**), `IK.ribbon` skin-tighten / squash share paths, `bezier_utils`, `rigFrame_utils.bezier` / **`rigFrame_utils.spline`** (driver curve return), **`segment_mid`**, `bezier_ik_block_utils.py` (incl. **`segment_inflate_stretch_result_from_volume_joints`**, **`rig_inflate`** helpers), `dynamic_utils._apply_hair_spline_ik_advanced_twist`, `skin_utils.surface_tightenEnds` / `curve_tightenEnds`, **`rigShapes_utils.ik_end`** / **`builder_utils.shapes_fromCast`** (**`ikEndFrameHandle`**), or Segment / Head neck / Limb bezier squash-stretch paths (`segment.py`, `head.py`, `limb.py`).

**Related**

- [`Feature_MRSWiring.md`](Feature_MRSWiring.md) — rigNull messages, control caches
- [`Builder.py`](../../cgmToolsPy3/cgm/core/mrs/Builder.py) — MRS Builder **Step Build** (`ui_stepBuild`)
- [`ik_utils.py`](../../cgmToolsPy3/cgm/core/rig/ik_utils.py), [`bezier_utils.py`](../../cgmToolsPy3/cgm/core/rig/bezier_utils.py), [`rigFrame_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/rigFrame_utils.py), [`bezier_ik_block_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/bezier_ik_block_utils.py), [`rigShapes_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/rigShapes_utils.py), [`builder_utils.py`](../../cgmToolsPy3/cgm/core/mrs/lib/builder_utils.py), [`segment.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/segment.py), [`head.py`](../../cgmToolsPy3/cgm/core/mrs/blocks/organic/head.py)

---

## Scope (current)

### In scope (shipped / verified)

| Block config | Behavior |
|--------------|----------|
| `ikSetup` **bezier** | `RIGFRAME.bezier` → `IK.bezier_spline` + CV control wire + **`bezier_ik_connect_spline_advanced_twist`** (Object Rotation Up Start/End; optional **`ikSplineTwistUpStart`** / **`ikSplineTwistUpEnd`** on Segment + Head) |
| `ikSetup` **bezier** or **spline** + **`ikBase=hips`** (any **`segmentType`**) | **Maya-verified** on parent spine — dual IK handles (hip/chest) + chain bezier CVs when bezier; **`bezier_ik_resolve_main_ik_list`** for wire/subs; no legacy spine **`handleJoints[1]`** handle. **Hips base orient follow** on **`*_ikOrientFrame`**; FK/IK blend IK chain index **0** = orient frame via **`ml_ikBlendUse`** (§ Segment IK orient follow). **`ml_ikUse[0]`** unchanged for spline solve. |
| `segmentType` **parent** | Precheck enforces; ribbon-style segment joints optional per parent path |
| `scaleSetup` on | FK/IK → blend: **parent** `blendChainsBy` + **`blendChainsScaleByAttr`** (not scaleConstraint) |
| `scaleSetup` + squash **simple** / **both** / **none** (via **`_segment_bezier_should_run_spline_stretch`**) | Module **`bezier_spline_stretch`** on **`ml_ikUse`** when stretch gate passes — see **`segmentType`** split below |
| **`segmentType=parent`** + module bezier | **`segmentStretchBy`** **translate** or **scale** on **`ikJoints`**; block **`squashMeasure`**, volume squash, **`squashExtraControl`**; **`d_stretchInflateRes`** for parent inflate |
| **`segmentType` ≠ parent** + module bezier | **`ikJoints`**: **`stretchBy=translate`**, **arcLength**, **`applyVolumeSquash=False`** — length follows driver only. **`segmentJoints`**: block **`segmentStretchBy`**, squash, inflate, **`pointDist`** (ribbon / seg bezier / curve in **`rig_segments`**) |
| `squashMeasure` (block / `d_squashStretch`) | **arcLength** (default, production) — global driver `curveInfo` ratio. **pointDist** — *(experimental)* per-segment `distanceDim` on driver **POCI** positions at **bind-time U only** (no **nearestPointOnCurve** tracking on bezier stretch — avoids translate feedback). Bind rest from evaluated `distanceDim` or joint span; per-segment ratio clamped before stretch blend. **Maya-verified (Oct 15):** `globalScalePlug` → driver `masterScale` normalizes **live** segment distance only (`distance / masterScale / bindSegDist`); bind rest is **not** divided by `masterScale` (matches arcLength + ribbon pointDist). |
| Head **`neckIK`** **bezier** + **`neckControls` > 1** (split **`headIK`** / neck-end **`controlIK`**) | **`ml_ikUse`**: neck chain + **`_splineEnd`** dup (parent **`ml_ikJoints[-2]`**). **`ml_ikJoints[-1]`** (`head_*_ik_sknJnt`) **only** **`p_parent = headIK`** — no **`pointConstraint`**, **`_splineControl`**, or **`followIK`** on the head IK joint. Ribbon end **`ribbonIKDrivers[-1]`** → neck-end **`controlIK`**. Twist end: **`mTwistEndControl=headIK`** in **`RIGFRAME.bezier`** (`twistEndAdd` on **`headIK`**); advanced-twist **WU** from bezier CV span (unchanged). Module stretch on **`ml_ikUse`**: same **`segmentType`** split as Segment (**`segment_bezier_module_ik_spline_stretch_profile`**; **`block_uses_bezier_module_ik`** reads **`neckIK=bezier`**). **`int_handleEndIdx = -2`**. With **`scaleSetup`**, no **`scaleConstraint(headIK → ml_ikJoints[-1])`** when split (scale from parenting). |

### Out of scope (this feature doc)

- Sine / wave driver stack on hidden POCI curve (**tabled** on [`Branch_BezierIK.md`](../Branches/Branch_BezierIK.md))
- `segmentType` ribbon / spline / curve / linear with `ikSetup` bezier — **experimental** vs **parent** sign-off; non-parent **IK translate stretch + segment deform squash** path in py3 (Head **`neckIK=bezier`** + ribbon segment allowed — no parent-only precheck)
- **Limb** `segmentType=bezier` — roll-section stretch in progress (see § Limb bezier segments); shapes/controls parity still paired with user

### Roadmap — Segment build combinations

| Config | Status |
|--------|--------|
| `ikSetup=bezier`, `segmentType=parent`, no `scaleSetup` | Shipped |
| Same + `scaleSetup` + `squash=simple` + `segmentStretchBy` translate or scale | Maya-verified |
| `segmentType=bezier`, any supported `ikSetup` except **bezier** | Shipped (py3) — **`segment_rig_segments_bezier`** on **segmentJoints** (rig guts: `bezierIKCurve` / `bezierIKDriverCurve`); bezier CV **handleJoints**; `RIGFRAME.segment_handles` + module **`ikSetup`** on IK chain |
| `segmentType=bezier` + `ikSetup=bezier` | **Blocked** — precheck fail; use **`ikSetup=bezier`** + **`segmentType=parent`** or **`ribbon`** / **`ribbonLive`** |
| Sine / wave on driver | Tabled (lib only in `ik_utils`) |

---

## Artist / block toggles

| Attr | Effect |
|------|--------|
| `ikSetup` / Head `neckIK` = bezier | Bezier driver + ikSplineSolver chain |
| **`ikSplineBezierMode`** (Segment, Head, Limb — rig UI) | **`uniform`** (default) \| **`bend`** — passed to **`IK.bezier_spline`** as **`bezierAnchorMode`** via **`block_bezier_anchor_mode`**. Legacy block nodes may still have **`splineBezierMode`**; lib reads that name when **`ikSplineBezierMode`** is absent. |
| **`ikBezierControlShape`** (Segment, `ikSetup=bezier`) | **`ball`** (default) — FK cross-section **cube** mains + **sphere** subs (neck bezier). **`segmentHandle`** — cast-thin **cube** mains (**`jointRadius`** on aim, cross from proxy cast — limb bezier) + **`limbSegmentHandle`** semiSphere subs. Head/Limb unchanged (no attr → **`ball`**). **SemiSphere size** (all segment **`limbSegmentHandle`** casts, incl. **`RIGSHAPES.segment_handles`**) — **`builder_utils.segment_handle_cast_semisphere_size`**: mean **`moduleJoints`** adjacent span **÷ 4**, capped by **`jointRadius`**. |
| `segmentType` = **parent** | Bezier solve on **ik** chain; mains = `controlIKBase` / mids / `controlIK` (default **`ikBase`**). **`ikBase=hips`**: hip/chest **`controlIKBase`** / **`controlIK`** keep **`ik_base`** / **`ik_end`** shapes; bezier CV mains on **`bezierIKChainStart`** / mids / **`bezierIKChainEnd`** (see § Hips parent bezier). |
| **`ikBase`** = **hips** (Segment, `ikSetup=bezier`) | Spine-style hips chain path (any **`segmentType`**): no extra **`handleJoints[1]`** mid spine handle; chain bezier **visSub**; pickwalk **`controlsIK`** = hip IK + chest IK + bezier chain. |
| `segmentType` = **bezier** | Bezier CV mains/subs on **handleJoints** (`controlsSegmentBezier`); segment deformation via **`segment_rig_segments_bezier`** on **`segmentJoints`**. **`ikSetup=bezier`**: **`rig_segments`** reuses module **`bezierIKCurve`** (no second CV wire on handle joints); **`segmentBezierIKSplineHandle`** holds the segment ikSpline handle. |
| `scaleSetup` | Enables scale blend to **blend** joints; bezier does **not** use ribbon IK scaleConstraints on IK (stretch owns IK channels) |
| `scaleSetup` + squash modes | **`_segment_bezier_should_run_spline_stretch`**: squash **simple**, **both**, or **none** (no squash attr → stretch still runs). Gates module **`bezier_spline_stretch`** in **`rig_frame`** / Head neck bezier |
| `segmentStretchBy` | On **parent** module IK and on **segment deform** (`rig_segments`). **Non-parent** module IK **ignores** block value — forced **`translate`** on **`ikJoints`**. **`translate`** — length via joint **translate**; volume squash = linear **1/ratio**. **`scale`** — aim-axis **scale**; volume = **ratio^-0.5** |
| Settings **`stretch`** | Curve-follow weight on settings (from `bezier_spline_stretch`). **`0`** = rest bind for the curve term; **`1`** = full arc-length match. Does **not** change length when arc ratio **`r`** stays **1**. |
| Settings **`lengthScale`** | Uniform length multiplier on settings (default **1**, min **0.0001**). **`finalRatio = curveBlend × lengthScale`**. Key this when **`r ≈ 1`** (bind match or static curve). No block mirror attr in v1 — settings only. |
| Settings **`squash`** | Volume compensation strength on perpendicular scales (see volume driver below). **`bezier_spline_stretch`** creates it with default **1.0** (Maya default + current value). **Volume squash** paths (block **`squash`** **simple** / **both**) keep **1.0** after build. **`squash:none`** stretch-only (no volume on joints) pins **`squash`** to **0** on settings so the attr is inert. |
| `squashExtraControl` | Enables per-joint volume **`{base}_outFactor_i`** on settings (`extraSquashControl` in lib). Requires volume squash active on the block path (limb: `_limb_bezier_volume_squash_active`). |
| `squashInflateControl` | Segment / Head / Limb. When **on**, `bezier_spline_stretch` gets **`extraInflateControl`** (settings **`squashInflate`** / **`squashInflateOffset`**, **`{part}_inflateFactor_i`**). Independent of **`squashExtraControl`**. Legacy blocks without the attr fall back to **`squashExtraControl`**. Default **on**. |
| **`squashInflateFactorMin` / `Max` / `Mode`** (block Squash/Stretch UI) | Ramp for **settings** `{partName}_inflate_inflateFactor_i` defaults — **not** **`squashFactorMin/Max`** (those drive volume **`outFactor_*`** only). **`squashInflateFactorMode`**: same enum set as **`squashFactorMode`** (`midPeak`, **`midBulge`**, …). **`squashInflateFactorMin` may be negative** for contract vs inflate. Legacy block attrs **`inflateFactorMin/Max/Mode`** still read via **`block_squash_inflate_factor_min_max`** / **`block_squash_inflate_factor_mode`**. |
| Settings **`squashInflate`** | Additive strength on the inflate ramp (default **0**). Raise **> 0** to inflate; negative **`inflateFactor_*`** on a joint contracts when this is **> 0**. |
| Settings **`squashInflateOffset`** | ±2 slides the inflate ramp along the chain (`shift = offset × maxIdx/2`; sample index `s = g − shift` with lerp between adjacent factor indices). Limb: **`g`** is global across roll sections (`inflateSlideGlobalCount` / `Start`). |
| End IK **`followIK`** | On **`rigNull.controlIK`** (not bezier CV mains). **`segment_ik_spline_orient_follow_setup`**: orient blend on end **skin** IK joint; **`pointConstraint`** from **`_splineEnd`**; **`_splineControl`** dup under **`controlIK`**. Driver **0** = spline span orient (**`_splineEnd`**), **1** = follow control hierarchy. **Defaults:** **`ikSetup=bezier`** end **`followIK`** default **1.0**; **`ikSetup=spline`** end default **0.0**. **Head** split path (**`headIK` ≠ `controlIK`**): **no** end follow on **`ml_ikJoints[-1]`**. |
| Hips base **`followIK`** | **`ikBase=hips`** only. On **`controlIKBase`**. **`segment_ik_base_orient_follow_setup(self, …)`**: **`*_ikOrientFrame`** under **`ml_ikJoints[0]`**; **`_splineControlStart`** under **`controlIKBase`**. Orient blend on **`*_ikOrientFrame`** only (not pelvis IK joint). Driver **0** = **`_splineControlStart`**, **1** = ik pelvis. Sets **`self.ml_ikBlendUse[0]`** = orient frame for FK/IK **`blendChainsBy`**. **Defaults:** bezier **`followIK`** **1.0**; spline **0.0**. |
| **`ikSplineTwistUpStart`** / **`ikSplineTwistUpEnd`** | Segment + Head only (`BLOCKSHARE._d_attrsTo_make['shapeDirection']`). **`dWorldUpVector`** / **`dWorldUpVectorEnd`** on bezier ikSpline handle (defaults **y+** start; end **y+** on Segment, **z-** on Head). **`bezier_ik_block_twist_world_up_vectors`** → **`RIGDYN._apply_hair_spline_ik_advanced_twist`**. Limb roll bezier unchanged (orientation up vector only). |
| Head **`ikMidAimSetup`** | **Head block only** (default **off**). With **`ikMidSetup=linearTrack`** and aim **on**: **`{part}_midRootEnd_aimRef`** parented under **`controlIKBase`**; **`aimConstraint`** base → end IK; each mid **`mainDriver`** **`orientConstraint`** to ref (not driver-to-driver aim). **`cubicTrack`** / Segment (no attr) keep legacy driver-chain aim when aim is on. |
| **`segmentEndHandleUp`** (Limb only, rig UI) | Last roll-segment **`back`** **`aimer`** **`aimConstraint`** **`worldUpObject`**. **`stableUp`** (default) = **`stableEnd`** upObj on that span. **`last`** = immediate previous rig **`handleJoints`** main (same as back aim target). Applies to **`segmentType=bezier`** (**`_limb_rig_segments_bezier_end_main_follow_root`**) and legacy ribbon/curve/linear roll **`rig_segments`** last-handle path. **`stableEnd`** orient stack is built in both modes. |
| **`ikEnd`** (Segment rig UI) | Where **`controlIK`** lives: **`helper`** (prerig end **`ikEndHandle`**), **`tipBase`** / **`tipMid`** / **`tipEnd`** (penultimate attach, chain midpoint, rig tip — see § Segment IK end shapes). Adjusts **`int_handleEndIdx`** in **`rig_dataBuffer`**. |
| **`ikEndShape`** (Segment rig UI) | **`cast`** \| **`cube`** \| **`locator`**. **`cast`**: connected proxy cast like the **last FK `frameHandle`** (cross-section at cast **U** → connector rails → loft **max U**), but cast **U** from the **`ikEnd`** rule (§ below). **`cube`** / **`locator`**: primitive at form handle. Not the same as **`simpleCast`** (short local span) or parenting **`ml_fkShapes[-1]`** when **`ikEnd` ≠ last FK index. |

---

## Prechecks and Step Build

Rig validation lives in block **`rig_prechecks`** (via `rigFactory.prechecks`). Relevant bezier rules today:

| Check | Message (typical) |
|-------|-------------------|
| `segmentType` bezier + `numControls` < 2 | `segmentType bezier requires at least 2 controls` |
| `ikSetup` bezier + `segmentType` bezier | `Bezier/bezier is not a viable path. Bezier/Ribbon or Bezier/Parent is recommended` |
| `segmentType` parent + `numControls` ≠ `numJoints` | `segmentType parent requires same number of controls as joints` |
| Head parent + `neckControls` ≠ `neckJoints` | `segmentType parent requires same number of controls as joints` |

**How to run prechecks**

| Entry | Behavior |
|-------|----------|
| **Rig → Prechecks** (MRS Builder block menu) | `mBlock.asRigFactory(mode='prechecks')` — PASS/FAIL banner + numbered lines in Script Editor; no rig build |
| **Rig → Step Build** | Same precheck pass **before** `rigFactory` full init; on fail, stepped UI shows **Precheck errors** (indexed list) and **no** rig step buttons — does not raise through `GuiFactory` |

Block must be **skeleton** state for Step Build layout (unchanged). Fix attrs on the block, then reopen Step Build or refresh the tool after reloading `Builder.py`.

**Maintenance**: If `rig_prechecks` messages or factory precheck contract change, update this table and [`Branches/Branch_BezierIK.md`](../Branches/Branch_BezierIK.md).

---

## Lib API

### `IK.bezier_spline`

Hidden POCI **driver** curve + visible **bezierIKCurve** + ikSpline IK handle. Returns dict (`mDriverCurve`, `mBezierCurve`, `mIKHandle`, `ml_joints`, twist plugs, …).

**Block anchor mode:** **`RIGFRAME.bezier`** and **`segment_rig_segments_bezier`** pass **`bezierAnchorMode=block_bezier_anchor_mode(mBlock)`** — from block enum **`ikSplineBezierMode`** (`uniform` \| `bend`).

### `IK.bezier_spline_stretch`

Arc-length stretch from **driver curve** (`bezierIKDriverCurve` on rigNull — POCI driver, not CV rig curve).

**Note:** Block **`squashMeasure` → `pointDist`** (per-segment driver distances) is **experimental** for bezier scale/stretch; default **`arcLength`** for production. Segment **Step Build → prechecks** emits a warning when `pointDist` is selected.

- **`r`** = `arcRatio` (global **arcLength**) or per-segment **`segRatio`** (**pointDist**): live measure ÷ joint rest (with existing **`masterScale`** rules).
- **`curveBlend = 1 + stretch * (r - 1)`** — unchanged **`stretch`** semantics.
- **`finalRatio = curveBlend * lengthScale`** — both attrs on **settings**; **`lengthScale`** default **1**.
- **translate**: per-segment `translate` on aim axis × `finalRatio`; secondary scales via squash blend
- **scale**: aim-axis scale × `finalRatio`
- Volume driver: see `_bezier_stretch_volume_driver` in `ik_utils` (uses **`finalRatio`**, not curve blend alone)
- **DG helpers** (`ik_utils`): **`_bezier_stretch_curve_blend_network`**, **`_bezier_stretch_apply_length_scale`**; global multiply node **`{base}_stretch_lengthScale_md`**; pointDist per segment **`{base}_stretch_seg_##_lengthScale_md`**, **`_bezier_stretch_point_dist_bind_rest`**, **`_ratioClamp`**, **`_msClamp`** on master scale divisor. Return dict adds **`mPlug_lengthScale`**, **`mLengthScaleMd`** (arc path).
- **Ribbon / curve segment + `squashSkipAim`**: **`IK.ribbon`** / **`IK.curve`** get **`setupAimScale=False`** when **`segmentStretchBy=scale`** and **`squashSkipAim`** is on (Segment, Head neck ribbon, Limb roll ribbon/curve) — no aim-length **`scaleZ`** stack fighting surface/constraints.
- **Module IK `bezier_spline_stretch` vs `segmentType`** (**`segment_bezier_module_ik_spline_stretch_profile`** in **`bezier_ik_block_utils`**): **`segmentType=parent`** — block **`segmentStretchBy`**, **`squashMeasure`**, volume squash, **`extraSquashControl`** on **`ml_ikUse`**; stores **`d_stretchInflateRes`** when volume on IK. **Any other `segmentType`** — module IK still runs stretch when the gate passes, but **`stretchBy='translate'`**, **`squashStretchMain='arcLength'`**, **`applyVolumeSquash=False`**, settings **`squash`** pinned **0** on IK path; **no** **`pointDist`** POCI on **`ikJoints`**. Segment **`rig_segments`** (ribbon, seg bezier, curve, …) owns block **`segmentStretchBy`**, volume squash, **`pointDist`**, and inflate overlay.
- **Rebuild**: existing rigs need **`rig_frame`** / limb **`rig_segments`** re-run to create **`lengthScale`** + multiply nodes (not attr-only).
- **`globalScalePlug`**: Segment passes **`get_blockScale` / `segMeasure`** master scale (`mPlug_masterScale`) — wired to driver **`masterScale`**. **arcLength** and **pointDist** both use **live measure / masterScale** over **bind rest** (pointDist: per-segment `distance / masterScale / bindSegDist`; do not divide bind rest by masterScale or global scale double-applies on volume squash).
- **`volumeSquashInflateOnly`**: When **True**, builds arc-length **volume squash** + optional **inflate** (`inflateDriveDirectParents`) on joint **secondary scales only** — does **not** connect translate / aim-axis stretch (spline IK keeps length channels). Segment parent **`ikSetup=spline`** uses this in **`rig_inflate`** with the skinned spline driver curve from **`RIGFRAME.spline`** (`mSplineDriverCurve` on the block instance).

#### Volume squash vs inflate (`squashExtraControl`)

| Layer | Settings attrs | Math (per squash joint) |
|-------|----------------|---------------------------|
| Volume | `{base}_outFactor_i` | `1 + (volBase − 1) × outFactor × squash` — **N−1** factors for **N** IK joints (per stretch span; tip has no `outFactor`). |
| Inflate | `{part}_inflateFactor_i`, `squashInflate`, `squashInflateOffset` | `volScale + factorSample × squashInflate` (`inflateAdd_*` mult + PMA). Ramp attrs **`inflateFactor_0 … inflateFactor_{N−1}`** for **N** joints (whole chain). **Direct-parent inflate** (`inflateScale` null): span joints use per-`outFactor` volume; **tip** uses global/last-span volume squash + last ramp slot (no `outFactor` attr). Settings factor attrs use block **`squashInflateFactorMin/Max`**; **`squashInflateFactorMin` may be negative** so some joints contract while others inflate. **`squash`**, **`squashInflate`**, **`squashInflateOffset`** are keyable; per-joint **`inflateFactor_*`**, **`outFactor_*`**, and ribbon **`aimFactor_*`** are **not keyable** but stay **visible** in the channel box / attribute editor. |

**Lib kwargs** (Segment + Head + Limb callers): `extraSquashControl`, `extraInflateControl` (inflate attrs can build when `squashExtraControl` is on even if volume squash is off on a given code path — **wiring** still requires the volume per-joint squash network today: `ml_inflate_pending` is populated only inside `extraSquashControl` stretch branches). `inflateFactorBaseName`, `inflateSlideGlobalCount`, `inflateSlideGlobalStart`, `inflateFactorMin/Max/Mode` (block **`squashInflateFactorMode`** → **`inflateFactorMode`** kwarg). **`skipTipInflate`**: skip chain-tip inflate wire + tip **`l_inflateDirectPlugs`** entry (Limb **last roll section**). **`inflateDriveDirectParents`**: IK joints get **volume squash only**; full inflate scale plugs are returned in **`l_inflateDirectPlugs`** for block wiring.

**FK + direct controls** (`squashInflateControl` on): inflate must not ride **`blendChainsScaleByAttr`** alone (FKIK=0 drops IK inflate). **`bezier_inflate_parent_direct_controls`** (via **`segment_inflate_parent_rig_direct_controls`** / limb **`_limb_bezier_inflate_parent_direct_controls`**) **inserts** visible **`{rigJoint}_inflateScale`** nulls into the **existing** control hierarchy: capture **`masterGroup`**’s DAG parent, parent **`inflateScale`** there, then **`masterGroup`** under **`inflateScale`**. Volume squash stays on IK/seg joint **scales**; inflate **scale** drives the null only — **do not** reparent directs under **`segJoints`** / deform chain for FK visibility.

#### Segment inflate build order (`segment.py`)

Segment **`__l_rigBuildOrder__`** runs **`rig_inflate`** **after** **`rig_segments`** and **before** **`rig_cleanUp`** (deform squash must exist on joints before overlay; direct **`masterGroup`** exists from **`rig_controls`**).

| Step | Inflate responsibility |
|------|-------------------------|
| **`rig_segments`** | **`IK.ribbon`** / curve / spline segment deform only — **no** inflate parent wire on ribbon segment types. **`segmentType=bezier`**: **`bezier_spline_stretch`** on seg chain → **`self.d_segmentBezierStretch`**. Combo **`ikSetup=bezier`**: **`segment_rig_segments_bezier_shared_module_curve`** — shared author curve, module driver for stretch. |
| **`rig_frame`** | **`ikSetup=bezier`** / Head **`neckIK=bezier`**: **`bezier_spline_stretch`** on **`ml_ikUse`** via stretch profile (**parent** full / **non-parent** translate-only). **`d_stretchInflateRes`** only when profile **`ikVolumeSquash`**. Spline IK: stash **`self.mSplineDriverCurve`** for **`rig_inflate`**. **Do not** parent **`inflateScale`** nulls here. |
| **`rig_inflate`** | **`squashInflateControl`** + overlay **`segmentType`**: build stretch result (if needed), then **one** **`segment_inflate_parent_rig_direct_controls`** pass. |

| Block / path | When | How inflate is built | Direct-control wire (inflate null) |
|--------------|------|----------------------|-------------------------------------|
| **Segment** parent + **`ikSetup=bezier`** | **`scaleSetup`**, squash, **`squashInflateControl`** | **`rig_frame`** → **`bezier_spline_stretch`**; **`rig_inflate`** → parent wire from **`d_stretchInflateRes`** | **Insertion** under pre-wire **`masterGroup`** parent (typically **`blendJoints[i]`**) |
| **Segment** **`segmentType=bezier`** | squash + inflate on seg stretch | **`rig_segments`** → **`bezier_spline_stretch`**; **`rig_inflate`** → parent from **`d_segmentBezierStretch`** | **Insertion** (directs usually parented under **`segmentJoints`** in **`rig_controls`** before **`rig_inflate`**) |
| **Segment** **`segmentType=ribbon` / `ribbonLive`** | squash on seg ribbon + **`squashInflateControl`** | **`rig_inflate`** → **`segment_inflate_stretch_result_from_volume_joints`** on **`segmentJoints`** with **`leave_joint_volume_wiring=True`** (read ribbon volume drivers; **do not** reconnect seg joint scale) | **Insertion** (same as bezier seg overlay) |
| **Segment** parent + **`ikSetup` spline** | **`scaleSetup`**, block **`squash`**, **`squashExtraControl`**, **`squashInflateControl`** | **`rig_frame`**: **`RIGFRAME.spline`** → stash **`self.mSplineDriverCurve`**. **`rig_inflate`**: **`bezier_spline_stretch`** with **`volumeSquashInflateOnly=True`**, **`inflateDriveDirectParents=True`**, driver = spline curve, joints = **`ikJoints`**; then **`segment_inflate_parent_rig_direct_controls`** on **`blendJoints`**. Spline IK length/stretch unchanged. | **Insertion** under **`blendJoints[i]`** (typical) |
| **Segment** parent + **`ikSetup` curve** | **`scaleSetup`**, **`b_squashSetup`** (ribbon squash on **`ikJoints`** in **`rig_frame`**) | **`rig_inflate`**: **`segment_inflate_stretch_result_from_volume_joints`** on **`ikJoints`** (reads existing volume drivers; reconnects IK to volume-only when not ribbon seg). | **Insertion** |
| **Head** | `neckIK=bezier` | Same stretch profile + **`rig_inflate`** timing as Segment; **`segmentType=parent`** → full IK stretch + **`d_stretchInflateRes`**; **non-parent** → translate IK stretch, ribbon/seg squash on **`segmentJoints`** | **Insertion** under **`blendJoints[i]`** |
| **Limb** | `segmentType=bezier`, `scaleSetup` | Per-section **`bezier_spline_stretch`** in **`rig_segments`** (**`skipTipInflate`** on **last roll section** — no end-direct **`inflateScale`**); inflate parent at end of **`rig_segments`** | **Insertion** — plug index from **`segJoints_{section}[i].drivenJoint`**, **not** parenting inflate under seg joint |

**Settings attrs** (`squashInflate`, **`squashInflateOffset`**, **`{part}_inflate_inflateFactor_*`**) are created when the inflate **DAG** build runs ( **`bezier_spline_stretch`** with **`extraInflateControl`**, or **`segment_inflate_stretch_result_from_volume_joints`** after volume drivers exist). **`{rig}_inflateScale`** nulls are inserted when **`l_inflateDirectPlugs`** is non-empty and **`bezier_inflate_parent_direct_controls`** runs (**after** direct **`masterGroup`** parents exist from **`rig_controls`** / limb segment parenting).

#### Direct inflate hierarchy (contract)

```
existingParent          # masterGroup.getParent() before inflate wire
  └── {rig}_inflateScale   # scale driven from stretch inflate plug
        └── masterGroup    # direct anim control stack unchanged below
```

**Do not** parent **`inflateScale`** under **`segJoints`** / IK deform joints to “follow seg squash” — that replaces FK blend parenting. Limb maps stretch plug index → rig joint via **`segJoints_{section}[i].drivenJoint`** only.

#### Parent `ikSetup=spline` — inflate vs `{rig}_inflateScale` (troubleshooting)

| Symptom | Likely cause | Fix |
|---------|----------------|-----|
| Settings **`squashInflate`** / **`inflateFactor_*`** exist, **no** **`{rig}_inflateScale`** nulls | **`rig_inflate`** skipped parent wire (`skip parent wire` log) — no **`l_inflateDirectPlugs`** | Full module rebuild through **`rig_inflate`** (not attr-only refresh). Check Script Editor. |
| **`skip parent wire \| segmentType:parent ikSetup:spline`** | Missing **`mSplineDriverCurve`** ( **`rig_frame`** did not return curve), or **`squashExtraControl`** off, or **`scaleSetup`** off | **`scaleSetup`**, **`squashExtraControl`**, **`squashInflateControl`** on; block **`squash`** not **none**; rebuild **`rig_frame`** then **`rig_inflate`**. |
| No **`spline volume squash + inflate`** log | **`squashInflateControl`** off, or **`segmentType`** not in overlay set (**`parent`**, **`ribbon`**, **`ribbonLive`**, **`spline`**, **`curve`**) | Enable **`squashInflateControl`**; parent **`segmentType`** for standard FK/IK → blend modules. |
| Inflate attrs on, ribbon seg path | **`segment_inflate_stretch_result_from_volume_joints`** created settings then found **no** volume on **`segmentJoints`** | Rebuild **`rig_segments`** first; ribbon squash must drive seg joint **`scaleX`/`scaleY`** (or aim-axis volume attrs) before **`rig_inflate`**. |
| Wrist/end direct **`masterGroup`** under **seg/bezier joint** after inflate | Old path parented **`inflateScale`** on **`segJoints_{section}[i]`** | Reload **`bezier_ik_block_utils`**; rebuild **`rig_segments`** / **`rig_inflate`**. Expect **`blendJoint → inflateScale → masterGroup`**. Limb end: **`skipTipInflate`** on last roll section — end direct may have **no** **`inflateScale`**. |

**Success logs (Script Editor):** `rig_inflate` → `spline volume squash + inflate | driver:<splineCurve>` → `inflate direct parents | ikSetup:spline segmentType:parent | plugs:N` (expect **N** = joint count for inflate ramp, incl. tip — see § volume vs inflate counts).

#### What NOT to do (Segment ribbon / ribbonLive inflate)

| Do not | Why |
|--------|-----|
| Call **`IK.bezier_spline_stretch`** with **`volumeSquashInflateOnly=True`** + **`replaceExisting=True`** on **`segmentJoints`** after **`IK.ribbon`** | Disconnects ribbon volume scale wiring and rebuilds squash from the measure curve — **breaks base segment squash/stretch**. |
| Run inflate overlay in **`rig_frame`** before **`rig_segments`** | Segment ribbon squash does not exist yet; volume driver read fails or targets wrong joints. |
| Pass **`extraInflateControl`** / inflate ramp kwargs through **`squash_stretch_ik_share_kwargs`** into **`IK.ribbon`** | **`shared_dat`** strips those keys on purpose; ribbon IK does not own inflate settings. |
| **`_bezier_stretch_connect_inflate_joint_or_direct`** on ribbon **`segmentJoints`** when **`leave_joint_volume_wiring=True`** is required | Reconnects joints to “volume-only” plugs and fights ribbon **`scaleX`/`scaleY`** (or MD) squash. Inflate belongs on **`{rig}_inflateScale`** above directs only. |
| Add ad-hoc DG (**`floatConstant`**, fake unity volume nodes, factor-only networks without reading existing volume) for ribbon | Use **`segment_inflate_stretch_result_from_volume_joints`** sampling **existing** drivers, or full **`bezier_spline_stretch`** only on chains **you** own (parent IK bezier, **`segmentType=bezier`** seg solve). |
| Create settings inflate attrs in a separate “ensure” path when stretch did not build | If inflate built correctly, settings attrs are already there; fix the stretch/overlay path instead. |

Rebuild module after py3 edits.

#### `IK.ribbon` skin weight tighten (Python 3)

Shared legacy path for **`ikSetup=ribbon`** / **`ribbonLive`** in **`segment.rig_frame`**, **`segmentType=ribbon` / `ribbonLive`** in **`rig_segments`**, and other callers — **not** Bezier-spline-specific, but often hit while rebuilding Segment with squash on after inflate/ribbon work.

| Symptom | `TypeError: slice indices must be integers…` in **`RIGSKIN.surface_tightenEnds`** at `l_cvsUse[:blendLength]` |
|---------|------------------------------------------------------------------------------------------------------------------|
| Cause | **`blendLength = int_lenJoints / 2`** is a **float** in py3. When **`extendEnds`** is on (block default **`ribbonExtendEnds=True`**) or **`int_lenInfluences > 2`**, **`IK.ribbon`** sets **`mode_tighten=None`**, so **`surface_tightenEnds`** does **not** run the **`twoBlend`** branch that recomputes integer **`blendLength`**. |
| Typical block setup | **`ikSetup=ribbon`**, **no** mid IK (only start/end **`ribbonIKDrivers`** → **`int_lenInfluences == 2`**), squash on ( **`get_blendList`** log before skinning is normal). |
| Fix (py3) | **`ik_utils`**: **`blendLength = int_lenJoints // 2`** (both ribbon skin blocks). **`skin_utils`**: **`blendLength = int(blendLength)`** after **`twoBlend`** reassignment in **`surface_tightenEnds`** and **`curve_tightenEnds`**. |

Reload **`ik_utils`** / **`skin_utils`** (module rebuild or core reload) after py3 sync.

**Inflate factor sampling** (`_bezier_stretch_inflate_offset_sample_network`): clamped `s` → floor index + fractional lerp via **choice** + **blendTwoAttr**; floor from a hidden **`floorUtil`** transform + expression (`floor(sampleS)`). DG nodes are created with **`_bezier_stretch_dg_named_node`** (`cgmMeta.cgmNode(mc.createNode(type))` then `rename`) — do not use `cgmNode(nodeType='floatMath')` (invalid / wrong node type in scene). All `{part}_inflateFactor_0..maxIdx` attrs are ensured on settings before sampling (`_bezier_stretch_inflate_factor_plugs_ensure`); **maxIdx = joint count − 1** (not `outFactor` span count − 1).

**Rebuild**: Changing inflate DAG requires re-running **`bezier_spline_stretch`** (module segment/limb build), not attr-only refresh. Reload **`ik_utils`** after py3 edits.

#### Stretch verification (Maya)

| Case | Expect |
|------|--------|
| Bind **`r=1`**, **`stretch=1`**, **`lengthScale`** 0.5 → 2 | Chain length scales; **`stretch`** alone unchanged vs pre-**`lengthScale`** rigs |
| **`r=1.2`**, **`stretch=1`**, **`lengthScale=1`** | **`finalRatio=1.2`** (same as before **`lengthScale`**) |
| **`r=1.2`**, **`stretch=0.5`**, **`lengthScale=1`** | **`finalRatio = 1 + 0.5×0.2 = 1.1`** |
| **`stretch=0`**, **`lengthScale=2`** | **`finalRatio=2`** (rest × 2) |

### `RIGBEZIER.bezier_controls_wire_from_handles`

Index-aligned main IK cubes + tangent sub spheres; subs parent to main handle (not main `masterGroup`).

### `RIGCONSTRAINT.blendChainsScaleByAttr`

Per-joint `blendTwoAttr` on `scaleX/Y/Z`: FK = `input[0]`, IK = `input[1]`, driver = **FKIK** (0 FK, 1 IK). Used for Segment scale setup instead of scaleConstraint FK/IK → blend.

### `bezier_ik_connect_spline_advanced_twist` (`bezier_ik_block_utils`)

After **`bezier_ik_wire_handle_twist_from_controls`** in **`RIGFRAME.bezier`**: ikSpline handle **`dTwistValueType`** = Start/End (not ramp); **`dTwistStart`** / **`dTwistEnd`** driven **only** by **`twistBaseAdd`** / **`twistEndAdd`** on module base/end IK (not control rotate). Main twist distribution uses advanced-twist **world-up objects**. Then enables spline IK advanced twist, sets **`dForwardAxis`** / **`dWorldUpAxis`** from module orientation, **`dWorldUpMatrix`** / **`dWorldUpMatrixEnd`** from base + end IK controls. **Advanced-twist world-up objects** stay on **`ml_bezierMainIK`** span (or **`mTwistEndControl`** on Head split), **not** swapped to hip/chest when hips chain layout is used. Optional per-block **`ikSplineTwistUpStart`** / **`ikSplineTwistUpEnd`** override **`dWorldUpVector`** / **`dWorldUpVectorEnd`**. Limb roll sections call the same helper for WU only (**`wire_driver_twist_from_mains`** no longer feeds handle twist from mains). Classic **`ikSetup=spline`** still uses ramp twist via **`IKHandle_addSplineIKTwist`** **`twistSetupMode='ramp'`**.

### `segment_bezier_module_ik_spline_stretch_profile` (`bezier_ik_block_utils`)

Returns kwargs/log flags for module **`ikJoints`** **`bezier_spline_stretch`** in **`segment.py`** / **`head.py`** **`rig_frame`**. **`block_uses_bezier_module_ik`**: **`ikSetup=bezier`** or Head **`neckIK=bezier`**. Gate caller: **`_segment_bezier_should_run_spline_stretch(self, mBlock)`** ( **`scaleSetup`** + squash **simple** / **both** / **none** ).

### `RIGFRAME.segment_mid` (Head mid IK aim)

**`linearTrack`**: mid controls ride **`mainDriver`** + **`attach_toShape`**. Head + **`ikMidAimSetup`**: shared root→end orientation via **`midRootEnd_aimRef`** under start IK (**`mIKBase`**), **`orientConstraint`** onto each **`mainDriver`**.

---

## MRS build flow (Segment)

```mermaid
flowchart TD
  skeleton[rig_skeleton] --> ssc[segmentScaleCompensate on ik/fk/blend if squash]
  shapes[rig_shapes bezier IK cubes + subs] --> frame[rig_frame]
  frame --> bez[RIGFRAME.bezier]
  bez --> stretch{scaleSetup and stretch gate?}
  stretch -->|yes| bstr[IK.bezier_spline_stretch profile parent or translate IK]
  frame --> endFollow[segment_ik_spline_orient_follow_setup tip]
  frame --> hipsFollow[segment_ik_base_orient_follow_setup when ikBase hips]
  hipsFollow --> ikBlendUse[ml_ikBlendUse index 0 ikOrientFrame]
  frame --> fkik[blendChainsBy parent + blendChainsScaleByAttr on ml_ikBlendUse if scaleSetup]
```

### rigNull messages (bezier)

| Message / msgList | Content |
|-------------------|---------|
| `bezierIKDriverCurve` | Hidden driver for stretch `curveInfo` (child of rigNull from `rigFrame_utils.bezier`) |
| `bezierIKSubControls` | Tangent sub control joints |
| `bezierIKTrackCurves` | Linear track curves (aux); `overrideVisibility` → settings `result_IKon` (FK/IK vis) |
| `bezierIKSubsBase`, `bezierIKSubsMidN`, `bezierIKSubsEnd` | Subs per main IK slot |
| **`bezierIKChainStart`**, **`bezierIKChainEnd`** | Hips parent bezier only — chain-end CV mains (not hip/chest **`controlIK*`**); wire/switch targets on **`ikJoints`** |
| **`segmentBezierIKCurve`**, **`segmentBezierIKDriverCurve`**, **`segmentBezierIKSplineHandle`**, **`segmentBezierIKControlsGrp`** | **`ikSetup=bezier`** + **`segmentType=bezier`** — separate segment bezier + driver (not shared **`bezierIKCurve`** shape); CVs driven from same module IK mains/subs as **`rig_frame`** |

Session build buffers on block instance: `md_bezierIKSubsBySlot`, `ml_bezierIKSubControls`, `ml_bezierIKTrackCurves` — reinit after `MODULECONTROL.register` (`bezier_ik_reinit_session_meta`). **`rig_dataBuffer`**: `ml_ikBlendUse = None`. **`rig_frame`** (when IK on): `ml_ikBlendUse = copy(ikJoints)`; hips base follow replaces **`ml_ikBlendUse[0]`** with **`*_ikOrientFrame`** inside **`segment_ik_base_orient_follow_setup`** (pass block build **`self`**). FK/IK parent + scale blend uses **`self.ml_ikBlendUse`**, not raw **`ml_ikJoints`**, so chain2 index **0** is the orient frame while **`ml_ikUse[0]`** stays the solver pelvis.

**Pickwalk / ordered IK DAG lists:** At **`rig_controls`**, each main IK DAG gets a **`bezierIKSubs`** msgList (ordered sub **transforms** only). **Segment (`ikSetup=bezier`, `segmentType=parent`, default `ikBase`):** **`controlsIK`** = full bezier chain on **`controlIKBase`** / mids / **`controlIK`**. **Segment hips parent bezier (`ikBase=hips`):** register hip/chest **`controlIKBase`** / **`controlIK`** as main IK; chain CVs via **`rig_controls_bezier_segment_parent_hips_chain`** (**`mPlug_visSub`** → main **`masterGroup.visibility`**, same step as **`segmentType=bezier`** handle registration); **`controlsIK`** = **`controller_getDat_ik_merge_bezier_msglist`**(hip + chest + built chain). **Segment (`segmentType=bezier`):** **`controlsSegmentBezier`** = handle CV pickwalk; **`controlsIK`** = module base/end IK. **Head (`neckIK=bezier`):** primary **`controlsIK`** = neck root + **`headIK`**; neck CV chain on **`controlsNeckBezier`**. **Limb (`segmentType=bezier`):** foot/hand IK plugs first in **`d_controlDat_links['ik']`**, then **`controlsSegmentBezier`**. Flat **`bezierIKSubControls`** is auxiliary. **`bezier_ik_ensure_aggregate_ik_msglist`** repairs aggregate lists at verify. Registered anim controls use **`controlAnim`** + **`ikBezier`** / **`ikBezierSub`** modifiers. Track curves stay on **`bezierIKTrackCurves`** only.

### Hips bezier chain (`ikSetup=bezier`, `ikBase=hips`)

Spine-style layout: animators keep familiar **hip** and **chest** IK (`controlIKBase` / `controlIK` from **`RIGSHAPES.ik_base`** / **`ik_end`**); bezier spline CVs are **separate** transforms on the IK joint span, not prerig mid IK helpers and not the legacy **`handleJoints[1]`** spine handle.

| Build step | Behavior |
|------------|----------|
| **`rig_skeleton`** | Skip duplicate **`handleJoints`** at FK index **1** (no extra **`spine_*_handle`**). |
| **`rig_shapes`** | Skip **`RIGSHAPES.segment_handles`** on handle joints. **`rig_shapes_bezier_segment_hips_chain_mains`**: create **`bezierIKChainStart`** / **`bezierIKChainEnd`**, snap to **`ikJoints[0]`** and **`ikJoints[int_handleEndIdx]`**; **`rig_shapes_bezier_ik_apply_from_fk`** with **`skip_base_end=True`** (mids only; hip/chest cubes stay on **`controlIK*`**). |
| **`rig_controls`** | Generic mid IK loop skipped for hips chain; **`rig_controls_bezier_segment_parent_hips_chain`** registers chain mains/subs + **`controlSegMidIK`**; hip/chest IK registered above as usual. |
| **`rig_frame`** | **`rig_frame_bezier_segment_hips_chain_master_groups`**: **`bezierIKChainStart.masterGroup`** → **`controlIKBase`**, **`bezierIKChainEnd.masterGroup`** → **`controlIK`** (after hip/chest **`masterGroup`** → **`mIKGroup`**). **`bezier_ik_resolve_main_ik_list`** drives **`RIGFRAME.bezier`** wire and slot subs (not raw **`controlIK*`** as CV mains). Driver **`twistBaseAdd`** / **`twistEndAdd`** only on **`controlIKBase`** / **`controlIK`** (not chain CVs); **advanced-twist WU** targets unchanged (**`ml_bezierMainIK`** span). Skip legacy **`RIGFRAME.segment_handles`** on handle joints. **Orient follow:** end via **`segment_ik_module_follow_end_control`** + **`segment_ik_spline_orient_follow_setup`**; hips base via **`segment_ik_module_follow_base_control`** + **`segment_ik_base_orient_follow_setup(self, ml_ikJoints[0], …)`** (see § Segment IK orient follow). |

**Detection:** **`segment_bezier_ik_uses_hips_chain_mains(mBlock)`** — `ikSetup=bezier` and `ikBase=hips` only (not gated on **`segmentType`**). No new block enum (do not overload **`ikBezierSub`** modifier naming).

**Reload:** **`BEZIERIKBLOCK`** / **`bezier_ik_block_utils`** with segment stack (`Builder` Step Build reload, **`general_utils.reloadMRSStuff`**).

### Segment IK end shapes (`rig_shapes` → `RIGSHAPES.ik_end`)

Applies whenever Segment **`ikSetup`** builds **`rigNull.controlIK`** (parent bezier, hips chest handle, spline/ribbon end IK, etc.). **`rig_shapes`** passes **`ml_fkCastTargets`** ( **`fkAttachJoints`** or FK joints) into **`ik_end`**.

| Layer | Contract |
|-------|----------|
| **Control transform** | **`ik_end`** per **`ikEnd`**: e.g. **`tipBase`** → **`ml_handleTargets[int_handleEndIdx]`** duplicate; **`helper`** → **`ikEndHandle`**; **`tipEnd`** → **`ikEndHandle`** at last **rig** joint; **`tipMid`** → midpoint along **`ml_rigJoints`**. |
| **Cast shape (`ikEndShape=cast`)** | **`builder_utils.shapes_fromCast`**, **`mode='ikEndFrameHandle'`**: one **`RAYS.cast`** from **`_ik_end_cast_source_dag`** → **`SURF.get_splitValues`** with **`insertMax=True`** (same insets/connectors/offset as FK **`frameHandle`** last span). Shape geometry follows cast **U** on the proxy loft; **pivot** stays on the control transform above. |
| **Cast DAG vs pivot** | Intentionally split when **`tipBase`**: cast **U** from **`fkAttachJoints[int_handleEndIdx]`**; control at **`ml_handleTargets[int_handleEndIdx]`** (same index, attach vs FK joint world position may differ). |

| **`ikEnd`** | Cast source DAG |
|-------------|-----------------|
| **`helper`** | **`mBlock.ikEndHandle`** |
| **`tipBase`** | **`ml_fkCastTargets[int_handleEndIdx]`** (typically **−2**) |
| **`tipEnd`** | **`ml_rigJoints[-1]`** |
| **`tipMid`** | Positioned **`controlIK`** after midpoint solve (cast uses that transform) |

**Logs:** **`ik_end`** boundary **`log.info`**: **`ikEnd`**, **`endIdx`**, **`castDag`**, position. Cast fail → fallback parent **`ml_fkShapes[int_handleEndIdx]`** (not always **`[-1]`**).

**Reload:** **`rigShapes_utils`**, **`builder_utils`**, **`segment`** — module rebuild / MRS reload dependencies; no **`mClass`** / **`CGM._reload()`** required.

### Segment IK orient follow (`bezier_ik_block_utils`)

**`rig_frame`** (module IK: **`ikSetup`** **bezier** or **spline**). Follow attrs live on module IK anim controls only — **`segment_ik_module_follow_end_control`** → **`rigNull.controlIK`**; **`segment_ik_module_follow_base_control`** → **`rigNull.controlIKBase`** (not **`bezierIKChain*`** CV mains).

| Helper | When | Nodes |
|--------|------|--------|
| **`segment_ik_spline_orient_follow_setup`** | End (tip) follow | **Skin** = end **`ml_ikJoints[-1]`**; span = **`_splineEnd`** dup on **`ml_ikUse`**; follow dup parented to **`controlIK`** (or caller influence). |
| **`segment_ik_base_orient_follow_setup`** | **`ikBase=hips`** base follow | Pass **`self`** (segment build instance). Creates **`{pelvis}_ikOrientFrame`** under **`ml_ikJoints[0]`**; **`{pelvis}_splineControlStart`** under **`controlIKBase`**. Writes **`self.ml_ikBlendUse[0] = m_ik_orient_frame`**. **`ml_ikJoints[0]`** / **`ml_ikUse[0]`** stay the solver pelvis — no orient constraint on pelvis. |

**`rig_segments`** (segment deform ribbon/bezier): **`followEnd`** on last **`segmentJoints`** entry may use **`ml_handleJoints[-1]`** as follow influence — separate from module **`rig_frame`** **`controlIK`** contract.

**Rejected (do not restore):** orient FK/IK or **`followIK`** blend directly on **`ml_ikUse[0]`** pelvis; **`_ikSplineRoot`** reparent of solve chain; pelvis sibling **`*_ikOrientBlend`**.

### Squash skeleton invariant

When `b_squashSetup` and IK on: **`rig_skeleton`** calls `_squash_ik_fk_blend_segment_scale_compensate` — **`segmentScaleCompensate = True`** on **ik**, **fk**, and **blend** chains (not segment measure joints).

### Aim axis for stretch

`_bezier_ik_stretch_aim_axis` uses `d_orientation['stringAim']`, not rotate-order string alone.

### Limb bezier segments

**`limb.py`**: `segmentType=bezier` per roll section — `_limb_rig_segments_bezier_squash_stretch` → `IK.bezier_spline_stretch` on section IK chain with shared settings, `inflateFactorBaseName='{partName}_inflate'`, and `_limb_bezier_inflate_slide_global_spec` for cross-section inflate indices (span slots = **sum(N−1)** per roll section). Volume squash gated by `_limb_bezier_volume_squash_active`.

**Limb end joint (last roll section tip — wrist/ankle culled IK end):** volume squash on deform joint **yes** (no `{base}_outFactor_*` on tip, same as span-based squash extra control). **Inflate overlay no** on that joint: **`skipTipInflate=True`** on the last roll section’s stretch build — no `{rig}_inflateScale` above the end direct control; span joints in that section still get inflate + direct-parent wire. Segment / Head neck tip inflate unchanged.

**Interior seg aim world-up (Limb only):** `_limb_bezier_seg_handle_reg_curve` / `_limb_rig_segments_bezier_section_seg_aims` set forward/back **aimConstraint** `worldUpObject` to the roll section **start main** (`ml_mains[0]` / `handleJoints[section_idx]` ikBezier anim). **stableEnd** / **stable** follow blends and `curveSeg_{section}` networks are unchanged.

**End segment main stable / followRoot (Limb only, all profiles):** `_limb_rig_segments_bezier_end_main_follow_root` on the culled IK end main (**`handleJoints[-1]`** — wrist/ankle, not prerig **`int_handleEndIdx`** alone). **`followRoot`** + **`stableEnd`**. **Call site:** **`addBall` / `addLeverEnd`** → section **`section_idx + 1 == len(handleJoints)−1`**, parent **`handleJoints[-1]`**; else **last roll section**, parent **`ml_mains[-1]`** (typical arm/wrist). **`{endMain}_back_aimer`** world-up from **`segmentEndHandleUp`** via **`_limb_segment_end_back_aimer_world_up_node`**. Rebuild **`rig_segments`** after enum or wiring changes.

### Head neck bezier (not Segment parity for controls)

**`head.py`** with **`neckIK=bezier`**, **`neckControls > 1`** (any allowed **`segmentType`**):

| rigNull / control | Role |
|-----------------|------|
| **`headIK`** | Main head anim IK — **end of primary IK pickwalk** (`controlsIK`: neck root + **`headIK`**). |
| **`controlIK`** / **`controlIKBase`** / mids / subs | Neck **bezier** system only — ordered on **`controlsNeckBezier`** (not replacing foot/head primary IK). |
| **`controlsNeckBezier`** | Full neck bezier pickwalk (base → … → neck-end **`controlIK`** + subs). Walk **after** **`controlsIK`** in `d_controlDat_links['ik']`. |

**`rig_frame` (split head path, `neckControls > 1`):** Ribbon end **`ribbonIKDrivers[-1]`** → neck-end **`controlIK`** (not **`headIK`**). **`RIGFRAME.bezier`** on **`ml_ikUse`** (last entry = **`_splineEnd`** dup of head IK joint, parented under **`ml_ikJoints[-2]`**). **`ml_ikJoints[-1]`** is parented under **`headIK`** only — **not** under neck-end **`controlIK`**, and **without** the Segment-style **`pointConstraint` + `followIK` + `_splineControl`** stack on the head IK joint. **`mTwistEndControl=headIK`** for driver twist / advanced twist world-up end. **`rig_controls`**: neck-end **`controlIK`** **`get_switchTarget`** → **`headIK`**; **`int_handleEndIdx = -2`** sizes end bezier cube from last neck FK. **`rig_cleanUp`**: neck-end **`controlIK`** dyn parents include **`headIK`**; separate **`headIK`** dyn parent pass when **`headIK` ≠ `controlIK`**. No **`parentConstraint`** from **`headIK`** onto neck-end **`controlIK`**. Legacy single-control neck (**`headIK` == `controlIK`**) keeps Segment-like end follow on **`ml_ikJoints[-1]`**.

**`rig_cleanUp`:** When **`headIK`** ≠ **`controlIK`**, **`headIK`** gets its own **`cgmDynParentGroup`** rebuild (same parent list as neck **`controlIK`** / **`controlIKBase`**: attach/world/end pivots, **`controlIKNeckRoot`**, parent module IK/root, **`mRoot`** when present). Not **`blendHead`** — that alias is for **look-at** dyn parents on the neck blend joint, not the head anim IK.

Legacy neck modes (spline / ribbon / single **`controlIK`** on head) keep one transform for **`headIK`** + **`controlIK`**.

**Mid IK (`ikMidSetup`) on Head:** **`ikMidAimSetup`** exists only on **`head.py`** (not Segment). Ribbon / spline neck paths use existing handle aim; bezier + **`linearTrack`** + aim on uses root→end ref (above). Do not use **`handle_fixTwist`** on bezier ikSpline handles (rp-only).

---

## Reload / test

| Change | Maya |
|--------|------|
| `ik_utils`, `bezier_utils`, `constraint_utils`, `rigFrame_utils`, segment build funcs (no `mClass`) | Rebuild segment or module **Reload Dependencies** on MRS tool if applicable |
| **`rigShapes_utils`**, **`builder_utils`** (`ikEndFrameHandle`, **`ik_end`**) | Rebuild module **`rig_shapes`** (or full build); reload deps on block tool |
| `mClass` / meta registry | `import cgm.core as CGM; CGM._reload()` then rebuild |

---

## Revision history

| Date | Summary |
|------|---------|
| 2026-10-29 | **Module IK stretch split:** **`segment_bezier_module_ik_spline_stretch_profile`** — **`segmentType=parent`** full **`segmentStretchBy`** + volume on **`ikJoints`**; **non-parent** **`translate`** + arcLength on IK, deform **`rig_segments`** keeps block squash/stretch; **`_segment_bezier_should_run_spline_stretch`** gate; Head **`neckIK=bezier`** + **`block_uses_bezier_module_ik`**; removed Head precheck **neck bezier requires parent segment** |
| 2026-10-28 | **Segment bezier:** **`twistBaseAdd`** / **`twistEndAdd`** on **`controlIKBase`** / **`controlIK`** only; advanced-twist WU inputs unchanged (**`ml_bezierMainIK`**) |
| 2026-10-28 | **Segment `ikEndShape=cast`**: **`ikEndFrameHandle`** in **`shapes_fromCast`** (FK last **`frameHandle`** span to loft max U, start **U** from **`ikEnd`** cast DAG); **`RIGSHAPES.ik_end`** keeps separate control pivot; **`ml_fkCastTargets`** from **`rig_shapes`** |
| 2026-10-28 | **`bezier_inflate_parent_direct_controls`**: **`inflateScale`** **insertion** — preserve pre-wire **`masterGroup`** DAG parent; limb uses **`segJoints`** only for **`drivenJoint`** / plug index, not inflate null parent |
| 2026-10-28 | **Limb** end **`followRoot`**: hybrid call — ball/leverEnd culled end index vs last roll + **`ml_mains[-1]`** for arm/wrist |
| 2026-10-27 | **Limb** block **`segmentEndHandleUp`** (`stableUp` \| `last`, default **`stableUp`**) — end-segment back **`aimer`** world-up on bezier + ribbon roll paths |
| 2026-10-27 | **Limb bezier:** last roll section **`skipTipInflate`** on **`bezier_spline_stretch`** — limb-end joint keeps volume squash, no tip **`inflateFactor`** / **`inflateScale`**; global inflate ramp stays span-indexed (**`_limb_bezier_inflate_slide_global_spec`**) |
| 2026-10-23 | **Segment `rig_frame` orient follow (Maya-verified):** **`segment_ik_*_orient_follow_setup`**; hips **`*_ikOrientFrame`** + **`ml_ikBlendUse[0]`** for FK/IK; **`followIK`** on **`controlIK`/`controlIKBase`**; end defaults bezier **1.0** / spline **0.0** |
| 2026-10-23 | **`ikSetup=bezier`** + **`segmentType=bezier`**: **`rig_prechecks`** fail — *Bezier/bezier is not a viable path. Bezier/Ribbon or Bezier/Parent is recommended* |
| 2026-10-22 | **`ikSetup=bezier`** + separate segment deform: module IK volume off when **`segmentType` ≠ parent**; **Oct 29** adds **`segment_bezier_module_ik_spline_stretch_profile`** (**translate** IK stretch, segment owns block stretch/squash) |
| 2026-10-22 | Segment **`rig_prechecks`**: removed **`ikSetup=bezier`** ↔ **`segmentType`** locks (allow experimental combos; **parent** remains signed-off path) |
| 2026-10-23 | **pointDist** translate stretch stability: bind-time POCI U only; **`_bezier_stretch_point_dist_bind_rest`**; clamp seg ratio + master scale divisor. **Ribbon `squashSkipAim`**: gate **`setupAimScale`** off when skip aim + scale stretch (segment/head/limb). |
| 2026-10-22 | Segment **`ikSetup=bezier`** + **`ikBase=hips`** + **`segmentType=parent`**: **`bezierIKChainStart`/`End`**, skip spine handle joint; shapes/controls/visSub chain; **`rig_frame`** masterGroup under hip/chest IK; **`bezier_ik_resolve_main_ik_list`** for wire |
| 2026-10-22 | Block attr **`ikSplineBezierMode`** (was **`splineBezierMode`**) on Segment / Head / Limb + **`shared_dat`**; **`block_bezier_anchor_mode`** legacy read. Settings **`squash`** default **1.0** on volume squash (**`bezier_spline_stretch`** + segment/limb post-build); **0** when volume squash off |
| 2026-10-22 | **`IK.ribbon`** py3: integer **`blendLength`** for skin **`surface_tightenEnds`** (`// 2` in **`ik_utils`**, **`int()`** guard in **`skin_utils`**) — fixes ribbon **`rig_frame`** / segment ribbon build when **`extendEnds`** + two influences |
| 2026-10-21 | **Segment** `segmentType=bezier` + `ikSetup=bezier`: handle CV shapes/controls, `segment_rig_segments_bezier`, ikJoints follow seg; `controlsSegmentBezier` pickwalk |
| 2026-10-15 | **Head** neck bezier **`controlsIK`** pickwalk + **`controller_getDat`** / **`d_controlDat_links`**; **`controlSegMidIK`** msgList |
| 2026-10-15 | **Head** **`ikMidAimSetup`** + **`linearTrack`**: **`midRootEnd_aimRef`** under **`controlIKBase`**, **`orientConstraint`** on mid **`mainDriver`** (not handle-chain aim) |
| 2026-10-15 | **Segment** + **Head** **`ikSplineTwistUpStart`** / **`ikSplineTwistUpEnd`**; **`bezier_ik_connect_spline_advanced_twist`** + **`_apply_hair_spline_ik_advanced_twist`** (no **`handle_fixTwist`** on bezier) |
| 2026-10-15 | **Inflate**: negative **`inflateFactor_*`** / **`inflateFactorMin`** allowed — contract vs inflate via **`volScale + factor × squashInflate`** |
| 2026-10-15 | **pointDist** stretch: fix `_bezier_stretch_seg_final_ratio_network` — `masterScale` on live distance only (bind rest static); Maya-verified vs arcLength under puppet scale |
| 2026-10-19 | **Head** neck bezier (split): **`head_*_ik_sknJnt`** clean child of **`headIK`**; no end **`pointConstraint` / `followIK` / `_splineControl`** on head IK joint; **`ml_ikUse`** spline end under **`ml_ikJoints[-2]`**; skip **`scaleConstraint(headIK → last ik)`** when split |
| 2026-10-19 | **Head** neck-end **`controlIK`**: space / switch target + dyn parent **`headIK`** (not blend joint) |
| 2026-10-19 | Block **`squashInflateFactorMin/Max/Mode`** (Squash/Stretch UI; replaces **`inflateFactor*`** names) — ramp for settings **`{part}_inflate_inflateFactor_i`**, separate from **`squashFactorMin/Max`** |
| 2026-10-19 | **Head** + **Limb** bezier inflate: same **`inflateDriveDirectParents`** / direct-parent contract as Segment |
| 2026-10-19 | **`bezier_spline_stretch`**: settings **`lengthScale`**; **`finalRatio = curveBlend × lengthScale`**; shared curve-blend + length-scale DG helpers (arcLength + pointDist) |
| 2026-10-22 | **Parent `ikSetup=spline`**: **`rig_inflate`** + **`bezier_spline_stretch`** **`volumeSquashInflateOnly`** on **`ikJoints`** (driver **`mSplineDriverCurve`** from **`RIGFRAME.spline`**); **`{rig}_inflateScale`** on **`blendJoints`** like bezier |
| 2026-10-21 | **Segment `rig_inflate`** step after **`rig_segments`**; ribbon/ribbonLive overlay via **`segment_inflate_stretch_result_from_volume_joints`** + **`leave_joint_volume_wiring`**; **do not** second-pass **`bezier_spline_stretch`** on ribbon seg joints |
| 2026-10-19 | **Segment** bezier inflate: **`inflateDriveDirectParents`** + **`segment_inflate_parent_rig_direct_controls`** so FK sees inflate on direct-control parents (not FK/IK scale blend) |
| 2026-10-19 | **Head** neck bezier: drop **`headIK → controlIK`** parent constraint; ribbon end on neck-end **`controlIK`** |
| 2026-10-15 | **Head** **`rig_cleanUp`**: dyn parent rebuild on separate **`headIK`** (was only on **`ml_ikControls`** / **`controlIK`**) |
| 2026-10-15 | **Head** neck bezier: split **`headIK`** (anim) vs **`controlIK`** (neck-end ikBezier); ribbon end + constraint follow; stretch chain through neck + spline end |
| 2026-10-14 | `bezier_spline_stretch` additive inflate (`squashInflate`, separate inflate factor ramp, offset slide); limb + segment block attrs; DG named-node + floor util sampling (no `floatMath`) |
| 2026-10-13 | Docs: MRS build matrix (parent vs bezier `segmentType`); roadmap table in feature + branch |
| 2026-10-13 | Step Build: `ui_stepBuild` runs `mode='prechecks'` first; failures listed in window |
| 2026-10-13 | Segment parent bezier: stretch translate/scale, SSC at skeleton, `blendChainsScaleByAttr`, volume driver split for translate vs scale |
| 2026-10-12 | Initial feature stub; lib `bezier_spline` + CV rig (branch doc) |
