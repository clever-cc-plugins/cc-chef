Research Report: Recipe Import Interoperability for an AI Cooking Assistant

Scope: Evaluate the minimum set of recipe output formats and delivery mechanisms (file, URL, API) needed to support the largest number of popular recipe-management applications as of 2026-11-01. Findings are based primarily on official documentation, specifications, and source repositories.

1. Schema.org Recipe (JSON-LD)
   Why Schema.org Recipe Matters

The single most important interoperability format in the recipe ecosystem today is Schema.org Recipe encoded as JSON-LD. Most recipe importers do not consume app-specific formats first; instead they scrape web pages and read embedded Schema.org Recipe markup. Many modern apps effectively use Schema.org as their canonical import format. turn1search10

Core Recipe Properties

Schema.org defines Recipe as a subtype of HowTo. Importnt properties include: turn1search12

Property Purposename Recipe title
image ecipe image URL(s)
description Summary
recipeIngredient Ingredient list
recipeInstructions Steps/sections
recipeYield Servings/yield
prepTime Preparation time
cookTime Cooking time
totalTime Total time
nutrition NutritionInformation
recipeCategory Category
recipeCuisine Cuisine
keywords Tags/search terms
author Creator
datePublished Publication date
suitableForDiet Dietary classification

turn1search12

Google Rich Result Requirements

Google's Recipe rich-result documentation reqires structured recipe markup and recommends fields including: name, image, recipeIngredient, recipeInstructions, author, prepTime, cookTime, totalTime, recipeYield, nutrition information, ratings, video, category, cuisine, and keywords. turn1search10

The de-facto interoperability subset is:

{
"@context": "https://schema.org"
"@type": "Recipe",
"name": "Chocolate Cake",
"image": ["https://example.com/cake.jpg"],
"recipeYield": "8 servings",
"prepTime": "PT20M",
"cookTime": "PT35M",
"totalTime": "PT55M",
"recipeIngredient": [
"250 g flour",
"200 g sugar"
],
"recipeInstructions": [
{
"@type": "HowToStep",
"text": "Mix ingredients."
}
]
}

turn1search12

Ingredient Representation

Typically represented as:

"recipeIngredien": [
"2 cups flour",
"1 tsp salt"
]

Structured ingredient modeling exists but is inconsistently supported across importers. Most apps expect human-readable ingredient strings. turn1search12

Instruction Representation
Flat Steps
"recipeInstructions": [

    "@type": "HowToStep",
    "text": "Mix ingredients."

}
]

Sectioned Recipes
"recipeInstructions": [
{
"@type": "HowToSection",
"name": "Cake"
},
{
"@type": "HowToStep",
"text": "Mix cake ingredients."
}
]

Schema.org explicitly supports both HowToStep and HowToSection. turn1search10

Time Encoding

ISO 8601 durations:

Duration Example15 minutes PT15M
1 hour PT1H
1h 30m PT1H30M

Used for:

prepTime
cookTime
totalTime

turn1search12

Nutrition

Represented using NutritionInformation:

"nutrition": {
"@type": "NutritionInformation",
"calories": "250 calories",
"fatContent": "10 g"
}

turn1search12

Categories & Tags
"recipeCategory": "Dessert",
"recipeCuisine": "Frenh",
"keywords": "cake,chocolate,easy"

turn1search12

Which Apps Actually Consume Schema.org?
Strong Native Schema.org Import
App Schema.org UsageTandoor Yes
Mealie Yes
Nextcloud Cookbook Yes
ManageMeals Yes
AnyList Yes
Paprika Yes (via scraper)
Mela Yes
Crouton Yes
RecipeSage JSON-LD import explicitly supported
Recipya URL scraping

Sources indicate URL scrapers are generally reading embedded Recipe JSON-LD or recipe-scrapers outputs. turn1search78

Robustness
Quality BehaviorExcellent Tandoor, ealie, Nextcloud, RecipeSage
Good Paprika, Mela, Crouton
Variable AnyList, ManageMeals

Most importers work best when valid Schema.org Recipe JSON-LD exists. turn1search16

2. App-by-App Import Support
   Tandoor Recipes (v2.7.2 checked)

Maintained, ctive OSS project. turn1search16

Imports
URL scraping (JSON-LD/microdata)
Mealie export
Nextcloud Cookbook eport
Paprika exports
Cooklang
RecipeSage JSON-LD
MealMaster
ZIP migrations

turn1search19

Sections

Supports ingredient groups and step grouping.

Images

Imported and tored.

Mealie (v3.29.0 checked)

Actively maintained. turn1search25

Imports
URL
Raw HTML
Raw JSON
Other-app archive imports
Bulk text
API turn1search27
Supported Migrations
Tandoor
Paprika
Nextcloud
Recipe Keeper
Chowdown -Plan to Eat

turn1search78

Imports
Web URLs
Mealie exports
Tandoor exports
Nextcloud exports
Papria imports

turn1search78

Features
Auto nutrition
Metric/imperial conversion
kitshn

Not a recpe backend.

It is an unofficial Tandoor client. Import capability routes through Tandoor APIs. turn1search81

Likely dependency

Recipe scraping from structured recipe metadata.

Nextcoud Cookbook

Actively maintained. turn1search62

Storage

Recipes stored as files inside Nextcloud.

KitchenOwl

Maintained turn1search66

Imports

Historically limited. Maintainer stated imports mainly used internal JSONformats. turn1search74

Native Recipe Import

Weak.

Most users rely on:

Recipe Buddy
Grocy Recipe Imort

which scrape Schema.org recipes and create recipes through the Grocy API. turn1search33

Imports
Built-in browser
Bookmarklet
URL scraping

Uses NLP and structured ecipe extraction. turn1search31

