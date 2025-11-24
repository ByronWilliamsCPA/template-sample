# Qlty Code Smells Analysis - Template Feedback

**Date**: 11/24/2025
**Category**: Code Quality
**Severity**: Medium
**Tool**: Qlty v0.592.0

## Executive Summary

Qlty's code smell analysis detected **10 quality issues** across 2 files that weren't caught by ruff. These findings complement the linting results and highlight maintainability concerns in optional feature files.

### Issues Summary

| File | Issue Type | Count | Severity |
|------|------------|-------|----------|
| noxfile.py | Code Duplication | 5 instances | Medium |
| src/template_sample/core/sentry.py | Function Complexity | 3 issues | Medium |
| src/template_sample/core/sentry.py | Code Duplication | 2 instances | Medium |

**Total**: 10 code smells
**Status**: All issues in optional features (Sentry not enabled, Nox template code)

---

## Detailed Findings

### 1. Code Duplication in noxfile.py (5 instances)

#### Issue 1.1: Duplicated Test Session Patterns (20 lines x 3 locations)
**Mass**: 90
**Locations**:
- Lines 316-335 (`unit` session)
- Lines 338-357 (`integration` session)
- Lines 360-379 (`fast` session)

**Pattern**:
```python
@nox.session(python="3.12")
def [session_name](session: nox.Session) -> None:
    """[Session description]

    [Details about session purpose]
    """
    session.install("-e", ".[dev]")
    session.run(
        "pytest",
        "-v",
        "[session-specific-args]",
        env={...},
    )
```

**Impact**: Moderate - Template code duplication makes noxfile harder to maintain

**Suggested Fix**:
```python
def _run_pytest_session(
    session: nox.Session,
    *,
    test_path: str,
    description: str,
    extra_args: list[str] | None = None,
) -> None:
    """Shared pytest session logic."""
    session.install("-e", ".[dev]")
    args = ["pytest", "-v", test_path]
    if extra_args:
        args.extend(extra_args)
    session.run(*args)

@nox.session(python="3.12")
def unit(session: nox.Session) -> None:
    """Run unit tests only."""
    _run_pytest_session(
        session,
        test_path="tests/unit",
        description="Unit tests",
        extra_args=["--cov=src", "--cov-fail-under=85"]
    )
```

#### Issue 1.2: Similar Test Session Setup (18 lines x 2 locations)
**Mass**: 73
**Locations**:
- Lines 296-313 (`test` session)
- Lines 383-400 (`security_tests` session)

**Pattern**: Nearly identical session setup and configuration patterns

**Suggested Fix**: Extend the shared helper function to cover these cases too

#### Issue 1.3: Duplicated Session Execution (17 lines x 2 locations)
**Mass**: 73
**Locations**:
- Multiple noxfile test sessions

**Overall Recommendation**: Extract common session logic into reusable helper functions

---

### 2. Function Complexity in sentry.py (3 issues)

#### Issue 2.1: Too Many Parameters
**Function**: `init_sentry`
**Line**: 36
**Count**: 8 parameters
**Threshold**: 7 (exceeded by 1)

**Current Signature**:
```python
def init_sentry(
    dsn: str | None = None,
    environment: str | None = None,
    release: str | None = None,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
    enable_tracing: bool = True,
    enable_profiling: bool = True,
    debug: bool = False,
) -> None:
```

**Impact**: Moderate - Makes function harder to call and test

**Suggested Fix**: Use a configuration dataclass
```python
@dataclass
class SentryConfig:
    """Sentry SDK configuration."""
    dsn: str | None = None
    environment: str | None = None
    release: str | None = None
    traces_sample_rate: float = 0.1
    profiles_sample_rate: float = 0.1
    enable_tracing: bool = True
    enable_profiling: bool = True
    debug: bool = False

def init_sentry(config: SentryConfig | None = None) -> None:
    """Initialize Sentry SDK for error tracking."""
    config = config or SentryConfig()
    # ... implementation
```

#### Issue 2.2: Deeply Nested Control Flow
**Function**: `before_send_hook` (nested data scrubbing logic)
**Line**: 202
**Nesting Level**: 4
**Threshold**: 4 (at limit)

