# cc-chef

A [Claude Code](https://claude.ai/code) plugin to create, adapt, rework and export grounded everyday recipes: comfort food, traditional fare and rustic home cooking, written to be cooked, in your language and units.

## Installation

```
/plugin marketplace add clever-cc-plugins/marketplace
/plugin install cc-chef@clever-cc-plugins
```

## Skills

| Skill                         | What it does                                                                                                     |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `/cc-chef:chef-onboarding`    | Sets up your cooking preferences: language, units, region, household, equipment, tastes and recipe save folder   |
| `/cc-chef:create-recipe`      | Turns a mood, ingredients, a fridge photo or a dish name into recipe ideas and then one full, cookable recipe    |
| `/cc-chef:rework-recipe`      | Restructures an existing recipe (text, URL, photo or saved file) to your preferences and, optionally, guidelines |
| `/cc-chef:dietary-guidelines` | Opt-in: writes a personal dietary guideline per household member that the other skills apply                     |
| `/cc-chef:research-prompt`    | Builds a ready-to-paste deep-research prompt about a diet, intolerance or food practice                          |
| `/cc-chef:export-recipe`      | Saves recipes as Markdown and converts them to JSON-LD or a Paprika archive                                      |

## Quick start

```
/cc-chef:chef-onboarding
/cc-chef:create-recipe
```

Onboarding runs once. After that, tell `create-recipe` what is in your fridge or what you fancy.

## What gets saved and exported

Recipes are saved as Markdown files in a save folder of your choice. `export-recipe` can convert them to JSON-LD (schema.org Recipe) or a Paprika archive. Python 3 is needed for validation and conversion, not for saving: without it, recipes are still written as Markdown.

Tandoor support: coming in phase 2.

## Health disclaimer

cc-chef offers general information for healthy everyday cooking. It is not medical advice and does not replace a doctor, dietitian or pharmacist, especially for medical conditions, medicines, pregnancy, infants and prescribed diets. You are responsible for checking ingredient labels for allergens, and nutrient values are estimates. For a suspected allergic or medical emergency, call your local emergency number.

## Contributing

See [tests/README.md](tests/README.md) for the script tests and dry-run scenarios.
