# Branch Documentation Guide

## Purpose
Branch docs provide lightweight overviews of branch work with day-by-day timeline tracking. They keep feature docs focused on comprehensive implementation details while branch docs track "what we did and when" for PR preparation.

## When to Create a Branch Doc
Create a branch doc when:
- Starting a new feature branch that will take multiple days
- Working on a significant refactor or system change
- Need to track progress across multiple systems/files
- Want to prepare PR notes as you work

**Don't create for**:
- Quick bug fixes (single file, single day)
- Trivial changes (typos, formatting)
- Work that fits in a single commit

## File Naming Convention
`Branch_[BranchName].md`

Examples:
- `Branch_MovementPass.md`
- `Branch_EmotionalStates.md`
- `Branch_FetchPlay.md`

## Template

Copy this template to start a new branch doc.

**CRITICAL FORMATTING NOTES:**
- Use HTML entities for angle brackets in **regular text**: Func&lt;string&gt; not `Func<string>` (angle brackets break markdown)
- Angle brackets are **fine inside code blocks**: use `Func<string>` normally
- Spell out comparisons: "less than 1ms" not "<1ms" (leading `<` breaks markdown)
- No backticks for attributes/directives in timeline entries

```markdown
# Branch: [your-branch-name]

## 📋 Quick Info
**Status**: Active / Ready for Merge / Merged  
**Created**: [Date]  
**Last Updated**: [Date]  
**PR**: [Link when ready / Pending - Ready for submission]

## 🎯 Goals
[2-3 sentence summary of what this branch accomplishes]

## 📚 Related Documentation
- **[Feature_Name.md](../Features/Feature_Name.md)** - [Brief description]
- **[Plan_System.md](../[Category]/Plan_System.md)** - [Brief description]
- **[TrackPlan_Flow.md](../Tracking/TrackPlan_Flow.md)** - [Brief description]

## 🗓️ Timeline

### [Date] - [Brief Title]
**What**: [What was worked on]  
**Files**: 
- NEW: `File1.cs`, `File2.cs`
- EXTENDED: `File3.cs`, `File4.cs`

**Features**:
- Feature 1
- Feature 2
- Feature 3

**Decisions**:
- Decision 1 with rationale
- Decision 2 with rationale

**Status**: ✅ Complete / 🚧 In Progress / ⏳ Pending

---

### [Date] - [Brief Title]
[Repeat for each day/major work session]

---

## 📦 Deliverables

### [Phase/Feature Name]
- [ ] Task 1
- [ ] Task 2
- [x] Completed task

### [Another Phase/Feature]
- [ ] Task 1
- [ ] Task 2

### Testing
- [ ] Code implementation complete
- [ ] No linter errors
- [ ] Documentation updated
- [ ] Unity testing complete

---

## 🚀 PR Notes

**IMPORTANT**: Use HTML entities for angle brackets in regular text: Func&lt;string&gt; not `Func<string>`. Code blocks are fine.

### [PR Title]

#### Overview
[Brief overview of the PR]

#### Major Features

##### 1. [Feature Name] ✨
[Description]

**Files Modified:**
- `File1.cs` - Description
- `File2.cs` - Description

**Configuration:**
- `setting1`: value
- `setting2`: value

##### 2. [Another Feature] 🎛️
[Description]

#### Technical Details

##### [Feature Name] Implementation

Use 4-space indented code blocks for code examples (not triple backticks):

    public class Example
    {
        public void Method()
        {
            // Key code example
        }
    }

#### Architecture Decisions

1. **Decision 1**: Rationale
2. **Decision 2**: Rationale

#### Testing

##### [Feature Name]
- ✅ Test 1 passing
- ✅ Test 2 passing
- ⏳ Test 3 pending

#### Configuration Assets

##### [System Name] Parameters
- `param1`: value
- `param2`: value

#### Documentation Updated
- ✅ `Feature_Name.md` - Updates made
- ✅ `Plan_System.md` - Updates made

#### Breaking Changes
None / [List any breaking changes]

#### Next Steps
- Phase X: [Description]
- Phase Y: [Description]

---

**Ready for Review** - [Brief summary of readiness]

---

## 📝 Notes

### Architectural Patterns Established
- Pattern 1
- Pattern 2

### Lessons Learned
- Lesson 1
- Lesson 2

### Future Considerations
- Consideration 1
- Consideration 2

---

*Last Updated: [Date]*  
*Branch Status: [Active/Ready for Merge/Merged]*
```

## Maintaining the Branch Doc

### Daily Updates
At the end of each work session:
1. Add a new timeline entry with the date
2. List files modified (NEW vs EXTENDED)
3. Note key features implemented
4. Document any architectural decisions
5. Mark status (Complete/In Progress/Pending)
6. Update "Last Updated" date
7. Update deliverables checklist

### When Adding Features
- Add to Timeline with date
- Update Deliverables checklist
- Add to PR Notes section
- Document in Notes if it establishes a pattern

