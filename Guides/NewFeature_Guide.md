# New Feature Documentation Guide

## Purpose
Feature documents provide a complete record of how a system works: goals, scope, architecture, configuration, testing, and future considerations. They should be the single source of truth for a feature’s design and implementation details, supplementing day-to-day branch docs.

## When to Create a Feature Doc
Create a feature doc when:
- The work spans multiple branches or substantial refactors
- The feature introduces new architecture, configuration, or testing patterns
- The system will be referenced by multiple teams/branches

Skip standalone docs for:
- Small tweaks contained within an existing feature
- One-off bug fixes already covered by a plan doc

## File Naming
`Feature_Name.md`

Examples:
- `Feature_LookAnimator.md`
- `Feature_TailAnimator.md`
- `Feature_TrackingDebugUI.md`

Place the file under `Docs/CursorRef/Features/`.

## Template
Use this template to start a new feature doc, then tailor sections based on the system’s needs.

```markdown
# Feature: [Name]

## 🎯 Status & Overview
- **Status**: Planning / In Progress / Code Complete / Shipped
- **Last Updated**: [Date]
- **Owners**: [Who maintains/tests]
- **Purpose**: [One paragraph summary of why the feature exists]

## 📋 Scope
- **In Scope**:
  - Item 1
  - Item 2
- **Out of Scope**:
  - Item A
  - Item B

## 🧩 Architecture
### Core Concepts
- Concept/Component descriptions

### Data / Configuration
- ScriptableObjects, JSON, or other data sources
- Runtime toggles, inspector fields, debug fences

### State Diagram / Flow (if applicable)
- Text description of flow
- Optionally embed diagram (link or markdown image)

## ⚙️ Implementation Details
### Files & Responsibilities
| File | Responsibility |
|------|----------------|
| `File1.cs` | Description |
| `File2.cs` | Description |

### Key Methods / APIs
- `MethodA()` – what it does, key parameters, return values, exceptions
- `EventB` – who fires it, who listens

### Initialization / Lifecycle
- When the feature initializes, tears down, or responds to Unity events

## 🔧 Configuration Guide
### Inspector Setup
- Required components, serialized fields, recommended defaults

### ScriptableObject Fields
- Field list with descriptions, validations, ranges

### Runtime Controls / Debug UI
- Debug toggles, console commands, dashboard panels

## ✅ Testing & Validation
- Unit / EditMode tests
- Playmode scenarios
- Manual test checklist
- Performance considerations

## 🧱 Dependencies & Integration
- Other systems/features touched by this work
- Known interactions or conflicts
- Feature flags/guard rails

## 📚 Related Documentation
- **[Branch_BranchName.md](../Branches/Branch_BranchName.md)** – development timeline
- **[Plan_System.md](../Plans/Plan_System.md)** – high-level design plan
- **[DebugDoc.md](../Debug/DebugDoc.md)** – runtime tuning reference

## 🚀 Future Work / Ideas
- Follow-on tasks, refactors, or enhancements
- Known limitations or tech debt

## 📝 Revision History
| Date | Author | Summary |
|------|--------|---------|
| 2025-11-07 | Alice | Initial draft |
| YYYY-MM-DD | Name | Major update |
```

## How to Maintain Feature Docs
1. **Create early**: Start during planning so architecture decisions are documented as they happen
2. **Update per milestone**: After each major branch merge or code milestone
3. **Link from branch docs**: Cross-reference the feature doc in every related branch doc’s “Related Documentation” section
4. **Keep PR notes separate**: Feature docs explain “why/how”; branch docs capture implementation timeline and PR copy

## Best Practices
- Keep content system-focused (avoid branch-specific minutiae)
- Include diagrams/figures when they clarify flows or architecture
- Note assumptions, constraints, and non-goals explicitly
- Use tables for config settings and responsibilities
- Update testing section with real test cases and expected results

## Formatting Checklist
- Status line kept up to date
- Scope clearly defined (avoid scope creep)
- Architecture sections explain both high-level principles and specific components
- Configuration instructions include inspector screenshots or field descriptions when necessary
- Testing includes manual test plan + automated coverage when available
- Future work clearly delineated from current scope
- Revision history table updated whenever substantial edits occur

## Ready-Made Process
1. **Create doc** using template above in `Docs/CursorRef/Features/`
2. **Link doc** in `Plan_Cursor.md` quick reference under appropriate category
3. **Reference doc** in all related branch docs and PR notes
4. **Update doc** post-merge to reflect final status and follow-up items

Maintaining feature docs this way keeps the team aligned, makes onboarding easier, and ensures future work references an accurate, centralized source of truth.

