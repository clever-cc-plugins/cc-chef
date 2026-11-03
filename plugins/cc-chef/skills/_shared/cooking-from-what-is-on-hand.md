# Cooking from what is on hand

Use this file when the user starts from a mood, a list of ingredients or a photo of a fridge or pantry instead of a named dish: `create-recipe` loads it to rank the ingredients by urgency, choose a dish template, fill its slots, assume a minimal pantry, swap ingredients by function and offer three clearly different options. Section 1 gives the workflow, section 2 perishability, section 3 pantry assumptions, section 4 the dish templates, section 5 the seasoning layer, section 6 substitutions, section 7 photo handling, section 8 option presentation, section 9 evidence notes. Leftover storage limits, reheating rules and high-risk foods live in `food-safety.md`, not here.

Conventions: `(to verify)` marks a claim that only one research report made. "Default" is what the plugin does when reports disagree. Evidence tags: official = authority guidance; empirical = studies or benchmarks; practitioner = cookbook and test-kitchen heuristics; design = a rule chosen for this plugin.

## 1. Workflow

| Step | Do                                                                                         | Notes                                                                            |
| ---- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 1    | Take the input: mood, typed list, or photo                                                 | A photo becomes a draft inventory first (section 7)                              |
| 2    | Build the inventory with identity, amount, state (raw, cooked, opened) and age where known | Ask only about what changes the decision                                         |
| 3    | Rank by urgency: safety-critical tier first, then quality tier (section 2)                 | Exclude anything with an unknown or unsafe history rather than "rescuing" it     |
| 4    | Screen against the registered diet, allergens and life-stage rules                         | A dish that breaks a registered rule is never offered, or is adapted and says so |
| 5    | Pick templates that can absorb a meaningful amount of the urgent items (section 4)         | Two leaves of spinach in a dish do not count as "used"                           |
| 6    | Fill the slots, close the seasoning layer (section 5), list pantry assumptions (section 3) | Items that cannot be filled become "to buy"                                      |
| 7    | Present 3 different options (section 8)                                                    | Write the full recipe only after the user picks                                  |

Ranking order when options compete (design): safety and diet fit; amount of urgent food consumed; time and equipment fit; number of items to buy; flavour coherence; total inventory used. It is acceptable to leave an ingredient unused when the dish is better without it.

Mood input ("something warm", "light", "quick") narrows the template choice: warm and comforting leans to soup, stew, curry, gratin, hash; light and fresh to salad, grain bowl, quick stir-fry; quick to egg bakes, fried rice, pasta, stir-fry, savoury pancake. If the inventory supports very different directions, ask one optional question about warm versus fresh, never a questionnaire.

## 2. Perishability tiers

Keep two separate judgements: whether an item is eligible at all (safety) and, among eligible items, which to use first (quality and waste). Appearance never certifies safety; do not use the sniff test as a safety check, because the bacteria that cause food poisoning cannot be smelled.

| Tier                                    | Items                                                                                                                                                                           | Handling                                                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| A. Safety-critical, use or freeze first | Raw poultry, fish and shellfish, minced meat, offal; cooked rice and other cooked starches; cooked leftovers near their limit; opened ready-to-eat items near their use-by date | Ask for date, storage and cooking history; if unknown, leave the item out; limits are in `food-safety.md` |
| B. Quality falls quickly                | Soft herbs, spinach and salad leaves, berries, mushrooms, bean sprouts, cut fruit, opened cream, soft fresh cheese, opened tofu                                                 | Give them the main slot, not the garnish; prefer templates that forgive tired texture                     |
| C. Medium                               | Peppers, courgette, broccoli, cucumber, opened milk and yoghurt, cooked leftovers within their window, whole cuts of meat                                                       | Plan within about a week                                                                                  |
| D. Low                                  | Roots, onions, winter squash, hard cheese, cured meat, eggs, condiments, dry goods, frozen items                                                                                | Use as supporting ingredients; they must not crowd out tiers A and B                                      |

Tier boundaries differ slightly between reports: the one-to-two-day band for fish is shared, but two reports place ground meat in the "use first" band and one places it a step later (default: ground meat is tier A). Eggs sit in tier C or D depending on the report (default: tier D, unless cracked or cooked). Mushrooms and tofu are tier B in two reports and "use soon" in one (default: tier B once opened or cut).

Condition cues that choose the technique, not the safety verdict:

| Cue                                                        | Use                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Wilted herbs or leaves                                     | Cook them: soup, curry, frittata, fried rice, sauce; not raw salad                    |
| Soft, wrinkled peppers or courgette                        | Roast, braise, stir-fry, soup                                                         |
| Limp roots                                                 | Soup, hash, gratin                                                                    |
| Sprouting or green potatoes                                | Cut away sprouts and green or rotten parts, discard if heavily affected               |
| Mould                                                      | Soft foods are discarded; firm foods may be trimmed only if the local guidance allows |
| Slime, off odour, swollen packs, unexplained colour change | Safety advice, not a rescue recipe                                                    |

