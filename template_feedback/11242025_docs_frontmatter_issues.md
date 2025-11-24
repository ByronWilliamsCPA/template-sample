# Template Feedback - Documentation Front Matter Issues

**Date**: 11/24/2025
**Category**: Bug
**Severity**: Medium
**Files Affected**: 24 documentation files

## Summary

The template-generated documentation files have systematic front matter validation issues that cause pre-commit hooks to fail.

## Issues Identified

### 1. Redundant H1 Headers (21 files)

**Problem**: Documentation files include H1 headers (`# Title`) that duplicate the front matter `title` field. The validation hook correctly identifies these as redundant since MkDocs Material automatically renders titles from front matter.

**Affected Files**:
- `docs/OPENSSF_COMPLIANCE.md`
- `docs/PROJECT_SETUP.md`
- `docs/PYTHON_COMPATIBILITY.md`
- `docs/api-reference.md`
- `docs/index.md`
- `docs/development/architecture.md`
- `docs/development/code-quality.md`
- `docs/development/contributing.md`
- `docs/development/testing.md`
- `docs/guides/configuration.md`
- `docs/guides/overview.md`
- `docs/guides/usage.md`
- `docs/planning/README.md`
- `docs/planning/adr/README.md`
- `docs/planning/project-vision.md`
- `docs/planning/roadmap.md`
- `docs/planning/tech-spec.md`
- `docs/project/changelog.md`
- `docs/project/license.md`
- `docs/project/roadmap.md`
- `docs/template_feedback.md`

**Example**:
```markdown
---
title: Project Setup Guide
---

# Project Setup Guide  ← REDUNDANT - Remove this line
```

**Fix**: Remove the H1 header from each file.

### 2. Invalid Tags (4 files)

**Problem**: Some files use tags that don't match the expected schema (`script`, `knowledge`, `planning`, `common`).

**Files**:
1. `docs/ADRs/adr-template.md`
   - Invalid `schema_type`: 'adr' (should be one of: script, knowledge, planning, common)
   - Unknown tags: `decision`, `your-topic`, `relevant-area`
   - Unknown owner: 'Your Team Role or Name' (placeholder text)

2. `docs/planning/project-plan-template.md`
   - Unknown tags: `project`, `strategy`
   - Missing required field: `planning/source`
   - Validation error: `purpose` must end with terminal punctuation

3. `docs/project/changelog.md`, `docs/project/license.md`, `docs/project/roadmap.md`
   - Unknown tag: `project`

**Fix**: Update tags to match allowed schema or update validation schema to allow these tags.

### 3. Schema Validation Errors (2 files)

**Files**:
1. `docs/planning/adr/README.md`
   - Unable to extract tag using discriminator 'schema_type'

2. `docs/template_feedback.md`
   - Unable to extract tag using discriminator 'schema_type'

**Fix**: Add proper `schema_type` field to front matter.

## Root Cause

The template generates documentation files with:
1. **Legacy formatting**: H1 headers that pre-date front matter standardization
2. **Placeholder content**: Template files (`adr-template.md`, `project-plan-template.md`) have placeholder tags/owners
3. **Incomplete schema coverage**: The validation schema doesn't cover all legitimate tag categories used in generated docs

## Suggested Template Fixes

### Fix 1: Remove Redundant H1 Headers in Template

**Location**: All documentation templates in the cookiecutter template

**Change**: Remove H1 headers from documentation file templates since MkDocs Material renders them automatically from front matter.

**Before**:
```markdown
---
title: {{ cookiecutter.project_name }}
---

# {{ cookiecutter.project_name }}

Content here...
```

**After**:
```markdown
---
title: {{ cookiecutter.project_name }}
---

Content here...
```

### Fix 2: Fix Template File Placeholders

**File**: `docs/ADRs/adr-template.md`

**Change**:
```yaml
# Before
tags:
  - schema_type: adr  # Invalid
  - decision
  - your-topic       # Placeholder
  - relevant-area    # Placeholder
owner: Your Team Role or Name  # Placeholder

# After
tags:
  - schema_type: planning  # Valid type
  - decision
  - architecture
  - adr
owner: Development Team
```

### Fix 3: Expand Validation Schema

**Location**: `.claude/skills/validate-front-matter` (or wherever validation is defined)

**Change**: Add support for legitimate tag categories:
```python
ALLOWED_SCHEMA_TYPES = ['script', 'knowledge', 'planning', 'common', 'project', 'adr']
```

### Fix 4: Complete Front Matter for All Files

**Files**: `docs/planning/adr/README.md`, `docs/template_feedback.md`

**Add**:
```yaml
---
title: [Appropriate Title]
tags:
  - schema_type: common  # or appropriate type
  - [other relevant tags]
---
```

## Impact

**Current**:
- ❌ Pre-commit validation fails on all generated projects
- ❌ Developers must manually fix 20+ documentation files
- ❌ Creates friction in template adoption

**After Fix**:
- ✅ Pre-commit passes on freshly generated projects
- ✅ No manual intervention required
- ✅ Consistent documentation structure

## Priority

**HIGH** - This affects every project generated from the template and blocks pre-commit workflow.

## Workaround for This Project

For now, we can skip the front matter validation to unblock other tests:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: validate-front-matter
      name: Validate documentation front matter
      entry: python .claude/skills/project-planning/scripts/validate-front-matter.py
      language: python
      files: 'docs/.*\.md$'
      exclude: 'docs/index.md'  # Add exclusions as needed
```

Or temporarily disable in this test project:
```bash
SKIP=validate-front-matter pre-commit run --all-files
```

## Verification

After template fixes:
1. Generate new project from template
2. Run `pre-commit run --all-files`
3. Verify no front matter validation errors
4. Check documentation renders correctly in MkDocs

---

**Action Required**: Update cookiecutter template to fix these systematic documentation issues.
