# cc-chef Phase 1 (Recipe Core) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the cc-chef recipe core: repo scaffolding, the distilled knowledge base, a recipe file format with a converter script, and six skills (`chef-onboarding`, `create-recipe`, `rework-recipe`, `dietary-guidelines`, `research-prompt`, `export-recipe`), registered in the marketplace.

**Architecture:** Markdown skills (`SKILL.md`) follow one shared skill contract and load distilled research from `skills/_shared/` on demand. A recipe is written as a Markdown file in one fixed, parseable layout (steps with their own ingredients). A dependency-free Python script validates that layout and converts it to schema.org JSON-LD and Paprika archives. Tandoor (phase 2) gets its own plan once this ships; it builds on the same file format and script.

**Tech Stack:** Claude Code plugin skills (frontmatter + `@` imports with **Read when:**), Python ≥ 3.9 standard library only (`unittest`, `json`, `gzip`, `zipfile`), prettier via the repo's PostToolUse hook.

**Spec:** `docs/superpowers/specs/2026-11-02-cc-chef-design.md`. Read it before any task; §n refers to its sections.

## Global Constraints

- Repo layout, hooks, `.githooks/pre-commit`, `scripts/sync-config-table.sh`, CLAUDE.md, marketplace entry per `../marketplace/docs/cc-plugin-repo-guideline.md`.
- New Markdown files: no hard-wrapped paragraphs (one line per paragraph).
- Commits: Conventional Commits with gitmoji, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Run `git status --short` before each commit. Never push.
- `plugin.json` starts at version `0.1.0`; after that, never edit the version (the release workflow bumps it on merge to `main`).
- Never commit `docs/owner-inputs/` and never quote personal details from it (health values, family members) into committed files. The repo is public.
- `SKILL.md` files and reference files are written in English; everything a skill produces for the user is in the user's output language.
- Invocation examples are namespaced: `/cc-chef:<skill>`. Learnings tag: `[cc-chef:<skill>] <observation> — <YYYY-MM-DD>`.
- Companion files are imported as `@../_shared/<file>` with a **Read when:** note (pattern: `../cc-content/plugins/cc-content/skills/humanize/SKILL.md`); scripts are called as `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" ...`.
- Context: `## Context files` table in the user's `CLAUDE.md`; skills match context by the Summary column, never by label or filename; context enriches but never gates (§3).
- Folder names a user sees are never hard-coded: the recipe save folder comes from preferences; onboarding proposes a name in the user's output language (§4.1).
- Health wording is descriptive, never a health claim; the disclaimer appears only in `chef-onboarding` and `dietary-guidelines` (§7).
- `recipe_tool.py` must never be required for saving a recipe: without `python3`, skills still write the Markdown file and say that validation and JSON-LD/Paprika export are unavailable.

## Review Focus

- A recipe file a user edited by hand: unicode fractions (`½`), decimal commas (`0,5`), ranges (`1–2`, `1-2`), extra blank lines, an ingredient with no amount (`Salz`), an amount with no unit (`**2** Eier`). The parser accepts all of these; `validate` names the line of anything it can't parse. Pinned in Task 3 (`test_lenient_amounts`, `test_validate_reports_line`).
- Non-ASCII titles and name collisions: `Käsespätzle`, `Bœuf bourguignon` give readable slugs (`kasespatzle`, `boeuf-bourguignon`); an existing file gets `-2`, `-3`. Pinned in Task 3 (`test_slug`, `test_unique_path`).
- No `python3` on the machine: skills still save the Markdown recipe and say what is unavailable. Pinned in Task 10 (scenario F).
- A registered allergen or life-stage rule (toddler in the household) versus an idea that would break it: the idea is never offered, or is adapted and says so. Pinned in Task 10 (scenario B).
- A user who mentions a referral condition (kidney disease, insulin) while asking for guidelines: `dietary-guidelines` declines to write therapeutic rules and refers out. Pinned in Task 10 (scenario D).

---

### Task 1: Repo scaffolding and plugin manifest

**Files:**

