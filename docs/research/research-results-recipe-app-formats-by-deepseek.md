# Recipe Import Formats and App Support for an AI Cooking Assistant

**Research date:** 2026-11-01  
**Scope:** Official documentation, specifications, and source repositories were used as primary sources. Where a claim is inferred, version-dependent, or could not be verified from a primary source, it is explicitly flagged. Maintenance status reflects the repositories/docs as checked on the research date.

---

## 1. SCHEMA.ORG RECIPE (JSON-LD)

### 1.1 What Google requires vs. what schema.org defines

Schema.org’s `Recipe` type defines a broad vocabulary. Google’s recipe rich-result guidelines are narrower and specify which properties are required for eligibility, which are recommended, and which are ignored or conditionally required.

Google requires:

- `name` — the dish name.
- `image` — image of the completed dish, crawlable and indexable.

Google recommends:

- `author`, `datePublished`, `description`, `keywords`
- `recipeCategory`, `recipeCuisine`
- `recipeIngredient`, `recipeInstructions`
- `recipeYield`
- `prepTime`, `cookTime`, `totalTime`
- `nutrition.calories`
- `aggregateRating`, `video`

A critical conditional rule: **if `nutrition.calories` is present, `recipeYield` must be present with the number of servings** .

Schema.org itself does not require these properties; the requirements above are Google’s rich-result requirements, not schema.org validity requirements .

### 1.2 Representation of key recipe components

| Component                 | schema.org representation                                                                                                                                                                                                                      | Practical notes                                                                                                                                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ingredients**           | `recipeIngredient`: `Text[]` (array of strings). schema.org also permits `ItemList` or `PropertyValue`, but Google recommends plain ingredient text .                                                                                          | Ingredient **sections** are not a first-class Google/schema.org property. `HowToSection` applies to instructions, not ingredients. Most apps therefore store ingredients as a flat list or use text headings. |
| **Instructions**          | `recipeInstructions`: `HowToStep[]`, `HowToSection[]`, or text. Google recommends `HowToStep` with `text`; `HowToSection` can group steps with `name` and `itemListElement` .                                                                  | Google treats plain text as a single block and attempts to split it automatically. Explicit `HowToStep` objects produce more reliable imports.                                                                |
| **Yield**                 | `recipeYield`: `Text` or `QuantitativeValue`. Google prefers a plain number for servings and allows additional yields such as `["6", "24 cookies"]` .                                                                                          | If calories are provided, `recipeYield` becomes mandatory.                                                                                                                                                    |
| **Times**                 | `prepTime`, `cookTime`, `totalTime`: ISO 8601 durations, e.g. `PT30M`, `PT1H30M` .                                                                                                                                                             | All three are optional, but Google recommends them.                                                                                                                                                           |
| **Nutrition**             | `nutrition`: `NutritionInformation` object. Google supports `nutrition.calories` for rich results; other fields such as `fatContent`, `proteinContent`, `carbohydrateContent` are schema.org-valid but not all are Google rich-result fields . | Calories without yield is a common validation error.                                                                                                                                                          |
| **Images**                | `image`: URL, `ImageObject`, or array of URLs. Google recommends multiple high-resolution images with 16:9, 4:3, and 1:1 aspect ratios .                                                                                                       | Apps typically download the first image or all images.                                                                                                                                                        |
| **Keywords / categories** | `keywords`: comma-separated `Text`. `recipeCategory` and `recipeCuisine`: separate `Text` properties .                                                                                                                                         | Google warns against putting category/cuisine values into `keywords`.                                                                                                                                         |

### 1.3 Which apps import schema.org data, and how

| App                                  | Import path for schema.org                                                                                                   | Robustness notes                                                                                                                                                                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nextcloud Cookbook**               | URL scraping; native storage is schema.org JSON; API accepts schema.org-style JSON .                                         | Good metadata coverage. Ingredient parsing can produce `NaN` quantity/unit values on some imports .                                                                             |
| **Tandoor Recipes**                  | URL importer parses schema.org/Recipe JSON-LD and microdata .                                                                | JSON **file** import appears to expect Tandoor’s own JSON model rather than arbitrary schema.org JSON; schema.org support is primarily URL-based. Flagged as version-dependent. |
| **Mealie**                           | URL scraping; paste structured HTML or JSON; AI import from text; API `create/html-or-json` accepts schema.org Recipe JSON . | Strong schema ingestion. Ingredient parsing is separate and may require re-parsing after import.                                                                                |
| **RecipeSage**                       | Direct JSON-LD file upload .                                                                                                 | Explicitly requires JSON-LD, not generic JSON.                                                                                                                                  |
| **Crouton**                          | Paste schema.org Recipe JSON/JSON-LD or import individual JSON files/ZIP archives .                                          | Explicit schema.org file support. Manual section repair is sometimes needed.                                                                                                    |
| **Paprika**                          | URL import via built-in browser parses schema.org markup .                                                                   | No schema.org JSON **file** import verified. Paprika’s own export HTML contains schema metadata, but import is via URL or `.paprikarecipes`.                                    |
| **Mela**                             | URL import parses recipe pages .                                                                                             | `.melarecipe` is Mela’s own JSON, not schema.org JSON-LD. No direct JSON-LD file import verified.                                                                               |
| **AnyList**                          | URL import via browser extension/share sheet .                                                                               | No JSON-LD file import verified.                                                                                                                                                |
| **KitchenOwl, ManageMeals, Recipya** | URL scraping using schema.org data .                                                                                         | File import is either absent or app-specific JSON.                                                                                                                              |
| **Grocy**                            | No direct schema.org import; recipes are created through the object API .                                                    | Not a schema.org importer.                                                                                                                                                      |

