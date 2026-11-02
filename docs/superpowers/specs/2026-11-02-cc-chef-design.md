# cc-chef — Plugin Design

Date: 2026-11-02. Status: draft for owner review. Inputs: `docs/skill-ideas.md` (intent and captured ideas), the research results in `docs/research/` (five topics, several tools each), and the brainstorming conversation of 2026-11-01/02.

Markers used below: **(owner)** = decided by the owner in conversation; **(call)** = decided by the designer, open to the owner's veto; **(builder)** = left to whoever builds it.

## 1. Intent

cc-chef is a public plugin in the clever-cc-plugins marketplace for creating, adapting, reworking and exporting recipes. It grew out of two Claude.ai project prompts the owner used; their output was cookable but lacked culinary finesse, and getting recipes into a recipe app (Tandoor) still meant a lot of manual reordering and polishing.

**Quality bar (owner):** grounded, cookable everyday food — comfort food, traditional fare, rustic home cooking — with one or two deliberate touches (a spice, a finishing element, a contrast) that make a dish worth remembering. Not experimental, not star-chef complexity.

**Why the research matters:** the research translated this bar into concrete, checkable rules (see section 6). The plugin's value is applying those rules consistently, not carrying a large food or diet database.

## 2. Goals, non-goals, anti-goals

**Goals**

- Recipe ideas from a mood, an ingredient list, a fridge/pantry photo, or a named dish; full recipes that meet the quality bar.
- Reworking existing recipes (pasted text, URL, photo of a page, or a Tandoor recipe) into the user's preferred structure, optionally adapted to dietary guidelines.
- Opt-in personal dietary guidelines, applied by every skill when present; the plugin works fine without them.
- A research-prompt skill so users with special dietary needs can research them with a deep-research tool and bring the result back as context (owner: "the plugin skills cannot provide useful dietary information for a wide range of use cases without carrying a huge database").
- Recipes leave the plugin in a form recipe apps import well; for Tandoor, with ingredients matched to the user's food database and attached to the steps that use them.
- Tandoor maintenance: restructuring already-imported recipes and cleaning up a messy food database.
- Language-agnostic: works in any language; output language is a user preference.

**Non-goals (v1)**

- The plugin keeps no recipe collection of its own beyond saved files; recipe management is the recipe app's job. **(call)**
- Meal planning, shopping lists, pantry stock tracking. **(call)**
- API integrations other than Tandoor (Mealie, Nextcloud Cookbook, KitchenOwl, Grocy). File export covers those apps for now; Mealie is the most likely next adapter. **(call)**
- Cooklang, Mela, MasterCook, Meal-Master writers. **(call, following research)**

**Anti-goals (failure even if it technically works)**

- Generic, flat, over-spiced "AI recipes" — the failure modes listed in section 6.1.
- Experimental or fusion cooking as a default; "authentic" labels on modified dishes.
- Medical nutrition therapy: therapeutic diets, carbohydrate targets for insulin users, renal limits, calorie or weight targets. The plugin supports healthier everyday eating and does not replace medical or dietetic advice.
- Food-safety judgements from photos.
- Silent changes to a user's Tandoor data: no write without a preview and explicit OK; no silently created duplicate foods.
- Reproducing a source recipe's expressive text verbatim, or presenting a reworked recipe as original.

## 3. Constraints

