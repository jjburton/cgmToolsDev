# Branch: Jan2026

## 📋 Quick Info
**Status**: Active  
**Created**: January 16, 2026  
**Last Updated**: February 23, 2026  
**PR**: Pending

## 🎯 Goals
Improve ribbon IK attachment configuration and face handle creation flexibility: 1) Add configurable ribbon attachment ends to influences (start/end/both/none), 2) Add flexible parent parameter to face handle creation functions, 3) Pass mStateNull through muzzle block handle creation, 4) Add debug logging for mesh creation operations, 5) Add dynParentModeEnabled option to disable dynParent setup on handle blocks, and 6) Add skeletonMode support to Segment and Head blocks for skeleton parenting control (chain/floating).

## 📚 Related Documentation
- **[brow.py](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/organic/brow.py)** - Brow block with ribbon IK setup
- **[segment.py](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/organic/segment.py)** - Segment block with ribbon configuration and skeleton mode
- **[head.py](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/organic/head.py)** - Head block with skeleton mode
- **[muzzle.py](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/organic/muzzle.py)** - Muzzle block handle creation
- **[blockShapes_utils.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/blockShapes_utils.py)** - Face handle creation utilities
- **[handle.py](../../../repos/cgmToolsPy3/cgm/core/mrs/blocks/simple/handle.py)** - Handle block mesh creation and dynParent setup
- **[shared_dat.py](../../../repos/cgmToolsPy3/cgm/core/mrs/lib/shared_dat.py)** - Shared MRS block attributes
- **[Scene.py](../../../repos/cgmToolsPy3/cgm/core/mrs/Scene.py)** - Scene UI, Export Queue

## 🗓️ Timeline

