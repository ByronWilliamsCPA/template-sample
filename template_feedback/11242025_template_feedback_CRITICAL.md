# Template Feedback - 11/24/2025 (CRITICAL)

## CRITICAL ISSUE: Manual .cruft.json Edit Instead of Proper Update

**Category**: Bug
**Severity**: CRITICAL
**Files Affected**: `.cruft.json`, entire project
**Commit**: 468a169646e1974e541a10459ea9be6f46ddc530

### Executive Summary

Commit 468a169 ("chore: update template tracking to latest commit") **manually edited `.cruft.json`** instead of running `cruft update`. This resulted in:
- ❌ `.cruft.json` claims project is at template commit `117d92a0` (latest)
- ❌ Actual project files remain at template commit `d400df9` (20 commits behind)
- ❌ `cruft check` reports "up to date" (false positive)
- ❌ `cruft update` says "Nothing to do" (incorrect)
- ❌ `cruft diff` shows ~2000 lines of differences (ignored)

**This is a template testing/validation failure that masks real issues.**

---

## Root Cause Analysis

### 1. Manual Edit Detected
```bash
$ git show 468a169 --stat
 .cruft.json | 6 +++---
 1 file changed, 3 insertions(+), 3 deletions(-)
```

Only `.cruft.json` was changed. No project files were updated. This is **not** the output of `cruft update`, which would apply template changes.

### 2. Template Commits Skipped
Between old (`d400df9`) and new (`117d92a0`) tracking commits:
- **20 template commits** with actual code/config changes
- **0 project files** updated to match

Template improvements completely bypassed:
```bash
$ cd /home/byron/dev/cookiecutter-python-template
$ git log --oneline d400df9..117d92a0
117d92a (HEAD -> main) Merge pull request #9
a347f05 fix(qlty): correct cookiecutter template exclusion pattern
75584a8 fix(ci): make SonarCloud non-blocking
95685d3 fix(template): remove hardcoded references
... [16 more commits with real changes]
```

### 3. Why Cruft Update Failed (When Attempted)

When attempting a proper `cruft update` after reverting `.cruft.json`:
```bash
$ cruft update --skip-apply-ask
Error: Unable to interpret changes between current project and
cookiecutter template as unicode. Typically a result of hidden
binary files in project folder.
```

**Cause**: Binary files in the project directory that cruft cannot diff:
- `.mypy_cache/` - Type checker cache (binary JSON)
- `.venv/` - Python virtual environment
- `.git/index` - Git index (binary)
- Jupyter notebook artifacts (`.orig` files)

**These directories should be excluded from cruft processing but aren't.**

---

## Impact Assessment

### Immediate Impacts
1. **False "up to date" status** - Project appears current but isn't
2. **Missed bug fixes** - 20 commits of improvements not applied:
   - Code quality fixes (`removeprefix()` → slice notation)
   - CI/CD improvements (SonarCloud, validation)
   - Documentation improvements
   - Template rendering fixes
3. **Test project invalid** - Cannot validate template changes
4. **Hidden divergence** - Project and template silently out of sync

### Long-Term Risks
1. **Compound divergence** - Each failed update increases gap
2. **Migration difficulty** - Larger diffs = harder manual merges
3. **Lost confidence** - Cannot trust cruft status
4. **Template QA failure** - Test project doesn't catch issues

---

## Suggested Fixes

### Fix 1: Add Binary Exclusions to Template (HIGH PRIORITY)

**For Template** (`cookiecutter.json` or post-gen hook):

Add `skip` field to generated `.cruft.json`:
```json
{
  "template": "/path/to/template",
  "commit": "...",
  "skip": [
    ".git/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "venv/",
    ".tox/",
    "*.pyc",
    "__pycache__/",
    "*.egg-info/",
    ".coverage",
    "htmlcov/",
    "dist/",
    "build/"
  ]
}
```

**Implementation**: Add to `hooks/post_gen_project.py`:
```python
import json
from pathlib import Path

cruft_file = Path(".cruft.json")
cruft_config = json.loads(cruft_file.read_text())

# Add skip patterns
cruft_config["skip"] = [
    ".git/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "venv/",
    ".tox/",
    "*.pyc",
    "__pycache__/",
    "*.egg-info/",
    ".coverage",
    "htmlcov/",
    "dist/",
    "build/"
]

cruft_file.write_text(json.dumps(cruft_config, indent=2))
```

### Fix 2: Add Cruft Update Validation Hook (MEDIUM PRIORITY)

**For Template**: Add pre-commit hook that prevents manual `.cruft.json` edits.

Create `.github/workflows/validate-cruft.yml`:
```yaml
name: Validate Cruft Status

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Check if .cruft.json was manually edited
        run: |
          if git diff HEAD^ HEAD --name-only | grep -q '\.cruft\.json'; then
            # .cruft.json was changed
            if ! git diff HEAD^ HEAD --name-only | grep -qv '\.cruft\.json'; then
              # ONLY .cruft.json was changed (suspicious)
              echo "❌ ERROR: .cruft.json was edited without updating project files"
              echo "This suggests manual editing instead of 'cruft update'"
              echo ""
              echo "To fix: Run 'cruft update' instead of manually editing .cruft.json"
              exit 1
            fi
          fi

      - name: Install cruft
        run: pip install cruft

      - name: Verify cruft status
        run: |
          if ! cruft check; then
            echo "❌ Project is out of sync with template"
            echo "Run: cruft diff"
            echo "Then: cruft update"
            exit 1
          fi
```

