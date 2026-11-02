# Writing and Restructuring Recipes for a Multilingual AI Cooking Assistant

## Scope, evidence standard, and how to read this report

Recipe writing is a hybrid craft: part technical documentation, part food science, part editorial convention. Some recommendations are backed by measurement standards, food-safety authorities, or instructional-design research. Many others are house conventions that vary by publisher, test kitchen, and country. This report labels each major recommendation accordingly:

- **Evidence-based** — supported by metrology standards, food-safety guidance, experimental research, or explicit regulatory/technical documentation.
- **Test-kitchen convention** — established practice in professional test kitchens and publisher style guides; widely used but not experimentally validated in every detail.
- **Editorial convention** — a house-style choice that varies across publications and markets; consistency matters more than the specific choice.

A well-designed AI cooking assistant should encode conventions as defaults but expose them as configurable “house style” parameters, because recipe writing has legitimate disagreements rather than one universal standard.

---

## 1. Anatomy of a well-written recipe

### 1.1 Standard components and their purposes

| Component               | Purpose                                                                  | Typical conventions                                                                                                                                        | Evidence status                                                                                            |
| ----------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Title**               | Identify the dish and make it searchable                                 | Name by main ingredient, cooking process, or commonly known name; put the largest-quantity ingredient first when possible (e.g., “Broccoli Beef Stir-Fry”) | Editorial convention; Virginia Cooperative Extension gives this guidance                                   |
| **Headnote**            | Context, technique rationale, substitutions, serving ideas, author voice | 1–3 short paragraphs; utility-first in instructional contexts; longer narrative in cookbooks                                                               | Editorial convention; experts disagree strongly on length and necessity                                    |
| **Yield/servings**      | Tell the cook how much the recipe makes and what a portion is            | Give both number of servings and portion size; for baked goods, give pan dimensions and count                                                              | Test-kitchen convention; USDA standardized-recipe practice distinguishes yield and portion size            |
| **Time**                | Help the cook plan                                                       | Separate prep, cook, and total time; ideally distinguish active from hands-off time                                                                        | Editorial convention; definitions vary and are not standardized                                            |
| **Equipment**           | Ensure the cook has the right tools and pan sizes                        | List only non-obvious or outcome-critical equipment; give pan dimensions where size matters                                                                | Editorial convention; some guides require a separate equipment list, others integrate equipment into steps |
| **Ingredient list**     | Shopping list and prep list                                              | Order of use, grouped by component when necessary, with prep notes                                                                                         | Test-kitchen convention; see Section 2                                                                     |
| **Method**              | Reproduce the dish reliably                                              | Numbered steps, one main action per step, sensory cues, times and temperatures                                                                             | Evidence-informed convention; see Section 4                                                                |
| **Notes**               | Make-ahead, storage, variations, substitutions, technique                | Separate from the main method so it does not interrupt flow                                                                                                | Editorial convention                                                                                       |
| **Serving suggestions** | Help the cook complete the meal                                          | Sides, drinks, garnishes, leftovers                                                                                                                        | Editorial convention                                                                                       |

The standard components are well established in recipe-writing handbooks. Ostmann and Baker’s _The Recipe Writer’s Handbook_ treats the headnote, title, ingredient list, method, yield, notes, and variations as standard components of recipe style. America’s Test Kitchen similarly describes the “basic anatomy” of a published recipe as headnote, ingredient list, and steps, produced under publisher style guides.

### 1.2 Where experts disagree

**Headnotes.** America’s Test Kitchen argues that the headnote contains vital information not found elsewhere — ingredient selection, substitutions, and technique tips — and should not be skipped. Food52 frames headnotes as a trust and voice device: “The best headnotes not only give you a sense of the recipe and why this particular recipe is noteworthy or challenging or different from all the rest,” but also show why the author should be trusted. The Kitchn, by contrast, notes that many readers skip headnotes and prefer the recipe itself; it treats headnotes as optional context rather than essential instruction.

**Recommendation for an AI assistant:** use a short “utility headnote” by default — 50–120 words covering provenance, key technique, substitutions, and serving — and place longer narrative or personal material behind an optional “story” field. This satisfies both camps without forcing narrative on users who want to cook.

**Active time.** There is no universal definition. Southern Living explicitly notes that publications use “active time,” “inactive time,” “prep time,” and “total time” differently; active time is supposed to mean time physically in the kitchen, but occasional stirring is still active because the cook cannot leave. The result is that active-time labels are subjective and often inaccurate across publishers.

**Recommendation:** never rely on a single “active time” label. Store prep time, cook time, hands-off time, and total time separately, and display them with explicit definitions.

**Separate equipment list.** Virginia Cooperative Extension recommends a separate equipment section listing general tools and pan sizes. Other publishers integrate equipment into the method at the point of use, arguing that a separate list adds length and encourages readers to skip it. A practical compromise is to list only “non-obvious equipment” separately — springform pan, blender, instant-read thermometer, steamer — and mention ordinary tools such as bowls and knives in the step where they are used.

---

## 2. The ingredient list

### 2.1 Order and grouping

The dominant English-language convention is **order of use**: list ingredients in the order they appear in the method. Dianne Jacob calls ingredients out of order “by far the biggest error” in recipe writing: “If the first thing you’ll do is sauté the onions, don’t list the steak first, even if it’s the star of the recipe”. Virginia Cooperative Extension gives the same rule and adds that when several ingredients are added at the same time, list them from largest to smallest quantity, or alphabetically if the quantities are equal. McCormick’s test kitchen also instructs recipe writers to list ingredients “in order of their use” and always give a quantity.

When a recipe has distinct components — a marinade, sauce, filling, topping, or dough — group by component with subheads such as “For the marinade” or “For the sauce.” Jacob recommends subheads to separate amounts when the same ingredient is used in different components: for example, vinegar in both a marinade and a dressing should be listed under separate subheads with the appropriate amount for each. McCormick’s example recipe uses numbered component groups: “Citrus, chilli and garlic blend,” “Vinaigrette,” and “Tuna”.

