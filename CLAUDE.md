# cc-chef

A Claude Code plugin to create, adapt, rework and export grounded everyday recipes.

## Key Config Files

| File                                              | Purpose                                                                                        |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `.claude/format-markdown.sh`                      | PostToolUse hook: formats Markdown files with prettier after edits                             |
| `.claude/guard-secret-files.sh`                   | PreToolUse hook: blocks reads/edits/writes of secret .env files                                |
| `.claudeignore`                                   | Paths excluded from Claude Code indexing                                                       |
| `CLAUDE.md`                                       | Project instructions, loaded every message                                                     |
| `.claude/settings.json`                           | Permissions, hooks, environment variables                                                      |
| `.githooks/pre-commit`                            | Secret scanning (gitleaks) + CLAUDE.md table sync                                              |
| `.github/workflows/claude-code-review.yml`        | Auto-runs Claude Code review on PRs from trusted authors (owner/member/collaborator)           |
| `.github/workflows/claude.yml`                    | Runs Claude Code on `@claude` mentions in issues/PR comments/reviews, gated to trusted authors |
| `.github/workflows/release.yml`                   | Triggers the shared `clever-cc-plugins/.github` release workflow on push to `main`             |
| `.gitignore`                                      | Git ignore patterns                                                                            |
| `plugins/cc-chef/.claude-plugin/plugin.json`      | Plugin manifest                                                                                |
| `plugins/cc-chef/skills/chef-onboarding/SKILL.md` | TODO: add description                                                                          |
| `plugins/cc-chef/skills/export-recipe/SKILL.md`   | TODO: add description                                                                          |
| `scripts/sync-config-table.sh`                    | Keeps Key Config Files table in sync on each commit                                            |

## Don't

- Don't commit secrets or credentials to git
- Don't use `--force` flags — fix the underlying issue instead
- Don't commit `docs/owner-inputs/` or quote personal details from it

## Learnings

When the user corrects a mistake or points out a recurring issue, append a one-line summary to `.claude/learnings.md`. Don't modify `CLAUDE.md` directly.
