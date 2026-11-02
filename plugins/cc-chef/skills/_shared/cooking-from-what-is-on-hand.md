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
| B. Quality falls quickly                | Soft herbs, salad leaves, spinach, berries, mushrooms, bean sprouts, cut fruit, opened cream, soft fresh cheese, opened tofu                                                    | Give them the main slot, not the garnish; prefer templates that forgive tired texture                     |
| C. Medium                               | Peppers, courgette, broccoli, cucumber, opened milk and yoghurt, cooked leftovers within their window, whole cuts of meat                                      | Plan within about a week                                                                                  |
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

| Tier | Items | Treatment |
| --- | --- | --- |
| 0, assume silently | Water, salt, a cooking fat | Name them in the "assumes" line anyway so a correction is easy |
| 1, assume and list | Black pepper, sugar, one acid (vinegar or lemon), flour or starch, stock cube, onion, garlic | Show under "assumes"; onion and garlic are perishable, so confirm when a dish depends on them |
| 2, regional defaults to ask about | See table below | Offer, confirm, or give a fallback |
| 3, cuisine-specific, never assume | Fish sauce, miso, tahini, curry paste, garam masala, sumac, tamarind, coconut milk, specialty flours, crème fraîche, paneer | Ask, make optional, or pick another template |

| Region or cuisine | Defaults to offer and confirm |
| --- | --- |
| Western and Northern Europe, North America | Butter, olive or neutral oil, mustard, dried oregano or thyme, paprika, canned tomatoes, pasta, rice |
| Mediterranean, Middle East | Olive oil, lemon, cumin, dried mint, sumac, tahini, chickpeas, bulgur |
| South Asia | Ghee or neutral oil, cumin and mustard seeds, turmeric, chilli powder, garam masala, lentils, atta, rice |
| East Asia | Soy sauce, rice vinegar, sesame oil, ginger, spring onion, rice; gochujang or doenjang (Korea); miso, mirin, dashi (Japan) |
| Southeast Asia | Fish sauce, lime, palm sugar, chilli, rice, coconut milk |
| Latin America | Cumin, dried chillies, oregano, limes, beans, masa or tortillas, rice |

Ask, assume or offer a fallback (design):

| Situation | Action |
| --- | --- |
| The answer changes safety, diet, structure or the top recommendation | Ask |
| Wrong guess is cheap and easy to correct | Assume and state it |
| Several items can do the same job | Offer the alternative inline |
| A structural item is missing and nothing reliable replaces it | Choose another template |

Keep three lists separate on every option: required, assumed, optional. An optional garnish never becomes a mandatory purchase, and "just pantry staples" followed by nine unconfirmed condiments is a failure.

Fallbacks for flavour-defining staples: no fish sauce, use soy sauce with a pinch of sugar; no fresh ginger, ground ginger at about a quarter of the amount (practitioner); no soy sauce, salt with a splash of vinegar (the weakest option, say so); no fresh garlic, garlic powder at roughly one clove to an eighth of a teaspoon, added to liquid rather than hot oil.

## 4. Dish templates

A template is a set of slots plus constraints. Fill the slots from the inventory, giving urgent items the main role; unfilled slots become "to buy"; prefer templates whose gaps are pantry staples. Ratios are starting points: state the assumption (cooked and drained vegetables, cooled rice) and adjust to the ingredients.