- **Ecosystem conventions:** repo layout, `.claude/` hooks, pre-commit, CLAUDE.md and marketplace entry per `marketplace/docs/cc-plugin-repo-guideline.md`. Skills invoked namespaced (`/cc-chef:<skill>`). Learnings tagged `[cc-chef:<skill>] <observation> — <YYYY-MM-DD>` in `.claude/learnings.md`.
- **Context management like the siblings:** a `## Context files` table in the user's `CLAUDE.md`; skills find their context by semantic match on the Summary column, never by label or filename; context enriches but never gates (skills run with sensible defaults when nothing is registered). Onboarding recognises context an existing project already provides (see `cc-career/plugins/cc-career/skills/career-onboarding/SKILL.md` for the pattern).
- **Shared skill contract:** a `plugins/cc-chef/skills/_shared/skill-contract.md` defines the step sequence all skills follow (silent learnings recall at Step 0, context loading, the skill's work, feedback with auto-stored learnings), as in `cc-coach/plugins/cc-coach/skills/_shared/skill-contract.md`. SKILL.md files reference it instead of restating it.
- **HTTP under restrictive settings:** projects set up by cc-config (and the ecosystem baseline) deny `Bash(curl:*)` and `Bash(wget:*)`, and the guard hook blocks reading `.env*` files. Tandoor access therefore can't rely on curl or on a `.env` file in the project. **(call)** A bundled, standard-library-only Python script (`plugins/cc-chef/scripts/tandoor.py` or similar), invoked via Bash, does all Tandoor HTTP. The instance URL and API token come from environment variables (e.g. `TANDOOR_URL`, `TANDOOR_TOKEN`) set in the user's shell or keychain-backed tooling; the token is never written to the project or echoed into the conversation. Exact invocation and the `allowed-tools` needed are **(builder)**.
- **Public plugin:** nothing may assume the owner's setup. Tandoor features activate only when the user has configured an instance; everyone else gets file export.
- **Evidence honesty:** nutrient values are shown as rounded ranges with their data source; health statements use descriptive wording, not health claims (EU 1924/2006).

## 4. Skills

Order of build: **phase 1** = recipe core (4.1–4.6, with file export only); **phase 2** = Tandoor (4.6 upload, 4.3 Tandoor source/target, 4.7). **(call — the owner did not pick an order; the Tandoor export needs the recipe model the core produces)**

### 4.1 `chef-onboarding`

Sets up and registers the user's cooking context. Interview-based, one question at a time, with defaults offered. Collects into a preferences context file (path proposed, user can change it):

- output language and units (metric/imperial, weights preferred or not)
- region/country — sets the food-safety rule set (leftover limits, reheating) and unit conventions (AU tablespoon, JP cup, etc.)
- default servings; preferred recipe layout (see 4.2 output); whether to separate "preparation" from "cooking"
- household members with life stage (infant, toddler, child, pregnant, adult, older adult) — triggers automatic safety rules; no health data is required here
- equipment (oven with/without fan, etc.) and assumed staple pantry
- likes, dislikes, cuisines, time and skill
- recipe target: Tandoor (instance configured), a file format for another app, or plain saved files; and the save folder. The folder is always the user's choice (**owner**): onboarding proposes a name in the user's output language (e.g. `Rezepte/` for German, `recipes/` for English) or an existing folder it finds in the project, and the user can pick any path. Skills never hard-code a folder name.

Also registers existing files the user already has (e.g. the owner's food list with cholesterol, iron and fibre values in their personal-assistant repo) and states the plugin's health disclaimer once. Offers — but never pushes — `dietary-guidelines`.

### 4.2 `create-recipe`

Carries over the owner's Claude.ai flow:

1. **Input:** mood/description, ingredient list ("what needs to be used"), fridge/pantry photo, or a named dish. A named dish skips straight to step 4.
2. **Photo → draft inventory.** The model lists recognised items with confidence; the user confirms or corrects items, rough quantities and condition before anything is planned. No model is required beyond what the session runs; the confirmation step is the safeguard (research: good at naming common items, weak at quantity, freshness, packaged goods). Never judge spoilage or safety from the image.
3. **Ideas:** rank on-hand ingredients by perishability (safety-critical first: raw fish, poultry, mince, cooked rice; then quality: soft herbs, greens, berries, opened dairy); fill one of ~12 dish templates (section 6.2); present **3** clearly different ideas by default, each with time, which on-hand items it uses and what (little) must be bought. The user can ask for more, up to 5. **(call, following research; the owner's old prompt used up to 5)** Ideas should be quick and uncomplicated by default (owner's old prompt). Assume only salt, a cooking fat and water unless the registered pantry says otherwise. Where a web-search tool is available, ground ideas and traditional dishes in real recipes found on the web (the owner's old prompt did this; `skill-ideas.md` names grounding in real recipes as part of reaching the quality bar); without one, rely on the reference files. Found recipes are inspiration, not text to copy.
4. **Full recipe** for the chosen idea, built as the structured recipe model (section 5), reviewed against the culinary checklist (6.1), constrained by registered guidelines and preferences, with region-appropriate safety notes. Default layout (owner's defaults, overridable in preferences): servings up front; ingredients; preparation; cooking; weights preferred; oven mode and temperature (conventional and fan in metric locales); times paired with visual doneness cues; closing notes on serving, side dishes and drinks; the dish's one "signature" touch named in a sentence.
5. **Output:** presented in chat; then saved or exported via `export-recipe` according to the configured recipe target (no app → saved as a file, **owner**).

### 4.3 `rework-recipe`

Takes an existing recipe and restructures it to the user's preferences. Sources: pasted text, URL, photo/scan of a page, a saved recipe file, or (phase 2) a Tandoor recipe.

- **Restructure (free changes):** wording in neutral house style, step splitting into steps that make sense for the dish with their ingredients attached, grouping, headings, language, units within a system. Warnings and doneness cues are never dropped.
- **Changes to quantities or ingredients are recipe changes:** volume→weight with ingredient-specific densities (stating the convention used), regional units only after detecting the source locale, scaling (never linear for time, salt, leavening, reductions), substitutions. Each is flagged, explained (e.g. "whole-grain flour absorbs more liquid — add 2–3 tbsp water"), and the original kept in the notes.
- **Adapt to guidelines (on request):** swap hindering ingredients for helpful ones from the registered guidelines; respect the dish's identity core or label the result as a variation.
- **Attribution:** keep "Adapted from <title>, <author>, <source>" by default; never reproduce headnotes or distinctive prose verbatim; never present the result as original.
- **Tandoor mode (phase 2):** reads a recipe from the instance, restructures it, maps ingredients to the user's food database (4.6 matching), shows a preview, and updates the recipe in place after OK. Processed recipes get a marker keyword (e.g. `cc-chef`, **call**) so later runs can tell polished from unpolished recipes. The user names which recipes to process; the plugin does not guess which ones were hand-tweaked.

### 4.4 `dietary-guidelines`

Opt-in only — runs when the user asks. Drafts a personal guideline context file (one per household member, or one household file with per-member sections, **builder**) from an interview, from research results (e.g. produced via 4.5), or both, then registers it.

- **Screening first:** medications, kidney disease, diabetes on insulin/sulfonylureas, anticoagulants, pregnancy (and complications), eating-disorder history, allergies/anaphylaxis. For referral conditions (section 6.4) the skill declines to write therapeutic rules and points to a doctor or registered dietitian; it may still record clinician-set limits exactly as the user reports them.
- **Guideline structure** (from research): profile (age band, life stage, country) → hard constraints (allergens with severity and cross-contact, coeliac, clinician-set limits, absolute religious/ethical exclusions) → automatic safety rules triggered by profile (toddler, pregnancy) → soft targets, each tagged with evidence source and certainty → preferences → review triggers.
- **Households:** "base + branch" — the strictest safety rule applies to the shared base; individual targets are met through branches, sides and toppings (research example: adult with high LDL and a toddler needing iron, from one pot).
- **Content defaults:** the convergent healthy-pattern core (Mediterranean, DASH, Portfolio, Nordic, DGE 2024, etc.); where the US DGA 2025–2030 diverges (protein, full-fat animal foods), follow WHO/AHA/ACC and say so. "Raise HDL" is not a valid diet target — target LDL instead (relevant to the owner's old prompt 2).

### 4.5 `research-prompt`

Same pattern as `cc-content:research-prompt` and `cc-coach:research-prompt`: vendor-neutral, produces only the prompt in a delimited copy-paste block, runs no research, saves nothing. Topic here: a diet, intolerance, condition-related pattern, cultural or religious practice, or cooking constraint. **(call)** The generated prompt asks for practical cooking guidance — foods to prefer, limit or avoid; swaps and how they change preparation; hidden sources; safety notes; evidence grading and sources — so the result converts easily into a guideline via 4.4. The closing line points to `dietary-guidelines` for turning the result into context. Referral boundaries still apply downstream: researching a renal diet does not make 4.4 write one.

### 4.6 `export-recipe`

Turns the structured recipe model into the configured target. Also invoked by 4.2 and 4.3 at the end of a run.

- **Plain saved file (no app, owner):** one file per recipe in the configured save folder (from preferences; if none is configured, ask once and offer to store the answer). **(call)** Markdown with YAML frontmatter (title, servings, times, language, tags, source/attribution, format version) and a fixed, parseable body layout that keeps the full model — steps with their attached ingredients, ingredient sections, notes — so the file can later be uploaded to Tandoor or exported without loss, while remaining readable in any Markdown viewer. The exact layout is **(builder)**; the saved file uses one fixed layout regardless of the user's chat-display preference. Filename collisions get a numeric suffix.
- **schema.org Recipe JSON-LD** file (plain-string `recipeIngredient` lines in "quantity unit food, note" order; `HowToSection`/`HowToStep`; `inLanguage`) — imports into Mealie, Nextcloud Cookbook, Crouton, RecipeSage and others.
- **Paprika `.paprikarecipes`** (zip of gzipped JSON; ingredient sections as heading lines ending in `:`) — reaches Paprika, AnyList, Cookmate, and bulk paths into Mealie/Tandoor.
- **Tandoor upload (phase 2):** via the API, with steps and step-attached ingredients sent as structure, not text. Before creating anything: fetch the instance's foods and units, map every ingredient to an existing entry (including existing Food Alias / Unit Alias automations), split each line into amount, unit, food and note (preparation details and qualifiers go to the note, never into the food name), and list ingredients without a confident match for the user to decide: create new, or map to an existing food. Show a preview (steps, attached ingredients, new database entries); write only after OK.

### 4.7 `tandoor-food-cleanup` (phase 2)

Cleans up the user's Tandoor food (and unit) database. Owner context: a few dozen imported recipes polluted a database originally imported from Tandoor's recommended open-data sources, with duplicates and with recipe-level information (quantities, preparation) stored in food names.

1. Read all foods and units; propose duplicate groups, each with a suggested entry to keep (default: the one with nutrition properties, typically from the open-data import), and list foods whose names contain preparation or quantity details.
2. The user reviews and approves group by group; nothing changes before that.
3. Per approved group: move the extra details from the food name into the note of every affected recipe ingredient; merge the duplicates into the kept entry; add a Food Alias automation so future imports map correctly.
4. Work in small batches with a summary after each. Recommend an instance backup before the first run (merges are irreversible).

**Tandoor facts checked against the default branch of `TandoorRecipes/recipes` on 2026-11-02 (`cookbook/views/api.py`, `cookbook/models.py`) — verify against the user's instance API schema before relying on them:**

- Foods, units and supermarket categories expose `PUT /api/<type>/<id>/merge/<target_id>/`. The merge re-points every related object (so all recipe ingredients move to the target automatically) and deletes the source.
- Merging a food deletes the source food's properties (nutrition values) and its unit conversions; merging a unit deletes conversions involving it. Hence "keep the entry with nutrition data".
- Information embedded in the source food's name is not carried anywhere — step 3's note migration must happen before the merge.
- Foods are a tree; a food cannot be merged into its own descendant.
- `Automation` types include `FOOD_ALIAS`, `UNIT_ALIAS`, `NEVER_UNIT` and `TRANSPOSE_WORDS`.

## 5. The structured recipe model

One internal model connects creation, reworking, saved files and every exporter. Without it, each exporter would have to re-parse text and step-ingredient links would be lost again — the owner's main pain with imports.

Per recipe: title, language, servings, times (prep, cook, total), source and attribution, tags, notes (serving, sides, drinks), signature touch, oven mode and temperatures, and an ordered list of steps. Per step: instruction text (goal first, one main action, sensory cue with any time) and the ingredients used in that step. Per ingredient: amount (number or range, or none for "to taste"), unit, food (locale name), note (preparation, form such as "packed" or "chopped"), section (component group), optional flag, and — for converted values — the original amount and unit and the conversion convention used. An ingredient used in several steps is split per step. A flat ingredient overview is derived from the steps for display and for formats without step links (schema.org, Paprika). Concrete representation is **(builder)**.

## 6. Knowledge base — distilled research in `_shared/`

The research becomes compact reference files in `plugins/cc-chef/skills/_shared/`, loaded by skills on demand. **Build work:** the designer read only the Claude report per topic in full; the builder must merge all reports per topic (Claude, ChatGPT, Consensus, Copilot, DeepSeek, Gemini, Perplexity, where present), resolve conflicts, keep evidence grading, and mark claims supported by a single report as "to verify". Reference files distil the knowledge in the plugin's own words; they don't copy report text. Proposed files (**call** on the split, **builder** on content):

### 6.1 `culinary-craft.md`

Balance (salt in stages, acid, umami, fat, sweetness only to balance); depth (aromatics cooked in fat, blooming spices, browning without crowding, deglazing, reduction); contrast and finish (exactly one finishing element from the same or a neighbouring tradition); molecule-based "food pairing" is not a basis. Identity core vs. regional variables vs. finesse levers for traditional dishes, with worked examples; the test "would a good home cook from that tradition call it a very good version?"; label variations honestly. The review checklist (identity, seasoning, depth, contrast, signature and restraint, practicality) and the table of typical AI-recipe failure modes with fixes.

### 6.2 `cooking-from-what-is-on-hand.md`

~12 structural dish templates (egg-bound bakes, stir-fry/fried rice, soup/stew, curry, pasta, grain bowl, savoury pancake, hash, gratin, tart, composed salad, …) with slots, base ratios and a seasoning layer; perishability tiers; pantry assumptions by region; substitutions by function (structure, moisture, fat, leavening, binding, emulsifying, acid, sweetness, flavour) with "fails in" cases (baking, emulsions, set custards); photo-inventory confirmation practice; option presentation (3 distinct "shapes").

### 6.3 `recipe-writing.md`

Recipe anatomy; ingredient order and grouping; prep-note placement ("1 cup walnuts, chopped" vs. "1 cup chopped walnuts"); weight vs. volume and regional unit definitions (US/AU/JP cups, AU tablespoon); dual units and rounding; method writing (goal first, one action per step, time plus cue, warnings at the point of use, quantities repeated in steps); oven modes and fan offsets; scaling rules; per-locale conventions (grammatical mood, headings, ingredient naming, package sizes) for at least German, English, French, Italian, Spanish, Japanese; restructuring risk table; attribution tiers ("adapted from", "inspired by").

### 6.4 `nutrition-and-guidelines.md`

The convergent healthy-pattern core; graded cooking levers (LDL, fibre, iron, blood pressure, glucose, gut, cooking methods) with certainty tags; life-stage rules (infants/toddlers, children, pregnancy, older adults); allergens (EU 14, US 9) and cross-contact; the guideline-document structure and base + branch; referral triggers and the behaviour table; claims to avoid (myths filter); disclaimer contents; nutrient-data guidance (show rounded ranges with source; a user-registered food list takes precedence; open databases: USDA FDC, BLS 4.0, CoFID, Ciqual).

### 6.5 `food-safety.md`

Locale rule table for leftovers and reheating (USDA FSIS, UK FSA, German BfR, others found in the reports); default to the strictest rule when the region is unknown; high-risk items (cooked rice, nitrate-rich vegetables, poultry, etc.); stricter rules for vulnerable groups.

### 6.6 `export-formats.md` and `tandoor-api.md`

schema.org Recipe fields and parser behaviour; Paprika archive format; coverage matrix of apps (to be re-verified at build time — app status changes, e.g. ManageMeals URL-import-only and Recipya stagnating are single-source claims); Tandoor endpoints for recipes, foods, units, keywords, automations and merges, with request shapes verified against a live instance's OpenAPI schema.

## 7. Behaviour across all skills

- **Context use:** load preferences, guidelines and registered food lists when present; state in one line whether the run is personalised and with what. Without context: ask only what the task can't proceed without (e.g. servings), otherwise use defaults.
- **Hard constraints are hard:** allergens and life-stage safety rules are checked against every recipe; never relaxed for flavour.
- **Nutrient values:** shown only when a registered guideline has quantified targets or the user asks; as rounded ranges with the data source; never presented as precise enough for clinical use. **(call)**
- **Health disclaimer:** stated in onboarding and in `dietary-guidelines`, not appended to every recipe; referral behaviour in conversation does the real work. **(call)**
- **Language:** output language from preferences, else the language of the conversation; skills' own instructions are written in English. In German, address the user with "du" by default (owner's prompts; a preference can change the default for other users).
- **Tone (carried over from the owner's prompts):** clear, conversational, honest; no hype or advertising words; no flattery; ask when a request is ambiguous.
- **Feedback and learnings:** per the shared contract, tagged `[cc-chef:<skill>]`.

## 8. Left to the builder

- Concrete recipe-model representation and the saved-file layout (constraints in 4.6 and 5).
- Merging the research reports into the `_shared/` files (section 6), including resolving conflicts between reports.
- Tandoor script interface, request shapes, pagination, error handling, and the exact `allowed-tools` per skill.
- Ingredient-matching approach (fuzzy match, alias use, confidence threshold) as long as unmatched items always go to the user.
- Duplicate-detection heuristics for food cleanup.
- Evals or test scenarios per skill; README content; CLAUDE.md config table.
- Whether `rework-recipe`'s Tandoor mode needs its own skill after all, if the SKILL.md gets too long.

## 9. Owner inputs and testing

- **Owner inputs:** `docs/owner-inputs/` holds `project-prompt-1.md` (general recipe prompt), `project-prompt-2.md` (health-focused variant) and `Lebensmittelliste.csv` (107 foods; columns: category, food, good for cholesterol yes/no, iron per 100 g, amounts for 7/10 mg iron, fibre per 100 g, amounts for 15/30 g fibre; semicolon-separated, German decimal commas, multi-line quoted headers, UTF-8 with BOM). The folder is gitignored because the repo is public and the prompts contain personal health details — never commit it, and don't quote personal details from it into committed files. Use the prompts to carry over the owner's defaults (already reflected in 4.2) and the CSV as the test case for registering an existing food list.
- **Tandoor testing (owner):** the builder may use the owner's live Tandoor instance; German recipes are fine as test data. Develop and test read operations first; test writes on dedicated test recipes created for the purpose (removed afterwards); run food merges only through the skill's normal per-group approval with the owner, after an instance backup. The instance's own API schema is the reference for request shapes.