There is a minor convention conflict: some publishers list “most important” ingredients first if this is consistent with order of use, and some list ingredients as one would buy them in a supermarket. The Chicago Tribune’s recipe guidance says ingredients are listed in “the logical order of use” and, whenever possible, “as you would buy them in the supermarket”. These goals can conflict. For an AI assistant, **order of use should win** when the two conflict, because it reduces cross-referencing during cooking.

### 2.2 Precision and prep notes

A precise ingredient line should answer four questions:

1. **What** is the ingredient, with enough specificity to shop for it?
2. **How much**, by weight, volume, or count?
3. **What form** should it be in — whole, diced, melted, room temperature?
4. **When** is it used, if the ingredient is divided?

The placement of prep notes matters. America’s Test Kitchen explains that comma placement changes meaning: “1 teaspoon peppercorns, ground coarse” means measure whole peppercorns and then grind them, whereas “1 teaspoon ground peppercorns” means measure the already-ground spice. The same logic applies to produce: **“1 onion, finely chopped”** means take one onion, then chop it; **“1 cup finely chopped onion”** means chop onion until you have one measured cup. Those are not equivalent, because a whole onion of a given size may yield more or less than a cup after chopping. McCormick similarly says all preparation descriptors should be listed after the ingredient itself: “4 carrots, washed and diced”.

**Recommendation:** use the comma form for whole-item ingredients with prep, and use the “measured form + adjective” form only when the cook must measure after preparation. For an AI system, store the ingredient as structured data: `{ingredient: onion, quantity: 1, unit: count, prep: finely chopped, measure_stage: before_prep}`. This makes the distinction machine-readable and translatable.

### 2.3 “Divided,” “to taste,” and “optional”

**Divided ingredients.** When an ingredient is used at more than one point, the common convention is to list the total amount once with “divided” and then specify the portion in each step: “2 cups all-purpose flour, divided.” Jacob argues that “divided” is imprecise and advises giving the first amount in the method and then saying “add the remaining ¼ cup” when the rest is used. America’s Test Kitchen treats “divided” as a keyword that signals the ingredient is used more than once, possibly in different ways.

**Recommendation:** use both. List the total with “divided” so the shopping list is correct, and give explicit sub-amounts in the method steps. Do not rely on “divided” alone.

**“To taste.”** This is one of the clearest expert disagreements. Some handbooks prefer “season to taste with salt and pepper” over “salt and pepper the meat” because the latter uses a noun as a verb and obscures the action. Others argue that “to taste” is overused and that writers should give a specific starting amount, especially for salt, so the cook can learn rather than guess. Saveur’s recipe-writing guidance says the author provides specific salt and pepper measurements instead of instructing readers to season “to taste,” “so you can learn how much to actually use”.

**Recommendation:** give a specific starting amount for salt in doughs, brines, cured foods, and baking, where salt affects structure and safety. Use “to taste” only at the end of cooking, when the cook can safely taste and adjust. For pepper and fresh herbs, “to taste” is acceptable. The AI should distinguish **critical salt** (bread, sausage, brine) from **finishing salt** (soup, salad).

**Optional ingredients.** The common convention is to place optional ingredients last in the list with “(optional)” and to say “if desired” in the method. Virginia Cooperative Extension recommends exactly this: “1/2 teaspoon dried oregano (optional)”. Food Hero’s style guide similarly says to mark “(optional)” in the ingredient list and “if desired” in the directions.

### 2.4 Ingredients used in several steps

Use component subheads when the same ingredient appears in multiple components, and use “divided” plus explicit sub-amounts when the ingredient is used in multiple steps within one component. Jacob gives the steak-salad example: vinegar in the marinade and vinegar in the dressing should be separated under “Marinade” and “Dressing” rather than listed as one ambiguous “½ cup vinegar, divided”.

Water is a special case. Some editors treat “water” as an ingredient only when it is critical to the ratio — bread dough, rice, brine, stock — and otherwise mention it only in the method. Others list all water. For an AI assistant, list water when the amount affects the outcome; otherwise mention it in the step. This is an editorial convention, not a safety rule.

---

## 3. Units and measurement

### 3.1 Weight versus volume: what the evidence says

**Evidence-based.** NIST’s Office of Weights and Measures states that measuring ingredients by mass using a kitchen scale is a best practice for improving recipe accuracy, rather than measuring by volume using fluid or dry measuring cups. NIST also warns that using a dry measuring cup for liquids, or a liquid cup for dry ingredients, is a common source of measurement error.

The practical size of the error is large for flour. King Arthur Baking’s ingredient weight chart uses **120 g per cup of all-purpose flour**. Other reputable sources use 125 g, 130 g, or 140 g per cup, depending on brand and measuring method. A difference between 120 g and 140 g per cup is about 17% — enough to change the texture and rise of cakes, cookies, and breads. King Arthur explicitly recommends weighing for best results and notes that volume measurement depends on technique.

**Recommendation for baking:** give weight first, volume in parentheses, and state the assumed cup weight if volume is the primary unit. For example: “250 g (2 cups) all-purpose flour” or “2 cups (250 g) all-purpose flour, spooned and leveled.” Do not give volume alone for flour, sugar, cocoa, or leavening in baking recipes.

For cooking — soups, stews, sautés — volume is often sufficient because small errors do not compound. The AI should switch precision modes based on recipe type: **baking mode** (weight-first, gram precision), **cooking mode** (volume acceptable, taste-and-adjust cues), and **large-batch mode** (weight mandatory).

### 3.2 Regional units and their differences

