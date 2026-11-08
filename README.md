<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/clever-cc-plugins/.github/main/assets/logo-dark.svg" />
    <img src="https://raw.githubusercontent.com/clever-cc-plugins/.github/main/assets/logo.svg" width="220" alt="clever [cc] plugins" />
  </picture>
</p>

# <img src="assets/icon.svg" width="40" height="40" align="top" alt="" />&nbsp;cc-chef

A [Claude Code](https://claude.ai/code) plugin to create, adapt, rework, and export grounded everyday recipes. A recipe is a program that runs on a stove, so it deserves the same care as any other: clear inputs, sensible steps, no undefined behavior.

---

## At a Glance

`cc-chef` is for comfort food, traditional fare, and rustic home cooking. It writes recipes that are meant to be cooked, in your language and units, with one or two deliberate touches that make a dish worth remembering. It applies culinary rules consistently instead of carrying a large food or diet database, and it keeps no recipe collection of its own. Recipes end up as files or in your recipe app.

Every skill works without setup and uses sensible defaults. If you run onboarding, your preferences, household, and allergies shape every recipe. Allergens and life-stage safety rules are hard constraints that are never relaxed for flavor.

| Skill                           | What it does                                                                                                                      |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `/cc-chef:chef-onboarding`      | Sets up your cooking preferences: language, units, region, household, equipment, tastes, and recipe save folder                   |
| `/cc-chef:create-recipe`        | Turns a mood, ingredients, a fridge photo, or a dish name into recipe ideas and then into one full, cookable recipe               |
| `/cc-chef:rework-recipe`        | Restructures an existing recipe (text, URL, photo, saved file, or Tandoor recipe) to your preferences and, optionally, guidelines |
| `/cc-chef:dietary-guidelines`   | Opt-in: writes a personal dietary guideline per household member that the other skills apply                                      |
| `/cc-chef:research-prompt`      | Builds a ready-to-paste deep-research prompt about a diet, intolerance, or food practice                                          |
| `/cc-chef:export-recipe`        | Saves recipes as Markdown and converts them to JSON-LD or a Paprika archive, or uploads them to Tandoor                           |
| `/cc-chef:tandoor-food-cleanup` | Merges duplicate foods and units in your Tandoor instance, group by group, after you approve each one                             |

---

## Installation

Open Claude Code in any project and run:

```
/plugin marketplace add clever-cc-plugins/marketplace
/plugin install cc-chef@clever-cc-plugins
```

All skills are available immediately.

### Keeping Skills Current

Auto-update is off by default for third-party marketplaces. To switch it on:

1. Run `/plugin` in Claude Code
2. Open the **Marketplaces** tab
3. Toggle auto-update for `clever-cc-plugins/marketplace`

Once it's on, Claude Code updates the skills on startup whenever a new version is available.

### Uninstalling

```
/plugin uninstall cc-chef@clever-cc-plugins
```

To remove the marketplace as well (this uninstalls every plugin you installed from it):

```
/plugin marketplace remove clever-cc-plugins
```

---

## Getting Started

Run onboarding once to store your preferences. It asks one question at a time and offers a default for each:

```
/cc-chef:chef-onboarding
```

Then tell `create-recipe` what's in your fridge, what you fancy, or which dish you want:

```
/cc-chef:create-recipe
```

You get three clearly different ideas, each with its time, the items it uses, and what you'd need to buy. Pick one and you get the full recipe, which is saved according to your preferences. A named dish skips the ideas.

To turn a recipe you already have into your preferred structure and units, pass it to `rework-recipe`. It flags changes to quantities and ingredients and keeps crediting the source:

```
/cc-chef:rework-recipe
```

If you have special dietary needs, research them first and bring the result back as a guideline:

```
/cc-chef:research-prompt
/cc-chef:dietary-guidelines
```

---

## Saving and Exporting

Recipes are saved as Markdown files in a save folder of your choice, in one fixed layout that keeps each step's ingredients attached to it. `export-recipe` can convert them for recipe apps:

| Target  | Output                     | Imports into                                         |
| ------- | -------------------------- | ---------------------------------------------------- |
| Files   | Markdown with frontmatter  | Any Markdown viewer                                  |
| JSON-LD | schema.org Recipe, `.json` | Apps that read schema.org recipes, such as Mealie    |
| Paprika | `.paprikarecipes` archive  | Paprika and other apps that read this archive format |

Validation and conversion need Python 3. Saving doesn't.

### Tandoor

If you run [Tandoor](https://tandoor.dev), cc-chef can work with it directly, and only after you've configured an instance. Everyone else keeps using files.

- **Upload:** `export-recipe` sends a recipe with its steps and the ingredients attached to the steps that use them. Every ingredient is matched against your food and unit database, including your existing aliases. Anything without a confident match is put to you, and a close match is only ever a suggestion. You see a preview and approve it before anything is written. The Markdown file is always saved first.
- **Matching names while writing:** with a working connection, `create-recipe` and `rework-recipe` look up the foods and units of a recipe in your database before they show it, and they use your existing names. That way the upload creates fewer near-duplicates. This step is read-only and is skipped without a connection.
- **Rework in place:** `rework-recipe` can take a recipe from your instance, restructure it, and update it in place after a preview. Processed recipes get a `cc-chef` keyword, and existing keywords are kept.
- **Food cleanup:** `tandoor-food-cleanup` finds duplicate and polluted foods and units and merges them group by group. Details in a food name move into the notes of the ingredients first. Merges can't be undone, so make a backup of the instance before the first run.

Setup, once:

1. In Tandoor, create an API token with the `read` and `write` scopes.
2. In the project where you use the skills, put `TANDOOR_URL` (the address of your instance) and `TANDOOR_API_TOKEN` into a `.env` file, and make sure `.env` is in that project's `.gitignore`. Don't paste the token into the chat.
3. Run `/cc-chef:chef-onboarding` and pick `tandoor` as the recipe target, or ask `export-recipe` for Tandoor directly. It checks the connection first.

The script uses only Python 3's standard library, so there's nothing to install.

---

## Health Disclaimer

cc-chef offers general information for healthy everyday cooking. It is not medical advice and does not replace a doctor, dietitian, or pharmacist, especially for medical conditions, medicines, pregnancy, infants, and prescribed diets. You are responsible for checking ingredient labels for allergens, and nutrient values are estimates. For a suspected allergic or medical emergency, call your local emergency number.

---

## Contributing

Issues and pull requests are welcome. If you've spotted a gap or a rough edge, please open an issue first so we can agree on the approach. [tests/README.md](tests/README.md) describes the script tests and dry-run scenarios.

---

## License

[MIT](LICENSE), Copyright (c) 2026 Michael van Laar

---

<p align="center">
  Part of the <a href="https://github.com/clever-cc-plugins">clever-cc-plugins</a> family · <a href="https://github.com/clever-cc-plugins/marketplace">marketplace</a> · <a href="https://github.com/clever-cc-plugins/cc-config">cc-config</a> · <a href="https://github.com/clever-cc-plugins/cc-concept">cc-concept</a> · <a href="https://github.com/clever-cc-plugins/cc-content">cc-content</a> · <a href="https://github.com/clever-cc-plugins/cc-career">cc-career</a> · <a href="https://github.com/clever-cc-plugins/cc-coach">cc-coach</a> · <a href="https://github.com/clever-cc-plugins/cc-handoff">cc-handoff</a> · <a href="https://github.com/clever-cc-plugins/cc-chime">cc-chime</a>
</p>