### January 16, 2026 - Ribbon Attachment and Handle Improvements
**What**: Added configurable ribbon attachment ends and improved face handle creation flexibility  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/organic/brow.py` - Added ribbonAttachEndsToInfluence attribute and configuration
- EXTENDED: `cgm/core/mrs/blocks/organic/segment.py` - Added ribbonAttachEndsToInfluence to standard attributes
- EXTENDED: `cgm/core/mrs/blocks/organic/muzzle.py` - Added mStateNull parameter to handle creation calls
- EXTENDED: `cgm/core/mrs/blocks/simple/handle.py` - Added debug logging for mesh operations
- EXTENDED: `cgm/core/mrs/lib/blockShapes_utils.py` - Added mParent parameter to handle creation functions
- EXTENDED: `cgm/core/mrs/lib/shared_dat.py` - Added ribbonAttachEndsToInfluence to shared attributes

**Features**:
- Configurable ribbon attachment ends (start/end/both/none) for brow and segment blocks
- Flexible parent parameter in face handle creation (falls back to mStateNull)
- Consistent mStateNull passing through muzzle block handle creation
- Debug logging for nurbs-to-mesh conversion and mesh coloring operations

**Decisions**:
- Moved ribbonAttachEndsToInfluence to shared_dat.py for consistency across blocks
- Made mParent parameter optional with mStateNull as fallback for backward compatibility
- Used conditional logic in brow.py to set attachStartToInfluence/attachEndToInfluence based on enum value

**Status**: ✅ Complete

---

### January 17, 2026 - DynParent Mode Enabled Option and Skeleton Mode Support
**What**: Added dynParentModeEnabled attribute to allow disabling dynParent setup on handle blocks, and added skeletonMode support to Segment and Head blocks for skeleton parenting control  
**Files**:
- EXTENDED: `cgm/core/mrs/blocks/simple/handle.py` - Added dynParentModeEnabled attribute, conditional dynParent setup, and precheck validation
- EXTENDED: `cgm/core/mrs/blocks/organic/segment.py` - Added skeletonMode attribute and floating skeleton parent logic
- EXTENDED: `cgm/core/mrs/blocks/organic/head.py` - Added skeletonMode attribute and floating skeleton parent logic
- EXTENDED: `cgm/core/mrs/lib/shared_dat.py` - Added dynParentModeEnabled to space attributes and skeletonMode enum definition

**Features**:
- Boolean attribute `dynParentModeEnabled` (default: True) to control dynParent setup
- When False, skips entire dynParent group setup in rig_cleanUp
- Precheck validation requires parentToDriver to be True when dynParentModeEnabled is False
- Conditional dynParentGroup creation when registering root control
- `skeletonMode` enum attribute ('chain' or 'floating') for Segment and Head blocks
- When 'floating', all skeleton joints after the first are parented to the first joint's parent (sibling structure)
- When 'chain' (default), normal chain parenting occurs

**Decisions**:
- Default value for dynParentModeEnabled is True to maintain backward compatibility
- Precheck ensures parentToDriver is enabled when dynParent is disabled to maintain proper hierarchy
- Wrapped entire dynParent setup section in conditional check for clean code flow
- skeletonMode defaults to 'chain' to maintain existing behavior
- Floating mode useful for independent joint control without chain hierarchy

**Status**: ✅ Complete

---

### February 23, 2026 - Export Queue UI Improvements
**What**: Replaced Export Queue text buttons with icons, improved layout spacing, hid category from list display, and added double-click to select file in top section  
**Files**:
- EXTENDED: `cgm/core/mrs/Scene.py` - Export Queue UI and queue list behavior

**Features**:
- Replaced Save, Load, Update, Report, Sort text buttons with icon buttons (file_save, file_open, refresh, report, sortBy_name)
- Kept original labels as tooltips
- Matched icon row layout to Add to queue section (MelHSingleStretchLayout, h=40, stretch widget)
- Added leading spacer on icon row; restored spacing between Remove and Remove All
- Hid category from queue list display (data unchanged)
- Double-click queue entry navigates top section to select that file (like Select Open File)

**Decisions**:
- Used create_exportButton with optional w/h params for consistent icon sizing
- rowSpacing=0 on column to minimize gap; add_LineSubBreak for separator
- ExportQueue_selectEntryInUI mirrors uiFunc_selectOpenFile navigation flow

**Status**: ✅ Complete

---

## 📦 Deliverables

### Ribbon Attachment Configuration
- [x] Add ribbonAttachEndsToInfluence attribute to brow block
- [x] Add ribbonAttachEndsToInfluence attribute to segment block
- [x] Move attribute definition to shared_dat.py for consistency
- [x] Update brow ribbon IK setup to use configurable attachment
- [x] Support start/end/both/none attachment options

### Face Handle Creation Improvements
- [x] Add mParent parameter to create_face_handle function
- [x] Add mParent parameter to create_face_anchorHandleCombo function
- [x] Maintain backward compatibility with mStateNull fallback
- [x] Update muzzle block to pass mStateNull through handle creation

### Debug Logging
- [x] Add debug logging for nurbs-to-mesh conversion
- [x] Add debug logging for mesh coloring operations

### DynParent Mode Enabled
- [x] Add dynParentModeEnabled attribute to handle block
- [x] Add to shared_dat.py space attributes
- [x] Add conditional check in rig_cleanUp to skip dynParent setup when disabled
- [x] Add precheck validation for parentToDriver requirement
- [x] Update root registration to conditionally create dynParentGroup

### Skeleton Mode Support
- [x] Add skeletonMode attribute to Segment block
- [x] Add skeletonMode attribute to Head block
- [x] Add skeletonMode enum definition to shared_dat.py ('chain:floating')
- [x] Implement floating skeleton parent logic (all joints parented to first joint's parent)
- [x] Maintain chain mode as default for backward compatibility

### Testing
- [ ] Code implementation complete
- [ ] No linter errors
- [ ] Test ribbon attachment with different configurations
- [ ] Test face handle creation with custom parent
- [ ] Verify backward compatibility

---

## 🚀 PR Notes

```markdown
# Ribbon Attachment Configuration and Handle Creation Improvements

## Overview
This PR adds configurable ribbon attachment ends to influences, improves face handle creation flexibility with optional parent parameters, adds debug logging for mesh creation operations, adds dynParentModeEnabled option to disable dynParent setup on handle blocks, and adds skeletonMode support to Segment and Head blocks for skeleton parenting control.

## Major Features

### 1. Configurable Ribbon Attachment Ends ✨
Adds `ribbonAttachEndsToInfluence` attribute to brow and segment blocks, allowing users to configure which ends of ribbon IK chains attach to influences (start, end, both, or none).

**Files Modified:**
- `cgm/core/mrs/blocks/organic/brow.py` - Added attribute, enum options, and conditional attachment logic
- `cgm/core/mrs/blocks/organic/segment.py` - Added to standard attributes list
- `cgm/core/mrs/lib/shared_dat.py` - Added to shared attributes dictionary

**Configuration:**
- `ribbonAttachEndsToInfluence`: Enum option in brow/segment blocks (default: 'start' for brow)
- Options: 'none', 'start', 'end', 'both'
- Controls `attachStartToInfluence` and `attachEndToInfluence` parameters in ribbon IK setup

