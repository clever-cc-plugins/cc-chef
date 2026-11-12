# Tandoor API reference

Use this file for everything that touches a user's Tandoor instance: `export-recipe` (upload), `create-recipe` and `rework-recipe` (food and unit names while writing, and update in place), `tandoor-food-cleanup` (food and unit merges) and `chef-onboarding` (offering Tandoor as the recipe target). It covers the one-time setup, the commands of the bundled script `tandoor.py`, the API facts the script relies on, and what Tandoor cannot hold. All HTTP goes through the script; never use `curl`, `wget`, and never read the `.env` file yourself (the script reads it) or put the token into a command line or the conversation.

Every fact below is marked `from source, 2026-11-05` until it was confirmed on a live instance; then the mark reads `verified against <version>, <date>`. If the instance behaves differently, trust the instance, fix the script, and change the fact here.

## 1. Setup

1. In Tandoor, open the user's API settings and create a token with the `read` and `write` scopes. A token with `read` only works for `check`, `lookup`, `recipes`, `pull`, `match`, `preview` and `foods-report`.
2. Put `TANDOOR_URL` (the address of the instance, with a sub-path if it has one) and `TANDOOR_API_TOKEN` as `KEY=value` lines into the `.env` file in the root of the project where the skills run, and make sure `.env` is in that project's `.gitignore`. The script reads the file from the working directory; if either variable is set in the environment, the environment is used for both and `.env` is ignored. The token stays out of the chat.
3. Run `check`. It prints `OK: <url>, Tandoor <version>` and exits 0. Exit 3 means a variable is missing, exit 1 means the instance answered with an error (the message says which).

If the user pastes a token into the conversation: do not repeat it, do not store it, and tell them to create a new one and revoke the pasted one.

## 2. Commands

Run as `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py" <command> ...`. Exit codes: `0` success, `1` error (one message on stderr), `3` not configured. Read commands change nothing. Every write command needs `--confirm <code>`, and the code is the one `preview` or `group-preview` printed for exactly that plan file; changing the plan (a `resolve`) changes the code.

| Command                                                                                                                              | What it does                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `check`                                                                                                                              | Reads the version and one food to prove URL and token                                                                                                            |
| `match <recipe.md> -o <plan.json> [--image-url <url>]` | Matches foods, units and keywords to the database, looks for recipes with the same title, writes the plan (with the image URL of a new recipe), prints one `OPEN` line per open decision |
| `resolve <plan.json> --kind food\|unit\|keyword --text <text> (--id <n> \| --create)`                                                | Settles one open decision: use an existing entry, or create a new one                                                                                            |
| `preview <plan.json>`                                                                                                                | Shows steps with attached ingredients, new entries, existing recipes with that name, then `Confirm: <code>`; exits 1 while anything is open or a problem remains |
| `upload <plan.json> --confirm <code> [--allow-duplicate]`                                                                            | Creates the new entries, then the recipe (or updates it in place), then attaches the plan's image to a new recipe, then reads it back and prints differences                                                     |
| `lookup [--food <text>...] [--unit <text>...]` | Read-only: prints, per text, the database name it would use (exact name, plural or alias), similar entries, or that it is not in the database |
| `recipes [--query <text>] [--limit 25]`                                                                                              | Lists `<id>  <name>`, with `[cc-chef]` on recipes that carry the marker keyword                                                                                  |
| `pull <id> -o <backup.json>`                                                                                                         | Saves the raw recipe (refuses to overwrite an existing file), prints it as text plus the `tandoor-id` and `tandoor-updated-at` frontmatter lines                                                         |
| `foods-report -o <report.json>`                                                                                                      | Reads all foods, units, conversions and aliases; writes duplicate groups and polluted names to the file; prints only counts                                      |
| `group-plan <report.json> --kind food\|unit --keep <id> --merge <id>[,<id>] [--detail <id>=<text>] [--rename <name>] [--plural <name>] -o <plan.json>` or `group-plan <report.json> --kind food\|unit --delete <id>[,<id>] -o <plan.json>` | Re-reads the entries from the instance and plans notes, merges, rename, plural name and aliases for one approved group, or the deletion of entries that no ingredient uses                                                        |
| `group-preview <plan.json>`                                                                                                          | Shows affected recipes with notes before and after, warnings, then `Confirm: <code>`                                                                             |
| `group-apply <plan.json> --confirm <code>`                                                                                           | Runs the operations in order and stops at the first failure                                                                                                      |

The plan is a JSON file the script writes and reads; skills never edit it by hand. A plan is bound to the instance it was made for and is refused when `TANDOOR_URL` points somewhere else.

