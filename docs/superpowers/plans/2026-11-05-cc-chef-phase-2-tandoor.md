# cc-chef Phase 2 (Tandoor) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Connect cc-chef to a user's Tandoor instance: upload recipes as real structure, rework existing recipes in place, and clean up the food and unit database, with no write before a preview and an explicit OK.

**Architecture:** A standard-library Python CLI (`tandoor.py`) does all Tandoor HTTP and works in two phases: read commands build a JSON plan file, and write commands accept only that plan plus the digest shown in its preview. Pure modules hold the mapping, matching and cleanup logic, so a fake HTTP server can test them. Skills stay thin: they run the CLI, ask the user to decide, and show previews.

**Tech Stack:** Claude Code plugin skills, Python ≥ 3.9 standard library only (`urllib`, `http.server`, `difflib`, `unittest`), reusing `recipe_tool.py`.

**Spec:** `docs/superpowers/specs/2026-11-02-cc-chef-design.md`. Read it before any task; §n refers to its sections. Phase 2 covers §4.3 Tandoor mode, §4.6 Tandoor upload, §4.7 and §6.6 `tandoor-api.md`.

## Global Constraints

- Work on branch `feat/phase-2-tandoor`. Never push. Commit this plan file in Task 1.
- Commits: Conventional Commits with gitmoji, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Run `git status --short` before each commit. Never edit the version in `plugin.json`.
- Python ≥ 3.9, standard library only, `from __future__ import annotations` as in `recipe_tool.py`. Scripts live in `plugins/cc-chef/skills/_shared/scripts/` and are called as `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py" ...`.
- Instance URL and token come only from `TANDOOR_URL` and `TANDOOR_TOKEN`. The token is never written to a file, printed, or put in an error message (§3). No `curl`, no `wget`, no `.env` file.
- No write without a preview and explicit OK; no silently created duplicate foods (§2). In code: every write command requires `--confirm <digest>`, and a payload holds only database IDs and database names, never recipe text, for foods and units.
- Public plugin: Tandoor features activate only when both variables are set; everyone else gets file export (§3). The Markdown file is always saved first, even for Tandoor.
- `SKILL.md` and reference files are in English; everything shown to the user is in their output language. No hard-wrapped paragraphs. Invocations are namespaced (`/cc-chef:<skill>`). Learnings tag: `[cc-chef:<skill>] <observation> — <YYYY-MM-DD>`.
- Never commit `docs/owner-inputs/` or quote personal details from it. The repo is public.
- Live instance (§9): reads first; writes only on dedicated test recipes, removed afterwards; food merges only through the skill's per-group approval with the owner, after an instance backup.

## API facts this plan relies on

Read from `TandoorRecipes/recipes` (branch `develop`, latest release 2.7.2) on 2026-11-05. Task 11 confirms them on the live instance. If one differs, change the code and `tandoor-api.md`, not the test expectation alone.

- Auth is `Authorization: Bearer <token>`; scopes are `read` and `write`. Paths need the trailing slash; without it you get login HTML. Schema: `GET /openapi/`. Version: `GET /api/server-settings/current/` (public, field `version`).
- Pagination is `page` and `page_size`, with `results` and `next`. Maximum `page_size` is 200, and 100 for `/api/recipe/`. `next` can carry an internal host, so count pages and never follow it.
- `POST /api/recipe/` takes nested `steps[].ingredients[]`. A nested `food` without an `id` runs `get_or_create` on the exact name, which is the silent-duplicate path. A nested `food` with an `id` updates that food from the payload, so a wrong `name` renames it.
- `PATCH /api/recipe/<id>/` with `steps` removes steps left out of the list from the recipe and creates steps sent without `id` (`drf-writable-nested`). `keywords` works the same way.
- `Ingredient`: `amount` is one decimal, with no ranges; `no_amount` marks "to taste"; `note` ≤ 256; `original_text` ≤ 512; `is_header` marks a heading row. Limits: recipe `name` ≤ 128, `description` ≤ 512, step `name` ≤ 128, food and unit `name` ≤ 128, `source_url` ≤ 1024. `Step` also has `step_recipe` (embedded recipe) and `file`.
- Food and unit names are unique per space, and matching in `create` is case-sensitive. `?extended=1` adds `numrecipe`. Foods have `parent`, `properties`, `plural_name`, `open_data_slug`.
- `GET /api/ingredient/?food=<id>&simple=1` leaves out ingredients of other users' private recipes, and those in orphaned steps. The merge still moves them.
- `PUT /api/<food|unit>/<id>/merge/<target>/` re-points relations and deletes the source, plus its properties and conversions. Merging into a descendant returns 403.
- `Automation`: `FOOD_ALIAS`, `UNIT_ALIAS`, `KEYWORD_ALIAS` use `param_1` (alias, compared lowercased) and `param_2` (target name). They run in importers and the ingredient parser, not on `POST /api/recipe/`, so this plugin applies them itself.

## Review Focus