Date labels: "use by" is a safety date, "best before" a quality date that is not a hard stop. Opened items need the opening date; "bought Tuesday" says nothing about remaining life. Store `opened_at`, `cooked_at` and storage place separately in the inventory. When leftovers turn into a new dish, the original cooking and storage timeline travels with them; reheating is not a reset. For any safety rule see `food-safety.md`.

Framing: users rarely see themselves as wasting food, so present suggestions as saving money and time, not as waste reduction. Concrete, timely prompts ("the chicken is on day two, here are three dishes") fit the evidence on what works better than generic awareness messages.

## 3. Pantry assumptions

Nothing in the reports measured what households in each country really own, so regional defaults are a starting point to confirm, never a fact. The user's registered pantry (if any) overrides everything below; learn from each confirmation, and do not treat nationality or interface language as proof of ownership.

| Tier                              | Items                                                                                                                       | Treatment                                                                                     |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 0, assume silently                | Water, salt, a cooking fat                                                                                                  | Name them in the "assumes" line anyway so a correction is easy                                |
| 1, assume and list                | Black pepper, sugar, one acid (vinegar or lemon), flour or starch, stock cube, onion, garlic                                | Show under "assumes"; onion and garlic are perishable, so confirm when a dish depends on them |
| 2, regional defaults to ask about | See table below                                                                                                             | Offer, confirm, or give a fallback                                                            |
| 3, cuisine-specific, never assume | Fish sauce, miso, tahini, curry paste, garam masala, sumac, tamarind, coconut milk, specialty flours, crème fraîche, paneer | Ask, make optional, or pick another template                                                  |

| Region or cuisine                          | Defaults to offer and confirm                                                                                                             |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Western and Northern Europe, North America | Butter, olive or neutral oil, mustard, paprika, dried thyme or oregano, tinned tomatoes, pasta, rice                                      |
| Mediterranean, Middle East                 | Olive oil, lemons, cumin, sumac, dried mint, bulgur, chickpeas, tahini                                                                    |
| South Asia                                 | Neutral oil or ghee, mustard and cumin seeds, turmeric, chilli powder, garam masala, lentils, atta, rice                                  |
| East Asia                                  | Soy sauce, rice vinegar, sesame oil, ginger, spring onion, rice; add gochujang or doenjang for Korea, and miso, mirin and dashi for Japan |
| Southeast Asia                             | Fish sauce, limes, palm sugar, chilli, rice, coconut milk                                                                                 |
| Latin America                              | Cumin, dried chillies, oregano, limes, beans, masa or tortillas, rice                                                                     |

Ask, assume or offer a fallback (design):

| Situation                                                            | Action                       |
| -------------------------------------------------------------------- | ---------------------------- |
| The answer changes safety, diet, structure or the top recommendation | Ask                          |
| Wrong guess is cheap and easy to correct                             | Assume and state it          |
| Several items can do the same job                                    | Offer the alternative inline |
| A structural item is missing and nothing reliable replaces it        | Choose another template      |

Keep three lists separate on every option: required, assumed, optional. An optional garnish never becomes a mandatory purchase, and "just pantry staples" followed by nine unconfirmed condiments is a failure.

Fallbacks for flavour-defining staples: no fish sauce, use soy sauce with a pinch of sugar; no fresh ginger, ground ginger at about a quarter of the amount (practitioner); no soy sauce, salt with a splash of vinegar (the weakest option, say so); no fresh garlic, garlic powder at roughly one clove to an eighth of a teaspoon, added to liquid rather than hot oil.

## 4. Dish templates

A template is a set of slots plus constraints. Fill the slots from the inventory, giving urgent items the main role; unfilled slots become "to buy"; prefer templates whose gaps are pantry staples. Ratios are starting points: state the assumption (cooked and drained vegetables, cooled rice) and adjust to the ingredients.