| # | Template | Slots | Base ratio or rule | Absorbs well | Constraint that prevents failure |
| --- | --- | --- | --- | --- | --- |
| 1 | Egg-bound bake (frittata, tortilla, omelette, kuku) | Egg, fat, fillings, sharp element | About 6 eggs to 120 ml dairy; roughly 1 egg per 50-80 g filling (practitioner); a custard runs about 2 liquid to 1 egg | Cooked veg, potato, cheese, cured meat, herbs, leftover pasta | Pre-cook and drain watery veg (mushroom, courgette, spinach); salt the eggs; do not drown the egg |
| 2 | Stir-fry | Fat, aromatics, protein, veg, sauce | Sauce about 3 savoury liquid to 1 sour or sweet; slurry of equal parts starch and water if thickening (single report, to verify) | Firm and soft veg, thin protein, tofu, mushrooms | Small batches, dry surface, similar cuts, add by cooking time; crowding steams |
| 3 | Fried rice | Cold rice, fat, egg, aromatics, additions, seasoning | Additions are accents, rice is the bulk | Diced veg, cooked protein, kimchi, peas | Cooled day-old rice; confirm its history first (see `food-safety.md`) |
| 4 | Soup | Aromatic base, liquid, bulk, body, finish | About 1 part solids to 3 parts liquid (two reports, rough) | Almost anything, rinds, wilted greens, legumes | Sweat aromatics, season in layers, acid or herbs at the end; starch for body in purées |
| 5 | Stew or braise | Browned main, aromatics, liquid, acid | Liquid partly covers; long low heat | Tough cuts, roots, legumes, tomato | Brown first, deglaze, lean cuts dry out; quick bean stews are a different, short template |
| 6 | Curry | Fat, aromatic or spice base, liquid, main, balance | Bloom spices in fat before liquid | Veg, pulses, paneer, tofu, chicken, fish, eggs | Sour, sweet and salt in balance; dairy or coconut late to avoid splitting; name the direction (tomato-lentil, coconut) |
| 7 | Pasta | Pasta, sauce family, starchy water, umami, lift | Finish the pasta in the sauce with a ladle of cooking water | Veg, cured meat, canned fish, cheese, nuts, herbs | One sauce family (oil, tomato, cream, broth); rich salty extras count as seasoning |
| 8 | Grain bowl (donburi, bibimbap) | Grain, protein, veg, sauce, crunch | Roughly 1 cup cooked grain, 1/2 cup veg, 80-90 g protein, 2-3 tbsp dressing (single report, to verify) | Raw, roasted, pickled veg, eggs, pulses | A strong dressing links parts; mix textures and temperatures |
| 9 | Savoury pancake or fritter | Batter or binder, mix-ins, fat, dip | About equal flour and liquid by weight plus an egg, 2-3 parts shredded solids (single report, to verify) | Cabbage, spring onion, courgette, kimchi, cooked fish | Squeeze out water, hot oiled pan; chickpea-flour batters are their own dish |
| 10 | Hash | Cooked starch, fat, onion, extras | Equal parts diced base | Roast potato, roots, cooked meat | Dry components, one layer, leave it alone to crisp; sauce turns it into a sauté |
| 11 | Gratin or bake | Starch or veg, binding sauce, topping | Thin even slices; sauce well seasoned | Roots, squash, cooked pasta, greens, cheese ends | Pre-cook dense items; cheese cannot rescue a watery filling; brown top needs fat and starch or cheese |
| 12 | Tart, pie, quiche, börek | Pastry, filling, binder | Short pastry about 3 flour : 2 fat : 1 water; custard as in row 1 | Cheese, veg, cooked meat, greens | Pre-cook and drain filling; blind-bake for wet fillings; bought pastry cuts time |
| 13 | Composed salad (fattoush, panzanella, slaw) | Base, dressing, crunch, protein | Vinaigrette starts near 3 oil : 1 acid; adjust to the acid | Raw veg, stale bread, grains, fruit, nuts | Dress lightly, salt wet parts separately; tired veg does not suit raw salad |

Fridge-clearing favourites, because they take the widest range with the fewest purchases: egg bake, fried rice, stir-fry, soup, grain bowl. Greens in bulk go to soup, curry, börek filling or pancake; a handful goes into fried rice or an egg bake.

Pick a template by what the urgent item needs: delicate and wilting means cooked-soft formats (soup, curry, egg bake); crisp and firm means stir-fry, salad or roast bowls; a large amount means soup, pancake, pie filling or curry.

