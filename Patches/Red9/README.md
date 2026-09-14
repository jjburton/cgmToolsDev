# Red9 local patches

cgm-local edits to vendored `Red9/` in `cgmToolsPy3` are recorded here so they can be reapplied after upstream drops.

## Quick use

From `cgmToolsDev`:

```bash
# Preview
python Patches/Red9/apply_red9_patches.py --dry-run

# Apply to default target (../cgmToolsPy3/Red9)
python Patches/Red9/apply_red9_patches.py

# Custom target
python Patches/Red9/apply_red9_patches.py --target D:/Repos/cgmToolsPy3/Red9

# Single patch
python Patches/Red9/apply_red9_patches.py --id pyperclip-vendored-import
```

## After upstream Red9 sync

1. Copy the new upstream `Red9` tree into `cgmToolsPy3/Red9`.
2. Run `apply_red9_patches.py --dry-run`, then without `--dry-run`.
3. Fix any failed entries (update `manifest.json` if upstream changed context).
4. Smoke-test Maya and batch mayapy.
5. Set `upstream_tested` on each patch entry in `manifest.json`.

## Adding a patch

1. Prefer a **cgm-side workaround** in `cgm/core/` when possible.
2. If Red9 must change, add an entry to `manifest.json` in the same session.
3. See [`Features/Feature_Red9Patches.md`](../../Features/Feature_Red9Patches.md) for the full contract.
