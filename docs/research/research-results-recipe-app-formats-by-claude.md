# Recipe Export Formats for an AI Cooking Assistant: What Imports Where (checked 1 November 2026)

You can reach almost every app on the list with three outputs. Use **schema.org Recipe JSON-LD** as the internal model and the file you emit (also served as an HTML page when an app only imports from a URL). Add a **Paprika `.paprikarecipes` archive** for the closed consumer apps. Add **native API adapters for Tandoor and Mealie**, which give the best quality on your self-hosted stack. Cooklang and Meal-Master are optional extras, not core outputs.

## TL;DR

- **Canonical format: schema.org JSON-LD.** It is what Tandoor, Mealie, Nextcloud Cookbook, KitchenOwl, ManageMeals and Recipya parse (via the recipe-scrapers library or similar), what Crouton imports as a file, and what Nextcloud Cookbook stores on disk. Write it with plain-string `recipeIngredient` lines in the form "200 g Mehl, gesiebt" and `HowToSection`/`HowToStep` instructions.
- **Second format: Paprika.** The `.paprikarecipes` file (a zip of gzipped JSON) is the closest thing consumer apps have to a shared exchange format. Paprika, AnyList, Mealie, Tandoor, Cookmate, RecipeSage-adjacent tools and many commercial apps import it. It is cheap to generate from your JSON-LD model.
- **For your own servers: use the APIs directly.** Use Tandoor's `POST /api/recipe/` and Mealie's `POST /api/recipes/create/html-or-json` (or create plus PATCH) with least-privilege tokens kept in the OS keychain. Mealie 3.29+ blocks requests to private addresses during URL import by default, which you should keep on. KitchenOwl had an open SSRF report on recipe-URL import in October 2026.

## Key Findings

- **Maintenance status (checked 1 Nov 2026):**
  - Tandoor 2.7.2 was released 27 Oct 2026.\[1\]
  - Mealie v3.30.0 was released 31 Oct 2026.\[2\]
  - kitshn v2.1.4 was released 16 Sep 2026.\[3\]
  - Recipya's last stable release is v1.2.2 (Dec 2024). It has a nightly build from Sep 2026, and a Rust rewrite that its README says is "not ready for production nor to selfhost".\[4\]\[5\]\[6\]
  - ManageMeals v1.6.1 was released Mar 2026, with repository activity in Sep 2026.\[7\]
  - Nextcloud Cookbook is active: a PR adding a JSON import dialog was opened Oct 2026.\[8\]
- **The schema.org parser decides URL import quality.** Tandoor relies only on recipe-scrapers. Tandoor maintainer smilerz wrote in GitHub Discussion #3243 (2 Aug 2024): "Tandoor exclusively uses the recipe-scrapers library. That library, if ld+json is not available, will fail unless someone creates a custom scraper for that specific site." Mealie adds an AI fallback for pages its scraper cannot read; its feature docs say that "if the default recipe scraper is unable to read the recipe data from a webpage, the webpage contents will be parsed by OpenAI (v1.9.0)."
- **Ingredient parsing is still weak outside English.** Mealie maintainer michael-genson wrote in Discussion #7187 that "The NLP parser is trained on tens of thousands of recipes in English so it's pretty accurate for recipes written in English," and that the OpenAI parser "can often have better success (especially with recipes in languages other than English)." Maintainers also point non-English users to the brute-force parser. For German content, you should either send structured data through the API or put the ingredient lines in the simple order quantity, unit, food, note.
- **Ingredient sections are the most commonly lost detail.** Each format marks them differently:
  - schema.org has no grouping for ingredients; it only has `HowToSection` for instructions.
  - Paprika uses a heading line that ends with a colon.\[9\]
  - Mela uses a `#` prefix.\[10\]
  - Cooklang uses `== Section ==`.\[11\]
  - Tandoor and Mealie keep sections only through their native formats or APIs.

## 1. Schema.org Recipe (JSON-LD)

### Required and recommended properties

Google's Recipe rich-result guidelines (Search Central) list only two **required** properties: `name` and `image`.\[12\] The recommended properties are:

- `author`
- `datePublished`
- `description`
- `prepTime`, `cookTime`, `totalTime`
- `keywords`
- `recipeYield`, `recipeCategory`, `recipeCuisine`
- `nutrition.calories`
- `aggregateRating`
- `recipeIngredient`
- `recipeInstructions`
- `video`

For your purposes, the Google requirements are a floor, not a target. Recipe managers care most about `recipeIngredient` and `recipeInstructions`, which Google only "recommends".

### How each part is represented

