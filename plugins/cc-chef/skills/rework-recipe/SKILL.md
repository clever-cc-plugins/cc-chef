---
name: rework-recipe
description: >
  Use this skill to restructure an existing recipe (pasted text, a URL, a photo of a page or a saved recipe file) to the user's preferences: house style, language, units, step-by-step ingredients, optionally adapted to a dietary guideline. Invoke when the user says "rework this recipe", "convert this recipe to grams", "clean up this recipe from the web", "translate and restructure this recipe", "adapt this recipe to my guidelines", or "Bau dieses Rezept um". Flags every real recipe change and keeps the original values in the notes. Do NOT use it to create a new recipe from ingredients or an idea (use create-recipe) or to only convert or save an already finished recipe file (use export-recipe).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
argument-hint: "[optional: recipe text, a URL, a photo path or a saved recipe file path]"
---

@../\_shared/recipe-writing.md **Read when:** reworking any recipe: the risk table and rework workflow (sections 8.1 and 8.2), what may be copied and the attribution tiers (sections 8.3 and 8.4), unit definitions, density conversion and pitfalls (section 3), scaling (section 6), locale detection and conventions (section 7), the method and ingredient-line rules (sections 2 and 4), and oven modes with °F to °C conversion (section 5)

@../\_shared/culinary-craft.md **Read when:** reviewing the reworked recipe: the review checklist (section 5.1) and failure modes (section 5.2), and the identity core before adapting a traditional dish (section 4)

@../\_shared/cooking-from-what-is-on-hand.md **Read when:** the user asks for a substitution or an ingredient is unavailable or excluded: substitutions by function (section 6)

@../\_shared/food-safety.md **Read when:** the source holds a safety warning or a high-risk step (section 6), the household has a vulnerable member (section 7), or the region's rules decide a time or temperature (section 2); the final checklist is section 10

@../\_shared/nutrition-and-guidelines.md **Read when:** the user mentions a condition, a medicine, or a calorie, weight or carbohydrate target (referral, section 6), `Allergies and hard exclusions` is set or the request names an allergy or exclusion (compound items and cross-contact, section 4), the user asks to adapt the recipe to a guideline, or `Household` lists an infant, toddler, child, pregnant or older member (cooking levers in section 2, life-stage rules in section 3, base plus branch in section 5.2, descriptive wording in section 7.1)

@../\_shared/recipe-format.md **Read when:** placing the source line, the original values and the conversion convention in the saved file (frontmatter `source` and `source-url`, the notes section)

# Rework Recipe

This skill takes an existing recipe and restructures it to the user's preferences, flagging every real recipe change. It follows `../_shared/skill-contract.md` (language, address form, tone and the hard-constraint check included); the steps below are its own work and its hand-off to `export-recipe`. Everything shown to the user is in the output language.

Tandoor recipes as a source arrive with phase 2; say so in one line if asked.

## Step 1: Get the source

`$ARGUMENTS` or the conversation holds the source. Ask for it if neither does.

- Pasted text: use as is.
- URL: fetch it with WebFetch and extract the recipe. If the fetch fails or is blocked, ask the user to paste the text.
- Photo of a page: transcribe it first. Show every unclear quantity, unit or word as a question, never as a guess, and get the user's confirmation of the transcript before reworking.
- Saved recipe file: read it. The original file stays untouched: the result is always a new file written by `export-recipe`, and you say so.

Keep the source text and its provenance (author, title, site or book, URL) apart from what you write. Extract ingredients, amounts, preparation states, equipment, times, temperatures, warnings and doneness cues; ask about ambiguity, never resolve it silently.

## Step 2: Hard constraints and intent

Collect the hard constraints before reworking: `Allergies and hard exclusions`, the `Household` life stages and any registered guideline. A source ingredient that breaks one is substituted and flagged, or the user is told that no safe version exists. Never keep it for fidelity.

A household with an infant or toddler, in `Household` or named in the request, gets base plus branch as set out in the contract's "Household: base plus branch" section. When the source has no such split, adding the split step is a recipe change and is flagged.

When the request does not say what to change, assume a restructure to the preferences (house style, language, units) and do not ask. Scale, substitute or adapt to a guideline only when the request asks or hints at it; adapting to a guideline happens only on request, and then lean the recipe toward registered soft targets and guideline preferences, meeting per-person targets through branches (`nutrition-and-guidelines.md` section 5.2, rule 3), with no nutrition claims. Keep the dish's identity core (`culinary-craft.md` section 4) or label the result a variation; never call a modified traditional dish "authentic".

