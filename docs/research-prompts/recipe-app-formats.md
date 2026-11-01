# Research Prompt: recipe app formats

**For:** the export of recipes in a format that recipe management apps can import.
**Why research helps:** users manage recipes in many different apps, self-hosted and commercial. The plugin should save recipes in a format their app accepts, ideally choosing from a small set of formats that covers most apps. This is technical research: official documentation and source code matter more than scientific literature.

Any tool with good web search works. Save the response as `docs/research/research-results-recipe-app-formats-by-<tool>.md`.

---

```text
─────────────────────────────────────────────
Research prompt: recipe import/export formats
─────────────────────────────────────────────
You are a technical research analyst. I am building an AI cooking assistant that saves recipes as files (or sends them via API) so they can be imported into the user's recipe management app. I need to know which formats and import paths the popular apps support, so the assistant can cover as many apps as possible with as few formats as possible.

Provide a comprehensive, well-structured report using headers to separate these areas:

1. SCHEMA.ORG RECIPE (JSON-LD)
   The schema.org Recipe type: required and recommended properties (including what Google's recipe rich-result guidelines require), and how ingredients, instructions (HowToStep, HowToSection), yield, times (ISO 8601 durations), nutrition, images, and keywords/categories are represented. Which apps import schema.org data — via URL, pasted HTML/JSON, or file — and how robust their parsing is.

2. APP-BY-APP IMPORT SUPPORT
   For each of the following apps, verify that it exists and is maintained, then document supported import formats and paths (file upload, pasted text, URL scraping, API), required fields, and how they handle ingredient sections, units and quantities, multilingual content, images, nutrition data, and tags: Tandoor Recipes, Mealie, Recipya, kitshn, ManageMeals, Nextcloud Cookbook, KitchenOwl, Grocy, Paprika, Mela, Crouton, Recipe Keeper, AnyList, and any other app with significant user numbers you find. Link the official documentation or the relevant source code, and note the version and date you checked.

3. OPEN AND LEGACY INTERCHANGE FORMATS
   Cooklang (specification and tooling), Paprika's export format, MasterCook (MXP/MX2), Meal-Master, RecipeML, Open Recipe Format, and app-specific export archives (e.g. Tandoor or Mealie exports). For each: structure, current adoption, and which apps import it.

4. INGREDIENT PARSING
   How apps parse free-text ingredient lines into quantity, unit, food, and note — and how well this works for non-English languages, fractions, ranges, and metric vs. imperial units. Which input conventions maximize correct parsing.

5. API-BASED IMPORT FOR SELF-HOSTED APPS
   REST APIs for creating recipes in self-hosted apps (e.g. Tandoor, Mealie, Nextcloud Cookbook): endpoints, authentication, required payload, and security considerations for a local tool that stores an API token.

6. RECOMMENDATION
   The smallest set of output formats that covers the largest share of the apps above, with a coverage matrix (app × format), and the trade-offs (fidelity of sections, units, images, nutrition).

Requirements:
- Use official documentation, specifications (schema.org, Cooklang), and source repositories as primary sources, with in-text citations and links. Flag anything you could not verify.
- Provide a formatted source list in APA style at the end.
- Respond in Markdown.
─────────────────────────────────────────────
```