**Robustness assessment:** Schema.org ingestion is generally reliable for title, image, times, yield, tags, and step text. Ingredient structuring is the weak point: `recipeIngredient` is free text, and each app applies its own parser. Non-English ingredients and units frequently degrade parsing quality. Ingredient sections are usually lost because schema.org has no Google-supported ingredient-section property.

---

## 2. APP-BY-APP IMPORT SUPPORT

### 2.1 Maintenance and existence check

All apps below were verified to exist and have public documentation or repositories. Maintenance status is based on repository activity or current documentation as of 2026-11-01. Closed-source apps are marked as commercial and were checked via official help pages/app listings.

### 2.2 Self-hosted and open-source apps

#### Tandoor Recipes

- **Status:** Actively maintained open-source project; documentation current .
- **Import paths:** URL scraping; file import for many formats; REST API.
- **Supported file/source imports:** Nextcloud, Mealie, Chowdown, Safron, Paprika, ChefTap, Pepperplate, RecipeSage, Rezeptsuite.de, Domestica, MealMaster, RezKonv, OpenEats, Plantoeat, CookBook Manager, Cooklang, CopyMeThat, Mela, Cookmate, PDF (experimental), Gourmet .
- **Required fields:** Recipe `name`; other fields optional in API payloads .
- **Ingredient sections:** Partial. Tandoor supports structured steps; ingredient headers in JSON import are a known gap .
- **Units/quantities:** Supports fractions or decimals . Non-Latin ingredient parsing is known to be weak .
- **Multilingual:** UI localized, but ingredient parser is English-centric and fails on some non-Latin inputs.
- **Images:** Supported for most importers, including Paprika and Nextcloud .
- **Nutrition:** Supported.
- **Tags:** Supported as keywords/tags.

#### Mealie

- **Status:** Actively maintained; current documentation and v3.x API .
- **Import paths:** URL scraping; paste structured HTML/JSON; AI text/image import; migration from Tandoor, Nextcloud Cookbooks, Paprika, Chowdown, Plan to Eat, Recipe Keeper, Copy Me That, My Recipe Box, DVO Cook’n X3 .
- **Required fields:** API creation generally requires `name`; ingredients and instructions are expected for a complete recipe, but other fields are optional .
- **Ingredient sections:** Mealie supports section headers in ingredient text using `#`/`##` in some MCP/API tooling . Official UI support should be verified; flagged as partial.
- **Units/quantities:** Uses CRF-based NLP parser, brute-force parser, and optional AI parser . NLP training data is English-centric; custom units improve non-English parsing .
- **Multilingual:** Better than many peers because of AI parser option, but default NLP is English-trained.
- **Images:** Supported.
- **Nutrition:** Supported.
- **Tags:** Categories, tags, and tools supported .

#### Recipya

- **Status:** Maintained, but being rewritten in Rust; current release and nightly builds exist .
- **Import paths:** URL scraping of schema.org data; migrations from Mealie, Tandoor, Nextcloud Cookbook, MasterCook, and Paprika .
- **Required fields:** Recipe name and basic fields; schema.org fields mapped.
- **Ingredient sections:** Partial; migration fidelity depends on source format.
- **Units/quantities:** Measurement-system conversion is a feature .
- **Multilingual:** Not well documented; parser likely English-centric. Flagged.
- **Images/nutrition/tags:** Supported in imports.

#### ManageMeals

- **Status:** Maintained open-source, self-hosted .
- **Import paths:** URL import only; browser bookmarklet .
- **Required fields:** URL; parser extracts name, ingredients, instructions, and other fields.
- **Ingredient sections:** Parser-dependent; no file-based import or API documented.
- **Units/quantities/multilingual:** Parser-dependent.
- **Images/nutrition/tags:** Extracted when present on the page.

