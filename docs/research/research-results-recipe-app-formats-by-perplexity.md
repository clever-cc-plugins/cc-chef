# Recipe interchange for an AI cooking assistant

**Use schema.org Recipe JSON-LD as the primary exchange model, delivered both as a JSON file and as an ordinary recipe webpage. Add Paprika’s `.paprikarecipes` archive as the first offline compatibility format; use native API adapters where preserving structured ingredients matters more than minimizing integrations.** These routes are complementary: support for importing a recipe’s **URL does not imply support for opening its JSON-LD file**. [paprikaapp](https://www.paprikaapp.com/help/android/)

**Verification date:** November 1, 2026.

**Evidence boundary:** This is a documentation-and-source-code compatibility assessment, not an end-to-end import certification. Where the evidence establishes only an import route—not its behavior for every field—the report says so. No parser success rates or current market-share figures could be verified.

---

## 1. Schema.org Recipe — JSON-LD

### Required versus recommended properties

Three different requirements must be kept separate:

- **Schema.org vocabulary:** Defines properties and expected value types; the Recipe page does not prescribe a universal set of mandatory fields for recipe-management applications. [schema](https://schema.org/Recipe)
- **Google rich results:** Currently requires `name` and `image`, with additional conditional requirements and recommended properties. [schema](https://schema.org/Recipe)
- **Application importers:** Apply their own validation, defaults, supported subsets, and sometimes proprietary extensions. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

Google’s current recipe documentation explicitly lists **`name` and `image` as required**. Ingredients and instructions are recommended properties, even though an assistant should plainly require them for a usable cooking recipe. [schema](https://schema.org/Recipe)

| Property                  | Representation                                                                               | Google requirements and guidance                                                                                                                                             | Recommended exporter behavior                                                                       |
| ------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `@context`, `@type`       | `"https://schema.org"` and `"Recipe"`                                                        | Establish the vocabulary and type used in Google’s JSON-LD examples. [schema](https://schema.org/Recipe)                                                                     | Always include both.                                                                                |
| `name`                    | String                                                                                       | Required. [schema](https://schema.org/Recipe)                                                                                                                                | Require a nonempty title.                                                                           |
| `image`                   | URL, `ImageObject`, or multiple values                                                       | Required; images must represent the dish and be crawlable. Google recommends high-resolution images in 1:1, 4:3, and 16:9 aspect ratios. [schema](https://schema.org/Recipe) | Use an absolute HTTPS image URL. Do not invent an image when none exists.                           |
| `description`             | String                                                                                       | Recommended. [schema](https://schema.org/Recipe)                                                                                                                             | Plain text; keep cooking instructions elsewhere.                                                    |
| `recipeIngredient`        | Commonly an array of strings; current schema.org also permits `PropertyValue` and `ItemList` | Google documents ingredient **text**, not a portable structured quantity/unit/food contract. [schema](https://schema.org/Recipe)                                             | Export text strings for broad compatibility; retain structured ingredients internally.              |
| `recipeInstructions`      | Text, or ordered `HowToStep` / `HowToSection` structures                                     | Google recommends `HowToStep`; sections can group steps. [schema](https://schema.org/Recipe)                                                                                 | Use explicit steps, adding sections only when needed.                                               |
| `recipeYield`             | Text or `QuantitativeValue` in schema.org; Google also documents integer values              | Required when providing per-serving nutrition such as calories; Google recommends expressing serving count numerically. [schema](https://schema.org/Recipe)                  | A simple string such as `"4"` is a conservative common denominator.                                 |
| `prepTime`, `cookTime`    | ISO 8601 durations                                                                           | Recommended; Google says to use prep and cook times together. [schema](https://schema.org/Recipe)                                                                            | For example, `"PT15M"` and `"PT30M"`.                                                               |
| `totalTime`               | ISO 8601 duration                                                                            | Recommended; Google allows total time or the prep/cook combination. [schema](https://schema.org/Recipe)                                                                      | Preserve elapsed time, including resting or chilling where applicable.                              |
| `nutrition`               | `NutritionInformation` object                                                                | `nutrition.calories` is recommended; per-serving information requires a serving yield. [schema](https://schema.org/Recipe)                                                   | Include units and an explicit serving basis. Do not invent nutrition values.                        |
| `recipeCategory`          | Text                                                                                         | Recommended; describes meal/course, such as dessert or main course. [schema](https://schema.org/Recipe)                                                                      | Keep separate from general tags.                                                                    |
| `recipeCuisine`           | Text                                                                                         | Recommended; describes regional cuisine. [schema](https://schema.org/Recipe)                                                                                                 | Keep separate from category and tags.                                                               |
| `keywords`                | Text or other schema.org-supported values                                                    | Google recommends a comma-separated text list and says not to duplicate cuisine/category here. [schema](https://schema.org/Recipe)                                           | Use a comma-separated string for interoperability.                                                  |
| `author`, `datePublished` | Person/Organization; ISO-formatted date                                                      | Recommended. [schema](https://schema.org/Recipe)                                                                                                                             | Preserve known provenance.                                                                          |
| `inLanguage`              | BCP 47 language code or Language object                                                      | Defined by schema.org; not a Google recipe-specific required field. [schema](https://schema.org/Recipe)                                                                      | Include, for example, `"de-DE"`. Do not assume it controls the importer’s ingredient parser.        |
| `url`, `identifier`       | URL; identifier value                                                                        | Defined by schema.org. [schema](https://schema.org/Recipe)                                                                                                                   | Use stable identifiers for reconciliation, without assuming the receiving app deduplicates on them. |

**Important recent distinction:** The checked schema.org Recipe page, version **30.1, dated September 16, 2026**, permits structured ingredients through `PropertyValue` and `ItemList`. That does **not** establish widespread application support; Google’s recipe documentation still describes the interoperable ingredient representation as text. [schema](https://schema.org/Recipe)

### Ingredients and ingredient sections

For broad import compatibility, prefer:

```json
"recipeIngredient": [
  "250 g flour",
  "150 ml water",
  "5 g salt"
]
```

Schema.org can express more structure, for example an ingredient as a `PropertyValue` with `name`, `value`, and `unitCode` or `unitText`. However, the checked application evidence does not establish reliable cross-app support for that representation. [schema](https://schema.org/Recipe)

**Ingredient sections are a weak point.** Current schema.org allows `ItemList`, but there is no verified, widely implemented ingredient-group convention across the requested apps. Paprika, for example, uses a presentation convention: an ingredient line ending in a colon becomes a heading. [paprikaapp](https://www.paprikaapp.com/help/android/)

**Recommendation:** Keep ingredient groups as first-class objects internally. Flatten them only in a target-specific renderer; do not assume that `"Sauce:"` in `recipeIngredient` will be recognized as a heading rather than an ingredient.

### Instructions and sections

A portable step is:

```json
{
  "@type": "HowToStep",
  "name": "Mix",
  "text": "Mix the flour, water, and salt."
}
```

A section groups steps through `itemListElement`:

```json
{
  "@type": "HowToSection",
  "name": "Prepare the dough",
  "itemListElement": [
    {
      "@type": "HowToStep",
      "text": "Mix the flour, water, and salt."
    },
    {
      "@type": "HowToStep",
      "text": "Knead until smooth."
    }
  ]
}
```

Google requires a section’s `name` and `itemListElement`; a step needs `text` or the documented substep representation. Step names, images, and URLs are optional enhancements. [schema](https://schema.org/Recipe)

Do not include redundant labels such as “Step 1” or “Directions” inside step text. Google explicitly advises keeping those labels outside the structured instructional text. [schema](https://schema.org/Recipe)

### Yield, time, nutrition, and images

Use durations such as `PT45M`, `PT1H30M`, or `P1D`, not display strings such as `"90 minutes"` in schema.org duration fields. [schema](https://schema.org/Recipe)

For nutrition, use a typed object with units:

```json
"nutrition": {
  "@type": "NutritionInformation",
  "servingSize": "1 serving",
  "calories": "420 kcal",
  "proteinContent": "18 g",
  "fatContent": "12 g",
  "carbohydrateContent": "58 g"
}
```

The values above illustrate **syntax only**, not calculated nutrition. Google interprets calories as per serving and requires an appropriate `recipeYield` when per-serving nutrition is supplied. [schema](https://schema.org/Recipe)

Schema.org accepts image URLs or `ImageObject` values. For app interoperability, an absolute image URL is the least complicated representation; embedded base64 images belong in formats that explicitly support them, such as the inspected Paprika import implementation. [paprikaapp](https://www.paprikaapp.com/help/android/)

### Recommended JSON-LD profile

This is an original interoperability fixture, not an app-tested reference file:

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "identifier": "urn:uuid:00000000-0000-4000-8000-000000000001",
  "name": "Simple flatbread",
  "description": "A basic flour-and-water flatbread.",
  "inLanguage": "en",
  "recipeYield": "4",
  "prepTime": "PT15M",
  "cookTime": "PT15M",
  "totalTime": "PT30M",
  "recipeCategory": "Bread",
  "keywords": "simple, stovetop",
  "recipeIngredient": ["250 g flour", "150 ml water", "5 g salt"],
  "recipeInstructions": [
    {
      "@type": "HowToSection",
      "name": "Prepare",
      "itemListElement": [
        {
          "@type": "HowToStep",
          "text": "Mix the flour, water, and salt."
        },
        {
          "@type": "HowToStep",
          "text": "Knead until smooth, then divide into four pieces."
        }
      ]
    },
    {
      "@type": "HowToSection",
      "name": "Cook",
      "itemListElement": [
        {
          "@type": "HowToStep",
          "text": "Roll out each piece and cook in a hot pan on both sides."
        }
      ]
    }
  ]
}
```

This deliberately omits images and nutrition rather than supplying fabricated data. It is a usable interchange profile, but without a real `image` it does not meet Google’s documented rich-result requirements. [schema](https://schema.org/Recipe)

### Delivery paths and robustness

| Application                           | Schema.org delivery route established                                                             | Qualification                                                                                                                                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mealie                                | URL; pasted HTML or JSON; REST endpoint accepting raw HTML/schema JSON                            | Explicitly documented in source. Native Mealie JSON is a separate representation. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)                        |
| Crouton                               | URL; pasted schema data; individual JSON files; ZIP archives; Shortcuts creation from schema data | Explicitly advertised in current App Store release notes. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)                                                              |
| Nextcloud Cookbook                    | URL metadata import; schema-oriented recipe JSON through its API and storage model                | Do not confuse its filesystem/API representation with a generic browser file-upload feature. [apps.nextcloud](https://apps.nextcloud.com/apps/cookbook/)                                                                |
| Tandoor                               | Website import; JSON-LD file migration through the named RecipeSage integration                   | RecipeSage export compatibility does not prove that every arbitrary standalone JSON-LD file is accepted unchanged. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                        |
| Recipya                               | URL scraper with a schema model; JSON file processing exists                                      | The precise JSON variants accepted by a particular release need fixtures; Go and Rust implementations must be evaluated separately. [github](https://github.com/reaper47/recipya/blob/main/internal/scraper/scraper.go) |
| KitchenOwl                            | Website scraping, with schema.org fallback reported for its scraping stack                        | Raw schema JSON file import was not verified as a user-facing feature. [repocloud](https://repocloud.io/details/KitchenOwl/)                                                                                            |
| Paprika, Mela, Recipe Keeper, AnyList | Website/browser/share import                                                                      | General website import is documented; a complete schema.org parser contract is not public in the reviewed evidence. [paprikaapp](https://www.paprikaapp.com/help/android/)                                              |

**Robustness cannot be reduced to a supported/unsupported checkbox.** Mealie and Crouton explicitly expose structured-data input, whereas the closed-source web clippers publish much less about accepted JSON-LD shapes. None of the reviewed documentation provides a reproducible multilingual, section-preservation, or nutrition-preservation benchmark. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)

For a hosted compatibility page, the conservative design is server-rendered HTML containing visible recipe content and one straightforward JSON-LD Recipe object. Avoid making import depend on client-side JavaScript, login, expiring image URLs, or a complex graph.

---

## 2. App-by-app import support

### Version and maintenance status

Repository snapshots below identify what was inspected; they are **not claims that the development branch equals the latest stable release**.

| App                | Checked version or source snapshot                                                                                                         | Existence and maintenance assessment                                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tandoor Recipes    | [`cbb96e1`](https://github.com/TandoorRecipes/recipes/commit/cbb96e1), development snapshot, October 27, 2026                              | Exists; recent source activity establishes active development.                                                                                                                                   |
| Mealie             | [`a18e63d`](https://github.com/mealie-recipes/mealie/commit/a18e63d), November 1, 2026                                                     | Exists; active development. Current-source features may precede a stable release. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py) |
| Recipya, Go        | [`f8d13a0`](https://github.com/reaper47/recipya/commit/f8d13a0), November 1, 2026                                                          | Exists; maintained alongside a Rust rewrite. [github](https://github.com/reaper47/recipya/discussions/422)                                                                                       |
| Recipya, Rust      | [`fdb745a`](https://github.com/reaper47/recipya-rs/commit/fdb745a), nightly snapshot, October 31, 2026                                     | Active rewrite; the Go project README warns that the Rust replacement is not production-ready. [github](https://github.com/reaper47/recipya/discussions/422)                                     |
| kitshn             | Release marker **2.1.5**, October 25, 2026                                                                                                 | Exists; actively developed Tandoor client, not an independent recipe backend. [github](https://github.com/kitshn-app/kitshn/commit/07c004f8790bf3a80abc59e8612af5799060dc28)                     |
| ManageMeals        | API repository snapshot [`dc86f9b`](https://github.com/managemeals/manage-meals-api/commit/dc86f9b), tagged **v1.9.3**, September 25, 2026 | Exists; recent backend activity. Public integration documentation is comparatively limited. [github](https://github.com/managemeals/manage-meals-web)                                            |
| Nextcloud Cookbook | App Store lists **0.11.12**; source snapshot [`e291863`](https://github.com/nextcloud/cookbook/commit/e291863), November 1, 2026           | Exists; maintained. App version and API specification version are different numbers. [apps.nextcloud](https://apps.nextcloud.com/apps/cookbook/)                                                 |
| KitchenOwl         | [`4aea8ee`](https://github.com/TomBursch/kitchenowl/commit/4aea8ee), November 1, 2026                                                      | Exists; recent activity; official documentation explicitly describes it as actively maintained. [docs.kitchenowl](https://docs.kitchenowl.org/)                                                  |
| Grocy              | Official repository and API routes checked; exact current release **unverified**                                                           | Exists. Recent-release maintenance status was not conclusively established by the reviewed release evidence. [github](https://github.com/grocy/grocy/blob/master/routes.php)                     |
| Paprika            | **Paprika 3** documentation; separate **Paprika 4 beta** documentation                                                                     | Exists; the beta documentation establishes ongoing product development. Do not silently apply beta-only behavior to version 3. [paprikaapp](https://www.paprikaapp.com/help/android/)            |
| Mela               | Official product/help presence; exact current build **unverified**                                                                         | Exists. A recent version number and update date were not independently established. [mela](https://mela.recipes/)                                                                                |
| Crouton            | Current App Store history includes schema JSON/JSON-LD importing; exact build **unverified**                                               | Exists; release history establishes ongoing development. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)                                        |
| Recipe Keeper      | Official product site; exact current build **unverified**                                                                                  | Exists. Current maintenance cadence was not conclusively established. [recipekeeperonline](https://recipekeeperonline.com/)                                                                      |
| AnyList            | Official product/help pages; exact current build **unverified**                                                                            | Exists. Current release number and release date were not established. [help.anylist](https://help.anylist.com/articles/feature-overview-recipe-import-android/)                                  |

### Tandoor Recipes

**Import paths.** Tandoor has an extensive file-migration system covering its own archive, Nextcloud Cookbook, Mealie, Paprika, RecipeSage JSON-LD, Meal-Master, Cooklang, Mela, Cookmate, Recipe Keeper, and numerous other app exports. Its default importer expects the exported **ZIP archive**, not merely an extracted JSON file. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

**Required fields and structure.** The inspected recipe serializer exposes a recipe name and nested steps; each step has an ingredient collection. Ingredient objects include `amount`, `unit`, `food`, `note`, `order`, `is_header`, `no_amount`, and `original_text`, which makes the native representation substantially richer than flat ingredient strings. See the [inspected serializers](https://github.com/TandoorRecipes/recipes/blob/cbb96e1/cookbook/serializer.py).

**Fidelity.** Native data can represent ingredient headings, step allocation, explicit units and quantities, nutrition, keywords, and images. The importer determines what survives: Cooklang currently has no image import, while Paprika, Mealie, Nextcloud, and several other integrations support images. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

**Languages and parsing.** Native food/unit names and original ingredient text should be distinguished from successful language-aware parsing. No comprehensive locale/fraction/range benchmark was verified; use the API’s structured fields when deterministic interpretation matters.

**Important migration caveat:** Tandoor distinguishes Mealie backups from before and after version 1.0 and warns that Mealie nutrition’s per-serving versus per-recipe basis must be selected during import. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

### Mealie

**Import paths.** Mealie supports recipe URLs and pasted HTML/JSON. Its documented migration sources include Tandoor, Nextcloud Cookbook, Paprika, Chowdown, Plan to Eat, Recipe Keeper, Copy Me That, My Recipe Box, and DVO Cook’n X3. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

**Required fields and API model.** Treat recipe creation, schema scraping, and native recipe replacement as separate operations. The raw structured-data endpoint takes a `data` string; native Mealie recipes carry additional structure such as ingredient references, food/unit objects, organizers, and step links. [github](https://github.com/mealie-recipes/mealie/pull/8651)

**Fidelity.** Current source includes a dedicated path for recognizing a complete Mealie recipe dump and preserving foods, units, step titles, ingredient links, notes, tools, tags, and categories. That path is deliberately different from schema.org scraping, which rebuilds a recipe from the web-oriented representation. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

**Version caveat.** The full-structure pasted-native-export enhancement appears in an October 2026 change. Verify that the user’s installed release includes it rather than assuming all Mealie versions behave like the checked branch. [github](https://github.com/mealie-recipes/mealie/pull/8651)

**Parsing.** Mealie has ingredient parsing separate from merely saving the original lines. The inspected NLP call invokes `parse_ingredient` with database custom units but no explicit locale argument; multilingual correctness therefore needs independent validation. The project’s user survey also records substantial variation in perceived parser quality, but that is feedback—not a benchmark. [docs.mealie](https://docs.mealie.io/news/surveys/2024-october/q12/)

### Recipya

**Import paths.** The established Go app supports website import and migration from Mealie, Tandoor, and Nextcloud Cookbook. Inspected file handling additionally includes JSON, Paprika archives, MasterCook processing, and Crouton files; see the [Go import implementation](https://github.com/reaper47/recipya/blob/f8d13a0/internal/services/files_apps.go). [github](https://github.com/reaper47/recipya/blob/main/internal/scraper/scraper.go)

**Required fields.** The website scraper uses a `RecipeSchema` model and fills defaults such as missing schema context/type and source URL. A definitive minimum field set across every file importer was not verified. [github](https://github.com/reaper47/recipya/blob/main/internal/scraper/scraper.go)

**Fidelity.** The Paprika importer reads embedded `photo_data` or falls back to an image URL. Recipya advertises measurement-system conversion and automatic nutritional calculation, but those capabilities should not be equated with lossless preservation of imported nutrition or ingredient parsing.

**Sections and versions.** Ingredient-group support has been discussed explicitly as incomplete in the Go implementation, with groundwork in the Rust rewrite. Do not transfer features from `recipya-rs` into a Go-release compatibility claim. [github](https://github.com/reaper47/recipya/discussions/422)

**API.** A stable, documented external recipe-creation API contract was not verified. Treat automation against internal routes as a version-pinned adapter, not a public-standard integration.

### kitshn

**Architecture.** kitshn is a client for Tandoor; its persistent recipe model and server-side import behavior come from the connected Tandoor instance. [github](https://github.com/kitshn-app/kitshn/commit/07c004f8790bf3a80abc59e8612af5799060dc28)

**Import paths.** The app supports creating/editing recipes and receiving shared recipe URLs. That establishes a convenient mobile route into Tandoor, not an independently verified general-purpose file importer. [play.google](https://play.google.com/store/apps/details?id=de.kitshn.android&hl=en_GB)

**Fidelity.** Ingredient-step allocation, Markdown, and editing are client features; backend-supported units, sections, images, nutrition, and keywords remain governed by Tandoor and the particular import path. [play.google](https://play.google.com/store/apps/details?id=de.kitshn.android&hl=en_GB)

**Implementation consequence:** Count kitshn as **Tandoor coverage**, not as a second backend requiring a separate exchange format.

### ManageMeals

**Import paths.** ManageMeals is a real, self-hostable application with a SvelteKit frontend and a separate backend. URL import is its clearly established recipe-acquisition route. [github](https://github.com/managemeals/manage-meals-web)

**File/API support.** A published, stable bulk recipe-file contract was not verified. The backend wiki lists import/export and bulk import as work items, so those should not be promised merely because the application itself has an API. [github](https://github.com/managemeals/manage-meals-api/wiki/TODO)

**Required fields and fidelity.** Exact create payload, ingredient-group handling, quantity/unit parsing, nutrition preservation, tag mapping, and image import rules remain **unverified** in this assessment.

**Recommendation:** Start with the URL route and a small compatibility test set; defer a native adapter until its authentication and request schemas are pinned to an installed version.

### Nextcloud Cookbook

**Import paths.** Its documented API exposes a website import operation based on schema.org metadata and a recipe-creation operation accepting a JSON recipe representation. Its stored recipe collections use recipe folders containing `recipe.json` and associated images. [apps.nextcloud](https://apps.nextcloud.com/apps/cookbook/)

**Required fields.** The checked OpenAPI specification documents missing `name` as a recipe-creation error. See the [API specification](https://github.com/nextcloud/cookbook/blob/e291863/docs/dev/api/0.1.3/openapi-cookbook.yaml).

**Fidelity.** Its schema-oriented model is a good fit for text ingredients, instructions, durations, nutrition, keywords, category, and image references. It is not equivalent to Tandoor’s food/unit database model; structured ingredient identities and sections need particular care.

**File route caveat.** Writing/importing a recipe through Nextcloud storage and reindexing is different from uploading an arbitrary `.json` file through the Cookbook web interface. Do not advertise the latter without checking the installed UI.

**Languages.** Preserve UTF-8 content and language metadata where accepted, but do not assume unit normalization or locale-aware ingredient parsing merely because the recipe text is multilingual.

### KitchenOwl

**Import paths.** KitchenOwl supports URL-based recipe acquisition and has a documented API ecosystem. The reviewed native import function consumes KitchenOwl-specific dictionaries rather than schema.org Recipe objects. [repocloud](https://repocloud.io/details/KitchenOwl/)

**Required fields.** In the inspected native importer, `name` and `description` are accessed directly. Optional fields include times, yield, source, photo, items, and tags; each supplied item is read through `name`, `description`, and `optional`. See the [native importer](https://github.com/TomBursch/kitchenowl/blob/4aea8ee/backend/app/service/importServices/import_recipe.py).

**Fidelity.** Ingredients are associated with household items, while their recipe-specific description carries additional information. That is not the same contract as separate numeric quantity and unit fields. Photos and tags are explicitly handled by the inspected importer; nutrition and ingredient sections are not handled there.

**Languages.** Item naming and recipe text should be tested separately from NLP extraction. A translated interface or multilingual item collection does not establish reliable parsing of arbitrary ingredient prose.

### Grocy

**Architecture.** Grocy is inventory-oriented: recipes refer to products and quantities rather than functioning purely as text recipe documents. Its maintainers explicitly describe creating recipes and ingredient positions through generic entity API routes. [github](https://github.com/grocy/grocy/issues/544)

**Import paths.** A core, general-purpose schema.org/Paprika/Cooklang file importer was not verified. The established automation route is to create a recipe, then create associated `recipes_pos` records. [github](https://github.com/grocy/grocy/issues/544)

**Required fields and fidelity.** A basic recipe can be created with `name` and `description`; ingredient positions refer to `recipe_id`, `product_id`, and `amount`. Current source also includes ingredient grouping and quantity-unit relationships. [github](https://github.com/grocy/grocy/blob/7d15c46b/migrations/0249.sql)

**Nutrition, images, and tags.** The checked source calculates recipe calories from product data. That is not equivalent to preserving a full imported `NutritionInformation` object; image and general tag mappings require additional, version-specific work. [github](https://github.com/grocy/grocy/blob/7d15c46b/migrations/0249.sql)

**Implementation consequence:** Grocy needs an adapter with product/unit reconciliation. An additional export file alone will not solve that mapping problem.

### Paprika

**Import paths.** Paprika 3 documents `.paprikarecipe`, `.paprikarecipes`, MasterCook `.mx2`/`.mxp`/`.mz2`, Meal-Master `.mmf`, Living Cookbook `.fdx`/`.fdxz`, `.yml`, Cook’n `.dvo`, and Pepperplate `.db` imports. Website clipping and manual clipboard-assisted capture are separate paths. [paprikaapp](https://www.paprikaapp.com/help/android/)

**Required fields.** For its documented YAML input, `name`, `ingredients`, and `directions` are required; most other fields are optional. The guide recommends UTF-8 and correct YAML indentation. [paprikaapp](https://www.paprikaapp.com/help/android/)

**Ingredient sections and parsing.** Ingredient headings end with a colon, such as `Sauce:`. Paprika explicitly recommends the order **quantity → unit → ingredient**, such as `1 cup milk`, for scaling and conversion. [paprikaapp](https://www.paprikaapp.com/help/android/)

**Fidelity.** Paprika has category hierarchies, text nutrition, multiple photos, and formatted recipe text. It documents resizing photos to a maximum of 2048 × 2048 pixels; consequently, its export should not be treated as a preservation master for original photographs. [paprikaapp](https://www.paprikaapp.com/help/android/)

**API and version caveat.** No supported public recipe-creation REST API was verified. Paprika 4 beta introduces additional capabilities, including clipboard recipe interpretation, but these are not a Paprika 3 baseline. [paprikaapp](https://www.paprikaapp.com/help/v4/android/)

### Mela

**Import paths.** Mela documents its in-app browser, sharing extension, RSS-based recipe discovery, and text recognition from books. Its native files are `.melarecipe` and `.melarecipes`; Tandoor’s official migration documentation confirms the collection archive’s nested-file structure. [mela](https://mela.recipes/)

**Native structure.** A `.melarecipe` is described in third-party implementations as JSON with title, text ingredients/instructions, categories, times, yield, notes, nutrition, source link, and base64 images. A collection is a ZIP containing individual recipe files, potentially with nesting. [github](https://github.com/regg00/mela-recipe-paul)

**Confidence limitation.** Those field-level details were **not independently confirmed against a reviewed official Mela file-format specification**. Treat them as an implementation lead requiring fixture validation, not an authoritative schema.

**Sections and fidelity.** Third-party format analysis identifies `#`-prefixed ingredient headings and text-based nutrition. Exact required fields, unit parsing, multilingual edge cases, and generic schema JSON-file import remain unverified. [github](https://github.com/vrih/recipe-store/blob/main/docs/PRD.md)

**API.** No public recipe-creation REST API was verified.

### Crouton

**Import paths.** Current App Store release notes explicitly state support for **schema.org Recipe JSON or JSON-LD**, pasted structured data, individual JSON files, and ZIP archives from **Settings → Import Recipes**. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)

**Automation.** The same release history describes expanded Shortcuts functionality, including creating recipes from schema data. This is a relevant local automation path even without a public REST API. [apps.apple](https://apps.apple.com/in/app/crouton-recipe-manager/id1461650987?l=mr&platform=mac)

**Fidelity and parsing.** Crouton documents recipe scaling and metric/imperial conversion; release notes also mention improved handling of ingredient lines with quantity after the ingredient, such as “Olive oil, 2 tbsp.” [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)

**Unverified details.** The exact minimum schema fields, preservation of nested ingredient sections, full nutrition mapping, and tag/category behavior were not established. Also verify the installed version: direct schema-file importing should not be assumed for older builds.

### Recipe Keeper

**Import paths.** The official site documents pasted recipes, website import, importing from other recipe applications, photos, and organization by course/category. [recipekeeperonline](https://recipekeeperonline.com/)

**File-format limitation.** The reviewed official material does not provide a sufficiently precise importer extension/version list to certify arbitrary Paprika, MasterCook, or schema JSON files. Tandoor documents importing Recipe Keeper’s exported ZIP, but **export readability in Tandoor does not prove the reverse import route**. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

**Required fields and fidelity.** Minimum required fields, ingredient-section rules, normalized quantity/unit storage, multilingual parsing, and nutrition import mapping remain unverified. Categories and photos exist as product features, but their survival through each import route needs testing. [recipekeeperonline](https://recipekeeperonline.com/)

**API.** No supported public recipe-creation API was verified.

### AnyList

**Import paths.** AnyList officially documents recipe import from websites through mobile sharing and desktop browser extensions. It also imports its own recipe files received through email or messaging. [help.anylist](https://help.anylist.com/articles/feature-overview-recipe-import-android/)

**Limits.** The documented free allowance is five web-imported recipes; unlimited web recipe import requires AnyList Complete. [help.anylist](https://help.anylist.com/articles/getting-started/)

**Sections.** AnyList supports ingredient headings and offers a command to convert an imported ingredient into a heading. This establishes a heading model, but not automatic recognition of every source-site section. [help.anylist](https://help.anylist.com/articles/recipe-ingredient-headings/)

**Unverified details.** A public native-file schema, generic JSON-LD file importer, supported REST creation API, nutrition mapping, and multilingual parser contract were not verified. Do not confuse the native attachment route with a documented open interchange format. [help.anylist](https://help.anylist.com/articles/open-recipe-file/)

### Additional ecosystem applications

**RecipeSage is worth including as a direct JSON-LD target.** Tandoor’s official documentation explicitly instructs users to export RecipeSage as JSON-LD and also describes importing Tandoor-generated RecipeSage JSON back into RecipeSage; it warns that Tandoor’s RecipeSage export does not currently include images. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

**Cookmate, Plan to Eat, and Copy Me That are relevant migration ecosystems**, because Tandoor and/or Mealie explicitly provide importers for their exports. However, their inbound format lists, current maintenance versions, and current user counts were not independently verified here; they should not be added to a guaranteed inbound-coverage total. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

No defensible current ranking by users was established. Repository stars, store ratings, installed copies, registered accounts, and monthly active users are different measurements; this report does not substitute one for another.

---

## 3. Open and legacy interchange formats

### Format characteristics and adoption

| Format                          | Structure and strengths                                                                                                                                                                                                                   | Verified adoption in this assessment                                                                                                                                                                    | Main limitations                                                                                                                                                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Cooklang**                    | Plain `.cook` text; inline ingredients, quantities, units, cookware, timers, steps, sections, and metadata. [github](https://github.com/lexi2042/cooklang-spec)                                                                           | Active Cooklang tooling; Tandoor imports `.cook`. [cooklang](https://cooklang.org/docs/getting-started/)                                                                                                | Not a broad replacement for JSON-LD among the requested consumer apps. Tandoor’s importer currently lacks images and ZIP import. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                 |
| **Paprika archive**             | `.paprikarecipes` is a ZIP containing gzip-compressed JSON recipe files. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                                                           | Paprika; Tandoor; Mealie; inspected Recipya importer. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                                            | App-specific contract; ingredients and nutrition are substantially text-oriented.                                                                                                                                              |
| **MasterCook MXP**              | Legacy text exchange format; do not confuse it with MasterCook cookbook databases.                                                                                                                                                        | Paprika explicitly lists `.mxp`; Recipya contains MasterCook file processing. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                    | Exact dialect and field-preservation rules require fixtures.                                                                                                                                                                   |
| **MasterCook MX2 / MZ2**        | MasterCook exchange formats; MX2 is the XML-oriented family, while MZ2 is an associated packaged variant.                                                                                                                                 | Paprika explicitly lists both. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                                                                   | A current authoritative byte-level specification was not verified. Do not infer image support solely from the extension.                                                                                                       |
| **Meal-Master**                 | Legacy text format with recipe headers and quantity/unit/ingredient lines.                                                                                                                                                                | Paprika; Tandoor. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                                                                                | Variants matter: Tandoor supports one-column ingredients and moves second-line ingredient notes into instructions. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                               |
| **RecipeML 0.5**                | XML with a DTD; structured ingredient amounts/units/items and step-based directions. [formatdata](http://formatdata.com/recipeml/dtd.html)                                                                                                | Historical implementations and current community tooling exist; no importer among the core requested apps was conclusively verified here. [formatdata](http://www.formatdata.com/recipeml/gallery.html) | Legacy ecosystem; poor evidence of broad current app coverage.                                                                                                                                                                 |
| **Open Recipe Format**          | YAML with `recipe_name`, ingredients, explicit amounts/units, steps, yields, notes, and richer optional metadata. [open-recipe-format.readthedocs](https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html) | Specification documentation exists; no requested-app importer verified. [open-recipe-format.readthedocs](https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html)         | Documentation checked shows a 2016 copyright/revision; active widespread adoption was not established. [open-recipe-format.readthedocs](https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html) |
| **Tandoor native archive**      | ZIP containing Tandoor’s structured recipe data and associated assets. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                                                      | Tandoor; Mealie migration; Recipya migration. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                                             | Excellent native fidelity, but app/version-specific.                                                                                                                                                                           |
| **Mealie export/backup**        | Recipe exports and server backups are distinct artifacts; migration tools may require one specifically. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                     | Mealie-native workflows; Tandoor and Recipya migration paths. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                             | Backup layout and version matter; not a generic schema JSON interchange contract.                                                                                                                                              |
| **Nextcloud recipe collection** | Recipe directories containing `recipe.json` and images, commonly transferred as ZIP. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                                        | Nextcloud-native storage; Tandoor; Mealie; Recipya migration. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                             | Directory layout and image filenames matter.                                                                                                                                                                                   |
| **Mela native files**           | Individual recipe JSON and collection ZIP archives. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                                                                         | Mela ecosystem; Tandoor imports individual `.melarecipe` files. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                                           | Field-level official specification was not independently verified.                                                                                                                                                             |

**MasterCook caution:** `.mc2` and `.mcx` are cookbook storage files, not interchangeable names for `.mx2` or `.mxp`. MasterCook’s own support documentation describes `.mc2` as recipe text storage with `.mcx` as its photo companion. [support.mastercook](https://support.mastercook.com/hc/en-us/articles/216889146-Adding-Cookbook-Files-to-MasterCook)

### Cooklang specification and tooling

Cooklang embeds machine-readable information directly in readable instructions:

```cook
---
title: Simple dough
servings: 4
tags: [bread, simple]
---

== Dough ==

Mix @flour{250%g}, @water{150%ml}, and @salt{5%g} in a #bowl.

Rest for ~{20%minutes}.
```

Ingredients use `@`, cookware uses `#`, timers use `~`, quantities appear inside braces, and `%` separates a quantity from its unit. Paragraphs define steps, and section markers group related preparation work. [github](https://github.com/lexi2042/cooklang-spec)

Current Cooklang guidance recommends YAML frontmatter for metadata. Tooling includes CookCLI, parsers in several programming languages, and a language server with editor diagnostics and completion. [cooklang](https://cooklang.org/docs/getting-started/)

**Assessment:** Cooklang is a strong authoring and archival format for text-first users. It is not the smallest route to broad compatibility with Paprika, AnyList, Recipe Keeper, and the other proprietary apps.

### Paprika archive details

The documented outer structure is:

```text
recipes.paprikarecipes        ZIP
├── recipe-a.paprikarecipe    gzip-compressed JSON
└── recipe-b.paprikarecipe    gzip-compressed JSON
```

Paprika’s own guide describes the ZIP/gzipped-JSON packaging, and Tandoor’s migration documentation independently confirms it. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

The inspected Recipya implementation expects recognizable Paprika fields and handles embedded `photo_data` or an image URL. That is useful implementation evidence, but it is not a vendor commitment that every historical or future Paprika field remains unchanged.

**Implementation recommendation:** Generate the smallest validated subset first—title, ingredient text, directions, source, servings, times, categories, and an optional image—then add fields only after round-trip tests against actual target versions.

### Native archives are not universal backups

Tandoor’s default ZIP is intended to carry its full native recipe data. Its documentation explicitly says that importing the extracted JSON alone is unsupported. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

Mealie distinguishes data exports from server backups, and Tandoor’s Mealie migration instructions specifically request a backup ZIP rather than a recipe-only export. Consequently, “Mealie JSON support” is not a sufficiently precise compatibility claim. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

**Recommendation:** Do not make your assistant manufacture full application backups merely to create one recipe. Use a recipe-level API or a documented interchange importer.

---

## 4. Ingredient parsing

### Text preservation versus semantic parsing

A successful import can mean either:

1. The app saved `"1 1/2 cups flour, sifted"` as text.
2. The app extracted quantity `1.5`, unit `cup`, food `flour`, and note `sifted`.

Those are different capabilities. Tandoor exposes explicit ingredient fields, Paprika documents a preferred text order for scaling, and KitchenOwl’s inspected importer instead associates an item name with a recipe-specific description. [paprikaapp](https://www.paprikaapp.com/help/android/)

| App or approach                      | Established behavior                                                                                                                                                                                          | What should not be assumed                                                    |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Tandoor native API                   | Explicit amount, food, unit, note, heading flag, and original text in the inspected serializer.                                                                                                               | That every free-text importer parses every language or range correctly.       |
| Mealie                               | Separate ingredient parsing; structured food/unit/reference data in the native model. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md) | That importing JSON-LD automatically produces correct normalized ingredients. |
| Recipya                              | Advertises measurement conversion; separate Go/Rust implementations and section-development history. [github](https://github.com/reaper47/recipya/issues/517)                                                 | That conversion support proves robust multilingual extraction.                |
| KitchenOwl                           | Native importer reads item name plus description/optional state.                                                                                                                                              | A universal quantity/unit/food/note tuple.                                    |
| Paprika                              | Recommends `quantity unit ingredient`; supports scaling, conversion, and colon headings. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                               | That arbitrary prose order or every localized unit is recognized.             |
| Crouton                              | Documents scaling/conversion and improved trailing-quantity parsing. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)                                         | A published accuracy guarantee for fractions, ranges, or languages.           |
| Closed-source web clippers generally | Can extract recipes from supported sites. [help.anylist](https://help.anylist.com/articles/feature-overview-recipe-import-android/)                                                                           | A documented semantic ingredient parser or lossless section preservation.     |

### Non-English ingredients

The biggest distinction is **Unicode text support versus linguistic interpretation**. Keeping “1 EL Olivenöl” intact is much easier than recognizing `EL`, identifying a tablespoon, resolving a canonical food, and correctly scaling the result.

The checked evidence does not establish a comprehensive multilingual parser contract for any of the requested apps. Mealie’s survey contains requests for better multilingual ingredients and unit aliases, which reinforces the need for testing rather than a blanket compatibility claim. [docs.mealie](https://docs.mealie.io/news/surveys/2024-october/q12/)

**Recommended design:** Keep recipe language, display unit, canonical unit, and original text as separate fields. Do not translate an ingredient solely to make an English-oriented parser happier.

### Fractions, ranges, and unit systems

The following are **export conventions recommended for your assistant**, not measured guarantees:

| Input issue               | Recommended convention                                                                                                                              |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fractions                 | Preserve exact rational values internally. For text output, start with ASCII fractions such as `1/2` or `1 1/2`; test Unicode fractions separately. |
| Decimal separator         | Use JSON numbers with a decimal point in native numeric payloads. Apply decimal commas only in localized display strings.                           |
| Ranges                    | Preserve both bounds and the original line. Do not silently replace `2–3` with a midpoint or lower bound.                                           |
| Missing quantity          | Model “to taste” or “as needed” explicitly; do not turn it into a fabricated numeric quantity.                                                      |
| Counted ingredients       | Keep count and size distinct: `2 onions, medium`, rather than encoding size into the unit.                                                          |
| Package sizes             | Distinguish package count from package mass: `2 cans`, each `400 g`.                                                                                |
| Alternatives              | Preserve alternatives in notes or a dedicated internal structure; do not present “butter or oil” as one canonical food.                             |
| Metric/imperial           | Keep original units and unit-system provenance. Distinguish mass ounces from fluid ounces and US measures from Imperial measures.                   |
| Volume-to-mass conversion | Require ingredient-specific conversion data; do not treat a cup as a universal mass.                                                                |
| Preparation notes         | Place notes after the food, for example `250 g carrots, finely diced`.                                                                              |
| Ingredient sections       | Use native heading/group fields where available; otherwise apply the target app’s convention.                                                       |

Paprika’s explicit preferred order supports adopting **quantity → unit → ingredient → note** as the initial common text renderer. Its colon-heading rule should remain a Paprika-specific formatting rule, not a schema.org assumption. [paprikaapp](https://www.paprikaapp.com/help/android/)

### Suggested acceptance fixtures

Before declaring an adapter supported, test at least:

```text
250 g flour
1 1/2 tbsp olive oil
0.5 l milk
2-3 cloves garlic, crushed
2 cans tomatoes, 400 g each
salt, to taste
1 EL Olivenöl
1,5 kg Kartoffeln, geschält
½ TL Salz
Sauce:
```

Test four outcomes separately: **display preservation, parsed fields, scaling, and shopping-list aggregation**. A visually correct import can still fail the last three.

---

## 5. API-based import for self-hosted apps

### API overview

| App                   | Recipe creation/import route                                                                | Authentication                                                                                                                                             | Payload strategy                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Tandoor               | `POST /api/recipe/`; separate image handling in the inspected serializers                   | Token authentication with read/write scope in current source; confirm the authorization scheme against the installed instance                              | Native nested recipe/step/ingredient objects.                                                                                  |
| Mealie                | `POST /api/recipes/create/html-or-json`; `POST /api/recipes/create/url`; native recipe CRUD | Bearer authentication in published OpenAPI. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py) | Use schema input for convenience; native recipe structure for maximum fidelity.                                                |
| Nextcloud Cookbook    | `POST /apps/cookbook/api/v1/recipes`; `POST /apps/cookbook/api/v1/import`                   | HTTP Basic in checked OpenAPI; use a Nextcloud app password                                                                                                | Schema-oriented recipe object or URL object.                                                                                   |
| KitchenOwl            | Household-scoped recipe API; exact deployed contract must be checked                        | Version-specific token/session contract not fully verified                                                                                                 | Native KitchenOwl payload, not schema.org directly. [docs.kitchenowl](https://docs.kitchenowl.org/)                            |
| Grocy                 | `POST /api/objects/recipes`, then `POST /api/objects/recipes_pos`                           | Grocy API key; confirm header and permissions in instance API documentation                                                                                | Create recipe, resolve products/units, add ingredient records. [github](https://github.com/grocy/grocy/blob/master/routes.php) |
| Recipya / ManageMeals | Internal application routes exist                                                           | Stable external integration contract not verified                                                                                                          | Pin an adapter only after reviewing the installed version.                                                                     |

### Tandoor

The inspected source uses a native nested serializer, with recipe steps containing ingredient objects. It also exposes an image serializer separately; `image` is read-only on the main recipe serializer. See the [recipe serializers](https://github.com/TandoorRecipes/recipes/blob/cbb96e1/cookbook/serializer.py) and [API views](https://github.com/TandoorRecipes/recipes/blob/cbb96e1/cookbook/views/api.py).

An illustrative native payload is:

```json
{
  "name": "Simple dough",
  "description": "Basic dough",
  "steps": [
    {
      "instruction": "Mix and knead.",
      "ingredients": [
        {
          "food": { "name": "flour" },
          "unit": { "name": "g" },
          "amount": 250,
          "note": ""
        }
      ]
    }
  ]
}
```

**Validation caveat:** This is a serializer-shaped example, not an executed request. Before shipping, confirm nested object creation, defaults, token scopes, and field requirements against the instance’s generated API schema.

For reliable synchronization, resolve existing foods and units rather than repeatedly creating spelling variants. Add images through the supported image route instead of assuming a remote image URL can be written through the main recipe object.

### Mealie

The clearest schema.org path is:

```http
POST /api/recipes/create/html-or-json
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "data": "{\"@context\":\"https://schema.org\",\"@type\":\"Recipe\",\"name\":\"Simple dough\",\"recipeIngredient\":[\"250 g flour\",\"150 ml water\"],\"recipeInstructions\":[{\"@type\":\"HowToStep\",\"text\":\"Mix and knead.\"}]}"
}
```

The endpoint explicitly accepts raw HTML or a schema.org Recipe object **encoded as a JSON string in `data`**. Its documented response is the created recipe’s slug. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

URL import is a distinct endpoint:

```http
POST /api/recipes/create/url
```

```json
{
  "url": "https://recipes.example/recipe/simple-dough"
}
```

The source documents this route as fetching a URL and attempting to scrape it into the database. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

For maximum fidelity, use Mealie’s native model rather than repeatedly passing through the scraper. Current source specifically preserves richer structure when it recognizes a complete native Mealie dump, but that recognition requires fields such as a nonempty slug, group identity, and ingredient reference data; a hand-written partial object is not automatically treated as such a dump. [github](https://github.com/mealie-recipes/mealie/pull/8651)

### Nextcloud Cookbook

The checked specification defines:

```http
POST /apps/cookbook/api/v1/recipes
Content-Type: application/json
Authorization: Basic <credentials>
```

A conservative schema-oriented payload is:

```json
{
  "name": "Simple dough",
  "description": "Basic dough",
  "recipeYield": "4",
  "recipeIngredient": ["250 g flour", "150 ml water"],
  "recipeInstructions": ["Mix the ingredients.", "Knead until smooth."]
}
```

The documented creation operation requires a name, returns the created recipe ID, and documents a conflict when a recipe with that name already exists. The checked specification is available [here](https://github.com/nextcloud/cookbook/blob/e291863/docs/dev/api/0.1.3/openapi-cookbook.yaml).

Website import is:

```http
POST /apps/cookbook/api/v1/import
```

```json
{
  "url": "https://recipes.example/recipe/simple-dough"
}
```

**Deployment caveat:** A Nextcloud installation may require an `index.php` prefix or another base path. Also, the checked OpenAPI example contains some older-looking field names; use the actual recipe schema and installed application behavior as the final contract.

### Grocy

Grocy’s maintainer documents the two-stage creation pattern:

```http
POST /api/objects/recipes
```

```json
{
  "name": "Simple dough",
  "description": "Mix and knead."
}
```

After obtaining the recipe ID:

```http
POST /api/objects/recipes_pos
```

```json
{
  "recipe_id": 8,
  "product_id": 2,
  "amount": 250
}
```

These routes and the ingredient linkage are explicitly documented by the maintainer. [github](https://github.com/grocy/grocy/issues/544)

The omitted work is the important part: the adapter must determine what product `2` means and what unit the amount uses. Product and unit reconciliation should therefore be an explicit user-visible mapping step, not an LLM guess.

### Security considerations

The following are implementation recommendations for the local assistant:

- **Store secrets in the OS credential store**, not recipe files, prompts, exported archives, or ordinary application logs.
- **Use a dedicated application token/account**, with only the permissions needed for the selected recipe library.
- **Validate TLS certificates.** For private servers, install the appropriate trusted certificate rather than disabling verification globally.
- **Do not send API tokens to the language model.** The local integration should insert credentials only when making the HTTP request.
- **Never place tokens in query strings.** Redact authorization headers and sensitive response data from diagnostic output.
- **Pin the destination origin.** A recipe URL or model response must not be allowed to redirect authenticated requests to another server.
- **Separate fetching from authenticated API calls.** Remote recipe pages and image URLs are untrusted inputs.
- **Apply SSRF safeguards** when a service fetches arbitrary URLs: allow only intended schemes, constrain redirects, and consider private-address access explicitly.
- **Limit archive and image processing:** enforce compressed/uncompressed size limits, reject path traversal, and validate decoded media.
- **Handle duplicate and partial imports deliberately:** record remote IDs, retry safely, and avoid creating a second recipe after a timeout.
- **Offer token revocation and deletion** when an integration is disconnected.

This separation is particularly important because several documented import paths cause the receiving service to fetch a supplied website or image URL. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

---

## 6. Recommendation

### Smallest practical output set

**Recommended first release: two exchange formats, plus native API adapters.**

1. **Schema.org Recipe JSON-LD**, with two delivery mechanisms: downloadable JSON and a server-rendered HTML recipe page.
2. **Paprika `.paprikarecipes`**, for offline/bulk exchange with Paprika and verified migration importers.
3. **Native API adapters** for Tandoor, Mealie, and Nextcloud Cookbook; a separate product-aware adapter for Grocy.

This recommendation follows the documented direct schema input in Mealie and Crouton, the broad availability of web recipe import, and the verified Paprika migration paths in Tandoor, Mealie, and Recipya. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

**Do not describe this as “two files import into every app.”** For several consumer apps, the broad-coverage route is a webpage URL; their support for a custom assistant-generated site still needs acceptance testing.

### Coverage matrix

**Legend:** **✓** = established route; **~** = indirect, dialect-specific, or requires validation; **?** = not verified; **—** = no verified route in this assessment, not proof of impossibility.

| App                               |   Schema webpage URL |          Schema JSON file / paste |  Paprika archive | Cooklang `.cook` | Native route / caveat                                                                                                                                  |
| --------------------------------- | -------------------: | --------------------------------: | ---------------: | ---------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tandoor                           |                    ✓ |          ~ RecipeSage integration |                ✓ |                ✓ | Native ZIP and REST model. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                                               |
| Mealie                            |                    ✓ |                       ✓ paste/API |                ✓ |                — | Native export structure and migrations. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py) |
| Recipya Go                        |                    ✓ |       ~ JSON shape must be tested |                ✓ |                — | App migration importers; separate from Rust rewrite. [github](https://github.com/reaper47/recipya/blob/main/internal/scraper/scraper.go)               |
| kitshn                            |    ✓ through Tandoor |                 ~ through backend | ~ backend import | ~ backend import | Not an independent backend. [play.google](https://play.google.com/store/apps/details?id=de.kitshn.android&hl=en_GB)                                    |
| ManageMeals                       |                    ~ |                                 ? |                ? |                ? | URL import established; bulk format unverified. [selfhost-hub](https://selfhost-hub.com/en/managemeals/)                                               |
| Nextcloud Cookbook                |                    ✓ | ✓ API/storage, not generic upload |                — |                — | Schema-oriented API and recipe folders. [apps.nextcloud](https://apps.nextcloud.com/apps/cookbook/)                                                    |
| KitchenOwl                        |                    ✓ |                                 — |                ? |                — | Household-specific native payload. [repocloud](https://repocloud.io/details/KitchenOwl/)                                                               |
| Grocy                             |                    — |                                 — |                — |                — | Product-aware API adapter. [github](https://github.com/grocy/grocy/issues/544)                                                                         |
| Paprika 3                         |        ~ web clipper |                                 — |                ✓ |                — | Also documented YAML and legacy formats. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                        |
| Mela                              |        ~ web clipper |                                 ? |                ? |                — | Native `.melarecipe` / collection archive. [mela](https://mela.recipes/)                                                                               |
| Crouton, current documented build |                    ✓ |                ✓ JSON, ZIP, paste |                ? |                — | Shortcuts can create from schema data. [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)                |
| Recipe Keeper                     |       ~ web importer |                                 ? |                ? |                ? | Other-app import advertised; precise matrix unverified. [recipekeeperonline](https://recipekeeperonline.com/)                                          |
| AnyList                           |       ~ web importer |                                 — |                — |                — | Native AnyList attachment import. [help.anylist](https://help.anylist.com/articles/feature-overview-recipe-import-android/)                            |
| RecipeSage                        | ? in this assessment |                         ✓ JSON-LD |                ? |                ? | Bidirectional JSON migration documented by Tandoor. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                      |

Do not turn this matrix into a percentage of market coverage: comparable active-user numbers were not established, and several cells are intentionally conditional.

### Fidelity trade-offs

| Route               | Ingredient groups                                                                                                                   | Quantities and units                                                                                                               | Images                                                                                                                        | Nutrition                                                                                                  | Best use                                                      |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Schema.org JSON-LD  | Instructions have standard sections; ingredient-group interoperability remains weak. [schema](https://schema.org/Recipe)            | Text is the safest common denominator; structured schema ingredients are not broadly verified. [schema](https://schema.org/Recipe) | Usually URL references. [schema](https://schema.org/Recipe)                                                                   | Typed object, but receiver mapping varies. [schema](https://schema.org/Recipe)                             | Primary interchange and web delivery.                         |
| Paprika archive     | Text heading conventions. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                    | Primarily text ingredients interpreted by the receiver. [paprikaapp](https://www.paprikaapp.com/help/android/)                     | Can carry image data; receiving importers vary. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000) | Text-oriented in Paprika’s documented editor model. [paprikaapp](https://www.paprikaapp.com/help/android/) | Offline Paprika and migration bridges.                        |
| Cooklang            | Explicit preparation sections. [github](https://github.com/lexi2042/cooklang-spec)                                                  | Explicit ingredient quantities and units. [cooklang](https://cooklang.org/docs/getting-started/)                                   | Target-dependent; Tandoor import lacks images. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)  | No broadly verified cross-app nutrition contract.                                                          | Text-first authoring and archival.                            |
| Native APIs         | Best opportunity to preserve the target’s actual group/step model.                                                                  | Can use explicit fields and database identities.                                                                                   | Often a separate upload or attachment operation.                                                                              | Target-specific typed fields and serving basis.                                                            | High-fidelity self-hosted integration.                        |
| Native app archives | Usually strongest within the same app/version family. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000) | Preserves native structure where the importer supports it.                                                                         | Often packaged assets. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                          | Version- and app-dependent. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)  | Migration and backup—not the default single-recipe interface. |

### Internal model to keep

Do **not** make flat JSON-LD ingredient strings your sole internal representation. Tandoor and Mealie demonstrate why: native models can retain food/unit identities, headings, step links, and original text that a generic scraper representation may discard. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

Recommended internal fields:

```text
Recipe
  stable ID and revision
  title, description, language, provenance
  yield: numeric value + unit + original display text
  times: preparation, cooking, waiting, total
  ingredient groups[]
    heading
    ingredients[]
      original text
      quantity: exact value or range
      unit: canonical ID + display text + measurement system
      food: canonical ID + localized name
      preparation/note
      optional flag
  instruction sections[]
    heading
    steps[]
      text
      linked ingredient IDs
      timers
      image references
  images[]
    local asset + export URL + attribution
  nutrition
    values + units + serving basis + provenance
  tags, category, cuisine
```

These are design recommendations, not a proposed universal file standard.

### Implementation order

| Priority | Deliverable                              | Reason                                                                                                                                                                                       |
| -------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | JSON-LD renderer and matching HTML page  | One semantic model serves direct schema importers and web-clipping workflows. [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py) |
| 2        | Mealie and Nextcloud API adapters        | Closely aligned with structured-data import; comparatively small conversion layer.                                                                                                           |
| 3        | Tandoor native adapter                   | Preserves richer ingredient and step structure than text scraping.                                                                                                                           |
| 4        | Paprika archive renderer                 | Adds a practical offline migration bridge. [paprikaapp](https://www.paprikaapp.com/help/android/)                                                                                            |
| 5        | Crouton Shortcuts handoff                | Avoids unnecessary hosting on supported Apple installations. [apps.apple](https://apps.apple.com/in/app/crouton-recipe-manager/id1461650987?l=mr&platform=mac)                               |
| 6        | Mela native renderer, if demand warrants | Potentially useful Apple-specific route, but validate the file contract first. [github](https://github.com/vrih/recipe-store/blob/main/docs/PRD.md)                                          |
| 7        | Grocy adapter                            | Valuable but requires product/unit reconciliation, not just serialization. [github](https://github.com/grocy/grocy/issues/544)                                                               |
| 8        | Cooklang renderer                        | Good text-first option; limited additional verified coverage among the requested apps. [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)                         |

**Release gate:** Mark an app “supported” only after testing the exact route and version with fixtures for ingredient sections, German text, fractions, ranges, images, nutrition basis, and tags. Keep separate labels for **documented**, **implemented**, and **tested** compatibility.

---

## Sources — APA style

Apple. (n.d.). _Crouton: Recipe Manager_ [App Store listing and version history]. Retrieved November 1, 2026, from [https://apps.apple.com/qa/app/crouton-recipe-manager/id1461650987](https://apps.apple.com/qa/app/crouton-recipe-manager/id1461650987) [apps.apple](https://apps.apple.com/us/app/crouton-recipe-manager/id1461650987?l=ru&platform=tv)

AnyList. (n.d.). _Adding ingredient headings_. Retrieved November 1, 2026, from [https://help.anylist.com/articles/recipe-ingredient-headings/](https://help.anylist.com/articles/recipe-ingredient-headings/) [help.anylist](https://help.anylist.com/articles/recipe-ingredient-headings/)

AnyList. (n.d.). _Getting started with AnyList_. Retrieved November 1, 2026, from [https://help.anylist.com/articles/getting-started/](https://help.anylist.com/articles/getting-started/) [help.anylist](https://help.anylist.com/articles/getting-started/)

AnyList. (n.d.). _Importing recipes from the web on Android_. Retrieved November 1, 2026, from [https://help.anylist.com/articles/feature-overview-recipe-import-android/](https://help.anylist.com/articles/feature-overview-recipe-import-android/) [help.anylist](https://help.anylist.com/articles/feature-overview-recipe-import-android/)

AnyList. (n.d.). _Opening an AnyList recipe file_. Retrieved November 1, 2026, from [https://help.anylist.com/articles/open-recipe-file/](https://help.anylist.com/articles/open-recipe-file/) [help.anylist](https://help.anylist.com/articles/open-recipe-file/)

Cooklang. (n.d.). _Getting started_. Retrieved November 1, 2026, from [https://cooklang.org/docs/getting-started/](https://cooklang.org/docs/getting-started/) [cooklang](https://cooklang.org/docs/getting-started/)

Cooklang. (n.d.). _Language overview_. Retrieved November 1, 2026, from [https://cooklang.org/docs/](https://cooklang.org/docs/) [cooklang](https://cooklang.org/docs/)

Cooklang. (n.d.). _Tips, tricks, and best practices_. Retrieved November 1, 2026, from [https://cooklang.org/docs/best-practices/](https://cooklang.org/docs/best-practices/) [cooklang](https://cooklang.org/docs/best-practices/)

Cooklang. (n.d.). _Cooklang language server_ [Source code]. GitHub. [https://github.com/cooklang/cooklang-language-server](https://github.com/cooklang/cooklang-language-server) [github](https://github.com/cooklang/cooklang-language-server)

FormatData. (n.d.). _RecipeML document type definition_. Retrieved November 1, 2026, from http://formatdata.com/recipeml/dtd.html [formatdata](http://formatdata.com/recipeml/dtd.html)

FormatData. (n.d.). _RecipeML examples_. Retrieved November 1, 2026, from http://formatdata.com/recipeml/examples.html [formatdata](http://formatdata.com/recipeml/examples.html)

FormatData. (n.d.). _RecipeML frequently asked questions_. Retrieved November 1, 2026, from http://formatdata.com/recipeml/faq.html [formatdata](http://formatdata.com/recipeml/faq.html)

Google. (2026, September 8). _Recipe (Recipe, HowTo, ItemList) structured data_. Google Search Central. [https://developers.google.com/search/docs/appearance/structured-data/recipe](https://developers.google.com/search/docs/appearance/structured-data/recipe) [schema](https://schema.org/Recipe)

Grocy contributors. (n.d.). _Grocy routes_ [Source code]. GitHub. Retrieved November 1, 2026, from [https://github.com/grocy/grocy/blob/master/routes.php](https://github.com/grocy/grocy/blob/master/routes.php) [github](https://github.com/grocy/grocy/blob/master/routes.php)

Grocy project. (2020). _Add recipe via API_ [Issue #544]. GitHub. [https://github.com/grocy/grocy/issues/544](https://github.com/grocy/grocy/issues/544) [github](https://github.com/grocy/grocy/issues/544)

Hindsight Labs. (n.d.). _Paprika user guide for Android_ [Paprika 3 documentation]. Retrieved November 1, 2026, from [https://www.paprikaapp.com/help/android/](https://www.paprikaapp.com/help/android/) [paprikaapp](https://www.paprikaapp.com/help/android/)

Hindsight Labs. (n.d.). _Paprika 4 (beta) user guide for Android_. Retrieved November 1, 2026, from [https://www.paprikaapp.com/help/v4/android/](https://www.paprikaapp.com/help/v4/android/) [paprikaapp](https://www.paprikaapp.com/help/v4/android/)

KitchenOwl contributors. (n.d.). _KitchenOwl documentation_. Retrieved November 1, 2026, from [https://docs.kitchenowl.org/](https://docs.kitchenowl.org/) [docs.kitchenowl](https://docs.kitchenowl.org/)

kitshn contributors. (2026, October 25). _Release: 2.1.5_ [Commit]. GitHub. [https://github.com/kitshn-app/kitshn/commit/07c004f8790bf3a80abc59e8612af5799060dc28](https://github.com/kitshn-app/kitshn/commit/07c004f8790bf3a80abc59e8612af5799060dc28) [github](https://github.com/kitshn-app/kitshn/commit/07c004f8790bf3a80abc59e8612af5799060dc28)

ManageMeals. (n.d.). _ManageMeals API_ [Source repository]. GitHub. Retrieved November 1, 2026, from [https://github.com/managemeals/manage-meals-api](https://github.com/managemeals/manage-meals-api) [github](https://github.com/managemeals/manage-meals-api/wiki/TODO)

ManageMeals. (n.d.). _ManageMeals web_ [Source repository]. GitHub. Retrieved November 1, 2026, from [https://github.com/managemeals/manage-meals-web](https://github.com/managemeals/manage-meals-web) [github](https://github.com/managemeals/manage-meals-web)

MasterCook. (n.d.). _Adding cookbook files to MasterCook_. Retrieved November 1, 2026, from [https://support.mastercook.com/hc/en-us/articles/216889146-Adding-Cookbook-Files-to-MasterCook](https://support.mastercook.com/hc/en-us/articles/216889146-Adding-Cookbook-Files-to-MasterCook) [support.mastercook](https://support.mastercook.com/hc/en-us/articles/216889146-Adding-Cookbook-Files-to-MasterCook)

Mealie contributors. (n.d.). _Features_ [Documentation source]. GitHub. Retrieved November 1, 2026, from [https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md) [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/docs/docs/documentation/getting-started/features.md)

Mealie contributors. (n.d.). _Recipe CRUD routes_ [Source code]. GitHub. Retrieved November 1, 2026, from [https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py) [github](https://github.com/mealie-recipes/mealie/blob/mealie-next/mealie/routes/recipe/recipe_crud_routes.py)

Nextcloud. (n.d.). _Cookbook_ [Application listing]. Retrieved November 1, 2026, from [https://apps.nextcloud.com/apps/cookbook/](https://apps.nextcloud.com/apps/cookbook/) [apps.nextcloud](https://apps.nextcloud.com/apps/cookbook/)

Open Recipe Format contributors. (n.d.). _Getting started_. Retrieved November 1, 2026, from [https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html](https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html) [open-recipe-format.readthedocs](https://open-recipe-format.readthedocs.io/en/latest/topics/tutorials/walkthrough.html)

Recipe Keeper. (n.d.). _Recipe Keeper_. Retrieved November 1, 2026, from [https://recipekeeperonline.com/](https://recipekeeperonline.com/) [recipekeeperonline](https://recipekeeperonline.com/)

reaper47. (2024, August 6). _The future of Recipya_ [Discussion #422]. GitHub. [https://github.com/reaper47/recipya/discussions/422](https://github.com/reaper47/recipya/discussions/422) [github](https://github.com/reaper47/recipya/discussions/422)

reaper47. (2025). _Ingredient groups within recipe_ [Issue #517]. GitHub. [https://github.com/reaper47/recipya/issues/517](https://github.com/reaper47/recipya/issues/517) [github](https://github.com/reaper47/recipya/issues/517)

Rizzi, S. (n.d.). _Mela_. Retrieved November 1, 2026, from [https://mela.recipes/](https://mela.recipes/) [mela](https://mela.recipes/)

Schema.org. (2026, September 16). _Recipe_ [Version 30.1]. [https://schema.org/Recipe](https://schema.org/Recipe) [schema](https://schema.org/Recipe)

Tandoor Recipes contributors. (n.d.). _Import/export_. Retrieved November 1, 2026, from [https://docs.tandoor.dev/features/import_export/](https://docs.tandoor.dev/features/import_export/) [context7](https://context7.com/tandoorrecipes/recipes/llms.txt?tokens=10000)

Vrih. (2026). _Recipe-store product requirements: Mela file format and import_ [Third-party implementation analysis]. GitHub. [https://github.com/vrih/recipe-store/blob/main/docs/PRD.md](https://github.com/vrih/recipe-store/blob/main/docs/PRD.md) [github](https://github.com/vrih/recipe-store/blob/main/docs/PRD.md)