- The same recipe uploaded twice: a second `match` finds the existing name, the preview says so, and upload needs the user's choice. Pinned in Task 4 (`test_preview_warns_existing_recipe`).
- `zwiebel`, `Zwiebeln` and `Zwiebel ` against a database holding `Zwiebel` (plural `Zwiebeln`): case, space and plural map to the entry, a near miss stays a question, and no new food appears. Pinned in Task 3 (`test_match_case_and_plural`, `test_fuzzy_never_auto`) and Task 4 (`test_upload_sends_only_ids`).
- A wrong `TANDOOR_URL`: an HTTP-to-HTTPS redirect, a login page with status 200, a subpath with a trailing slash. A clear error, and the token never reaches another host. Pinned in Task 1 (`test_redirect_not_followed`, `test_html_response_is_error`, `test_base_url_subpath`).
- A cleanup run that dies between note migration and merge: running it again neither doubles the note nor loses the detail. Pinned in Task 7 (`test_rerun_after_failure_is_idempotent`).
- A food used in a recipe the token can't see: the note can't be migrated there, so the preview warns before the irreversible merge. Pinned in Task 7 (`test_hidden_recipes_warning`).

---

## File structure

| File                                                   | Responsibility                                                              |
| ------------------------------------------------------ | --------------------------------------------------------------------------- |
| `plugins/cc-chef/skills/_shared/scripts/tandoor.py`    | CLI: argument parsing, plan files, digests, printing. No mapping logic      |
| `.../scripts/tandoor_client.py`                        | Config from the environment, HTTP, pagination, errors, token scrubbing      |
| `.../scripts/tandoor_model.py`                         | Pure: recipe model ↔ Tandoor JSON, amounts, limits, source text, read-back  |
| `.../scripts/tandoor_match.py`                         | Pure: normalising, indexes, matching foods, units and keywords              |
| `.../scripts/tandoor_cleanup.py`                       | Pure: name splitting, duplicate groups, keep suggestion, group plans, notes |
| `plugins/cc-chef/skills/_shared/tandoor-api.md`        | Reference: endpoints, request shapes, field limits, setup (§6.6)            |
| `plugins/cc-chef/skills/tandoor-food-cleanup/SKILL.md` | New skill (§4.7)                                                            |
| `tests/tandoor/fake_tandoor.py`                        | Threaded `http.server` double, also runnable with `--port` for dry runs     |
| `tests/tandoor/test_*.py`, `tests/tandoor/fixtures/`   | Unit and CLI tests; `seed.json` holds foods, units, keywords, automations   |

Exit codes for `tandoor.py`: `0` success, `1` error (one message on stderr), `3` not configured.

---

### Task 1: HTTP client, fake server and `check`

**Files:**

- Create: `.../scripts/tandoor_client.py`, `.../scripts/tandoor.py`, `tests/tandoor/fake_tandoor.py`, `tests/tandoor/fixtures/seed.json`, `tests/tandoor/test_client.py`

**Interfaces:**

- Produces: `TandoorError(Exception)` with `.status: int | None`; `NotConfigured(TandoorError)`; `Config(url: str, token: str)` with the token excluded from `repr`; `load_config(env=os.environ) -> Config`; `Client(config, timeout=30)` with `get(path, params=None)`, `post(path, body)`, `patch(path, body)`, `put(path, body=None)`, `list_all(path, params=None, page_size=200) -> list[dict]`. Paths are relative with a trailing slash, for example `api/food/`.
- Produces: `FakeTandoor(seed: dict, token="test-token")` with `start() -> str` (base URL), `stop()`, `.requests: list[dict]` (method, path, headers, body) and `.db`. It requires the Bearer token, returns login HTML with status 200 for a path without a trailing slash, caps `page_size`, puts an unreachable host in `next`, and treats a nested food without `id` as `get_or_create`, so a test can see a silent creation.

- [ ] **Step 1: Write the failing tests** in `test_client.py`:

```python
def test_missing_env_raises_not_configured(self):
    with self.assertRaises(tc.NotConfigured): tc.load_config({"TANDOOR_URL": "http://x"})
def test_base_url_subpath(self):      # TANDOOR_URL=<fake>/recipes/ → request path /recipes/api/food/
def test_list_all_counts_pages(self): # 450 foods, page_size 200 → 3 requests, 450 items, no request to the `next` host
def test_redirect_not_followed(self): # 301 to a second FakeTandoor: raises, second server got 0 requests, message names the Location
def test_html_response_is_error(self):# 200 text/html → TandoorError with "TANDOOR_URL" in the message
def test_401_and_403_messages(self):  # 401 says token rejected; 403 on POST says write scope
def test_400_shows_field_errors(self):# {"name": ["too long"]} appears, cut to 300 characters
def test_token_never_in_output(self): # for 401, 400, connection refused: token not in str(e), repr(e), repr(config)
def test_check_cli(self):             # exit 0, prints URL and version, token absent; no env → exit 3
def test_check_warns_on_http(self):   # http:// to a non-localhost name → warning line on stderr
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -v`. Expected: FAIL (`tandoor_client` not found).
- [ ] **Step 3:** Implement the client. Disable redirects with an `HTTPRedirectHandler` subclass whose `redirect_request` returns `None`, because `urllib` otherwise copies `Authorization` to the new host. Run every error message through `str.replace(token, "***")`. Implement `tandoor.py check`: read `api/server-settings/current/` for the version, then `api/food/?page_size=1` to prove the token; print `OK: <url>, Tandoor <version>`; warn on stderr for plain `http://` unless the host is `localhost` or `127.0.0.1`, and for a major version below 2.
- [ ] **Step 4:** Run the same command. Expected: all PASS. Also run `python3 -m unittest discover -s tests/recipe-tool`: 42 tests OK.
- [ ] **Step 5: Commit** (including this plan file) — `feat: ✨ add Tandoor client and connection check`.