#### Nextcloud Cookbook

- **Status:** Maintained Nextcloud app; current repository and API docs .
- **Import paths:** URL scraping; recipes stored as schema.org JSON files; API create.
- **Required fields:** `name`; schema.org fields optional.
- **Ingredient sections:** Ingredients are typically a flat list in schema.org JSON. No first-class section model verified.
- **Units/quantities:** Known issue where imported lines can display `NaN` for quantity/unit until edited .
- **Multilingual:** URL importer is schema-driven, but ingredient unit parsing is weak for non-English.
- **Images/nutrition/tags:** Supported via schema fields.

#### KitchenOwl

- **Status:** Maintained open-source app .
- **Import paths:** URL import via `recipe-scrapers` with schema.org fallback; only a very specific JSON format for file import; no easy migration from other apps .
- **Required fields:** JSON format specific to KitchenOwl; URL import requires a URL.
- **Ingredient sections:** Limited.
- **Units/quantities:** Parser-dependent.
- **Multilingual:** `recipe-scrapers` supports many sites, but non-English parsing is not guaranteed.
- **Images/nutrition/tags:** Extracted from URL where available.

#### Grocy

- **Status:** Maintained household ERP with recipe objects .
- **Import paths:** REST API only; no recipe import UI or file format.
- **Endpoints:** `/api/objects/recipes` and `/api/objects/recipes_pos` .
- **Required fields:** Grocy database fields; recipe name, ingredient positions, amounts.
- **Ingredient sections:** Ingredient positions in `recipes_pos`; not a general recipe section model.
- **Units/quantities:** Product-based units, tied to Grocy stock management.
- **Multilingual/images/nutrition/tags:** Not a rich recipe importer; limited compared with recipe managers.

#### kitshn

- **Status:** Maintained unofficial Tandoor client for Android, iOS, and desktop .
- **Import paths:** Uses Tandoor backend; AI-powered social media import from Instagram/TikTok; share links to kitshn .
- **Required fields:** Delegated to Tandoor.
- **Ingredient sections/units/multilingual:** Inherits Tandoor behavior.
- **Images/nutrition/tags:** Inherits Tandoor behavior.

### 2.3 Commercial / closed-source apps

#### Paprika

- **Status:** Commercial, actively maintained.
- **Import paths:** Native `.paprikarecipes` archive; URL import via built-in browser; manual entry .
- **Export formats:** HTML (with schema metadata) and `.paprikarecipes` (ZIP of JSON) .
- **Required fields:** Recipe name; ingredients and directions for a useful recipe.
- **Ingredient sections:** Flat ingredient list; no structured section model verified.
- **Units/quantities:** Free-text ingredient lines.
- **Multilingual:** Browser import depends on schema markup; manual entry supports any language.
- **Images:** Supported.
- **Nutrition:** Paprika has nutrition fields, but import coverage from schema is not fully documented. Flagged.
- **Tags:** Categories.

#### Mela

- **Status:** Commercial iOS/Mac app, actively maintained.
- **Import paths:** URL import; `.melarecipe` (single JSON) and `.melarecipes` (ZIP) files .
- **Required fields:** `id`, `title`; other fields optional .
- **Ingredient sections:** Ingredients are a string with Markdown support; group titles can be represented with Markdown headings .
- **Units/quantities:** Free text.
- **Multilingual:** URL import from sites in any language; parsing quality varies.
- **Images:** Base64-encoded images in `.melarecipe` .
- **Nutrition:** String field .
- **Tags:** Categories array .

#### Crouton

- **Status:** Commercial iOS app, actively maintained .
- **Import paths:** URL, photo/scan, PDF, pasted text, file from another recipe app, schema.org JSON/JSON-LD files and ZIP archives .
- **Required fields:** Recipe name and enough content to form a recipe.
- **Ingredient sections:** Headings can be converted to sections manually; automatic import may misclassify section headings as ingredients .
- **Units/quantities:** Parser-dependent; manual repair possible.
- **Multilingual:** AI/OCR and paste import can handle non-English text, but parsing accuracy varies.
- **Images/nutrition/tags:** Supported.

#### Recipe Keeper

- **Status:** Commercial, actively maintained.
- **Import paths:** URL import with AI extraction; manual entry; export as `.zip` containing schema-tagged HTML and images .
- **Direct JSON-LD import:** Not verified. Its export is schema-tagged HTML, not necessarily re-importable as JSON-LD. Flagged.
- **Required fields:** Recipe name and ingredients/directions.
- **Ingredient sections:** Limited.
- **Units/quantities:** Free text.
- **Multilingual:** Imports in original language .
- **Images/nutrition/tags:** Supported.

