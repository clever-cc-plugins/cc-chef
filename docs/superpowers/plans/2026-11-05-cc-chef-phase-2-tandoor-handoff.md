# Phase 2 (Tandoor): handoff

Status on 2026-11-06: Tasks 1–11 of `2026-11-05-cc-chef-phase-2-tandoor.md` are done and committed on `feat/phase-2-tandoor`. Task 11 (live verification against Tandoor 2.7.2) passed after two fixes. What is left is the merge to `main`.

## State

- Both test suites pass: `python3 -m unittest discover -s tests/tandoor -v` (102 tests) and `python3 -m unittest discover -s tests/recipe-tool -v` (42 tests), on Python 3.9 and 3.12; `.github/workflows/tests.yml` runs both on every PR and on pushes to `main`.
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
- PR comments (CodeRabbit, Claude review, CodeQL), fixed with tests:
  - upload compares amounts at Tandoor's four decimals (`1/3` is stored as `0.3333`; the old comparison saved the recipe and then exited 1);
  - `match` and `upload` look at every page of same-title recipes, and `upload` refuses a plan whose title now exists, which also stops a replay;
  - plans and reports are written owner-only through a temp file; a failed save names the path; `pull` creates the backup owner-only;
  - a renamed keeper gets an alias for its old name, and the hidden-recipes warning covers it;
  - `group-apply` refuses when an ingredient of a touched food appeared or vanished after `group-plan` (this closes the deferred "ingredient added after group-plan" minor);
  - `pull` keeps the servings count next to a servings label;
  - a `TANDOOR_URL` without scheme is a setup error, `::1` is exempt from the http warning, `live_smoke.py --help` works without a configured instance, and onboarding asks before choosing Tandoor as the target.
- `build_index` takes, among entries with the same normalized name (`Zwiebel`, `zwiebel`), the one the cleanup would keep (`suggest_keep`) instead of the first listed.

Not changed, on purpose:

- The PATCH cannot be made atomic with the `updated_at` check: Tandoor has no conditional update, so the check only narrows the window.
- `match` does not fetch recipe counts for same-name foods, the read-back does not compare notes or instructions, and the near-duplicate search still blocks by the first two letters: each trades cost against a rare case.
- A merge that stops after the merge but before the alias cannot be replanned; the alias has to be added by hand.
- `live_smoke.py` deletes its test entries by name (`Cctest…`, `cctest-kcal`, unit `g`); use it only on a test instance.
- `list_all` and the plan loaders assume the shapes the scripts write and Tandoor returns.

Decided later or left open:

- `scripts/sync-config-table.sh` deletes every `|` line in the Key Config Files section: outside Phase 2, check separately.
- The alias filter, `ALIAS_TYPES` and the unit-name set are repeated in several places.

## Still unchecked

- Whether the ingredient list leaves out other users' private recipes: needs a second user. The script treats a gap between `numrecipe` and the recipes reached as hidden recipes.
- Alias matching on a real import. The merge creates the alias live; resolving it in `match` is only covered by `test_alias_from_a_merge_resolves_in_the_next_match` against the fake.
- A wrong `name` in a nested `food` with `id` renames the food (from source, not tried).

## Rulings made during implementation

- The commit trailer says `Claude Sonnet 5.5`, not the plan's `Claude Opus 5.5`, because that was the model doing the work. Cost if wrong: amend the trailers.
- The branch was pushed on the owner's explicit request, although the plan says "never push".

## Deferred minors

- Plan and report files stay in `/tmp` when a session refuses `rm`.
- "Maybe" duplicate groups list one best entry per cluster and can overlap a "same" group's keep entry.
