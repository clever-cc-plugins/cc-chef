# Phase 2 (Tandoor): handoff

Status on 2026-11-06: Tasks 1–10 of `2026-11-05-cc-chef-phase-2-tandoor.md` are done and committed on `feat/phase-2-tandoor`. Task 11 (live verification) is open and is the gate before merge to `main`.

## State

- Both test suites pass: `python3 -m unittest discover -s tests/tandoor -v` (83 tests) and `python3 -m unittest discover -s tests/recipe-tool -v` (42 tests), on Python 3.12 and 3.15. Python 3.9 is unverified.
- Dry runs of scenarios J–O and the smoke test (see `tests/README.md`) passed against the fake server. Scenario M reached its update only after recovering from one denied call, and was not re-run after the last text fix.
- Nothing in the code has touched a real Tandoor instance. Every API fact in `plugins/cc-chef/skills/_shared/tandoor-api.md` is still marked `from source, 2026-11-05`.

## Task 11: what to do next session

Needs the owner. Do not paste the token into the chat.

1. Set `TANDOOR_URL` and `TANDOOR_TOKEN` in the shell, start Claude Code from that shell, and make an instance backup before any write.
2. Reads only first: `check`, `GET /openapi/` (compare request shapes with `tandoor-api.md`), `foods-report`, `pull` on one real recipe.
3. Write `tests/tandoor/live_smoke.py` (opt-in; the name must not match `test_*.py`). It uploads a recipe named `cc-chef-test-<date>`, using a food that has properties, and checks:
   - a `POST` with `{id, name}` leaves the food's `name`, `plural_name` and `properties` unchanged (the riskiest assumption);
   - `PATCH` with `steps` replaces the steps and keeps image, `rating` and `private`;
   - a note-only `PATCH` on an ingredient works;
   - `?extended=1` returns `numrecipe` on a single entry;
   - replaced steps do not stay behind as orphans (record the result either way).
4. Delete the test recipe and any test foods; confirm they are gone.
5. One real merge, only through `/cc-chef:tandoor-food-cleanup`, with the owner approving a small group. Confirm in the Tandoor UI: notes moved, recipes intact, alias present, kept food's nutrition untouched.
6. Replace `from source, 2026-11-05` with `verified against <version>, <date>` for each confirmed fact in `tandoor-api.md`. For a difference: fix the code, adjust the fake server and its test, and re-run the suite.
7. Also confirm the three assumptions in `tandoor-api.md` section 4.4: `used_in_recipes` on `GET /api/ingredient/` rows as `{id, name}`, `numrecipe` on a single-entry GET with `extended=1`, and `GET /api/recipe/?query=<title>`.
8. Commit as `test: ✅ verify Tandoor support against a live instance`. Merge only after this passes.

## Rulings made during implementation

- The commit trailer says `Claude Sonnet 5.5`, not the plan's `Claude Opus 5.5`, because that was the model doing the work. Cost if wrong: amend the trailers.
- Task 11 was not run and `live_smoke.py` was not written, because both need the owner's instance. Cost if wrong: the riskiest assumption stays unchecked.
- `group-plan` assumes `/api/ingredient/` lists each ingredient's recipes in `used_in_recipes` as `{id, name}` and that `?extended=1` works on a single entry. Cost if wrong: previews lack recipe names and every food gets the hidden-recipes warning.
- The final review was a self-review plus one advisor pass, with no fresh subagent. A fresh-reviewer pass of the branch is still open.

## Deferred minors

- Plan and report files stay in `/tmp` when a session refuses `rm`.
- `group-apply` does not re-list a source's ingredients before merging, so an ingredient added after `group-plan` loses its detail on merge.
- "Maybe" duplicate groups list one best entry per cluster and can overlap a "same" group's keep entry.
- Python 3.9 is unverified.
