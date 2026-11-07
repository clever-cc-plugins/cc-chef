---
name: chef-onboarding
description: >
  Set up the cooking context the other cc-chef skills use: language, units,
  region, household, equipment, tastes and recipe save folder. Invoke when the
  user says "set up cc-chef", "onboard me for cooking" or "change my recipe save
  folder". Can be re-run to change single answers. Do NOT use it to write a
  recipe (create-recipe) or a dietary guideline (dietary-guidelines).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[optional: path to an existing food list or preferences file to register]"
---

@../\_shared/nutrition-and-guidelines.md **Read when:** writing the one-time disclaimer (section 7.3) and asking about household members' life stages (section 3)

@../\_shared/tandoor-api.md **Read when:** the user wants Tandoor as the recipe target, or the connection check fails

# Chef Onboarding

This skill sets up a cooking preferences file and registers it, and any food list the user already has, in the `## Context files` table of `CLAUDE.md`. It follows `../_shared/skill-contract.md` (language, address form and tone included); the steps below add only onboarding-specific behaviour. Step 4 of the contract (output, save or export) does not apply: this skill writes context, not a recipe.

Ask one question at a time and wait for the answer. Offer a default with every question; Enter or "default" accepts it.

## Step 1: Discover existing context

Run the discovery commands from the contract's "Finding context". For each `context/`-like folder, list its Markdown files too: a folder can hold files nobody registered yet. Keep the list of `CLAUDE.md` paths for Step 7. Show the user what is registered, grouped by location, as a table with the columns `Label | File | Summary` (or "(none)"). Until an output language is set in Step 3, everything shown to the user, including this table and its column names, is in the conversation's language.

Decide by Summary whether a cooking preferences file is already registered ("cooking preferences, units, language, household, recipe target, save folder"), and whether a food list or dietary guideline is. Look for an existing recipe folder too (a directory with recipe files, or one named like `recipes`, `Rezepte`, `Recettes`), to offer in Step 5.

## Step 2: Choose fresh onboarding or update

- No preferences file registered: fresh onboarding. Continue with Step 3.
- One registered: read it and say what it holds in one line. Ask what to change ("Which parts do you want to change? Name them, or say 'all' to go through everything."). Ask only those questions. An update changes only the answered fields: edit those sections in place, leave every other heading and value untouched, and do not re-register the file.
- `$ARGUMENTS` holds a path: if it is a food list, register it per Step 6 first; when no preferences are registered, then continue with fresh onboarding (Step 3). If it is a preferences file, register it and treat it as the registered one (and show the Step 8 disclaimer).

## Step 3: Interview, part 1: language and conventions

Ask in this order, one question each, with the default in brackets:

1. Output language for recipes and skill replies (the conversation's language). For German, use "du" by default and offer "Sie" as a one-line option within this question; do the same for other languages with a formal/informal distinction. Record `Address form` only if it differs from the default.
2. Region or country (needed for food-safety rules and unit conventions; no default; if skipped, the strictest food-safety rule applies, see `food-safety.md`).
3. Units: metric or imperial, and weights preferred over volumes or not (metric, weights preferred).
4. Default servings (2).
5. Recipe layout: `ingredients-up-front` (one ingredient list, then the steps) or `per-step` (ingredients listed with each step) (ingredients-up-front).
6. Separate "preparation" from "cooking" in the method (yes).

## Step 4: Interview, part 2: household and kitchen

1. Household members with their life stage: infant, toddler, child, pregnant, adult, older adult (one adult). Explain in one line that this switches on safety rules automatically and that no health data is needed. Do not ask for diagnoses or medical values.
2. Equipment (default: standard hob and oven; ask whether the oven has a fan).
3. Staple pantry: what is always at home (default: salt, pepper, oil, flour, sugar, common spices).
4. Likes and dislikes (taste only; default: none).
5. Optional, never pressed: allergies and hard exclusions to respect in every recipe: allergens with severity and cross-contact sensitivity, and absolute religious or ethical exclusions (default: none). Do not probe for health details, and do not name `/cc-chef:dietary-guidelines` here: Step 9 offers it once.
6. Favourite cuisines, usual time on weekdays and cooking skill (default: no preference, 30-45 minutes, intermediate).

## Step 5: Recipe target and save folder

1. Recipe target: `files` (Markdown recipe files only), `json-ld` (schema.org JSON-LD for apps that import it) or `paprika` (Paprika archive). Default `files`. Offer `tandoor` only after asking whether the user runs a Tandoor instance. If they do and want their recipes sent there, point to the setup in `../_shared/tandoor-api.md` section 1 (token with `read` and `write` scope, `TANDOOR_URL` and `TANDOOR_API_TOKEN` in the project's `.env` file) and run `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py" check`. On success, store `tandoor`. On failure, say why in one line, store `files`, and tell them they can re-run this skill once the setup works. Never ask for the token in the chat. If the user pastes one anyway, do not repeat it, do not store it anywhere, and tell them to create a new token and revoke the pasted one.
2. Save folder: the user's choice. If Step 1 found an existing recipe folder, propose it. Otherwise propose a name in the output language ("Rezepte/" for German, "recipes/" for English, and so on) and let the user pick any other path. Never use a name the user did not confirm.

## Step 6: Register an existing food list (optional)

Ask once: "Do you already have a list of foods with nutrient or suitability values that recipes should use? Give me the path, or skip." If the user skips, move on. If given a path:

- Read the file. It may be CSV or another text format. Expect semicolon separators, decimal commas, quoted headers that span several lines and a UTF-8 BOM; strip the BOM, detect the separator and decimal mark, and carry on rather than failing.
- Describe its columns in the Summary in plain words, for example "per-food iron and fibre amounts, cholesterol suitability". Name the language of the food names and whether values are per 100 g, if the file says so.
- Do not copy or change the file; register it where it is. Never read the file back to the user in full.

## Step 7: Write and register

1. Preferences file: propose `context/cooking-preferences.md` (the user may change it; if a `context/`-like folder exists elsewhere, offer that one). If the path exists and was not the registered preferences file, add `-2`, `-3`, and never overwrite. Create the file from `preferences-template.md` (next to this SKILL.md) by filling in each section with the answers, in the output language for values and English for headings. A section the user skipped gets its default; leave nothing as a placeholder. For an update, edit only the answered sections.
2. Register in the `## Context files` table of the right `CLAUDE.md` (the root, or the most specific nesting that applies; create the section if missing), with columns `Label | File | Summary`:

   ```markdown
   | Label               | File                             | Summary                                                                     |
   | ------------------- | -------------------------------- | --------------------------------------------------------------------------- |
   | Cooking preferences | `context/cooking-preferences.md` | Cooking preferences, units, language, household, recipe target, save folder |
   | Food list           | `<path>`                         | <column description from Step 6>                                            |
   ```

   Do not hand-edit the Key Config Files table; the pre-commit hook owns it. Do not add a duplicate row for a file already registered; for an update, change the Summary only if the content changed. Edit the existing `CLAUDE.md` in place: add a row to the table, or append the `## Context files` section if it is missing; never rewrite or overwrite the file (no `cat >`). If the `CLAUDE.md` does not exist yet, creating it is fine.

3. Create the save folder if it does not exist yet.

## Step 8: Disclaimer, once

Show the health disclaimer once, now, in the output language and plain words, covering the six points in the disclaimer section of the imported nutrition file. Do not repeat it in later steps or add it to recipes. Show it on fresh onboarding and when registering a pre-existing preferences file (passed via `$ARGUMENTS` or found in the project). Skip it only on a true update of a file this skill wrote earlier.

## Step 9: Offer guidelines, then feedback

Summarise in a few lines what was written and registered. Then mention once, without pressing: "If you want recipes adapted to a personal dietary guideline, `/cc-chef:dietary-guidelines` builds one. Nothing else needs it." If the user declines or ignores it, drop it.

End with the contract's Step 5 (feedback and learnings), tag `[cc-chef:chef-onboarding]`.