| Element | Representation | Recommendation for your emitter |
|---|---|---|
| Ingredients | `recipeIngredient`: array of plain strings | One line per ingredient, metric first: `"200 g Weizenmehl (Type 405), gesiebt"` |
| Instructions | `recipeInstructions`: array of `HowToStep` (`text`, optional `name`, `url`, `image`), or `HowToSection` (`name`, `itemListElement: [HowToStep…]`) | Use `HowToStep` always; wrap in `HowToSection` only for real sub-recipes (Google: add sections "only if the recipe has sections")\[12\] |
| Yield | `recipeYield`: text or number (Google example: `"4 servings"`) | Emit a number **and** a text, e.g. `["4", "4 Portionen"]`, or just `"4"` for maximum parser compatibility |
| Times | ISO 8601 durations: `PT1H30M` | Always ISO 8601; never ranges (Google does not support time ranges)\[13\] |
| Nutrition | `nutrition: {"@type": "NutritionInformation", "calories": "120 calories", "proteinContent": "5 g", …}` | State values **per serving**. Tandoor makes the user choose per-serving vs per-recipe when importing from Mealie, which shows how ambiguous this is\[14\] |
| Images | `image`: URL, array of URLs, or `ImageObject` | Google recommends multiple aspect ratios (1:1, 4:3, 16:9).\[13\] For file exports, prefer an absolute HTTPS URL; base64 data URIs are not portable |
| Tags | `keywords` (comma-separated text), `recipeCategory`, `recipeCuisine` | Put course in `recipeCategory`, cuisine in `recipeCuisine`, everything else in `keywords` |
| Language | `inLanguage` (e.g. `"de"`) | Always set it. Few importers read it, but it costs nothing and helps AI-based parsers |

### Which apps import schema.org, and how