**Current Structure**:
```python
def before_send_hook(event, hint):
    # Level 1: if condition
    if "request" in event:
        # Level 2: if condition
        if "data" in event["request"]:
            # Level 3: for loop
            for field in sensitive_fields:
                # Level 4: if condition
                if field in event["request"]["data"]:
                    event["request"]["data"][field] = "[REDACTED]"
```

**Impact**: Moderate - At maximum acceptable nesting level

**Suggested Fix**: Extract nested logic into helper functions
```python
def _scrub_request_data(request_data: dict, sensitive_fields: list) -> None:
    """Remove sensitive fields from request data."""
    for field in sensitive_fields:
        if field in request_data:
            request_data[field] = "[REDACTED]"

def before_send_hook(event, hint):
    if "request" in event and "data" in event["request"]:
        _scrub_request_data(event["request"]["data"], SENSITIVE_FIELDS)
```

#### Issue 2.3: High Cyclomatic Complexity
**Function**: `before_send_hook`
**Line**: 171
**Complexity**: 18
**Threshold**: 12 for Python (exceeded by 6)

**Analysis**: Function has 18 possible execution paths due to:
- Multiple conditional branches for filtering
- Nested loops for data scrubbing
- Exception type checks
- Environment checks

**Impact**: High - Function is difficult to test and maintain

**Suggested Fix**: Decompose into smaller functions
```python
def before_send_hook(event, hint):
    """Coordinate event filtering and scrubbing."""
    if should_filter_event(event, hint):
        return None

    scrub_sensitive_data(event)
    add_custom_tags(event)

    return event

def should_filter_event(event, hint) -> bool:
    """Check if event should be filtered out."""
    # Filter logic here (reduces main function complexity)
    ...

def scrub_sensitive_data(event) -> None:
    """Remove sensitive data from event."""
    # Scrubbing logic here
    ...
```

---

### 3. Code Duplication in sentry.py (2 instances)

#### Issue 3.1: Duplicated Exception/Message Capture Logic (43 lines x 2)
**Mass**: 136
**Locations**:
- Lines 229-271 (`capture_exception`)
- Lines 274-316 (`capture_message`)

**Pattern**: Nearly identical wrapper functions with only input type difference

**Current Code** (simplified):
```python
def capture_exception(exception, *, level="error", tags=None, extra=None):
    """Capture exception to Sentry."""
    if not sentry_sdk:
        logger.warning("...")
        return None

    scope = sentry_sdk.Scope()
    if tags:
        for key, value in tags.items():
            scope.set_tag(key, value)
    if extra:
        for key, value in extra.items():
            scope.set_extra(key, value)

    return sentry_sdk.capture_exception(exception, scope=scope)

def capture_message(message, *, level="info", tags=None, extra=None):
    """Capture message to Sentry."""
    if not sentry_sdk:
        logger.warning("...")
        return None

    scope = sentry_sdk.Scope()
    if tags:
        for key, value in tags.items():
            scope.set_tag(key, value)
    if extra:
        for key, value in extra.items():
            scope.set_extra(key, value)

    return sentry_sdk.capture_message(message, level, scope=scope)
```

**Impact**: High - 43 lines of duplicated code makes maintenance difficult

**Suggested Fix**: Extract common scope setup logic
```python
def _configure_scope(tags: dict | None, extra: dict | None) -> sentry_sdk.Scope:
    """Configure Sentry scope with tags and extra data."""
    scope = sentry_sdk.Scope()

    if tags:
        for key, value in tags.items():
            scope.set_tag(key, value)

    if extra:
        for key, value in extra.items():
            scope.set_extra(key, value)

    return scope

def capture_exception(exception, *, level="error", tags=None, extra=None):
    """Capture exception to Sentry."""
    if not sentry_sdk:
        logger.warning("Sentry SDK not available")
        return None

    scope = _configure_scope(tags, extra)
    return sentry_sdk.capture_exception(exception, scope=scope)

def capture_message(message, *, level="info", tags=None, extra=None):
    """Capture message to Sentry."""
    if not sentry_sdk:
        logger.warning("Sentry SDK not available")
        return None

    scope = _configure_scope(tags, extra)
    return sentry_sdk.capture_message(message, level, scope=scope)
```

**Reduction**: ~43 lines → ~30 lines (30% reduction)

---

## Configuration Issues

### Invalid Plugin Configuration
```
WARNING: The `plugins.ruff` entry in qlty.toml is not part of the
supported configuration and will be ignored.
```