### Writing with the database's names

`create-recipe` and `rework-recipe` do this once the ingredient list is settled and before the recipe is shown, so the upload later finds confident matches and creates no near-duplicate foods or units. It applies whenever a connection works, whatever `Recipe target` says, and it changes nothing in Tandoor.

1. Run `check`. Any failure, including exit 3, ends this procedure silently: most users have no Tandoor, and a broken connection is not the reason they asked for a recipe.
2. Run `lookup --food <each food name> --unit <each unit>` once, with the food names as written in the ingredient lines (no preparation or qualifier) and each distinct unit.
3. For `use '<name>'`, write exactly that name in the ingredient line. For `similar`, switch only when it is plainly the same food or unit in the same language; otherwise keep your own name, because `export-recipe` asks about it at upload. `not in the database` stays as written. Never change what the ingredient is, only how it is named, and keep the amount.
4. Do not mention the lookup unless a name changed in a way the user would notice; then one short line.

## 3. How the script keeps its promises

| Promise                              | How it is kept                                                                                                                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No write without a preview and an OK | Write commands refuse without the code of the current plan; `preview` prints no code while a decision is open or a problem remains                                                    |
| No silent duplicate foods            | A food, unit or keyword is sent as `{id, name}` of a database entry, never as free text; only exact name or plural matches and aliases count as confident, fuzzy hits are suggestions; a new keyword is still created without a question, and the preview lists what it resembles |
| No silent rename                     | Tandoor updates a nested entry that carries an `id` from the payload, so upload first checks every reused entry against the live name and stops if it changed                         |
| The token never leaves the instance  | Redirects are not followed, every message is scrubbed of the token, and a plan made for one instance is refused for another                                                           |
| A merge refuses a changed ingredient set | The plan records the ingredient ids of every food it touches; `group-apply` refuses when an ingredient was added or removed since, so no detail is lost on the way |
| Plan, report and backup files are private | Plans and reports are written through an owner-only temp file and replaced in one step; `pull` creates the backup owner-only and never overwrites one |
| A source image cannot reach internal hosts | The URL must be http(s) and resolve to public addresses (the connection goes to the address that was checked, again on every redirect, at most 3), the file at most 10 MB and a jpeg, png, webp or gif; the Tandoor token is never sent to the image host |
| Update mode creates new entries first | Foods, units and keywords the plan marks as new are created before the recipe is patched. If the patch fails they stay; `upload` lists them, and a new `match` finds them as exact |
| Updates cannot overwrite newer edits | The plan stores `updated_at`; update mode refuses when the recipe changed since the pull or since the plan                                                                            |

## 4. API facts the script relies on

Source: `TandoorRecipes/recipes`, branch `develop`, release 2.7.2. The status column says what `tests/tandoor/live_smoke.py` and a live merge confirmed (`verified against 2.7.2, 2026-11-06`), what the live check corrected, and what is still `from source, 2026-11-05`.

### 4.1 Access

| Fact                                                                                                                 | Status                             |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Auth is `Authorization: Bearer <token>`; scopes are `read` and `write`                                               | verified against 2.7.2, 2026-11-06 |
| Paths need the trailing slash; without it the instance answers with the login page and status 200                    | from source, 2026-11-05            |
| Schema: `GET /openapi/` (add `?format=json`). Version: `GET /api/server-settings/current/` (public, field `version`) | verified against 2.7.2, 2026-11-06 |
| Pagination: `page` and `page_size`, with `results` and `next`. Maximum `page_size` is 200 (100 for `/api/recipe/`)   | verified against 2.7.2, 2026-11-06 |
| `next` can carry an internal host: the script counts pages and never follows it                                      | from source, 2026-11-05            |

### 4.2 Recipes

