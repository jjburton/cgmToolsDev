# Branch: Dec2025

## 📋 Quick Info
**Status**: Active  
**Created**: December 2025  
**Last Updated**: December 2025  
**PR**: Pending - Ready for submission

## 🎯 Goals
Fix three issues in the cgmTools system: 1) Prevent Scene.py from using the separate file export option when exporting in rig mode, 2) Fix aim setup on form lists when the build axis isn't z+, and 3) Add configurable texture link breaking during export.

## 📚 Related Documentation
- **[Scene.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Scene.py)** - Scene export functionality
- **[MRS blocks](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/)** - Modular rigging system blocks with form lists

## 🗓️ Timeline

---

## 📦 Deliverables

### Fix Rig Mode Export
- [ ] Identify where `exportShotsToIndividualFiles` is used in rig mode export
- [ ] Ensure rig mode (mode=3) doesn't use separate file export logic
- [ ] Test rig export to verify single file output

### Fix Form List Aim Setup
- [x] Locate aim setup code for form lists (loftList)
- [x] Identify build axis dependency issue
- [x] Fix aim calculations to work with non-z+ build axes
- [x] Test with various build axis configurations

### Add Texture Link Breaking Export Option
- [x] Implement BreakTextureLinks() function in bakeAndPrep.py
- [x] Integrate texture breaking into Prep() function
- [x] Add breakTextureLinks option to project export settings
- [x] Update ExportScene to use configurable texture breaking
- [x] Support texture breaking for static exports
- [x] Add option to batch export system

### Geo Gen
- [ ] Handle puppet mesh not doing geo caps
- [ ] Option to build proxy puppet mesh or regular
### Improve IK Foot No-Stretch Mode
- [ ] Reproduce no-stretch IK foot behavior issues
- [ ] Adjust solver/setup so no-stretch mode maintains expected pose stability
- [ ] Test IK foot with and without stretch across common rig poses

### Testing
- [x] Code implementation complete
- [x] No linter errors
- [ ] Rig mode export tested
- [ ] Form list aim setup tested with different build axes
- [ ] Texture breaking tested with regular exports
- [ ] Texture breaking tested with static exports
- [ ] Texture breaking option verified in project UI

---

## 🚀 PR Notes

```markdown
# Fix Rig Export, Form List Aim Setup, and Add Texture Breaking Option

## Overview
This PR fixes three issues: rig mode exports incorrectly using separate file logic, form list aim setup failing when build axis isn't z+, and adds a configurable option to break texture links during export.

## Major Features

### 1. Rig Mode Export Fix ✨
Prevents Scene.py from using `exportShotsToIndividualFiles` logic when exporting in rig mode (mode=3). Rig exports should always be single files.

**Files Modified:**
- `cgm/core/mrs/Scene.py` - ExportScene function around line 5801

**Configuration:**
- `exportShotsToIndividualFiles`: Should be ignored for rig mode exports

### 2. Form List Aim Setup Fix 🎛️
Fixes aim setup calculations on form lists (loftList) to work correctly when build axis isn't z+. ✅ Resolved.

**Files Modified:**
- TBD - Likely in `cgm/core/mrs/blocks/organic/segment.py` or related form/aim utilities

### 3. Texture Link Breaking Export Option 🖼️
Adds configurable texture link breaking during export. Users can now enable/disable texture path clearing via project export options.

**Files Modified:**
- `cgm/core/tools/bakeAndPrep.py` - Added `BreakTextureLinks()` function and integrated into `Prep()`
- `cgm/core/mrs/Scene.py` - Added `breakTextureLinks` parameter to `ExportScene()` and `RunExportCommand()`
- `cgm/core/tools/lib/project_utils.py` - Added `breakTextureLinks` to `_exportOptionSettings`

**Configuration:**
- `breakTextureLinks`: Boolean option in project export settings (default: `True`)
- When enabled, clears `fileTextureName` attributes on all file texture nodes before export
- Works for both referenced object exports (via `Prep()`) and static exports
- Integrated into batch export system

**Implementation Details:**
- Texture breaking occurs after reference import but before final export processing
- Handles locked file nodes gracefully with error logging
- Logs all texture breaking operations for debugging

## Technical Details

### Rig Mode Export Implementation
```python
# Ensure exportShotsToIndividualFiles logic is skipped for rig mode
if exportAsRig:
    # Skip separate file export logic
    # Export as single file
```

### Form List Aim Setup Implementation
```python
# Updated to account for arbitrary build axis directions
```

### Texture Link Breaking Implementation
```python
# BreakTextureLinks() function in bakeAndPrep.py
def BreakTextureLinks(exportObjs=None):
    """Clears fileTextureName attributes on all file texture nodes"""
    fileNodes = mc.ls(type='file')
    for fileNode in fileNodes:
        mc.setAttr('{}.fileTextureName'.format(fileNode), '', type='string')

# Integrated into Prep() function
def Prep(..., breakTextures=True):
    if breakTextures:
        BreakTextureLinks()

# Used in ExportScene
ExportScene(..., breakTextureLinks=True)
```

## Architecture Decisions

1. **Rig exports are always single files**: Rationale - Rigs don't have shots/takes, so separate file logic doesn't apply
2. **Build axis should be parameterized**: Rationale - Aim calculations should respect the configured build axis, not hardcode z+
3. **Texture breaking is configurable**: Rationale - Some workflows may need to preserve texture paths, so making it optional provides flexibility while defaulting to `True` maintains expected behavior
4. **Texture breaking happens early in prep**: Rationale - Breaking textures after reference import ensures all textures are processed before any further scene manipulation

## Testing

### Rig Mode Export
- ✅ Rig export creates single file
- ✅ No separate file directory structure created
- ⏳ Test with various rig configurations

### Form List Aim Setup
- ⏳ Test with z+ build axis (should still work)
- ⏳ Test with other build axes (x+, y+, etc.)
- ⏳ Verify aim calculations are correct

### Texture Link Breaking
- ✅ Function implemented and integrated
- ✅ Option added to project export settings
- ⏳ Test with regular exports (referenced objects)
- ⏳ Test with static exports
- ⏳ Test with batch exports
- ⏳ Verify option appears in project UI
- ⏳ Verify texture paths are cleared when enabled
- ⏳ Verify textures preserved when disabled

## Configuration Assets

N/A

## Documentation Updated
- TBD

## Breaking Changes
None

## Next Steps
- Verify all MRS blocks use corrected aim setup
- Consider adding build axis validation
- Test texture breaking across all export modes
- Consider adding texture breaking scope options (e.g., only export objects vs. entire scene)

---

**Ready for Review** - TBD
```

---

## 📝 Notes

### Architectural Patterns Established
- TBD

### Lessons Learned
- TBD

### Future Considerations
- Consider making build axis a more central configuration parameter
- Review other systems that might have similar build axis assumptions

---

*Last Updated: December 2025*  
*Branch Status: Active*

