# Template Feedback - 11/23/2025

## Issue 1: Missing Org-Level Claude Skills from Template

**Category**: Enhancement
**Severity**: High
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/skills/`

### Description

The cookiecutter template only includes 3 skills, while the organization-level `.claude` repo (`~/.claude/` / `williaby/.claude`) contains 5+ comprehensive skill sets with workflows and context files. Projects generated from the template are missing significant automation capabilities.

**What's Included in Template:**
- `project-planning/` - Project planning document generation
- `pr-prepare/` - PR description preparation
- `commit-prepare/` - Conventional commit message preparation

**What's Available at Org Level (MISSING from template):**
- `git/` - Full git workflow skill with branch validation, status checks, milestone management
  - Workflows: branch.md, commit.md, pr-prepare.md, pr-check.md, status.md, milestone.md
  - Context: branch-strategies.md, conventional-commits.md
- `quality/` - Code quality automation
  - Workflows: format.md, lint.md, precommit.md, naming.md
- `security/` - Security validation and scanning
  - Workflows: validate-env.md, scan.md, encrypt.md
  - Context: owasp-top-10.md, security-commands.md
- `testing/` - Comprehensive testing automation
  - Workflows: generate.md, review.md, e2e.md, security.md, performance.md
  - Context: pytest-commands.md, pytest-patterns.md
- `rad/` - Response-Aware Development (assumption tracking)
  - Workflows: verify.md, list.md, test.md
  - Context: methodology.md, tagging-standards.md

### Suggested Fix

**Option A (Recommended): Git Subtree Approach**
Extend the existing git subtree pattern to include the full `.claude/skills/` directory from `williaby/.claude`:

```bash
# In post_gen_project.py hook, add:
git subtree add --prefix .claude/org-skills https://github.com/williaby/.claude.git main --squash
```

**Option B: Selective Inclusion**
Add the most valuable skills directly to the template (prioritized):
1. `git/` - Essential for git workflow automation
2. `quality/` - Critical for code quality enforcement
3. `security/` - Important for security-first development
4. `testing/` - Valuable for test automation

**Option C: Feature Flag**
Add `include_org_skills` cookiecutter variable to optionally include org-level skills.

### Workaround Applied

Users must manually copy skills from `~/.claude/skills/` or set up additional git subtrees.

---

## Issue 2: Missing Specialized Agents Definitions

**Category**: Enhancement
**Severity**: High
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/agents/` (doesn't exist)

### Description

The template doesn't include any agent definitions, while the org-level repo contains 19+ specialized agent definitions that enable powerful automation workflows via the Task tool.

**Available Org-Level Agents (NOT in template):**

**Core Development Agents:**
- `code-reviewer.md` - Automated code quality and standards review
- `test-engineer.md` - Test strategy and generation
- `security-auditor.md` - Security analysis and vulnerability detection
- `documentation-writer.md` - Technical documentation generation

**Specialized Technical Agents:**
- `api-development-agent.md` - API development and OpenAPI specs
- `database-operations-agent.md` - Database operations and migrations
- `frontend-design-agent.md` - Frontend design and React components
- `devops-deployment-agent.md` - CI/CD and deployment automation
- `git-workflow-agent.md` - Git workflow assistance
- `github-workflow-agent.md` - GitHub API interactions

**AI/Knowledge Agents:**
- `ai-engineer.md` - LLM applications and RAG systems
- `prompt-engineer.md` - Prompt optimization
- `knowledge-manager.md` - Knowledge base management

**Orchestration Agents:**
- `project-plan-synthesizer.md` - Project plan synthesis
- `journey-orchestrator.md` - Multi-level UX management
- `modularization-assistant.md` - System decomposition

### Suggested Fix

Create `.claude/agents/` directory in template with commonly-needed agents:

**Priority 1 (Always Include):**
- `code-reviewer.md`
- `test-engineer.md`
- `security-auditor.md`

**Priority 2 (Python Projects):**
- `api-development-agent.md`
- `database-operations-agent.md`

**Priority 3 (Feature-Flagged):**
- `frontend-design-agent.md` (if `include_frontend`)
- `devops-deployment-agent.md` (if `include_docker` or `include_github_actions`)

### Workaround Applied

None - agents are only available if defined in `~/.claude/agents/` at user level.

---

## Issue 3: Missing Quality/Security/Testing Slash Commands

**Category**: Enhancement
**Severity**: Medium
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/commands/`

### Description

The template only includes 2 commands (`plan.md`, `pr.md`), while the org-level repo has 15+ slash commands for quality, security, testing, and meta operations.

**What's in Template:**
- `plan.md` - Project planning
- `pr.md` - PR preparation

**Missing Commands from Org Level:**

**Quality Commands:**
- `quality-format-code.md` - Format code files
- `quality-lint-check.md` - Run linters
- `quality-precommit-validate.md` - Pre-commit validation
- `quality-naming-conventions.md` - Check naming conventions

**Security Commands:**
- `security-validate-env.md` - Validate GPG/SSH keys
- `security.md` - Security validation

**Testing Commands:**
- `testing.md` - Testing strategy and execution

**Meta Commands:**
- `meta-command-help.md` - Command help system
- `meta-list-commands.md` - List available commands

### Suggested Fix

Add essential commands to template (prioritized):
1. `quality-lint-check.md` - Most commonly needed
2. `security-validate-env.md` - Security-first requirement
3. `testing.md` - Testing automation
4. `meta-command-help.md` - User discoverability

### Workaround Applied

Users rely on org-level commands in `~/.claude/commands/` (if available).

---

## Issue 4: Missing Hooks Configuration

**Category**: Enhancement
**Severity**: Medium
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/settings.json` (doesn't exist)

### Description

The template doesn't include any Claude Code hooks configuration, while the org-level repo has valuable hooks for TDD enforcement and MCP usage tracking.

**Org-Level Hooks (NOT in template):**

**PreToolUse Hooks:**
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hook": "$HOME/.claude/scripts/tdd-enforcement-hook.sh"
}
```
Purpose: Enforce TDD by requiring tests before implementation.

**PostToolUse Hooks:**
```json
{
  "matcher": "mcp__*",
  "hook": "$HOME/.claude/scripts/track-mcp-usage.sh"
}
```
Purpose: Track MCP server usage for analytics.

### Suggested Fix

Add optional `settings.json` or `settings.local.json` to template with:

1. **Feature-flagged hooks:**
   - `enforce_tdd` cookiecutter variable enables TDD hook
   - `track_mcp_usage` enables MCP tracking

2. **Project-specific hooks:**
   - Pre-commit validation hook
   - Code review trigger hook

### Workaround Applied

Users must configure hooks manually or rely on global hooks in `~/.claude/settings.json`.

---

## Issue 5: Missing Context Files for Shared Patterns

**Category**: Enhancement
**Severity**: Medium
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/context/` (doesn't exist)

### Description

The org-level repo has shared context files that agents and skills reference for consistency. These are missing from generated projects.

**Org-Level Context Files:**
- `shared-architecture.md` - Common system architectures
- `development-standards.md` - Universal coding standards
- `integration-patterns.md` - Common integration patterns

### Suggested Fix

Create `.claude/context/` directory with project-relevant context:
- `python-standards.md` - Python-specific standards (reference to ruff, basedpyright)
- `testing-patterns.md` - pytest patterns for this project
- `api-patterns.md` (if building APIs)

### Workaround Applied

Context must be included inline in prompts or referenced from global files.

---

## Issue 6: Missing MCP Server Project Configuration

**Category**: Enhancement
**Severity**: Low
**Files Affected**: `{{cookiecutter.project_slug}}/.claude/.mcp.json` (doesn't exist)

### Description

While the template root has `.mcp.json`, the generated project directory doesn't include project-specific MCP configuration, limiting discoverability of available MCP servers.

**Template Root Has:**
```json
{
  "mcpServers": {
    "zen": { ... },
    "context7": { ... },
    "sonarqube": { ... }
  }
}
```

**Generated Project Has:** Nothing (relies on global `~/.claude/.mcp.json`)

### Suggested Fix

Add `.claude/.mcp.json` to generated projects with:
1. Comments explaining available servers
2. Project-specific server configurations
3. Feature-flagged servers (sonarqube if `include_sonarqube`)

### Workaround Applied

Users rely on global MCP configuration.

---

## Issue 7: Standards Subtree Only Includes `claude.md`

**Category**: Bug
**Severity**: High
**Files Affected**: `.claude/standard/` subtree setup

### Description

The git subtree from `williaby/.claude` should bring in the full standards structure, but it appears the template only references `.claude/standard/claude.md`. The org repo has a complete `/standards/` directory with domain-specific files.

**Org-Level Standards Available:**
- `standards/python.md` - Python development standards
- `standards/git-workflow.md` - Git workflow standards
- `standards/git-worktree.md` - Git worktree patterns
- `standards/security.md` - Security requirements
- `standards/linting.md` - Linting configuration

**What Template References:** Only `.claude/standard/claude.md`

### Suggested Fix

1. Verify git subtree is pulling full directory structure
2. Update CLAUDE.md references to point to specific standard files
3. Ensure `update-claude-standards.sh` script pulls all standards

### Workaround Applied

Standards are documented in global `~/.claude/CLAUDE.md` but not accessible at project level.

---

## Issue 8: Missing Temporary Reference File Pattern

**Category**: Enhancement
**Severity**: Low
**Files Affected**: `{{cookiecutter.project_slug}}/tmp_cleanup/` (doesn't exist)

### Description

The org-level CLAUDE.md documents the anti-compaction strategy using `tmp_cleanup/` directory for temporary reference files, but this isn't set up in generated projects.

### Suggested Fix

1. Create `tmp_cleanup/` directory in template with `.gitkeep`
2. Add `.gitignore` entry: `tmp_cleanup/.tmp-*`
3. Document usage in CLAUDE.md

### Workaround Applied

Users create the directory manually when needed.

---

## Summary: Priority Recommendations

### Must-Have (High Priority)
1. **Git skill** with full workflow automation
2. **Quality skill** for code quality enforcement
3. **Code-reviewer agent** for automated reviews
4. **Test-engineer agent** for test generation
5. **Security-auditor agent** for vulnerability detection
6. **Full standards subtree** (not just claude.md)

### Should-Have (Medium Priority)
7. Quality/security/testing slash commands
8. Hooks configuration (TDD enforcement)
9. Context files for shared patterns

### Nice-to-Have (Low Priority)
10. Project-specific MCP configuration
11. tmp_cleanup directory setup
12. Additional specialized agents (feature-flagged)

---

## Impact Assessment

**Current State:** Generated projects have ~15% of available Claude Code automation capabilities.

**With Recommended Changes:** Projects would have ~80% of capabilities, with the remaining 20% available through user-level configuration for specialized needs.

**Token Efficiency:** Including skills/agents at project level allows better context loading and reduces reliance on large global CLAUDE.md files.

---

# Pre-Commit & Code Quality Issues (Discovered During Validation)

## Issue 9: Syntax Error in `financial.py` - Malformed Module Docstring

**Category**: Bug (Critical)
**Severity**: Critical
**Files Affected**: `{{cookiecutter.project_slug}}/src/{{cookiecutter.project_slug}}/utils/financial.py`

### Description

The `financial.py` file has a malformed module docstring. The docstring closes on line 1 but additional documentation text continues on lines 3-22 **outside** the docstring, causing Python syntax errors.

**Current (Broken):**
```python
"""Financial utilities module."""

CRITICAL: Always use Decimal for financial calculations...
```

**Expected:**
```python
"""Financial utilities module.

CRITICAL: Always use Decimal for financial calculations...
"""
```

### Impact

- **268 ruff errors** cascade from this syntax error
- File cannot be imported or type-checked
- All tests for financial utilities fail

### Suggested Fix

Update the template to properly format the module docstring with all content inside the triple quotes.

---

## Issue 10: Missing Dev Dependencies Not Installed by Default

**Category**: Bug
**Severity**: High
**Files Affected**: `pyproject.toml`, project setup documentation

### Description

Running `uv sync` (default) does not install development dependencies. Users must explicitly run `uv sync --all-extras` or `uv sync --extra dev`. This causes:

1. `basedpyright` not found when running type checks
2. `pytest-cov` not available - coverage options fail
3. `python-frontmatter` not installed - pre-commit hook fails

**Error Examples:**
```bash
$ uv run basedpyright src/
error: Failed to spawn: `basedpyright`

$ uv run pytest -v
pytest: error: unrecognized arguments: --cov=src/template_sample
```

### Suggested Fix

1. Update `README.md` and `CLAUDE.md` Quick Start to explicitly show:
   ```bash
   uv sync --all-extras  # NOT just "uv sync"
   ```

2. Consider adding a Makefile or `justfile` with:
   ```makefile
   setup:
       uv sync --all-extras
       uv run pre-commit install
   ```

---

## Issue 11: Pre-Commit `validate-front-matter` Hook Missing Dependency

**Category**: Bug
**Severity**: Medium
**Files Affected**: `.pre-commit-config.yaml`, `tools/validate_front_matter.py`

### Description

The custom `validate-front-matter` hook fails because `python-frontmatter` is in dev dependencies but the hook runs in a separate environment without access to project dependencies.

**Error:**
```
Traceback (most recent call last):
  File "/home/byron/dev/template-sample/tools/validate_front_matter.py", line 32, in <module>
    import frontmatter
ModuleNotFoundError: No module named 'frontmatter'
```

### Suggested Fix

**Option A**: Add `additional_dependencies` to the pre-commit hook:
```yaml
- repo: local
  hooks:
    - id: validate-front-matter
      additional_dependencies: ['python-frontmatter>=1.1.0']
```

**Option B**: Use a pre-commit repo that includes the dependency.

---

## Issue 12: Interrogate Hook Fails on Python 3.14 Syntax

**Category**: Bug
**Severity**: High
**Files Affected**: `.pre-commit-config.yaml`

### Description

The `interrogate` pre-commit hook runs in Python 3.10 but encounters Python 3.14-specific syntax in source files (or files with syntax errors), causing AST parsing failures.

**Error:**
```python
File "/usr/lib/python3.10/ast.py", line 50, in parse
  return compile(source, filename, mode, flags,
File "<unknown>", line 74
  except ImportError:
  ^^^^^^
SyntaxError: invalid syntax
```

### Root Cause

The hook's Python version (3.10) cannot parse newer Python syntax. This is exacerbated by the `financial.py` syntax error (Issue 9).

### Suggested Fix

1. Fix the `financial.py` syntax error first (Issue 9)
2. Consider pinning interrogate to use the project's Python version:
   ```yaml
   - repo: https://github.com/econchick/interrogate
     hooks:
       - id: interrogate
         language_version: python3.12
   ```

---

## Issue 13: Qlty Configuration Warnings

**Category**: Bug (Minor)
**Severity**: Low
**Files Affected**: `qlty.toml`

### Description

Qlty reports configuration warnings:
1. `plugins.ruff` entry is not supported and will be ignored
2. `Plugin not found: diff`

**Warning:**
```
WARNING: The `plugins.ruff` entry in qlty.toml is not part of the supported configuration and will be ignored.
ERROR > Plugin not found: diff
```

### Suggested Fix

Review and update `qlty.toml` to use only supported configuration options. Remove or update unsupported plugin references.

---

## Issue 14: Ruff Linting Errors in Template-Generated Code

**Category**: Bug
**Severity**: High
**Files Affected**: Multiple files in `src/template_sample/`

### Description

Beyond the `financial.py` syntax error, there are **268 ruff errors** across the codebase, including:

| Rule | Count | Description |
|------|-------|-------------|
| BLE001 | 3+ | Blind exception catches (`except Exception`) |
| ERA001 | 8+ | Commented-out code |
| PLC0415 | 3+ | Imports not at top-level |
| PLW0603 | 1+ | Global statement usage |
| TC002/TC003 | 2+ | Type-only imports outside TYPE_CHECKING |
| ARG001 | 2+ | Unused function arguments |

**Files with issues:**
- `src/template_sample/api/health.py` - Placeholder code with blind exceptions and commented code
- `src/template_sample/core/cache.py` - Global state, non-top-level imports
- `src/template_sample/utils/logging.py` - Unused arguments, type import issues

### Suggested Fix

1. Remove or properly guard placeholder/example code with `# noqa` comments and TODOs
2. Follow PyStrict-aligned rules for exception handling:
   ```python
   # Instead of:
   except Exception as e:

   # Use specific exceptions:
   except (ConnectionError, TimeoutError) as e:
   ```
3. Add type-only imports inside `TYPE_CHECKING` blocks

---

## Issue 15: pytest.ini Coverage Options Fail Without pytest-cov

**Category**: Bug
**Severity**: Medium
**Files Affected**: `pyproject.toml` (pytest configuration)

### Description

The `pyproject.toml` includes pytest addopts with coverage options, but these fail if `pytest-cov` is not installed:

```toml
[tool.pytest.ini_options]
addopts = "-v --cov=src/template_sample --cov-report=html ..."
```

**Error:**
```
pytest: error: unrecognized arguments: --cov=src/template_sample
```

### Suggested Fix

**Option A**: Move coverage options to a separate profile:
```toml
[tool.pytest.ini_options]
addopts = "-v"

# In pyproject.toml or conftest.py, document:
# For coverage: pytest --cov=src/template_sample
```

**Option B**: Add pytest-cov to core dependencies (not just dev).

---

## Updated Summary: All Issues

### Critical (Fix Immediately)
- **Issue 9**: `financial.py` syntax error (blocks all linting/testing)

### High Priority
- **Issue 10**: Dev dependencies not installed by default
- **Issue 12**: Interrogate hook Python version incompatibility
- **Issue 14**: 268 ruff linting errors in template code

### Medium Priority
- **Issue 11**: validate-front-matter missing dependency
- **Issue 15**: pytest coverage options require missing package

### Previously Documented (Enhancement Requests)
- Issues 1-8: Missing skills, agents, commands, hooks, context files

---

## Issue 16: Syntax Error in `sentry.py` - Misaligned except Block

**Category**: Bug (Critical)
**Severity**: Critical
**Files Affected**: `{{cookiecutter.project_slug}}/src/{{cookiecutter.project_slug}}/core/sentry.py`

### Description

The `sentry.py` file has an `except ImportError:` block that is incorrectly indented, placing it outside the `try` block.

**Current (Broken - Lines 68-74):**
```python
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        except ImportError:  # <-- WRONG INDENTATION
```

**Expected:**
```python
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    except ImportError:  # <-- CORRECT INDENTATION
```

### Impact

- File cannot be imported
- Bandit skips file due to syntax error
- basedpyright reports multiple cascading errors
- Any code importing Sentry integration fails

---

## Issue 17: MkDocs Build Fails - Missing `overrides` Directory

**Category**: Bug
**Severity**: High
**Files Affected**: `mkdocs.yml`

### Description

The `mkdocs.yml` configuration references `custom_dir: overrides` but the `overrides/` directory does not exist in the project.

**Error:**
```
ERROR - Config value 'theme': The path set in custom_dir ('/home/byron/dev/template-sample/overrides') does not exist.
Aborted with a configuration error!
```

### Suggested Fix

**Option A**: Create the `overrides/` directory with a `.gitkeep`:
```bash
mkdir overrides && touch overrides/.gitkeep
```

**Option B**: Remove or comment out the `custom_dir` line in `mkdocs.yml` if not needed.

---

## Issue 18: Vulnerable Dependency - `py` Package (CVE-2022-42969)

**Category**: Security
**Severity**: Medium
**Files Affected**: `pyproject.toml` (dependency chain)

### Description

The `safety check` command reports a vulnerability in the `py` package version 1.11.0:

```
Vulnerability ID: 51457
Affected spec: <=1.11.0
ADVISORY: ** DISPUTED ** Py throughout 1.11.0 allows remote attackers to conduct a ReDoS attack
CVE-2022-42969
```

### Root Cause

The `py` package is likely a transitive dependency from `pytest` or another testing library.

### Suggested Fix

1. Check which package requires `py`:
   ```bash
   uv pip show py
   ```

2. If not directly needed, consider adding to `[tool.uv]` constraints to exclude or upgrade.

3. Note: This CVE is **disputed** but should be documented.

---

## Issue 19: Bandit Security Finding - Hardcoded Bind Address

**Category**: Security (Minor)
**Severity**: Low
**Files Affected**: `src/template_sample/middleware/security.py:191`

### Description

Bandit reports B104 (hardcoded_bind_all_interfaces) for `0.0.0.0` in the blocked addresses list.

**Code:**
```python
BLOCKED_ADDRESSES = {
    "127.0.0.1",
    "0.0.0.0",  # <-- Bandit flags this
    "169.254.169.254",  # AWS metadata
}
```

### Analysis

This is a **false positive**. The `0.0.0.0` is in a BLOCKED_ADDRESSES set used to prevent SSRF attacks, not as a bind address.

### Suggested Fix

Add a `# nosec B104` comment to suppress the warning:
```python
"0.0.0.0",  # nosec B104 - This is a blocked address, not a bind address
```

---

## Issue 20: basedpyright Reports 100+ Type Errors

**Category**: Bug
**Severity**: High
**Files Affected**: Multiple files in `src/template_sample/`

### Description

basedpyright in strict mode reports numerous type errors:

| Error Type | Count | Description |
|------------|-------|-------------|
| reportCallIssue | 30+ | Missing/wrong parameters in log calls |
| reportMissingImports | 1 | Missing `database` module |
| reportExplicitAny | 20+ | Untyped `Any` usage |
| reportUnknownVariableType | 15+ | Unknown types |
| reportMissingTypeArgument | 5+ | Missing generics |
| reportDeprecated | 3 | Using deprecated `datetime.utcnow()` |

**Key Issues:**
- `health.py`: Missing `error` parameter in ReadinessCheck calls
- `cache.py`: Incorrect Redis method parameters
- `worker.py`: Multiple missing parameters in log calls
- `worker.py`: Using deprecated `datetime.utcnow()`

### Suggested Fix

1. Fix log function signatures to match actual usage
2. Replace `datetime.utcnow()` with `datetime.now(timezone.utc)`
3. Add proper type annotations to generic types

---

## Issue 21: Safety Command Deprecation Warning

**Category**: Documentation
**Severity**: Low
**Files Affected**: Documentation, CI workflows

### Description

The `safety check` command is deprecated:

```
DEPRECATED: this command (`check`) has been DEPRECATED, and will be unsupported beyond 01 June 2024.
We highly encourage switching to the new `scan` command.
```

### Suggested Fix

Update all references from `safety check` to `safety scan`:
- CLAUDE.md
- CI workflows
- Pre-commit hooks

---

## Final Summary: All CI/CD Issues

### Critical (Blocks CI/CD)
| Issue | File | Description |
|-------|------|-------------|
| #9 | `financial.py` | Malformed docstring syntax |
| #16 | `sentry.py` | Misaligned except block |
| #17 | `mkdocs.yml` | Missing `overrides/` directory |

### High Priority
| Issue | Description |
|-------|-------------|
| #10 | Dev dependencies require `--all-extras` |
| #12 | Interrogate hook Python version |
| #14 | 268 ruff linting errors |
| #20 | 100+ basedpyright type errors |

### Medium Priority
| Issue | Description |
|-------|-------------|
| #11 | validate-front-matter missing dependency |
| #15 | pytest coverage options require pytest-cov |
| #18 | Vulnerable `py` package (disputed CVE) |

### Low Priority
| Issue | Description |
|-------|-------------|
| #13 | Qlty configuration warnings |
| #19 | Bandit false positive (nosec needed) |
| #21 | Safety command deprecation |

### Tests Status
✅ **All 21 tests pass** (without coverage options)

---

# Qlty Code Quality Issues

## Issue 22: Qlty Configuration - `plugins.ruff` Not Supported

**Category**: Bug
**Severity**: Medium
**Files Affected**: `.qlty/qlty.toml`

### Description

The qlty configuration uses `[plugins.ruff]` section, but this syntax is not supported by current qlty versions:

```
WARNING: The `plugins.ruff` entry in qlty.toml is not part of the supported configuration and will be ignored.
```

**Current Config (Line 45-52):**
```toml
[plugins.ruff]
enabled = true
package_file = "pyproject.toml"
config_files = ["pyproject.toml", "ruff.toml", ".ruff.toml"]
file_types = ["python"]
triggers = ["pre-commit", "pre-push", "ide", "build"]
```

### Impact

- Qlty shows "0 available plugins"
- Ruff linting is not integrated with qlty
- Pre-commit hook falls back to separate ruff execution

### Suggested Fix

1. Remove unsupported `[plugins.ruff]` section
2. Use `qlty plugins enable ruff` to properly configure
3. Or rely on pre-commit for ruff (current fallback behavior)

---

## Issue 23: Qlty Smells - High Function Complexity

**Category**: Code Quality
**Severity**: Medium
**Files Affected**: Multiple scripts and source files

### Description

`qlty smells --all` reports multiple functions exceeding complexity thresholds:

| File | Function | Complexity | Threshold |
|------|----------|------------|-----------|
| `scripts/check_quality_gate.py` | `format_report` | 33 | 12 |
| `.claude/.../validate-planning-docs.py` | `main` | 24 | 12 |
| `scripts/check_type_hints.py` | `main` | 24 | 12 |
| `scripts/check_type_hints.py` | `has_future_annotations_import` | 16 | 12 |
| `scripts/check_type_hints.py` | `add_future_import` | 16 | 12 |
| `scripts/setup_github_protection.py` | `setup_branch_protection` | 13 | 12 |

### Suggested Fix

Refactor complex functions by:
1. Extracting helper functions
2. Using early returns to reduce nesting
3. Breaking down into smaller, focused functions

---

## Issue 24: Qlty Smells - Deeply Nested Control Flow

**Category**: Code Quality
**Severity**: Low
**Files Affected**: Multiple files

### Description

Several files have control flow nesting exceeding the threshold (level 4, threshold 4):

| File | Location |
|------|----------|
| `.claude/.../validate-planning-docs.py` | Line 233 |
| `scripts/check_type_hints.py` | Lines 83, 249 |

### Suggested Fix

Reduce nesting by:
1. Using guard clauses (early returns)
2. Extracting nested logic to separate functions
3. Using comprehensions where appropriate

---

## Issue 25: Qlty Smells - Code Duplication

**Category**: Code Quality
**Severity**: Medium
**Files Affected**: `noxfile.py`, `.claude/.../validate-planning-docs.py`

### Description

Qlty detected significant code duplication:

| File | Locations | Lines | Mass |
|------|-----------|-------|------|
| `validate-planning-docs.py` | 2 | 20 | 110 |
| `noxfile.py` | 3 | 20 | 90 |
| `noxfile.py` | 2 | 18 | 73 |
| `noxfile.py` | 2 | 17 | 73 |

**In `noxfile.py`**: Test session definitions (`unit`, `integration`, `fast`) share similar boilerplate.

**In `validate-planning-docs.py`**: `validate_tech_spec` and `validate_roadmap` have duplicated validation logic.

### Suggested Fix

1. **noxfile.py**: Create a helper function for common test session setup
2. **validate-planning-docs.py**: Create a generic validation function with document-specific parameters

---

## Issue 26: Qlty Smells - Functions with Many Returns

**Category**: Code Quality
**Severity**: Low
**Files Affected**: `scripts/setup_github_protection.py`, `src/template_sample/core/cache.py`

### Description

Functions exceeding the return statement threshold (5):

| File | Function | Returns | Threshold |
|------|----------|---------|-----------|
| `setup_github_protection.py` | `setup_branch_protection` | 5 | 5 |
| `cache.py` | `cached` | 5 | 5 |

### Suggested Fix

Consider consolidating return logic:
1. Use a result variable and single return
2. Raise exceptions for error cases instead of returning early

---

## Updated Final Summary: All Issues (Including Qlty)

### Critical (Blocks CI/CD)
| Issue | File | Description |
|-------|------|-------------|
| #9 | `financial.py` | Malformed docstring syntax |
| #16 | `sentry.py` | Misaligned except block |
| #17 | `mkdocs.yml` | Missing `overrides/` directory |

### High Priority
| Issue | Description |
|-------|-------------|
| #10 | Dev dependencies require `--all-extras` |
| #12 | Interrogate hook Python version |
| #14 | 268 ruff linting errors |
| #20 | 100+ basedpyright type errors |

### Medium Priority
| Issue | Description |
|-------|-------------|
| #11 | validate-front-matter missing dependency |
| #15 | pytest coverage options require pytest-cov |
| #18 | Vulnerable `py` package (disputed CVE) |
| #22 | Qlty `plugins.ruff` config not supported |
| #23 | 6 functions exceed complexity threshold |
| #25 | Code duplication in noxfile.py and validate-planning-docs.py |

### Low Priority
| Issue | Description |
|-------|-------------|
| #13 | Qlty configuration warnings |
| #19 | Bandit false positive (nosec needed) |
| #21 | Safety command deprecation |
| #24 | Deeply nested control flow (4 instances) |
| #26 | Functions with many returns (2 instances) |

### Metrics Summary
- **Tests**: ✅ 21/21 pass
- **Ruff Errors**: 268
- **Type Errors**: 100+
- **Qlty Smells**: 15+ findings
- **Security Findings**: 1 (false positive)

---

# Additional CI/CD Issues

## Issue 27: REUSE Compliance - Missing LICENSES Directory

**Category**: Bug
**Severity**: High
**Files Affected**: Project root, `.reuse/` configuration

### Description

The project references SPDX license identifiers (MIT, CC-BY-4.0, CC0-1.0) but the `LICENSES/` directory does not exist. REUSE compliance check fails:

```
# MISSING LICENSES
'CC-BY-4.0' found in: CHANGELOG.md, CLAUDE.md, README.md...
'CC0-1.0' found in: .github/workflows/*.yml...
'MIT' found in: src/**/*.py...

Unfortunately, your project is not compliant with version 3.3 of the REUSE Specification
```

### Impact

- REUSE CI workflow will fail
- OpenSSF Scorecard penalizes missing license compliance
- 40 files missing copyright/licensing headers

### Suggested Fix

1. Create LICENSES directory and add license files:
   ```bash
   mkdir LICENSES
   reuse download MIT CC-BY-4.0 CC0-1.0
   ```

2. Add SPDX headers to files missing them (40 files in `.claude/`, `.qlty/`, etc.)

---

## Issue 28: Nox Configuration - `nox_uv.register()` Deprecated/Removed

**Category**: Bug (Critical)
**Severity**: Critical
**Files Affected**: `noxfile.py:39`

### Description

The noxfile.py calls `nox_uv.register()` but this function doesn't exist in the installed version of nox-uv (0.6.3):

```python
# noxfile.py:39
nox_uv.register()
```

**Error:**
```
AttributeError: module 'nox_uv' has no attribute 'register'
```

### Impact

- All nox sessions fail to run
- CI workflows using nox will fail
- Development workflows blocked

### Suggested Fix

Update noxfile.py to use the current nox-uv API:
```python
# Remove this line:
# nox_uv.register()

# nox-uv 0.6.x uses nox.options.default_venv_backend = "uv"
# or session.install() works automatically with uv
```

---

## Issue 29: REUSE Compliance - 40 Files Missing Copyright Headers

**Category**: Bug
**Severity**: Medium
**Files Affected**: `.claude/**`, `.qlty/`, `Dockerfile`, config files

### Description

40 files are missing SPDX copyright and license headers. Key files include:

| Category | Files |
|----------|-------|
| Claude Config | `.claude/README.md`, all agents, commands, skills, contexts |
| Build Config | `Dockerfile`, `.dockerignore` |
| Qlty Config | `.qlty/qlty.toml` |
| Other | `.env.example`, `uv.lock`, `sonar-project.properties` |

### Suggested Fix

Add SPDX headers to each file or use `.reuse/dep5` for bulk configuration:

```
# .reuse/dep5
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/

Files: .claude/*
Copyright: 2025 Byron Williams
License: MIT

Files: .qlty/*
Copyright: 2025 Byron Williams
License: CC0-1.0
```

---

## Issue 30: GitHub Actions Workflows - Valid YAML

**Category**: Verification
**Severity**: N/A (Pass)
**Files Affected**: `.github/workflows/*.yml`

### Description

All 11 GitHub Actions workflow files pass YAML syntax validation:
- ci.yml ✅
- cifuzzy.yml ✅
- docs.yml ✅
- pr-validation.yml ✅
- publish-pypi.yml ✅
- release.yml ✅
- reuse.yml ✅
- sbom.yml ✅
- scorecard.yml ✅
- security-analysis.yml ✅
- sonarcloud.yml ✅

---

## Final Complete Summary: All 30 Issues

### Critical (Blocks CI/CD) - 5 Issues
| Issue | File | Description |
|-------|------|-------------|
| #9 | `financial.py` | Malformed docstring syntax |
| #16 | `sentry.py` | Misaligned except block |
| #17 | `mkdocs.yml` | Missing `overrides/` directory |
| #27 | Project root | Missing `LICENSES/` directory |
| #28 | `noxfile.py` | `nox_uv.register()` doesn't exist |

### High Priority - 5 Issues
| Issue | Description |
|-------|-------------|
| #10 | Dev dependencies require `--all-extras` |
| #12 | Interrogate hook Python version |
| #14 | 268 ruff linting errors |
| #20 | 100+ basedpyright type errors |
| #29 | 40 files missing REUSE headers |

### Medium Priority - 6 Issues
| Issue | Description |
|-------|-------------|
| #11 | validate-front-matter missing dependency |
| #15 | pytest coverage options require pytest-cov |
| #18 | Vulnerable `py` package (disputed CVE) |
| #22 | Qlty `plugins.ruff` config not supported |
| #23 | 6 functions exceed complexity threshold |
| #25 | Code duplication in noxfile.py and validate-planning-docs.py |

### Low Priority - 6 Issues
| Issue | Description |
|-------|-------------|
| #13 | Qlty configuration warnings |
| #19 | Bandit false positive (nosec needed) |
| #21 | Safety command deprecation |
| #24 | Deeply nested control flow (4 instances) |
| #26 | Functions with many returns (2 instances) |

### Enhancement Requests - 8 Issues
| Issue | Description |
|-------|-------------|
| #1-8 | Missing skills, agents, commands, hooks, context files from org-level |

### Passed Checks
- ✅ Tests: 21/21 pass
- ✅ Cruft: Template up to date
- ✅ GitHub Actions YAML: All 11 files valid

---

## Issue 31: Test Coverage Gap - Only 20.68% Coverage

**Category**: Bug
**Severity**: High
**Files Affected**: Template test generation, `pyproject.toml`

### Description

The template generates multiple modules but does not include corresponding tests, resulting in only **20.68% test coverage** against an 80% target.

**Coverage by Module:**
| Module | Coverage | Status |
|--------|----------|--------|
| `__init__.py` | 100% | ✅ |
| `cli.py` | 100% | ✅ |
| `core/__init__.py` | 100% | ✅ |
| `core/config.py` | 100% | ✅ |
| `utils/__init__.py` | 100% | ✅ |
| `utils/logging.py` | 96.15% | ✅ |
| `api/__init__.py` | 0% | ❌ |
| `api/health.py` | 0% | ❌ |
| `core/cache.py` | 0% | ❌ |
| `jobs/__init__.py` | 0% | ❌ |
| `jobs/worker.py` | 0% | ❌ |
| `middleware/__init__.py` | 0% | ❌ |
| `middleware/security.py` | 0% | ❌ |

**Error:**
```
FAIL Required test coverage of 80% not reached. Total coverage: 20.68%
```

### Impact

- CI coverage gate fails (`--cov-fail-under=80`)
- New projects immediately fail quality checks
- Developers must write tests for template-generated code before any work

### Root Cause

1. Template generates functional modules (`api/`, `jobs/`, `middleware/`, `core/cache.py`) but no tests for them
2. Coverage also couldn't parse `sentry.py` and `financial.py` due to syntax errors (Issues #9, #16)

### Suggested Fix

**Option A**: Include stub tests for all generated modules:
```python
# tests/unit/test_health.py
"""Tests for health check endpoints."""
import pytest
from template_sample.api.health import HealthChecker

class TestHealthChecker:
    def test_initialization(self):
        """Test health checker can be instantiated."""
        checker = HealthChecker()
        assert checker is not None
```

**Option B**: Lower default coverage threshold for new projects:
```toml
# pyproject.toml
[tool.coverage.report]
fail_under = 50  # Start at 50%, increase as tests are added
```

**Option C**: Make untested modules optional features:
- Only generate `api/`, `jobs/`, `middleware/` when explicitly enabled
- Or mark them as "example" code excluded from coverage

---

## Updated Final Summary: All 31 Issues

### Critical (Blocks CI/CD) - 5 Issues
| Issue | File | Description |
|-------|------|-------------|
| #9 | `financial.py` | Malformed docstring syntax |
| #16 | `sentry.py` | Misaligned except block |
| #17 | `mkdocs.yml` | Missing `overrides/` directory |
| #27 | Project root | Missing `LICENSES/` directory |
| #28 | `noxfile.py` | `nox_uv.register()` doesn't exist |

### High Priority - 6 Issues
| Issue | Description |
|-------|-------------|
| #10 | Dev dependencies require `--all-extras` |
| #12 | Interrogate hook Python version |
| #14 | 268 ruff linting errors |
| #20 | 100+ basedpyright type errors |
| #29 | 40 files missing REUSE headers |
| #31 | Test coverage only 20.68% (target 80%) |

### Medium Priority - 6 Issues
| Issue | Description |
|-------|-------------|
| #11 | validate-front-matter missing dependency |
| #15 | pytest coverage options require pytest-cov |
| #18 | Vulnerable `py` package (disputed CVE) |
| #22 | Qlty `plugins.ruff` config not supported |
| #23 | 6 functions exceed complexity threshold |
| #25 | Code duplication in noxfile.py and validate-planning-docs.py |

### Low Priority - 6 Issues
| Issue | Description |
|-------|-------------|
| #13 | Qlty configuration warnings |
| #19 | Bandit false positive (nosec needed) |
| #21 | Safety command deprecation |
| #24 | Deeply nested control flow (4 instances) |
| #26 | Functions with many returns (2 instances) |

### Enhancement Requests - 8 Issues
| Issue | Description |
|-------|-------------|
| #1-8 | Missing skills, agents, commands, hooks, context files from org-level |

### Metrics Summary
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Tests | 21/21 pass | All pass | ✅ |
| Coverage | 20.68% | 80% | ❌ |
| Ruff Errors | 268 | 0 | ❌ |
| Type Errors | 100+ | 0 | ❌ |
| Security | 1 false positive | 0 high/critical | ✅ |
| Qlty Smells | 15+ | 0 | ⚠️ |
