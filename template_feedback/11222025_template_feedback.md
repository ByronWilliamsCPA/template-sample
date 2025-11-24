# Template Feedback - 11/22/2025

## Issue 1: Missing LICENSES Directory Files

**Category**: Configuration
**Severity**: High
**Files Affected**: `LICENSES/` directory (missing), `REUSE.toml`

### Description

The REUSE compliance check fails because the `LICENSES/` directory does not contain the actual license text files for the licenses referenced in source files via SPDX headers. The template defines licenses (CC0-1.0, CC-BY-4.0, MIT) in `REUSE.toml` but doesn't include the corresponding license files.

Error from CI:
```
Missing licenses: CC0-1.0, CC-BY-4.0, MIT
Files with copyright information: 84 / 111
Files with license information: 84 / 111
```

### Suggested Fix

Add the following to the cookiecutter template:
1. Create `LICENSES/` directory in template
2. Add license text files:
   - `LICENSES/MIT.txt`
   - `LICENSES/CC0-1.0.txt`
   - `LICENSES/CC-BY-4.0.txt`

Or add a post-generation hook that runs `reuse download --all` after project creation.

### Workaround Applied

None yet - needs to be fixed in template.

---

## Issue 2: ClusterFuzzLite Configuration Issue

**Category**: Configuration
**Severity**: Medium
**Files Affected**: `.github/workflows/cifuzzy.yml`, `fuzz/` directory

### Description

The ClusterFuzzLite (address sanitizer) CI job fails. This appears to be a configuration issue with the fuzzing infrastructure setup in the template.

### Suggested Fix

Review the ClusterFuzzLite workflow configuration and ensure:
1. The fuzz targets are properly configured
2. The build system correctly compiles with sanitizers
3. The corpus directory exists if required

### Workaround Applied

None - CI check fails but doesn't block development.

---

## Issue 3: SonarCloud Analysis Workflow Issue

**Category**: Configuration
**Severity**: Medium
**Files Affected**: `.github/workflows/sonarcloud.yml`, `sonar-project.properties`

### Description

The SonarCloud Analysis workflow fails. This may be due to missing secrets configuration or project setup issues.

### Suggested Fix

1. Ensure `SONAR_TOKEN` secret is documented as required
2. Verify `sonar-project.properties` has correct default values
3. Add conditional check to skip if secrets not configured

### Workaround Applied

None - separate SonarCloud Code Analysis check passes.

---

## Issue 4: Validate Requirements Sync Cache Issue

**Category**: Configuration
**Severity**: Low
**Files Affected**: `.github/workflows/pr-validation.yml`

### Description

The UV cache path doesn't exist error appears in CI:
```
Cache path /home/runner/work/_temp/setup-uv-cache does not exist on disk.
```

This is a minor issue related to UV cache configuration in GitHub Actions.

### Suggested Fix

Update the UV setup action configuration to handle empty cache gracefully or disable caching for validation-only jobs.

### Workaround Applied

None - this is a warning that doesn't affect functionality.

---

## Issue 5: Files Missing SPDX Headers

**Category**: Configuration
**Severity**: Medium
**Files Affected**: Multiple files (27 files without SPDX headers)

### Description

REUSE compliance shows 84/111 files have copyright/license information. The remaining 27 files need SPDX headers or should be added to `REUSE.toml` annotations.

Missing files include:
- `.sonarlint/connectedMode.json`
- `.qlty/qlty.toml`
- Various config files

### Suggested Fix

Update `REUSE.toml` in the template to include glob patterns for common config files that don't support comments, or add SPDX headers to files that support them.

### Workaround Applied

None yet.

---