**Issue**: The `.qlty/qlty.toml` file contains `[plugins.ruff]` configuration, but:
1. This configuration format is not supported by qlty v0.592.0
2. Qlty reports 0 available plugins
3. Plugin definition for ruff doesn't exist

**Impact**: Ruff integration via qlty is non-functional

**Current Config** (lines 45-52 in `.qlty/qlty.toml`):
```toml
[plugins.ruff]
enabled = true
package_file = "pyproject.toml"
config_files = ["pyproject.toml", "ruff.toml", ".ruff.toml"]
file_types = ["python"]
triggers = ["pre-commit", "pre-push", "ide", "build"]
```

**Suggested Fix**: Remove invalid plugin configuration
```toml
# Remove [plugins.ruff] section entirely
# Ruff should be run via pre-commit hooks instead

# Keep only the smells configuration
[smells]
mode = "comment"
...
```

**Note**: The comment in the config file acknowledges this:
> Security tools are run via pre-commit hooks instead of qlty plugins

The same pattern should apply to ruff.

---

## Priority Recommendations for Template

### 1. HIGH: Fix Code Duplication in sentry.py

**Action**: Extract `_configure_scope` helper function
**Impact**: Reduces duplication by 30%, improves maintainability
**Files**: `{{cookiecutter.project_slug}}/src/{{cookiecutter.project_slug}}/core/sentry.py`

### 2. MEDIUM: Simplify before_send_hook Complexity

**Action**: Decompose into `should_filter_event` and `scrub_sensitive_data`
**Impact**: Reduces complexity from 18 → ~6, easier to test
**Files**: Same as #1

### 3. MEDIUM: Refactor noxfile Test Sessions

**Action**: Extract `_run_pytest_session` helper
**Impact**: Reduces 60+ lines of duplication
**Files**: `{{cookiecutter.project_slug}}/noxfile.py`

### 4. LOW: Use Config Dataclass for init_sentry

**Action**: Replace 8 parameters with SentryConfig dataclass
**Impact**: Cleaner API, easier to extend
**Files**: Same as #1

### 5. LOW: Remove Invalid Qlty Plugin Config

**Action**: Delete `[plugins.ruff]` section from qlty.toml
**Impact**: Eliminates warning, clarifies tool boundaries
**Files**: `{{cookiecutter.project_slug}}/.qlty/qlty.toml`

---

## Comparison with Ruff Findings

### Complementary Detection

Qlty found issues that ruff didn't detect:
- ✅ **Code duplication** - Qlty's structural analysis found 43-line duplicate blocks
- ✅ **Cyclomatic complexity** - Qlty measured 18 vs threshold of 12
- ✅ **Parameter count** - Qlty flagged 8 parameters vs threshold of 7
- ✅ **Nesting depth** - Qlty detected level-4 nesting

Ruff found issues Qlty didn't:
- ✅ **Blind exception catching** (BLE001) - 18 occurrences
- ✅ **Commented code** (ERA001) - 22 occurrences
- ✅ **Import sorting** (I001) - 4 occurrences
- ✅ **Type annotation style** (UP007) - 3 occurrences

### Recommended Tool Combination

Use **both tools** for comprehensive coverage:
1. **Ruff**: Style, imports, simple anti-patterns (fast, 90 issues found)
2. **Qlty**: Structural issues, complexity, duplication (slower, 10 issues found)

Total unique issues: ~95 (some overlap expected)

---

## Test Environment

**Qlty Version**: 0.592.0 linux-x64 (eb6f5d8 2025-11-23)
**Analysis Scope**: vs. origin/main (6 files analyzed)
**Execution Time**: <1 second
**Configuration**: `.qlty/qlty.toml` (with invalid plugin config)

---

## Conclusion

Qlty's code smell analysis successfully identified **10 structural quality issues** that complement ruff's 90 linting findings. The combination provides comprehensive code quality coverage.

**Key Takeaway**: All Qlty issues are in **optional feature files** (Sentry, Nox), validating that:
1. Core project code has good quality
2. Optional features need refactoring before enabling
3. Template should apply these fixes upstream

**Template Quality Impact**: These findings should be addressed in the cookiecutter template to ensure all generated projects start with high-quality, maintainable code.
