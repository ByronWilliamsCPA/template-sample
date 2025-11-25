# Cruft Update Effectiveness Evaluation - CRITICAL FAILURE

**Date**: 11/24/2025
**Category**: Template Synchronization
**Severity**: CRITICAL
**Impact**: All existing projects using cruft updates

## Executive Summary

The cruft update process is **fundamentally broken** for this template. While `cruft check` reports the project is "up to date," it fails to remove conditional files that should be deleted based on the cookiecutter context settings.

**Result**: Projects accumulate orphaned files for disabled features, causing:
- ❌ Test coverage failures (testing code that shouldn't exist)
- ❌ False positive security/lint findings
- ❌ Confusion about what features are enabled
- ❌ Bloated project size

---

## Evidence

### Configuration in `.cruft.json`

The cookiecutter context specifies these features are **DISABLED**:

```json
{
  "include_api_framework": "no",
  "include_sentry": "no",
  "include_background_jobs": "no",
  "include_caching": "no"
}
```

### Files That Should NOT Exist (But Do)

| Feature | Setting | Files Present | Should Exist? |
|---------|---------|---------------|---------------|
| API Framework | `no` | `src/template_sample/api/` (2 files) | ❌ NO |
| Sentry | `no` | `src/template_sample/core/sentry.py` (12KB) | ❌ NO |
| Background Jobs | `no` | `src/template_sample/jobs/` (2 files) | ❌ NO |
| Caching | `no` | `src/template_sample/core/cache.py` (12KB) | ❌ NO |
| Security Middleware | (implied by no API) | `src/template_sample/middleware/security.py` | ❌ NO |

**Total orphaned code**: ~55KB across 7+ files

### What `cruft check` Reports

```
SUCCESS: Good work! Project's cruft is up to date and as clean as possible :).
```

This is **FALSE** - the project contains ~55KB of code that shouldn't exist.

### What `cruft diff` Shows

```
🧹 Cleaning up conditional files...
  ✓ Removed: src/template_sample/api/health.py
  ✓ Removed: src/template_sample/api/
  ✓ Removed: src/template_sample/core/sentry.py
  ✓ Removed: src/template_sample/middleware/security.py
  ✓ Removed: src/template_sample/jobs/
  ✓ Removed: src/template_sample/core/cache.py
```

The diff shows what **WOULD** happen if you regenerated the project fresh. But `cruft update` **DOES NOT** execute post-generation hooks that clean up conditional files.

---

## Root Cause Analysis

### How Cookiecutter Conditional Files Work

1. **During initial generation**: Post-generation hooks in `hooks/post_gen_project.py` delete files based on cookiecutter context settings
2. **During cruft update**: Only file content changes are applied - post-generation hooks are **NOT re-run**

### The Fundamental Problem

```
Initial Generation:
  cookiecutter → generates all files → post_gen_project.py deletes conditional files → clean project

Cruft Update:
  cruft update → applies diffs to existing files → SKIPS post_gen_project.py → orphaned files remain
```

### Why This Happened

1. Template originally generated with `include_api_framework: "yes"` (or similar)
2. Later `.cruft.json` was updated to `include_api_framework: "no"`
3. `cruft update` updated the context but **NOT** the actual file structure
4. Conditional files remained because cruft doesn't re-run cleanup hooks

---

## Impact Assessment

### On This Project

| Issue | Impact |
|-------|--------|
| **Test Coverage** | 14.75% instead of expected 80%+ (orphaned files count against coverage) |
| **Ruff Issues** | 90 issues (mostly in orphaned files) |
| **Bandit Issues** | 5 issues (4 in orphaned files) |
| **SonarCloud Issues** | 37 code smells (majority in orphaned files) |
| **Qlty Issues** | 10 code smells (all in orphaned files) |
| **CI/CD Failures** | Coverage threshold fails due to uncovered orphaned code |

### On All Existing Projects Using This Template

Any project that:
1. Was generated with optional features enabled
2. Later changed `.cruft.json` context to disable features
3. Ran `cruft update`

...will have the same orphaned file problem.

---

## Recommended Fixes

### Fix 1: Add Cruft Post-Update Hook (PREFERRED)

**Problem**: Cruft doesn't support post-update hooks natively.

**Workaround**: Create a wrapper script that runs after cruft update:

```bash
#!/bin/bash
# scripts/cruft-update.sh

# Run normal cruft update
cruft update "$@"

# Run conditional file cleanup
python hooks/cleanup_conditional_files.py
```

**Template Change Required**: Extract cleanup logic from `hooks/post_gen_project.py` into reusable script.

### Fix 2: Add CI Validation for Orphaned Files

Add workflow to detect configuration/file mismatches:

```yaml
# .github/workflows/validate-cruft.yml
- name: Check for orphaned conditional files
  run: |
    python scripts/check_conditional_files.py
```

```python
# scripts/check_conditional_files.py
import json
from pathlib import Path

CONDITIONAL_FILES = {
    "include_api_framework": ["src/*/api/"],
    "include_sentry": ["src/*/core/sentry.py"],
    "include_background_jobs": ["src/*/jobs/"],
    "include_caching": ["src/*/core/cache.py"],
}

with open(".cruft.json") as f:
    context = json.load(f)["context"]["cookiecutter"]

errors = []
for feature, paths in CONDITIONAL_FILES.items():
    if context.get(feature) == "no":
        for pattern in paths:
            for match in Path(".").glob(pattern):
                errors.append(f"Orphaned file: {match} (feature '{feature}' is disabled)")

if errors:
    print("❌ ORPHANED FILES DETECTED:")
    for e in errors:
        print(f"  - {e}")
    exit(1)
```

### Fix 3: Document the Limitation

At minimum, document in template README:

```markdown
## Important: Cruft Update Limitations

When using `cruft update` to sync with template changes, **conditional files
are NOT automatically removed**. After changing feature flags in `.cruft.json`:

1. Manually delete orphaned directories/files
2. Or regenerate the project fresh

Files to check when disabling features:
- `include_api_framework: no` → delete `src/*/api/`
- `include_sentry: no` → delete `src/*/core/sentry.py`
- `include_background_jobs: no` → delete `src/*/jobs/`
- `include_caching: no` → delete `src/*/core/cache.py`
```

### Fix 4: Immediate Manual Cleanup for This Project

```bash
# Remove orphaned files for disabled features
rm -rf src/template_sample/api/
rm -f src/template_sample/core/sentry.py
rm -f src/template_sample/core/cache.py
rm -rf src/template_sample/jobs/
rm -f src/template_sample/middleware/security.py

# Also remove related test files if they exist
rm -rf tests/unit/api/
rm -rf tests/integration/api/

# Update __init__.py files to remove imports
# (may need manual editing)
```

---

## Verification After Fix

After cleaning up orphaned files, re-run validation:

```bash
# Coverage should improve dramatically
pytest --cov=src/template_sample --cov-fail-under=80

# Ruff issues should drop significantly
ruff check .

# SonarCloud issues should reduce
# (will require new analysis)
```

**Expected Improvements**:
- Coverage: 14.75% → 80%+ (removing untested orphaned code)
- Ruff issues: 90 → ~10-20 (removing issues in orphaned files)
- SonarCloud code smells: 37 → ~10 (removing smells in orphaned files)

---

## Template Changes Required

### Priority 1: Immediate Documentation
Add warning to template's README about cruft update limitations.

### Priority 2: Validation Script
Add `scripts/check_conditional_files.py` to detect orphaned files.

### Priority 3: CI Integration
Add orphaned file check to `validate-cruft.yml` workflow.

### Priority 4: Wrapper Script (Long-term)
Create `scripts/cruft-update.sh` that re-runs cleanup after update.

---

## Related Issues

- Previous feedback: `11242025_template_feedback_CRITICAL.md` (cruft skip patterns)
- Test results: `11242025_test_suite_results.md` (coverage failure explanation)
- SonarCloud: `11242025_sonarcloud_analysis.md` (code smell distribution)

---

## Conclusion

The cruft update process created a **false sense of synchronization**. While the template tracking (`.cruft.json`) was updated correctly, the actual project files remained out of sync with the configured features.

**This is a fundamental limitation of cruft** - it syncs file contents but doesn't re-run post-generation cleanup hooks.

**Recommended Action**:
1. Manually remove orphaned files from this project NOW
2. Add validation scripts to the template to prevent this in future projects
3. Document the limitation prominently in template documentation

---

## Test Environment

- **Cruft Version**: Latest (installed at `/usr/local/bin/cruft`)
- **Template Commit**: `4c7d848cee14f5f4d37f24e52a192ecd1a805757`
- **Project**: template-sample
- **Date**: 2025-11-24