**Implementation Details:**
- Brow block: Conditional logic sets attachment flags based on enum value
- Segment block: Attribute added to standard attributes for consistency
- Shared definition in shared_dat.py ensures consistent behavior across blocks

### 2. Face Handle Parent Parameter 🎛️
Adds optional `mParent` parameter to face handle creation functions, allowing custom parent assignment while maintaining backward compatibility.

**Files Modified:**
- `cgm/core/mrs/lib/blockShapes_utils.py` - Added mParent parameter to create_face_handle and create_face_anchorHandleCombo
- `cgm/core/mrs/blocks/organic/muzzle.py` - Updated handle creation calls to pass mStateNull

**Configuration:**
- `mParent`: Optional parameter in handle creation functions
- Falls back to `mStateNull` if not provided (backward compatible)
- Allows custom parent assignment for handles and anchors

**Implementation Details:**
- create_face_handle: Added mParent parameter with mStateNull fallback
- create_face_anchorHandleCombo: Added mParent parameter, reordered parameters for clarity
- Muzzle block: All handle creation calls now explicitly pass mStateNull

### 3. Debug Logging 📝
Adds debug logging for mesh creation operations to aid in troubleshooting.

**Files Modified:**
- `cgm/core/mrs/blocks/simple/handle.py` - Added debug logs for nurbs-to-mesh conversion and mesh coloring

**Implementation Details:**
- Logs when creating mesh from nurbs geometry
- Logs when coloring mesh operations occur
- Helps track mesh creation pipeline

### 4. DynParent Mode Enabled Option 🔧
Adds `dynParentModeEnabled` boolean attribute to handle blocks, allowing users to disable dynParent setup entirely.

**Files Modified:**
- `cgm/core/mrs/blocks/simple/handle.py` - Added attribute, conditional dynParent setup, and precheck validation
- `cgm/core/mrs/lib/shared_dat.py` - Added to space attributes and attribute definitions

**Configuration:**
- `dynParentModeEnabled`: Boolean attribute in handle blocks (default: `True`)
- When `False`, skips entire dynParent group setup in rig_cleanUp
- When `False`, requires `parentToDriver` to be `True` (enforced by precheck)

**Implementation Details:**
- Wraps entire dynParent setup section (lines 2069-2114) in conditional check
- Precheck validates that parentToDriver is enabled when dynParent is disabled
- Root registration conditionally creates dynParentGroup based on attribute value
- Default value of True maintains backward compatibility

### 5. Skeleton Mode Support 🦴
Adds `skeletonMode` enum attribute to Segment and Head blocks, allowing control over skeleton joint parenting structure.

**Files Modified:**
- `cgm/core/mrs/blocks/organic/segment.py` - Added skeletonMode attribute and floating parent logic
- `cgm/core/mrs/blocks/organic/head.py` - Added skeletonMode attribute and floating parent logic
- `cgm/core/mrs/lib/shared_dat.py` - Added skeletonMode enum definition

**Configuration:**
- `skeletonMode`: Enum attribute in Segment and Head blocks (default: `'chain'`)
- Options: `'chain'` (default) or `'floating'`
- Controls how skeleton joints are parented during skeleton build

**Implementation Details:**
- When `'chain'`: Normal chain parenting (each joint parents to previous)
- When `'floating'`: All joints after the first are parented to the first joint's parent (creates sibling structure)
- Applied after `skeleton_connectToParent` call in skeleton_build functions
- Floating mode useful for independent joint control without chain hierarchy constraints

## Technical Details

### Ribbon Attachment Implementation
```python
# Brow block - conditional attachment based on enum
if self.str_ribbonAttachEndsToInfluence == 'both':
    d_ik['attachEndsToInfluences'] = True
elif self.str_ribbonAttachEndsToInfluence == 'start':
    d_ik['attachStartToInfluence'] = True
elif self.str_ribbonAttachEndsToInfluence == 'end':
    d_ik['attachEndToInfluence'] = True
```

### Face Handle Parent Implementation
```python
# blockShapes_utils.py - flexible parent with fallback
if mParent is None:
    mParent = mStateNull
mHandle.p_parent = mParent
```