| Unit                 | US customary                                         | Metric / UK / Canada              | Australia                  | Notes                                                                                                            |
| -------------------- | ---------------------------------------------------- | --------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Cup                  | 236.6 mL (US customary); 240 mL (US legal/nutrition) | 250 mL metric cup                 | 250 mL                     | NIST uses 240 mL as the approximate 1-cup equivalent for home cooking; Canada’s food guide uses 250 mL           |
| Tablespoon           | 15 mL                                                | 15 mL (UK, Canada, NZ)            | **20 mL**                  | Australia is the main exception; a US/UK tablespoon is 15 mL, an Australian tablespoon is 20 mL                  |
| Teaspoon             | 5 mL                                                 | 5 mL                              | 5 mL                       | Generally consistent                                                                                             |
| Fluid ounce vs ounce | 1 fl oz volume ≠ 1 oz weight                         | 1 mL volume vs 1 g weight         | Same distinction           | NIST explicitly warns that US customary has both fluid ounces and avoirdupois ounces, unlike metric volume units |
| Oven temperature     | Fahrenheit, conventional                             | Celsius, often fan/gas mark in UK | Celsius, fan-forced common | See Section 5                                                                                                    |

A US cup is about 236.6 mL, while a metric cup is 250 mL; the difference is about 5.7% per cup. For four cups of liquid, that is nearly 60 mL extra if a US recipe is made with a metric cup. An Australian tablespoon is 20 mL versus 15 mL in the US and UK — a 33% difference — which matters for salt, baking powder, and strong spices.

### 3.3 Presenting dual units

There is no single international standard for dual-unit presentation, but three patterns are common:

1. **Metric-first with imperial in parentheses** — common in Canada: “250 mL (1 cup),” “15 mL (1 Tbsp)”.
2. **Imperial-first with metric in parentheses** — common in US cookbooks that serve metric users: “1 cup (120 g) all-purpose flour.”
3. **Oven triple format** — common in UK recipes: “220°C/200°C fan/gas 7”.

**Recommendation:** choose one “source of truth” unit per ingredient and derive the other by conversion, then round to a sensible kitchen increment. Do not independently round both values, or the two measurements will disagree. For example, if the source is 250 g flour, do not write “250 g (2 cups)” if your house cup weight is 120 g, because 2 cups would be 240 g. Write “250 g (2 cups plus 1 tablespoon)” or use a consistent 125 g cup standard. State the assumed conversion in the recipe notes or house style.

NIST advises that the safest way to convert a traditional American recipe is to measure the ingredient with a traditional tool, then weigh the result in grams with a kitchen scale. For an AI system, this means conversion should be ingredient-specific, not a generic volume-to-weight multiplier.

### 3.4 Common conversion pitfalls

| Pitfall                                  | Why it matters                                                                      | Better practice                                                                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Flour by volume**                      | 1 cup can weigh 120–150 g depending on flour type, humidity, sifting, and scooping  | Give grams; if volume is given, state “spooned and leveled” and the assumed gram weight                     |
| **“A stick of butter”**                  | A US stick is 113 g = ½ cup = 8 tbsp; butter packaging differs elsewhere            | Write “113 g (½ cup/1 stick) unsalted butter” or “115 g butter”                                             |
| **Egg size**                             | “Large” eggs differ by country; US large is about 50 g shelled, about 57 g in shell | Give egg weight when eggs are a major structural ingredient; otherwise specify “large (about 50 g shelled)” |
| **Onion size**                           | “Medium onion” ranges from about 150 g to 225 g across sources                      | Give weight: “1 medium onion (150–170 g), finely chopped”                                                   |
| **Can sizes**                            | Evaporated milk, tomatoes, coconut milk, and beans vary by market and brand         | Give drained weight and volume, not just “1 can”; state the exact can size used in testing                  |
| **Fluid ounce vs weight ounce**          | A fluid ounce measures volume; an ounce measures weight                             | Use mL for liquids and g for solids; avoid “oz” without clarification                                       |
| **Cup of leafy greens vs cup of liquid** | The same volume weighs very different amounts and packs differently                 | Give weight for leaves, grated cheese, and other compressible ingredients                                   |

For counted items, the best practice is **count + weight or volume**: “2 large eggs (about 100 g shelled),” “1 medium onion (150–170 g), finely chopped,” “2 sticks butter (226 g).” This is a test-kitchen convention rather than a legal standard, but it resolves the ambiguity that causes most conversion failures.

---

## 4. Writing the method

### 4.1 One main action per step

The strongest instructional-design recommendation is to keep each step focused on one main action, or a small cluster of actions that must be performed together. Cognitive load theory holds that working memory is limited, and instructional formats that force the learner to hold and integrate too many elements increase extraneous load. The split-attention effect shows that when interdependent information is separated — for example, a step that refers to an ingredient far away in the list — performance and learning suffer. Dixon’s use-order principle similarly finds that procedural instructions are easier to execute when the order of presentation matches the order of action and when action information precedes condition information.

**Recommendation:** one main action per numbered step, with a maximum of two closely coupled actions (“Whisk the eggs and sugar until pale” is one coherent action; “Chop the onion, heat the oil, and brown the meat” is three). A recent instructional-design review argues that single-action segmentation reduces cognitive load, although direct experimental evidence in real recipe contexts is limited. Label this **evidence-informed test-kitchen convention**, not a proven law of recipe writing.

### 4.2 Separating preparation from cooking

Professional kitchens use **mise en place**: gather and prepare all ingredients and equipment before applying heat. America’s Test Kitchen treats the ingredient list as both a shopping list and a prep list: at a glance, the cook should know what to buy and what to do before starting. BBC Good Food’s recipe-writing guidance says the method and ingredient list should correlate so the recipe is as easy to follow as possible, and ingredients should be listed in the order they appear in the method.

**Recommendation:** provide a short “Before you start” or “Prep” section for recipes with significant knife work, marinating, or component assembly, then a “Cook” section. Do not force this structure on simple recipes; for a 20-minute pasta, prep notes inside the steps are less disruptive.