| #   | Template                                            | Slots                                                | Base ratio or rule                                                                                                               | Absorbs well                                                  | Constraint that prevents failure                                                                                       |
| --- | --------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | Egg-bound bake (frittata, tortilla, omelette, kuku) | Egg, fat, fillings, sharp element                    | About 6 eggs to 120 ml dairy; roughly 1 egg per 50-80 g filling (practitioner); a custard runs about 2 liquid to 1 egg           | Cooked veg, potato, cheese, cured meat, herbs, leftover pasta | Pre-cook and drain watery veg (mushroom, courgette, spinach); salt the eggs; do not drown the egg                      |
| 2   | Stir-fry                                            | Fat, aromatics, protein, veg, sauce                  | Sauce about 3 savoury liquid to 1 sour or sweet; slurry of equal parts starch and water if thickening (single report, to verify) | Firm and soft veg, thin protein, tofu, mushrooms              | Small batches, dry surface, similar cuts, add by cooking time; crowding steams                                         |
| 3   | Fried rice                                          | Cold rice, fat, egg, aromatics, additions, seasoning | Additions are accents, rice is the bulk                                                                                          | Diced veg, cooked protein, kimchi, peas                       | Cooled day-old rice; confirm its history first (see `food-safety.md`)                                                  |
| 4   | Soup                                                | Aromatic base, liquid, bulk, body, finish            | About 1 part solids to 3 parts liquid (two reports, rough)                                                                       | Almost anything, rinds, wilted greens, legumes                | Sweat aromatics, season in layers, acid or herbs at the end; starch for body in purées                                 |
| 5   | Stew or braise                                      | Browned main, aromatics, liquid, acid                | Liquid partly covers; long low heat                                                                                              | Tough cuts, roots, legumes, tomato                            | Brown first, deglaze, lean cuts dry out; quick bean stews are a different, short template                              |
| 6   | Curry                                               | Fat, aromatic or spice base, liquid, main, balance   | Bloom spices in fat before liquid                                                                                                | Veg, pulses, paneer, tofu, chicken, fish, eggs                | Sour, sweet and salt in balance; dairy or coconut late to avoid splitting; name the direction (tomato-lentil, coconut) |
| 7   | Pasta                                               | Pasta, sauce family, starchy water, umami, lift      | Finish the pasta in the sauce with a ladle of cooking water                                                                      | Veg, cured meat, canned fish, cheese, nuts, herbs             | One sauce family (oil, tomato, cream, broth); rich salty extras count as seasoning                                     |
| 8   | Grain bowl (donburi, bibimbap)                      | Grain, protein, veg, sauce, crunch                   | Roughly 1 cup cooked grain, 1/2 cup veg, 80-90 g protein, 2-3 tbsp dressing (single report, to verify)                           | Raw, roasted, pickled veg, eggs, pulses                       | A strong dressing links parts; mix textures and temperatures                                                           |
| 9   | Savoury pancake or fritter                          | Batter or binder, mix-ins, fat, dip                  | About equal flour and liquid by weight plus an egg, 2-3 parts shredded solids (single report, to verify)                         | Cabbage, spring onion, courgette, kimchi, cooked fish         | Squeeze out water, hot oiled pan; chickpea-flour batters are their own dish                                            |
| 10  | Hash                                                | Cooked starch, fat, onion, extras                    | Equal parts diced base                                                                                                           | Roast potato, roots, cooked meat                              | Dry components, one layer, leave it alone to crisp; sauce turns it into a sauté                                        |
| 11  | Gratin or bake                                      | Starch or veg, binding sauce, topping                | Thin even slices; sauce well seasoned                                                                                            | Roots, squash, cooked pasta, greens, cheese ends              | Pre-cook dense items; cheese cannot rescue a watery filling; brown top needs fat and starch or cheese                  |
| 12  | Tart, pie, quiche, börek                            | Pastry, filling, binder                              | Short pastry about 3 flour : 2 fat : 1 water; custard as in row 1                                                                | Cheese, veg, cooked meat, greens                              | Pre-cook and drain filling; blind-bake for wet fillings; bought pastry cuts time                                       |
| 13  | Composed salad (fattoush, panzanella, slaw)         | Base, dressing, crunch, protein                      | Vinaigrette starts near 3 oil : 1 acid; adjust to the acid                                                                       | Raw veg, stale bread, grains, fruit, nuts                     | Dress lightly, salt wet parts separately; tired veg does not suit raw salad                                            |

Fridge-clearing favourites, because they take the widest range with the fewest purchases: egg bake, fried rice, stir-fry, soup, grain bowl. Greens in bulk go to soup, curry, börek filling or pancake; a handful goes into fried rice or an egg bake.

Pick a template by what the urgent item needs: delicate and wilting means cooked-soft formats (soup, curry, egg bake); crisp and firm means stir-fry, salad or roast bowls; a large amount means soup, pancake, pie filling or curry.

## 5. Seasoning and balancing layer

Run this checklist on every filled template before presenting it. A dish that fails a line gets the missing item added or an honest note that it will taste flat without it.