### Task 2: Mapping the recipe model to Tandoor

**Files:**

- Create: `.../scripts/tandoor_model.py`, `tests/tandoor/test_model.py`

**Interfaces:**

- Consumes: `recipe_tool.parse_recipe`, `Recipe`, `Ingredient`, `ingredient_line`.
- Produces: `MARKER = "cc-chef"`; `normalize(text: str) -> str` (NFC, casefold, single spaces, stripped); `parse_amount(raw: str | None) -> tuple[float | None, float | None]` (low, high); `to_payload(r: Recipe) -> dict`, in which each ingredient holds `"food": {"text": str}` and `"unit": {"text": str} | None`, and `"keywords"` is a list of `{"text": str}` that always includes `MARKER`; `finalize(payload, foods, units, keywords) -> dict`, which swaps every `{"text": t}` for `{"id", "name"}` from the resolved maps keyed by `normalize(t)` and raises `ValueError` on anything unresolved; `limit_problems(payload) -> list[str]`; `render_source(recipe: dict) -> str`; `read_back_diff(sent: dict, got: dict) -> list[str]`.

Mapping decisions: `working_time` = `prep-minutes`, `waiting_time` = `cook-minutes`, `source_url` = `source-url`. `servings` is the integer value, else `1`, with the original text in `servings_text`. Each step maps to `name`, `instruction`, `order`, `show_as_header: true`, `time: 0`. Tandoor has no field for notes, `oven`, `signature` or `source`, so a final step without ingredients carries them, joined by blank lines in the order `oven`, `signature`, `source`, notes body. Its `name` is the notes heading without `## `, else `Notes`; it sets `show_ingredients_table: false`. It is left out when all four are empty.

- [ ] **Step 1: Write the failing tests** in `test_model.py`:

```python
def test_parse_amount(self):
    for raw, want in [("½", (.5, None)), ("0,5", (.5, None)), ("1 1/2", (1.5, None)), ("1–2", (1.0, 2.0)), ("1-2", (1.0, 2.0)), (None, (None, None))]:
        self.assertEqual(tm.parse_amount(raw), want)
def test_no_amount(self):   # "Salz" → amount 0, no_amount True, unit None
def test_range_goes_to_note(self):  # "**1–2 EL** Öl, kalt" → amount 1.0, note "1–2 EL, kalt"
def test_payload_rouladen(self):    # step count = file steps + 1; ingredients stay on their steps; order 0..n; working_time 40; waiting_time 120
def test_notes_step(self):          # last step name "Hinweise", no ingredients, instruction holds oven, signature, source and notes
def test_no_notes_step_when_empty(self):
def test_marker_keyword_always_present(self):
def test_finalize_uses_database_name(self):  # text "zwiebeln" → {"id": 7, "name": "Zwiebel"}; "text" key gone
def test_finalize_refuses_unresolved(self):
def test_limit_problems(self):      # title 129, description 513, note 257, step name 129 → one problem each, naming the step or ingredient
def test_render_source(self):       # step titles, "200 g Mehl, gesiebt", is_header rows marked "[heading]", step_recipe and file marked, source_url shown
def test_read_back_diff(self):      # equal → []; a missing step or a changed food id → one line each
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -p 'test_model.py' -v`. Expected: FAIL.
- [ ] **Step 3:** Implement the module. `limit_problems` covers the limits listed under API facts. `read_back_diff` compares step count, then per step the ingredient count, food IDs, unit IDs and amounts as floats.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Commit** — `feat: ✨ map recipes to the Tandoor data model`.

### Task 3: Ingredient matching

**Files:**

- Create: `.../scripts/tandoor_match.py`, `tests/tandoor/test_match.py`

**Interfaces:**

- Consumes: `tandoor_model.normalize`.
- Produces: `CANDIDATE_CUTOFF = 0.75`; `build_index(entries: list[dict], aliases: list[dict]) -> Index`; `match(text: str, index: Index) -> dict` with `{"text", "status", "id", "name", "candidates"}`. `status` is `exact`, `alias`, `candidate` or `unmatched`; `candidates` holds at most 3 `{"id", "name", "score"}`.