### 4.3 Parallel tasks and timing

Parallel tasks — “While the onions caramelize, bring the pasta water to a boil” — are useful but easy to misuse. A “meanwhile” with no time anchor forces the cook to search the recipe. Better practice is to anchor parallel tasks to a sensory or time cue: “While the onions cook, start the pasta water; it should come to a boil by the time the onions are golden, about 12 minutes.”

This is an **editorial convention** rather than a research finding. It follows from the broader principle of reducing cross-references and working-memory burden.

### 4.4 Sensory cues alongside times and temperatures

Times alone are unreliable because ovens, pans, burners, ingredient temperatures, and produce sizes vary. Temperatures alone are precise for safety but not sufficient for texture and browning. The strongest recipes combine:

- **Time range**: “20–25 minutes”
- **Temperature**: “until the center registers 165°F/74°C”
- **Sensory cue**: “until the juices run clear and the skin is golden”
- **Visual/tactile/aroma cue**: “until the onions are soft and translucent, not browned”

For safety, USDA FSIS gives specific minimum internal temperatures: beef, pork, veal, and lamb steaks and roasts 145°F/63°C with a 3-minute rest; ground meats 160°F/71°C; all poultry 165°F/74°C. These should be written at the point where they matter, not buried in a note.

**Recommendation:** put the time range first, then the temperature, then the sensory cue. For example: “Roast for 20–25 minutes, until the center registers 165°F/74°C and the juices run clear.” This order lets the cook choose the tool they have — timer, thermometer, or senses — without reading the step twice.

### 4.5 Warnings at the point of use

Safety warnings should appear immediately before the risky action, in bold or as a callout, not in a general note at the bottom. Deep-frying oil can exceed 400°F, and USDA FSIS advises extreme caution to prevent burns and fires. Raw dough and batter can contain pathogens from raw flour and eggs; the FDA advises against eating uncooked dough or batter. Allergen warnings should be attached to the ingredient, not buried in a headnote.

**Recommendation:** a warning system with three levels: **Danger** (hot oil, raw dough, pressure cooking), **Caution** (allergens, sharp blades, splatter), and **Note** (technique tip). Place the warning at the step where the hazard occurs, and repeat critical allergen information in the ingredient list.

---

## 5. Heat and equipment

### 5.1 Oven conventions: conventional, fan, gas, Fahrenheit, Celsius

Oven temperature is one of the largest sources of recipe failure because the same dial setting means different things in different countries and appliance types.

- **Conventional oven** — heat comes from elements without a fan. US recipes generally assume conventional baking unless stated otherwise.
- **Fan/convection oven** — a fan circulates hot air, so the same dial setting cooks faster and browns more. The common conversion is to lower the temperature by about **20°C / 25°F** and check earlier. America’s Test Kitchen has tested convection adjustments and recommends a 25°F reduction for many baked goods.
- **Gas mark** — a UK scale. Gas mark 4 is conventionally 180°C / 350°F / 160°C fan.
- **UK triple format** — “220°C/200°C fan/gas 7” is standard in BBC Good Food recipes.

There is no single exact conversion. Heart Foundation New Zealand’s adaptation guidance, for example, suggests reducing oven temperature by 10°C and cooking time by 25% for convection, which differs from the more common 20°C rule. The difference reflects appliance variation and the fact that fan effectiveness varies by manufacturer.

**Recommendation:** store oven temperature as a structured object: `{conventional_c: 180, fan_c: 160, gas_mark: 4, fahrenheit: 350}` and display the format appropriate to the user’s locale. In US-style recipes, state “conventional oven” explicitly and add a fan note. In UK-style recipes, use the triple format. Do not assume the fan conversion is exact; add “check 5–10 minutes early” for baked goods.

### 5.2 Stovetop heat levels

“Low,” “medium,” and “high” are not standardized across burners, pans, and fuels. A “medium-high” setting on a powerful gas burner may be much hotter than on a coil electric stove. Recipe writers use visual and auditory cues to compensate: “heat the oil until it shimmers,” “add a bread cube and it should sizzle immediately,” “the onions should soften without coloring.”

**Recommendation:** pair every stovetop heat level with at least one sensory cue. For example: “Heat a large skillet over medium-high heat until a drop of water sizzles and evaporates on contact, about 2 minutes.” This is an **editorial convention** grounded in the variability of equipment.

### 5.3 Pan sizes and how they affect results

Pan size is not cosmetic. A 9-inch round pan is more than 25% larger in area than an 8-inch round pan, so the same batter will be thinner and can overbake. America’s Test Kitchen recommends scaling cake recipes by the ratio of pan areas when changing pan size, not by guessing. Dark metal pans absorb more heat and can overbrown crusts; glass pans heat more slowly and can shatter under broilers; cast iron retains heat and sears differently.

**Recommendation:** give pan dimensions and depth, not just “a baking dish.” For example: “a 9-inch (23-cm) round cake pan, 2 inches (5 cm) deep.” When pan size is flexible, state the range and the cue for doneness rather than a fixed time. For pan substitutions, provide an area conversion factor or warn that the recipe has not been tested in other pans.

### 5.4 Writing recipes that tolerate equipment differences

A resilient recipe gives the cook multiple ways to judge success:

- **Temperature range** rather than a single number: “350–375°F (175–190°C).”
- **Visual and tactile cues**: “until the crust is golden and pulls away from the sides.”
- **Time range** with a check point: “start checking at 20 minutes.”
- **Equipment notes**: “If using a dark pan, reduce the oven temperature by 25°F.”
- **Thermometer guidance**: NIST calls thermometers invaluable kitchen tools and recommends verifying them in boiling water.

The AI should flag recipes that are **equipment-sensitive** — baking, candy, deep-frying, pressure cooking, sous vide — and provide more explicit equipment specifications for those than for a soup or stir-fry.

---

## 6. Scaling

### 6.1 What scales linearly and what does not

