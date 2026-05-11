# New Testing Guide Documentation Template

## Purpose
Testing guides document validation steps for a system or feature once implementation is code-complete. They provide repeatable checklists, expected results, and troubleshooting tips so anyone on the team can confirm functionality without diving into the code. Use this guide to create consistent testing docs alongside feature and branch documentation.

## When to Create a Testing Guide
Create (or update) a testing guide when:
- Delivering a new feature that requires structured validation (keep feature docs focused on architecture)
- Refactoring a system where regression risk is high
- Establishing reusable test plans that other branches will reference
- Preparing for release milestones or QA hand-off

**Skip standalone testing docs for:**
- Single script bug fixes verified during development
- Temporary experiments or throwaway prototypes
- Unit tests that are already covered inside the codebase with comments

## File Naming and Location
- Create a **new Markdown file** for each guide under `Docs/CursorRef/Testing/` (do not append to this reference document)
- Use the format `Feature_SystemPhase_Testing_Guide.md`
  - Examples: `LaserPointer_Testing_Guide.md`, `ModularDebugUI_Testing_Guide.md`
- Use underscores between words; capitalize each segment

## Reference Before Writing
According to @Plan_Cursor.md, testing documentation should align with existing plans and feature docs:
- Review the relevant feature doc (for example, `Feature_LaserInteraction.md`)
- Check any interaction plans (for example, `Plan_Equipment.md`) or tracking plans if states are involved
- Cross-reference prior testing guides (for example, `LaserPointer_Testing_Guide.md`, `DebugItemSpawner_Testing_Guide.md`) for tone and depth

## Template

**Formatting Criticals:**
- Use HTML entities for angle brackets in regular text: Func&lt;string&gt;, spell out comparisons (less than 1ms)
- Angle brackets are fine inside code blocks
- Do not wrap attributes or directives in backticks in the timeline/checklist sections
- Use `[ ]` and `[x]` checkboxes for step tracking
- Keep emoji status markers consistent (✅ Ready, 🚧 In Progress, ⏳ Pending)

```markdown
# [Feature/System Name] - Testing Guide

## 📋 Status
**Implementation**: Code Complete / In Progress / Pending  
**Unity Configuration**: ✅ / 🚧 / ⏳  
**Last Updated**: [Date]

## Overview
One or two paragraphs describing the system under test, why the guide exists, and any high-level context. Link to feature docs with standard markdown links.

**Key Features to Validate:**
- Point-form list of the most critical behaviors under test
- Keep each bullet to a single line
- Call out integration touchpoints (FamiliarEvents, PlayerInteractionController, etc.)

## Testing Prerequisites

### Required Code ✅
- ✅ `FileA.cs` - brief description
- ✅ `FileB.cs` - brief description

### Required Prefabs / Assets ⏳
- ⏳ `PrefabName` - why it matters

### Unity Configuration ⏳
- ⏳ Scene/GameObject setup requirements

## Testing Checklist

### 1. [Phase Title] ✅/🚧/⏳
**Preparation:**
- [ ] Step-by-step setup actions

**Validation:**
- [ ] Observable behavior
- [ ] Console output expectations
- [ ] Event firing confirmation

Repeat numbered sections for each functional area. Keep headings descriptive (for example, "Raycast Validation", "Event Subscription Cleanup", "Desktop vs VR Input").

## Detailed Testing Steps

### Step 1: [Concise Title]
1. **Action**: Detailed instruction. Use bold labels and colon pattern.
2. **Observe**: Describe expected results.
3. **Validate**: Reference the specific UI, console, or inspector feedback.

Break the testing flow into digestible step groups. Include screenshots references if available (link with markdown).

## Expected Results

### Console Output
    [System/Class] Log message example

### UI / Visual Behavior
- Summaries of what testers should see (panels, gizmos, in-game visuals)

### State or Event Outcomes
- Notable events or state transitions that confirm success

## Common Issues and Solutions
- **Issue**: Symptom description  
  **Cause**: Likely root cause  
  **Fix**: Steps to resolve

Repeat for each known pitfall. Keep answers actionable and fail-fast aligned (no silent fallbacks).

## Success Criteria
- ✅ Bullet checklist summarizing pass/fail gates
- Group items if helpful (Configuration, Runtime, Integration, Error Handling)

## Quick Smoke Test (Optional)
- Short sequence (5-8 steps) for rapid regression checks after minor changes

## Related Documentation
- **Feature Doc**: `Docs/CursorRef/Features/Feature_Name.md`
- **Branch Doc**: `Docs/CursorRef/Branches/Branch_Name.md`
- **Plan Doc**: `Docs/CursorRef/Interaction/Plan_Equipment.md`

---

*Last Updated: [Date]*  
*Status: Ready for Unity Testing / Draft / Archived*
```

## Maintaining Testing Guides
1. Update the status section after every major validation pass.
2. Append new failure modes or solutions as they are discovered.
3. Sync deliverable checklists with related branch docs (mark tasks completed in both places).
4. Reflect Unity configuration changes immediately to keep onboarding smooth.
5. When a system ships, mark the guide as Ready for Unity Testing (or Archived if superseded).

## Best Practices
- ✅ Keep steps explicit; avoid assuming editor knowledge
- ✅ Call out required inspector values rather than overriding them in code
- ✅ Include both XR and flat-screen workflows when applicable
- ✅ Reference FamiliarEvents, state machine transitions, and fail-fast expectations
- ✅ Use consistent emoji status markers and checkbox formatting across sections

## Formatting Reminders
- Func&lt;string&gt;, IList&lt;T&gt; for generics in text
- Spell out comparisons (less than 2ms) to avoid markdown parsing issues
- Attributes: [RequireComponent] not `[RequireComponent]`
- Directives: #if UNITY_EDITOR not `#if UNITY_EDITOR`
- Use 4-space indented code blocks when embedding samples inside templates

## Example References
- `Docs/CursorRef/Testing/LaserPointer_Testing_Guide.md` – Isolation-first equipment testing
- `Docs/CursorRef/Testing/DebugItemSpawner_Testing_Guide.md` – Complex checklist structure
- `Docs/CursorRef/Testing/LaserChasePlay_Phase2_Testing_Guide.md` – Multi-phase state integration testing

---

*Last Updated: November 7, 2025*  
*Status: Active reference template for testing documentation*

