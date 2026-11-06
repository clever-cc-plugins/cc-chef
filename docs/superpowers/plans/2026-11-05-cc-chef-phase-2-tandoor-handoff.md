# Phase 2 (Tandoor): handoff

Status on 2026-11-06: Tasks 1–11 of `2026-11-05-cc-chef-phase-2-tandoor.md` are done and committed on `feat/phase-2-tandoor`. Task 11 (live verification against Tandoor 2.7.2) passed after two fixes. What is left is the merge to `main`.

## State

- Both test suites pass: `python3 -m unittest discover -s tests/tandoor -v` (94 tests) and `python3 -m unittest discover -s tests/recipe-tool -v` (42 tests). Python 3.9 is unverified.
- `python3 tests/tandoor/live_smoke.py --run` ran against a fresh, empty test instance: 35 results, 0 FAIL, and it removes everything it creates. It is opt-in and needs `TANDOOR_URL` and `TANDOOR_TOKEN` (write scope).
- One real food merge went through the `tandoor-food-cleanup` flow: the notes moved, the recipe stayed intact, the alias exists, the kept food was unchanged, and the source's properties were deleted with it.
- `tandoor-api.md` section 4 has a status column per fact: `verified against 2.7.2, 2026-11-06`, corrected by the live check, or still `from source, 2026-11-05`.

## What the live check changed

- `numrecipe` is only on a single entry with `?extended=1`, never in the lists. `foods-report` now asks for the members of duplicate groups one by one.
- `GET /api/ingredient/?simple=1` drops `used_in_recipes`. `group-plan` no longer sends `simple`; before, every preview said "recipe unknown" and warned about hidden recipes.
- The fake server now behaves like the instance in both points, and tests pin both fixes.

## Review of the branch (`/code-review high main`, 2026-11-06)

Fixed, each with a test that fails on the old code:

- `upload`: a failed read-back after a successful save now prints the recipe id and says not to upload the plan again.
- `pull` refuses to overwrite an existing file, so a second rework on the same day cannot destroy the first backup. `rework-recipe` adds `-2`, `-3` for a taken name.
- `render_source` writes `(unnamed)` for a step without a name; `recipe_tool` rejects a bare `### 2.`.
- `group-plan` stops with a message for ids that are not in the report.
- "Maybe" groups pick the representative of each cluster after the recipe counts are loaded.
- `preview` shows what a new keyword resembles (`similar: Familie (id 7)`); keywords stay auto-created, since a tag is cheap to rename and a question per tag would nag on every upload.
- `build_index` takes, among entries with the same normalized name (`Zwiebel`, `zwiebel`), the one the cleanup would keep (`suggest_keep`) instead of the first listed.

Decided later or left open:

- `scripts/sync-config-table.sh` deletes every `|` line in the Key Config Files section: outside Phase 2, check separately.
- The alias filter, `ALIAS_TYPES` and the unit-name set are repeated in several places.

## Still unchecked

- Whether the ingredient list leaves out other users' private recipes: needs a second user. The script treats a gap between `numrecipe` and the recipes reached as hidden recipes.
- Alias matching on a real import. The merge creates the alias live; resolving it in `match` is only covered by `test_alias_from_a_merge_resolves_in_the_next_match` against the fake.
- A wrong `name` in a nested `food` with `id` renames the food (from source, not tried).
- Python 3.9.

## Rulings made during implementation

- The commit trailer says `Claude Sonnet 5.5`, not the plan's `Claude Opus 5.5`, because that was the model doing the work. Cost if wrong: amend the trailers.
- The branch was pushed on the owner's explicit request, although the plan says "never push".

## Deferred minors

- Plan and report files stay in `/tmp` when a session refuses `rm`.
- `group-apply` does not re-list a source's ingredients before merging, so an ingredient added after `group-plan` loses its detail on merge.
- "Maybe" duplicate groups list one best entry per cluster and can overlap a "same" group's keep entry.