Images

Imported from source pages when available.

Mela

Maintained Appleecosystem app. turn1search37

Imports
URL import
Share extension
Paprika export
Native .melarecipe
ative .melarecipes

turn1search43

Recipe Keeper

Actively maintained commercial app.

Imports

Verified migrtion targets exist in Mealie, Tandoor, RecipeSage ecosystems. turn1search54

3. Open and Legacy Interchange Formats
   Cooklang

Plain-text cooking DSL:

``cooklang Add 500g flour{flour}. Chop @onion{1}.

Tandoor imports Cooklang. turn1search17

Adoption: growing among OSS/self-hosted tools.

---

## Paprika Format

Extension:

``text
.paprikarecipe
.paprikarecipes

Widely supported for migration:

Mealie
Tandoor
Mela
RecipeSage

turn1search45

MasterCook

Formats:

MXP
MX2
MZ2

Still supported by conversion tools ad Recipya importers. turn1search79

Meal-Master

Format:

MMMMM----- Recipe via Meal-Master

Legacy bu still frequently imported. Supported by Tandoor and Recipya. turn1search79

RecipeML

Exists but has limited modern adoption.

Could not verify significan import support among the surveyed applications.

Open Recipe Format (ORF)

Emerging exchange concept rather than established standard.

Could not verify broad production adoption.

App-Specific Archives
Tandoor

ZIP → JSON + images. turn1search34

4. Ingredient Parsing

Most systems ultimately parse:

1½ cups flour, sfted

into:

Component Valuequantity 1.5
unit cups
food flour
note sifted
What Works Best

Use:

1.5 tbsp olive oil

or

1 1/2 tbsp olive oil

instead of:

olive oil, about a spoon and a half

Parsing Strength
Strong
Mealie
Tandoor
Paprika

turn1search31

Moderate
Mela
Crouton
Nextcloud
Weak
Grocy native
KitchenOwl
Internationalization

Observed limitations:

Most parsers are English-focused.
Metric units usually outperform imperial.
Fractions generally work.
Ranges ("2-3 cloves") often become notes.

turn1search24

5. API-Based Import for Self-Hosted Apps
   Tandoor
   Authentication

Beare token. turn1search19

Create Recipe
POST /api/recipe/

Supports:

name
servings
source_ur
steps
ingredients

turn1search19

Tandoor URL Import
POST /api/recipe-from-source/

{
"url":"ttps://example.com/recipe"
}

turn1search25

Suitable for AI-generated recipe creation workflows.

Nextcloud Cookbook

API xists and third-party clients create/import recipes programmatically. turn1search66

Can be used directly by automation tools.

Security Recommendations

For localAI assistants:

Store tokens encrypted at rest.
Use least-privilege tokens.
Prefer localhost/self-hosted communication.
Allow per-app API credential separation.
Support token rotation. 6. Recommendation
Best Minimal Output Set

For maximum coverage with minimal implementation effort:

Format A — Schema.org Recipe JSON-LD

Use as primary interchange payload.

Covers:

Tandoor
Mealie
Nextcloud
ManageMeals
Paprika
Mela
Crouton
AnyList
RecipeSage
Recipya

Directly or indirectly. turn1search45

Format B — Hosted HTML Page with Embedded JSON-LD

Generating:

<scrit type="application/ld+json">
...
</script>

allows almost every URL-import workflow to work.

This is arguably the single highest-value format.

Format C — API Push

Direct creation into:

Tandoor
Mealie
KitchenOwl
Nextcloud Cookbook

for self-hosted users.

turn1search66

Optional D — Paprika Export

Valuable only if targeting migration-heavy powerusers.

Coverage Matrix
App Schema.org JSON-LD HTML+JSON-LD URL APITandoor ✅ ✅ ✅
Mealie ✅ ✅ ✅
Nextcloud Cookbook ✅ ✅ Partial
Paprika ✅ ✅ ❌
Mela ✅ ✅ ❌
Crouton ✅ ✅ ❌
AnyList ✅ ✅ ❌
ManageMeals ✅ ✅ ❌
Recipya ✅ ✅ Limited
Recipe Keeper Indirect ✅ ❌
KitchenOwl ❌ Limited ✅
Grocy Via tools Via tools ✅
Final Conclusion

If your AI assistant can produce:

Schema.org Recipe JSON-LD
An HTML file containing embedded Recipe JSON-LD
Direct API submissions to self-hosted apps

you will cover the vast majority of modern recipe-management software with one canonical internal recipe model. Nearly every major importer ultimately consumes Recipe Schema or data derived from it, making Schema.org Recipe the closest thing the recipe ecosystem currently has to a universal exchange format. turn1search24

References (APA)

Google Developers. (2026). Recipe structured data. https://develpers.google.com/search/docs/appearance/structured-data/recipe

Schema.org. (2026). Recipe type. https://schema.org/Recipe

Schema.org. (2026). recipeInstructions property. https://schema.org/recipeInstructions

Tandoor Recipes. (2026). Documentation and import/export. https://docs.tandoor.dev/

Mealie. (2026). Official documentation. https://mealie.io/

Nextcloud Cookbook. (2026). Cookbook documentation. https://nextcloud.github.io/cookbook/

Mela. (2026). File format documentation. https://mela.recipes/fileformat/

AnyList. (2026). Recipe import documentation. https://help.anylist.com/articles/feature-overview-recipe-import/

KitchenOwl. (2026). API reference. https://docs.kitchenowl.org/dev/reference/API/

ManageMeals. (2026). Official website. https://managemeals.com/

Recipya. (2026). GitHub repository. https://github.com/reaper47/recipya

RecipeSage. (2026). Import documentation. https://docs.recipesage.com/docs/tutorials/settings/import/