| Category                                       | Scaling behavior                                                                                         | Why                                                                                                     |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Meat, vegetables, stock, most liquids**      | Approximately linear by weight                                                                           | These are bulk ingredients whose mass determines the dish’s quantity                                    |
| **Salt in dough, brine, cured foods**          | Should be proportional to flour/water/meat weight                                                        | Salt affects structure, water activity, and safety; use baker’s percentages or brine ratios             |
| **Salt and strong spices in sauces and stews** | Sublinear; start lower than the calculated amount                                                        | Perceived saltiness and spice heat do not scale linearly with concentration; taste is the final control |
| **Chemical leavening**                         | Often sublinear at large batches; test-kitchen guidance suggests about 1.5× when doubling rather than 2× | Leavening affects crumb structure and can produce bitter or collapsing results if overused              |
| **Eggs**                                       | Linear by weight; use grams                                                                              | Egg size varies; weight is the reliable scaler                                                          |
| **Alcohol**                                    | Sublinear in some dishes                                                                                 | Alcohol flavor and evaporation behavior change with volume and surface area                             |
| **Garnish, herbs, finishing oil**              | Often sublinear                                                                                          | Plate balance and aroma intensity do not need to double with portion count                              |
| **Cooking time**                               | Not linear                                                                                               | Depends on thickness, pan geometry, heat transfer, and surface-area-to-volume ratio                     |
| **Pan size**                                   | Area-based, not volume-based                                                                             | A small increase in diameter is a large increase in area                                                |
| **Reduction sauces**                           | Not linear in the same pot                                                                               | Evaporation is a function of surface area, not liquid volume                                            |

Heart Foundation New Zealand’s adaptation guidance recommends increasing baking powder, baking soda, yeast, spices, and salt by **1.5× when doubling**, then tasting and adjusting. This is a **test-kitchen convention** rather than a universal law; the exact factor depends on the recipe. The same guidance says small inaccuracies in the original recipe become large inaccuracies when scaled up, especially for ingredients used in very small amounts.

### 6.2 Cooking time and pan geometry

Cooking time does not double when the batch doubles. It depends primarily on the **distance heat must travel** — the thickness of a roast, the depth of batter in a pan, the diameter of a potato — and on the pan’s surface-area-to-volume ratio. America’s Test Kitchen warns that doubling baked goods changes the depth and surface area of the batter, so the same temperature and time will not produce the same result. Doubling rice and water in the same pot can produce mushy rice because the absorption ratio and surface area do not scale together. Doubling a bean stew in the same pot adds liquid but not evaporation surface area, so the stew takes longer to reduce.

**Recommendation:** when scaling, decide whether to **scale the pan** or **scale the batch within the same pan**. If the pan is scaled to maintain the same depth, cooking time may stay similar. If the same pan is used and the depth increases, cooking time must increase and the center may need extra protection from overbrowning. For baking, the safest approach is to scale the recipe to the pan area or to bake in multiple batches.

### 6.3 Practical scaling rules for an AI assistant

1. **Scale by weight, not volume**, wherever possible. Convert the source recipe to grams first, apply the factor, then convert back to user-friendly units.
2. **Scale up to 2× by formula** for most cooking recipes. Adjust salt and strong spices to about 1.25–1.5× when doubling, then taste.
3. **For 2–4×**, split into batches for frying, baking, and reductions. Do not try to double a single cake batter in one pan or fry twice as much food in the same oil without recovery time.
4. **Above 4×**, use a tested large-quantity recipe or run separate batches. Home equipment capacity — mixer bowl, oven, fryer, stockpot — becomes the limiting factor.
5. **Re-test any scaled baking recipe** that changes leavening, pan size, or flour type. Scaling is not a purely mathematical operation in baking.
6. **Flag nonlinear ingredients** in the UI: “This recipe contains baking powder; the scaled amount has been adjusted to 1.5× rather than 2×. Check the batter consistency before baking.”

---

## 7. Language and locale

### 7.1 Grammatical mood of instructions

Recipe instructions are not phrased the same way across languages. English recipes overwhelmingly use the imperative: “Mix the flour and sugar.” German recipes conventionally use the **infinitive** as a directive form: “Mehl und Zucker verrühren.” French recipes use either the **infinitive** or the **imperative**, with the infinitive common in written recipes: “Mélanger la farine et le sucre” or “Mélangez la farine et le sucre.” Spanish recipes frequently use the **passive reflexive/impersonal “se”**: “Se baten los huevos” — literally “the eggs are beaten” — rather than a direct imperative.

| Language | Typical recipe mood                 | Example                      | Notes                                                             |
| -------- | ----------------------------------- | ---------------------------- | ----------------------------------------------------------------- |
| English  | Imperative                          | “Mix the flour and sugar.”   | Standard in UK, US, Australian, Canadian English                  |
| German   | Infinitive                          | “Mehl und Zucker verrühren.” | Text-type convention; not a command form in the grammatical sense |
| French   | Infinitive or imperative            | “Mélanger…” / “Mélangez…”    | Both are used; infinitive is common in written recipes            |
| Spanish  | Passive reflexive / impersonal “se” | “Se baten los huevos.”       | Common in recipe instructions; avoids direct address              |

**Recommendation:** do not translate English imperatives word-for-word into German or Spanish. Generate the target-language recipe from a structured action representation — verb, ingredients, equipment, cue — and realize it in the target language’s conventional recipe mood.

### 7.2 Section headings

Section headings vary by language and publisher. Common patterns include:

| Language     | Ingredients  | Method / preparation      |
| ------------ | ------------ | ------------------------- |
| English (UK) | Ingredients  | Method                    |
| English (US) | Ingredients  | Directions                |
| German       | Zutaten      | Zubereitung               |
| French       | Ingrédients  | Préparation               |
| Spanish      | Ingredientes | Preparación / Elaboración |

