# Writing and Restructuring Recipes for a Multilingual AI Cooking Assistant: Conventions, Evidence, and Pitfalls

Most of what makes a recipe "well written" is editorial convention that experienced editors broadly agree on. The parts that rest on hard evidence are narrower: weighing beats volume for dry ingredients; cup and spoon sizes really do differ by country; time is not a reliable doneness cue without a sensory check; and research on procedural instructions supports goal-first structure, overviews of sub-tasks, and keeping needed information where the cook is looking. For an assistant that restructures recipes, the safest rule is simple: you can freely change structure, wording and presentation, but any change to *quantities* (unit conversion, scaling, substitution) is a change to the recipe itself and needs to be handled as such.

## TL;DR

- **Structure and wording are free to change; quantities are not.** Rewriting steps, regrouping ingredients, splitting "preparation" from "cooking" and translating are presentation changes. Converting cups to grams, scaling, or swapping "double cream" for "heavy cream" changes the food and should be done with ingredient-specific data, flagged, and ideally tested. In the US, ingredient lists and plain directions are not copyrightable, but headnotes and expressive method text are — so restructure in your own words and attribute ("adapted from").
- **Weight is the most reliable unit, and "cup" and "tablespoon" are not universal.** A cup of flour can vary by up to 20% depending on the measuring method and "the heavy- or light-handedness of the baker" (America's Test Kitchen), and from about 120 g to 160 g (King Arthur Baking); a US cup is about 237 mL, the FDA labelling cup 240 mL, the Australian/metric cup 250 mL and the Japanese cup 200 mL; the Australian tablespoon is 20 mL versus 15 mL elsewhere. Store quantities internally as mass (or mL for liquids) plus the source unit, and render per locale.
- **Write methods as goal-first, one-action-per-step instructions with sensory cues.** Research (Dixon, 1987; Ganier, 2004; Buykx, 2013) supports putting the goal before the actions, giving an overview of sub-tasks, and reducing the need to look back and forth between ingredient list and method. Pair every time with a doneness cue ("10–12 minutes, until golden at the edges"), and put warnings at the step where they matter.

---

## Key Findings

| Area | Evidence-based | Editorial convention |
|---|---|---|
| Weight vs. volume | Flour by cup varies up to 20% (America's Test Kitchen) and by about 30 g between testers (Cuisine at Home) | Whether to lead with grams or cups in a given market |
| Unit definitions | Cup/spoon sizes are defined by regulation or national practice (FDA, Australian, Japanese conventions) | Rounding rules for dual units |
| Ingredient order | — (no controlled studies found) | Order of use; group by component |
| Method structure | Goal-first and overview-first instructions are read faster and cause fewer problems (Dixon; Buykx) | Numbered steps; one action per step |
| Doneness | Food-safety temperatures (physical fact); oven variability | Phrasing "X minutes, or until…" |
| Fan ovens | Physical effect is real; exact offset is not standardised | UK: −20 °C; US: −25 °F |
| Scaling | Evaporation scales with surface area; heat penetration with thickness (physics)\[1\] | Specific reduction factors for salt and leavening\[2\]\[3\] |
| Copyright | US Copyright Office: ingredient lists and simple directions not protected | "Adapted from" / "inspired by" attribution tiers\[4\] |

---

## 1. Anatomy of a Well-Written Recipe

Each element of a recipe answers a question the cook has *before* or *during* cooking. Most of these elements are convention, not evidence; they persist because they reduce failures and support decisions.

**Title.** Tells the cook what the dish is and, ideally, what makes it distinct ("Cucumber Salad with Fresh Dill"). Ostmann and Baker's guidance, as adapted in the Archangel Ink cookbook style guide, asks that title tone be consistent across a collection — either descriptive or playful, not mixed.\[5\] For an AI assistant, descriptive titles are safer, because titles get translated and searched.

**Headnote.** One or two paragraphs that explain why to make the dish, its origin, or a key tip. The Archangel Ink guide (adapted from Ostmann and Baker) states that "each recipe must have a headnote."\[5\] This is a book-publishing convention. Online, headnotes have grown long, partly — as legal commentators note — because the narrative text is copyrightable while the recipe itself is not.\[6\] *Where experts disagree:* editors value short, useful headnotes; many readers dislike long blog preambles. For an assistant, the useful headnote is short and practical: what the dish is, what the key technique is, and what can go wrong.

**Yield/servings.** Mandatory in every style guide consulted. Ostmann and Baker recommend one consistent construction, e.g., "Makes 4 servings," "Makes 1 cup," "Makes 2 dozen."\[5\] Yield is also the anchor for scaling, so an assistant should store it in a structured form (count + unit, e.g., "24 cookies" or "4 servings"). The Recipe Writer's Handbook lists failure to indicate yield among the common errors.\[7\]

**Active and total time.** Not covered in the handbooks consulted here; it is a modern editorial and web convention (recipe cards, schema.org markup). Its purpose is planning. The common failure is leaving out passive time (marinating, chilling, rising, resting), which is what decides whether a recipe works on a weeknight. Recommendation: always state passive time separately ("Active 25 min · Total 3 h, including 2 h chilling").

**Equipment.** Ostmann and Baker's guidance is to specify sizes: "a large skillet" can be general, but baking dishes need dimensions ("9 x 13-inch pan," "2-quart baking dish").\[5\] A separate equipment list is optional convention; mentioning equipment in the method is essential. Listing unusual equipment up front (stand mixer, 23 cm springform, thermometer) prevents mid-recipe surprises.

**Ingredient list.** See section 2.

**Method.** See section 4.

**Notes (make-ahead, storage, variations).** Notes keep the method clean. The Archangel Ink guide recommends moving conversational or technical tangents into "sidebars or chef's notes rather than appearing in the middle of directions."\[5\] Make-ahead and storage notes are also where food-safety information (refrigeration time, reheating) belongs. Variation notes are where substitutions belong — clearly separated from the tested recipe.

**Serving suggestions (side dishes, drinks).** Pure convention, and optional. These are useful for meal planning, but they are also where an assistant is most likely to produce generic filler. Keep them specific to the dish and the locale (a German *Beilage* suggestion such as Salzkartoffeln makes sense for a German user in a way it may not for a Japanese user).

**Consistency across a collection** is the strongest cross-cutting principle in the Ostmann and Baker–derived guide: use the same ingredient name everywhere (not "scallions" in one recipe and "green onions" in the next), the same yield phrasing, and a style sheet to track decisions.\[5\] An AI assistant should enforce this with a controlled vocabulary per locale.

---

## 2. The Ingredient List

### Order and grouping

- **Order of use.** This is the most consistently agreed rule. Dianne Jacob calls "list ingredients in order of use, and make sure every ingredient is used in the method" the "most irrefutable" conventions;\[8\] Ostmann and Baker's guidance says the oil, onions and garlic for a first-step sauté should come first in both list and method.\[5\] *Evidence status:* convention, but supported indirectly by procedural-instruction research showing cooks don't read linearly and rely on the "narrative of ingredients" (Buykx, 2013).\[9\]
- **Every listed ingredient must appear in the method, and vice versa.** Missing ingredients are among the most common recipe errors Ostmann and Baker identify.
- **Group by component** when a recipe has distinct parts ("For the dough," "For the filling," "For the glaze"). This mirrors the sub-goal structure that Buykx and Petrie (2012) found helps cooks plan.\[10\]

### Prep notes: why "1 cup chopped walnuts" ≠ "1 cup walnuts, chopped"

Ostmann and Baker make the point explicitly: "'1 cup chopped walnuts' is going to yield a different result than '1 cup walnuts, chopped.'"\[5\] The rule is about *when you measure*:

- **Prep before the ingredient name** → prep first, then measure ("1 cup chopped walnuts": chop, then fill the cup).\[11\] Chopped pieces pack differently from whole ones.
- **Prep after the comma** → measure or count first, then prep ("1 cup walnuts, chopped").\[11\]
- For counted items, the comma form is standard: "1 large onion, finely chopped." "1 finely chopped onion" is grammatically odd but means the same; for counted items the difference matters little. It matters most for volume measures and for weights of trimmed vs. untrimmed produce ("500 g potatoes, peeled" vs. "500 g peeled potatoes" differ by the weight of the peel).
- **Order prep words in the order you do them**: "1 (15-ounce) can chickpeas, drained and rinsed"; "1 small avocado, pitted and peeled" (Ostmann and Baker, via Archangel Ink).\[5\]
- **Specify cut size when it affects cooking** ("cut into ½-inch cubes"); use general terms ("coarsely chopped," "finely chopped") only when the size doesn't matter, and use one term consistently.\[5\]

For an assistant, the important design point is that "chopped walnuts, 1 cup" and "walnuts, 1 cup, chopped" are *different data*, and conversion to grams must use the density of the right form.

### "To taste," optional, and multi-use ingredients

- **No amount needed** for garnishes, dusting, adjusting texture, and seasoning to preference: "Freshly ground black pepper, to taste"; "Water, as needed"; "Powdered sugar, for dusting" (Archangel Ink, adapted from Ostmann and Baker).\[5\] The Italian equivalent is **q.b.** (*quanto basta*, "as much as needed"), which Treccani defines as used both in medical prescriptions and cooking recipes.\[12\]\[13\]
- **But give a starting point for salt** in anything where it's structural (bread, brines, pasta water, cured items) — "to taste" is unusable for a beginner and unsafe for a brine. A good pattern is "1 tsp fine salt, plus more to taste."
- **Optional ingredients** should be labelled "(optional)" in the list, and the method should say what to do with them or without them.
- **Ingredients used in several steps**: list the total once, with the split ("3 tbsp butter, divided" in US style; or "3 tbsp butter (2 for the sauce, 1 for finishing)"). Then give the specific amount at each step in the method. This is more than politeness: Buykx (2013) found that putting quantities into the method steps made recipes "clearer and easier to read" because it "reduces the need for the cook to look up and mentally integrate information from different sources."\[9\]

### Precision

- Specify sizes for produce and packages: "2 small onions," "1 (1-inch) piece fresh ginger," "1 (15-ounce) can black beans" (Ostmann and Baker). Exceptions where size is not needed include garlic cloves, green onions, cherry tomatoes, and berries — but an amount is still required.\[5\]
- Ostmann and Baker prefer fractions over decimals in US recipes ("1½ ounces," not "1.5 ounces").\[5\] In metric locales, decimals with grams are normal (and fractions of grams are unusual outside of yeast and salt).

---

## 3. Units and Measurement

### Weight vs. volume: the evidence

The evidence here comes from test kitchens rather than peer-reviewed studies, but it is consistent:

- **America's Test Kitchen** found "up to a 20 percent difference in the weight of a cup of flour" depending on technique and handedness, "a variance that can easily ruin a recipe"; it took the average of dozens of volunteers' measurements, 5 oz (~142 g), as its standard per cup.
- **King Arthur Baking** says a cup of all-purpose flour holds "around 120 grams" when fluffed, scooped and levelled, but "can hold up to 160 grams" if packed, and standardises on 120 g per cup.
- **Cuisine at Home** had eight testers measure a cup of flour with two measuring cups: weights ranged from 117–145 g with one cup and 110–141 g with the other — a ~30 g spread, plus a visible difference in capacity between two nominally identical cups.\[14\]
- **NIST** notes that using a dry measuring cup for liquids (or vice versa) "is a common way of introducing measurement errors," and recommends levelling dry measures and reading liquid meniscus on a flat surface.\[15\]

Note the conflict: ATK's cup of flour is ~142 g; King Arthur's is 120 g. **There is no single "correct" grams-per-cup for flour** — it depends on the source author's method. An assistant converting an American recipe should use the conversion convention of the source publisher where known, and otherwise a documented default, and say so.

**Where volume is fine:** liquids (volume is accurate), and small amounts of salt, spices and leaveners, where home scales lack resolution. Most of the world measures dry bulk ingredients by weight and small amounts by spoon.\[16\]

### Regional unit definitions

| Unit | US customary | US nutrition label (FDA) | UK / EU / NZ | Australia | Japan |
|---|---|---|---|---|---|
| Teaspoon | ~4.93 mL | 5 mL | 5 mL | 5 mL | 小さじ 5 mL |
| Tablespoon | ~14.79 mL | 15 mL | 15 mL | **20 mL** | 大さじ 15 mL |
| Cup | ~236.6 mL | 240 mL | 250 mL (metric cup, where used) | 250 mL | **200 mL** |
| Rice "cup" | — | — | — | — | 1 合 (gō) = **180 mL** |

Sources: FDA's 21 CFR 101.9(b)(5)(viii) defines, "for nutrition labeling purposes," a teaspoon as 5 mL, a tablespoon as 15 mL, a cup as 240 mL, 1 fl oz as 30 mL and 1 oz as 28 g.\[17\]\[18\] NIST's Metric Kitchen equivalency table likewise lists 240 mL = 1 cup, 15 mL = 1 tbsp and 5 mL = 1 tsp as approximate equivalents for "home cooking applications." Australian publishers state their conventions explicitly: Penguin Australia's conversion page says "One Australian metric measuring cup holds 250 ml, one Australian metric tablespoon holds 20 ml and one Australian teaspoon holds 5 ml."\[19\] Japanese manufacturers and publishers state 1 tbsp = 15 mL, 1 tsp = 5 mL, 1 cup = 200 mL, and 1 gō = 180 mL (e.g., Miyajima Shoyu).\[20\] Rice cookers come with a 180 mL cup, and a 200 mL cooking cup cannot substitute for it.\[21\]

**Practical consequences:**
- An Australian recipe calling for "2 tbsp cocoa" means 40 mL; a 15 mL spoon delivers 25% less.\[22\]\[23\]
- A Japanese recipe's "1 cup" of dashi is 200 mL — about 15% less than a US cup.
- "1 cup rice" in a Japanese rice-cooker context means 180 mL.\[21\]
- The UK has no standard culinary cup; modern UK recipes use grams and mL, with 15 mL tablespoons.

### Presenting dual units

Convention, not standard: lead with the unit system of the target locale and give the other in parentheses, rounded sensibly ("225 g (1 cup) butter" for UK; "1 cup (225 g) butter" for US). Rounding rules matter: FDA guidance rounds metric equivalents for labels, but for recipes the meaningful precision depends on the ingredient — 5 g for flour is fine; 1 g matters for salt and yeast in bread. Avoid false precision ("236.59 mL") and avoid rounding that compounds when scaled.

### Common conversion pitfalls

- **Flour and other powders by volume.** See above; use ingredient-specific density and state the convention.
- **Butter.** A US "stick" is ½ cup / 8 tbsp / 4 oz (~113 g). Outside the US, butter is sold in blocks (250 g in much of Europe and Australia) and "a stick" is meaningless. Convert to grams.
- **Brown sugar** ("packed" vs. not) and **chopped/grated items** (density depends on prep) — store the form with the quantity.
- **Fluid ounces vs. weight ounces.** FDA: 1 fl oz = 30 mL, 1 oz weight = 28 g; recipes conflate them.\[17\]
- **UK pint (~568 mL) vs. US pint (~473 mL).**
- **Eggs.** USDA "Large" is defined by a minimum of 24 oz per dozen (~57 g per egg in the shell; ~50 g edible). EU/UK grades are per egg: M 53–63 g, L 63–73 g, XL 73 g and over. A UK "large" egg is therefore bigger than a US "large"; the closest match to a US large is an EU/UK medium.\[24\]\[25\]\[26\] In egg-heavy baking (custards, genoise), specify egg weight in grams.
- **Onions, lemons, garlic.** "1 medium onion" varies widely across countries and seasons. Ostmann and Baker recommend specifying sizes and, where it matters, weights ("2 pounds russet potatoes").\[5\]
- **Can and package sizes.** "1 (15-ounce) can" is a US convention; common European tins are 400 g. When localizing, map to the nearest local package *and* check whether the recipe is sensitive to the difference (beans in a stew: no; condensed milk in a fudge: yes).

### Counted items

Counts are fine when the size doesn't matter much and the cook buys by count (eggs, cloves of garlic, lemons for juice). Best practice is count + size + weight where it matters: "2 medium carrots (about 200 g), peeled." For juice and zest, give the yield: "juice of 1 lemon (about 3 tbsp / 45 mL)."

---

## 4. Writing the Method

### What the research supports

Research on procedural instructions — mostly on devices and software, with a small body on recipes — offers several findings that transfer well:

- **Goal first, then actions.** Dixon (1987) found that "procedural directions are read faster when general organizational information is found at the beginning rather than at the end."\[27\] In recipes: "Make the sauce: melt the butter…" beats "Melt the butter… this is your sauce."
- **Readers alternate reading and doing.** Ganier (2004) models instruction use as cycles of reading a chunk, forming a goal, planning, acting and checking — all in limited working memory.\[28\]\[29\] So steps should be short enough to hold in mind while your hands are busy.
- **Specific instructions help first-time performance.** Eiriksdottir and Catrambone's (2011) review found that "specific instructions help initial performance, whereas more general instructions, requiring problem solving, help learning and transfer."\[30\] Most recipes are followed for first-time success, which argues for specific steps — with optional explanation for learners (see section 9).
- **Recipe-specific evidence.** In controlled cooking studies, Buykx (2013) found that cooks "do not read or perform the tasks of recipe instructions in sequence"; that putting ingredient quantities into method steps reduced cross-referencing; and that an overview of the recipe's sub-goals "reduced problems due to recipe content" and helped cooks plan parallel tasks. Step-by-step photos were liked, "but they did not reduce problems or errors."\[9\] (Ganier's appliance studies did find text-plus-pictures faster than either alone — so pictures help for some tasks, but don't assume they fix a recipe.)\[28\]
- **Split attention.** Cognitive load theory (Chandler & Sweller, 1991) predicts that forcing readers to integrate physically separated information (list here, step there) adds load.\[31\] This is the theoretical basis for repeating quantities in the steps.

*Caveat:* none of these studies tested the exact rules below; they are the research consistent with them.

### Best practices (mostly convention, informed by the above)

1. **One main action per step, or one tightly linked sequence.** "Heat the oil in a large skillet over medium-high heat. Add the onions and cook, stirring often, until soft and translucent, 6–8 minutes." is one step (one goal: soften onions). Breaking it into four steps adds navigation; merging it with the next stage overloads working memory.
2. **Strict chronological order, including invisible steps.** "Preheat the oven" goes where it must start — first for quick recipes, later for recipes with long marinating or rising (Ostmann and Baker). Same for boiling water and softening butter.\[5\]
3. **Separate preparation from cooking when the cooking is fast.** A "Before you start" or "Prep" block (mise en place: chop, measure, line pans) is ideal for stir-fries and anything where there's no time to chop mid-recipe. For slow recipes (braises, stews), integrated prep is more efficient — chop the carrots while the onions soften. This is a user-preference axis and a natural place for the assistant to let users choose.
4. **Make parallel tasks explicit.** "While the pasta cooks, make the sauce." Buykx's finding that sub-goal overviews help planning supports giving an overview line for complex recipes\[9\] ("You'll make the dough, chill it for 1 hour, then fill and bake").
5. **Pair times with sensory doneness cues.** Ostmann and Baker's guidance: give "both a suggested cooking time as well as a 'doneness test' when possible," e.g., "Bake 7 to 10 minutes, or until golden brown on the bottom."\[5\] Times vary with equipment; cues (colour, smell, sound, texture, internal temperature) don't. For meat and poultry, give an internal temperature — this is a food-safety requirement, not style.
6. **Always specify heat level** ("over medium heat," "reduce to a simmer").\[5\]
7. **Warnings at the point of use**, not in a headnote: "Carefully — the caramel will bubble up when you add the cream." "Don't let the garlic brown, or it will taste bitter." Put the reason in when it changes behaviour.
8. **Concise but not terse.** Ostmann and Baker's example: "Knead the dough for 3 to 5 minutes. I think it's best to coat your hands in a little flour before you knead the dough. You should also flour the work surface." (32 words, wrong order) becomes "Sprinkle some flour on a work surface and coat your hands as well. Knead the dough for 3 to 5 minutes." (21 words, right order).\[5\]
9. **Use the ingredient's list name in the method** so the cook can match them.

---

## 5. Heat and Equipment

### Ovens

- **Celsius vs. Fahrenheit.** °C = (°F − 32) ÷ 1.8. Recipes conventionally round: 350 °F is printed as 180 °C (exact: 176.7 °C). Rounding to the nearest 10 °C is standard in UK charts.\[32\]\[33\]\[34\]
- **Gas marks** (UK). Gas mark 1 = 275 °F (~140 °C), each mark adds 25 °F; gas 4 = 350 °F / 180 °C; gas 9 = 475 °F (BBC Good Food chart, as reproduced across UK references).\[35\]\[36\]
- **Fan/convection.** The UK convention is to set a fan oven **20 °C lower** than conventional. BBC Good Food's chart uses this, and Delia Smith's site explains its recipes "are tested using conventional top and bottom heat, so if you are using a fan oven, the general rule is to reduce the oven temperature by 20 degrees." The common US convention is **25 °F lower** (≈14 °C). These are rules of thumb; ovens differ, and manufacturers give their own figures. The exception Delia notes is telling: for her Christmas cake on the bottom shelf, she recommends 115 °C rather than a straight 20-degree cut — specific recipes sometimes deviate.\[33\]\[37\]
- **German recipes** commonly give both: "Ober-/Unterhitze 200 °C, Umluft 180 °C." This dual-mode convention is a good model for any locale.

**For an assistant:** always know which mode the source recipe assumed (UK recipes often print both; US recipes almost always assume conventional), store it, and render the user's mode. Flag that oven thermostats are often inaccurate and recommend an oven thermometer for baking.\[38\]

### Stovetop heat levels

There are no standard definitions of "medium heat"; burners and induction levels vary widely. Best practice is to describe the *effect* alongside the setting: "over medium heat, so the butter foams but doesn't brown"; "a gentle simmer — small bubbles breaking the surface occasionally." Sensory descriptions transfer across gas, electric and induction; numeric dial settings don't.

### Pan sizes

- **Area and depth drive baking time.** King Arthur Baking's substitution method compares bottom area (assuming ~2-inch depth): an 8-inch square and a 9-inch round both have about 64 sq in and are interchangeable; a 9 x 13-inch recipe can be made in two 9-inch rounds.\[39\] Shallower batter bakes faster, deeper batter slower.\[40\]\[41\]
- **Local pan sizes differ.** US recipes use inches (9 x 13, 9 x 5 loaf); European recipes use cm (24–26 cm springform, 30 cm loaf). Map to the nearest local standard by *area*, then adjust time and say so.
- **Stovetop pans:** a wider pan means faster evaporation and better browning; crowding a pan steams rather than sears.\[1\] Specify pan size when it affects the result ("a 12-inch / 30 cm skillet, so the chicken isn't crowded").

### Writing for equipment tolerance

- Give cues, not just numbers (section 4).
- Give a time range, and tell the cook to check at the start of the range.
- Name what can go wrong with substitute equipment ("If using a dark metal pan, check 5 minutes early").
- Avoid single-appliance dependence when possible, or provide an alternative ("If you don't have a stand mixer, use a hand mixer and beat for twice as long").

---

## 6. Scaling

Scaling the ingredient list by a single factor is the easy part.\[1\] The physics of cooking does not scale linearly, which means an assistant should scale quantities but *warn* about the elements below.\[3\]

| Element | Scales linearly? | Why |
|---|---|---|
| Most ingredients (flour, liquid in batters, meat, vegetables) | Yes | Proportions define the result |
| Eggs | Yes, but rounding | You can't easily use 1.5 eggs — weigh (≈50 g per US large egg) or round and adjust liquid\[3\] |
| Salt, spices, chilli | Start lower, adjust | Perception isn't linear; in reductions, salt concentrates as water evaporates. Specific "75%" rules circulate but lack primary evidence\[2\]\[42\] |
| Leavening | Roughly, at small factors | Practitioner sources recommend reducing for large scale-ups; evidence is anecdotal. At 2x for home batches, linear generally works\[43\]\[44\] |
| Liquid in reductions, braises, soups | No | Evaporation depends on surface area, not volume. A doubled sauce in the same pot reduces far more slowly; in a wider pan, closer to original\[1\]\[43\] |
| Cooking time (stovetop) | No | Bigger volume takes longer to heat; same piece size cooks in the same time\[2\]\[45\] |
| Baking/roasting time | No | Heat penetration depends on thickness/depth, not total mass. Same depth in a bigger pan ≈ same time; deeper ≈ much longer. A thicker roast takes disproportionately longer\[1\]\[3\] |
| Pan size | No — by area | Doubling batter needs double the *area* to keep depth constant (e.g., 8-inch square → 9 x 13-inch is ~1.8x)\[43\] |
| Oven temperature | Doesn't change | Unless depth changes substantially (deeper cakes sometimes bake lower and longer)\[44\]\[46\] |
| Frying oil, greasing fat | No | Set by pan, not batch\[3\] |

*Evidence status:* the evaporation and heat-transfer points are basic physics; the specific percentage adjustments widely quoted online for salt and leavening are rules of thumb without primary sources found in this research.\[47\]\[48\] The honest instruction is: scale linearly, then season to taste at the end, and check doneness by cue rather than time.\[44\]

**Practical rules for an assistant:** cap automatic scaling warnings at factors beyond about 2x or below ½; recalculate pan suggestions by area; never scale times by the factor;\[49\] restate doneness cues in scaled recipes; and for baked goods scaled up a lot, suggest multiple pans of the original size rather than one larger one\[48\] (this keeps depth and time constant, which King Arthur also suggests via the two-pan approach).\[1\]\[39\]\[43\]

---

## 7. Language and Locale

### Grammatical mood of instructions

| Language | Typical forms | Notes |
|---|---|---|
| English (US/UK/AU) | Imperative ("Chop the onion") | Universal in modern recipes |
| German | Infinitive ("Zwiebeln schälen und würfeln") or polite imperative ("Schälen Sie…"), sometimes informal "du" imperative online | The infinitive replaced the archaic subjunctive "man nehme…"; when the imperative is used, it is used without exclamation marks (LEO language blog). The infinitive is impersonal and compact\[50\]\[51\] |
| French | Infinitive ("Éplucher les oignons") or imperative *vous* ("Épluchez les oignons") | Both are standard. The OQLF says the infinitive suits short, impersonal, "less prescriptive" instructions, notes that "recipes are often in the imperative," and asks for consistency within a document.\[52\] Print cookbooks and packaging lean infinitive; magazines and web often use *vous* imperative |
| Italian | Imperative (often *tu* or *voi*), infinitive, or impersonal *si* | "q.b." (*quanto basta*) for unmeasured items (Treccani)\[12\] |
| Spanish | Imperative (*tú* or *usted*) or infinitive, varying by country and publisher | (Observed convention; not verified against a style authority in this research) |
| Japanese | Plain/polite verb forms and nominal step lists; measurements in 大さじ/小さじ/カップ/合 | "少々" (a little) and "ひとつまみ" (a pinch) are common unquantified amounts |

**For an assistant:** choose one mood per locale and enforce it. Don't mix "Éplucher… Ajoutez…" — the OQLF explicitly advises consistency.\[52\] Let users choose formality in languages where it matters (German *du/Sie*, Spanish *tú/usted*, French *tu/vous*).

### Section headings

Conventions vary: English "Ingredients / Method" (UK) or "Directions / Instructions" (US); German "Zutaten / Zubereitung"; French "Ingrédients / Préparation" (often with "Temps de préparation / Temps de cuisson"); Italian "Ingredienti / Procedimento" (or "Preparazione"); Spanish "Ingredientes / Preparación" (or "Elaboración"); Japanese 材料 (ingredients) / 作り方 (method). Many European formats separate prep time and cooking time explicitly — a natural fit for users who want "preparation" separated from "cooking."

### Ingredient naming that doesn't map one-to-one

- **Cream.** The UK's Food Labelling Regulations 1996 define minimum fat: single 18%, whipping 35%, double 48%.\[53\] US "heavy cream" is at least 36% milk fat (21 CFR 131.150); light whipping cream 30–36%.\[54\] So US heavy cream ≈ UK whipping cream, not double cream; double cream is richer and whips faster.\[53\]\[55\] German *Schlagsahne* (typically ≥30%) and French *crème fraîche* / *crème liquide* / *crème entière* are different again.
- **Quark, fromage blanc, ricotta, cottage cheese, Greek yogurt** — overlapping but not equivalent; substitution changes moisture and acidity.
- **Flour.** US all-purpose ≈ UK plain ≈ German Type 405/550 ≈ French T45/T55 ≈ Italian 00/0 — approximately, but protein contents differ. UK "self-raising" contains leavener; US "self-rising" similar but often with salt.
- **British vs. US vs. Australian terms:** aubergine/eggplant, courgette/zucchini, coriander (leaf)/cilantro, rocket/arugula, icing sugar/powdered sugar, caster sugar/superfine sugar, bicarbonate of soda/baking soda, minced meat (UK "mince")/ground meat, prawns/shrimp,\[56\] capsicum (AU)/bell pepper. "Biscuit" means cookie in the UK and a scone-like bread in the US.
- **Chilli, paprika, curry powder** vary in heat and composition by country.

### Produce and package sizes

As above: eggs graded differently (US per-dozen minimums vs. EU per-egg bands); butter in 250 g blocks vs. US 4 oz sticks; tins of 400 g vs. US 15-oz cans; produce sizes differ (American "medium" onions and lemons are often larger than European ones — an observation, not a standard). Use weights for anything that matters.

### Translation and localization pitfalls

1. **Translating "cup" as "Tasse"/"tasse"/"tazza"** without converting — the target-language reader will use a drinking cup.
2. **Translating units without converting regional definitions** (Australian tbsp, Japanese cup, rice gō).
3. **Literal ingredient translation** ("double cream" → "doppelte Sahne") instead of the closest local product, with a note.
4. **Oven mode loss** — dropping "fan" or "Umluft" in translation.
5. **Technique words without equivalents** (e.g., "fold," "cream butter and sugar," French *monter*, German *unterheben*). Prefer a short description over a single word in the target language when unsure.
6. **Culinary false friends:** French "crème" ≠ any one English cream; German "Paprika" is both the spice and bell peppers.
7. **Locale formatting:** decimal comma (1,5 kg), date-like fractions, temperature symbols, and units abbreviations (EL/TL in German = tablespoon/teaspoon; c. à s./c. à c. in French; Cc/cc ambiguity in Italian — Cookist notes "cc" and "Cc" are cucchiaino and cucchiaio, which is easily confused).\[57\]

---

## 8. Restructuring Existing Recipes

### What can change freely, what needs care

| Change | Risk | Treatment |
|---|---|---|
| Reordering ingredient list, grouping by component | None (if order-of-use is preserved) | Free |
| Rewriting steps in house voice; splitting/merging steps; adding a prep section | Low | Free, but don't drop warnings or cues |
| Translating language and headings | Low–medium | Use locale glossary; watch technique terms |
| Converting units within a system (tbsp → tsp) | Low | Free |
| Converting volume → weight | **Medium–high** | Use ingredient-and-form-specific density; state source convention (ATK 142 g vs. KAB 120 g per cup flour) |
| Converting regional units (AU tbsp, JP cup) | **Medium** | Must detect source locale; an error is 25% (AU tbsp) or 15% (JP cup) |
| Substituting ingredients (local equivalents) | **High** | Label as substitution; explain the difference (fat %, protein); keep original in notes |
| Scaling | **High** for baking and reductions | See section 6; warn and adjust pan/time guidance |
| Changing oven mode or pan | **Medium** | Apply conventions, widen time range, add cues |

The principle editors follow: changing the presentation of a recipe is editing; changing quantities or ingredients is *developing* a new recipe, and in a test-kitchen setting would require retesting. Since an AI assistant cannot retest, it should (a) prefer conversions with documented sources, (b) round in ways that do not drift, (c) flag uncertain conversions to the user, and (d) preserve the original quantities somewhere accessible.

### Copyright: what is and isn't protected (US)

- The **US Copyright Office's Circular 33** states: "A mere listing of ingredients or contents, or a simple set of directions, is uncopyrightable. As a result, the Office cannot register recipes consisting of a set of ingredients and a process for preparing a dish."\[58\]\[59\] Its FAQ adds that where a recipe is "accompanied by substantial literary expression in the form of an explanation or directions, or when there is a collection of recipes as in a cookbook, there may be a basis for copyright protection."\[60\]
- Courts agree. In *Publications International v. Meredith* (7th Cir. 1996), the recipes were not protected because they "contain no expressive elaboration upon either of these functional components."\[61\] In *Barbour v. Head* (S.D. Tex. 2001), the court would not rule out protection for recipes "infused with light-hearted or helpful commentary."\[62\]
- **Implication:** the ingredient list and the bare procedure are free to use; the headnote, the author's distinctive phrasing of the method, photos, and the selection and arrangement of a cookbook are protected.\[63\]\[64\] Restructuring that rewrites the method in neutral house style, drops the headnote, and uses no photos stays on the safe side in the US. Copying the original wording verbatim does not, even with credit. Other jurisdictions differ (EU originality standards, UK database rights); this report covers the US position only, and an assistant serving many countries should treat verbatim reproduction as off-limits everywhere.
- **The "three changes" rule is a myth legally.** Ostmann and Baker (as summarised by Faith Kramer on Dianne Jacob's blog) describe making three *major* changes as a rule of thumb for claiming a recipe, but note that legal ownership of recipes is "murky" and cite IACP ethical guidelines: "when in doubt give credit."\[65\] Changing three ingredients does not make copied expressive text legal, and isn't needed to use an ingredient list.\[63\]

### Attribution norms

- **The New York Times** has described three tiers: "adapted from" (most recipes, because nearly all are changed at least slightly in testing or copy-editing), "based on a recipe from" (for more dramatic changes), and acknowledgement of inspiration when a recipe only sparked an idea (as quoted by Eat Your Books, 2013).\[66\] NYT Cooking later went further and gave thousands of original recipe creators bylines alongside adapters;\[67\] according to NYT Cooking editor Emily Fleischaker, "about 20 percent of the some 20,000 recipes that appear on NYT Cooking are adapted from another source," and creators now get a "Recipe from" byline.
- **David Lebovitz's** widely cited guidance: "adapted from" when your version resembles the original; "inspired by" when strongly influenced but substantially reworked; your own only when unrecognisable — and link to the original.\[4\]\[68\]
- **Recommended practice for an assistant:** when restructuring a recipe the user supplies, keep the source attribution ("Adapted from [Title], [Author], [Book/Site]") in the output by default; never present a restructured recipe as original; do not reproduce headnotes or distinctive prose verbatim; and when the user is restructuring for personal use only, still preserve attribution metadata.

---

## 9. Readability and Accessibility

### Beginners vs. experienced cooks

The research tension here is real: Eiriksdottir and Catrambone (2011) found specific instructions help first-time performance while general instructions help learning, and that learners "typically opt for low effort."\[69\] Experienced cooks find detailed steps slow; beginners fail without them. The Ostmann and Baker–derived guide makes the same point editorially: recipes must be clear because "most readers do not have a deep knowledge of culinary technique or lingo," but the tone must not be "patronizing or condescending."\[5\]

**Ways to serve both** (convention, informed by the research):

1. **Layered detail.** A concise step, with an optional expansion: "Fold in the egg whites. *(How: cut down through the centre with a spatula, sweep along the bottom and up the side, rotate the bowl a quarter turn; repeat until no streaks remain.)*" In an app, this is a tap-to-expand. In print, technique notes or a glossary.
2. **Overview line for complex recipes** (supported by Buykx's sub-goal finding):\[70\] "This takes three stages: dough (15 min + 1 h chilling), filling (20 min), assembly and baking (45 min)."
3. **Sensory cues for everyone.** They help beginners know what "done" looks like, and let experienced cooks skip timers.
4. **Explain "why" sparingly, at the decision points** ("Rest the dough 30 minutes so the gluten relaxes and it rolls without shrinking"). Reasons help transfer and help cooks recover from deviations.
5. **Skill-level presets** in an assistant: "Concise" (experienced: fewer, denser steps, technique names) vs. "Guided" (beginner: one action per step, technique explanations inline, every cue). Both must preserve all quantities, temperatures, warnings and doneness tests.
6. **Plain wording and consistent terms.** Use one name per ingredient and per technique; avoid jargon without explanation (or explain it once in a note).

### Accessibility

- Numbered steps and short paragraphs help screen readers and help cooks find their place after looking away.
- Don't rely on colour alone for doneness ("golden") — add texture, sound, smell or temperature where possible, which also helps colour-blind cooks.
- Use real fraction characters or consistent text fractions for screen readers; avoid ambiguous abbreviations (T vs. t for tablespoon/teaspoon — Ostmann and Baker recommend spelling out units).\[5\]
- Visual recipes help some users with language impairments (an early CHI study, VERA, tested picture-based recipes with four participants with aphasia — a very small sample).\[71\]

---

## Recommendations for the AI assistant

1. **Model a recipe as structured data, not text.** For every ingredient: name (locale-mapped), quantity, unit, *form* (whole vs. chopped, packed vs. loose), prep instructions, component group, the step(s) where it's used, and the split per step. Store source unit and source locale. Render units per user preference.
2. **Detect source locale before converting.** An Australian "tablespoon," a Japanese "cup" and a US "cup" are different. If unsure, ask or flag.
3. **Convert volume to weight only with ingredient-and-form-specific densities**, and record which convention was used (e.g., "flour converted at 120 g/cup"). Prefer the source publisher's own conversions.
4. **Offer "Prep" vs. "Cook" separation as a user setting**, with the default chosen by recipe type (fast cooking → separate; slow cooking → integrated).
5. **Repeat quantities in method steps** (especially for divided ingredients), and add a one-line overview for multi-component recipes.
6. **Never scale times linearly; recompute pans by area; restate doneness cues; warn on salt, leavening and reductions** for scale factors beyond ~2x.
7. **Always store oven mode** and render both conventional and fan for metric locales.
8. **Treat substitutions as recipe changes**: mark them, explain the difference, keep the original.
9. **Preserve attribution and avoid reproducing expressive text** from sources.
10. **Enforce per-locale style**: one grammatical mood, local headings, local ingredient names, local formatting.

## Caveats

- The peer-reviewed literature on recipes specifically is small (a PhD thesis and a few workshop papers); most "rules" here are well-established editorial convention, not tested findings. Where this report says "evidence-based," it means test-kitchen measurements, regulations/standards, physics, or instructional-design research that transfers by analogy.
- Some specific figures (e.g., fan-oven offsets, grams per cup of flour) differ between authoritative sources; the report notes the conflicts rather than choosing one.
- Weight-vs-volume evidence comes from test kitchens (ATK, King Arthur, Cuisine at Home), not controlled academic studies.
- The copyright section covers US law; other countries' rules differ, and this is not legal advice.
- Spanish and Japanese conventions in section 7 are less thoroughly sourced than the German, French, Italian and English ones.

---

## References

America's Test Kitchen. (n.d.). *Flour volume to weight*. https://support.americastestkitchen.com/hc/en-us/articles/22914162910363-Flour-Volume-to-Weight

Archangel Ink. (2017). *Cookbook style guide: Adapted from The Recipe Writer's Handbook by Barbara Gibbs Ostmann and Jane L. Baker*. https://archangelink.com/wp-content/uploads/2018/10/AI_Cookbook-Style_Guide.pdf

Barbour v. Head, 178 F. Supp. 2d 758 (S.D. Tex. 2001).

BBC Good Food. (n.d.). *Conversion guides: Oven temperatures*. http://www.bbcgoodfood.com/conversion-guides

Buykx, L. (2013). *Interactive recipe instructions: Supporting cooks with better designs* [Doctoral thesis, University of York]. White Rose eTheses Online. https://etheses.whiterose.ac.uk/5158/

Buykx, L., & Petrie, H. (2012). Recipe sub-goals and graphs: An evaluation by cooks. In *Proceedings of the ACM Multimedia 2012 Workshop on Multimedia for Cooking and Eating Activities (CEA '12)* (pp. 59–64). ACM.

Chandler, P., & Sweller, J. (1991). Cognitive load theory and the format of instruction. *Cognition and Instruction, 8*(4), 293–332. https://doi.org/10.1207/s1532690xci0804_2

Cookist. (2024, April 5). *Cosa significano le abbreviazioni nelle ricette?* https://www.cookist.it/cosa-significano-le-abbreviazioni-nelle-ricette/

Cuisine at Home. (n.d.). *Step up your baking game by weighing your ingredients*. https://www.cuisineathome.com/articles/step-up-your-baking-game-by-weighing-your-ingredients/

Delia Online. (n.d.). *Oven temperatures for fan setting*. https://www.deliaonline.com/ask-lindsey/oven-temperatures-for-fan-setting

Dixon, P. (1987). The processing of organizational and component step information in written directions. *Journal of Memory and Language, 26*(1), 24–35. https://doi.org/10.1016/0749-596X(87)90060-X

Eat Your Books. (2013, February 5). *When can you claim a recipe as your own?* https://www.eatyourbooks.com/blog/2013/02/05/when-can-you-claim-a-recipe-as-your-own

Eiriksdottir, E., & Catrambone, R. (2011). Procedural instructions, principles, and examples: How to structure instructions for procedural tasks to enhance performance, learning, and transfer. *Human Factors, 53*(6), 749–770. https://doi.org/10.1177/0018720811419154

European Commission. (2008). *Commission Regulation (EC) No 589/2008 of 23 June 2008 laying down detailed rules for implementing Council Regulation (EC) No 1234/2007 as regards marketing standards for eggs*. Official Journal of the European Union, L 163.

Food Labelling Regulations 1996, SI 1996/1499, Schedule 8 (UK). https://www.legislation.gov.uk/uksi/1996/1499

Ganier, F. (2004). Factors affecting the processing of procedural instructions: Implications for document design. *IEEE Transactions on Professional Communication, 47*(1), 15–26. https://doi.org/10.1109/TPC.2004.824289

Jacob, D. (2010a). *7 most common recipe writing errors*. Will Write for Food. https://diannej.com/2010/7-most-common-recipe-writing-errors/

Jacob, D. (2010b). *Adapting a recipe doesn't make it yours*. Will Write for Food. https://diannej.com/2010/adjusting-a-recipe-doesnt-make-it-yours/

King Arthur Baking. (2019, April 23). *The essential alternative baking pan sizes*. https://www.kingarthurbaking.com/blog/2019/04/23/the-essential-alternative-baking-pan-sizes

King Arthur Baking. (2023, October 13). *How to measure flour the right way*. https://www.kingarthurbaking.com/blog/2023/10/13/how-to-measure-flour

Lebovitz, D. (n.d.). *Recipe attribution*. https://www.davidlebovitz.com/recipe-attribution/

LEO GmbH. (2020, February 4). *Der Modus in Rezepten: Man nehme…* LEO Blog. https://blog.leo.org/2020/02/04/der-modus-in-rezepten-man-nehme/

Miyajima Shoyu. (n.d.). *Instructions on the measuring spoons & measuring cups*. https://www.miyajima-soy.co.jp/english-site/en-recipes/measure

National Institute of Standards and Technology. (n.d.-a). *Metric kitchen: Cooking measurement equivalencies*. https://www.nist.gov/pml/owm/metric-kitchen-cooking-measurement-equivalencies

National Institute of Standards and Technology. (n.d.-b). *Metric kitchen: Culinary measurement tips*. https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-culinary-measurement-tips

Benham, E., Dill, K., Nguyen, T., Tehrani, A., & Bekele, L. (2026). *NIST metric recipes: Measure. Mix. Learn.* (NIST Special Publication 1290e2026). National Institute of Standards and Technology. https://www.nist.gov/publications/nist-metric-recipes-measure-mix-learn

The New York Times Company. (n.d.). *Giving recipe creators their due*. The New York Times.

Office québécois de la langue française. (n.d.). *Distinction entre l'impératif et l'infinitif*. Banque de dépannage linguistique. https://vitrinelinguistique.oqlf.gouv.qc.ca

Ostmann, B. G., & Baker, J. L. (2001). *The recipe writer's handbook* (Rev. ed.). John Wiley & Sons.

Penguin Random House Australia. (n.d.). *Conversion chart* [Bake with Brooki]. https://cdn2.penguin.com.au/content/resources/bake-with-brooki-conversions-page.pdf

Publications International, Ltd. v. Meredith Corp., 88 F.3d 473 (7th Cir. 1996).

Treccani. (n.d.). *q. b.* In *Vocabolario on line*. https://www.treccani.it/vocabolario/q-b/

U.S. Copyright Office. (2021). *Works not protected by copyright* (Circular 33). https://www.copyright.gov/circs/circ33.pdf

U.S. Copyright Office. (n.d.). *Frequently asked questions: How do I protect my recipe?* https://www.copyright.gov/help/faq/faq-protect.html

U.S. Food and Drug Administration. (1993). *Guidance for industry: Guidelines for determining metric equivalents of household measures*. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-guidelines-determining-metric-equivalents-household-measures

U.S. Food and Drug Administration. (2017). *Nutrition labeling of food*, 21 C.F.R. § 101.9. https://www.govinfo.gov/content/pkg/CFR-2017-title21-vol2/pdf/CFR-2017-title21-vol2-sec101-9.pdf

U.S. Food and Drug Administration. (n.d.). *Heavy cream*, 21 C.F.R. § 131.150.

U.S. Department of Agriculture, Agricultural Marketing Service. (n.d.). *United States standards, grades, and weight classes for shell eggs* (AMS 56).

## Quellen

1. [How to scale a recipe up or down without ruining it — Sous Chef](https://mysouschef.app/blog/how-to-scale-a-recipe/)
2. [Recipe Scaler](https://caltrx.com/everyday/recipe-scaler/)
3. [How to scale recipe servings without wrecking ratios](https://recibites.app/blog/how-to-scale-recipe-servings)
4. [Recipe Attribution](https://www.davidlebovitz.com/recipe-attribution/)
5. <https://archangelink.com/wp-content/uploads/2018/10/AI_Cookbook-Style_Guide.pdf>
6. [Trademark vs Copyright for a Recipe](https://blockchainsign.io/trademark-vs-copyright-a-recipe)
7. [Jump to ratings and reviews](https://www.goodreads.com/book/show/4833654)
8. [7 Most Common Recipe Writing Errors - Dianne Jacob, Will Write For Food](https://diannej.com/2010/7-most-common-recipe-writing-errors/)
9. [Interactive recipe instructions: supporting cooks with better designs](https://etheses.whiterose.ac.uk/id/eprint/5158/1/Lucy%20Buykx%20accepted%20thesis.pdf)
10. [(PDF) Recipe Sub-goals and Graphs: An Evaluation by Cooks](https://www.researchgate.net/publication/257758092_Recipe_Sub-goals_and_Graphs_An_Evaluation_by_Cooks)
11. [Baking 101: How To Read A Recipe - Joy the Baker](https://joythebaker.com/2013/09/baking-101-how-to-read-a-recipe/)
12. [Q. b. - Significato ed etimologia - Vocabolario - Treccani](https://www.treccani.it/vocabolario/q-b/)
13. [q.b.: Significato - Glossario di Cucina - FraGolosi](https://www.fragolosi.it/glossario/q-b/)
14. [Step Up Your Baking Game by Weighing Your Ingredients](https://www.cuisineathome.com/articles/step-up-your-baking-game-by-weighing-your-ingredients/)
15. [Metric Kitchen: Culinary Measurement Tips](https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-culinary-measurement-tips)
16. [Cooking weights and measures](https://en.wikipedia.org/wiki/Cooking_weights_and_measures)
17. [Contains Nonbinding Recommendations Food Labeling: Serving Sizes of Foods](https://www.fda.gov/media/133699/download)
18. [19 Food and Drug Administration, HHS § 101.9 Commerce for the common or usual](https://www.govinfo.gov/content/pkg/CFR-2012-title21-vol2/pdf/CFR-2012-title21-vol2-sec101-9.pdf)
19. [CONVERSION CHART](https://cdn2.penguin.com.au/content/resources/bake-with-brooki-conversions-page.pdf)
20. [Instructions on the measuring spoons & measuring cups](https://www.miyajima-soy.co.jp/english-site/en-recipes/measure)
21. [Why Is a Japanese Rice Cup 180 mL? Rice Cooker Cup vs US Cup](https://japanese-food-faq.com/articles/why-japanese-rice-cups-are-180-ml/)
22. [Cup Sizes Around the World: US, Metric, and Imperial](https://gramstocupsconverter.net/blog/cup-sizes-around-the-world/)
23. [Cooking Measurement Converter: Cups, Tbsp, tsp & mL](https://4calculators.com/calculators/cooking-measurement-conversion-calculator/)
24. [Egg Size Converter: US, UK & EU Baking Conversions](https://starlighttools.org/cooking/egg-size-conversion-calculator)
25. [Egg Weight, Egg Sizes & Types of Eggs: Complete USDA & Culinary Guide](https://egg.foodnutrify.com/nutrition/egg-sizes-and-weights)
26. [Egg Size Chart by Weight: Grams, Ounces & Baking Swaps](https://chickencalc.com/egg-size-calculator)
27. [The processing of organizational and component step information in written directions - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0749596X8790060X)
28. [(PDF) Factors Affecting the Processing of Procedural Instructions: Implications for Document Design](https://www.academia.edu/48588648/Factors_Affecting_the_Processing_of_Procedural_Instructions_Implications_for_Document_Design)
29. [(PDF) Factors Affecting the Processing of Procedural Instructions: Implications for Document Design](https://www.researchgate.net/publication/3230319_Factors_Affecting_the_Processing_of_Procedural_Instructions_Implications_for_Document_Design)
30. [Procedural Instructions, Principles, and Examples - Elsa Eiriksdottir, Richard Catrambone, 2011](https://journals.sagepub.com/doi/abs/10.1177/0018720811419154)
31. [Full article: Shall we teach students to skip steps? Designing optimal instructions from a cognitive load perspective](https://www.tandfonline.com/doi/full/10.1080/0020739X.2026.2633245)
32. [Useful measurements](http://pinkblocks.com/useful-measurements)
33. [Oven Temperature Conversion Calculator](https://fastcalc.us/cooking/oven-temperature-conversion/)
34. [Gas mark](https://en.wikipedia.org/wiki/Gas_mark)
35. [Oven Temperature Converter — °F, °C, Gas Mark & Fan](https://induwara.lk/tools/oven-temperature-converter)
36. [Gas Mark Conversion Chart: °C, Fan and °F - RightSums](https://rightsums.com/oven-temperature)
37. [Oven temperatures for fan setting](https://www.deliaonline.com/ask-lindsey/oven-temperatures-for-fan-setting)
38. [Gas Mark — Glossary](https://convertitive.com/glossary/gas-mark/)
39. [The essential alternative baking pan sizes](https://www.kingarthurbaking.com/blog/2019/04/23/the-essential-alternative-baking-pan-sizes)
40. [The Baker's Calculator — Pan Converter, Recipe Scaler & More](https://thebakerscalculator.com/)
41. [The Ultimate King Arthur Baking Conversion Guide: Perfecting Your Recipes 2026](https://bakingstarter.com/king-arthur-baking-conversion-chart/)
42. [How to Scale a Recipe Up or Down for Any Crowd Size - Shop Choice Foods - Healthy diet tips and suggestions?](https://shopchoicefoods.com/2026/07/12/how-to-scale-a-recipe-up-or-down-for-any-crowd-size/)
43. [How to Scale a Recipe: Complete Guide with Calculator](https://ingredientcalculator.com/how-to-scale-recipes)
44. [How to Scale a Recipe — Doubling, Halving, and Adjusting Servings - Basic Free Tools](https://basicfreetools.com/blog/how-to-scale-a-recipe/)
45. [How to Scale a Recipe for More or Fewer Servings](https://tastysave.app/guides/how-to-scale-a-recipe)
46. [Baking Dish and Pan Size Conversions](https://whatscookingamerica.net/q-a/bakingdish.htm)
47. [How to Double or Halve a Recipe (Without It Going Wrong)](https://cooklang.org/blog/26-how-to-scale-recipes-without-mistakes/)
48. [How to Scale a Recipe Up or Down (Without Ruining It)](https://kordu.tools/blog/how-to-scale-recipe-up-or-down/)
49. [Recipe Scaler](https://frukal.com/calculators/recipe-scaler)
50. [Der Modus in Rezepten](https://blog.leo.org/2020/02/04/der-modus-in-rezepten-man-nehme/)
51. [Imperativ (Modus)](<https://de.m.wikipedia.org/wiki/Imperativ_(Modus)>)
52. [Distinction entre l’impératif et l’infinitif](https://vitrinelinguistique.oqlf.gouv.qc.ca/24208/la-grammaire/le-verbe/modes/imperatif/distinction-entre-limperatif-et-linfinitif)
53. [Cream in Cocktails: Single vs Double, Floats and Curdling](https://jerrycanspirits.co.uk/field-manual/ingredients/cream/)
54. [Heavy Cream vs Whipping Cream vs Double](https://lux-gas.com/blogs/product-education-buyer-guides/heavy-cream-vs-whipping-cream-vs-double-cream)
55. [US vs UK Cream Types Converter - Heavy Cream, Double Cream & More](https://www.bakingscalepro.com/converter/cream-types-converter)
56. [Australian Cooking Measurements](https://recipeland.com/how-to/australian-cooking-measurements)
57. [Cosa significano le abbreviazioni nelle ricette?](https://www.cookist.it/cosa-significano-le-abbreviazioni-nelle-ricette/)
58. [Circular 33 Works Not Protected by Copyright](https://upload.wikimedia.org/wikipedia/commons/d/d9/U.S._Copyright_Office_circular_33.pdf)
59. [Ingredients lists are not copyrightable. The text and photos around them can be ...](https://news.ycombinator.com/item?id=25358996)
60. [Can You Copyright Recipes? Whats Cooking America](https://whatscookingamerica.net/q-a/cookbookadvice.htm)
61. [Copyright in Recipes! Well Done or Half-Baked? |](https://copyright.nova.edu/copyright-in-recipes/)
62. [Mixing Things Up: Let’s Talk Recipes, Part One of a Four-Part Series on Copyright](https://natlawreview.com/article/mixing-things-let-s-talk-recipes-part-one-four-part-series-copyright)
63. [Can Recipes Be Copyrighted? Everything to Know](https://abounaja.com/blog/can-recipes-be-copyrighted)
64. [websites.umass.edu](https://websites.umass.edu/copyright/copyright-basics/copyrightability)
65. [Adapting a Recipe Doesn't Make it Yours - Dianne Jacob, Will Write For Food](https://diannej.com/2010/adjusting-a-recipe-doesnt-make-it-yours/)
66. [When can you claim a recipe as your own?](https://www.eatyourbooks.com/blog/2013/02/05/when-can-you-claim-a-recipe-as-your-own)
67. [Cooks Without Borders](https://cookswithoutborders.substack.com/p/the-recipe-fair-use-no-ones-discussing)
68. [How to Correctly Attribute a Recipe - Bootstrapped Ventures](https://bootstrapped.ventures/recipe-attribution/)
69. [Procedural Instructions, Principles, and Examples](https://www.deepdyve.com/lp/sage/procedural-instructions-principles-and-examples-JVqOP6xxvN?key=sage)
70. [(PDF) Interactive recipe instructions: supporting cooks with better designs - Thesis abstract](https://www.academia.edu/4774310/Interactive_recipe_instructions_supporting_cooks_with_better_designs_Thesis_abstract)
71. [A Visual Recipe Book for Persons with Language Impairments](https://www.cs.ubc.ca/~joanna/papers/CHI2005_Tee.pdf)
