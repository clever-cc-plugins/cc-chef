---
name: export-recipe
description: >
  Use this skill to save a recipe as a Markdown file and, if wanted, convert it to JSON-LD or a Paprika archive. Invoke when the user says "save this recipe", "export this recipe", "export as JSON-LD", "make a Paprika file", "convert my recipes for import", or "put this in my recipe folder". Takes a recipe from the conversation or one or more existing recipe files (paths). Other cc-chef skills hand their finished recipe to this one. Do NOT use it to make a new recipe (use create-recipe).
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: "[optional: path(s) to saved recipe .md files to export]"
---

@../\_shared/recipe-format.md **Read when:** writing the Markdown file, naming it by hand, or fixing a validation error

@../\_shared/export-formats.md **Read when:** the user asks which target fits their app, or the recipe has ingredient groups, ranges or other content a format cannot hold

# Export Recipe

This skill saves a recipe as a Markdown file and converts it to the configured target. It follows `../_shared/skill-contract.md` (language, address form and tone included); the steps below add only export-specific behaviour. Everything shown to the user is in the output language. Run directly, it opens with the contract's framing line (its Step 2) and ends with the contract's Step 5, tagged `[cc-chef:export-recipe]`; on a hand-off it skips both.

`$ARGUMENTS` holds zero or more paths to saved recipe files. With paths, the Markdown files already exist: skip Step 3 and validate them in Step 4. Without paths, the recipe in the conversation is the input.

When another skill hands off (`create-recipe`, `rework-recipe`), it follows this skill from Step 1 with the recipe already in the conversation and skips this skill's framing line, which the handing-off skill already showed. Steps 1 and 2 always run; Step 3 writes the Markdown from the conversation's recipe.

## Step 1: Check the tools

Run `command -v python3` once, before the first script call. Without it: continue, but validation (Step 4) and JSON-LD or Paprika conversion (Step 5) are unavailable. Say so once, in the user's language, and in Step 5 offer to write the JSON-LD by hand following `export-formats.md`. Saving the Markdown file never depends on python3.

## Step 2: Find the save folder and target

Read `Recipe target` (`files`, `json-ld` or `paprika`) and, when Step 3 will run, `Save folder` from the registered cooking preferences. If the user names a different target in the request, use that one for this run.

If `Recipe target` is `tandoor`, or the user asks for Tandoor: say that Tandoor upload arrives with phase 2, save the Markdown file (or keep the given files), and offer JSON-LD or Paprika; `export-formats.md` section 5 says which of the two Tandoor reads best.

If Step 3 will run and no `Save folder` is configured, ask once where to save. Propose either an existing recipe-like folder found in the project or a new name in the output language (`Rezepte/` for German, `recipes/` for English). Create the folder once the user agrees. Then offer to store the answer: if the user agrees and a preferences file is registered, Edit only its `Save folder` field. With no preferences file, say that `/cc-chef:chef-onboarding` can store it.

## Step 3: Write the Markdown file

Choose the path:

```bash
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" newpath "<save folder>" "<title>"
```

It prints a collision-free path, for example `Rezepte/rinderrouladen.md`. Without python3, apply the slug rules from `recipe-format.md` by hand and check that the file does not exist; add `-2`, `-3` and so on if it does. Write the recipe with the Write tool in the fixed layout of `recipe-format.md`, whatever display layout the conversation used. Never overwrite an existing Markdown file.

## Step 4: Validate

```bash
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" validate "<recipe.md>"
```

Run it for each file. Exit 0 prints `OK: <title>, <n> steps, <m> ingredients`. Exit 1 prints one `<file>:<line>: <message>` per problem. Fix those lines in the file with Edit and validate again, at most 3 rounds per file. If errors remain after the third round, keep the Markdown file saved and do not export it. For a batch, export the valid files and list the failing ones with their remaining `<file>:<line>` messages, plainly.

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

Derived files are regenerated on every export. If one already exists, replace it and tell the user it was replaced; the Markdown file itself is never touched. Check `export-formats.md` section 7 for anything the format cannot hold (ingredient groups in JSON-LD, ranges, non-English units) and tell the user in one line.

## Step 6: Report

Name each file written and each derived file replaced, with its path, and state the validation result. Mention the target's import route in one line (for example, which app reads the file) using `export-formats.md`, and do not describe formats the user did not ask about.