These are conventions, not fixed rules. Some publishers separate “Preparation” (prep) from “Cooking” in English; others use a single “Method.” For an AI assistant, store headings as a locale-specific style pack and allow the user to choose “prep/cook split” as a structural preference.

### 7.3 Ingredient naming and dairy products

Ingredient names do not map one-to-one across countries. Well-known English pairs include:

- UK **aubergine** = US **eggplant**
- UK **courgette** = US **zucchini**
- UK **plain flour** = US **all-purpose flour**
- UK **bicarbonate of soda** = US **baking soda**
- UK **cornflour** = US **cornstarch**
- UK **double cream** ≈ US **heavy cream**
- UK **single cream** ≈ US **light cream**
- UK **soured cream** = US **sour cream**

Dairy is especially treacherous. **Half-and-half** is a US product made from milk and cream; the UK has no exact equivalent, and single cream is close but not identical in fat content. **Crème fraîche** and **sour cream** have different cultures, fat levels, and heat stability; substituting one for the other one-to-one can cause curdling or change the acidity of the dish. The AI should model dairy by **fat percentage and behavior** (whipping, curdling, culturing), not just by name.

### 7.4 Package sizes and produce sizes

Package sizes are a major source of localization failure:

- US butter sticks are 113 g; Australian and European butter blocks are often 250 g.
- US cans of evaporated milk are 5 fl oz (about 147 mL) or 12 fl oz (about 354 mL); other markets use different sizes.
- US “large” eggs are about 50 g shelled; egg sizing systems differ in Europe and Australia.
- “Medium onion” ranges from about 150 g to 225 g depending on the source and country.

**Recommendation:** specify weight and volume, not just package counts. “1 × 400 mL can chopped tomatoes, drained (about 240 g drained weight)” is localizable; “1 can tomatoes” is not.

### 7.5 Localization pitfalls

- **Literal translation of “cup.”** A US cup is not a metric cup. Translate the unit, not just the word.
- **Oven temperatures.** US recipes assume conventional Fahrenheit; UK recipes often give fan and gas. Do not translate “350°F” to “180°C” without stating conventional versus fan.
- **False friends.** “Biscuit” in the US is a quick bread; in the UK it is a cookie. “Pudding” can mean a specific dessert in the UK or a general dessert in the US. “Entrée” is a main course in the US but a starter in French.
- **Vague quantities.** “A knob of butter,” “a glug of oil,” “a pinch” do not translate cleanly. Convert to approximate grams or millilitres and label as approximate.
- **Ingredient availability.** Do not assume the target market has the same product. Offer a local substitute with a rationale: fat content, acidity, starch content, or salt level.

The AI should treat localization as **adaptation, not translation**: preserve the dish’s function, texture, and safety, while changing names, units, package sizes, and equipment references to match the target market.

---

## 8. Restructuring existing recipes

### 8.1 What can be changed freely

Under US copyright law, “mere listings of ingredients as in recipes, formulas, compounds, or prescriptions are not subject to copyright protection.” Copyright may apply when a recipe is accompanied by “substantial literary expression in the form of an explanation or directions,” or when recipes are compiled into a cookbook with original selection and arrangement. This means an editor can generally change:

- **Structure**: reorder sections, separate prep from cooking, add an equipment list.
- **Headings**: use house-style headings.
- **Wording of the method**: rewrite in the house voice, provided the rewrite is not a close paraphrase of distinctive expressive prose.
- **Units**: convert to the user’s unit system, with the caveats in Section 3.
- **Ingredient list format**: order by use, group by component, add prep notes.
- **Notes and serving suggestions**: add or reorganize.
- **Headnote**: rewrite entirely; do not copy the original headnote verbatim.

What should **not** be changed freely is the **expressive content** of the original — a distinctive headnote, a literary description, a personal story, or a photographer’s image. Those are protected expression, even if the underlying recipe is not.

### 8.2 What requires re-testing or care

Any change that affects the chemistry, physics, or safety of the dish needs verification:

| Change                         | Risk                                                                             | Action                                                                                            |
| ------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Unit conversion**            | Rounding errors, especially for flour, leavening, and small-quantity ingredients | Convert by weight where possible; flag ingredients where volume and weight diverge                |
| **Scaling**                    | Nonlinear salt, leavening, cooking time, pan size                                | Use the scaling rules in Section 6; re-test baking                                                |
| **Substitutions**              | Fat, protein, starch, acidity, and water content change                          | Provide rationale and expected sensory change; test or warn                                       |
| **Pan size change**            | Depth and surface area change; center may undercook or edges overbrown           | Use area conversion; adjust time and temperature; test                                            |
| **Oven type change**           | Conventional vs fan vs gas                                                       | Provide conversion and “check early” guidance                                                     |
| **High altitude**              | Leavening, boiling point, evaporation change                                     | NIST advises adjustments for baking, canning, pressure cooking, and candy making at high altitude |
| **Food-safety-critical steps** | Undercooking, raw dough, improper cooling                                        | Never change without referencing USDA/FDA guidance                                                |
| **Allergen claims**            | Legal and safety risk                                                            | Verify every ingredient and cross-contact statement                                               |

### 8.3 Copyright and attribution ethics

The legal minimum is not the ethical minimum. Even when a recipe’s ingredient list is not copyrightable, professional norms require attribution. The Los Angeles Times describes three levels of attribution used by its test kitchen:

- **“Adapted from”** — used for most recipes taken from other sources, because almost every recipe is changed in testing or copy-editing.
- **“Based on a recipe from”** — used when the recipe has been changed more dramatically.
- **“Inspired by”** — used when another recipe provided an idea or flavor pairing rather than a closely followed formula.

The International Association of Culinary Professionals’ ethics guidelines similarly advise using “adapted from,” “based on,” or “inspired by,” depending on how much the recipe has been revised. Attribution should include the author, title, publisher or URL, and year, and should state what was changed.

