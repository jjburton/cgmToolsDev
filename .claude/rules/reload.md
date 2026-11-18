# Module reload

Applies to cgmToolsPy3, ProjectScripts, cgmToolsDev docs, and any other in-house Maya Python, including code,
comments, docs, and Script Editor snippets you hand the user.

## Only `cgmGEN._reloadMod`

Reload with `cgmGEN._reloadMod(module)` after `import cgm.core.cgm_General as cgmGEN` (match the file's import
style). It is the project wrapper (`importlib.reload` on py3, `reload()` on py2). Never call lower-level reload
APIs directly, not even "just this once".

1. `import` the target module with its full dotted path and a normal alias (`import cgm.core.tools.dynFKTool as DYNFKTOOL`).
2. Pass that module object to `cgmGEN._reloadMod(...)`.
3. Rebind callers if needed (`global RIGDYN = RIGDYNMOD`; `self.__class__ = DYNFKTOOL.ui` after reloading the tool module).

```python
import cgm.core.cgm_General as cgmGEN
import cgm.core.rig.dynamic_utils as RIGDYN
import cgm.core.tools.dynFKTool as DYNFKTOOL

cgmGEN._reloadMod(RIGDYN)      # after its lib deps were reloaded
cgmGEN._reloadMod(DYNFKTOOL)   # tool module last
```

Multi-module tools (e.g. cgmDynSimTool): dependencies first, consumer last (lib -> `ik_utils` -> `dynamic_utils`
last), then the tool module so its imports see fresh libs. Match entry points in
`cgm/core/tools/lib/tool_calls.py` (`reload_dependencies()` -> `cgmGEN._reloadMod(dynFKTool)` -> `dynFKTool.ui()`).

Session cache modules (e.g. `cgm.core.lib.perforce_session`): same `import` + `_reloadMod`, or
`P4UTIL.reload_session_cache()` when it exists.

## Banned

- `importlib.reload(...)`, `importlib.import_module` for session reload
- bare `reload(...)`, `imp.reload(...)`
- `__import__(__name__)` (also when passed to `_reloadMod`): on dotted names Python returns the top-level package
  (e.g. `cgm`), not the tool module, giving `AttributeError` on `.ui`
- `sys.modules[...]` tricks instead of a normal `import full.path as ALIAS` before `_reloadMod`
- telling the user to `importlib.reload` in docs, comments, or Script Editor snippets

## Reloading a tool module from inside that tool

Use the same explicit import + `_reloadMod` as `tool_calls`, not introspection shortcuts.

```python
def _reload_dynfk_ui(self):
    reload_dependencies()
    cgmGEN._reloadMod(DYNFKTOOL)
    self.__class__ = DYNFKTOOL.ui
    _dynfk_rebind_loaded_mDynFK(self, rigdyn_module=DYNFKTOOL.RIGDYN)
    super(DYNFKTOOL.ui, self).reload()
```

RETAIN windows: clear stale Mel widget attrs on `self` before `super(...).reload()` if a layout rebuild can touch
deleted controls (`dynFKTool._dynfk_clear_stale_layout_widget_refs`).

## Meta / `mClass`: no partial reload

Registered `mClass` subclasses (`cgmDynFK`, blocks, puppets, ...) depend on Red9's registry and
`registerMClassInheritanceMapping()` running in `cgm.core._reload` order (`_l_core_order` in `cgm/core/__init__.py`).
Never build a "mini" Red9 -> `cgm_Meta` -> `cgm_RigMeta` stack inside a tool's `reload_dependencies()`; it breaks
other metaclasses still bound to the previous registry.

| After editing... | In Maya |
|------------------|---------|
| `lib/` / `rig/` module functions, presets, tool UI (no `mClass` class body change) | Tool Reload Dependencies + rebind meta (`_dynfk_rebind_loaded_mDynFK`, etc.) |
| `cgm_Meta`, `cgm_RigMeta`, `mrs/` / `rig/` subclass class defs, `registerMClassInheritanceMapping` tails | Tell the user to run the full core reload: `import cgm.core as CGM; CGM._reload()` (or team toolbox equivalent), then relaunch tools / rebind handles |

If you changed metaclass code, tell the user to core-reload before expecting new subclass behavior. New subclass
instance methods need explicit user approval ([`meta-runtime.md`](meta-runtime.md)).

## Rebind loaded meta after backend reload

`_reloadMod` updates module-level functions only. Existing meta handles stay on the old Python class (Red9 cache)
until re-wrapped. On the Reload Dependencies path only (not Create Chain / bake): rebind the loaded setup
(`dynFKTool._dynfk_rebind_loaded_mDynFK` = `cgmMeta.reinitializeMetaClass` + fresh `RIGDYN.cgmDynFK(node)`); the
same applies to any RETAIN tool holding a meta handle into a reloaded backend module. After `mClass` class edits,
the user core-reloads first, then tool reload + rebind. The header "refresh" (re-read scene) is only
`reinitializeMetaClass` + re-wrap; it does not load new Python from disk.

## Log each module on multi-module reloads

Log before every `cgmGEN._reloadMod`: a start line, one line per `module.__name__`, then a done line +
`cgmGEN._str_subLine`. Match `cgm.core._reload`, `Scene.reloadSceneStuff`, `dynFKTool.reload_dependencies`.
Without per-module lines neither artists nor agents can tell whether Reload Dependencies ran or which revision loaded.

## Never reload inside action callbacks

Never call `reload_dependencies()`, `cgmGEN._reloadMod(...)`, or rebind loaded meta (re-wrap `self._mDynFK` from a
fresh module) from Create Chain, bake, export, or any one-shot UI button handler. If Maya runs old backend code
while the UI looks updated, that is a session reload problem: Setup -> Reload Dependencies, shelf/menu relaunch,
or restart Maya. Don't patch stale code by reloading mid-call. Diagnosis: [`debugging.md`](debugging.md).