#### AnyList

- **Status:** Commercial, actively maintained.
- **Import paths:** URL import via browser extension/share sheet; `.paprikarecipes` import; paste ingredients and steps .
- **Required fields:** Recipe name; ingredient and step text.
- **Ingredient sections:** No structured section model verified.
- **Units/quantities:** Free text; AnyList parses some quantities for shopping lists.
- **Multilingual:** Manual paste supports any language; URL import depends on site markup.
- **Images/nutrition/tags:** Images supported; nutrition and tags are limited compared with self-hosted apps.

#### RecipeSage

- **Status:** Commercial/open-core, actively maintained .
- **Import paths:** JSON-LD file upload, plain text, URL, image/PDF, Paprika, Pepperplate, Living Cookbook, Cookmate, Recipe Keeper .
- **Required fields:** Recipe name; other fields optional.
- **Ingredient sections:** Partial.
- **Units/quantities:** Parser-dependent.
- **Multilingual:** Manual/paste supports source language; parser may be English-centric.
- **Images/nutrition/tags:** Supported.

### 2.4 Other apps with significant user numbers

- **Plan to Eat, Copy Me That, Pepperplate, ChefTap, Cookmate, My Recipe Box, DVO Cook’n X3** are supported as migration sources by Mealie and/or Tandoor . Their native formats are app-specific archives/CSV/HTML rather than open standards. Direct import by a new AI assistant would require per-app exporters and are lower priority than schema.org and Paprika archives.
- **BigOven, Samsung Food, Whisk** are large consumer platforms but generally rely on URL import or proprietary APIs; no open file import standard was verified. Flagged as out of scope for a minimal-format strategy.

---

## 3. OPEN AND LEGACY INTERCHANGE FORMATS

| Format                           | Structure                                                                                                                                                            | Adoption                                                             | Apps that import it                                                                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cooklang**                     | Plain-text `.cook` files. Ingredients: `@flour{200%g}`. Cookware: `#whisk{}`. Timer: `~{25%minutes}`. Sections: `==Dough==`. Metadata via YAML-like front matter .   | Niche but active ecosystem; human-readable and Git-friendly.         | Tandoor supports Cooklang import . Mealie and other apps do not natively import Cooklang, though converters exist.                                   |
| **Paprika `.paprikarecipes`**    | ZIP archive containing individually compressed JSON data for each recipe .                                                                                           | Broad migration format among consumer apps.                          | Paprika native; AnyList; Mealie; Tandoor; RecipeSage; Recipya .                                                                                      |
| **MasterCook MXP/MX2**           | MXP/MX2 are MasterCook recipe text formats. MX2 includes an XML representation for MasterCook 5+ and a text fallback for older versions .                            | Legacy; still used by MasterCook 24 users and old cookbook archives. | MasterCook; Recipya lists MasterCook import . Tandoor does not list MasterCook directly; it lists MealMaster.                                        |
| **Meal-Master**                  | Fixed-format plain text. Recipe header begins with hyphens and contains “Meal-Master”; servings/categories have fixed positions; title limited to 60 characters .    | Legacy; popular in older recipe collections and BBS-era archives.    | Tandoor supports MealMaster import . MacGourmet/KRecipes historically supported it.                                                                  |
| **RecipeML**                     | XML-based format with a DTD (`recipeml.dtd`), originally created by FormatData in 2000. Version 0.5 supports detailed ingredient markup and measurement conversion . | Very low adoption.                                                   | Largo Recipes historically read/wrote RecipeML; MacGourmet supported import. No major modern recipe manager was verified to import it natively.      |
| **Open Recipe Format**           | YAML-based format (JSON is syntactically valid YAML); JSON Schema added in 2021 .                                                                                    | Very low adoption; no significant app import verified.               | No major app import verified. Flagged.                                                                                                               |
| **App-specific export archives** | Mealie ZIP (`recipes/<dir>/*.json` + images); Tandoor JSON/ZIP; Nextcloud `Recipes.zip`; Recipe Keeper `.zip` with schema-tagged HTML.                               | Useful for migrations between self-hosted apps.                      | Mealie and Tandoor cross-import each other and Nextcloud; Vanilla Cookbook imports Paprika, Mealie, Nextcloud, Recipe Keeper, and Tandoor archives . |

**Adoption summary:** The only legacy formats with meaningful modern import support are **Paprika `.paprikarecipes`** and **Meal-Master** (mainly Tandoor). MasterCook is mostly relevant to Recipya and legacy desktop tools. RecipeML and Open Recipe Format are not practical targets for broad app coverage.