- Create: `.claude/settings.json`, `.claude/guard-secret-files.sh`, `.claude/format-markdown.sh`, `.githooks/pre-commit`, `scripts/sync-config-table.sh`, `.claudeignore`, `CLAUDE.md`, `README.md` (skeleton: title, one-line description, install line, "Skills" heading left for Task 9), `.github/workflows/{claude-code-review,claude,release}.yml`, `plugins/cc-chef/.claude-plugin/plugin.json`
- Modify: `.gitignore` (guideline content, keep the existing `docs/owner-inputs/` lines)

**Interfaces:**

- Produces: plugin root `plugins/cc-chef/`; `plugin.json` with `name: "cc-chef"`, `description: "Create, adapt, rework and export grounded everyday recipes"`, `version: "0.1.0"`, author/homepage/repository/license per guideline.

- [ ] **Step 1:** Copy `.claude/*`, `.githooks/pre-commit`, `scripts/sync-config-table.sh`, `.github/workflows/*` from `../cc-coach/` (adjust repo names in workflow files if they contain any). Write `CLAUDE.md` from the guideline template plus a `## Don't` line "Don't commit `docs/owner-inputs/` or quote personal details from it".
- [ ] **Step 2:** Run `chmod +x .githooks/pre-commit && git config core.hooksPath .githooks`.
- [ ] **Step 3: Verify** — `claude plugin validate plugins/cc-chef` passes; `git check-ignore docs/owner-inputs/project-prompt-2.md` prints a match; `bash scripts/sync-config-table.sh && git diff --stat CLAUDE.md` shows only table rows.
- [ ] **Step 4: Commit** — `chore: 🔧 scaffold cc-chef repo per plugin guideline`.

### Task 2: Knowledge base (`_shared/` reference files)

Do this as five sub-commits, one per file; each sub-agent reads **all** research reports of its topic in `docs/research/` (§6).

**Files:**

- Create: `plugins/cc-chef/skills/_shared/culinary-craft.md` (§6.1, from `research-results-culinary-craft-by-*`)
- Create: `plugins/cc-chef/skills/_shared/cooking-from-what-is-on-hand.md` (§6.2, from `*cooking-from-what-is-on-hand-by-*`, except food safety)
- Create: `plugins/cc-chef/skills/_shared/food-safety.md` (§6.5, from the safety sections of the on-hand and nutrition reports)
- Create: `plugins/cc-chef/skills/_shared/recipe-writing.md` (§6.3, from `*recipe-writing-by-*`)
- Create: `plugins/cc-chef/skills/_shared/nutrition-and-guidelines.md` (§6.4, from `*nutrition-and-personal-guidelines-by-*`)
- Create: `plugins/cc-chef/skills/_shared/export-formats.md` (§6.6 minus Tandoor, from `*recipe-app-formats-by-*`)
- Test: `tests/knowledge/check_overlap.py`

**Interfaces:**

- Produces: the six files above, each starting with a one-paragraph "Use this file for …" header and an "Evidence notes" section at the end. Claims supported by only one report carry `(to verify)`. Where reports conflict, the file states both positions and the default the plugin uses.

- [ ] **Step 1: Write the overlap check.** `check_overlap.py <ref-file> <research-glob>` exits 1 and prints the passage if any run of 12 consecutive words (case-folded, punctuation stripped) in the reference file also appears in a research report; exits 0 otherwise. Test it by running it on a research file against itself (must exit 1).
- [ ] **Step 2:** Write each reference file in the plugin's own words, covering every item §6.n lists. Keep each file under ~600 lines; prefer tables and checklists over prose.
- [ ] **Step 3: Verify** — `python3 tests/knowledge/check_overlap.py <file> 'docs/research/*.md'` exits 0 for all six; `grep -c "to verify"` is > 0 in `export-formats.md` (ManageMeals URL-only, Recipya status are single-source).
- [ ] **Step 4: Commit** each file — `docs: 📝 add <topic> reference for cc-chef skills`.

### Task 3: Recipe file format and parser

**Files:**