## 5. Seasoning and balancing layer

Run this checklist on every filled template before presenting it. A dish that fails a line gets the missing item added or an honest note that it will taste flat without it.

| Check | Question | Typical fix |
| --- | --- | --- |
| Salt | Is there a salt source, counting stock, soy, cheese and cured meat already present? | Season in stages; final adjustment after assembly |
| Fat | Is there a fat that carries flavour, and is the aromatic cooked in it? | Cook aromatics and spices in the fat; finish with an aromatic oil or butter |
| Acid | Is there something sharp, at the right moment? | Lemon, vinegar, tomato, yoghurt, pickles, tamarind at the end |
| Aromatic | Onion family, ginger, garlic, spices or herbs? | Bloom spices in fat, soft herbs last |
| Umami | A savoury depth source that fits the dish? | Tomato paste, mushroom, aged cheese, soy, fish sauce, miso, anchovy |
| Heat or sweetness | Needed only to balance? | Make chilli optional; a pinch of sugar rounds acid or bitterness |
| Texture | Is there contrast (crunch against soft)? | Toasted nuts or seeds, crisp onion, fresh veg added at the bowl |
| One direction | One identifiable flavour direction and one finishing contrast? | Pick ginger-soy, or cumin-lemon, not both; drop extras that do not do a job |

Dish-specific points: salt eggs before cooking; salt the greens directly before dressing; season gratin layers and the sauce; add dairy or coconut late in curry; an acid finish lifts soups and stews. For deeper craft rules see `culinary-craft.md`.

## 6. Substitutions by function

Ask what the ingredient does in this dish, then check whether the replacement does the same job. Savoury stovetop dishes (stir-fry, soup, stew, curry, pasta) tolerate swaps because flavour and bulk dominate; baking, emulsions and set custards are chemical and structural, so be conservative there and say when a swap changes the dish rather than imitates it.

### 6.1 Function table

| Function | What must be kept | Common mistake | Fails in |
| --- | --- | --- | --- |
| Structure | A matrix that holds shape or traps gas | Swapping for something that adds only moisture | Baking, set custards, quiche, frittata |
| Moisture | Total water and where it sits | Matching volume without regard to absorption | Batters, doughs, gratin |
| Fat | Tenderness, richness, sometimes aeration or layers | Treating oil and solid fat as identical | Creamed cakes, laminated or flaky pastry, shortbread, buttercream |
| Leavening | Gas made, and the acid or base that makes it | Dropping buttermilk or yoghurt without adjusting the soda | Cakes, quick breads, pancakes |
| Binding | Cohesion, not always setting | Assuming every binder sets when heated | Meatballs rely on it mildly; omelettes and custards fully |
| Emulsifying | Stable fat-in-water mix | Fixing thickness only | Mayonnaise, vinaigrette, cream sauces, hollandaise |
| Acid | Taste, sometimes setting or leavening | Using seasoning swaps where the formula or a preserve needs the acid | Pickles and preserves (never improvise), soda-leavened batters |
| Sweetness | Bulk, water holding, browning, not only taste | Matching sweetness only | Meringue, creamed cookies, cakes |
| Flavour | Aroma and savouriness | Calling look-alikes identical | Raw finishing herbs, long-simmered bases |

### 6.2 Ingredient swaps and what changes