### Fix 3: Document Proper Update Workflow (MEDIUM PRIORITY)

**For Template**: Add `TEMPLATE_MAINTENANCE.md` to generated projects:

```markdown
# Template Maintenance Guide

This project was generated from cookiecutter-python-template.

## Staying in Sync

### Check for Updates
\`\`\`bash
cruft check  # Returns success if up to date
cruft diff   # Show what would change
\`\`\`

### Apply Updates
\`\`\`bash
# 1. Ensure clean working tree
git status  # Must show "nothing to commit"

# 2. Update from template
cruft update

# 3. Review changes
git diff

# 4. Run tests
uv run pytest

# 5. Commit if successful
git add .
git commit -m "chore: update from template"
\`\`\`

### Troubleshooting

**Error: "Unable to interpret changes as unicode"**
- Cause: Binary files (.mypy_cache/, .venv/, .git/)
- Fix: Add exclusions to .cruft.json "skip" field

**Cruft says "up to date" but files don't match**
- Cause: .cruft.json was manually edited
- Fix: Revert .cruft.json to last known good commit, then run cruft update
\`\`\`bash
git log -- .cruft.json  # Find last good version
git checkout <commit> -- .cruft.json
cruft update
\`\`\`

**Never manually edit .cruft.json**
- Always use `cruft update` to sync with template
- Manual edits break cruft's tracking
\`\`\`
\`\`\`

### Fix 4: For This Project (IMMEDIATE)

**Recovery Steps**:
```bash
# 1. Revert the bad commit (already done in testing: c596a18)
# Currently .cruft.json points to d400df9 (old commit)

# 2. Clean binary caches
rm -rf .mypy_cache .pytest_cache .ruff_cache

# 3. Add skip patterns to .cruft.json
jq '.skip = [".git/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/", ".venv/", "venv/", "*.pyc", "__pycache__/", "*.egg-info/"]' .cruft.json > .cruft.json.tmp
mv .cruft.json.tmp .cruft.json

# 4. Run proper update
cruft update

# 5. Review and test changes
git diff
uv run pytest

# 6. Commit
git add .
git commit -m "fix: properly apply template updates via cruft"
```

---

## Verification

After applying fixes, verify:
```bash
# 1. Cruft status is accurate
cruft check  # Should pass

# 2. Files match template
cruft diff  # Should show no (or minimal) differences

# 3. Skip patterns work
echo "test" > .mypy_cache/test.json
cruft diff  # Should NOT show .mypy_cache/ changes

# 4. Updates apply cleanly
# (Make a change in template and test update)
```

---

## Additional Template Improvements

### 1. Add Cruft Status to README Badge
```markdown
[![Cruft Status](https://img.shields.io/badge/cruft-up%20to%20date-brightgreen)](https://github.com/cruft/cruft)
```

### 2. Add Renovate Bot Rule for Template Updates
```json
{
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["\\.cruft\\.json$"],
      "matchStrings": [
        "\"commit\":\\s*\"(?<currentValue>[a-f0-9]+)\""
      ],
      "depNameTemplate": "cookiecutter-python-template",
      "datasourceTemplate": "git-refs",
      "packageNameTemplate": "https://github.com/ByronWilliamsCPA/cookiecutter-python-template"
    }
  ]
}
```

### 3. Add MkDocs Page for Template Sync
Generate a documentation page showing:
- Current template version (commit hash + date)
- Last sync date
- Link to `cruft diff` output
- Instructions for updating

---

## Lessons Learned

1. **Never manually edit `.cruft.json`** - Always use `cruft update`
2. **Binary files break cruft** - Must add skip patterns
3. **"Up to date" can be false** - Validate with `cruft diff`
4. **Test projects need automation** - CI should catch these issues
5. **Documentation is critical** - Users need clear update workflow

---

## Priority Action Items

**For Template** (upstream fixes):
- [ ] CRITICAL: Add `skip` patterns to `.cruft.json` generation
- [ ] HIGH: Add cruft validation CI workflow
- [ ] MEDIUM: Create `TEMPLATE_MAINTENANCE.md` documentation
- [ ] LOW: Add README badge for cruft status

**For This Project** (immediate recovery):
- [ ] CRITICAL: Clean binary caches
- [ ] CRITICAL: Add skip patterns to `.cruft.json`
- [ ] CRITICAL: Run proper `cruft update`
- [ ] HIGH: Validate all 20 template commits were applied
- [ ] HIGH: Test project functionality after update
- [ ] MEDIUM: Document the incident for future reference

---

## References

- Original bad commit: 468a169
- Template range skipped: d400df9..117d92a0 (20 commits)
- Cruft documentation: https://cruft.github.io/cruft/
- Related issue: Binary file handling in cruft diffs