| Check             | Question                                                                            | Typical fix                                                                 |
| ----------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Salt              | Is there a salt source, counting stock, soy, cheese and cured meat already present? | Season in stages; final adjustment after assembly                           |
| Fat               | Is there a fat that carries flavour, and is the aromatic cooked in it?              | Cook aromatics and spices in the fat; finish with an aromatic oil or butter |
| Acid              | Is there something sharp, at the right moment?                                      | Lemon, vinegar, tomato, yoghurt, pickles, tamarind at the end               |
| Aromatic          | Onion family, ginger, garlic, spices or herbs?                                      | Bloom spices in fat, soft herbs last                                        |
| Umami             | A savoury depth source that fits the dish?                                          | Tomato paste, mushroom, aged cheese, soy, fish sauce, miso, anchovy         |
| Heat or sweetness | Needed only to balance?                                                             | Make chilli optional; a pinch of sugar rounds acid or bitterness            |
| Texture           | Is there contrast (crunch against soft)?                                            | Toasted nuts or seeds, crisp onion, fresh veg added at the bowl             |
| One direction     | One identifiable flavour direction and one finishing contrast?                      | Pick ginger-soy, or cumin-lemon, not both; drop extras that do not do a job |

Dish-specific points: salt eggs before cooking; salt the greens directly before dressing; season gratin layers and the sauce; add dairy or coconut late in curry; an acid finish lifts soups and stews. For deeper craft rules see `culinary-craft.md`.

## 6. Substitutions by function

Ask what the ingredient does in this dish, then check whether the replacement does the same job. Savoury stovetop dishes (stir-fry, soup, stew, curry, pasta) tolerate swaps because flavour and bulk dominate; baking, emulsions and set custards are chemical and structural, so be conservative there and say when a swap changes the dish rather than imitates it.

### 6.1 Function table

| Function    | What must be kept                                  | Common mistake                                                       | Fails in                                                          |
| ----------- | -------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Structure   | A matrix that holds shape or traps gas             | Swapping for something that adds only moisture                       | Baking, set custards, quiche, frittata                            |
| Moisture    | Total water and where it sits                      | Matching volume without regard to absorption                         | Batters, doughs, gratin                                           |
| Fat         | Tenderness, richness, sometimes aeration or layers | Treating oil and solid fat as identical                              | Creamed cakes, laminated or flaky pastry, shortbread, buttercream |
| Leavening   | Gas made, and the acid or base that makes it       | Dropping buttermilk or yoghurt without adjusting the soda            | Cakes, quick breads, pancakes                                     |
| Binding     | Cohesion, not always setting                       | Assuming every binder sets when heated                               | Meatballs rely on it mildly; omelettes and custards fully         |
| Emulsifying | Stable fat-in-water mix                            | Fixing thickness only                                                | Mayonnaise, vinaigrette, cream sauces, hollandaise                |
| Acid        | Taste, sometimes setting or leavening              | Using seasoning swaps where the formula or a preserve needs the acid | Pickles and preserves (never improvise), soda-leavened batters    |
| Sweetness   | Bulk, water holding, browning, not only taste      | Matching sweetness only                                              | Meringue, creamed cookies, cakes                                  |
| Flavour     | Aroma and savouriness                              | Calling look-alikes identical                                        | Raw finishing herbs, long-simmered bases                          |

### 6.2 Ingredient swaps and what changes