- **Tandoor:**
  - Imports schema.org from a URL via recipe-scrapers.\[15\]
  - Accepts pasted HTML or JSON-LD through the "source" import; the API endpoint `/api/recipe-from-source/` takes a `data` field.\[16\]
  - Its Nextcloud importer has historically mishandled `HowToStep` objects inside Nextcloud `recipe.json` (Tandoor issue #2428).\[17\]
- **Mealie:** Imports from a URL, and also accepts "Copy/paste structured HTML or JSON" in the UI and via `POST /api/recipes/create/html-or-json`.\[18\]\[19\]\[20\]
- **Nextcloud Cookbook:**
  - Imports from a URL.\[21\]\[22\]
  - Its API accepts schema.org JSON at `POST /api/v1/recipes`.\[23\]
  - A UI dialog for pasting schema.org JSON (PR #3430, opened Oct 2026) was in review at the time of checking.\[8\]
- **Crouton (iOS):** The App Store listing says it can "Import recipes using schema.org Recipe JSON or JSON-LD", either pasted or as individual JSON files and ZIP archives.\[24\]
- **KitchenOwl, ManageMeals, Recipya, RecipeSage, Paprika, AnyList, Mela, Recipe Keeper:** Import from a URL by scraping the page (schema.org in practice). None of them, as far as I could verify, document importing a standalone JSON-LD file.

### How robust the parsing is

recipe-scrapers (used by Tandoor and Mealie, and by KitchenOwl per its README) reads JSON-LD and microdata.\[25\] In practice it handles:

- `@graph` wrappers
- image arrays (it takes the first)
- `HowToSection`, which it flattens into steps

How fully section names are kept depends on the app. I could not run fresh tests on edge cases in this session.

Practical rule: emit a **single top-level `Recipe` object** (not inside `@graph`) with plain-string ingredients. That is the shape every parser handles.

## 2. App-by-App Import Support

"Verified" means I checked the information against official docs, release pages or the source repository on 1 Nov 2026.

| App | Version / activity (checked 1 Nov 2026) | Import paths | Notes on sections, units, languages, images, nutrition, tags |
|---|---|---|---|
| **Tandoor Recipes** | 2.7.2 (27 Oct 2026). Verified\[1\] | URL scrape (recipe-scrapers); pasted HTML/JSON-LD; AI import (photos/PDF); ~25 file importers (Default zip, Nextcloud, Mealie, Paprika, RecipeSage JSON-LD, MealMaster, RezKonv, Recipe Keeper, Plan to Eat, CopyMeThat, Cookmate `.mcb`, Cooklang `.cook`, Mela `.melarecipe`, Rezeptsuite.de XML, Gourmet, Pestle, and more); REST API\[14\] | Structured steps with their own ingredients; ingredient parser splits amount/unit/food/note (2.6.15 improved moving alternative measurements into notes); UI in German; images supported by most importers; keywords as tags; nutrition via properties/food database\[26\] |
| **Mealie** | v3.30.0 (31 Oct 2026). Verified\[2\] | URL scrape plus AI fallback; paste HTML/JSON; migrations from Tandoor, Nextcloud, Paprika, Chowdown, Plan to Eat, Recipe Keeper, Copy Me That, My Recipe Box, DVO Cook'n X3; ZIP of Mealie exports; REST API\[20\] | Ingredient sections via ingredient titles; NLP/brute/OpenAI parser; 3.29.0 added metric/imperial conversion; centilitre added to seeded units in 3.30.0; tags and categories; nutrition fields\[2\]\[27\] |
| **Recipya** | v1.2.2 stable (Dec 2024); nightly Sep 2026; Rust rewrite "not ready for production". **Flag: stagnating**\[5\]\[6\] | URL scrape; text-file import (since v1.1.0); migrations from Mealie, Tandoor, Nextcloud Cookbook; Recipe Keeper and others\[28\]\[29\] | Metric/imperial conversion; automatic nutrition calculation; JSON export (one schema.org JSON per recipe since v1.0.1)\[28\]\[29\] |
| **kitshn** | v2.1.4 (16 Sep 2026). Verified\[3\] | Client only: share links to kitshn to trigger Tandoor's URL import; uses Tandoor's API\[30\] | Inherits everything from Tandoor; no file import of its own |
| **ManageMeals** | v1.6.1 (Mar 2026); repo activity Sep 2026. Partly verified | URL import ("hundreds of supported websites"), bookmarklet, browser extension\[31\]\[32\] | No documented file import or public recipe-create API. **Flag: file import not verifiable**\[7\]\[33\] |
| **Nextcloud Cookbook** | Active (PR #3430, Oct 2026); exact latest server-app version **not verified** | URL import; recipes stored as `Recipes/<name>/recipe.json` plus `full.jpg`, so any schema.org JSON dropped into the folder can be indexed after "Rescan library"; REST API\[14\]\[22\] | schema.org fields as is; images as files; `keywords`/`recipeCategory`\[21\]\[34\] |
| **KitchenOwl** | Active (MCP endpoint, PR #1160, issue #1169 Oct 2026); exact version **not verified**\[35\]\[36\]\[37\] | URL scrape (recipe-scrapers); AI generate; REST API (JWT)\[36\]\[38\] | Ingredients are shopping items with a free-text "description" (e.g. "200 g"), so quantities are not structured; tags; images by upload\[25\]\[39\] |
| **Grocy** | Exact release **not verified** in this session | **No URL import**; REST API only (`/api/objects/recipes`, `recipes_pos`)\[40\] | Every ingredient must reference an existing product and unit; strong for stock, poor for importing recipes\[41\] |
| **Paprika 3** | Commercial, active; version not checked | URL clipping; `.paprikarecipes`/`.paprikarecipe`; YAML `.yml`; MasterCook `.mx2/.mxp/.mz2`; Meal-Master `.mmf`; Living Cookbook `.fdx/.fdxz`; Cook'n `.dvo`; MacGourmet; My CookBook `.mcb`; Pepperplate; YummySoup | Ingredient headings = lines ending in `:`; nutrition is free text; categories\[9\]\[42\] |
| **Mela** | Commercial (Apple); version not checked | URL/browser; `.melarecipe` (JSON) and `.melarecipes` (zip); scan/OCR; Paprika import (secondary source) | `#` group titles in ingredients; nutrition free text; categories (no commas allowed); base64 images\[10\]\[43\]\[44\] |
| **Crouton** | Commercial (Apple); 2026.x releases on App Store | URL; AI/photo/PDF; **schema.org JSON/JSON-LD files and ZIPs**; Crouton `.crumb` | Section suggestions; Paprika/Mela import **not verified** from official sources\[24\] |
| **Recipe Keeper** | Commercial; iOS 26 support added | URL; pasted text and text files; Recipe Gallery files; scan/PDF | Exports a zip with `recipes.html` (schema.org microdata) plus `images/`\[45\]\[46\] |
| **AnyList** | Commercial | URL/apps; copy-paste; **Paprika `.paprikarecipes` via web import page** | Ingredient headers; shopping-list centric\[47\]\[48\] |
| **RecipeSage** | Open source (AGPL), v4.x | URL; Paprika; Mela (`.melarecipes`/`.melarecipe`); Recipe Keeper zip; JSON-LD export/import; PDF/Word/OCR | Its JSON-LD export is the preferred input for Tandoor\[14\]\[49\]\[50\]\[51\] |
| **Cookmate (My CookBook)** | Commercial | MCB `.xml/.mcb`, Meal-Master, MasterCook, RezKonv, CookML, Living Cookbook, Paprika `.paprikarecipes`, Recipe Keeper zip, CSV, TXT | Very broad legacy coverage, including German RezKonv/CookML\[52\] |
| **Plan to Eat** | Commercial | URL; bulk import from other programs (e.g. Recipe Keeper `.html`); PDF/DOCX; Paprika (secondary source) | —\[44\]\[53\] |
| **CookBook (cookbookmanager.com)** | Commercial | Self-service CSV template or `.cookbook` zip (≤250 recipes); other formats imported by staff via email | —\[54\] |
| **Whisk/Samsung Food, Pestle, ReciMe, Copy Me That** | **Not verified** in this session | URL import is standard; Pestle and CopyMeThat exports are importable by Tandoor/Mealie | Treat as URL/paste-only targets |

## 3. Open and Legacy Interchange Formats

- **Cooklang (`.cook`):**
  - Structure: plain text with `@ingredient{qty%unit}`, `#cookware{}`, `~timer{25%minutes}`, YAML front matter, and `== Section ==` headings.\[11\]\[55\]
  - Tooling: the official Rust parser is cooklang-rs (crate `cooklang` 0.18.6), which handles scaling, unit conversion and aisle configuration. There are also CookCLI, mobile apps, a playground, and parsers for PHP, .NET and Elixir. cooklang-import (0.9.9) converts URLs and images to Cooklang.\[56\]\[57\]\[58\]\[59\]\[60\]\[61\]
  - Adoption: Tandoor imports single `.cook` files without images or zips.\[14\] Mealie, Paprika and the commercial apps do not import it.
  - Verdict: good for a git-friendly personal archive, poor for reach.
- **Paprika (`.paprikarecipes`):**
  - Structure: a ZIP containing one gzip-compressed JSON file per recipe (`.paprikarecipe`).\[14\]\[42\]\[62\]\[63\]
  - Fields: `uid`, `name`, `ingredients` (newline-separated), `directions`, `servings`, `prep_time`, `cook_time`, `total_time`, `notes`, `description`, `nutritional_info`, `source`, `source_url`, `categories`, `rating`, `difficulty`, `photo_data` (base64 JPEG), `image_url`, `photo_hash`, `created`.\[62\]\[63\]\[64\]
  - Paprika also imports a simpler documented **YAML** format.\[42\]\[65\]
  - Importers: Paprika, AnyList, Mealie, Tandoor, Cookmate, Vanilla Cookbook, RecipeSage, Plan to Eat (secondary) and many smaller apps.\[47\]\[50\]\[52\]\[66\]\[67\]
- **Mela (`.melarecipe` / `.melarecipes`):**
  - Officially documented JSON with fields `id` (must not be empty), `title`, `text`, `images` (base64 array), `categories`, `yield`, `prepTime`, `cookTime`, `totalTime`, `ingredients` (`\n`-separated, `#` group titles), `instructions`, `notes`, `nutrition`, `link`. The `.melarecipes` file is a zip of these.\[10\]
  - Importers: Mela, Tandoor (single files only), RecipeSage.\[14\]\[49\]
- **MasterCook (`.mxp` text, `.mx2` XML, `.mz2`) and Meal-Master (`.mmf`):**
  - Legacy text and XML formats with fixed-column ingredient lines (quantity, unit, ingredient).
  - Imported by Paprika, Cookmate and Tandoor (Meal-Master only, one-column ingredients only).\[14\]\[42\]\[52\]
  - Useful only for legacy desktop users.
- **RezKonv / CookML:** German legacy formats. Tandoor imports RezKonv; Cookmate imports both.\[14\]\[52\] Relevant for German users moving from older Windows tools.
- **RecipeML, Open Recipe Format:** **I found no current importer in the apps above during this session.** Treat both as dormant; do not emit them.
- **App-native archives:**
  - Tandoor Default: a zip of numbered zips, each with `recipe.json` plus an image. Importing must use the zip as is, not the extracted JSON.\[14\]\[66\]
  - Mealie: a backup zip (`recipes/<dir>/*.json` plus images). Tandoor needs the full backup, not the data-management export.\[14\]\[66\]
  - Nextcloud Cookbook: `Recipes/<Recipe>/recipe.json` plus `full.jpg`.\[14\]\[34\]
  - RecipeSage: JSON-LD export.\[14\]
  - Recipe Keeper: `recipes.html` plus `images/`.\[46\]

## 4. Ingredient Parsing

**How the apps do it:**

- **Tandoor:** A rule-based parser splits each line into amount, unit, food and note, and supports fractions and decimals. Since 2.6.15 it moves alternative measurements, such as a parenthetical "(1 cup)", into the note.\[26\] It is exposed as `/api/ingredient-parser/`.\[68\]
- **Mealie** offers three parsers:
  - The **NLP parser** uses the ingredient-parser-nlp CRF model, trained in English.
  - The **brute-force parser** is rule-based; maintainers say non-English users "have found [it] works quite well".\[69\]
  - The **OpenAI-compatible AI parser** keeps the source language and can be given custom prompt instructions, e.g. "use metric units".\[70\]
- **ingredient-parser-nlp:** Python library, version 2.9.1, a sequence-labelling CRF model. Its GitHub README (strangetom/ingredient-parser) reports "Sentence-level results: Accuracy: 94.24%" and "Word-level results: Accuracy 97.73%" on a 25% test split, and its PyPI page says "A data set of 75,000 example sentences is used to train and evaluate the model"; it is unclear which release these README figures describe, so check them against 2.9.1. All training data is English, and there is no German model.

**German, fractions and units in practice:**

- German unit words (EL, TL, Prise, Bund, Becher, Pck.) and decimal commas ("1,5 kg") are where English-trained models fail.
- Rule-based parsers do better if the unit appears in the app's unit table. In Tandoor and Mealie you can add units and aliases.
- Unicode fractions (½) and ASCII fractions (1/2) are generally supported. Ranges ("2–3") are inconsistently handled.

**Conventions that maximise correct parsing:**

1. Order each line as `quantity unit food, note`, e.g. `200 g Mehl, gesiebt`.
2. Use metric units with standard abbreviations (g, kg, ml, l, EL, TL). Put a space between number and unit.
3. Use **decimal points or ASCII fractions** in data meant for parsers (`1.5`, `1/2`). Show decimal commas in the human-readable text only.
4. Do not put quantities in parentheses. Put alternatives in the note after a comma.
5. Write ranges as the lower value plus a note ("2 Eier, 2–3 je nach Größe"), or as an ASCII hyphen.
6. Keep one ingredient per line. Write section headers as separate lines in the target format's syntax.
7. Best option for Tandoor and Mealie: skip parsing entirely and send structured `amount`/`unit`/`food`/`note` through the API.

## 5. API-Based Import for Self-Hosted Apps

| App | Create endpoint | Auth | Payload essentials | Images |
|---|---|---|---|---|
| **Tandoor 2.x** | `POST /api/recipe/` (trailing slash mandatory; without it you get the login HTML). Parse-only: `POST /api/recipe-from-source/` (`url` or `data`) returns parsed JSON, not saved\[16\]\[71\] | `Authorization: Bearer tda_…`; token scope **read** or **write** (Settings → API)\[72\]\[73\] | `name`, `servings`, `steps[]` each with `instruction` and `ingredients[]` of `{food:{name}, unit:{name}, amount, note, is_header}`; nested food/unit without id are created anew, so look them up first to avoid duplicates\[74\] | `PUT /api/recipe/{id}/image/` multipart field `image` (or `image_url`)\[75\]\[76\] |
| **Mealie v3** | `POST /api/recipes/create/html-or-json` (`data` = JSON-LD string) for one-shot import; or `POST /api/recipes` (`{"name"}` → slug), then `PATCH /api/recipes/{slug}`; `POST /api/recipes/create/url`\[19\] | Long-lived API token (`/user/profile/api-tokens`), `Authorization: Bearer`; token inherits the user's permissions\[77\] | `recipeIngredient[]` (`note`/`display` or `quantity`/`unit`/`food`), `recipeInstructions[{text}]` | `PUT /api/recipes/{slug}/image` multipart (`image`, `extension`)\[78\] |
| **Nextcloud Cookbook** | `POST /index.php/apps/cookbook/api/v1/recipes` (schema.org JSON); `POST …/api/v1/import` (URL)\[23\]\[79\] | HTTP Basic with a Nextcloud **app password** (needs filesystem access)\[79\] | schema.org `Recipe`; `name` required | `image` URL in JSON |
| **KitchenOwl** | `POST /api/household/{id}/recipe` (body from community clients; official docs cover only auth) | JWT; long-lived token via `POST /api/auth/llt`, user-wide, never expires until revoked\[80\]\[81\] | `name`, `description`, `time`, `yields`, `items[{name, description}]`, `tags[]`\[82\] | separate upload endpoint |
| **Grocy** | `POST /api/objects/recipes`, then `POST /api/objects/recipes_pos` per ingredient\[40\]\[41\] | `GROCY-API-KEY` header\[83\] | `recipes_pos` needs existing `product_id` and `qu_id`; Grocy issue #1528 reports that posting 1 g of sugar to `recipes_pos` "results in 1Kg of Sugar being added to the recipe" | `PUT /api/files/recipepictures/{b64 name}` (unverified) |
| **Recipya** | No documented public create API found. **Flag** | — | — | — |

Some payload details in this table come from community clients or MCP servers rather than official docs. Check them against each instance's own OpenAPI page (`/docs` on Mealie; Tandoor's built-in API browser) before you ship.

**Security for a local tool that holds tokens:**

- **Least privilege:**
  - Tandoor tokens support read and write scopes; issue a write token only for the importer.
  - Mealie and KitchenOwl tokens carry the full user's rights, and KitchenOwl long-lived tokens never expire.\[77\]\[80\] Create a **dedicated low-privilege "importer" user** in a separate household or group where possible.\[84\]
  - Grocy API keys are all-powerful.
- **Storage:** Use the OS keychain (macOS Keychain, Windows Credential Manager, Secret Service/libsecret on Linux), never plaintext config. Redact tokens from logs and from LLM context.
- **Transport:** HTTPS only, even on the LAN, with certificate pinning or your own CA. Nextcloud Basic auth sends credentials on every request.
- **Rotation:** Use one token per device. Rotate on a schedule and immediately on suspected leak; Mealie, Tandoor and KitchenOwl all support revoking tokens.
- **SSRF:**
  - Server-side URL import lets anyone who can create recipes make your server fetch arbitrary URLs.
  - Mealie (3.29.0+) blocks private addresses by default; `HTTP_ALLOW_LIST`/`HTTP_DISALLOW_LIST` tune this.\[27\]\[85\]
  - KitchenOwl issue #1169 (Oct 2026) reports that recipe scraping bypasses its hardened HTTP client.\[37\]
  - Tandoor's `image_url` and URL import have the same exposure.
  - Prefer sending **content** (JSON-LD, structured payloads, uploaded image bytes) over sending URLs for the server to fetch.
- **Patch cadence:** Tandoor 2.6.12 fixed advisory GHSA-wjf3-fq5w-7j7w (CVE-2026-61726, rated High, CVSS 3.1 score 8.1, affecting versions up to 2.6.11, published 30 Jun 2026), titled "Private recipe authorization bypass via /api/step/ - read and modify another Space member's private recipe content". KitchenOwl 0.7.10 fixed a cross-user recipe read. Keep servers current.

## 6. Recommendation

### Coverage matrix

Key: ✅ supported, 🟡 partial or indirect, ❌ none, ? not verified.

| App | schema.org JSON-LD file/paste | schema.org via hosted URL/HTML | Paprika | Cooklang | Plain text paste | MasterCook / Meal-Master | Native API |
|---|---|---|---|---|---|---|---|
| Tandoor | ✅ (paste/API) | ✅ | ✅ | 🟡 (single file) | 🟡 (AI import) | 🟡 (MMF) | ✅ |
| Mealie | ✅ | ✅ | ✅ | ❌ | 🟡 (AI) | ❌ | ✅ |
| Recipya | ? | ✅ | ? | ❌ | ✅ (text files) | ? | ❌ |
| kitshn | via Tandoor | ✅ (share link) | via Tandoor | via Tandoor | ❌ | via Tandoor | via Tandoor |
| ManageMeals | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ? |
| Nextcloud Cookbook | ✅ (API/folder; UI PR pending) | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| KitchenOwl | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Grocy | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Paprika | ❌ | ✅ | ✅ | ❌ | 🟡 | ✅ | ❌ |
| Mela | ❌ | ✅ | 🟡 | ❌ | 🟡 (scan) | ❌ | ❌ |
| Crouton | ✅ | ✅ | ? | ❌ | 🟡 | ❌ | ❌ |
| Recipe Keeper | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| AnyList | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| RecipeSage | ✅ (JSON-LD) | ✅ | ✅ | ❌ | 🟡 | ? | ? |
| Cookmate | ❌ | ✅ | ✅ | ❌ | ✅ (TXT) | ✅ | ❌ |

### What to build

1. **Internal model: schema.org JSON-LD**, extended privately with structured ingredients (`amount`, `unit`, `food`, `note`, `section`) so adapters do not have to parse their own output. Emit a clean `.json` file and an `.html` page with the JSON-LD embedded. A small local or LAN web server serving that page makes every URL-scraping app (ManageMeals, KitchenOwl, AnyList, Mela, Recipe Keeper, Paprika) a target.
2. **Paprika `.paprikarecipes` exporter.** Encode ingredient sections as "Teig:" heading lines and embed the photo as `photo_data`. This reaches Paprika, AnyList, Cookmate and RecipeSage, and works as a bulk path into Mealie and Tandoor.
3. **Native API adapters for Tandoor and Mealie**, the only route that keeps structured German units, ingredient sections, step-ingredient links and images without parsing. Add Nextcloud Cookbook (trivial, since it accepts schema.org JSON) as a third adapter. KitchenOwl and Grocy are worth adding only if you use them.
4. **Optional:** a `.melarecipe` writer (simple documented JSON) for Apple users, and Cooklang for a git-versioned archive. Skip MasterCook, Meal-Master, RecipeML and Open Recipe Format.

### Trade-offs

- **Ingredient sections:** Kept by native APIs, Paprika (colon headings), Mela (`#`) and Cooklang. **Lost** in schema.org `recipeIngredient`.
- **Units and quantities:** Structured only through APIs. Every file format falls back to strings that each app re-parses with its own parser, which handles German content unevenly.
- **Images:** Embedded in Paprika and Mela (base64).\[10\]\[63\] Only URLs in schema.org files. Uploaded separately through APIs.
- **Nutrition:** Structured in schema.org and the Tandoor/Mealie APIs. Free text in Paprika and Mela.
- **Multilingual content:** None of the formats carries translations. Emit one recipe per language and set `inLanguage`.

## Caveats

- **Not verified in this session:**
  - The exact latest versions of Nextcloud Cookbook, KitchenOwl, Grocy, Paprika, Mela and AnyList.
  - All details for Whisk/Samsung Food, Pestle, ReciMe and Copy Me That.
  - Crouton's and Mela's Paprika import (the Mela claim comes from secondary sources).
  - Whether PR #3430 for Nextcloud Cookbook has been merged.
  - Whether KitchenOwl issue #1169 has been fixed.
- Some API payload details (Mealie request bodies, KitchenOwl recipe body, Grocy file upload) come from community clients, MCP servers or generated OpenAPI copies, not official docs. Check them against each instance's own OpenAPI page.
- I could not run fresh tests of recipe-scrapers on `@graph`, `HowToSection` and image arrays. Treat the robustness claims as based on code reputation and app behaviour, and test them with your own output.
- Per instructions, sources are named in the text; a separate citation pass supplies the formal references, so I have not added an APA list here.

## Quellen

1. [Releases · TandoorRecipes/recipes · GitHub](https://github.com/TandoorRecipes/recipes/releases)
2. [Releases · mealie-recipes/mealie · GitHub](https://github.com/mealie-recipes/mealie/releases)
3. [Releases · kitshn-app/kitshn · GitHub](https://github.com/aimok04/kitshn/releases)
4. [Release Nightly · reaper47/recipya · GitHub](https://github.com/reaper47/recipya/releases/tag/nightly)
5. [GitHub - kragent66-glitch/recipya-rs: A clean, simple and powerful recipe manager your whole family will enjoy. · GitHub](https://github.com/kragent66-glitch/recipya-rs)
6. [Recipya](https://old.recipya.ca/)
7. [ManageMeals - Applications - Awesome Selfhosted](https://awesome-web.theravenhub.com/apps/managemeals)
8. [feat: import recipe from schema.org JSON by TheTisiboth · Pull Request #3430 · nextcloud/cookbook · GitHub](https://github.com/nextcloud/cookbook/pull/3430)
9. [Paprika User Guide for Android](https://www.paprikaapp.com/help/android/)
10. [Documentation - Mela](https://mela.recipes/fileformat/index.html)
11. [Cooklang Playground](https://cooklang.github.io/cooklang-rs/)
12. [Google Recipe Structured Data: Rules and Properties (2026)](https://hirebalzac.ai/google-recipe-structured-data/)
13. [pages with recipe schema blocks](https://api-docs.lumar.io/docs/report-templates/crawl_structured_data_blocks/pages_with_recipe_schema_blocks)
14. [Import/Export - Tandoor Recipes](https://docs.tandoor.dev/features/import_export/)
15. [Is there a list of supported websites Tandoor can import recipes from? · TandoorRecipes/recipes · Discussion #3243 · GitHub](https://github.com/TandoorRecipes/recipes/discussions/3243)
16. [tandoor recipe from source api openapi](https://raw.githubusercontent.com/api-evangelist/tandoor/refs/heads/main/openapi/tandoor-recipe-from-source-api-openapi.yml)
17. [github.com](https://github.com/TandoorRecipes/recipes/issues/2428)
18. [Home - Mealie](https://mealie.io/)
19. [API Reference](https://deepwiki.com/mealie-recipes/mealie/3.1-api-reference)
20. [Features - Mealie](https://mealie.io/documentation/getting-started/features/)
21. [GitHub - christianlupus-nextcloud/nextcloud-cookbook · GitHub](https://github.com/christianlupus-nextcloud/nextcloud-cookbook)
22. [GitHub - nextcloud/cookbook: 🍲 A library for all your recipes · GitHub](https://github.com/nextcloud/cookbook)
23. [Sources of recipes that can be added with the URL in cookbook - ℹ️ Support - Nextcloud community](https://help.nextcloud.com/t/sources-of-recipes-that-can-be-added-with-the-url-in-cookbook/156338)
24. [Crouton: Recipe Manager - App Store - Apple](https://apps.apple.com/mx/app/crouton-recipe-manager/id1461650987?l=en-GB)
25. [GitHub - TomBursch/kitchenowl: KitchenOwl is a self-hosted grocery list and recipe manager. The backend is made with Flask and the frontend with Flutter. Easily add items to your shopping list before you go shopping. You can also create recipes and add items based on what you want to cook. · GitHub](https://github.com/TomBursch/kitchenowl)
26. [🔔 tandoor 2.6.15 Available · Issue #28 · mildman1848/tandoor · GitHub](https://github.com/mildman1848/tandoor/issues/28)
27. [Mealie](https://apps.umbrel.com/app/mealie)
28. [Releases · reaper47/recipya · GitHub](https://github.com/reaper47/recipya/releases)
29. [github.com](https://github.com/elliejs/recipya)
30. [GitHub - kitshn-app/kitshn: Unofficial Tandoor client for Android, iOS and Desktop devices · GitHub](https://github.com/aimok04/kitshn)
31. [ManageMeals Web - recipe manager frontend - LinuxLinks](https://www.linuxlinks.com/managemeals-web-recipe-manager-frontend/)
32. [ManageMeals - Recipe Manager](https://managemeals.com/)
33. [ManageMeals icon](https://alternativeto.net/software/managemeals/about)
34. [nextcloud/cookbook architecture diagram: how it works](https://gitdiagram.com/nextcloud/cookbook)
35. [glama.ai](https://glama.ai/mcp/servers/Harpune/mcp-kitchenowl/tree)
36. [feat: Add AI recipe generator chat by vanalmsick · Pull Request #1160 · TomBursch/kitchenowl · GitHub](https://github.com/TomBursch/kitchenowl/pull/1160)
37. [Recipe import bypasses the hardened HTTP client and allows SSRF into internal networks · Issue #1169 · TomBursch/kitchenowl · GitHub](https://github.com/TomBursch/kitchenowl/issues/1169)
38. [Releases · TomBursch/kitchenowl · GitHub](https://github.com/TomBursch/kitchenowl/releases)
39. [GitHub - guim31/gladys-kitchenowl: Gladys Assistant external integration: KitchenOwl shopping lists and meal planner · GitHub](https://github.com/guim31/gladys-kitchenowl)
40. [Grocy API - Productivity API](https://jentic.com/apis/grocy.info/grocy)
41. [Bug: Adding a recipe ingredient via the api with non-stock qu results in wrong amount · Issue #1528 · grocy/grocy · GitHub](https://github.com/grocy/grocy/issues/1528)
42. [Paprika User Guide for iOS](https://www.paprikaapp.com/help/ios/)
43. [Mela: An Elegant and Innovative Recipe and Cooking App for iPhone, iPad, and Mac - MacStories](https://www.macstories.net/reviews/mela-an-elegant-and-innovative-recipe-and-cooking-app-for-iphone-ipad-and-mac/)
44. [Best Recipe Organizer Apps: CookBook, Paprika, Mela and More](https://www.itechguides.com/the-best-recipe-organizer-apps-for-saving-planning-and-cooking/)
45. [Recipe Keeper App - App Store](https://apps.apple.com/us/app/recipe-keeper/id974683711)
46. [Convert Recipe Keeper Recipes](https://movemyrecipes.com/recipe-keeper)
47. [Importing Recipes from Paprika - AnyList Help](https://help.anylist.com/articles/paprika-import/)
48. [Recipes - AnyList Help](https://help.anylist.com/topics/recipes/)
49. [Importing From Mela](https://docs.recipesage.com/docs/tutorials/settings/import/mela/)
50. [Mela Alternative - Free & Open Source](https://recipesage.com/alternatives/mela/)
51. [Importing From Recipe Keeper](https://docs.recipesage.com/docs/tutorials/settings/import/recipe-keeper/)
52. [How to Import Recipes from a File in the Website?](https://mycookbook.zendesk.com/hc/en-us/articles/200780721-How-can-I-import-a-recipe-from-a-file)
53. [How to Bulk Import Recipes from Another Program (Website)](https://learn.plantoeat.com/help/import-recipe-files-from-other-programs)
54. [How do I bulk import recipes into CookBook?](https://help.cookbookmanager.com/hc/en-gb/articles/360002691195-How-do-I-bulk-import-recipes-into-CookBook)
55. [Cooklang Specification & Syntax Reference](https://cooklang.org/docs/spec/)
56. [cooklang-import 0.9.9](https://docs.rs/crate/cooklang-import/latest/source/src/lib.rs)
57. [cooklang php](https://github.com/devapeu/cooklang-php)
58. [What Goes Into Designing a Recipe Markup Language](https://cooklang.org/blog/37-designing-a-recipe-markup-language/)
59. [CooklangSharp 0.0.0-alpha.0.9](https://www.nuget.org/packages/CooklangSharp)
60. [0.0.1 alpha3](https://readme.hex.pm/cooklang_ex/0.0.1-alpha3)
61. [cooklang 0.18.6](https://docs.rs/crate/cooklang/latest/source/src/model.rs)
62. [Breaking Free from Paprika: What .paprikarecipes Files Actually Are](https://movemyrecipes.com/blog/breaking-free-from-paprika-what-paprikarecipes-files-actually-are)
63. [Paprika Recipe Manager for iPad: export format](https://yabukurosawa.wordpress.com/2012/09/30/paprika-recipe-manager-for-ipad-export-format/)
64. [paprika-api.md · GitHub](https://gist.github.com/mattdsteele/7386ec363badfdeaad05a418b9a1f30a)
65. [cookbook importer](https://github.com/ebridges/cookbook-importer)
66. [Import/Export - Vanilla Cookbook Documentation](https://vanilla-cookbook.readthedocs.io/en/latest/manual/import/)
67. [Self-Hosted Alternatives to Paprika Recipe Manager - DEV Community](https://dev.to/selfhostingsh/self-hosted-alternatives-to-paprika-recipe-manager-5a14)
68. [glama.ai](https://glama.ai/mcp/servers/Hugeldugelking/tandoor-mcp/tree)
69. [Add config option to disable ingredient parser · mealie-recipes/mealie · Discussion #6167 · GitHub](https://github.com/mealie-recipes/mealie/discussions/6167)
70. [AI Providers - Mealie](https://mealie.io/documentation/getting-started/installation/ai-providers/)
71. [API endpoints have changed · Issue #3887 · TandoorRecipes/recipes · GitHub](https://github.com/TandoorRecipes/recipes/issues/3887)
72. [image-to-tandoor/README.md at main · LekoArts/image-to-tandoor · GitHub](https://github.com/LekoArts/image-to-tandoor/blob/main/README.md)
73. [GitHub - ralphzimmermann/tandoor-mcp: MCP Tool Server for the Tandoor Recipe Management platform · GitHub](https://github.com/ralphzimmermann/tandoor-mcp)
74. [tandoor mcp](https://glama.ai/mcp/servers/Hugeldugelking/tandoor-mcp)
75. [Add recipes from photos: a transcription prompt and image upload links by etiennex9 · Pull Request #2 · etiennex9/tandoor-claude-connector · GitHub](https://github.com/etiennex9/tandoor-claude-connector/pull/2)
76. [Delete/Upload Image throws an Bad Request Error · Issue #1798 · TandoorRecipes/recipes · GitHub](https://github.com/TandoorRecipes/recipes/issues/1798)
77. [glama.ai](https://glama.ai/mcp/servers/vp31gip3sr)
78. [update recipe image](https://glama.ai/mcp/servers/2fst4u/mealie-mcp/tools/update_recipe_image)
79. [github.com](https://github.com/nextcloud/cookbook/issues/288)
80. [GitHub - n1tr0-5urf3r/ioBroker.kitchenowl: ioBroker adapter for self-hosted kitchenowl: shopping lists, recipes, meal planner, expenses and household balances, with optional write-back. · GitHub](https://github.com/n1tr0-5urf3r/ioBroker.kitchenowl)
81. [API - KitchenOwl Docs](https://docs.kitchenowl.org/dev/reference/API/)
82. [kitchenowl cli](https://pypi.org/project/kitchenowl-cli/)
83. [hermes grocy mcp](https://pypi.org/project/hermes-grocy-mcp)
84. [MCP server for Mealie](https://pypi.org/project/mcp-mealie/0.1.0/)
85. [Backend Configuration - Mealie](https://mealie.io/documentation/getting-started/installation/backend-config/)