---

## 4. INGREDIENT PARSING

### 4.1 How apps parse free-text ingredient lines

Most apps use one or more of these approaches:

1. **Regex/brute-force parsing:** Splits on the first number, then looks for a known unit, then treats the remainder as food/note. Fast but brittle with ranges, fractions, and non-English units.
2. **CRF/NLP models:** Conditional random fields trained on labeled ingredient phrases. Mealie uses CRF-based parsing and has an NLP parser trained on a large English dataset . The New York Times ingredient-phrase tagger is the canonical open example: a CRF trained on roughly 180,000 labeled phrases with about 89% sentence-level accuracy on its training distribution .
3. **AI/LLM parsing:** Mealie offers an AI ingredient parser as an alternative to NLP and brute-force parsers . Tandoor’s ecosystem also includes AI-assisted import tooling, but the core parser remains more traditional.
4. **Hybrid:** Try structured markup first (schema.org), then parser, then manual/LLM fallback.

### 4.2 Where parsing fails

| Challenge                    | Behavior                                                                                                                                                                                | Practical consequence                                                                                                                                      |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fractions**                | `1/2`, `½`, `1 1/2` are handled by some parsers, especially with Unicode fraction support .                                                                                             | Mixed numbers and Unicode fractions often need normalization to decimals before output.                                                                    |
| **Ranges**                   | `2-3 cloves`, `2 to 3 cups` are inconsistently parsed. Some parsers treat the first number only or fail entirely.                                                                       | For machine import, output a single quantity or put the range in the note; do not rely on the importer to understand ranges.                               |
| **Metric vs. imperial**      | Parsers recognize common units, but aliases (`g`, `gram`, `grams`, `gr`) vary.                                                                                                          | Use standard unit names and abbreviations from the target app’s unit database.                                                                             |
| **Non-English languages**    | English-trained CRF/NLP models degrade sharply. Mealie’s NLP data is trained exclusively on English; custom units help . Tandoor has documented failures on Japanese ingredient lines . | Preserve the original ingredient text and, where possible, supply structured quantity/unit/food hints rather than relying solely on the importer’s parser. |
| **Units in other languages** | German `gestr.`, Japanese `g` attached to food without spaces, CJK spaceless units are problematic .                                                                                    | Use ASCII spaces between quantity, unit, and food when possible.                                                                                           |
| **Notes and preparation**    | Parenthetical notes, “finely chopped,” “to taste,” “divided” are often misclassified as part of the food name.                                                                          | Put notes in parentheses at the end of the line; use a separate note field if the target format supports it.                                               |

### 4.3 Input conventions that maximize correct parsing

Recommended conventions for an AI assistant emitting ingredient lines:

- One ingredient per line.
- Quantity first, then a space, then unit, then food: `200 g flour`.
- Use decimals or simple fractions without mixed numbers: `0.5 tsp`, `1.5 cups`.
- Avoid Unicode vulgar fractions (`½`) unless the target app is known to support them.
- Avoid ranges in the quantity field. Use a single amount or write `2–3` in the note.
- Use standard unit abbreviations in the target app’s language: `g`, `kg`, `ml`, `l`, `tsp`, `tbsp`, `cup`.
- Put preparation notes at the end in parentheses: `1 onion (finely chopped)`.
- Use explicit section headers such as `For the sauce:` on their own line; do not rely on schema.org to preserve ingredient sections.
- For multilingual recipes, keep the original line intact and add structured hints only if the target API accepts them.

These conventions improve both regex parsers and CRF/NLP parsers, and they make manual correction easier when parsing fails.

---

## 5. API-BASED IMPORT FOR SELF-HOSTED APPS

### 5.1 Endpoints and authentication

