# Debugging Maya tools: stale session first, boundary logs, minimal diffs

Applies to "data not getting through", "option on but behavior off", and any turn where the user pastes Maya
Script Editor output. Reload mechanics live in [`reload.md`](reload.md).

## Order of work

1. **Stale session first.** When behavior doesn't match on-disk py3 code, assume session reload before broken
   wiring.
2. **Log at boundaries** (UI handler -> public API kwargs -> first backend branch; `log.info` with raw + resolved
   values) before adding validation, coercion, or joint/curve logic.
3. **Read kwargs pop order** on the actual code path (e.g. `require*` flags must be popped before the blocks that use them).
4. **One root cause per turn.** Don't stack trim + append + reload + validation fixes without Maya confirmation between them.
5. **Stop condition:** after one code change that doesn't move Maya output, if backend entry logs are still
   absent, stop patching build logic and document session/reload steps only.

## Symptom: UI logs new code, backend doesn't

New `log.info` (or UI-only strings) from the tool module but none from the backend module (e.g. `dynFKTool`
create log present, `dynamic_utils.chain_create_hair` entry log absent):

1. Treat as a stale imported backend and/or cached meta instance (`self._mDynFK` still bound to the pre-reload class).
2. Don't add reload/rebind inside Create Chain, bake, export, or other one-shot callbacks.
3. Artist fix: Setup -> Reload Dependencies, shelf relaunch (`tool_calls.cgmDynSimTool()`), or restart Maya.

Before another feature-fix pass:

1. Did Reload Dependencies run and print per-module reload lines? Ask, or infer from logs.
2. No reload lines: the session may still be on old tool code. Relaunch once from the toolbox.
3. Reload lines present but backend entry logs still missing on the loaded setup: verify the meta rebind on the
   reload path (`dynFKTool._dynfk_rebind_loaded_mDynFK`), not mid-call.
4. `mClass` / subclass edits need core reload (`CGM._reload`), not a partial meta stack. `AttributeError` on
   `mObj.<new_method>` while `SOMEMOD.<fn>(mObj)` works means: prompt core reload + tool rebind
   ([`Feature_CgmMetaAPI.md`](../../Features/Feature_CgmMetaAPI.md)).

## When the user pastes logs

1. Quote what is present vs absent (specific module / function log lines), then state one inference before editing.
2. If UI and backend lines disagree on freshness, the next step is reload verification (per-module reload logs,
   meta rebind), not another feature patch.
3. If the symptom persists after a reload-path fix, ask whether Reload Dependencies ran and which reload lines
   appeared. Don't assume silent failure and rewrite build code again.
4. Prefer a minimal diff (logging + reload-path rebind only) until session freshness is proven.
5. Don't re-explain the same root cause across turns without a new log or user confirmation.

## Do not

- Propose `reload_dependencies()` inside button handlers to "pick up" edited libs.
- Make large behavioral changes when the user only asked for clear logging of passed values.
- Interpret a count without naming which object it counts (sim joints vs follow locs vs inCurve CVs). For hair,
  use the `cgm-dynsim-debug` skill and [`Feature_DynSimTool.md`](../../Features/Feature_DynSimTool.md).