Only `exact` (name or `plural_name`) and `alias` count as confident. Fuzzy results are suggestions for the user and never resolve by themselves (§8: unmatched items always go to the user). Disabled automations are ignored by the caller, which passes only active ones.

- [ ] **Step 1: Write the failing tests** in `test_match.py`:

```python
def test_match_case_and_plural(self):
    for t in ["zwiebel", "Zwiebeln", " Zwiebel "]:
        m = match(t, idx); self.assertEqual((m["status"], m["id"]), ("exact", 7))
def test_alias(self):           # FOOD_ALIAS "Tomaten, passiert" → "Passierte Tomaten": status alias, id of the target
def test_alias_target_gone(self):   # alias points to a deleted name → not "alias"; falls through to candidate or unmatched
def test_fuzzy_never_auto(self):    # "Zwiebelchen" → status "candidate", id None, candidates[0]["name"] == "Zwiebel"
def test_unmatched(self):       # "Drachenfrucht" → "unmatched", no candidates
def test_umlaut_forms(self):    # "Käse" composed and decomposed give the same result
```

- [ ] **Step 2:** Run the tests. Expected: FAIL.
- [ ] **Step 3:** Implement with `difflib.get_close_matches` over normalized names and plurals.
- [ ] **Step 4:** Run the tests. Expected: PASS.
- [ ] **Step 5: Commit** — `feat: ✨ match ingredients to the Tandoor food database`.

### Task 4: Upload flow (`match`, `resolve`, `preview`, `upload`)

**Files:**

- Modify: `.../scripts/tandoor.py`
- Create: `tests/tandoor/test_upload.py`

**Interfaces:**

- Consumes: Tasks 1–3.
- Produces the plan file, version 1: `{"version": 1, "mode": "create", "source": <path>, "base_url": <url>, "tandoor_id": null, "updated_at": null, "payload": {...}, "foods": {<normalized>: <match + "decision">}, "units": {...}, "keywords": {...}, "existing": [{"id", "name"}], "problems": [...]}`. `decision` is `use` (with `id`, `name`) or `create`; it starts as `use` for `exact` and `alias`, and as `null` otherwise. Keywords without a match start as `create`, because the preview lists them as new entries.
- Produces the commands:
  - `tandoor.py match <recipe.md> -o <plan.json>` fetches foods, units, keywords and active automations, and looks up recipes by exact title. It prints one line per open decision.
  - `tandoor.py resolve <plan.json> --kind food|unit|keyword --text <text> (--id <n> | --create)`.
  - `tandoor.py preview <plan.json>` prints the steps with their attached ingredients, new database entries, existing recipes with that name, problems, then `Confirm: <digest>`. It exits 1 when anything is open or `problems` is not empty, and prints no digest then.
  - `tandoor.py upload <plan.json> --confirm <digest> [--allow-duplicate]`.
- Produces: `plan_digest(plan: dict) -> str`, the first 8 hex digits of SHA-256 over `json.dumps(plan, sort_keys=True)`.

`upload` runs in this order: check the digest; check `base_url` against `TANDOOR_URL`; refuse when `existing` is not empty and `--allow-duplicate` is missing; create the new foods, units and keywords; `finalize`; `POST api/recipe/`; `GET` the new recipe and run `read_back_diff`. It prints `Created: <id> <url>/recipe/<id>/` and any differences. If the recipe `POST` fails, it lists the entries already created; a new `match` then finds them as `exact`.

- [ ] **Step 1: Write the failing tests** in `test_upload.py`, all through the CLI against `FakeTandoor`:

```python
def test_match_writes_plan_and_lists_open_items(self):
def test_resolve_create_and_map(self):        # both clear the open decision; an unknown --text → exit 1
def test_preview_refuses_open_items(self):    # exit 1, "Confirm:" absent
def test_preview_shows_new_entries(self):     # names the food to create and the keyword cc-chef
def test_preview_warns_existing_recipe(self): # same title in the database → listed; upload without --allow-duplicate → exit 1, no POST
def test_upload_needs_digest(self):           # wrong or missing --confirm → exit 1, zero POST/PATCH/PUT requests
def test_digest_changes_after_resolve(self):  # digest from before a resolve → refused
def test_upload_other_instance_refused(self): # plan from fake A, TANDOOR_URL of fake B → exit 1, B got no POST
def test_upload_sends_only_ids(self):         # every food and unit in the POST body has an id and the database name; db food count grew only by the approved item
def test_upload_read_back(self):              # fake drops an ingredient → exit 1, difference printed
def test_failed_post_lists_created(self):     # recipe POST 500 → created food named; a new match reports it as exact
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -p 'test_upload.py' -v`. Expected: FAIL.
- [ ] **Step 3:** Implement the commands. Keep `tandoor.py` free of mapping logic: it loads the plan, calls the modules and prints.
- [ ] **Step 4:** Run `python3 -m unittest discover -s tests/tandoor -v`. Expected: all PASS.
- [ ] **Step 5: Commit** — `feat: ✨ upload recipes to Tandoor from a confirmed plan`.