| Original              | Replacement                                                               | Preparation change                                                                                                                                             | Fails in                                                                                          |
| --------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Butter                | Oil                                                                       | Savoury cooking: swap freely; use oil for high heat, butter or ghee for flavour. Baking: about three-quarters of the amount, denser moister crumb, no creaming | Flaky pastry, shortbread, creamed batters                                                         |
| Butter                | Ghee                                                                      | Higher smoke point, good for searing and tempering                                                                                                             | Less browning in baking                                                                           |
| Cream                 | Milk                                                                      | Fat under about 30 percent can curdle with acid at a boil; add off heat or stabilise with a little starch                                                      | Reduction sauces, hot acidic sauces                                                               |
| Cream or milk         | Plant drink                                                               | Soy is closest in protein; oat thickens and sweetens; almond and rice are thin; use unsweetened for savoury                                                    | Set custards, reduction sauces, béchamel with coconut                                             |
| Buttermilk or yoghurt | Milk                                                                      | Add lemon or vinegar, or switch soda to baking powder                                                                                                          | Soda-leavened bakes                                                                               |
| Egg (binding)         | Flax or chia gel (1 tbsp ground seed + about 3 tbsp water), starch slurry | Rest the gel; expect a denser result                                                                                                                           | Anything that must set                                                                            |
| Egg (foam)            | Aquafaba, about 3 tbsp per egg                                            | Less stable than egg white; fat and acid hurt the foam                                                                                                         | Delicate sponges                                                                                  |
| Egg (set)             | None reliable                                                             | Use a different dish (chickpea-flour pancake) instead of calling it a frittata                                                                                 | Custard, quiche, frittata, soufflé                                                                |
| White flour           | Whole wheat                                                               | Absorbs more water, slower; start with up to half whole wheat; rest 20-30 minutes; add liquid gradually                                                        | Delicate cakes                                                                                    |
| Wheat flour           | Gluten-free blend                                                         | Use a blend and a recipe made for it; hydration and a binder (xanthan or psyllium) matter together                                                             | Yeast bread, laminated dough, roux                                                                |
| Wheat flour           | Coconut or almond flour                                                   | Not 1:1; tested recipe only                                                                                                                                    | Any 1:1 swap                                                                                      |
| Sugar                 | Honey or syrup                                                            | Adds water: cut other liquid, lower the oven by about 15 C, expect faster browning                                                                             | Crisp or creamed bakes                                                                            |
| Sugar                 | Intense sweetener                                                         | Loses bulk and browning                                                                                                                                        | Meringue, cookies, cakes                                                                          |
| Lemon, lime, vinegar  | One another                                                               | Adjust to strength; rice vinegar is mild, malt is loud; tamarind, sumac, tomato, yoghurt belong to different traditions                                        | Preserves, pickles                                                                                |
| Meat                  | Beans, lentils, mushrooms, tofu                                           | Change timing and sequence, not just the name; add fat and umami; do not copy raw-meat steps to cooked legumes                                                 | Dry-heat roasts, dishes built on meat texture                                                     |
| Lean cut              | Fatty cut (or reverse)                                                    | Match cooking time class: thigh and shoulder in braises, quick fish or prawns in quick curries                                                                 | Lean cuts in long braises; delicate fish in long stews                                            |
| Onion                 | Shallot, leek, spring onion                                               | Shallot sweeter, leek milder and needs more time, spring onion for freshness                                                                                   | Spring-onion white for caramelised onion                                                          |
| Fresh garlic          | Powder                                                                    | Burns in hot oil; add to liquid                                                                                                                                | Raw preparations                                                                                  |
| Fresh herbs           | Dried                                                                     | Roughly 1 part dried to 3 fresh for hardy herbs, added early                                                                                                   | Soft herbs (basil, coriander, parsley, dill, mint) as a raw or finishing herb; pesto, salsa verde |
| Whole spice           | Ground spice                                                              | Rethink when to add; bloom ground spice briefly in fat, do not add to cold liquid                                                                              | Tadka-style dishes                                                                                |
| Spice blend           | Single spice                                                              | Check the blend for salt, heat, allergens                                                                                                                      | Dishes built on that blend                                                                        |

### 6.3 Rules to apply

- Each substitution is recorded as: original, role, replacement, quantity rule, water change, method change, taste change, diet and allergen change, confidence.
- Confidence has three levels: tested in this recipe, tested in a similar use, untested suggestion (design).
- Run the allergen check again after every swap: almond flour for wheat, soy milk for dairy, and tahini or sesame oil for peanut each introduce a common allergen. Lactose-free is not milk-allergy-safe.
- A name must not promise the original texture once the structure changed: "chickpea-flour pancake", not "vegan frittata".
- Acid in preserves, pickles and fermentation is a safety control, not seasoning; no improvised swaps. Do not cut salt casually in cures, brines and ferments.
- Lower-sugar, lower-salt and lower-saturated-fat baking: reduce modestly (about 10 percent sugar is a test-kitchen start); beyond that expect texture and keeping losses. For savoury dishes lean on acid, aromatics and umami and count salty condiments.
- Vegetarian: check hidden animal products in fish sauce, Worcestershire, gelatin, stock and some cheeses.

## 7. Photo handling

A photo of a fridge, pantry or counter is a source of candidate items, not an inventory. The plugin never plans from a photo alone: it drafts a list, the user corrects it, and only the corrected list feeds section 1. Nothing in an image establishes quantity, storage history or safety.

### 7.1 What image recognition can and cannot do

| Task                                                                                                                                             | Reliability                                                                                                                          | Consequence                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Naming common, clearly visible items (eggs, lemons, peppers, carrots, milk cartons, bottled condiments)                                          | Good when items are isolated and well lit; reports measured this mostly on dish photos and single products, not on cluttered shelves | Offer these as the draft list                                              |
| Look-alikes (parsley and coriander, spring onion and leek, cream and yoghurt in an unmarked tub, white miso and tahini, cooked chicken and tofu) | Weak; models get the category right and the exact item wrong                                                                         | Name the two candidates and ask                                            |
| Packaged goods, jars, foil, opaque tubs                                                                                                          | Weak; contents are not visible and labels are often unreadable in fridge light                                                       | Ask for a label close-up or a typed answer                                 |
| Hidden items (behind other items, in drawers, on the door at an angle)                                                                           | Not seen at all                                                                                                                      | Say "items I can see", never "everything you have"                         |
| Quantity and weight                                                                                                                              | Poor; scale and depth are ambiguous and error grows with the number of items                                                         | Ask, or record a count only for clearly separate items such as eggs        |
| Ripeness, freshness, spoilage                                                                                                                    | Unreliable; accuracy fell well below human raters even on single-fruit images                                                        | Condition is asked, never judged                                           |
| Prepared mixtures and leftovers                                                                                                                  | Contents and age unknowable                                                                                                          | Ask what it is and when it was cooked                                      |
| Regional products and local names                                                                                                                | Uneven coverage                                                                                                                      | Accept the user's name for an item rather than forcing a familiar category |

