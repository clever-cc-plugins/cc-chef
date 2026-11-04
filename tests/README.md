# cc-chef tests

Two kinds of tests: unit tests for `recipe_tool.py`, and dry-run scenarios that drive the skills end to end in real Claude Code sessions.

## Script tests

Run from the repo root:

```bash
python3 -m unittest discover -s tests/recipe-tool -v
```

They cover parsing, validation, slugs and collision-free paths, JSON-LD and the Paprika archive. Fixtures live in `tests/recipe-tool/fixtures/`.

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

## Acceptance checklist for every produced recipe

- Passes `recipe_tool.py validate`.
- Salt in stages (in a base-plus-branch household, after the child's portion is set aside), an acid, an umami source where it fits, one named finishing touch, and times paired with visual cues (`culinary-craft.md` section 5.1).
- The chat display follows the preferences' `Recipe layout` and `Separate preparation section`.
- Hard constraints are respected: allergens from the preferences and registered guidelines, and the life-stage rules for every household member.