| App                    | Create endpoint                                                                                                                                | Authentication                                                                                                             | Minimal payload                                                                                                                                                                        | Notes                                                                                                       |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Tandoor Recipes**    | `POST /api/recipe/` (documented in Tandoor’s OpenAPI/DRF browser) . Alternative: `POST /api/recipe-from-source/` for source-based import .     | API token from Settings → API → Access Tokens, sent as `Authorization: Token <token>` or `Authorization: Bearer <token>` . | `name`, `steps` array where each step has `instruction` and `ingredients` (`food`, `amount`, `unit`); optional `description`, `servings`, `working_time`, `waiting_time`, `keywords` . | Set `internal: true` to avoid the “External” badge . Food/unit names may need to exist or be auto-resolved. |
| **Mealie**             | `POST /api/recipes` creates a stub; then `PUT /api/recipes/{slug}` populates it. Or `POST /api/recipes/create/html-or-json` with schema JSON . | API token from Profile → API Tokens, sent as `Authorization: Bearer <token>` .                                             | `name`, `ingredients`, `instructions`; other fields optional . For `create/html-or-json`, `content` can be raw HTML, schema.org Recipe JSON, or plain text .                           | Mealie also has `/api/recipes/create/url` and streaming endpoints .                                         |
| **Nextcloud Cookbook** | `POST /index.php/apps/cookbook/api/recipes` or `/apps/cookbook/api/v1/recipes` .                                                               | HTTP Basic Auth with a Nextcloud **app password**, not the login password .                                                | schema.org Recipe JSON body: `name`, `recipeIngredient`, `recipeInstructions`, times, yield, etc. .                                                                                    | App passwords can be created under Settings → Security → Devices & sessions.                                |
| **Grocy**              | `POST /api/objects/recipes` and `/api/objects/recipes_pos` for ingredient positions .                                                          | `GROCY-API-KEY` header, or query parameter of the same name .                                                              | Grocy database fields: recipe name, description, ingredient product IDs, amounts, positions.                                                                                           | Grocy is not schema.org-based; payloads must match its object model.                                        |

### 5.2 Security considerations for a local tool storing API tokens

- **Store tokens in an OS keychain or secret vault**, not in plaintext config files or logs.
- **Use HTTPS and validate TLS certificates.** Self-hosted instances may use self-signed certificates; provide an explicit trust override rather than disabling verification globally.
- **Use a dedicated least-privilege account** for the assistant. On Mealie, a non-admin user token is preferable for automation . On Nextcloud, use an app password scoped to the assistant.
- **Avoid long-lived tokens if the app supports rotation.** Tandoor tokens are long-lived DRF tokens; rotate them periodically.
- **Never log the `Authorization`, `GROCY-API-KEY`, or cookie headers.**
- **Bind the local tool to localhost** unless remote access is required, and add authentication to the local tool itself if it stores tokens.
- **Prefer API creation over file creation when fidelity matters**, because the API can express structured ingredients and sections more precisely than schema.org’s flat ingredient arrays.

---

## 6. RECOMMENDATION

### 6.1 Smallest set of output formats with maximum coverage

For an AI cooking assistant that writes files or sends recipes via API, the smallest practical set is:

1. **Primary structured format: schema.org Recipe JSON-LD**
   - One JSON object per recipe, or an array/ZIP of JSON objects.
   - Include `name`, `image`, `recipeIngredient`, `recipeInstructions` (prefer `HowToStep`/`HowToSection`), `recipeYield`, ISO 8601 times, `nutrition`, `keywords`, `recipeCategory`, `recipeCuisine`.
   - Covers URL-based imports in almost every app and direct JSON ingestion in Nextcloud Cookbook, Mealie, RecipeSage, and Crouton.

2. **Secondary migration format: Paprika `.paprikarecipes` archive**
   - A ZIP of JSON recipe objects.
   - Natively imported by Paprika, AnyList, Mealie, Tandoor, RecipeSage, and Recipya.
   - Best single format for consumer-app migration and for apps that do not ingest schema.org JSON files.

3. **Fallback format: plain-text / Markdown recipe card**
   - Human-readable and pasteable into any app.
   - Use a consistent structure: title, yield, times, ingredient lines one per line, section headers, numbered steps.
   - Covers manual paste/import in AnyList, Crouton, RecipeSage, Mela, Recipe Keeper, KitchenOwl, and apps with no structured file import.

4. **Optional: native REST API for Tandoor, Mealie, Nextcloud Cookbook, and Grocy**
   - When credentials are available, use the native API instead of a file format. This gives the highest fidelity for ingredient sections, units, and images.

5. **Optional: Cooklang `.cook` only if Tandoor file import is a priority**
   - Cooklang preserves structured ingredients and sections and is human-readable, but only Tandoor was verified to import it among the apps surveyed. It adds a fourth format with limited coverage.

**Do not prioritize:** MasterCook MXP/MX2, Meal-Master, RecipeML, or Open Recipe Format for a new assistant. They are legacy or niche, and only Meal-Master has meaningful modern import support (Tandoor).

### 6.2 Coverage matrix

Legend: ✅ native/documented; ◐ partial, indirect, or requires workaround; ❌ not supported/verified.

