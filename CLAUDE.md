# cc-chef

A Claude Code plugin to create, adapt, rework and export grounded everyday recipes.

## Key Config Files

| File                                                   | Purpose                                                                                         |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `.claude/format-markdown.sh`                           | PostToolUse hook: formats Markdown files with prettier after edits                              |
| `.claude/guard-secret-files.sh`                        | PreToolUse hook: blocks reads/edits/writes of secret .env files                                 |
| `.claude/settings.json`                                | Permissions, hooks, environment variables                                                       |
| `.githooks/pre-commit`                                 | Secret scanning (gitleaks) + CLAUDE.md table sync                                               |
| `.github/workflows/claude-code-review.yml`             | Auto-runs Claude Code review on PRs from trusted authors (owner/member/collaborator)            |
| `.github/workflows/claude.yml`                         | Runs Claude Code on `@claude` mentions in issues/PR comments/reviews, gated to trusted authors  |
| `.github/workflows/release.yml`                        | Triggers the shared `clever-cc-plugins/.github` release workflow on push to `main`              |
| `.github/workflows/tests.yml`                          | Runs the recipe-tool and Tandoor unit tests on Python 3.9 and 3.12 for PRs and pushes to `main` |
| `.gitignore`                                           | Git ignore patterns                                                                             |
| `CLAUDE.md`                                            | Project instructions, loaded every message                                                      |
| `plugins/cc-chef/.claude-plugin/plugin.json`           | Plugin manifest                                                                                 |
| `plugins/cc-chef/skills/chef-onboarding/SKILL.md`      | Sets up cooking preferences, save folder and one-time disclaimer                                |
| `plugins/cc-chef/skills/create-recipe/SKILL.md`        | Turns a mood, ingredients, photo or dish name into a cookable recipe                            |
| `plugins/cc-chef/skills/dietary-guidelines/SKILL.md`   | Opt-in personal dietary guideline per household member                                          |
| `plugins/cc-chef/skills/export-recipe/SKILL.md`        | Saves recipes as Markdown; converts to JSON-LD or Paprika; uploads to Tandoor                   |
| `plugins/cc-chef/skills/research-prompt/SKILL.md`      | Builds a deep-research prompt for a diet or food constraint                                     |
| `plugins/cc-chef/skills/rework-recipe/SKILL.md`        | Restructures an existing recipe to the user's preferences                                       |
| `plugins/cc-chef/skills/tandoor-food-cleanup/SKILL.md` | Merges duplicate Tandoor foods and units group by group after approval                          |
| `scripts/sync-config-table.sh`                         | Keeps Key Config Files table in sync on each commit                                             |

<!-- cc-config: last-optimize-run: 2026-11-07 9eb135012687e7e4c76ff53541f9b2fb6a839d6c -->

## Commands

- Test the recipe tool: `python3 -m unittest discover -s tests/recipe-tool -v`
- Test the Tandoor scripts (fake server, no real instance): `python3 -m unittest discover -s tests/tandoor -v`

## Don't

- Don't commit secrets or credentials to git
- Don't use `--force` flags — fix the underlying issue instead
- Don't commit `docs/owner-inputs/` or quote personal details from it

## Learnings

When the user corrects a mistake or points out a recurring issue, append a one-line summary to `.claude/learnings.md`. Don't modify `CLAUDE.md` directly.

## Compact Instructions

When compacting, preserve: the list of modified files, test status, and open TODOs.