### Task 5: Reading and updating a recipe in place

**Files:**

- Modify: `.../scripts/tandoor.py`, `.../scripts/tandoor_model.py`
- Create: `tests/tandoor/test_update.py`

**Interfaces:**

- Consumes: Task 4's plan and commands; `render_source`.
- Produces:
  - `tandoor.py recipes [--query <text>] [--limit 25]` prints `<id>  <name>  [cc-chef]`, with the marker shown when the recipe has that keyword.
  - `tandoor.py pull <id> -o <backup.json>` saves the raw recipe JSON, prints `render_source`, then the two frontmatter lines `tandoor-id: <id>` and `tandoor-updated-at: <updated_at>`.
  - `match` switches to `"mode": "update"` when the recipe file's frontmatter has `tandoor-id`, and stores it with `updated_at`. In this mode `existing` stays empty.
  - `upload` in update mode sends `PATCH api/recipe/<id>/` with only `name`, `description`, `servings`, `servings_text`, `working_time`, `waiting_time`, `source_url`, `keywords`, `steps`.

Update rules: keywords are the recipe's current ones plus the file's tags plus `MARKER`, so nothing the user tagged is lost. `match` reads the live recipe. It adds a problem when `updated_at` differs from the frontmatter (edited in Tandoor since the pull), or when a step has `step_recipe` or `file`, because replacing steps would drop them. The preview adds a line with the backup advice and each step count before and after. Steps go without `id`, which replaces them (see API facts). The fields left out (`image`, `nutrition`, `properties`, `private`, `shared`) stay as they are.

- [ ] **Step 1: Write the failing tests** in `test_update.py`:

```python
def test_recipes_marks_processed(self):
def test_pull_saves_backup_and_prints_frontmatter(self):
def test_pull_unknown_id(self):                # exit 1, plain message
def test_update_patches_only_allowed_fields(self):  # PATCH body keys ⊆ the list above; no POST api/recipe/
def test_update_keeps_existing_keywords(self):
def test_update_refused_when_changed_since_pull(self):
def test_update_refused_for_embedded_recipe(self):
def test_update_refused_for_step_file(self):
def test_update_read_back(self):
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -p 'test_update.py' -v`. Expected: FAIL.
- [ ] **Step 3:** Implement, reusing `upload`'s digest, create and read-back path with one branch for `POST` or `PATCH`.
- [ ] **Step 4:** Run `python3 -m unittest discover -s tests/tandoor -v`. Expected: all PASS.
- [ ] **Step 5: Commit** — `feat: ✨ update Tandoor recipes in place`.

### Task 6: Food database report (read-only)

**Files:**

- Create: `.../scripts/tandoor_cleanup.py`, `tests/tandoor/test_cleanup_report.py`
- Modify: `.../scripts/tandoor.py`

**Interfaces:**

- Consumes: `normalize`, `Client.list_all`.
- Produces: `split_food_name(name: str, unit_names: set[str]) -> tuple[str, str | None]` (core, details); `suggest_keep(members: list[dict]) -> int`; `duplicate_groups(entries: list[dict], unit_names: set[str]) -> list[dict]`, each `{"key", "kind", "members", "keep", "confidence": "same" | "maybe"}`; `descendants(food_id: int, foods: list[dict]) -> set[int]`.
- Produces: `tandoor.py foods-report -o <report.json>`. It reads foods (`extended=1`), units (`extended=1`), conversions and aliases, and writes `{"base_url", "foods", "units", "groups", "polluted", "conversions", "aliases"}`. It prints only counts, because the data can run to thousands of entries. Groups are sorted by recipe count, highest first, with `id`s `f1`, `f2`, `u1`, ….

Rules: `split_food_name` splits at the first `, `, at a trailing `(…)`, and at a leading number plus a unit from `unit_names`, so no unit list is hard-coded. Word-based preparation such as `gehackte Zwiebel` can't be found in every language; the skill reviews names and passes those details by hand (Task 7 `--detail`). `same` means an equal core or an equal `plural_name`; `maybe` means a `difflib` ratio ≥ 0.9. `suggest_keep` prefers properties, then `open_data_slug`, then the highest `numrecipe`, then the shortest name, then the lowest ID (§4.7).

- [ ] **Step 1: Write the failing tests** in `test_cleanup_report.py`:

```python
def test_split_food_name(self):
    for name, want in [("Zwiebel, fein gehackt", ("Zwiebel", "fein gehackt")), ("Tomaten (gewürfelt)", ("Tomaten", "gewürfelt")), ("200 g Mehl", ("Mehl", "200 g")), ("Mehl", ("Mehl", None))]:
        self.assertEqual(split_food_name(name, {"g", "EL"}), want)
def test_group_same_core(self):       # "Zwiebel", "zwiebel", "Zwiebel, gehackt" → one "same" group
def test_group_plural(self):
def test_group_maybe(self):           # "Tomatenmark", "Tomatenmarkt" → "maybe"
def test_suggest_keep_prefers_properties(self):   # over a higher numrecipe
def test_descendants_tree(self):
def test_report_read_only_and_counts(self):       # no POST, PATCH or PUT; prints counts; no food names on stdout
def test_report_sorted_by_recipes(self):
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -p 'test_cleanup_report.py' -v`. Expected: FAIL.
- [ ] **Step 3:** Implement the functions and the command.
- [ ] **Step 4:** Run `python3 -m unittest discover -s tests/tandoor -v`. Expected: all PASS.
- [ ] **Step 5: Commit** — `feat: ✨ report duplicate and polluted Tandoor foods`.

### Task 7: Group plans and merges

**Files:**

- Modify: `.../scripts/tandoor_cleanup.py`, `.../scripts/tandoor.py`
- Create: `tests/tandoor/test_cleanup_apply.py`

**Interfaces:**

- Consumes: the Task 6 report; `plan_digest`.
- Produces: `merged_note(note: str | None, detail: str) -> str`, which appends with `, ` and returns the note unchanged when it already holds the detail; `build_group_plan(report, kind, keep, merge, details, ingredients, rename=None) -> dict`.
- Produces the group plan: `{"version": 1, "base_url", "kind", "keep": {...}, "sources": [<full source entries>], "ops": [...], "warnings": [...], "problems": [...]}`. Each op is one of `{"op": "note", "ingredient", "note"}`, `{"op": "merge", "source", "target"}`, `{"op": "rename", "id", "name"}`, `{"op": "alias", "name", "target"}`, `{"op": "repoint-alias", "id", "target"}`.
- Produces the commands:
  - `tandoor.py group-plan <report.json> --kind food|unit --keep <id> --merge <id>[,<id>] [--detail <id>=<text>]... -o <plan.json>`. `--merge` may be empty when `--rename <new name>` is given for a polluted food with no clean partner.
  - `tandoor.py group-preview <plan.json>` prints affected recipes, notes before and after, warnings, then `Confirm: <digest>`; it exits 1 with `problems`.
  - `tandoor.py group-apply <plan.json> --confirm <digest>`.

Plan rules (§4.7 and the API facts):