**Recommendation for the AI assistant:** maintain a provenance record for every recipe: source, author, URL or bibliographic data, date accessed, license or permission status, and a change log. When restructuring, generate an attribution line automatically based on the degree of change. Never strip attribution to make a recipe appear original.

### 8.4 A practical restructuring workflow

1. **Capture the source** exactly, including headnote, ingredient list, method, notes, and any images.
2. **Separate facts from expression** — ingredient quantities and basic procedures are facts; the headnote and distinctive method prose are expression.
3. **Parse into structured data** — ingredients with quantity, unit, prep, and step references; equipment; times; temperatures; sensory cues.
4. **Map to the target house style** — headings, section order, units, serving size, equipment list.
5. **Convert and scale with flags** — identify nonlinear ingredients and equipment-sensitive steps.
6. **Rewrite the method** in the target language and mood, one action per step, preserving safety warnings and critical cues.
7. **Re-test or mark as untested** — any change to leavening, pan size, scaling, or substitutions should be tested or explicitly flagged.
8. **Attribution and QA** — add source credit, change log, and a final read-through against the ingredient list and method.

---

## 9. Readability and accessibility

### 9.1 Serving beginners and experienced cooks

Beginners need more **explicit scaffolding**: equipment lists, prep notes, sensory cues, explanations of why a step matters, and definitions of techniques. Experienced cooks want **compression**: fewer basic explanations, faster scanning, and technique notes only where they add value. BBC Good Food’s recipe-writing guidance explicitly says the method should be explained clearly “to allow for both beginner and more experienced cooks”.

A layered format serves both:

- **At a glance**: yield, time, equipment, key allergens.
- **Method**: concise numbered steps with times, temperatures, and sensory cues.
- **Notes**: “Why this works,” “Make ahead,” “Storage,” “Substitutions,” “Technique.”
- **Beginner tip**: optional callout for knife skills, doneness, or equipment.
- **Advanced variation**: optional callout for experienced cooks.

This is an **editorial convention**, but it is consistent with cognitive-load principles: the main method stays uncluttered, while optional detail is available without forcing everyone to read it.

### 9.2 Cognitive load and procedural design

The research base supports several concrete design choices:

- **Headings and chunking** help readers build a mental model of the procedure and improve recall.
- **One action per step** reduces the amount of information that must be held in working memory while acting.
- **Use-order presentation** reduces the need to search back and forth between ingredients and steps.
- **Spatial contiguity** — keeping related information close together — reduces split attention.

**Recommendation:** keep ingredient quantities in the ingredient list, not repeated in every step, except for divided ingredients and critical small quantities. Use numbered lists, not dense paragraphs. Put warnings immediately before the action. Avoid cross-references such as “see step 3” when the information can be repeated locally.

### 9.3 Accessibility

Accessibility is broader than plain language. The Web Content Accessibility Guidelines require, among other things, text alternatives, sufficient contrast, resizable text, and consistent navigation【?】. For recipes specifically:

- **Do not rely on colour alone** to indicate doneness, danger, or ingredient grouping. Use text labels and icons with text alternatives.
- **Describe visual cues in non-visual terms**: sound (“a gentle sizzle”), smell (“nutty and toasted”), texture (“springs back when pressed”), time, and temperature. This helps blind and low-vision cooks, and also helps beginners.
- **Use real numbered lists and headings**, not tables or images of text, so screen readers can navigate the method.
- **Provide an ingredient checklist** that can be marked off; this supports working memory and shopping.
- **Offer scalable text and a high-contrast mode**; avoid PDF-only recipes.
- **Keep units and temperatures in text**, not only in images.

These are **accessibility standards and editorial best practices**, not recipe-specific research findings, but they align with the cognitive-load principles above.

### 9.4 Readability without loss of precision

Short sentences, active voice, and common words improve readability, but recipe writing cannot sacrifice precision for simplicity. “Cook the chicken until done” is readable but useless; “Cook the chicken until the thickest part registers 165°F/74°C, 18–22 minutes” is longer but safer and more reproducible.

**Recommendation:** use plain language for actions and cues, but keep precise nouns, numbers, and temperatures. Define technical terms once — “deglaze (add liquid to loosen the browned bits)” — and then use the term consistently.

---

## Cross-cutting recommendations for the AI cooking assistant

1. **Use a structured recipe schema**, not flat text: ingredients with quantity, unit, prep stage, and step references; equipment with dimensions; times split into prep/cook/hands-off; temperatures with oven type; safety warnings with severity.
2. **Make house style configurable**: unit system, section order, headnote length, equipment list on/off, “prep/cook” split, grammatical mood, and attribution format.
3. **Default to weight-first in baking**, volume-tolerant in cooking, and weight-mandatory in large-batch scaling.
4. **Flag nonlinear changes** — salt, spices, leavening, pan size, cooking time, evaporation — rather than silently multiplying.
5. **Localize, don’t literal-translate**: adapt ingredient names, package sizes, oven temperatures, and grammatical mood to the target market.
6. **Preserve provenance and attribution** for every restructured recipe; generate “adapted from,” “based on,” or “inspired by” automatically.
7. **Separate safety-critical information** from culinary preference: USDA/FDA temperatures, raw-dough warnings, allergens, and storage limits should never be treated as style choices.
8. **Layer detail**: concise method for scanning, optional notes for depth, beginner tips and advanced variations for different skill levels.
9. **Test the output against the source**: every ingredient in the list should appear in the method, every method ingredient should appear in the list, and every divided ingredient should reconcile.
10. **Mark untested adaptations**. If the system changes leavening, pan size, scaling, or substitutions, it should say so rather than presenting the result as fully tested.

---

## References

America’s Test Kitchen. (2024a, January 24). _How to actually follow a recipe_. https://www.americastestkitchen.com/articles/7947-how-to-actually-follow-a-recipe

