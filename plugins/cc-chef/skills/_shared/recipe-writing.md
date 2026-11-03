# Recipe writing

Use this file for writing, restructuring, localising and exporting the text of a recipe: `create-recipe` uses it to lay out a new recipe in the saved format, `rework-recipe` uses it when it reorders, converts, scales, translates or re-attributes an existing one, and `export-recipe` uses it to render a saved recipe for a target locale or app. It covers the anatomy of a recipe, ingredient lines, units, method wording, oven and pan handling, scaling, per-language conventions, the risk of each kind of restructuring and attribution. It does not judge flavour (see `culinary-craft.md`) or storage and reheating safety (see `food-safety.md`). Sections 1-4 are the recipe body, section 5 heat and equipment, section 6 scaling, section 7 locale, section 8 restructuring and attribution, section 9 readability, section 10 the evidence notes.

Conventions: `(to verify)` marks a claim that only one research report made. "Default" is what the plugin does when reports disagree. Evidence tags: strong = measurement, regulation, physics or controlled study; moderate = test-kitchen measurement or research that transfers by analogy; convention = editorial or publisher practice; design = a rule chosen for this plugin.

## 0. The core rule

Presentation (order, grouping, headings, wording, language) can be changed freely. Quantities, ingredients, equipment and process cannot: converting a unit, scaling, swapping an ingredient or changing the oven mode creates a new version of the recipe. The plugin cannot test-cook, so every such change is made from a documented source, flagged, and the original value is kept in the notes section of the saved file (design).

| Layer           | Examples                                                                                  | Treatment                                                                        |
| --------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Presentation    | Order of ingredients, step splitting, headings, translation of prose                      | Free, as long as no warning, cue or quantity is lost                             |
| Interpretation  | Reading "1 cup walnuts, chopped" as measure-then-chop, deciding a unit's regional meaning | Make explicit; ask or flag when the source locale is unclear                     |
| Culinary change | Unit conversion across systems, scaling, substitution, oven or pan change                 | Source the number, round carefully, flag as untested, keep the original in notes |

## 1. Recipe anatomy

Each element answers a question the cook has before or during cooking. The title-ingredients-method skeleton is convention, not an optimum; what follows is the plugin's default set (convention, design).

| Element             | Purpose                                                                  | Plugin default                                                                                                                                                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Title               | Identify the dish, make it findable and translatable                     | Descriptive, main ingredient plus method or distinguishing trait; no cute or vague names                                                                                                                                                                                      |
| Headnote            | Say what the dish is, the key technique, what can go wrong               | Short and practical (about 50-120 words); longer story only as an optional field. Never hide operational facts here (overnight chilling belongs with the times)                                                                                                               |
| Yield               | Anchor for scaling and meal planning                                     | Structured: count plus unit ("24 cookies", "4 servings"); for bakes add pan size; state portion size separately when it matters                                                                                                                                               |
| Times               | Planning                                                                 | Store active, cooking, waiting (marinate, chill, prove, rest) and total separately, and flag overnight or previous-day work. Total is elapsed time along the real schedule, not the sum of durations. Active time is subjective across publishers, so define it in the output |
| Equipment           | Avoid mid-recipe surprises                                               | List only non-obvious or outcome-critical items (springform, thermometer, stand mixer) with sizes; mention ordinary tools in the step that uses them                                                                                                                          |
| Ingredients         | Shopping list and prep list                                              | Section 2                                                                                                                                                                                                                                                                     |
| Method              | Reproduce the dish                                                       | Section 4                                                                                                                                                                                                                                                                     |
| Notes               | Make-ahead, storage, variations, substitutions, converted-from originals | Kept out of the method so the steps stay clean; substitutions clearly separated from the tested version                                                                                                                                                                       |
| Serving suggestions | Menu planning                                                            | Optional, specific to the dish and the user's locale, never generic filler                                                                                                                                                                                                    |

Consistency across a user's collection matters more than any single choice (convention): one name per ingredient, one yield phrasing, one grammatical mood per language. Enforce it with a per-locale vocabulary.

Where experts disagree: headnote length (cookbook editors want one, many readers skip it); separate equipment list versus equipment mentioned in steps; whether to show active time at all. Default: the choices in the table, with the long forms optional.

## 2. The ingredient list

### 2.1 Order and grouping