- Live state decides: `group-plan` re-reads each source, drops any that no longer exists, and fetches its ingredients with `simple=1`.
- Order is notes, then merges, then aliases, because details in a source food's name are lost on merge.
- Problems, which block the preview: `keep` is a descendant of a source; a note over 256 characters; a `--rename` target that already exists (that case is a merge).
- Warnings: a source with properties (they are deleted); conversions that will be deleted, with their count; `numrecipe` above the number of recipes reached through ingredients (hidden recipes, whose notes can't be migrated).
- Aliases: one per source, `FOOD_ALIAS` or `UNIT_ALIAS`, skipped when it exists. An existing alias whose target is a source name gets a `repoint-alias` op, since it would otherwise point at a deleted entry.
- `group-apply` checks the digest and `base_url` as `upload` does, runs the ops in order, prints each one, and stops at the first failure with exit 1, naming what was done and `Run group-plan again to continue.`

- [ ] **Step 1: Write the failing tests** in `test_cleanup_apply.py`:

```python
def test_merged_note(self):
    self.assertEqual(merged_note(None, "gehackt"), "gehackt")
    self.assertEqual(merged_note("fein", "gehackt"), "fein, gehackt")
    self.assertEqual(merged_note("fein, gehackt", "gehackt"), "fein, gehackt")
def test_ops_order(self):                 # all note ops before merge, merge before alias
def test_apply_needs_digest(self):        # wrong digest → exit 1, zero writes
def test_apply_other_instance_refused(self):
def test_notes_land_before_merge(self):   # fake's request log: PATCH ingredient precedes PUT merge
def test_merge_into_descendant_blocked(self):
def test_note_too_long_blocked(self):
def test_properties_warning(self):
def test_conversions_warning(self):
def test_hidden_recipes_warning(self):    # numrecipe 3, ingredients reach 2 recipes → warning names the gap
def test_alias_created_once(self):
def test_stale_alias_repointed(self):
def test_rename_polluted_food(self):      # "Zwiebel, gehackt" with no partner → note op, then PATCH name
def test_rename_collision_blocked(self):
def test_unit_merge_has_no_note_ops(self):
def test_stops_at_first_failure(self):    # merge 500 → exit 1, alias not attempted, done ops listed
def test_rerun_after_failure_is_idempotent(self):  # new group-plan and apply: note holds the detail once, merge done
```

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/tandoor -p 'test_cleanup_apply.py' -v`. Expected: FAIL.
- [ ] **Step 3:** Implement the plan builder and the three commands.
- [ ] **Step 4:** Run `python3 -m unittest discover -s tests/tandoor -v`. Expected: all PASS.
- [ ] **Step 5: Commit** — `feat: ✨ merge Tandoor foods from an approved group plan`.

### Task 8: Tandoor reference and export path

**Files:**

- Create: `plugins/cc-chef/skills/_shared/tandoor-api.md`
- Modify: `plugins/cc-chef/skills/export-recipe/SKILL.md`, `plugins/cc-chef/skills/chef-onboarding/SKILL.md`, `plugins/cc-chef/skills/chef-onboarding/preferences-template.md`, `plugins/cc-chef/skills/_shared/recipe-format.md`, `plugins/cc-chef/skills/_shared/export-formats.md`

**Interfaces:**

- Consumes: the commands of Tasks 1, 4 and 5.
- Produces: `Recipe target` value `tandoor`; frontmatter keys `tandoor-id` and `tandoor-updated-at`; the import target for `tandoor-api.md`, with a **Read when:** note.

- [ ] **Step 1:** Write `tandoor-api.md`: a "Use this file for" paragraph naming `export-recipe`, `rework-recipe`, `tandoor-food-cleanup` and `chef-onboarding`; setup (create a token with `read` and `write` scope in Tandoor, set both variables in the shell that starts Claude Code, restart, run `check`; keep the token out of the project and out of the chat); the CLI commands; the API facts from this plan as tables; what Tandoor can't hold and where it goes (ranges, notes step). Mark every fact `from source, 2026-11-05` until Task 11 confirms it.
- [ ] **Step 2:** Change `export-recipe`. In Step 2, replace the "arrives with phase 2" paragraph: when the target is `tandoor`, run `check`. Exit 3 or 1 means saying why, keeping the Markdown file and offering JSON-LD or Paprika. Without `python3`, say that Tandoor upload is unavailable. Add a Step 5 branch:
  1. Run `match`.
  2. Show the open decisions in one list, with the suggested candidate per item, and accept "use all suggestions".
  3. Run `resolve` for each answer.
  4. Run `preview` and show it in the user's language.
  5. On an explicit OK, run `upload --confirm`.

  A new request or a changed answer means a new preview. On a duplicate, ask whether to upload anyway, or use `/cc-chef:rework-recipe` to update the existing recipe. Add to the description: "upload to Tandoor". Step 6 reports the recipe link.

- [ ] **Step 3:** Change `chef-onboarding` Step 5 and `preferences-template.md`: add `tandoor` as a target, shown only after asking whether the user runs Tandoor. Point to the setup section, run `check`, and on failure fall back to `files` with the reason. Never ask for the token in chat; if the user pastes one, don't repeat it, don't store it, and tell them to replace it.
- [ ] **Step 4:** Add `tandoor-id` and `tandoor-updated-at` to `recipe-format.md` as optional keys written by `rework-recipe`. In `export-formats.md`, replace the phase 2 lines (sections 1 and 5) with the upload route.
- [ ] **Step 5: Verify** — `python3 tests/knowledge/check_overlap.py plugins/cc-chef/skills/_shared/tandoor-api.md 'docs/research/*.md'` exits 0; `grep -rn "phase 2" plugins/cc-chef/skills/export-recipe plugins/cc-chef/skills/chef-onboarding plugins/cc-chef/skills/_shared/export-formats.md` prints nothing; `claude plugin validate plugins/cc-chef` passes.
- [ ] **Step 6: Commit** — `feat: ✨ add Tandoor as a recipe target`.

### Task 9: Tandoor mode in `rework-recipe`

**Files:**

- Modify: `plugins/cc-chef/skills/rework-recipe/SKILL.md`

**Interfaces:**

- Consumes: `recipes`, `pull`, the frontmatter keys, and `export-recipe`'s Tandoor branch.

A separate skill isn't needed (§8): the skill gains one source and hands off as usual, because `export-recipe` already handles update mode.

- [ ] **Step 1:** Replace "Tandoor recipes as a source arrive with phase 2". Add to Step 1: the user names the recipes (ID, name or search); never guess which ones to process; `recipes` finds them, and a marker shows those already processed. Run `pull` to a backup file beside the save folder, and name the file to the user. Treat the output as the source text. A last step without ingredients holding notes goes back to the notes. Mention any `[heading]` rows and turn them into step titles.
- [ ] **Step 2:** Add to Step 6: the Tandoor `source_url` passes on as `source-url`. Add to Step 7: the frontmatter carries the two `tandoor-*` lines from `pull`. For several recipes, run each one through preview and OK on its own. Update the description with "a Tandoor recipe" and the trigger "rework my Tandoor recipe". Say that update replaces the steps in place and the backup file restores nothing by itself; it is a record for rebuilding by hand.
- [ ] **Step 3: Verify** — `grep -n "phase 2" plugins/cc-chef/skills/rework-recipe/SKILL.md` prints nothing; `claude plugin validate plugins/cc-chef` passes.
- [ ] **Step 4: Commit** — `feat: ✨ rework Tandoor recipes in place`.

### Task 10: `tandoor-food-cleanup` skill, docs and dry runs

**Files:**

- Create: `plugins/cc-chef/skills/tandoor-food-cleanup/SKILL.md`
- Modify: `tests/README.md`, `README.md`, `docs/skill-ideas.md`, `CLAUDE.md` (through the pre-commit sync)

**Interfaces:**

- Consumes: `check`, `foods-report`, `group-plan`, `group-preview`, `group-apply`.

- [ ] **Step 1:** Write the skill per §4.7 and the shared contract. `allowed-tools: Read, Write, Bash, Glob`. Steps:
  1. Run `check`; when not configured, explain the setup and stop.
  2. Before the first write, recommend an instance backup, say that merges can't be undone, and wait for a clear answer.
  3. Run `foods-report` into a file, and read it rather than printing it.
  4. Show 5 groups per batch, highest recipe count first, with the suggested keep entry and why. Review names for preparation details the script can't find.
  5. Per approved group: `group-plan`, `group-preview`, explicit OK, `group-apply --confirm`. `maybe` groups are never treated as duplicates without a word from the user.
  6. Summarise after each batch: merged, renamed, aliases, skipped, failed. Offer to stop.
  7. Finish with the contract's feedback step, tagged `[cc-chef:tandoor-food-cleanup]`.

  Add `Do NOT use it` lines for recipe upload and rework.

- [ ] **Step 2:** Add to `tests/README.md`: the script test command `python3 -m unittest discover -s tests/tandoor -v`; running `fake_tandoor.py --port <n> --seed tests/tandoor/fixtures/seed.json` with `TANDOOR_URL` and `TANDOOR_TOKEN=test-token` for dry runs, and `"Bash(python3:*)"` already in the allowlist. Add scenarios:
  - **J, not configured:** target `tandoor`, variables unset. Expect the Markdown saved, one line on why, and JSON-LD or Paprika offered.
  - **K, upload:** one exact, one alias, one fuzzy, one unknown food. Expect the fuzzy and unknown items asked about, a preview before any write, and in the fake's log no `POST` before the OK.
  - **L, user says no at the preview:** expect no write and the Markdown file kept.
  - **M, rework in place:** one named recipe. Expect a backup file, the marker keyword, and existing keywords kept.
  - **N, cleanup:** expect the backup advice first, one group at a time, notes before the merge, and no merge for a declined group.
  - **O, token in chat:** the user pastes a token during onboarding. Expect it neither repeated nor saved in any file.
- [ ] **Step 3:** Run scenarios J to O and the `tests/README.md` smoke test. Fix the skills for anything that fails. Grep each scratch project for `test-token`: no match.
- [ ] **Step 4:** Update `README.md`: skills table, a Tandoor section with setup, and the removal of "coming in phase 2". Update `docs/skill-ideas.md`: status line for phase 2.
- [ ] **Step 5: Verify** — `python3 -m unittest discover -s tests/tandoor` and `python3 -m unittest discover -s tests/recipe-tool` pass; `claude plugin validate plugins/cc-chef` passes.
- [ ] **Step 6: Commit** — `feat: ✨ add tandoor-food-cleanup skill`, then `docs: 📝 document Tandoor support`.

### Task 11: Live verification with the owner

Needs the owner: set `TANDOOR_URL` and `TANDOOR_TOKEN` in the shell, start Claude Code from it, and make an instance backup before step 4. The token stays out of the conversation.

**Files:**

- Create: `tests/tandoor/live_smoke.py` (opt-in, never part of `discover`: the file name doesn't match `test_*.py`)
- Modify: `plugins/cc-chef/skills/_shared/tandoor-api.md`, and any code a finding changes

- [ ] **Step 1: Reads.** Run `check`. Fetch `GET /openapi/` and compare the request shapes for recipe, step, ingredient, food, unit, keyword and automation with `tandoor-api.md`. Run `foods-report`, and `pull` on one real recipe. Expected: the shapes match, or the differences are listed.
- [ ] **Step 2: Writes on a test recipe.** `live_smoke.py` uploads a recipe named `cc-chef-test-<date>`, using a food that has properties, and confirms:
  - the food's `name`, `plural_name` and `properties` are unchanged after a `POST` with `{id, name}` (the riskiest assumption);
  - `PATCH` with `steps` replaces the steps, and keeps a set image, `rating` and `private`;
  - a note-only `PATCH` on an ingredient works;
  - `extended=1` returns `numrecipe`.

  Check whether replaced steps stay behind as orphans, and record the result in `tandoor-api.md`.

- [ ] **Step 3: Remove** the test recipe and any test foods with `DELETE`; confirm they are gone.
- [ ] **Step 4: One real merge,** only through `/cc-chef:tandoor-food-cleanup` with the owner approving a small group. Confirm in the Tandoor UI: notes moved, recipes intact, alias present, and the kept food's nutrition untouched.
- [ ] **Step 5:** Change `from source, 2026-11-05` to `verified against <version>, <date>` for each confirmed fact. For a difference: fix the code, adjust the fake and its test, and run `python3 -m unittest discover -s tests/tandoor`.
- [ ] **Step 6: Commit** — `test: ✅ verify Tandoor support against a live instance`.