The evidence behind this table is thin for the exact use case. No report found a peer-reviewed benchmark of current multimodal models on real fridge or pantry photos; the figures come from dish images, single-item images, cooking videos and a few preprints. One practitioner test of consumer fridge-scanning apps reported roughly 88-92 percent accuracy on a tidy, well-lit pantry and 65-75 percent in a crowded fridge (single report, practitioner, to verify). Treat the direction as reliable and any percentage as illustrative. Naming is the strong part; quantity, state and condition are separate and weaker tasks, and correct names do not repair bad quantity estimates.

### 7.2 Draft inventory

Show the draft before suggesting anything. Group it by how sure the plugin is, using words, not percentages: numeric confidence scores are not shown unless they have been calibrated on this very task (default; one report proposed fixed numeric thresholds, which the plugin does not adopt because nobody has calibrated them).

| Group       | Meaning                                                | Example wording                                        |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------ |
| Confirmed   | The user said it, or it is unmistakable and low-stakes | "Eggs, a bag of spinach, a block of cheddar"           |
| Likely      | Plausible reading with a named alternative             | "A white tub, probably yoghurt (or sour cream?)"       |
| Unsure      | Cannot tell                                            | "Two containers on the bottom shelf, what is in them?" |
| Not visible | Known gap                                              | "Crisper drawer and door shelves are hidden"           |

Per item, keep the fields separate rather than collapsing them into "detected, fine, 250 g":

| Field                               | Filled from the photo?          | Typical entry                          |
| ----------------------------------- | ------------------------------- | -------------------------------------- |
| Identity                            | Yes, with a confidence group    | "Probably spring onions"               |
| Visible count                       | Only for clearly separate items | "Two eggs visible"                     |
| Usable amount                       | No                              | "Unknown, ask"                         |
| State (raw, cooked, opened, frozen) | Rarely                          | "Cooked or raw, unclear"               |
| Visible condition                   | Only as a prompt                | "Some leaves look limp, how are they?" |
| Safety status                       | Never                           | "Not assessable from an image"         |

### 7.3 Confirmation before planning

1. Present the draft list and ask the user to confirm, correct, add or delete items. A short scan-and-correct pass still beats typing the whole list.
2. Ask about quantities only for items that will be a main ingredient, and in household terms ("about how many eggs?", "a handful or a whole bag?"). Rough amounts are enough.
3. Ask about condition and history only where it changes the decision: key perishables ("is the spinach still crisp or wilted?") and tier A items in section 2 ("when was the rice cooked and was it chilled promptly?").
4. Do not interrogate the user about condiments, dry goods or items the likely dishes will not touch.
5. Ask for one more photo or a label close-up only when a hidden or ambiguous item affects the options; a second angle helps more than further repeats, and typed corrections beat re-photographing. A photo per shelf or drawer works better than one wide shot.
6. Store the confirmed result as the inventory, with confirmed amounts and states, and update it from later confirmations and cooking events instead of re-reading old photos. One report found that structured food-state memory improved a small model's scores on a cooking-video benchmark (single report, to verify); the design argument for a persistent inventory does not depend on that figure.
7. Record that a quantity came from the user's estimate, so later steps do not treat it as measured.

### 7.4 Boundaries

- No spoilage, freshness or safety judgement from an image, in either direction. A normal-looking item is not certified safe and a dull-looking one is not condemned. Phrase observations as prompts ("check the use-by date on the chicken"), never verdicts.
- Visible mould, slime, swollen packaging or a sour smell the user reports lead to the safety advice in section 2 and `food-safety.md`, not to a rescue recipe.
- Allergens and diet suitability are not read from a photo. Packaged goods need the label; cross-contact is invisible. Diet and allergen screening in section 1 step 4 runs on the confirmed list.
- If the user declines to confirm, plan only from the items they confirmed or typed, and say which items were left out.

Sample opening message: "I spot eggs, mushrooms, spring onions and something like spinach. The white tub: is that yoghurt? Roughly how much spinach is there, and is it still fresh? I also see cooked rice: when was it cooked, and did it go into the fridge soon after?"

## 8. Option presentation

Present options only after the inventory is confirmed (section 7) and screened against diet, allergens and life stage (section 1 step 4). The first response helps the user choose a direction; the full recipe comes after the pick.

### 8.1 How many