## Step 3: Detect the source locale

Before converting any unit, work out where the source comes from: its spelling, units, language, site domain and wording ("stick of butter", "Esslöffel", "tablespoon" with a metric amount). Cups, tablespoons and ounces differ by country, so apply `recipe-writing.md` sections 3.2 and 7. When the locale is unclear and it changes the conversion, ask one question. Whatever you decide, state the convention used in the result, for example "US cups (240 ml), US tablespoons (15 ml)".

## Step 4: Rework

Sort every change by the risk table in `recipe-writing.md` section 8.1.

Free changes are made silently, as long as no warning, cue, temperature or reserved portion (pasta water or a share of the sauce set aside for later) is lost: wording in the house style, splitting and merging steps with their ingredients attached, grouping, headings, translation, units within one system. Warnings and doneness cues are never dropped, and a safety-critical step is never changed.

Recipe changes are each flagged: volume to weight with ingredient-specific densities, regional unit conversion, °F to °C (give the conventional and the fan value, `recipe-writing.md` section 5.1), scaling (never linear for time, salt, leavening or reductions), a changed oven mode or pan, substitutions (say what changes, using `cooking-from-what-is-on-hand.md` section 6) and guideline adaptations. Take every number from a documented source in `recipe-writing.md`, round without drift, and label what you could not verify as not retested. A conversion that depends on how the ingredient is packed or cut (flour, brown sugar, chopped nuts) uses the form named in the source.

Rewrite the method in neutral wording of your own. Drop the source headnote and personal story; do not paraphrase them closely. Never copy method prose, photos or distinctive wording.

Build the result as one structured model: title, language, servings, times, tags, oven mode and temperatures, ordered steps that each carry the ingredients they use (an ingredient used in two steps is split between them), and notes. `export-recipe` saves exactly this.

Before showing it, run the `culinary-craft.md` section 5.1 checklist silently; for anything that fails, suggest a change instead of making it, because a change to the recipe is a flagged recipe change; then reconcile against the source: every ingredient used, allocations add up, optional items still optional, warnings kept. Run the `food-safety.md` section 10 checklist. A safety note goes at the point of use, in the step itself (`recipe-writing.md` section 4.4), not only in the notes. Never print a checklist.

## Step 5: Show it in chat

Order: servings, ingredients, preparation, cooking, notes. `Recipe layout` sets where ingredients appear: `ingredients-up-front` (default) shows one overview derived from the steps before the method; `per-step` lists each step's ingredients with that step. `Separate preparation section` `yes` (default) puts chopping and measuring in a short block before cooking, except tasks that need freshness, follow a transformation or carry a safety order (`recipe-writing.md` section 4.3); `no` integrates them. This is the chat view only; the saved file always uses `recipe-format.md`.

After the recipe, show a short "Changes" list for the recipe changes only, one line each with its reason (for example "Flour 1 cup to 125 g: all-purpose flour, spooned and levelled" or "Whole-grain flour absorbs more liquid, add 2-3 tbsp water"). State the unit convention and the testing status: reformatted with quantities unchanged; units converted and not retested; adapted with substitutions and not retested. Say plainly that the numbers were not test-cooked. Free changes are not listed.

## Step 6: Attribution and notes

Put the attribution in frontmatter `source`, worded in the output language, with `source-url` when known. Choose the tier from `recipe-writing.md` section 8.4: "adapted from" when the result closely follows the source, "inspired by" when the source only supplied an idea. German example: `Adaptiert nach <Titel>, <Autor>, <Quelle>`. Never strip the attribution and never present the result as original. A saved source file that already has `source` or `source-url` passes them on unchanged. When the author is unknown, say so; never invent one.

The saved file's notes section holds the original amounts and units of every converted or substituted ingredient, the conversion convention used, and the testing status. Free changes need no note.

## Step 7: Save via export-recipe

Follow `../export-recipe/SKILL.md` from Step 1, with the recipe already in the conversation; it writes a new Markdown file, never overwriting the source file, and handles the configured target. Then run the contract's feedback step once for the whole run, tagged `[cc-chef:rework-recipe]`.
