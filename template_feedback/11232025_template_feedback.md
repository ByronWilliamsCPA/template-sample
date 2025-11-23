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