| Rule                              | Detail                                                                                                                                                             | Tag                                                                 |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Order of first use                | The strongest consensus across all reports. Where it conflicts with "as you would buy them", order of use wins. Do not alphabetise; offer a separate shopping view | convention, indirectly supported by procedural-instruction research |
| Group by component                | "For the dough", "For the filling", "For the glaze" for multi-part dishes; headings name a culinary object, never "Part 2"                                         | convention                                                          |
| Several items added together      | Larger quantity first (one publisher's rule, not universal)                                                                                                        | convention                                                          |
| List and method must match        | Every listed ingredient is used in a step and every step ingredient is listed; check both directions                                                               | convention, design as an automated check                            |
| Same ingredient in two components | List it under each component with its own amount rather than one "divided" line                                                                                    | convention                                                          |
| Water                             | List it when its amount affects the result (dough, rice, brine, stock); otherwise mention it in the step                                                           | convention                                                          |

The saved format gives each step its own ingredients, so the order-of-use rule is satisfied by construction; the combined list in a rendered export is built by merging the step lists in order of first use (design).

### 2.2 Preparation-note placement

The position of the prep word tells the cook when to measure.

| Wording                                        | Meaning                          | Use when                                                                                      |
| ---------------------------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------- |
| 1 cup walnuts, chopped                         | Measure whole nuts, then chop    | Default for counted or whole items and for anything weighed as bought                         |
| 1 cup chopped walnuts                          | Chop, then fill the cup          | Only when the measured form matters and the amount is by volume                               |
| 1 large onion, finely chopped                  | One onion, then chop             | Counted items: the two wordings give the same count, so use the comma form                    |
| 500 g potatoes, peeled / 500 g peeled potatoes | Differ by the weight of the peel | State which weight governs; give trimmed, drained or cooked weight explicitly when it matters |

- Put prep words in the order the cook does them: "1 can chickpeas, drained and rinsed".
- Give a cut size when it changes cooking (diced 1 cm); use "coarsely" or "finely" only where size does not matter, and use the same term every time.
- One report argues editors disagree over whether to add a whole-item equivalent to every prepared quantity; default: keep one governing quantity and an optional purchasing approximation, and mark which governs.
- In stored data keep prep and measure stage as separate fields, so punctuation is only a rendering choice: `{item, quantity, unit, prep, measured_before_prep}`. A volume converted to grams must use the density of the form that was measured (design).

### 2.3 To taste, optional, divided

| Case                                          | Rule                                                                                                                                                                                                                                                         |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| To taste                                      | Fine for pepper, herbs, final acid or salt adjustment after cooking. Say when to taste (after reducing, after adding salty ingredients). Never "to taste" for structural salt (bread, brine, cure, pasta water) or for leaveners; give a number there        |
| Starting amount                               | For salt in ordinary dishes write "plus more to taste" after a tested starting amount                                                                                                                                                                        |
| Do not taste raw mixtures that must be cooked | Cook a small sample first (raw meat, egg, fish mixtures)                                                                                                                                                                                                     |
| Optional                                      | Mark "(optional)" in the list and "if desired" in the step. Optional means the dish still works without it; an ingredient that changes texture or balance is not optional                                                                                    |
| Divided                                       | List the total once, mark "divided", and state the amount at each use ("2 tbsp for the vegetables, the rest for the sauce"). Store the total and each allocation and check that they add up; do not confuse greasing fat with an amount already in the total |
| Unmeasured amounts                            | Italian "q.b." (quanto basta), Japanese 少々 and ひとつまみ, "a pinch" are approximate by design; give an approximate gram or mL value when exporting to a locale without the idiom, labelled approximate                                                    |

Three reports say "to taste" is overused and a starting amount helps learners; one says some handbooks prefer "season to taste" over "salt the meat" for clarity of action. Default: starting amount plus "to taste" at the point where tasting is safe.

### 2.4 Precision and counted items

- Match precision to sensitivity: 1 g matters for yeast and salt in bread, 5 g for flour is fine, a medium onion needs no grams in a stew.
- Counted items: count plus size plus weight where size matters, for example "2 medium carrots (about 200 g)"; for juice or zest give the yield ("juice of 1 lemon, about 45 mL").
- Exact-looking conversions cannot repair a vague original. Keep vague quantities vague ("1 bunch") unless a controlling amount is available.
- Fractions or decimals: US style prefers fractions (1½), metric locales use decimals with grams (convention). Spell units out or use the locale's standard abbreviation; never T versus t.

## 3. Units and measurement

### 3.1 Weight versus volume

| Fact                                                                                                                                                            | Evidence                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| A cup of flour varies by about 20% with technique; testers differ by about 30 g with identical cups                                                             | moderate: test-kitchen measurements (America's Test Kitchen, Cuisine at Home), not academic trials |
| NIST recommends measuring by mass; using a dry cup for liquids or the reverse is a common error                                                                 | strong: standards body                                                                             |
| There is no single grams-per-cup for flour: one test kitchen uses 120 g (spooned and levelled), another about 142 g (dip and sweep), and some sources 125-140 g | moderate; a conflict between reports, not an error                                                 |

Default (design): baking and anything reproducibility-sensitive is weight-first, with volume in parentheses only if the source gave it; soups, stews and sautés tolerate volume. Small amounts of salt, spices and leaveners stay in spoons because home scales lack resolution. Large batches are weight only.

Conversion hierarchy for volume to weight:

1. The mass the source recipe itself states.
2. The weight table and measuring method of the source's publisher.
3. A named ingredient-and-form-specific reference.
4. An estimate labelled as such.
5. No conversion, when the uncertainty would be consequential.

Record which convention was used ("flour at 120 g per cup") in the notes. Do not replace every flour cup with one gram value: that changes the formula.

### 3.2 Regional unit definitions

| Unit       | US customary                               | US nutrition label | UK / EU / NZ / CA                                              | Australia  | Japan                                                    |
| ---------- | ------------------------------------------ | ------------------ | -------------------------------------------------------------- | ---------- | -------------------------------------------------------- |
| Teaspoon   | about 4.9 mL                               | 5 mL               | 5 mL                                                           | 5 mL       | 小さじ 5 mL                                              |
| Tablespoon | about 14.8 mL                              | 15 mL              | 15 mL                                                          | **20 mL**  | 大さじ 15 mL                                             |
| Cup        | about 236.6 mL (NIST rounds to 237 or 240) | 240 mL             | 250 mL where a metric cup is used; no standard UK culinary cup | **250 mL** | **200 mL** (to verify)                                   |
| Rice cup   | -                                          | -                  | -                                                              | -          | 1 合 (gō) = **180 mL**, the cooker's own cup (to verify) |

- The Australian tablespoon holds a third more than a 15 mL spoon; a 15 mL spoon used for an Australian recipe delivers 25% too little. A Japanese cup is about 15% below a US cup.
- The Japanese 200 mL cup and 180 mL gō come from one report plus manufacturer pages (to verify); the Australian and US values are confirmed by several reports and regulation.
- Canada's food guide uses a 250 mL cup; the UK has moved to grams and mL with 15 mL spoons.
- Fluid ounce (volume, 30 mL on US labels) is not the weight ounce (28 g on US labels); the UK pint (about 568 mL) is not the US pint (about 473 mL). In stored data use mL and g.
- Store the source measurement standard separately from the reader's locale. An Australian recipe shown to a US reader still starts from Australian quantities. If the source locale is unknown, ask or flag; do not infer it from the language.
- Charts sometimes round fractions (one third of a 250 mL cup as 80 mL); treat these as cooking guidance, not identities.

### 3.3 Dual units and rounding

| Rule                          | Detail                                                                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One controlling system        | Choose one per rendered version; the second goes in parentheses, consistently ("225 g (1 cup) butter" for a metric reader, "1 cup (225 g)" for a US reader)         |
| Convert from the stored value | Never from a previously rounded display value, and never round both numbers independently, or the two disagree (250 g next to "2 cups" when the house cup is 120 g) |
| Round by sensitivity and tool | Flour to 5 g, liquids to 5 or 10 mL, yeast and salt to 1 g or kitchen spoons, oven to 5 or 10 °C                                                                    |
| No false precision            | Not 236.59 mL                                                                                                                                                       |
| Label untested conversions    | In the notes section, with the original value                                                                                                                       |

A unit switch in a UI is cleaner than showing grams, ounces, cups and counts on every line; in a saved Markdown file show one controlling unit and at most one parenthetical.

### 3.4 Conversion pitfalls

| Pitfall                          | Handling                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Butter stick                     | US stick = 113 g (½ cup, 8 tbsp); outside the US convert to grams, since blocks are 250 g in much of Europe and Australia                                                                                                                                                                                                                                                                                              |
| Eggs                             | Give grams when eggs are structural (custard, sponge): about 50 g edible, about 57 g in shell for a US large. EU/UK sizes are bands per single egg (medium 53-63 g, large 63-73 g), so a UK large outweighs a US large and an EU medium is the nearer match (to verify). One report says no universal egg table was found; default: say "large (about 50 g without shell)" and do not invent an exact local equivalent |
| Onion, lemon, garlic             | Sizes vary by country; give a prepared weight when reproducibility matters ("1 medium onion, about 150-170 g")                                                                                                                                                                                                                                                                                                         |
| Cans and jars                    | US "15-ounce can" versus European 400 g tins: map to the nearest local package and check sensitivity (beans in a stew, no; condensed milk in fudge, yes). State drained versus net weight                                                                                                                                                                                                                              |
| Packed or loose, chopped, grated | Store the form with the quantity                                                                                                                                                                                                                                                                                                                                                                                       |
| Compressible items               | Leaves, grated cheese: weigh                                                                                                                                                                                                                                                                                                                                                                                           |
| Salt by spoon                    | Crystal type changes weight per spoon; keep the product or the verified mass                                                                                                                                                                                                                                                                                                                                           |
| Handfuls, bunches, knobs         | Intentionally approximate; convert only with a label                                                                                                                                                                                                                                                                                                                                                                   |
| Shopping view                    | The recipe holds the culinary amount; local package sizes belong to the shopping list, and surplus package contents do not enter the recipe                                                                                                                                                                                                                                                                            |

## 4. Writing the method

### 4.1 What the research supports

| Finding                                                                                                                                    | Source type                                                 | Tag                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Directions are read faster when the goal of a stage comes before its actions                                                               | Instructional research (Dixon)                              | moderate, transfers by analogy                                                   |
| Cooks do not read recipes in sequence; they alternate reading and doing, so steps must be short enough to hold in mind                     | Cooking-specific thesis (Buykx), appliance studies (Ganier) | moderate                                                                         |
| Putting each step's quantities inside the step cuts look-ups; an overview of the sub-goals reduces problems and helps plan parallel work   | Buykx thesis                                                | moderate; the quantities-in-steps point comes mainly from one report (to verify) |
| Step photos were liked but did not reduce errors                                                                                           | Buykx thesis                                                | moderate                                                                         |
| Specific instructions help first-time performance; general ones help learning                                                              | Human-factors review                                        | moderate                                                                         |
| Splitting related information across a page adds load (split attention)                                                                    | Cognitive load theory                                       | strong in the lab, inferred for recipes                                          |
| Egg-dish recipes: 92% gave a time, only two gave an end temperature, and an egg bake that looked done had not reached the safe temperature | One study of 226 recipes (to verify)                        | moderate                                                                         |

None of these studies tested the exact rules below. The rules are convention informed by them.

### 4.2 Method-writing rules

| #   | Rule                                                                                                          | Example or note                                                                                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Goal first, then actions                                                                                      | "Make the sauce: melt the butter..." not "Melt the butter... this is your sauce"                                                                                                         |
| 2   | One main objective per step; a tightly linked sequence may share a step, at most two or three coupled actions | "Warm the oil on medium, add the onion, stir now and then until soft, 6-8 minutes" is a single step. Dressing, roast check and garnish are three                                         |
| 3   | Chronological, including invisible tasks                                                                      | Preheat where the heat is needed (early for quick dishes, late after a long rise or marinade); start pasta water, soften butter in time. Do not start the oven hours early               |
| 4   | Time plus a cue                                                                                               | Time range first, then temperature if relevant, then the sensory endpoint: "20-25 minutes, until the centre reads 74 °C and the juices run clear". Tell the cook where to start checking |
| 5   | Heat level plus its effect                                                                                    | "Medium, so the butter foams but does not brown" (section 5.2)                                                                                                                           |
| 6   | Warnings at the point of use                                                                                  | Before the risky action, with the reason when it changes behaviour: "do not let the garlic brown, it turns bitter". Keep them in concise and detailed modes alike                        |
| 7   | Quantities repeated in the step                                                                               | Default: yes (see conflict below). Generate them from the same data as the ingredient list                                                                                               |
| 8   | Use the list name                                                                                             | The same word for the ingredient in list and step; name components ("the dressing", "the cooked lentils") instead of "the mixture"                                                       |
| 9   | Precise verbs                                                                                                 | Describe the technique once instead of an unexplained "fold" or a vague "mix": "stir gently, lifting from the bottom, until no dry flour remains"                                        |
| 10  | Concise                                                                                                       | Say it in the order it happens; cut chatter. Drop empty "set aside" but keep reservations that matter (pasta water, divided items)                                                       |
| 11  | Parallel work is explicit and anchored                                                                        | "While the lentils simmer, make the dressing; have it ready before draining." Add a time or cue so the cook need not search                                                              |
| 12  | Quality cue and safety endpoint are separate                                                                  | Colour or texture judge quality; temperature judges safety. Take safety temperatures from `food-safety.md`, never from colour                                                            |

Conflict, quantities in steps: one report (with a cognitive-load argument) says repeat each step's quantity; another says keep quantities in the list except for divided or tiny critical amounts, to avoid duplication; a third says repeat only if generated from the same data. Default: repeat, because the saved format already gives each step its own ingredients with amounts.

### 4.3 Prep block or integrated prep

| Dish type                                                          | Layout                                                                                                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Fast, high heat (stir-fry, anything without time to chop mid-cook) | Short "Before you start" block: chop, measure, line pans                                                                                                                 |
| Long, slow (braise, stew, soup)                                    | Integrated: chop the carrots while the onions soften                                                                                                                     |
| Short and simple (20-minute pasta)                                 | Integrated; a prep block adds noise                                                                                                                                      |
| Any recipe                                                         | Never move a task earlier if it needs freshness, follows a transformation (cooling, slicing cooked food, reserving liquid made during cooking) or carries a safety order |

No robust evidence shows a separate mise-en-place section is always better; it is a user setting with a default by dish type (design). Treat the method as a dependency graph and headings as views of it.

### 4.4 Warning levels

Three levels, placed at the step where the hazard occurs, with allergens repeated on the ingredient line (design, one report):

| Level   | Use for                                                                                     |
| ------- | ------------------------------------------------------------------------------------------- |
| Danger  | Hot oil, raw dough or batter, pressure cooking, anything that can burn or make the cook ill |
| Caution | Allergens, sharp blades, splatter, hot steam                                                |
| Note    | Technique tip, reason for a step                                                            |

## 5. Heat and equipment

### 5.1 Ovens

| Item                  | Rule                                                                                                                                                                                                                                                                            | Tag                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Fahrenheit to Celsius | C = (F - 32) / 1.8, then round to 5 or 10 °C: 350 °F is printed 180 °C (exact 176.7)                                                                                                                                                                                            | strong, rounding is convention               |
| Oven mode             | Store it with the temperature: conventional (top and bottom), fan, gas. US recipes almost always assume conventional; UK recipes often print both. Never infer fan from Celsius or conventional from Fahrenheit, and keep the unit conversion separate from the mode adaptation | convention, design                           |
| Fan offset, default   | 20 °C lower for metric users, 25 °F lower for US users, and check 5-10 minutes early                                                                                                                                                                                            | convention, widely printed, not standardised |
| Other offsets         | One report cites a national heart-foundation guide that lowers by 10 °C and shortens time by 25% for convection (to verify); one chef's site deviates for a long, low cake bake (115 °C instead of a flat cut). Manufacturer instructions override the rule of thumb            | conflict, default stays 20 °C / 25 °F        |
| Gas marks             | UK chart mapping, not a numeric unit: mark 4 = 180 °C / 350 °F / 160 °C fan; each mark adds 25 °F from mark 1 = 275 °F (about 140 °C)                                                                                                                                           | convention                                   |
| Triple notation       | UK style "200 °C / 180 °C fan / gas 6"; German "Ober-/Unterhitze 200 °C, Umluft 180 °C". Use the locale's form                                                                                                                                                                  | convention                                   |
| Thermostat accuracy   | Home ovens are often off; suggest an oven thermometer for baking                                                                                                                                                                                                                | convention                                   |
| Untested mode change  | Label it and widen the time range with a "check early" cue                                                                                                                                                                                                                      | design                                       |

Do not offer microwave, pressure cooker, air fryer and oven as interchangeable layouts of one recipe; each is a process change.

### 5.2 Stovetop heat

No standard defines low, medium or high across gas, coil, induction and pan types. Pair each level with its observable effect and do not translate "medium" into a dial number or wattage.

| Label        | Pair with                                                                  |
| ------------ | -------------------------------------------------------------------------- |
| Low / gentle | No browning, barely moving surface                                         |
| Medium       | Steady sizzle, onions soften without colour, butter foams without browning |
| High         | Fast boil or hard browning, plus an overheating warning                    |
| Simmer       | Small bubbles breaking now and then                                        |
| Oil ready    | Shimmers, or a test bread cube or water drop sizzles at once               |

### 5.3 Pans

- Baking time follows depth and area. Compare bottom areas at a similar depth: an 8-inch square and a 9-inch round hold about the same (about 64 sq in, one baking source); a 9 x 13 inch recipe fits two 9-inch rounds. A 9-inch round is more than a quarter larger in area than an 8-inch round, so the same batter is thinner and bakes sooner.
- US pans come in inches (9 x 13, 9 x 5 loaf), European ones in cm (a 24-26 cm springform, a 30 cm loaf tin). Pick the closest local size by area, adjust the time range, and say so.
- Dark metal browns faster (check early or lower by about 25 °F); glass heats slowly; cast iron holds heat.
- On the stove a wider pan evaporates and browns faster and a crowded pan steams. Give the size when it matters ("30 cm / 12-inch skillet so the chicken is not crowded").
- Give dimensions and depth, not "a baking dish", for baking, candy, frying and pressure cooking; for a forgiving soup "a large pot" is enough.

### 5.4 Equipment tolerance

Give cues next to numbers; give a time range and a first check point; name what changes with other equipment ("dark pan: check 5 minutes early"); offer an alternative to a single appliance ("hand mixer: beat twice as long"). Prefer "a heavy skillet, ideally cast iron" unless the result truly depends on the material. Verify thermometers in boiling water.

## 6. Scaling

Scale the list by one factor k = wanted yield / original yield, then handle the items below. Scale by weight: convert to grams first, multiply, then convert back to friendly units.

| Item                                        | Starting treatment                                                                                                | Why it may need adjusting                                                                                                                                 | Tag                              |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| Main ingredients, stock, most batter liquid | Linear by mass                                                                                                    | Vessel and oven capacity may no longer fit                                                                                                                | strong                           |
| Eggs                                        | Linear by weight in grams                                                                                         | Cannot use 1.5 eggs; weigh a beaten egg or round and adjust liquid. Never round silently                                                                  | moderate                         |
| Salt in dough, brine, cure                  | Keep the proportion (baker's percentage or brine ratio)                                                           | Structure and safety depend on it                                                                                                                         | strong                           |
| Salt and spices in sauces, stews            | Scale linearly, then season at the end                                                                            | Perception is not linear; reductions concentrate salt                                                                                                     | conflict, see below              |
| Chemical leavening                          | Linear up to about 2x; above that, flag it and consider several pans of the original size instead of one deep one | A deeper product is a process change                                                                                                                      | conflict, see below              |
| Yeast                                       | Keep the formula for the same process                                                                             | Quantity, temperature and proving time interact                                                                                                           | moderate                         |
| Liquid in reductions, braises               | Do not just multiply                                                                                              | Evaporation tracks exposed surface, not volume, so twice the sauce in the same pot takes much longer to thicken                                           | strong, physics                  |
| Cooking time                                | Never multiply by k                                                                                               | Heat travels through thickness; same depth in a bigger pan is about the same time, deeper is much longer; a thicker roast takes disproportionately longer | strong, physics                  |
| Prep time                                   | Re-estimate                                                                                                       | Some tasks repeat per item, others are fixed setup                                                                                                        | design                           |
| Pan                                         | By area, not diameter: for similar round pans d_new = d_old x sqrt(k)                                             | Keeps depth constant                                                                                                                                      | strong, geometry                 |
| Frying oil, greasing fat                    | Set by the pan                                                                                                    | Not part of the formula                                                                                                                                   | moderate                         |
| Garnish, herbs, finishing oil, alcohol      | Often less than linear                                                                                            | Plate balance does not double                                                                                                                             | moderate, one report (to verify) |
| Oven temperature                            | Unchanged unless depth changes a lot                                                                              | Deep cakes sometimes bake lower and longer                                                                                                                | moderate                         |

Conflict, salt and leaveners: one report cites a national guideline that raises salt, spices, leaveners and yeast by 1.5x when doubling, and suggests 1.25-1.5x for salt and spices (test-kitchen convention, to verify); another says online "use 75%" rules have no primary source; a third says ingredients are not exceptions to proportional scaling and that the real question is whether formula, geometry and process stay equivalent. Default: scale linearly, season to taste at the end, check doneness by cue, and warn above about 2x or below one half. Do not apply fixed reduction factors to leaveners or yeast.

Practical rules (design):

1. Up to 2x: formula scaling. From 2x to 4x: batches for frying, baking and reductions. Above 4x: a tested large-batch recipe or separate batches, since mixer, oven and pot become the limit.
2. Recalculate pan suggestions by area; prefer repeating the original pan size.
3. Restate doneness cues in the scaled version and say that times were adjusted, not multiplied.
4. Never label a scaled recipe as tested because the arithmetic is right.
5. Preserve and canning recipes are not scaled; keep the validated procedure.

## 7. Language and locale

Keep language, country, source measurement standard, destination preference, terminology, grammatical style, ingredient market, equipment assumptions and food-safety jurisdiction as separate fields (design). An English recipe is not necessarily American, and a German translation does not make the quantities German. Localise by adaptation, not word-for-word translation: keep the dish's function, texture and safety; change names, units, packages and equipment to the market.

### 7.1 Per-locale conventions

Generate the target text from a structured action (verb, ingredient, tool, cue) and realise it in the locale's usual mood. Choose one mood per language and keep it throughout; let the user pick formality where the language has it.

| Locale               | Instruction mood                                                                                                                                                                                                                                              | Headings (ingredients / method)                                                  | Ingredient and quantity notes                                                                                                                                       | Tag                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| English (US)         | Imperative                                                                                                                                                                                                                                                    | Ingredients / Directions (or Instructions)                                       | Cups and spoons, Fahrenheit, conventional oven assumed, fractions; "biscuit" is a scone-like bread                                                                  | convention                         |
| English (UK, AU, NZ) | Imperative                                                                                                                                                                                                                                                    | Ingredients / Method                                                             | Grams and mL, 15 mL spoon (AU: 20 mL), fan and gas notation; "biscuit" is a cookie                                                                                  | convention                         |
| German               | Infinitive ("Zwiebel fein hacken") is the dominant cookbook form; formal "Sie" imperative and informal "du" imperative also occur, mostly online. Default: infinitive, with du imperative when the user wants a personal tone and never mixed within a recipe | Zutaten / Zubereitung (Hinweise for notes); prep and cook times often separate   | EL / TL for spoons, decimal comma, Ober-/Unterhitze and Umluft, packages of 250 g butter, Schlagsahne about 30% fat                                                 | convention                         |
| French               | Infinitive ("Hacher finement l'oignon") or vous imperative ("Hachez..."); both standard, one language authority advises consistency; print and packaging lean infinitive, web and magazines lean vous imperative. Default: infinitive                         | Ingrédients / Préparation (often with Temps de préparation and Temps de cuisson) | c. à s. / c. à c. for spoons; "Préparation" can cover the whole procedure, so map by function; crème fraîche, crème liquide and crème entière are distinct products | convention                         |
| Italian              | Imperative (tu or voi), infinitive, or impersonal "si"; default: imperative tu or the infinitive, kept consistent (to verify)                                                                                                                                 | Ingredienti / Procedimento (or Preparazione)                                     | "q.b." for unmeasured items; cucchiaio versus cucchiaino is abbreviated Cs/cc and easily confused, so write the words; flour types 00 and 0                         | convention, one report (to verify) |
| Spanish              | Imperative (tú or usted), infinitive, or impersonal "se" ("Se baten los huevos") depending on country and publisher; default: tú imperative, switch to infinitive for a formal or print tone. Reports disagree on which form dominates (see Evidence notes)   | Ingredientes / Preparación (or Elaboración)                                      | Treat a "tú / usted" choice as a user setting                                                                                                                       | convention, weakly sourced         |
| Japanese             | Plain or polite verb endings, or nominal step lists; default: polite form (です・ます) for prose, plain nominal for numbered steps (to verify)                                                                                                                | 材料 / 作り方                                                                    | 大さじ (15 mL), 小さじ (5 mL), カップ (200 mL), 合 (180 mL); 少々 and ひとつまみ for tiny amounts; counters and package sizes differ                                | one report (to verify)             |

Spanish and Japanese rest on the thinnest evidence; German, French and English on the strongest.

### 7.2 Ingredient naming

Classify each localisation as a naming change (same thing, regional name), a product-equivalence mapping (similar category, check the properties), or a substitution (needs culinary validation). Model dairy by fat percentage and behaviour (whipping, curdling, culturing), not by name.

| Area                          | Notes                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cream                         | UK single 18%, whipping 35%, double 48% (regulation); US heavy at least 36%, light whipping 30-36%; so US heavy is close to UK whipping, not double (all single-source figures: to verify). Half-and-half has no exact UK equivalent. Sour cream, crème fraîche, quark, fromage blanc, ricotta, cottage cheese and Greek yogurt overlap but change moisture, acidity and heat stability |
| Flour                         | US all-purpose is roughly UK plain, German Type 405 or 550, French T45 or T55, Italian 00 or 0, but protein differs (to verify); self-raising contains leavener                                                                                                                                                                                                                         |
| English vocabulary            | UK/AU versus US pairs such as aubergine and eggplant, courgette and zucchini, coriander leaf and cilantro, rocket and arugula, icing and powdered sugar, caster and superfine sugar, bicarbonate of soda and baking soda, cornflour and cornstarch, prawns and shrimp, capsicum and bell pepper, mince and ground meat                                                                  |
| False friends                 | "Biscuit", "pudding", "entrée" (main course in the US, starter in French), German "Paprika" (spice and pepper), French "crème"                                                                                                                                                                                                                                                          |
| Chilli, paprika, curry powder | Heat and composition vary by country; say what is meant                                                                                                                                                                                                                                                                                                                                 |
| Vague quantities              | "A knob", "a glug", "a pinch" do not translate; convert to an approximate amount and label it                                                                                                                                                                                                                                                                                           |

### 7.3 Translation pitfalls

1. "Cup" translated as a drinking cup (Tasse, tasse, tazza) without converting the volume.
2. Units translated without their regional definition (Australian spoon, Japanese cup, gō).
3. Product names rendered literally ("double cream" as "doppelte Sahne") when a nearby local product plus a remark would serve the cook.
4. Oven mode lost (fan or Umluft dropped).
5. Technique words with no equivalent (fold, cream butter and sugar, unterheben, monter): describe the action briefly when unsure.
6. Locale formatting: decimal comma, unit abbreviations, EL / TL, c. à s., temperature symbol.
7. Packages and food-safety jurisdiction left at the source's values.

## 8. Restructuring existing recipes

### 8.1 Risk table

| Change                                                                      | Risk                                                    | Required treatment                                                                                                       |
| --------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Reorder list, group by component                                            | None if order of use is kept                            | Free                                                                                                                     |
| Rewrite steps in the house voice, split or merge steps, add a prep block    | Low                                                     | Free; keep every warning, cue, temperature and reserved item                                                             |
| Translate prose and headings                                                | Low to medium                                           | Locale glossary; watch technique terms and mood                                                                          |
| Move prep notes into steps                                                  | Low to medium                                           | Check nothing is duplicated or dropped and the measure stage is preserved                                                |
| Convert within a system (tbsp to tsp, g to kg)                              | Low                                                     | Free                                                                                                                     |
| Convert volume to weight                                                    | Medium to high                                          | Ingredient-and-form density, state the source convention (section 3.1), keep the original in notes                       |
| Convert regional units (AU spoon, JP cup, gō)                               | Medium                                                  | Detect the source locale first; a wrong guess is 25% (AU spoon) or 15% (JP cup)                                          |
| Change oven mode or pan                                                     | Medium                                                  | Section 5, widen the time range, add a "check early" cue, label untested                                                 |
| Substitute an ingredient                                                    | High                                                    | Label as substitution, say what changes (fat, protein, acidity, water), keep the original in notes                       |
| Scale                                                                       | High for baking, reductions and anything with leavening | Section 6, warn, recompute pan and times                                                                                 |
| Change a safety-critical step (undercooking, cooling, raw dough, allergens) | High                                                    | Do not change; take rules from `food-safety.md`; verify every allergen and cross-contact statement                       |
| High altitude                                                               | Medium to high                                          | Leavening, boiling point and evaporation shift; baking, canning, candy and pressure cooking need adjustment or a warning |

Changing presentation is editing; changing quantities or ingredients is developing a new recipe, which a test kitchen would retest. The plugin cannot retest, so it (a) prefers documented conversions, (b) rounds without drift, (c) flags uncertain conversions to the user, and (d) keeps the original values in the notes section. "Free" means low culinary risk after checking meaning, not "no review".

### 8.2 Safe rework workflow (design)

1. Keep the source text and provenance separate from the rendered recipe.
2. Extract ingredients, quantities, prep states, equipment, times, temperatures and cues; flag ambiguity instead of resolving it silently.
3. Build ingredient allocations per step and the dependency order.
4. Apply the requested locale and style.
5. Classify every change as presentational, interpretive or culinary.
6. Reconcile: every ingredient used, allocations add up, list matches steps, optional items still optional, warnings kept.
7. Record the version's testing status with one of: reformatted with quantities unchanged; units converted and not retested; adapted with substitutions and not retested; tested in the stated locale and equipment.

### 8.3 What is and is not free to copy

| Layer                                                                                          | Position (US-focused, not legal advice)                                                                                                  |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Bare ingredient list and simple directions                                                     | Not protected; facts and function                                                                                                        |
| Headnote, distinctive method prose, personal story, photos, cookbook selection and arrangement | Protected expression; courts have left room for protection where a recipe carries real commentary                                        |
| Other jurisdictions                                                                            | Rules differ (for example German protection turns on personal intellectual creation); do not turn the US rule into a worldwide clearance |

Plugin rule: rewrite the method in neutral own wording, drop the source headnote rather than paraphrase it closely, do not reproduce photos, and never present verbatim reproduction as acceptable anywhere. Attribution does not replace permission. The folk rule "change three ingredients and it is yours" has no legal basis (all reports that mention it agree); do not encode it.

### 8.4 Attribution tiers

| Tier                              | Use when                                                                                                  | Example line                                                                                                                  |
| --------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| From / reproduced with permission | Authorised reproduction                                                                                   | "From [Author], [Title]"                                                                                                      |
| Adapted from                      | The result resembles the source closely; most recipes taken from others, since nearly all change slightly | "Adapted from [Author], [Title], [Book or URL]. Quantities kept; prep separated from cooking; units converted, not retested." |
| Based on a recipe from            | Larger changes                                                                                            | "Based on a recipe from [Author]"                                                                                             |
| Inspired by                       | The source only supplied an idea or flavour pairing, with substantial rework                              | "Inspired by [Title]"                                                                                                         |
| Own recipe                        | Unrecognisable from any source                                                                            | No attribution needed; link to a source if one exists                                                                         |

Default: keep attribution metadata on every restructured recipe, state what changed, and never strip it to look original. For a recipe the plugin invents, no attribution is needed, but a named tradition (see `culinary-craft.md`) may be cited as the model. Provenance fields: source, author, URL or bibliography, date accessed, permission status, change log.

Conflict, which outlet defined the tiers: one report credits a national newspaper's food desk, another a West-Coast paper's test kitchen. The three-tier wording is the same. Default: use the tiers without naming an outlet. A chef-blogger's tiers (adapted when it resembles the original, inspired when substantially reworked) agree (single report, to verify).

## 9. Readability and accessibility

### 9.1 Beginner and experienced readers

| Information                                  | Beginner view                          | Experienced view            |
| -------------------------------------------- | -------------------------------------- | --------------------------- |
| Technique                                    | Short explanation inline or expandable | Familiar term only          |
| Preparation                                  | Explicit size, order, readiness checks | Concise specifications      |
| Timing                                       | Clear dependencies and order           | Compact scheduling cues     |
| Doneness                                     | Concrete observations                  | Same endpoints, fewer words |
| Safety, temperatures, ingredient allocations | Fully visible                          | Fully visible               |

Layers (design): (1) the core recipe, everything needed to cook correctly and safely, (2) expandable technique help, (3) background such as science, history and variations. Required temperatures, allocations and warnings never live inside the optional layers. Add an overview line for multi-stage dishes ("three stages: dough with 1 h chilling, filling, assembly and bake"). Explain the "why" only at decision points. Skill-level presets ("concise", "guided") must carry the same quantities, temperatures, warnings and doneness tests. Research on expertise reversal supports adaptable detail, not always giving experts the shortest text.

### 9.2 Accessibility checklist (design, not a compliance claim)

- Numbered steps, real headings, short paragraphs; a linear reading order.
- Never colour alone for doneness or warnings; add texture, sound, smell, temperature.
- Essential information in text, not only in images or icons; text explanation for technique photos.
- Consistent units, spelled out or standard; make fractions readable aloud.
- No ambiguous pronouns when several ingredients are in play.
- Meaningful timer names; the current step and its ingredients easy to retrieve.

### 9.3 Checks before saving or exporting

| Check                     | Pass condition                                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ingredient and step match | Every listed item is used and every step item is listed                                                                                           |
| Divided items             | Allocations add up to the total                                                                                                                   |
| Units                     | One controlling system, converted from stored values, original in notes                                                                           |
| Mood and terms            | One grammatical mood, one name per ingredient                                                                                                     |
| Oven                      | Mode, unit and conversion shown                                                                                                                   |
| Warnings and cues         | Present at the step, each timed step has a cue                                                                                                    |
| Attribution and status    | Source line and testing status present                                                                                                            |
| Reading test              | A cook from the target locale can find missing information, odd terms or unrealistic times (human check; the plugin only does the automated ones) |

## 10. Evidence notes

| Topic                          | Strength and caveats                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Editorial conventions          | Order of use, grouping, headnotes, yield phrasing and prep-note placement come from publishing handbooks, institutional style guides and professional editors; broadly agreed, not experimentally tested                                                                                                                                                                            |
| Weight versus volume           | Test-kitchen measurements and a standards body, no controlled academic study; the grams-per-cup spread between kitchens is a genuine disagreement, not an error                                                                                                                                                                                                                     |
| Regional units                 | US, Australian and metric values confirmed by regulation or several reports; Japanese cup and gō come from one report plus manufacturer pages (to verify)                                                                                                                                                                                                                           |
| Method research                | Procedural-instruction studies (Dixon, Ganier, Buykx, Chandler and Sweller) are mostly about devices and software; the recipe-specific work is one thesis and a few workshop papers. The rules are consistent with them, not proven by them                                                                                                                                         |
| Quantities in steps            | Backed by the Buykx thesis and the split-attention argument; one report advises keeping quantities in the list; default repeats                                                                                                                                                                                                                                                     |
| Oven offsets                   | 20 °C / 25 °F is a rule of thumb printed by several sources; the 10 °C and 25% time variant is single-source (to verify); no standard exists                                                                                                                                                                                                                                        |
| Scaling factors                | Physics of evaporation and heat penetration is firm; percentages for salt and leavening lack primary sources, and reports disagree (see section 6)                                                                                                                                                                                                                                  |
| Eggs, cream, flour equivalents | Per-egg EU and per-dozen US grades, cream fat percentages and flour-type pairings come from one report each (to verify)                                                                                                                                                                                                                                                             |
| Language conventions           | German, French and English are well sourced; one French authority supports both moods; Italian and Japanese are single-report (to verify); reports disagree on the Spanish default (imperative, infinitive or impersonal "se")                                                                                                                                                      |
| Attribution                    | The three-tier practice is described the same way by two reports but credited to different outlets; the "three changes" rule is a myth in every report that mentions it                                                                                                                                                                                                             |
| Copyright                      | US position only, from the Copyright Office and case law; not legal advice; other jurisdictions differ                                                                                                                                                                                                                                                                              |
| Safety temperatures            | Only referred to here; the authoritative values live in `food-safety.md`                                                                                                                                                                                                                                                                                                            |
| Egg-recipe study               | 226 egg dishes, 92% gave a time, two gave a temperature: single report (to verify)                                                                                                                                                                                                                                                                                                  |
| Accessibility                  | Product-design recommendations, not tested findings                                                                                                                                                                                                                                                                                                                                 |
| Coverage                       | Four reports merged: Claude, Copilot, DeepSeek, Perplexity. Copilot is short and mostly agrees on structure; it contributes the dual-unit examples and a general locale outline. DeepSeek adds the headnote and active-time debate, the 1.5x scaling cue and the three warning levels; Perplexity adds the conversion hierarchy, version status labels and the pan-diameter formula |