- Create: `plugins/cc-chef/skills/_shared/recipe-format.md` (the layout below, with one complete German and one English example)
- Create: `plugins/cc-chef/skills/_shared/scripts/recipe_tool.py`
- Test: `tests/recipe-tool/test_recipe_tool.py`, fixtures `tests/recipe-tool/fixtures/rouladen.de.md`, `tests/recipe-tool/fixtures/shakshuka.en.md`, `tests/recipe-tool/fixtures/messy.de.md` (hand-edited style), `tests/recipe-tool/fixtures/broken.md`

**Format (decided here; implements §4.6 and §5):**

```markdown
---
cc-chef: 1
title: Rinderrouladen
language: de
servings: 4
prep-minutes: 40
cook-minutes: 120
tags: [Hauptgericht, Schmoren]
source: Adapted from <title>, <author>, <book or site>
source-url: https://…
signature: Ein Löffel Gurkenwasser in der Soße
oven: 160 °C Ober-/Unterhitze, 140 °C Umluft
---

# Rinderrouladen

<optional description paragraph(s)>

## <any heading, e.g. "Zubereitung">

### 1. Rouladen füllen

- **4 Scheiben** Rinderoberschale, je ca. 180 g
- **2 EL** Senf, mittelscharf
- Salz

<instruction paragraph(s) for this step>

### 2. …

## <any heading, e.g. "Hinweise">

<free notes: serving, sides, drinks, conversions with originals, substitutions with originals>
```

Rules: frontmatter is a flat subset (`key: value`, inline lists `[a, b]`); unknown keys are kept. A step is a `###` heading starting with `<n>. `. Ingredient lines are the bullet lines directly under a step heading: optional bold amount+unit (first token = amount: digits, decimal comma or point, unicode fraction, `a/b`, range with `-` or `–`; rest = unit, may be empty), then the food up to the first `, `, then the note. The first `##` after the last step starts the notes. Headings other than `###` steps are free text in the user's language and are never parsed for meaning. "Optional" goes in the note in the user's language (no separate flag — deviation from §5, because neither Tandoor nor schema.org has one). The ingredient overview is derived, never stored. Original amounts of converted or substituted ingredients, and the conversion convention used, go into the notes section, not into separate fields (deviation from §5, same reason).

**Interfaces:**

- Produces (Python, in `recipe_tool.py`):
  - `@dataclass Ingredient(amount: str | None, unit: str | None, food: str, note: str | None)`; `amount` keeps the original text (`"½"`, `"1–2"`).
  - `@dataclass Step(number: int, title: str, ingredients: list[Ingredient], text: str)`
  - `@dataclass Recipe(meta: dict[str, object], title: str, description: str, steps: list[Step], notes: str)`
  - `parse_recipe(text: str) -> Recipe` (raises `RecipeFormatError(line: int, message: str)`)
  - `slugify(title: str) -> str`; `unique_path(folder: Path, slug: str, ext: str = ".md") -> Path`
  - CLI: `recipe_tool.py validate <file>` → exit 0 and `OK: <title>, <n> steps, <m> ingredients`, or exit 1 and `<file>:<line>: <message>`.

- [ ] **Step 1: Write failing tests** — `test_parse_rouladen` (title, servings `4`, 2+ steps, step 1 has 3 ingredients, `Ingredient("4", "Scheiben", "Rinderoberschale", "je ca. 180 g")`, `Ingredient(None, None, "Salz", None)`); `test_lenient_amounts` (messy fixture: `½`, `0,5`, `1–2`, `**2** Eier` → unit `None`, blank lines); `test_validate_reports_line` (broken fixture: bullet with unclosed `**` → exit 1, message contains the line number); `test_unknown_frontmatter_kept`; `test_slug` (`Käsespätzle` → `kasespatzle`, `Bœuf bourguignon` → `boeuf-bourguignon`); `test_unique_path` (existing `a.md` → `a-2.md`, then `a-3.md`).
- [ ] **Step 2: Run** `python3 -m unittest discover -s tests/recipe-tool -v` — expect failures (module missing).
- [ ] **Step 3: Implement** the dataclasses, `parse_recipe`, `slugify` (NFKD + `œ→oe`, `æ→ae`, `ß→ss`, lowercase, non-alphanumerics → `-`), `unique_path`, and the `validate` CLI with `argparse`.
- [ ] **Step 4: Run** the tests — expect all PASS.
- [ ] **Step 5: Commit** — `feat: ✨ add cc-chef recipe file format and parser`.