### DynParent Mode Enabled Implementation
```python
# handle.py - conditional dynParent setup
if self.mBlock.dynParentModeEnabled:
    # ... entire dynParent setup code ...
    mDynGroup = mHandle.getMessageAsMeta('dynParentGroup')
    if mDynGroup:
        # ... configure and rebuild dynParent group ...

# Precheck validation
if not mBlock.dynParentModeEnabled and not mBlock.parentToDriver:
    self.l_precheckErrors.append("If dynParentModeEnabled is False, parentToDriver must be True")
```

### Skeleton Mode Implementation
```python
# segment.py / head.py - floating skeleton parent logic
self.atBlockUtils('skeleton_connectToParent')
for mJnt in ml_joints:
    mJnt.rotateOrder = 5

if self.skeletonMode == 'floating':
    for mJnt in ml_joints[1:]:
        mJnt.p_parent = ml_joints[0].p_parent
```

## Architecture Decisions

1. **Shared attribute definition**: Rationale - ribbonAttachEndsToInfluence is used by multiple block types, so defining it in shared_dat.py ensures consistency and reduces duplication
2. **Optional parent parameter**: Rationale - Making mParent optional with mStateNull fallback maintains backward compatibility while allowing custom parent assignment when needed
3. **Conditional attachment logic**: Rationale - Using if/elif structure in brow block allows explicit control over attachment flags rather than mapping enum directly
4. **DynParent mode enabled default**: Rationale - Defaulting dynParentModeEnabled to True maintains backward compatibility while allowing users to opt out of dynParent setup when not needed
5. **Precheck validation**: Rationale - Requiring parentToDriver when dynParent is disabled ensures proper hierarchy and prevents orphaned controls
6. **Skeleton mode default**: Rationale - Defaulting skeletonMode to 'chain' maintains existing skeleton behavior while allowing floating mode for special cases
7. **Floating skeleton structure**: Rationale - Floating mode creates sibling joints instead of chain, useful for independent control without chain hierarchy constraints

## Testing

### Ribbon Attachment
- ⏳ Test brow block with 'start' attachment (default)
- ⏳ Test brow block with 'end' attachment
- ⏳ Test brow block with 'both' attachment
- ⏳ Test segment block with various attachment options
- ⏳ Verify ribbon IK chains attach correctly based on configuration

### Face Handle Creation
- ⏳ Test handle creation with custom parent
- ⏳ Test handle creation without parent (should use mStateNull)
- ⏳ Verify muzzle block handles use correct parent
- ⏳ Test backward compatibility with existing code

### Debug Logging
- ⏳ Verify debug logs appear during mesh creation
- ⏳ Verify logs don't impact performance

### DynParent Mode Enabled
- ⏳ Test handle block with dynParentModeEnabled = True (default behavior)
- ⏳ Test handle block with dynParentModeEnabled = False
- ⏳ Verify precheck catches missing parentToDriver when dynParent is disabled
- ⏳ Verify no dynParent groups created when disabled
- ⏳ Verify backward compatibility (default True)

### Skeleton Mode
- ⏳ Test Segment block with skeletonMode = 'chain' (default behavior)
- ⏳ Test Segment block with skeletonMode = 'floating'
- ⏳ Test Head block with skeletonMode = 'chain' (default behavior)
- ⏳ Test Head block with skeletonMode = 'floating'
- ⏳ Verify floating mode creates sibling joint structure
- ⏳ Verify chain mode maintains existing behavior

## Configuration Assets

N/A

## Documentation Updated
- TBD

## Breaking Changes
None - All changes maintain backward compatibility

## Next Steps
- Test ribbon attachment configurations in various scenarios
- Consider adding ribbon attachment options to other block types if needed
- Review debug logging output for optimization opportunities
- Test dynParentModeEnabled in various handle block configurations
- Consider if other block types could benefit from similar dynParent disable option
- Test skeletonMode in various Segment and Head block configurations
- Verify floating skeleton mode works correctly with rigging systems

---

**Ready for Review** - Implementation complete, testing pending
```

---

## 📝 Notes

### Architectural Patterns Established
- Shared attribute definitions in shared_dat.py for cross-block consistency
- Optional parameters with sensible defaults for backward compatibility
- Conditional configuration logic based on enum values

### Lessons Learned
- Moving shared attributes to central location improves maintainability
- Optional parameters with fallbacks are better than required parameters for API flexibility

### Future Considerations
- Consider adding ribbon attachment options to other organic blocks if needed
- Review if other handle creation functions could benefit from flexible parent parameter
- Consider adding more granular debug logging options

---

*Last Updated: February 23, 2026*  
*Branch Status: Active*
