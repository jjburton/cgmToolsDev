# Long-running UI work needs progress

Applies to any tool button or menu that can keep Maya busy for more than a moment: multi-frame bake, timeline
export, batch rebuild, heavy scene walks, many constraints/duplicates. It must show visible progress so artists
know the session is working, and support cancel where safe.

## Where progress lives

| Layer | Responsibility |
|-------|----------------|
| UI handler (`tools/`) | Thin: validate, call backend, show result. No tight loops over frames/nodes without backend progress |
| Backend (`rig/`, `lib/`, `mrs/`) | Owns the loop; drives the progress bar and honours cancel |

Don't add progress only in the UI while the backend still runs one opaque `mc.bakeResults` / export call. Wrap or
step the work in the backend, or pass a shared progress handle into helpers.

## Standard bar (`cgm.core.classes.GuiFactory`, alias `CGMUI` / `cgmUI`; match the importing module)

```python
import cgm.core.classes.GuiFactory as CGMUI

_progressBar = None
try:
    _progressBar = CGMUI.doStartMayaProgressBar(
        stepMaxValue,
        'Short action label | context',
        interruptableState=True)
except Exception:
    _progressBar = None

try:
    for i, mObj in enumerate(ml_work):
        if _progressBar and mc.progressBar(_progressBar, q=True, isCancelled=True):
            break
        if _progressBar:
            mc.progressBar(_progressBar, e=True, status='Doing X: {0}'.format(mObj.p_nameShort), step=1)
            mc.refresh()
        # ... work ...
finally:
    if _progressBar:
        CGMUI.doEndMayaProgressBar(_progressBar)
```

1. Start/end in `try` / `finally` so the bar always clears, including on errors.
2. `stepMaxValue` ~ user-visible steps (joints, frame batches, chains, files), matching perceived wait.
3. `status` = action name + current item short name, not "Please wait".
4. `mc.refresh()` (or equivalent) inside long loops so the bar repaints.
5. `interruptableState=True` when aborting mid-loop is safe; on cancel, clean up temp nodes/constraints and return
   without claiming success.

## When a bar is required

- Timeline bake (more than a few frames, or many targets); Bake Input / Bake Targets and similar sim-chain exports
- Multi-object export / prep pipelines
- Rebuild / reconnect passes over many chains or joints
- Any new feature where you'd add a `log.info` at start and artists might think Maya froze

Exception: truly instant ops (single attr set, one select, a toggle). Include progress in the same change as the
feature, not as a follow-up after "Maya hung" reports.

## Reference implementations

- cgmDynSimTool Bake Input: `chain_bake_input_from_targets` in `cgm/core/rig/dynamic_utils.py`. Progress steps go
  before/after a single `bake_nodes` / `mc.bakeResults` call; never per-frame `bakeResults` / `setKeyframe` loops for bar feedback.
- cgmDynSimTool load / Details rebuild: `uiFunc_update_details(..., with_progress=True)` in `dynFKTool.py`
  (autoload, load selected); per-chain steps; not on header refresh-only paths.
- MRS / puppet: `cgmUI.doStartMayaProgressBar` in `mrs/lib/puppet_utils.py`, `block_utils.py`.
- cgmGeneral: `autoProgressBar` on multi-step callables when appropriate.

See [`Feature_CgmToolUI.md`](../../Features/Feature_CgmToolUI.md) and
[`Feature_DynSimTool.md`](../../Features/Feature_DynSimTool.md).
