<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/clever-cc-plugins/.github/main/assets/logo-dark.svg" />
    <img src="https://raw.githubusercontent.com/clever-cc-plugins/.github/main/assets/logo.svg" width="220" alt="clever [cc] plugins" />
  </picture>
</p>

# <img src="assets/icon.svg" width="40" height="40" align="top" alt="" />&nbsp;cc-chef

A [Claude Code](https://claude.ai/code) plugin to create, adapt, rework and export grounded everyday recipes.

---

## Plugin: `cc-chef`

`cc-chef` is for comfort food, traditional fare and rustic home cooking: recipes written to be cooked, in your language and units, with one or two deliberate touches that make a dish worth remembering. It applies culinary rules consistently instead of carrying a large food or diet database, and it keeps no recipe collection of its own. Recipes end up as files or in your recipe app.

Every skill works without any setup and uses sensible defaults. If you run onboarding, your preferences, household and allergies shape every recipe. Allergens and life-stage safety rules are hard constraints that are never relaxed for flavour.

| Skill                         | What it does                                                                                                     |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `/cc-chef:chef-onboarding`    | Sets up your cooking preferences: language, units, region, household, equipment, tastes and recipe save folder   |
| `/cc-chef:create-recipe`      | Turns a mood, ingredients, a fridge photo or a dish name into recipe ideas and then one full, cookable recipe    |
| `/cc-chef:rework-recipe`      | Restructures an existing recipe (text, URL, photo or saved file) to your preferences and, optionally, guidelines |
| `/cc-chef:dietary-guidelines` | Opt-in: writes a personal dietary guideline per household member that the other skills apply                     |
| `/cc-chef:research-prompt`    | Builds a ready-to-paste deep-research prompt about a diet, intolerance or food practice                          |
| `/cc-chef:export-recipe`      | Saves recipes as Markdown and converts them to JSON-LD or a Paprika archive                                      |

---

## Installation

Open Claude Code in any project and run:

```
/plugin marketplace add clever-cc-plugins/marketplace
/plugin install cc-chef@clever-cc-plugins
```

This makes all skills immediately available.

### Keeping Skills Current

Auto-update is disabled by default for third-party marketplaces. To enable it:

1. Run `/plugin` in Claude Code
2. Go to the **Marketplaces** tab
3. Toggle auto-update for `clever-cc-plugins/marketplace`

Once enabled, skills update automatically on startup when new versions are available.

---

## Getting Started

Run onboarding once to store your preferences. It asks one question at a time and offers a default for each:

```
/cc-chef:chef-onboarding
```

Then tell `create-recipe` what is in your fridge, what you fancy, or which dish you want:

```
/cc-chef:create-recipe
```

You get three clearly different ideas, each with its time, the items it uses and what you would need to buy. Pick one and you get the full recipe, which is then saved according to your preferences. A named dish skips the ideas.

To turn a recipe you already have into your preferred structure and units, pass it to `rework-recipe`. Quantity and ingredient changes are flagged, and the source stays credited:

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

Python 3 is needed for validation and conversion, not for saving.

Tandoor support: coming in phase 2.

---

## Health Disclaimer

cc-chef offers general information for healthy everyday cooking. It is not medical advice and does not replace a doctor, dietitian or pharmacist, especially for medical conditions, medicines, pregnancy, infants and prescribed diets. You are responsible for checking ingredient labels for allergens, and nutrient values are estimates. For a suspected allergic or medical emergency, call your local emergency number.

---

## Contributing

See [tests/README.md](tests/README.md) for the script tests and dry-run scenarios.

---

## License

[MIT](LICENSE) — Copyright (c) 2026 Michael van Laar

---

<p align="center">
  Part of the <a href="https://github.com/clever-cc-plugins">clever-cc-plugins</a> family · <a href="https://github.com/clever-cc-plugins/marketplace">marketplace</a> · <a href="https://github.com/clever-cc-plugins/cc-config">cc-config</a> · <a href="https://github.com/clever-cc-plugins/cc-concept">cc-concept</a> · <a href="https://github.com/clever-cc-plugins/cc-content">cc-content</a> · <a href="https://github.com/clever-cc-plugins/cc-career">cc-career</a> · <a href="https://github.com/clever-cc-plugins/cc-coach">cc-coach</a> · <a href="https://github.com/clever-cc-plugins/cc-handoff">cc-handoff</a> · <a href="https://github.com/clever-cc-plugins/cc-chime">cc-chime</a>
</p>