| Situation                                       | Offer                                                                           |
| ----------------------------------------------- | ------------------------------------------------------------------------------- |
| Default                                         | 3 options                                                                       |
| User asks for more, or says nothing fits        | Up to 5, shown as an extension of the first 3, never as a wall of ideas         |
| "I am tired, just decide"                       | One clear recommendation plus two brief alternatives                            |
| Clear craving or format ("something with eggs") | 2 or 3 closely relevant options                                                 |
| Tight inventory or tight constraints            | Only the feasible options; do not invent a third                                |
| Rich inventory, unclear preferences             | One optional question (warm or fresh), or three deliberately contrasting dishes |

Why 3 (design): choice-overload research shows no universal optimum. Averaged over many studies the effect is close to zero; it appears when the choice set is complex, the task is hard, preferences are unclear or the person wants to minimise effort, and a fridge-clearing request has all four. Menu studies that found about 6 for quick service and 7-10 for fine dining measured menus the person scans, not dishes the person must evaluate. Three is a practitioner convention, not a measured optimum (three reports said 3 outright, four said 3-5; default 3, 5 on request).

### 8.2 Make the options truly distinct

Options differ in shape first, flavour second. Three stir-fries with different vegetables are one option.

| Axis                    | Examples of spread                                                            |
| ----------------------- | ----------------------------------------------------------------------------- |
| Template (section 4)    | Egg bake, soup, grain bowl; never two from the same row unless the user asked |
| Effort and equipment    | One pan on the hob; hands-off oven dish; cold or no-cook assembly             |
| Time                    | One under about 20 minutes, one slower and more comforting                    |
| Flavour direction       | Different cuisines or clearly different seasoning layers (section 5)          |
| Role of the urgent item | Main ingredient in each option, not a garnish in one                          |

A useful default trio, when the inventory allows it: a quick low-effort option; the option that uses the most tier A and B items; one more comforting or more adventurous option for a user with time. Label each with its archetype so the choice reads as a trade-off ("quickest", "uses the most", "most comforting"). If no template can honestly absorb a tier A or B item, say so rather than forcing it into the list.

### 8.3 Card format

Use the same fields in the same order for every option so the comparison becomes a grid.

| Field         | Content                                                                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name and hook | Familiar dish name plus one line on taste and texture ("crisp-edged, sharp and herby")                                                               |
| Template      | Named in plain words ("frittata-style") so the user can predict the format                                                                           |
| Time          | Total, and active time when they differ                                                                                                              |
| Uses          | The user's items it consumes, with the urgent ones marked                                                                                            |
| Buy           | What must be bought, ideally "nothing"; only required items, never optional garnish                                                                  |
| Assumes       | Pantry assumptions, split into required, assumed and optional (section 3)                                                                            |
| Open point    | Anything to resolve first, such as rice history or a missing structural item; high-risk ingredients carry a short safety note (see `food-safety.md`) |
| Tags          | Diet or allergen fit, difficulty, only when relevant                                                                                                 |

Wording rules: lead with the feature that decides the choice, not the cuisine label; one or two short lines per option; no recipe steps; no invented extras to inflate the "uses" count; end with a single narrow next step ("Which one should I turn into a full recipe?"), not an open "what would you like to do?". Put the best match first and say why in a few words (uses the most urgent items, nothing to buy).

Example for spinach, mushrooms, eggs, spring onions, yoghurt and cooked rice of unconfirmed history:

| Option                                     | Hook                                                             | Uses                                    | Buy                  | Open point                                                                                               |
| ------------------------------------------ | ---------------------------------------------------------------- | --------------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------- |
| Mushroom and spinach frittata (best match) | Soft egg, browned mushrooms, spinach as the main filling, 20 min | Eggs, mushrooms, spinach, spring onions | Nothing              | Assumes oil and salt                                                                                     |
| Vegetable fried rice                       | Quick pan meal with egg and spring onion, 15 min                 | Rice, eggs, mushrooms, some spinach     | Nothing              | Offered only after the user confirms the rice was chilled promptly and its age is within the local limit |
| Greens pancake with yoghurt dip            | Crisp-edged and vegetable-heavy, 25 min                          | Spinach, spring onions, yoghurt         | Flour if not at home | Dropped if no flour or tested batter is available                                                        |

### 8.4 Ranking

Order the shortlist by the ranking in section 1 (diet and safety fit first, then urgent food used, time and equipment, items to buy, coherence). One report suggested numeric weights (40 percent perishables used, 25 utilisation, 15 purchase minimisation, 10 time, 10 preference; single report, to verify); the plugin keeps the ordered list because nobody validated the weights. React to what the user says ("quick", "no chopping", "choose for me") instead of guessing at fatigue.

### 8.5 After the pick

Before writing the full recipe, settle the second-stage points: servings and usable amounts, structural pantry items, equipment and time, diet and allergen check, any leftover-safety question, which substitutions are tested and which are approximate (section 6.3), and storage advice for what the dish leaves over.

