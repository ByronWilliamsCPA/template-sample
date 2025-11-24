# Template Feedback - 11/24/2025

## Issue 1: Cruft Update Only Modified Tracking File, Not Project Files
**Category**: Configuration
**Severity**: Medium
**Files Affected**: `.cruft.json`

### Description
The recent cruft commit (468a169) updated the template tracking from commit `e1d2b76` to `117d92a0` (19 commits spanning significant template improvements), but only modified `.cruft.json` without applying any actual file changes to the project.

**Template commits skipped**:
- feat(template): add two-part standards system for safe cruft updates
- feat(template): add baseline files for README, feedback, and env
- refactor(template): consolidate CLAUDE.md into single file at root
- Multiple CI/CD, SonarCloud, and template validation fixes

**Changes identified by `cruft diff`**:
1. **Linear Integration Removal** (`.claude/commands/pr.md`, `.claude/skills/pr-prepare/SKILL.md`, `.coderabbit.yaml`)
   - Correctly removed since `include_linear: "no"` in `.cruft.json`
2. **Redis/ARQ Config Removal** (`.env.example`)
   - Correctly removed since caching and background jobs are disabled
3. **Code Quality Improvements** (`.claude/skills/project-planning/scripts/validate-planning-docs.py`)
   - Bug fix: Changed `removeprefix()` to slice notation for compatibility
   - Fix: Added explicit else block for better code structure
4. **Documentation Fixes** (`.claude/context/python-standards.md`)
   - Changed code fence from ` ``` ` to ` ```text ` for proper syntax highlighting
5. **Date Updates** (`.claude/README.md`)
   - Last Updated: 2025-11-23 → 2025-11-24

### Root Cause Analysis
The project appears to have **already diverged** from the template in ways that prevent automatic updates:
- Custom `.git/config` with remotes and branch configuration
- Project-specific modifications to template files
- Possible manual application of some template changes

This is a **template lifecycle issue**: Once projects start active development, they naturally diverge from the template, making `cruft update` less effective.

### Suggested Fix
**For Template**:
1. **Document the "baseline vs. customization" pattern** more clearly
   - Template should clearly mark which files are "safe to update" vs. "customize freely"
   - Consider a `TEMPLATE_MANAGED.md` file listing which files should remain in sync
2. **Add a `cruft-update-check` workflow** that validates updates
   - Detects when `cruft diff` shows changes but `cruft update` doesn't apply them
   - Creates an issue with a summary of missed updates
3. **Improve conditional rendering** for feature-specific content
   - The Linear removal is working correctly (conditional on `include_linear`)
   - Consider similar patterns for other integrations

**For Generated Projects**:
1. **Add a "template sync status" check** to pre-commit hooks
   - Warns when template version is outdated (commit hash check)
   - Suggests running `cruft diff` to see available updates
2. **Document the merge strategy** in project setup guide
   - When to use `cruft update` (early project lifecycle)
   - When to manually cherry-pick changes (mature projects)
   - How to handle merge conflicts

### Workaround Applied
1. Documented the issue in this feedback file
2. Identified that most "missed" changes are correctly excluded (Linear, Redis) due to feature flags
3. Manually reviewing the validation script improvements for potential cherry-pick

### Impact Assessment
**Low Impact** - The skipped changes are mostly:
- ✅ Correctly excluded due to feature flags (Linear, Redis)
- ✅ Minor documentation improvements
- ⚠️ One code quality fix that could be cherry-picked

**The template's conditional rendering is working as designed.**

---

## Issue 2: Branch Name Change from "master" to "main" Not Documented
**Category**: Documentation
**Severity**: Low
**Files Affected**: `.cruft.json` (`checkout` field)

### Description
The `.cruft.json` file shows a branch name change from `"master"` to `"main"` in the template repository. This is a positive change aligning with modern Git conventions, but:
1. The change wasn't mentioned in the commit message
2. No migration guidance provided for existing projects
3. Template documentation doesn't explain when this change occurred

### Suggested Fix
**For Template**:
1. Add a `CHANGELOG.md` entry documenting the branch rename
2. Include migration instructions for projects still tracking `master`
3. Document in template README that default branch is `main`

**For Generated Projects**:
- No action needed - cruft automatically updated the tracking branch

### Workaround Applied
None needed - the change was applied successfully.

---

## Issue 3: Git Configuration Not Managed by Template
**Category**: Enhancement
**Severity**: Low
**Files Affected**: `.git/config`, `.git/index`, `.git/COMMIT_EDITMSG`

### Description
The `cruft diff` shows differences in `.git/` directory files, which is expected since these are project-specific. However, this clutters the diff output and may confuse users.

### Suggested Fix
**For Template**:
1. Add `.git/` to cruft's skip patterns in `.cruft.json`
2. Ensure cookiecutter doesn't render anything into `.git/` directly
3. Document that git configuration is project-specific and not template-managed

### Workaround Applied
None needed - this is expected behavior. Documenting for template improvement.

---

## Issue 4: Code Quality Fix Available for Cherry-Pick
**Category**: Enhancement
**Severity**: Low
**Files Affected**: `.claude/skills/project-planning/scripts/validate-planning-docs.py`

### Description
Template commit introduces two code quality improvements to the validation script:
1. Replaces `removeprefix("./")` with slice notation `[2:]` for better compatibility
2. Adds explicit `else` block instead of implicit return path

**Diff**:
```python
# Old (lines 79-80):
link_path = link_path.removeprefix("./")

# New (lines 79-80):
if link_path.startswith("./"):
    link_path = link_path[2:]

# Old (lines 251-255):
    return 1
print("Status: All documents valid")
print(f"\n{'=' * 60}")
return 0

# New (lines 252-256):
    return 1
else:
    print("Status: All documents valid")
    print(f"\n{'=' * 60}")
    return 0
```

### Suggested Fix
**For This Project**:
Apply these changes manually if the validation script is actively used.

**For Template**:
Consider adding a "CHANGELOG-PATCHES.md" that lists small fixes projects may want to cherry-pick.

### Workaround Applied
Documented for later review - not critical for project functionality.

---

## Summary

**Total Issues**: 4 (1 Medium, 3 Low)

**Key Finding**: The template's conditional rendering is working correctly. Most "missed" changes were properly excluded due to feature flags (`include_linear: "no"`, caching disabled, etc.). The actual divergence is minimal and expected for an active project.

**Recommended Template Improvements**:
1. ✅ Document baseline vs. customization pattern
2. ✅ Add cruft-update-check workflow
3. ✅ Create CHANGELOG.md for template changes
4. ✅ Improve `.git/` exclusion in cruft config

**Recommended Project Actions**:
1. ✅ Review validation script improvements for cherry-pick (low priority)
2. ✅ Monitor template updates periodically via `cruft check` && `cruft diff`
3. ✅ No immediate action required - project is in good state