### Task 4: JSON-LD and Paprika export

**Files:**

- Modify: `plugins/cc-chef/skills/_shared/scripts/recipe_tool.py`
- Test: `tests/recipe-tool/test_export.py`

**Interfaces:**

- Consumes: `parse_recipe`, `Recipe`, `Ingredient` (Task 3).
- Produces:
  - `ingredient_line(i: Ingredient) -> str` — `"<amount> <unit> <food>, <note>"` with empty parts and their spaces/commas dropped.
  - `to_jsonld(r: Recipe) -> dict` — `@context: "https://schema.org"`, `@type: "Recipe"`, `name`, `description`, `inLanguage`, `recipeYield` (`str(servings)`), `prepTime`/`cookTime`/`totalTime` as ISO 8601 (`PT40M`, `PT2H`, `PT2H40M`; total = prep + cook when both exist), `keywords` (tags joined with `, `), `recipeIngredient` (all steps' lines in step order), `recipeInstructions` (one `HowToStep` per step, `name` = step title, `text` = step text), `isBasedOn` = `source-url` when present; notes are not exported (schema.org has no fitting field).
  - `to_paprika(r: Recipe) -> dict` — `uid` (uuid4 upper-case), `name`, `ingredients` (per step: `"<step title>:"` heading line, then its ingredient lines; `\n`-joined), `directions` (`"<n>. <title>\n<text>"` per step, blank line between), `servings`, `prep_time`/`cook_time`/`total_time` as `"40 min"` style text, `notes`, `description`, `source`, `source_url`, `categories` (tags), `created` (`YYYY-MM-DD HH:MM:SS`), `photo_data: None`, `rating: 0`, `difficulty: ""`, `nutritional_info: ""`, `hash` (sha256 hex of the JSON without `hash`).
  - CLI: `recipe_tool.py jsonld <file> [-o out.json]`; `recipe_tool.py paprika <file>... -o out.paprikarecipes` (zip; one `<slug>.paprikarecipe` gzip-compressed JSON per recipe).

- [ ] **Step 1: Write failing tests** — `test_ingredient_line` (`Ingredient("200","g","Mehl","gesiebt")` → `"200 g Mehl, gesiebt"`; `Ingredient(None,None,"Salz",None)` → `"Salz"`; `Ingredient("2",None,"Eier",None)` → `"2 Eier"`); `test_jsonld_rouladen` (`@type`, `recipeYield == "4"`, `prepTime == "PT40M"`, `totalTime == "PT2H40M"`, `len(recipeInstructions) == steps`, `inLanguage == "de"`); `test_paprika_archive_roundtrip` (write to a temp dir, open zip, gunzip each member, `json.loads`, check `name`, first ingredient line ends with `:`, `categories == ["Hauptgericht","Schmoren"]`).
- [ ] **Step 2: Run** `python3 -m unittest discover -s tests/recipe-tool -v` — new tests FAIL.
- [ ] **Step 3: Implement** the three functions and the two CLI subcommands.
- [ ] **Step 4: Run** the tests — all PASS. Then `python3 -c 'import json,sys; json.load(open(sys.argv[1]))' out.json` on a generated file as a sanity check.
- [ ] **Step 5: Commit** — `feat: ✨ add JSON-LD and Paprika export to recipe_tool`.

### Skill tasks (5–9): common shape

Every `SKILL.md` has frontmatter `name` (= directory), `description` (when to trigger, with 4–6 quoted user phrases, and a "Do NOT use for …" line naming the neighbouring skill), `allowed-tools`, `argument-hint`; then "This skill follows `../_shared/skill-contract.md`" and only its own steps. Each skill task ends with the same verification: `claude plugin validate plugins/cc-chef` passes; `grep -n "skill-contract.md" <SKILL.md>` matches; every `@../_shared/<file>` it imports exists; no hard-wrapped paragraphs. Behaviour is checked in Task 10.

### Task 5: Skill contract and `chef-onboarding`

**Files:**

- Create: `plugins/cc-chef/skills/_shared/skill-contract.md`
- Create: `plugins/cc-chef/skills/chef-onboarding/SKILL.md`, `plugins/cc-chef/skills/chef-onboarding/preferences-template.md`

**Interfaces:**

- Produces: the contract sequence every skill references — 0 recall learnings (silent); 1 load context (preferences, guidelines, food lists, matched by Summary; never gating); 2 one-line framing ("personalised with <files>" or "running with defaults"); 3 the skill's own work; 4 output and save/export per preferences; 5 feedback and auto-stored learnings (as in `../cc-coach/plugins/cc-coach/skills/research-prompt/SKILL.md` Step 5, with tag `[cc-chef:<skill>]`). Hard constraints from registered guidelines (allergens, life-stage rules) are checked before any idea or recipe is shown. Language, address form and tone per §7: output language from preferences, else the conversation's language; German defaults to "du" unless `Address form` says otherwise; clear, conversational, honest, no hype, no flattery.
- Produces: the preferences file fields other skills read (headings in `preferences-template.md`, English keys, values in the user's language): `Output language`, `Address form`, `Region`, `Units`, `Default servings`, `Recipe layout` (`ingredients-up-front` | `per-step`), `Separate preparation section` (yes/no), `Household` (member, life stage), `Equipment`, `Staple pantry`, `Likes`, `Dislikes`, `Cuisines`, `Time and skill`, `Recipe target` (`files` | `json-ld` | `paprika`; `tandoor` reserved for phase 2), `Save folder`.
- Default preferences path proposed: `context/cooking-preferences.md` (user may change it). Registered with a Summary containing "cooking preferences, units, language, household, recipe target, save folder".

- [ ] **Step 1:** Write `skill-contract.md` with the sequence above and the context-discovery commands from `../cc-career/plugins/cc-career/skills/career-onboarding/SKILL.md` Step 1 (multiple `CLAUDE.md`, `context/`-like folders).
- [ ] **Step 2:** Write `chef-onboarding/SKILL.md` per §4.1: discover existing context; interview one question at a time with defaults; propose a save folder name in the output language or an existing folder found in the project; register an existing food list (Summary must describe its columns, e.g. "per-food iron and fibre amounts, cholesterol suitability"); state the disclaimer once (§6.4 disclaimer contents); offer `/cc-chef:dietary-guidelines` without pushing. Updating an existing preferences file changes only the answered fields.
- [ ] **Step 3: Verify** (common shape) and `grep -n "Save folder" plugins/cc-chef/skills/chef-onboarding/preferences-template.md`.
- [ ] **Step 4: Commit** — `feat: ✨ add skill contract and chef-onboarding skill`.

### Task 6: `export-recipe`

**Files:**

- Create: `plugins/cc-chef/skills/export-recipe/SKILL.md`

**Interfaces:**

- Consumes: `recipe-format.md` (Task 3), `recipe_tool.py validate|jsonld|paprika` (Tasks 3–4), preferences `Recipe target` and `Save folder` (Task 5).
- Produces: the end-of-run behaviour `create-recipe` and `rework-recipe` invoke: "save or export the recipe per `Recipe target`". Accepts a recipe from the conversation or one or more existing recipe files (argument: paths).

- [ ] **Step 1:** Write the skill per §4.6: always write the Markdown file first (save folder from preferences; if none, ask once and offer to store the answer; `unique_path` naming via `recipe_tool.py` or the same rule by hand), run `validate`, fix and re-validate on errors; then `jsonld` or `paprika` if the target says so. Output files go next to the Markdown file. Without `python3`: save the Markdown, say validation and JSON-LD/Paprika are unavailable, offer to write the JSON-LD by hand. Tandoor targets: say it arrives with phase 2.
- [ ] **Step 2: Verify** (common shape).
- [ ] **Step 3: Commit** — `feat: ✨ add export-recipe skill`.

### Task 7: `create-recipe`

**Files:**

- Create: `plugins/cc-chef/skills/create-recipe/SKILL.md`

**Interfaces:**

- Consumes: `culinary-craft.md`, `cooking-from-what-is-on-hand.md`, `food-safety.md`, `recipe-writing.md`, `nutrition-and-guidelines.md` (only when guidelines are registered or nutrition is asked), `recipe-format.md`; ends by following `export-recipe`.

- [ ] **Step 1:** Write the skill per §4.2 steps 1–5 and §7: photo → draft inventory confirmed by the user, no safety judgement from images; 3 ideas by default (up to 5 on request), each with time, on-hand items used, items to buy; named dish skips ideas; web search for grounding when a search tool is available; the full recipe passes the §6.1 review checklist before it is shown, and names its one signature touch; chat display follows `Recipe layout` and `Separate preparation section`, the saved file always uses `recipe-format.md`; nutrient values only per §7 (rounded ranges with source; a registered food list takes precedence).
- [ ] **Step 2: Verify** (common shape).
- [ ] **Step 3: Commit** — `feat: ✨ add create-recipe skill`.

### Task 8: `rework-recipe`

**Files:**

- Create: `plugins/cc-chef/skills/rework-recipe/SKILL.md`

- [ ] **Step 1:** Write the skill per §4.3 (sources: pasted text, URL, photo of a page, saved recipe file; Tandoor mode deferred to phase 2 with a one-line note): free restructuring vs. flagged recipe changes (§6.3 restructuring risk table); detect source locale before converting units; originals of converted or substituted values go into the notes; adapt to guidelines only on request, keeping the identity core or labelling a variation; attribution line in frontmatter `source`, no verbatim headnotes or method prose; ends by following `export-recipe`.
- [ ] **Step 2: Verify** (common shape).
- [ ] **Step 3: Commit** — `feat: ✨ add rework-recipe skill`.

### Task 9: `dietary-guidelines` and `research-prompt`

**Files:**

- Create: `plugins/cc-chef/skills/dietary-guidelines/SKILL.md`, `plugins/cc-chef/skills/dietary-guidelines/guideline-template.md`
- Create: `plugins/cc-chef/skills/research-prompt/SKILL.md`

**Interfaces:**

- Produces: guideline files (proposed path `context/dietary-guidelines.md`, one file with a section per household member) with sections Profile, Hard constraints, Automatic safety rules, Soft targets (each with evidence source and certainty), Preferences, Review triggers (§4.4). Summary when registered: "dietary guidelines, allergens, hard constraints, nutrition targets".

- [ ] **Step 1:** Write `dietary-guidelines` per §4.4: opt-in; disclaimer; screening questions first; referral conditions from `nutrition-and-guidelines.md` → decline therapeutic rules, record clinician-set limits verbatim as the user reports them; accept research results (a file path or pasted text) as input; base + branch for households; LDL not HDL as target; US DGA 2025–2030 divergence stated.
- [ ] **Step 2:** Write `research-prompt` by adapting `../cc-coach/plugins/cc-coach/skills/research-prompt/SKILL.md` to §4.5: topic = diet, intolerance, condition-related pattern, cultural or religious practice, or cooking constraint; the prompt asks for foods to prefer/limit/avoid, swaps and their effect on preparation, hidden sources, safety notes, evidence grading, sources in APA; closing line points to `/cc-chef:dietary-guidelines`.
- [ ] **Step 3: Verify** (common shape) for both.
- [ ] **Step 4: Commit** — `feat: ✨ add dietary-guidelines and research-prompt skills`.

### Task 10: Dry-run scenarios

**Files:**

- Create: `tests/README.md` (how to run the script tests, the scenarios below, and the acceptance checklist)

Run each scenario in a scratch project outside the repo (empty `CLAUDE.md`, plugin loaded with `claude --plugin-dir plugins/cc-chef`), follow the skill literally, and answer as the scripted user. Fix the skill and re-run until every expectation holds. All scenario data is fictional; don't use `docs/owner-inputs/` except where noted.

- [ ] **A — onboarding, German.** `/cc-chef:chef-onboarding`, answers in German, region Germany, household two adults and a toddler, target `files`. Register a copy of `docs/owner-inputs/Lebensmittelliste.csv` placed in the scratch project (never in the repo). Expect: the proposed folder is German (e.g. `Rezepte/`), the preferences file and the food list are registered with descriptive Summaries, the disclaimer appears once, and `dietary-guidelines` is offered once.
- [ ] **B — create from fridge, constraint.** Continue A, then register a guideline with a hard constraint "peanuts: allergy". Ask for ideas from "Hähnchenschenkel, halbe Zucchini, Erdnussbutter, Reis von gestern". Expect: 3 ideas, the chicken and the day-old rice ranked first, a rice safety note following German rules, no idea uses peanut butter (or it is replaced, saying so), the toddler's portion is taken off before seasoning (base + branch), the saved file in `Rezepte/` passes `validate`.
- [ ] **C — rework, English source.** `/cc-chef:rework-recipe` with a fictional US recipe in cups ("1 cup flour, 1 stick butter") in a project whose preferences say German, metric. Expect: grams with the convention stated, originals in the notes, the "Adapted from" line, German output, no prose copied verbatim.
- [ ] **D — guidelines with a referral condition.** `/cc-chef:dietary-guidelines`, user says "I have chronic kidney disease, make me a guideline". Expect: no therapeutic rules written, a referral to a doctor or dietitian, an offer to record limits the clinician has set, no potassium-salt suggestion anywhere.
- [ ] **E — research prompt.** `/cc-chef:research-prompt histamine intolerance`. Expect: one delimited, vendor-neutral prompt covering foods to prefer/limit/avoid, swaps and preparation effects, evidence grading, APA sources, then the pointer to `/cc-chef:dietary-guidelines`.
- [ ] **F — no python.** Repeat the save step of B with `python3` hidden from `PATH`. Expect: the Markdown file is saved, the skill says validation and export are unavailable, nothing crashes.
- [ ] **G — export.** `/cc-chef:export-recipe` on the file from B with target `paprika`. Expect: a `.paprikarecipes` file next to it that passes the Task 4 round-trip check.

**Acceptance checklist for every produced recipe:** passes `recipe_tool.py validate`; §6.1 checklist items B–F hold (salt in stages, an acid, an umami source where it fits, one named finishing touch, times with visual cues); the chat display follows the preferences' layout; hard constraints are respected.

- [ ] **Commit** — `test: ✅ add cc-chef dry-run scenarios`.

### Task 11: Docs and marketplace registration

**Files:**

- Modify: `README.md` (what the plugin does, skills table with `/cc-chef:<skill>` invocations, quick start: onboarding → create-recipe, health disclaimer, "Tandoor support: coming in phase 2")
- Modify: `CLAUDE.md` (run `bash scripts/sync-config-table.sh`, then write descriptions for the new rows)
- Modify: `docs/skill-ideas.md` (Status: phase 1 built; next: phase 2 plan for Tandoor)
- Modify (other repo): `../marketplace/.claude-plugin/marketplace.json` — add the entry from the guideline with `name: "cc-chef"`, `path: "plugins/cc-chef"`, description as in `plugin.json`

- [ ] **Step 1:** Write the docs.
- [ ] **Step 2: Verify** — `claude plugin validate plugins/cc-chef` and `claude plugin validate ../marketplace` pass; `python3 -m unittest discover -s tests/recipe-tool` passes.
- [ ] **Step 3: Commit** in cc-chef — `docs: 📝 document cc-chef phase 1 skills`; in marketplace (separate repo, its own `git status --short` first) — `feat: ✨ register cc-chef in the marketplace`.