## 9. Evidence notes

| Topic                     | Strength and caveats                                                                                                                                                                                                                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dish templates and ratios | All seven reports describe the same structural approach; ratios come from cookbooks and test kitchens (practitioner). Numbers marked in section 4 as single-report are unverified. Treat all ratios as starting points                                                                                                                                 |
| Perishability tiers       | Safety-critical items are consistent across reports (raw poultry, fish, minced meat; cooked rice; leftovers near the limit). Tier boundaries for mid-range items are the plugin's synthesis. Reports gave no shared hour-level limits for tiers; one gave 12-36 hours for its top tier and nobody corroborated it, so no hours are stated in section 2 |
| Pantry assumptions        | No report measured what households own. Regional lists are a starting point (design); the "ask, assume, offer a fallback" policy is shared by Claude, DeepSeek and Perplexity                                                                                                                                                                          |
| Substitutions             | Function-based reasoning is shared; specific quantities are practitioner. Baking and set custards are the areas where all reports urge caution                                                                                                                                                                                                         |
| Food-waste research       | Intervention studies are mostly non-randomised and rely on self-report; prompts at the right moment, defaults and social-norm framing have better support than awareness messages alone. One 166-day household trial found a measurement effect, so the plugin does not claim its suggestions reduce waste                                             |
| Photo recognition         | Strong on common single items, weak on quantity, condition, packaged goods and occlusion. No benchmark covers real fridge scenes. Several 2025-2026 sources are preprints; model rankings change fast                                                                                                                                                  |
| Choice overload           | Meta-analyses show a near-zero average effect with moderators; 3 is a convention (practitioner/design). Menu-size studies do not transfer directly to dish shortlists                                                                                                                                                                                  |
| Safety limits             | Not repeated here; see `food-safety.md`. The reports agree that appearance and smell are not safety checks and that reheating is not a reset                                                                                                                                                                                                           |

### 9.1 Conflicts between reports and the default chosen

| Conflict                           | Positions                                                                                                   | Default                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Ground meat tier                   | Most reports group it with raw poultry and fish in the first band; one places it a step later               | Tier A                                                                  |
| Eggs                               | Medium in two reports, low in others                                                                        | Tier D unless cracked or cooked                                         |
| Mushrooms and tofu                 | Quality-falls-quickly in two reports, "use soon" in one                                                     | Tier B once opened or cut                                               |
| Number of options                  | 3 (Claude, Perplexity, Gemini, Consensus); 3-5 (ChatGPT, DeepSeek, Copilot)                                 | 3, up to 5 on request                                                   |
| Option archetypes                  | Gemini: express, max-utilisation, wildcard; Claude: one-pan, oven, cold or fast                             | Spread by template, effort and time, with an archetype label            |
| Ranking weights                    | Copilot's numeric weights against ordered criteria elsewhere                                                | Ordered criteria (section 1)                                            |
| Confidence display in photos       | Gemini: numeric thresholds with different UI per level; Perplexity: no numeric confidence unless calibrated | Word groups, no percentages                                             |
| Photo-count advice                 | Perplexity: second view helps most, more views add little; DeepSeek: photograph in sections                 | One overview, then one more angle or a section photo only if it matters |
| Whether to rank by quality or risk | DeepSeek ranks fish and cut produce first; others split safety from quality                                 | Two separate judgements (section 2)                                     |

### 9.2 Single-source claims

Marked `(to verify)` in this file: the practitioner accuracy percentages for fridge-scanning apps (DeepSeek), the memory-improves-scores finding (Claude), Copilot's numeric ranking weights, and, in sections 4 and earlier, the stir-fry slurry ratio, the grain-bowl proportions and the savoury-pancake ratio.

### 9.3 Not carried over

- The Hick-Hyman decision-time formula (Gemini): a loose analogy for a menu task, not evidence about dish shortlists.
- WRAP and other waste statistics, effect sizes of waste interventions and the hotel-study figure: context for a product case, not rules for cooking.
- Report-specific benchmark scores for vision models and the proposed benchmarking checklist: product-engineering material that goes stale quickly.
- Meal-kit and app interface observations beyond the card layout: practitioner impressions, not verified for any named service.
- Leftover storage limits, reheating temperatures, rice, nitrate and vulnerable-group rules: held in `food-safety.md` only.
- Gluten-free hydration and hydrocolloid dosing (Gemini) and dietary-adaptation detail: out of scope here; see the nutrition reference.
- The German-language ChatGPT and Consensus reports are shallow; they contribute agreement on tiers, confirmation before planning and 3-5 options, and nothing unique. Coverage: seven reports merged (Claude, ChatGPT, Consensus, Copilot, DeepSeek, Gemini, Perplexity).
