---
name: create-recipe
description: >
  Use this skill to turn a mood, a list of ingredients, a fridge or pantry photo, or a named dish into recipe ideas and then one full, cookable everyday recipe. Invoke when the user says "what can I cook with this", "I need to use up chicken and courgette", "here's a photo of my fridge, what can I make", "I fancy something warm and comforting", "write me a recipe for goulash", or "Was kann ich mit Reis und Zucchini kochen?". Reads the cooking preferences and any registered guidelines, and hands the finished recipe to export-recipe for saving. Do NOT use it to adapt or restructure an existing recipe (use rework-recipe) or to save or convert an already finished recipe (use export-recipe).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
argument-hint: "[optional: ingredients, a mood, a dish name, or a photo path]"
---

@../\_shared/cooking-from-what-is-on-hand.md **Read when:** the input is a mood, an ingredient list or a photo: workflow (section 1), perishability tiers (section 2), pantry assumptions (section 3), dish templates (section 4), photo handling (section 7), the idea cards (section 8) and the open points to settle before any full recipe, named dish included (section 8.5)

@../\_shared/food-safety.md **Read when:** the inventory or recipe holds cooked leftovers or a high-risk food (section 6), the household has a vulnerable member (section 7), or a safety note is written (decision rules in section 1, the region's authority in section 2, the checklist in section 10)

@../\_shared/nutrition-and-guidelines.md **Read when:** the user mentions a condition, a medicine, or a calorie, weight or carbohydrate target (referral, section 6), `Allergies and hard exclusions` is set or the request names an allergy or exclusion (compound items and cross-contact, section 4), `Household` lists an infant, toddler, child, pregnant or older member (life-stage rules, section 3; base plus branch, section 5.2), a guideline is registered (cooking levers, section 2; allergens, section 4), or nutrient values are shown (nutrient data, section 8; descriptive wording, section 7.1)

@../\_shared/culinary-craft.md **Read when:** drafting the full recipe: the review checklist (section 5.1), the AI failure modes (section 5.2), and the identity core of a named traditional dish (section 4)

@../\_shared/recipe-writing.md **Read when:** writing ingredient lines, units, the method and oven modes (sections 2-5), placing preparation (section 4.3), and applying locale conventions (section 7)

@../\_shared/recipe-format.md **Read when:** checking that the finished recipe carries every field the saved file needs (frontmatter keys, steps with their own ingredients, notes)

# Create Recipe

This skill turns a mood, an ingredient list, a photo or a named dish into ideas and then one full recipe of grounded everyday quality: comfort food, traditional fare, rustic home cooking, with one deliberate touch that makes it worth remembering; never experimental or star-chef. It follows `../_shared/skill-contract.md` (language, address form, tone and the hard-constraint check included); the steps below are its own work and its hand-off to `export-recipe`. Everything shown to the user is in the output language. The first reply opens with the contract's framing line (its Step 2), before any idea, question or recipe.

Where a web-search tool is available, ground ideas and traditional dishes in real recipes found on the web; found recipes are inspiration, never text to copy. Without one, rely on the reference files.

## Hard constraints and the household

Collect the hard constraints before the first idea or recipe: `Allergies and hard exclusions`, the `Household` life stages and any registered guideline. They apply to the shared base, so the whole meal honours them, not one plate. An on-hand item that breaks one is left out with a one-line reason; an idea that would break one is never offered, or is adapted and says so in one line; a requested dish that breaks one is adapted, or declined when no safe version exists, and the answer says so in one line.

A household with an infant or toddler, in `Household` or named in the request, gets base plus branch as set out in the contract's "Household: base plus branch" section: unsalted shared base, the child's portion taken off first, said in the method at that step.

## Step 1: Read the input

- Named dish: skip the ideas and go to Step 4.
- Photo: show a draft inventory grouped by confidence in words (confirmed, likely, unsure, not visible), per `cooking-from-what-is-on-hand.md` section 7.2. Before planning, the user confirms or corrects the items, rough quantities of the main ingredients and the condition of key perishables (section 7.3). Never judge spoilage, freshness or safety from the image; phrase what you see as a prompt ("check the use-by date on the chicken"). Allergens are never read from a photo.
- Ingredient list or mood: build the inventory per `cooking-from-what-is-on-hand.md` section 1; a mood narrows the template choice.

## Step 2: Rank and screen

Rank the confirmed items by perishability (`cooking-from-what-is-on-hand.md` section 2): the safety-critical tier first (raw poultry, fish, mince, cooked rice), then the quality tier. For a tier A item with unknown history, ask only what decides eligibility (when it was cooked, how fast it was chilled, per `food-safety.md` section 1, rule 4), in the same reply as the ideas: an idea that uses it is marked as conditional on the answer, and the ideas are never held back for it. Leave out anything with an unsafe history, or one still unknown when the full recipe is written, and say so. Screen what remains against the hard constraints.

## Step 3: Offer ideas

Offer 3 clearly different ideas by default, up to 5 when the user asks for more, following `cooking-from-what-is-on-hand.md` section 8: different in shape first, flavour second, best match first with a few words on why. Every idea is a card with the same fields in the same order (its section 8.3), including the time, the on-hand items it uses (urgent ones marked), the few items to buy, and the pantry assumptions: only salt, a cooking fat and water unless `Staple pantry` says otherwise (its section 3). A high-risk item carries a short safety note in its card, using the rule of the authority for `Region` (`food-safety.md` section 2; the strictest default if no region, said once). Keep ideas quick and uncomplicated by default, within `Time and skill` and `Equipment`, and lean on `Likes`, `Dislikes` and `Cuisines`, and toward any registered soft targets and guideline preferences, meeting per-person targets through branches (`nutrition-and-guidelines.md` section 5.2, rule 3), with no nutrition claims. No recipe steps yet; end with one narrow question: which idea to turn into a full recipe.

## Step 4: Write the full recipe

Settle the open points first (`cooking-from-what-is-on-hand.md` section 8.5): servings (`Default servings`, else ask), usable amounts, equipment, any leftover-safety question, substitutions. Build the recipe as one structured model: title, language, servings, prep and cook times, tags, signature touch, oven mode and temperatures, ordered steps that each carry the ingredients they use (an ingredient used in two steps is split between them), and notes, plus `source` and `source-url` when a found web recipe was adapted (`recipe-writing.md` section 8.4). `export-recipe` saves exactly this, so keep the step-ingredient links whatever the chat layout.

Lean the recipe toward registered soft targets and guideline preferences too, meeting per-person targets through branches (`nutrition-and-guidelines.md` section 5.2, rule 3), with no nutrition claims.

Defaults, overridable by preferences: weights preferred, per `Units`; oven mode with temperature, conventional and fan in metric locales; times paired with visual doneness cues; closing notes on serving, side dishes and drinks. For a named traditional dish, keep its identity core and never call a modified version "authentic".

Before showing it, run the `culinary-craft.md` section 5.1 checklist silently and fix what fails, check its section 5.2 failure modes, and run the `food-safety.md` section 10 checklist; never print a checklist. Name the dish's one signature touch in a sentence. Where a high-risk item is involved (day-old rice, poultry, mince), add a short safety note at the point of use, in the step itself (`recipe-writing.md` section 4.4), not only in the notes, with the rule of the authority for `Region` (`food-safety.md` section 2; with no region, the strictest default, and say so), worded as "within the cited limit", never "safe".

Nutrient values appear only when a registered guideline has quantified targets or the user asks: rounded ranges with the data source (`nutrition-and-guidelines.md` section 8.4), and a registered food list takes precedence over any database. Wording stays descriptive, never a health claim; no disclaimer here.

## Step 5: Show it in chat

Order: servings, ingredients, preparation, cooking, notes. `Recipe layout` sets where ingredients appear: `ingredients-up-front` (default) shows one overview derived from the steps, grouped by component, before the method; `per-step` lists each step's ingredients with that step. `Separate preparation section` `yes` (default) puts chopping and measuring in a short block before cooking, except tasks that need freshness, follow a transformation or carry a safety order (`recipe-writing.md` section 4.3); `no` integrates them into the method. This is the chat view only; the saved file always uses `recipe-format.md`.

## Step 6: Save via export-recipe

Follow `../export-recipe/SKILL.md` from Step 1, with the recipe already in the conversation; it saves the Markdown file and handles the configured target. Then run the contract's feedback step once for the whole run, tagged `[cc-chef:create-recipe]`.