| Fact                                                                                                                                                                  | Status                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `POST /api/recipe/` takes nested `steps[].ingredients[]`; every ingredient needs the key `unit` (may be `null`)                                                       | verified against 2.7.2, 2026-11-06                                             |
| A nested `food` without `id` runs get-or-create on the exact name: this is the silent-duplicate path the script avoids                                                | verified against 2.7.2, 2026-11-06                                             |
| A nested `food` with `id` and the right `name` leaves the food unchanged (`plural_name`, `description`, `properties` checked). A wrong `name` renames it              | unchanged: verified against 2.7.2, 2026-11-06; rename: from source, 2026-11-05 |
| `PATCH /api/recipe/<id>/` with `steps` replaces the steps and keeps `image`, `rating` and `private`; the replaced steps and ingredients do not stay behind as orphans | verified against 2.7.2, 2026-11-06                                             |
| `PATCH` with `steps` creates steps sent without `id`; `keywords` works the same way, so the script sends the full list                                                | from source, 2026-11-05                                                        |
| `PUT /api/recipe/<id>/image/` with a multipart file field `image` sets the recipe image; the script downloads the image itself and sends the file | verified against 2.7.2, 2026-11-12 |
| `PATCH /api/ingredient/<id>/` with only `note` changes only the note                                                                                                  | verified against 2.7.2, 2026-11-06                                             |
| `rating` is read-only: it is computed from `/api/cook-log/` entries                                                                                                   | verified against 2.7.2, 2026-11-06                                             |
| `GET /api/recipe/?query=<title>` finds recipes by name                                                                                                                | verified against 2.7.2, 2026-11-06                                             |
| Limits: recipe `name` 128, `description` 512, step `name` 128, food and unit `name` 128, ingredient `note` 256, `original_text` 512, `source_url` 1024                | from source, 2026-11-05                                                        |
| `Ingredient.amount` is one decimal, no ranges; `no_amount` marks "to taste"; `is_header` marks a heading row                                                          | from source, 2026-11-05                                                        |
| `Step` also has `step_recipe` (an embedded recipe) and `file`; replacing steps would drop both, so update mode refuses such recipes                                   | from source, 2026-11-05                                                        |

### 4.3 Foods, units and merges

| Fact                                                                                                                                                                                                                                                         | Status                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Food and unit names are unique per space; matching in `create` is case-sensitive                                                                                                                                                                             | from source, 2026-11-05                                                        |
| `numrecipe` comes only from a single entry with `?extended=1` (`GET /api/<food\|unit>/<id>/?extended=1`). The lists `/api/food/` and `/api/unit/` never carry it, with or without `extended`: the script asks for the members of duplicate groups one by one | verified against 2.7.2, 2026-11-06                                             |
| Foods have `parent`, `properties`, `plural_name`, `open_data_slug`. A nested `property_type` in `properties` needs its `name`                                                                                                                                | verified against 2.7.2, 2026-11-06                                             |
| `GET /api/ingredient/?food=<id>` lists `used_in_recipes` as `[{id, name}]` per row. With `simple=1` the field is missing, so the script does not use `simple`                                                                                                | verified against 2.7.2, 2026-11-06                                             |
| Whether the ingredient list leaves out other users' private recipes cannot be checked with a single user; the script treats a gap between `numrecipe` and the recipes reached as hidden recipes                                                              | from source, 2026-11-05                                                        |
| `PUT /api/<food\|unit>/<id>/merge/<target>/` re-points relations, deletes the source and its properties, and leaves the kept food unchanged. Notes moved first stay on the ingredients                                                                       | verified against 2.7.2, 2026-11-06                                             |
| Deleting a food on its own leaves its `Property` rows behind, and `DELETE /api/property-type/<id>/` answers 500 while rows still use the type: remove the rows first                                                                                         | verified against 2.7.2, 2026-11-06                                             |
| A food merge also deletes the source's unit conversions; merging into a descendant returns 403                                                                                                                                                               | from source, 2026-11-05                                                        |
| `Automation` types `FOOD_ALIAS`, `UNIT_ALIAS`, `KEYWORD_ALIAS` use `param_1` (alias, compared lowercased) and `param_2` (target name). The merge adds the alias                                                                                              | created: verified against 2.7.2, 2026-11-06; matching: from source, 2026-11-05 |
| Aliases run in importers and the ingredient parser, not on `POST /api/recipe/`, so the script applies them itself when matching                                                                                                                              | from source, 2026-11-05                                                        |

## 5. What Tandoor cannot hold, and where it goes

| Recipe content                       | Where it goes                                                                                    |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Amount ranges (`1–2 EL`)             | The lower bound is the amount; the full range is written at the start of the ingredient note     |
| Notes, `oven`, `signature`, `source` | A final step without ingredients, titled like the notes heading (default `Notes`), in that order |
| Servings that are not one number     | `servings` 1 and the original text in `servings_text`                                            |
| Preparation and qualifiers           | The ingredient note, never the food name                                                         |
| `prep-minutes`, `cook-minutes`       | `working_time` and `waiting_time`                                                                |
| Tags                                 | Keywords, plus the marker keyword `cc-chef` on every processed recipe                            |
| Image | A new recipe gets the source page's image only when `--image-url` is given; an update leaves it untouched. A failed image never undoes the saved recipe: `upload` prints `Image not set: <reason>` and still exits 0 |
| Rating, nutrition, sharing           | Untouched by an update; not set by an upload                                                     |