America’s Test Kitchen. (2024b, February 28). _No, you can’t always just double a recipe_. https://www.americastestkitchen.com/articles/8047-no-you-cant-always-just-double-a-recipe

America’s Test Kitchen. (2024c, January 31). _How to scale a cake recipe for any size pan_. https://www.americastestkitchen.com/articles/8002-scale-recipe-for-any-pan

BBC. (2009, January 27). _BBC Food blog: How to make the perfect meringue_. https://www.bbc.co.uk/blogs/food/2009/01/how-to-make-the-perfect-meringue

BBC Good Food. (2012, February 1). _How to write a recipe_. https://release.bbcgoodfood.com/howto/guide/how-write-recipe

Cabot Creamery. (2025, July 16). _How many tablespoons in a stick of butter?_ https://www.cabotcreamery.com

Chandler, P., & Sweller, J. (1991). Cognitive load theory and the format of instruction. _Cognition and Instruction, 8_(4), 293–332. https://doi.org/10.1207/s1532690xci0804_2

Delicious. (2024, December 10). _The difference between UK, US and Aussie tablespoons could make or break your next bake_. https://www.delicious.com.au/food-files/how-to/article/difference-between-australian-uk-us-tablespoon-measurements/1d2nrtnv

Dixon, P. (1982). Plans and written directions for complex tasks. _Journal of Verbal Learning and Verbal Behavior, 21_(1), 70–84. https://doi.org/10.1016/S0022-5371(82)90456-X

Espinosa Castañeda, M. (2016). _Macroestructura y microestructura de la receta de cocina_ [Bachelor’s thesis, Universidad de Salamanca]. Gredos. https://gredos.usal.es/xmlui/bitstream/handle/10366/127101/Espinosa_Castañeda_Mónica%20TFG.pdf

Food and Drug Administration. (n.d.). _Raw dough can make you sick_. https://www.fda.gov/consumers/consumer-updates/raw-dough-can-make-you-sick

Food52. (2019, February 22). _Recipe introductions matter. Here’s why_. https://food52.com/story/23840-why-recipe-headnotes-matter-kevin-kruse-tweet

Health Canada. (2026). _Measure ingredients like a pro_. Canada’s food guide. https://www.canada.ca/en/health-canada/services/food-guide/eating-support/kitchen/cooking-skills/measure-ingredients-pro.html

Heart Foundation New Zealand. (n.d.). _Recipe adaptation guidelines_. https://assets.heartfoundation.org.nz/documents/food-industry/hospitality-hub/recipe-adaptation-guidelines.pdf

Jacob, D. (2015). _Will write for food: The complete guide to writing cookbooks, blogs, memoir, recipes, and more_ (3rd ed.). Da Capo Lifelong Books.

Jacob, D. (2020). _15 common recipe-writing errors_ [E-book]. https://diannej.com/wp-content/uploads/2020/03/DJ_e-book_15-common-errors.2020.pdf

King Arthur Baking Company. (n.d.). _Ingredient weight chart_. https://www.kingarthurbaking.com/learn/ingredient-weight-chart

Los Angeles Times. (2012, December 17). _The complicated case of the simple cookie_. https://www.latimes.com/food/la-xpm-2012-dec-17-la-dd-complicated-case-simple-cookie-20121217-story.html

McCormick Test Kitchen. (n.d.). _Recipe writing tips_. https://www.mccormick.com.au/news/~/media/89dc84496b334bffacac21660d50f47c.ashx

Milk Street. (n.d.). _How to count your eggs before they hatch_. https://www.177milkstreet.com

National Institute of Standards and Technology. (2023a, March 14). _Metric kitchen: Cooking measurement equivalencies_. https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-cooking-measurement-equivalencies

National Institute of Standards and Technology. (2023b, March 1). _Metric kitchen: Culinary measurement tips_. https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-culinary-measurement-tips

Nigella Lawson. (2017, July 6). _Size of an onion_. https://www.nigella.com/ask/size-of-an-onion

Ostmann, B. G., & Baker, J. L. (2001). _The recipe writer’s handbook_ (Rev. ed.). Wiley.

Russchen, S. (2022). _One action at a time: The effect of action segmentation in multimodal origami instructions on experience and task performance_ [Master’s thesis, University of Groningen]. https://arts.studenttheses.ub.rug.nl/39267/2/Masterscriptie-final-version-Simone-Russchen-6518559.pdf

Southern Living. (2025, May 11). _Here’s why recipe times never seem accurate_. https://www.southernliving.com/recipe-times-never-seem-accurate-11725412

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. _Cognitive Science, 12_(2), 257–285. https://doi.org/10.1016/0364-0213(88)90023-7

The Kitchn. (2011, September 19). _Recipe headnotes: Do we really need them?_ https://www.thekitchn.com/recipe-headnotes-do-we-really-156205

U.S. Copyright Office. (n.d.). _Recipes_ (FL-122). https://www.copyright.gov/fls/fl122.html

USDA Food Safety and Inspection Service. (2024, August 9). _Deep fat frying and food safety_. https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/deep-fat-frying

USDA Food Safety and Inspection Service. (2025a, April 14). _Safe minimum internal temperature chart_. https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart

USDA Food Safety and Inspection Service. (2025b, September 5). _How long can you keep leftovers in the refrigerator?_ https://ask.fsis.usda.gov/article/how-long-can-you-keep-leftovers-in-the-refrigerator

USDA Team Nutrition. (n.d.). _Recipe adjustment – Method 1 (factor method)_. https://teamnutrition.usda.gov

Virginia Cooperative Extension. (n.d.). _How to write a recipe_ (FST-384). https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/FST/FST-155/FST-384.pdf

W3C. (2023). _Web Content Accessibility Guidelines (WCAG) 2.2_. https://www.w3.org/TR/WCAG22/

Which? (2021, November 22). _Oven temperature conversion table_. https://www.which.co.uk