| App                    |      Schema.org JSON-LD file | Schema.org URL scrape | Paprika `.paprikarecipes` | Plain text / Markdown | Native API create |                                    Other app archive |
| ---------------------- | ---------------------------: | --------------------: | ------------------------: | --------------------: | ----------------: | ---------------------------------------------------: |
| **Tandoor Recipes**    | ◐ (own JSON; schema via URL) |                    ✅ |                        ✅ |    ◐ (AI/text import) |                ✅ |                         ✅ (Mealie, Nextcloud, etc.) |
| **Mealie**             |                ◐ (paste/API) |                    ✅ |                        ✅ |          ✅ (AI/text) |                ✅ |         ✅ (Tandoor, Nextcloud, Recipe Keeper, etc.) |
| **Nextcloud Cookbook** |         ✅ (native JSON/API) |                    ✅ |                        ❌ |            ◐ (manual) |                ✅ |                                ❌ (imports URL only) |
| **RecipeSage**         |                           ✅ |                    ✅ |                        ✅ |                    ✅ |                ❌ |              ✅ (Pepperplate, Living Cookbook, etc.) |
| **Crouton**            |                           ✅ |                    ✅ | ◐ (file from another app) |                    ✅ |                ❌ |                                      ◐ (Crouton/PDF) |
| **Paprika**            |                           ❌ |                    ✅ |                        ✅ |            ◐ (manual) |                ❌ |                                                   ❌ |
| **AnyList**            |                           ❌ |                    ✅ |                        ✅ |            ✅ (paste) |                ❌ |                                                   ❌ |
| **Mela**               |                           ❌ |                    ✅ |                        ❌ |            ◐ (manual) |                ❌ |                              ❌ (`.melarecipe` only) |
| **Recipe Keeper**      |                           ❌ |                    ✅ |                        ❌ |            ◐ (manual) |                ❌ |                                 ❌ (export zip only) |
| **KitchenOwl**         |           ❌ (specific JSON) |                    ✅ |                        ❌ |            ◐ (manual) |      ◐ (CLI/JSON) |                                                   ❌ |
| **Recipya**            |                           ❌ |                    ✅ |                        ✅ |            ◐ (manual) |                ❌ | ✅ (Mealie, Tandoor, Nextcloud, MasterCook, Paprika) |
| **ManageMeals**        |                           ❌ |                    ✅ |                        ❌ |            ◐ (manual) |                ❌ |                                                   ❌ |
| **Grocy**              |                           ❌ |                    ❌ |                        ❌ |                    ❌ |   ✅ (object API) |                                                   ❌ |
| **kitshn**             |    ❌ (delegates to Tandoor) |      ✅ (via Tandoor) |          ✅ (via Tandoor) |       ◐ (via Tandoor) |  ✅ (via Tandoor) |                                     ✅ (via Tandoor) |

**Coverage interpretation:**

- **Schema.org JSON-LD file** has full native support in 3 apps and partial support in 2 more; **schema.org URL scraping** covers roughly 11 of 14 apps.
- **Paprika `.paprikarecipes`** covers 6 apps natively and is the single best file format for consumer-app migration.
- **Plain text/Markdown** is the universal fallback but loses structure.
- **Native API** gives the best fidelity but only covers 4 self-hosted apps and requires per-app payload mapping.
- **Grocy** is the outlier: it has no meaningful recipe file import and requires its object API.

### 6.3 Trade-offs

| Format                        | Ingredient sections                                                 | Units/quantities                   | Images                               | Nutrition                                | Tags                             | Overall fidelity                                        |
| ----------------------------- | ------------------------------------------------------------------- | ---------------------------------- | ------------------------------------ | ---------------------------------------- | -------------------------------- | ------------------------------------------------------- |
| **Schema.org JSON-LD**        | Poor: ingredients are flat; `HowToSection` only helps instructions. | Free text; target parser decides.  | Good: image URLs can be downloaded.  | Good: structured `NutritionInformation`. | Good: keywords/category/cuisine. | High for metadata, medium for ingredients.              |
| **Paprika `.paprikarecipes`** | Flat ingredient list; no structured sections verified.              | Free text.                         | Good: images included or referenced. | Partial; depends on source.              | Categories.                      | High for migration, medium for structured cooking data. |
| **Plain text / Markdown**     | Manual headings only.                                               | Parser-dependent; worst fidelity.  | Only if URLs are included.           | Only if written manually.                | Only if written manually.        | Low structure, high universality.                       |
| **Cooklang**                  | Good: `==section==` syntax.                                         | Good: `@ingredient{qty%unit}`.     | Not a primary concern.               | Metadata possible.                       | Metadata possible.               | High for structured text, but low app coverage.         |
| **Native API**                | Best: structured ingredient positions/sections.                     | Best: units and amounts are typed. | Best.                                | Best.                                    | Best.                            | Highest fidelity, but per-app integration work.         |