| Original | Replacement | Preparation change | Fails in |
| --- | --- | --- | --- |
| Butter | Oil | Savoury cooking: swap freely; use oil for high heat, butter or ghee for flavour. Baking: about three-quarters of the amount, denser moister crumb, no creaming | Flaky pastry, shortbread, creamed batters |
| Butter | Ghee | Higher smoke point, good for searing and tempering | Less browning in baking |
| Cream | Milk | Fat under about 30 percent can curdle with acid at a boil; add off heat or stabilise with a little starch | Reduction sauces, hot acidic sauces |
| Cream or milk | Plant drink | Soy is closest in protein; oat thickens and sweetens; almond and rice are thin; use unsweetened for savoury | Set custards, reduction sauces, béchamel with coconut |
| Buttermilk or yoghurt | Milk | Add lemon or vinegar, or switch soda to baking powder | Soda-leavened bakes |
| Egg (binding) | Flax or chia gel (1 tbsp ground seed + about 3 tbsp water), starch slurry | Rest the gel; expect a denser result | Anything that must set |
| Egg (foam) | Aquafaba, about 3 tbsp per egg | Less stable than egg white; fat and acid hurt the foam | Delicate sponges |
| Egg (set) | None reliable | Use a different dish (chickpea-flour pancake) instead of calling it a frittata | Custard, quiche, frittata, soufflé |
| White flour | Whole wheat | Absorbs more water, slower; start with up to half whole wheat; rest 20-30 minutes; add liquid gradually | Delicate cakes |
| Wheat flour | Gluten-free blend | Use a blend and a recipe made for it; hydration and a binder (xanthan or psyllium) matter together | Yeast bread, laminated dough, roux |
| Wheat flour | Coconut or almond flour | Not 1:1; tested recipe only | Any 1:1 swap |
| Sugar | Honey or syrup | Adds water: cut other liquid, lower the oven by about 15 C, expect faster browning | Crisp or creamed bakes |
| Sugar | Intense sweetener | Loses bulk and browning | Meringue, cookies, cakes |
| Lemon, lime, vinegar | One another | Adjust to strength; rice vinegar is mild, malt is loud; tamarind, sumac, tomato, yoghurt belong to different traditions | Preserves, pickles |
| Meat | Beans, lentils, mushrooms, tofu | Change timing and sequence, not just the name; add fat and umami; do not copy raw-meat steps to cooked legumes | Dry-heat roasts, dishes built on meat texture |
| Lean cut | Fatty cut (or reverse) | Match cooking time class: thigh and shoulder in braises, quick fish or prawns in quick curries | Lean cuts in long braises; delicate fish in long stews |
| Onion | Shallot, leek, spring onion | Shallot sweeter, leek milder and needs more time, spring onion for freshness | Spring-onion white for caramelised onion |
| Fresh garlic | Powder | Burns in hot oil; add to liquid | Raw preparations |
| Fresh herbs | Dried | Roughly 1 part dried to 3 fresh for hardy herbs, added early | Soft herbs (basil, coriander, parsley, dill, mint) as a raw or finishing herb; pesto, salsa verde |
| Whole spice | Ground spice | Rethink when to add; bloom ground spice briefly in fat, do not add to cold liquid | Tadka-style dishes |
| Spice blend | Single spice | Check the blend for salt, heat, allergens | Dishes built on that blend |

### 6.3 Rules to apply

- Each substitution is recorded as: original, role, replacement, quantity rule, water change, method change, taste change, diet and allergen change, confidence.
- Confidence has three levels: tested in this recipe, tested in a similar use, untested suggestion (design).
- Run the allergen check again after every swap: almond for wheat, tahini or sesame oil for peanut, soy milk for dairy each introduce a common allergen. Lactose-free is not milk-allergy-safe.
- A name must not promise the original texture once the structure changed: "chickpea-flour pancake", not "vegan frittata".
- Acid in preserves, pickles and fermentation is a safety control, not seasoning; no improvised swaps. Do not cut salt casually in cures, brines and ferments.
- Lower-sugar, lower-salt and lower-saturated-fat baking: reduce modestly (about 10 percent sugar is a test-kitchen start); beyond that expect texture and keeping losses. For savoury dishes lean on acid, aromatics and umami and count salty condiments.
- Vegetarian: check hidden animal products in fish sauce, Worcestershire, gelatin, stock and some cheeses.
