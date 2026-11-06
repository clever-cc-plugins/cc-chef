---
name: export-recipe
description: >
  Save a recipe as Markdown and, if wanted, convert it to JSON-LD or Paprika or
  upload it to Tandoor. Invoke when the user says "save this recipe", "export as
  JSON-LD", "make a Paprika file" or "upload this to Tandoor". Takes a recipe from
  the conversation or saved files. Do NOT use it to make a new recipe
  (create-recipe).
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: "[optional: path(s) to saved recipe .md files to export]"
---

@../\_shared/recipe-format.md **Read when:** writing the Markdown file, naming it by hand, or fixing a validation error

@../\_shared/export-formats.md **Read when:** the user asks which target fits their app, or the recipe has step titles that act as ingredient groups, ranges or other content a format cannot hold

@../\_shared/tandoor-api.md **Read when:** the target is Tandoor, or a call to `tandoor.py` fails or prints something unexpected

# Export Recipe

This skill saves a recipe as a Markdown file and converts it to the configured target. It follows `../_shared/skill-contract.md` (language, address form and tone included); the steps below add only export-specific behaviour. Everything shown to the user is in the output language. Run directly, its reply opens with the contract's framing line (its Step 2) as the first line, and it ends with the contract's Step 5 (feedback and learnings; the tag `[cc-chef:export-recipe]` goes into learnings entries only, never into the reply). On a hand-off it skips both.

`$ARGUMENTS` holds zero or more paths to saved recipe files. With paths, the Markdown files already exist: skip Step 3 and validate them in Step 4. Without paths, the recipe in the conversation is the input.

When another skill hands off (`create-recipe`, `rework-recipe`), it follows this skill from Step 1 with the recipe already in the conversation and skips this skill's framing line, which the handing-off skill already showed. Steps 1 and 2 always run; Step 3 writes the Markdown from the conversation's recipe.

## Step 1: Check the tools

Run `command -v python3` once, before the first script call. Without it: continue, but validation (Step 4) and JSON-LD or Paprika conversion (Step 5) are unavailable. Say so once, in the user's language, and in Step 5 offer to write the JSON-LD by hand following `export-formats.md`. Saving the Markdown file never depends on python3.

## Step 2: Find the save folder and target

Read `Recipe target` (`files`, `json-ld` or `paprika`; `files` when there are no preferences) and, when Step 3 will run, `Save folder` from the registered cooking preferences. If the user names a different target in the request, use that one for this run.

If `Recipe target` is `tandoor`, or the user asks for Tandoor, check the connection:

```bash
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py" check
```

Exit 0 means Tandoor upload is available for Step 5. Exit 3 (not configured) or exit 1 (the instance answered with an error): say why in one line, in the user's language, using the script's message and pointing to the setup in `tandoor-api.md` section 1; keep the Markdown file (the file is always saved first, Tandoor or not) and offer JSON-LD or Paprika instead (`export-formats.md` section 5 says which of the two Tandoor reads best). Without `python3` (Step 1), say that Tandoor upload is unavailable and offer the same. Never ask for the token in the chat.

If Step 3 will run and no `Save folder` is configured, ask once where to save. Propose either an existing recipe-like folder found in the project or a new name in the output language (`Rezepte/` for German, `recipes/` for English). Create the folder once the user agrees. Then offer to store the answer: if the user agrees and a preferences file is registered, Edit only its `Save folder` field. With no preferences file, say that `/cc-chef:chef-onboarding` can store it.

## Step 3: Write the Markdown file

Choose the path:

```bash
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" newpath "<save folder>" "<title>"
```

`${CLAUDE_SKILL_DIR}` is the directory of this `SKILL.md`; if it stays literal or empty because another skill read this file instead of invoking it, use the directory of this file instead (the `_shared` folder is its sibling). Write the resulting absolute path into the command itself; never assign it to a shell variable first, because a command that starts with an assignment matches no permission rule and gets refused.

It prints a collision-free path, for example `Rezepte/rinderrouladen.md`. Without python3, apply the slug rules from `recipe-format.md` by hand and check that the file does not exist; add `-2`, `-3` and so on if it does. Write the recipe with the Write tool in the fixed layout of `recipe-format.md`, whatever display layout the conversation used. Never overwrite an existing Markdown recipe file.