**Recommendation summary:** Use **schema.org Recipe JSON-LD** as the default output, add **Paprika `.paprikarecipes`** for app migrations and consumer-app compatibility, and keep a **plain-text/Markdown** fallback for manual paste. Use **native APIs** when the user has a self-hosted instance and wants maximum fidelity. Add **Cooklang** only if Tandoor file-based structured recipes are a priority.

---

## Source List (APA Style)

AnyList. (n.d.). _Importing recipes from Paprika_. https://help.anylist.com/importing-recipes-from-paprika

AnyList. (n.d.). _Copying and pasting recipes into AnyList_. https://help.anylist.com/copying-and-pasting-recipes-into-anylist

Cooklang. (2026). _Cooklang specification_. https://cooklang.org/docs/spec/

Crouton. (n.d.). _Recipe import troubleshooting guide_. https://combustioninc.gorgias.help/en-US/crouton-recipe-import-troubleshooting-guide-7701731

Google Search Central. (2026, September 8). _Recipe (Recipe, HowTo, ItemList) structured data_. https://developers.google.com/search/docs/appearance/structured-data/recipe

Grocy. (2019). _Feature proposal: Recipe import/export/sync_ (Issue #247). https://github.com/grocy/grocy/issues/247

KitchenOwl. (2023). _Importing recipes from other apps_ (Discussion #155). https://github.com/TomBursch/kitchenowl/discussions/155

kitshn. (2024). _kitshn: Unofficial Tandoor client for Android, iOS and Desktop_. https://github.com/kitshn-app/kitshn

ManageMeals. (2025, July 30). _ManageMeals Web – recipe manager frontend_. LinuxLinks. https://www.linuxlinks.com/managemeals-web-recipe-manager-frontend/

MasterCook. (n.d.). _The MC 5+ and text formats (_.MX2)\*. https://support.mastercook.com/

Mealie. (n.d.). _Features_. https://github.com/mealie-recipes/mealie/blob/2c04da733f88836f788234a4bf1127599fbc1294/docs/docs/documentation/getting-started/features.md

Mealie. (2026). _Improving the ingredient parser_. https://github.com/mealie-recipes/mealie/discussions

Mela. (n.d.). _Mela file format_. https://mela.recipes/fileformat/index.html

Nextcloud. (2026). _Cookbook app_. https://github.com/nextcloud/cookbook

Nextcloud. (2026). _Cookbook API_. https://nextcloud.github.io/cookbook/

Paprika. (2024, May 12). _What export formats do you support?_ https://paprikaapp.zendesk.com/hc/en-us/articles/360051324613-What-export-formats-do-you-support

RecipeSage. (2024). _Importing from JSON-LD_. https://docs.recipesage.com/docs/tutorials/settings/import/json-ld/

Recipya. (2026). _reaper47/recipya_. https://github.com/reaper47/recipya

Schema.org. (n.d.). _Recipe_. https://schema.org/Recipe

Tandoor Recipes. (n.d.). _Import/Export_. https://docs.tandoor.dev/features/import_export/

Tandoor Recipes. (2022). _Ingredient parsing for non-Latin languages_ (Issue #1983). https://github.com/TandoorRecipes/recipes/issues/1983

Tandoor Recipes. (2020). _Using the createRecipe API results in created_by_id violating not-null constraint_ (Issue #296). https://github.com/TandoorRecipes/recipes/issues/296

Tandoor Recipes. (2025). _Allow user to specify ingredient headers in JSON import_ (Issue #3539). https://github.com/TandoorRecipes/recipes/issues/3539

Open Recipe Format. (2021). _techhat/openrecipeformat_. https://github.com/techhat/openrecipeformat

RecipeML. (2006). _RecipeML_. Wikipedia. https://en.wikipedia.org/wiki/RecipeML

wmheigl. (2025). _recipeml-implementation_. https://github.com/wmheigl/recipeml-implementation

NYT. (2016). _Ingredient phrase tagger_. https://github.com/nytimes/ingredient-phrase-tagger

Ingredient Parser. (2026). _ingredient-parser documentation_. https://ingredient-parser.readthedocs.io/

---

**Flagged/unverified items:**

- Tandoor’s JSON **file** import may not accept arbitrary schema.org JSON; schema.org support is primarily URL-based. This should be tested against the target Tandoor version.
- Recipe Keeper’s ability to import arbitrary schema.org JSON-LD was not verified; its documented export is schema-tagged HTML.
- Mealie’s ingredient section header support via `#`/`##` is documented in API/MCP tooling but was not verified across all UI/API versions.
- Paprika nutrition import coverage from schema.org was not fully verified.
- Open Recipe Format has very low adoption; no major app import was verified.
- Grocy recipe API payloads are database-object-oriented and may require pre-existing products/units; this is not a schema.org import path.