### Before Creating PR
1. Update Status to "Ready for Merge"
- Review PR Notes section (should be copy/paste ready; when sharing in reviews or chat, wrap the entire section inside a ```markdown fenced block for clarity)
- Verify all deliverables are checked/noted
- Update Related Documentation links
- Final "Last Updated" date

### After Merge
1. Update Status to "Merged"
2. Add PR link to Quick Info
3. Archive or delete (team preference)

## Integration with Plan_Cursor.md

When creating a new branch doc:
1. Add it to the "Active Branches" list in `Plan_Cursor.md`
2. Use format: `- **\`Branch_Name.md\`** - [Brief description] ([Status])`

When branch is merged:
1. Remove from "Active Branches" in `Plan_Cursor.md`
2. Optionally add to a "Recent Merges" section

## Best Practices

### DO:
- ✅ Update daily or after significant work
- ✅ Document architectural decisions as you make them
- ✅ Keep timeline entries brief (details go in feature docs)
- ✅ Link to relevant feature/plan docs
- ✅ Make PR notes section copy/paste ready
- ✅ Use status emojis (✅ 🚧 ⏳)
- ✅ Use HTML entities for angle brackets in text (Func&lt;string&gt;)
- ✅ Write out comparisons ("less than 1ms" instead of "<1ms")
- ✅ Use plain text for attributes and directives in timeline sections

### DON'T:
- ❌ Duplicate feature doc content (just reference it)
- ❌ Include implementation details (put in feature docs)
- ❌ Wait until end to write everything
- ❌ Skip documenting decisions (you'll forget why)
- ❌ Forget to update deliverables checklist
- ❌ Use angle brackets in regular text: Func<string> (breaks markdown - use Func&lt;string&gt;)
- ❌ Use `<` or `>` symbols directly in text comparisons (use &lt; and &gt;)

## Markdown Formatting Guidelines

### Avoid These Common Issues

**1. Angle Brackets in Regular Text**
- ❌ BAD: The Func<string> callback handles this (angle brackets in regular text)
- ✅ GOOD: The Func&lt;string&gt; callback handles this (HTML entities)
- ✅ ALSO GOOD: Inside code blocks, `Func<string>` is fine
- WHY: Angle brackets break markdown parsing in regular text, but work fine in code blocks

**2. Comparison Operators**
- ❌ BAD: Performance: <1ms
- ✅ GOOD: Performance: less than 1ms
- WHY: Leading `<` breaks markdown

**3. Attributes and Directives**
- ❌ BAD: `[System.Obsolete]` attribute
- ✅ GOOD: [System.Obsolete] attribute
- ❌ BAD: `#if UNITY_EDITOR` directive
- ✅ GOOD: #if UNITY_EDITOR directive
- WHY: Backticks with brackets/special chars can break rendering

**4. Generic Types - Text vs Code Blocks**
- ❌ BAD: Regular text with angle brackets: The Func<string> method...
- ✅ GOOD: Regular text with HTML entities: The Func&lt;string&gt; method...
- ✅ GOOD: Code blocks with angle brackets: `Func<string>` or in triple-backtick blocks
- WHY: Angle brackets break markdown in regular text but work fine in code blocks

## Timeline Entry Format

Each timeline entry should answer:
- **What**: What was the focus?
- **Files**: What files were touched? (NEW vs EXTENDED)
- **Features**: What features were added?
- **Decisions**: What architectural decisions were made?
- **Status**: Is this work complete?

### Good Timeline Entry Example:
```markdown
### October 17, 2025 - Banking Physics Implementation
**What**: Implemented aircraft-style banking where dragon leans into turns  
**Files**:
- EXTENDED: `FamiliarDynamics.cs` (core banking system)
- EXTENDED: `FamiliarPlayLaserChaseState.cs` (chase state banking)
- EXTENDED: `FamiliarDebugUI.cs` (bank angle display)

**Features**:
- Turn rate calculation (degrees/second on horizontal plane)
- Proportional banking angle (smoothly lerps to target)
- Banked up vector (tilts world up around forward axis)

**Decisions**:
- Negated bank angle for correct left/right banking direction
- Applied to both automatic body tracking and manual rotation
- Uses Func&lt;string&gt; callbacks for real-time updates (NOTE: HTML entities!)
- Performance target: less than 1ms per frame (NOTE: spelled out, not <1ms)

**Status**: ✅ Complete - Banking physics working, ready for Unity testing
```

**Formatting Notes for Timeline Entries:**
- Use HTML entities for generics: `Func&lt;T&gt;` not `` `Func<T>` ``
- Spell out comparisons: "less than 1ms" not "<1ms"
- No backticks for attributes: `[Attribute]` not `` `[Attribute]` ``
- No backticks for directives: `#if` not `` `#if` ``

### Bad Timeline Entry Example:
```markdown
### October 17, 2025 - Worked on stuff
**What**: Added some banking code
**Files**: FamiliarDynamics.cs
**Features**: Banking
**Status**: Done
```
*(Too vague, no architectural context, no decisions documented)*

## Example Reference

See `Branch_MovementPass.md` for a complete example of a well-maintained branch doc.

## Tips

1. **Start immediately**: Create the doc when you create the branch
2. **Update as you go**: Don't wait until the end
3. **Think PR-first**: Write PR notes as you implement features
4. **Document decisions**: Future you will thank present you
5. **Link, don't duplicate**: Reference feature docs for details
6. **Use the template**: Copy/paste to maintain consistency
7. **Watch your markdown**: Use HTML entities for angle brackets in generics (Func&lt;string&gt;), spell out comparisons, avoid problematic backtick usage

## Quick Formatting Reference

When writing timeline entries and PR notes:

| Type | ❌ Wrong | ✅ Right |
|------|---------|---------|
| Generics in text | Func<string> | Func&lt;string&gt; |
| Generics in code | N/A | `Func<string>` is fine |
| Comparisons in text | <1ms | less than 1ms |
| Attributes | `` `[Obsolete]` `` | `[Obsolete]` |
| Directives | `` `#if UNITY_EDITOR` `` | `#if UNITY_EDITOR` |

---

*This guide helps maintain consistent, useful branch documentation that serves both development tracking and PR preparation.*

