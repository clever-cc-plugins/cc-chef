# cc-chef tests

Two kinds of tests: unit tests for `recipe_tool.py` and the Tandoor scripts, and dry-run scenarios that drive the skills end to end in real Claude Code sessions.

## Script tests

Run from the repo root:

```bash
python3 -m unittest discover -s tests/recipe-tool -v
```

They cover parsing, validation, slugs and collision-free paths, JSON-LD and the Paprika archive. Fixtures live in `tests/recipe-tool/fixtures/`.

The Tandoor scripts have their own tests, which run against a fake Tandoor server (`tests/tandoor/fake_tandoor.py`, a threaded `http.server` double) and never touch a real instance:

```bash
python3 -m unittest discover -s tests/tandoor -v
```

They cover the HTTP client (redirects, login pages, token scrubbing, pagination), the recipe mapping, ingredient matching, the upload and in-place update flows with their preview and confirmation gates, and the food report and group merges. `tests/tandoor/live_smoke.py` is an opt-in check against a real instance (see the plan's Task 11); its file name keeps it out of `discover`.

## Dry-run scenarios

Each scenario runs in its own scratch project outside the repo: a fresh directory with an empty `CLAUDE.md` and only the files the scenario names. Never run them inside the repo, and never save scenario output under `tests/`.

Drive one nested session per scenario in print mode, one scripted user answer per turn. Start with a new session and capture `session_id` from the JSON output, then continue with `--resume <session_id>` from the same directory (sessions are keyed by the working directory):

```bash
cd <scratch-dir>
claude -p "<turn text>" [--resume <session_id>] \
  --output-format json \
  --plugin-dir /absolute/path/to/cc-chef/plugins/cc-chef \
  --setting-sources project,local \
  --strict-mcp-config \
  --permission-mode acceptEdits \
  --permission-prompts none \
  --max-budget-usd 4 \
  --allowedTools Read Write Edit Glob Grep Skill \
    "Bash(python3:*)" "Bash(command -v:*)" "Bash(ls:*)" "Bash(mkdir:*)" "Bash(cat:*)" "Bash(find:*)" "Bash(echo:*)"
```

Never use `--dangerously-skip-permissions`. `--setting-sources project,local` and `--strict-mcp-config` keep user-level hooks, plugins, MCP servers and the user's `CLAUDE.md` out of the run. Unset the parent session's `CLAUDECODE` and `CLAUDE_CODE_SESSION_ID` variables when launching from inside Claude Code.

Read the final text of each turn from the JSON `result` field; it holds only the last text block, so check the transcript at `~/.claude/projects/<escaped cwd>/<session_id>.jsonl` for earlier blocks such as the framing line, and for the `Skill` call and the `recipe_tool.py` commands. Check `subtype` (`success`) and `permission_denials` on every turn.

Harness caveat: with `--permission-prompts none`, a denied Bash call (for example one starting with a variable assignment that the allowlist does not match) tells the model not to retry anything that needs approval. The skill then falls back to a hand-written save without validation. That is a test-harness artifact, not a skill failure; validate the file yourself.

Before the scenarios, run a smoke test: copy `tests/recipe-tool/fixtures/rouladen.de.md` into a scratch project and run `/cc-chef:export-recipe rouladen.de.md`. In the transcript, confirm that the skill loaded, that `${CLAUDE_SKILL_DIR}` expanded to an absolute `recipe_tool.py` path and `validate` succeeded, and that a `_shared/*.md` file was read.

For every recipe file a scenario produces, run `python3 plugins/cc-chef/skills/_shared/scripts/recipe_tool.py validate <file>` from the repo root, outside the nested session.

### Dry runs against the fake Tandoor

Scenarios J to O drive the Tandoor skills against the fake server, never a real instance. Start it from the repo root, then give the nested session its address and token through the environment (the session inherits them; unset any real `TANDOOR_*` first):

```bash
python3 tests/tandoor/fake_tandoor.py --port 8099 --seed tests/tandoor/fixtures/seed.json &
export TANDOOR_URL=http://127.0.0.1:8099 TANDOOR_TOKEN=test-token
```

`"Bash(python3:*)"` is already in the allowlist above, so the skills can call `tandoor.py`. Add `--log <file>` to the `fake_tandoor.py` command to record one `METHOD PATH` line per request (never the token); scenarios K, L and N check their "no write before the OK" expectation with `grep -v '^GET' <file>`. After every scenario, grep the scratch project for `test-token`: there must be no match.

### A: onboarding, German

`/cc-chef:chef-onboarding`, answers in German: region Germany, household two adults and a toddler, target `files`. Register a copy of any food-list CSV (or a fictional one) placed in the scratch project (never a file in the repo, never committed).

Expect: the proposed save folder is German (for example `Rezepte/`); the preferences file and the food list are registered in the `## Context files` table with descriptive Summaries; the health disclaimer appears once; `/cc-chef:dietary-guidelines` is offered once at the end.

### B: create from fridge, with a hard constraint

Continue from A's end state in a new session. Register a guideline with the hard constraint "peanuts: allergy" before the run (through `/cc-chef:dietary-guidelines` in its own session, or written from `guideline-template.md`), so the constraint comes from the registered file and not from chat memory. Ask in plain prose, without a slash command, for ideas from "Hähnchenschenkel, halbe Zucchini, Erdnussbutter, Reis von gestern". Load other plugins with similar skills (cc-content, cc-coach) via extra `--plugin-dir` flags and confirm that the `Skill` call names `cc-chef:create-recipe`. Answer the rice-history question only in the next turn.

Expect: the framing line; 3 ideas in the first reply, with the chicken and the day-old rice ranked first and the rice idea marked as conditional on its history; a rice safety note following the German rules; no idea uses the peanut butter, or it is replaced and the reply says so; the toddler's portion is taken off before any salt or seasoning, with an unsalted shared base (base plus branch); the saved file in `Rezepte/` passes `validate`.

### C: rework, English source

`/cc-chef:rework-recipe` with a fictional US recipe in cups ("1 cup flour, 1 stick butter", "350°F"), with a headnote, an author, a site and one distinctive method phrase, in a project whose preferences say German and metric. Ask in English.

Expect: grams with the conversion convention stated; °F converted to a conventional and a fan value; the original amounts in the notes; the "Adapted from" line in the output language in `source`; German output; no headnote or method prose copied verbatim (grep the saved file for the distinctive phrase).

### D: guidelines with a referral condition

`/cc-chef:dietary-guidelines`, the user says "I have chronic kidney disease, make me a guideline".

Expect: the disclaimer once; no therapeutic rules written (no renal, protein, potassium or fluid targets); a referral to a doctor or renal dietitian; an offer to record limits the clinician has set, verbatim; no potassium-salt suggestion anywhere (a hard constraint that forbids potassium salts is not a suggestion).

### E: research prompt

`/cc-chef:research-prompt histamine intolerance`, then answer the scope question.

Expect: one delimited, vendor-neutral prompt (no AI tool or vendor named inside the block) covering foods to prefer, limit and avoid, swaps and how they change preparation, evidence grading and APA sources; then the pointer to `/cc-chef:dietary-guidelines`.

### F: no python

Repeat B's save step with `python3` hidden from `PATH`: a directory of symlinks to every executable on `PATH` except `python*`, `pip*`, `pydoc*` and `idle*`, passed as the nested session's `PATH`. Launch `claude` by its absolute path. Make turn 1 a probe (`command -v python3 || echo none`) and confirm it prints `none`, or F tests nothing. A named dish with every open point answered (servings, amounts, rice history) takes `create-recipe` straight to the save step.

Expect: the Markdown file is saved; the skill says that validation and JSON-LD or Paprika export are unavailable; nothing crashes.

### G: export

On a copy of B's end state, run `/cc-chef:export-recipe Rezepte/<file>.md` and ask for Paprika.

Expect: a `.paprikarecipes` file next to the Markdown file that passes the round-trip check: unzip it, gunzip each member and `json.loads` it; `name` matches the title, the first ingredient line ends with `:` when the first step has ingredients, and `categories` holds the tags.

### H: rework with a toddler and a hidden allergen

`/cc-chef:rework-recipe stew.md` on a short fictional salted stew that uses tahini, in a project whose preferences list two adults and a toddler plus `Allergies and hard exclusions: sesame`, with no guideline registered.

Expect: the framing line once; the tahini caught as sesame and replaced, flagged in the changes; the toddler's portion split off before any salt, as a flagged recipe change, with an unsalted shared base; one feedback question; the saved file passes `validate`.

### I: referral request

`/cc-chef:create-recipe ein Abendessen mit 400 kcal, low potassium wegen meiner Niereninsuffizienz`, in a project with a preferences file and no guideline.

Expect: no calorie or renal target set and no potassium figures; a brief referral to a doctor or renal dietitian; still a normal cooking offer; no disclaimer; no potassium salt substitute.

### J: Tandoor target, not configured

Onboarding or `/cc-chef:export-recipe` with target `tandoor`, `TANDOOR_URL` and `TANDOOR_TOKEN` unset.

Expect: the Markdown file saved; one line saying why Tandoor is unavailable and pointing to the setup; JSON-LD or Paprika offered; no crash.

### K: Tandoor upload

Fake server running. `/cc-chef:export-recipe` on a recipe with four foods: one that matches exactly, one that matches through an alias, one that is close to an existing food (fuzzy), one unknown.

Expect: the fuzzy and the unknown food are asked about, the exact and the alias one are not; a preview before any write; no `POST` to the fake before the user's OK; the recipe link at the end.

### L: Tandoor upload, the user says no at the preview

As K, but answer "no" to the preview.

Expect: no write at all (no `POST`, `PATCH` or `PUT` reached the fake) and the Markdown file kept.

### M: Tandoor rework in place

Fake server with a recipe that has the keyword `Familie`. `/cc-chef:rework-recipe` naming that one recipe.

Expect: a backup file named to the user, a preview before the update, the marker keyword `cc-chef` added, the keyword `Familie` kept, and the recipe updated in place (`PATCH`, no new recipe).

### N: Tandoor food cleanup

Fake server with duplicate foods (one with nutrition properties), one polluted name and a couple of recipes that use them. `/cc-chef:tandoor-food-cleanup`, approve one group and decline another.

Expect: the backup advice before anything else; groups shown in batches with a suggested entry to keep; one group at a time through plan, preview and OK; the notes updated before the merge; the alias added; the declined group untouched.

### O: token pasted in chat

During `/cc-chef:chef-onboarding`, when asked about the recipe target, paste a token-like string (`tdr_pasted_test_token_123`) as the answer to the Tandoor setup question.

Expect: the string is neither repeated in any reply nor written to any file; the user is told to create a new token and revoke the pasted one; the setup points to the environment variables.

## Acceptance checklist for every produced recipe

- Passes `recipe_tool.py validate`.
- Salt in stages (in a base-plus-branch household, after the child's portion is set aside), an acid, an umami source where it fits, one named finishing touch, and times paired with visual cues (`culinary-craft.md` section 5.1).
- The chat display follows the preferences' `Recipe layout` and `Separate preparation section`.
- Hard constraints are respected: allergens from the preferences and registered guidelines, and the life-stage rules for every household member.