## Step 4: Validate

```bash
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" validate "<recipe.md>"
```

Run it for each file. Exit 0 prints `OK: <title>, <n> steps, <m> ingredients`. Exit 1 prints one `<file>:<line>: <message>` for the first problem only, because the tool stops at the first error. Fix that line in the file with Edit and validate again, at most 3 rounds per file; a fix may reveal the next error. If errors remain after the third round, keep the Markdown file saved and do not export it. For a batch, export the valid files and list the failing ones with their remaining `<file>:<line>` messages, plainly.

## Step 5: Convert to the target

- `files`: nothing to convert. Offer JSON-LD or Paprika only if the user mentioned an app.
- `json-ld`: one `.json` file per recipe, sharing the Markdown file's stem and placed next to it (`<recipe.json>` is the path of `<recipe.md>` with the extension swapped).

  ```bash
  python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" jsonld "<recipe.md>" -o "<recipe.json>"
  ```

- `paprika`: for one recipe, a `.paprikarecipes` archive with the file's stem next to it. For several recipes, one archive named `cc-chef-export-` plus today's date as `YYYY-MM-DD` and `.paprikarecipes` next to the first file.

  ```bash
  python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" paprika "<recipe.md>" ... -o "<archive.paprikarecipes>"
  ```

- `tandoor`: upload through the script, in this order. The Markdown file from Steps 3 and 4 already exists. Keep the plan file in the system temp folder (for example `${TMPDIR:-/tmp}/cc-chef-plan-<stem>.json`), never in the save folder, and delete it when the run ends, whether the upload happened or not. `<tandoor>` below stands for `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py"`: write out the full command on every call, and never store it in a shell variable or put a variable assignment in front of it, because permission rules match a command by how it starts and would refuse it.
  1. `<tandoor> match "<recipe.md>" -o "<plan.json>"` reads the database and prints one `OPEN` line per ingredient that has no confident match (exact name or plural, or an existing alias).
  2. Show the open decisions in one list, in the user's language, with the suggested candidate per item (or "no similar entry"). Accept "use all suggestions" as an answer. For each item the user either picks an existing entry or agrees to create a new one; never decide for them.
  3. Run `<tandoor> resolve "<plan.json>" --kind food|unit|keyword --text "<text>" (--id <n> | --create)` once per answer.
  4. Run `<tandoor> preview "<plan.json>"` and show it in the user's language: steps with their attached ingredients, new database entries, any recipe that already has this name. The preview exits 1 and prints no code while something is open or a problem (for example a field over Tandoor's length limit) remains; fix that first.
  5. On an explicit OK, run `<tandoor> upload "<plan.json>" --confirm <code>` with the code from the preview.

  A new request or a changed answer means a new preview, and a code from an earlier preview is never reused. When the preview lists a recipe with the same name, ask whether to upload anyway (then add `--allow-duplicate`) or to update the existing recipe with `/cc-chef:rework-recipe`. If the upload stops halfway, the script names the entries it already created; a new `match` finds them as exact. If a script call fails, say what failed in one line and keep the Markdown file; do not retry a write without a fresh preview.

Derived files are regenerated on every export. If one already exists, replace it and tell the user it was replaced; the Markdown file itself is never touched. Check `export-formats.md` section 7 for anything the format cannot hold (step titles as ingredient groups in JSON-LD, ranges, non-English units) and tell the user in one line. For `json-ld`, if the recipe has notes, tell the user that the notes (originals, conversions, serving tips) are not in the JSON-LD file and stay in the Markdown file; for either format, say that `signature` and `oven` are not carried unless they appear in the step text.

## Step 6: Report

Name each file written and each derived file replaced, with its path, and state the validation result. For a Tandoor upload, give the link the script printed (`Created: <id> <url>/recipe/<id>/`) and any differences it found when reading the recipe back. Mention the target's import route in one line (for example, which app reads the file) using `export-formats.md`, and do not describe formats the user did not ask about.
