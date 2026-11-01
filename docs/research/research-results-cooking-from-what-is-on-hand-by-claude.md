# Designing a "Use What's in My Fridge" Cooking Assistant: Evidence Base for Templates, Prioritization, Substitutions, Safety, Photo Recognition and Choice Presentation

The assistant should work from about a dozen structural dish templates, not a recipe database. It should rank ingredients by perishability and safety risk, assume only a small pantry that depends on the user's region and confirm everything else, and offer about three clearly different options. It must also treat any photo-based inventory as a draft for the user to confirm: on current benchmarks, models are good at naming common items but unreliable at judging quantity, freshness and packaged goods.

## TL;DR

- **Cook from templates, then rank the options.** Most "what can I make?" requests fit a small set of structural templates: egg-bound bakes, stir-fry and fried rice, soup and stew, curry, pasta, grain bowl, savory pancake, hash, gratin, tart, and composed salad. Each has a known base ratio (Ruhlman's custard is 2 parts liquid to 1 part egg; his bread dough is 5 parts flour to 3 parts water), takes certain ingredient categories, and needs a "balancing" layer of salt, fat, acid and aromatics to taste coherent. Choose the template that uses up the ingredient most at risk of spoiling, then check substitutions by what each ingredient does in the dish.
- **Safety rules differ by country, so set limits by the user's location and default to the strictest.** USDA FSIS allows 3–4 days for cooked leftovers and reheating to 165 °F/74 °C. The UK FSA says eat leftovers within 2 days, cooked rice within 24 hours, and reheat only once. Germany's BfR specifies reheating to at least 70 °C for 2 minutes and highlights *Bacillus cereus* in starchy foods and nitrite in nitrate-rich vegetables such as spinach.
- **Treat a photo as a draft inventory that the user confirms, and show about three options.**\[1\] GPT-4o reached an F1 of 0.86 for ingredient detection in one study (Pic2Plate). But on freshness, quantity and packaged goods, models are far below humans. In SFOOD, GPT-4o scored 0.50 accuracy on ripeness against 0.85 for humans.\[2\] In NutriBench-Kitchen, GPT-4o averaged 47.7% against 92% for humans.\[3\] Research on choice overload shows harm mainly when options are complex and preferences are uncertain.\[4\] That argues for a small, clearly differentiated set (about 3) rather than a long list.

## Key Findings

| Area | Bottom line | Evidence type |
|---|---|---|
| Templates | About 12 structural templates cover most fridge-clearing requests. Ratio-based thinking (Ruhlman) makes them scalable. | Practitioner (culinary texts) |
| Prioritization | Rank by safety-critical perishability first (raw fish, poultry, minced meat, cooked rice), then quality perishability (soft herbs, leafy greens, berries, opened dairy). Food-waste interventions that combine several components and include nudges work best. | Empirical (systematic reviews) plus official guidance |
| Pantry | Assume only salt, a cooking fat and water without asking. Ask about or offer alternatives for everything else, using region-specific defaults. | Practitioner; little empirical data |
| Substitutions | Classify each ingredient by function (structure, moisture, fat, leavening, binding, emulsifying, acid, sweetness, flavor). Swaps fail when a function is lost and nothing replaces it. | Food science plus test kitchens |
| Dietary adaptation | Gluten, egg, sugar and salt do structural or chemical work. Removing them requires putting that function back, not just leaving them out. | Peer-reviewed food science |
| Leftovers safety | Authorities differ on how many days (2 vs. 3–4), the reheating rule (165 °F vs. "steaming hot" vs. 70 °C for 2 min) and rice (24 h in the UK). | Official guidance |
| Photo recognition | Good at naming common items; weak on counts, weights, ripeness or spoilage, packaged goods and look-alikes. | Empirical (2025–2026 benchmarks) |
| Presenting options | 3 options (5 at most) with distinct "shapes", each described by time, ingredients used and what to buy. | Empirical (choice overload meta-analyses) plus industry practice |

## 1. Flexible Dish Templates

### How experienced cooks improvise

Published approaches to improvised cooking share one idea: learn the structure, then fill it with what you have.

- **Ratio-based cooking.** Michael Ruhlman's *Ratio* (2009) reduces many preparations to proportions by weight. Examples: bread dough is 5 parts flour to 3 parts water; fresh pasta is 3 parts flour to 2 parts egg; pie dough is 3 parts flour, 2 parts fat, 1 part water; custard is 2 parts liquid to 1 part egg. He argues that once you know the ratio, you can scale it to whatever amount of an ingredient you have on hand.\[5\]\[6\] For an assistant, ratios are the most useful kind of culinary knowledge: if the user has 3 eggs, the custard ratio tells you the frittata or quiche takes roughly 300 ml of dairy.\[7\]
- **Element-based seasoning.** Samin Nosrat's *Salt, Fat, Acid, Heat* (2017) treats seasoning as balancing four elements, not following a recipe. This is the main tool for making a mixed bag of ingredients taste deliberate.
- **Leftover-led cooking.** Tamar Adler's *An Everlasting Meal* (2011) and Niki Segnit's *Lateral Cooking* (2018) both treat dishes as families of related preparations, and leftovers as the start of the next meal.
- **Science-driven technique.** Harold McGee's *On Food and Cooking* (2004) and J. Kenji López-Alt's *The Food Lab* (2015) explain *why* techniques work. That is what lets you substitute safely (see Section 4).

All of these are practitioner frameworks. They are well established, but nobody has tested empirically whether "template cooking" produces better meals. The food-waste literature does link cooking skill and leftover management to lower household waste (see Section 2).

### Template catalogue

| Template | Structural requirement | Ingredient categories it absorbs | What makes it taste coherent |
|---|---|---|---|
| **Frittata / omelette / tortilla española / kuku sabzi / tamagoyaki-style rolled egg** | Eggs as binder. For bakes, roughly 2:1 liquid to egg by weight (Ruhlman); for a frittata, about 1 egg per 50–80 g of fillings (practitioner). | Cooked or quick-cooking vegetables, cheese, cured meat, cooked potato, herbs, leftover pasta or rice | Pre-cook watery vegetables (mushrooms, zucchini, spinach) so they don't weep. Salt the eggs. Add one sharp element: cheese, herbs or chili. |
| **Stir-fry** (Chinese chǎo; also Thai pad krapow) | High heat, small pan load, ingredients cut to similar size, sauce added at the end | Almost any vegetable, thin-sliced protein, tofu, eggs | An aromatic base (garlic, ginger, scallion), salty-umami (soy, oyster or fish sauce), a little sugar, and sometimes acid (rice vinegar). Add ingredients in order of cooking time. |
| **Fried rice / nasi goreng / bokkeumbap / arroz chaufa** | Cold, day-old rice (dry grains fry rather than steam); hot pan | Diced vegetables, leftover meat, eggs, kimchi, peas | Seasoning sauce, egg for richness, and a scallion or herb finish. Rice must have been cooled and stored safely (Section 6). |
| **Soup** (minestrone, miso soup, caldo, dal-style) | Liquid plus aromatic base; simmer | Nearly everything: wilting vegetables, rinds, bones, legumes, grains, small amounts of protein | Sweat the aromatics first. Season at the end. Finish with acid or fresh herbs. For blended soups, a starch (potato, bread, rice) for body. |
| **Stew / braise** (ragù, tagine, adobo, feijoada) | Liquid partly covering the food; long low heat | Tougher proteins, root vegetables, legumes, tomatoes | Brown the meat (Maillard flavor). Use a deglazing liquid. Balance with acid (wine, vinegar, tomato). |
| **Curry** (Indian, Thai, Japanese kare) | Aromatic paste or spice base bloomed in fat, plus a liquid (stock, coconut milk, yogurt, tomato) | Vegetables, legumes, paneer or tofu, chicken, fish, eggs | Bloom whole or ground spices in fat. Balance salt, sour (tamarind, lime, tomato) and sweet (palm sugar, onion). Add dairy or coconut late to avoid splitting. |
| **Gratin / bake / casserole** (gratin dauphinois, moussaka, pastitsio) | Starchy or vegetable base, a binding sauce (béchamel, cream, cheese sauce or egg custard), oven heat | Root vegetables, cooked pasta, leftover greens, cheese ends | Slice vegetables thin and evenly. Season the sauce well. Get a browned top. |
| **Pasta** (aglio e olio, "pasta with whatever", ragù) | Cooked pasta plus a sauce emulsified with starchy pasta water | Vegetables, cured meats, canned fish, cheese, nuts, herbs | Pasta water for emulsion. Fat plus aromatics. Hard cheese or anchovy for umami. Lemon, chili or herbs to lift. |
| **Grain bowl / donburi / bibimbap / Buddha bowl** | Starch base plus protein plus vegetables plus sauce | Raw, roasted or pickled vegetables, eggs, leftover proteins, legumes | A strong sauce or dressing (gochujang, tahini, soy-sesame, vinaigrette) ties the components together. Mix textures. |
| **Savory pancake / fritter** (Korean jeon or pajeon, Japanese okonomiyaki, Indian chilla, French galette) | Batter (flour plus liquid plus optional egg) holding shredded or chopped fillings | Cabbage, scallion, zucchini, kimchi, leftover seafood or meat | Squeeze moisture out of watery vegetables. Use a hot oiled pan. Dipping sauce (soy-vinegar, okonomi sauce). |
| **Hash** (corned-beef hash, bubble and squeak, Swedish pyttipanna) | Pre-cooked starchy base (potato), fried until crisp | Leftover meat and vegetables, onions | Crispness comes from contact with a hot pan and not stirring. Top with an egg. Finish with something acidic (pickles, ketchup, hot sauce). |
| **Pie / tart / quiche / börek** | Pastry (Ruhlman's 3:2:1) or bought sheets, plus a filling (often custard) | Cheese, vegetables, cooked meat, greens | Pre-cook and drain fillings. Use the custard ratio. Blind-bake the base for wet fillings. |
| **Salad** (fattoush, panzanella, Thai yam, slaw) | Fresh base plus dressing (classic vinaigrette is about 3:1 oil to acid, per Ruhlman) | Raw vegetables, herbs, stale bread, grains, fruit, nuts, leftover protein | Balance acid, salt and fat. Mix textures (crunch). Panzanella and fattoush are themselves leftover-bread dishes. |

**Design implication.** Encode each template as slots: base, binder or liquid, aromatics, main ingredients, finish or garnish. Add constraints (moisture handling, cooking order) and a seasoning checklist covering salt, fat, acid, heat or aromatic, and umami. When generating suggestions, the assistant should (a) fill the slots from the user's inventory, giving the priority ingredients the main roles, (b) count the slots it can't fill as "to buy", and (c) prefer templates where the missing items are pantry staples.

## 2. Prioritizing Ingredients

### What to use first

Rank perishable items on two separate axes: **safety risk** and **quality decline**.

1. **Highest priority (safety-critical, short limits):**
   - Raw poultry, fish, minced meat and offal: USDA FSIS says cook or freeze within 2 days.
   - Other raw beef, veal, lamb and pork: within 3–5 days (FSIS).
   - Cooked rice: within 24 hours under UK FSA rules.
   - Opened ready-to-eat items past their "use by" date.
   - Cooked leftovers nearing 2 days (UK) or 3–4 days (US).
2. **High priority (quality falls quickly):** soft herbs, salad leaves, spinach, berries, mushrooms, bean sprouts, opened cream, fresh soft cheeses, opened tofu.
3. **Medium:** most fresh vegetables (peppers, zucchini, broccoli), opened milk, yogurt, eggs.
4. **Low:** roots and alliums (potatoes, carrots, onions), hard cheese, cured meats, condiments, dry goods.

**Signs of age the assistant can ask about or look for:**
- wilting or sliminess on leaves
- soft spots and wrinkling on peppers or zucchini
- sprouting and green skin on potatoes
- off smells or sliminess on raw meat or fish
- mold

Mold on soft foods generally means throwing the item away, while firm foods can sometimes be trimmed (practitioner and official consumer guidance). The UK FSA warns that you cannot detect food-poisoning bacteria by smell, so the "sniff test" is not a safety check. Vision models are also weak at judging condition (Section 7). The assistant should therefore **ask** about the condition of key items rather than infer it.

**Building the dish around the priority item.** Practitioner heuristics:
- Give the most at-risk item the "main" slot: for example, wilting spinach becomes the filling of a frittata or the greens in a dal, not a garnish.
- Prefer templates that tolerate imperfect texture: soups, stews, fried rice, fritters and gratins tolerate tired vegetables; salads do not.
- Use high-volume perishables in dishes that use a lot of them: a bag of spinach shrinks into a curry or a börek filling.

### What the research says about household food waste

- **Scale and patterns.** WRAP's March 2026 Food Waste Action Week release puts UK household food waste at 6 million tonnes a year, of which 4.4 million tonnes could have been eaten; that edible food is worth £17 billion and costs an average household of four £1,000 a year, or £86 a month (the underlying data year is 2022). WRAP also finds that cheap staples (bread, potatoes, carrots) are wasted more than expensive foods such as pork and fresh chicken. Potatoes are the most binned item: WRAP's Household Food Management Survey release estimates that 510,000 tonnes are binned, 46% of all potatoes bought.
- **Perception gap.** In WRAP's 2025 Household Food Management Survey (n = 5,509), 80% believed they waste less than the average household, and 27% were classified as high food wasters.\[8\] This "denial" matters for product design: users won't call themselves wasters, so the assistant should frame suggestions as saving money and time, not as waste reduction.
- **Which interventions work.** A systematic review by Liechti et al. (2024, *Sustainable Production and Consumption*) of 49 studies covering 54 consumer-level interventions found that 36 of the 54 (67%) led to significant reductions in food waste. Multi-component interventions that included nudges achieved the largest reductions; the top figure of 84.3% came from a single non-randomised hotel study that combined nudges with awareness-raising, not from a household setting. The review also notes that most studies were non-randomised (quasi-)experiments. Simões, Carvalho & de Matos (2022), reviewing 96 papers in the *Journal of Cleaner Production*, conclude that "informational interventions alone are not enough to change consumers behaviour." Barker et al.'s (2021) critical-appraisal review found reliable evidence for nudges based on social norms and reminders, but not for disclosure alone (e.g., environmental cost messages).\[9\] Schanes, Dobernig and Gözet (2018) identify planning, shopping lists, managing leftovers and understanding date labels as practices that prevent waste.

**Implication.** An assistant that (a) prompts at the right moment ("your chicken is on day 2: here are 3 dishes"), (b) makes using leftovers the easy default and (c) uses gentle social-norm framing matches the intervention types with the best evidence. Generic "food waste is bad" messaging does not. *Evidence status:* the direction of effect is empirical. Exact effect sizes for an AI assistant are unknown and should be tested with A/B experiments.

## 3. Pantry Assumptions

### What can safely be assumed

There is little peer-reviewed data on which staples households actually keep in different countries, so this section is mostly practitioner guidance. A defensible tiered model:

- **Tier 0 (assume silently):** water, salt, a cooking fat or oil.
- **Tier 1 (assume, but list as "you'll need" so the user can object):**
  - black pepper
  - sugar
  - one acid (vinegar or lemon)
  - flour or another starch
  - one stock option (cubes or powder)
  - garlic and onion (these are perishable and often missing, so confirm them)
- **Tier 2 (region-dependent defaults, always confirmed):**

| Region / cuisine | Typical pantry defaults to *offer* (confirm) |
|---|---|
| Western/Northern Europe, North America | Butter, olive or neutral oil, mustard, dried oregano or thyme, paprika, canned tomatoes, pasta, rice |
| Mediterranean / Middle East | Olive oil, lemon, cumin, dried mint, sumac, tahini, chickpeas, bulgur |
| South Asia | Ghee or neutral oil, cumin and mustard seeds, turmeric, chili powder, garam masala, dal, atta, rice |
| East Asia | Soy sauce, rice vinegar, sesame oil, ginger, scallions, rice; doenjang or gochujang (Korea); miso, mirin, dashi (Japan) |
| Southeast Asia | Fish sauce, lime, palm sugar, chili, rice, coconut milk |
| Latin America | Cumin, dried chilies, oregano, limes, beans, corn masa or tortillas, rice |

### Handling uncertainty: ask, assume or offer alternatives

Recommended policy (practitioner reasoning, consistent with the confirmation best practices in Section 7):

1. **Assume Tier 0 silently.** Asking about salt is irritating.
2. **For Tier 1–2 items, assume and disclose.** Each suggestion lists the pantry items it relies on ("uses: soy sauce, garlic") so the user can spot gaps without being asked.
3. **Ask only when a staple decides the dish.** For example: "Do you have soy sauce or fish sauce?" before suggesting a stir-fry as the lead option.
4. **Always give a fallback for flavor-defining staples.** For example: no fish sauce → soy sauce plus a pinch of sugar; no fresh ginger → ground ginger at about one-quarter the amount (practitioner).
5. **Learn the pantry.** Keep a user-level pantry profile updated by their confirmations, and weight defaults by locale. This reduces questions over time.

## 4. Substitutions and Their Consequences

### Think in functions, not ingredients

The key move is to tag each ingredient with what it does in the specific dish: structure, moisture, fat, leavening, binding, emulsification, acidity, sweetness or flavor. A swap is safe when the replacement does the same job; it fails when a job goes undone. In practice:
- **Savory stovetop cooking (stir-fry, soup, stew, curry, pasta) tolerates swaps well**, because the main functions are flavor and bulk.
- **Baking and emulsions are fragile**, because the functions there are chemical and structural.
- The assistant should be liberal with swaps in the first group and conservative in the second.

### Category-by-category

**Fats**
- **Butter vs. oil.** Butter is roughly 80% fat with about 15–18% water and milk solids (McGee, 2004). Its water creates steam (flaky pastry), and its solids brown and add flavor. Oil is 100% fat and liquid at room temperature.
  - *Savory cooking:* swapping is reliable. Use oil for high-heat stir-fries, butter or ghee for flavor.
  - *Baking:* oil in place of butter gives a moister, denser crumb and no creaming aeration. Use about three-quarters of the butter amount (practitioner).
  - **Reliable failures:** laminated or flaky pastry, shortbread, and any recipe that creams butter and sugar to build volume, when made with oil.
- **Ghee / clarified butter** has no water or milk solids, so it has a higher smoke point (good for tadka and searing) but browns less in baking.
- **Coconut oil** is solid below about 24 °C, so it can stand in for butter in some pastry. It is very high in saturated fat (relevant to Section 5).

**Dairy and plant-based dairy**
- Milk → plant milks works in most batters and soups. Soy milk is closest in protein (it browns and sets better). Oat milk thickens when heated. Almond and rice milks are thin.
- **Cream vs. milk:** fat content decides whether a sauce resists splitting. Sauces with less than about 30% fat curdle when boiled with acid. Use cornflour or flour to stabilize, or add the cream off the heat.
- **Yogurt / buttermilk** add acid. In baking, that acid reacts with baking soda. If you replace them with plain milk, the soda has no acid, so you need baking powder or added lemon juice or vinegar (practitioner; standard chemistry).
- **Reliable failures:** coconut or low-fat plant "creams" in reduction sauces, and plant milks in set custards that need milk proteins and egg to firm up.

**Eggs.** Eggs bind, leaven (whipped whites), emulsify (yolk lecithin), add moisture and set structure (custards).
- *Binding* (meatballs, fritters, quick breads): flax or chia "egg" (1 Tbsp ground seed + about 3 Tbsp water; practitioner) or a starch slurry.
- *Foaming* (meringue, sponge): aquafaba. Peer-reviewed work shows chickpea aquafaba forms foams and emulsions and can replace egg white in sponge cake (Mustafa et al., 2018).\[10\] Centrifuged aquafaba even produced more stable emulsions than egg white under test conditions (Buhl et al., 2019).\[11\] Foaming quality varies by brand and cooking conditions.\[10\]\[12\]
- **Reliable failures:** set custards, quiche and frittata without egg. A chickpea-flour batter (Indian chilla, Ligurian farinata) is a *different dish* that fills the same slot, not a substitute.

**Flours**
- **Whole-grain vs. refined.** Whole wheat flour absorbs liquid *more slowly but ultimately more* than all-purpose flour.\[13\]\[14\]
  - King Arthur Baking recommends substituting up to 50% white whole wheat without other changes.\[15\]
  - For 100% substitution in yeast doughs, add 2 extra teaspoons of liquid per cup and let the dough rest 20–30 minutes before kneading.\[15\]\[16\]
  - If measuring by weight, use 113 g whole wheat for each 120 g of white flour.\[17\]
  - The more whole wheat you substitute, the denser the crumb and the stronger the flavor.\[18\]
- **Gluten-free flours** behave very differently. King Arthur's gluten-free bread flour needs 2–3 extra tablespoons of liquid per cup and a 20-minute rest, because it is more absorbent but slower to absorb than wheat flour.\[19\]
- **Coconut and almond flours are not 1:1 swaps.** Coconut flour is extremely absorbent; almond flour has no gluten and lots of fat.\[20\]
- **Reliable failures:** 1:1 swaps of coconut or almond flour for wheat; gluten-free flour in yeast bread without a binder; whole wheat flour in delicate cakes.

**Sweeteners**
- Sugar is not only sweet. It holds water and lowers water activity, tenderizes by delaying gluten development and starch gelatinization, browns (Maillard reaction and caramelization), aerates when creamed, and feeds yeast (Sahin et al., 2019).\[21\]\[22\]\[23\]
- Liquid sweeteners (honey, maple syrup) add water and acid. Practitioner rule: reduce other liquids, lower the oven by about 15 °C, and add a pinch of baking soda.
- **Reliable failures:**
  - replacing all the sugar in cookies or meringues with intense sweeteners (no bulk, no structure, no browning)
  - honey in recipes that depend on crisp, dry sugar crystallization

**Acids**
- Lemon juice, vinegars and lime are interchangeable for *seasoning*, adjusting for strength and flavor (rice vinegar is milder; malt vinegar is assertive).
- In baking, acid activates baking soda.
- In marinades for ceviche or kinilaw, acid "cooks" the fish and changes texture, but it does **not** make raw fish safe the way heat does.
- Tamarind, amchur, sumac, tomato and yogurt are the acids of different culinary traditions.

**Proteins**
- Swap within the same cooking-time class: chicken thigh ↔ pork shoulder in braises; firm white fish ↔ shrimp in quick curries.
- Tofu: firm for stir-fry, silken for blending.
- Cooked legumes can replace minced meat in ragù or chili, but they need more fat and umami (Section 5).
- **Reliable failures:** lean cuts in long braises (they dry out); delicate fish in long stews.

**Alliums**
- Onion ↔ shallot ↔ leek ↔ scallion: shallot is sweeter, leek milder, scallion fresher.
- Fresh garlic ↔ garlic powder: roughly 1 clove to ⅛ tsp (practitioner). Powder burns easily, so add it to liquid rather than hot oil.
- Asafoetida (hing) is the traditional Indian replacement in Jain or no-onion-garlic cooking.

**Fresh vs. dried herbs and spices**
- Common practitioner ratio: 1 part dried to about 3 parts fresh.
- Hardy herbs (thyme, oregano, rosemary, bay) dry well and go in early.
- Soft herbs (basil, cilantro, parsley, dill, mint) lose most of their character when dried and go in at the end.
- Whole spices bloomed in fat (tadka, sofrito) taste different from ground spices added to liquid.
- **Reliable failure:** dried soft herbs as the main flavor in a raw dish (pesto, chimichurri, salsa verde).

## 5. Dietary Adaptations

| Adaptation | What works | What breaks, and why |
|---|---|---|
| **Vegetarian** | Most templates. Rebuild umami with mushrooms, soy, miso, aged cheese, tomato paste, kombu or seaweed. Use legumes, eggs, paneer and tofu for protein. | Hidden animal products: fish sauce, anchovy in Worcestershire, gelatin, animal rennet in some hard cheeses (e.g., traditional Parmigiano Reggiano), meat stock. The assistant must check sauces and condiments, not just the main ingredients. |
| **Vegan** | Stir-fries, curries (coconut milk), grain bowls, pasta aglio e olio, dal, savory chickpea-flour pancakes. Aquafaba for foams. | Set custards, frittatas and quiches. Dishes that rely on dairy fat to emulsify (cream sauces split or turn thin). Cheese gratins: plant cheeses melt and brown poorly. Egg-washed glazes. |
| **Gluten-free** | Naturally gluten-free templates: rice dishes, potato hash, curries, corn tortillas, rice noodles, buckwheat (soba only if 100% buckwheat) | Wheat-based soy sauce (use tamari labelled GF), stock cubes, beer, breadcrumbs, roux. Gluten gives structure and gas retention, so yeast breads and laminated doughs fail without replacements such as xanthan gum or psyllium plus higher hydration. Cross-contact from shared toasters, colanders, flour dust and frying oil matters for coeliac disease. Codex Standard CXS 118-1979 (§2.1.1) defines "gluten-free" as gluten not exceeding 20 mg/kg in the food as sold, a threshold EU Implementing Regulation 828/2014 also adopts. |
| **Lactose-free** | Aged hard cheeses (Parmesan, aged Cheddar, Gruyère) are naturally very low in lactose. Lactose-free milk works 1:1 and is slightly sweeter (lactose is pre-split into glucose and galactose, which brown faster). Butter has little lactose. | Lactose-free ≠ dairy-free. Users with milk-protein *allergy* need full dairy avoidance, not lactose-free products, and the assistant must ask which applies. |
| **Lower saturated fat** | Replace some butter or cream with olive or rapeseed oil (savory), yogurt or blended white beans (creamy sauces); trim meat fat; roast instead of deep-fry | Pastry and shortbread rely on solid fat. Coconut oil and palm-based plant "butters" are high in saturated fat, so "vegan" doesn't mean lower in saturated fat. |
| **Lower sugar** | Savory templates hardly change. In desserts, reduce sugar modestly; use fruit, spices or vanilla for perceived sweetness. | In a 2026 pound-cake study (*International Journal of Food Science & Technology*), consumers rated texture "too hard" from 17.4% sugar reduction onward, and water activity rose steadily with each step.\[24\] Expect texture and shelf-life losses beyond modest reductions. Yeast needs some sugar or starch breakdown, and meringues need sugar for stability.\[25\] |
| **Lower salt** | Boost perceived flavor with acid, aromatics, umami (kombu, mushrooms, tomato), herbs and spices; salt at the end, on the surface | Sodium suppresses bitterness. Wise, Damani & Breslin (2019) found NaCl reduced bitterness in model broths by about 30%, while KCl did not.\[26\] Potassium chloride substitutes can taste bitter or metallic.\[27\]\[28\] Liem, Miremadi & Keast (2011) identify gradual "stealth" reduction as the best-supported approach, because salt preference adapts to exposure.\[29\] Salt also has structural roles: in bread it controls yeast and strengthens gluten; in brines and cures it is a safety factor and must not be cut casually. |

**Allergen cross-contact basics.** The EU requires labelling of 14 major allergens (Regulation 1169/2011). The US lists 9 (sesame was added by the FASTER Act, effective 2023). The assistant should:
- (a) capture allergies as hard constraints, separate from preferences
- (b) flag cross-contact risks: shared oil, cutting boards, toasters, and "may contain" labels on packaged goods it recognizes in photos
- (c) never suggest substitutes that introduce a common allergen without saying so (e.g., almond flour for wheat, tahini or sesame oil for peanut, soy milk for dairy)

## 6. Food Safety for Leftovers

### What the authorities say

| Topic | USDA FSIS (US) | UK FSA | German BfR / EU (EFSA) | Other |
|---|---|---|---|---|
| Fridge temperature | ≤40 °F (4 °C) | 0–5 °C\[30\] | Cool quickly to ≤7 °C (BfR, *B. cereus*) | Ireland's FSAI: cold food ≤5 °C\[31\] |
| Time at room temperature | Refrigerate within 2 h (1 h above 90 °F/32 °C) | Cool and refrigerate within 2 h; rice ideally within 1 h\[30\]\[32\] | Cool quickly or hold hot at ≥60 °C | Hong Kong CFS: cool 60→20 °C within 2 h, then 20→4 °C within 4 h\[33\] |
| Cooked leftovers in the fridge | 3–4 days (soups, stews, cooked poultry, fish, casseroles, pizza); chicken nuggets and patties 1–2 days\[34\] | **2 days** (48 h), or freeze\[30\]\[35\] | Not given as a single figure. BfR consumer advice: cooked rice and pasta within about a day | — |
| Reheating standard | **165 °F (74 °C)** internal; sauces and soups to a rolling boil\[32\] | **"Steaming hot all the way through"**; reheat only once\[36\] | **≥70 °C for 2 minutes in all parts** (BfR)\[37\] | FSAI/Hong Kong: core 75 °C\[31\]\[33\]\[38\] |
| How many reheats | No explicit limit | **Once** (rice and cooked-then-frozen food explicitly)\[32\]\[35\] | Consumer advice from German state agencies: rice only once | Hong Kong CFS: not more than once\[33\] |
| Cooked rice | Treated as a general leftover (3–4 days) | **24 h in the fridge; reheat once**\[32\] | Eat within about a day; rapid cooling is critical | —\[39\] |
| Freezer | Safe indefinitely at 0 °F; quality 2–6 months | About −18 °C; meats best within 2–3 months\[30\] | — | — |

### High-risk items and why

- **Cooked rice, pasta and other starchy foods (*Bacillus cereus*).** Spores survive cooking. If the food cools slowly or sits warm, they germinate and form **heat-stable emetic toxin (cereulide)**, which reheating does not destroy (UK FSA; BfR).\[31\]\[39\]\[40\]\[41\] BfR reports that *B. cereus* can grow between about 7 and 48 °C, and that cereulide forms best between 20 and 40 °C.\[40\]\[42\] EFSA's BIOHAZ Panel (2016) notes that most *B. cereus* illness involves food not stored below 4 °C or above 60 °C.\[43\] **For fried rice, the assistant should confirm the rice was chilled promptly and is within the local time limit (24 h under UK guidance).**
- **Poultry and minced meat.** Short raw shelf life (2 days, per FSIS).\[38\] Leftovers follow the general rules.
- **Fish and shellfish.** Cooked fish leftovers 3–4 days (FSIS).\[38\] Raw fish has the shortest limit. Acid "cooking" (ceviche) is not a safety step.
- **Cooked leafy greens and nitrate-rich vegetables (spinach, chard, beetroot).** Bacteria convert nitrate to nitrite when cooked greens are kept warm or cool slowly. BfR advises cooling such leftovers quickly and keeping them refrigerated.\[44\]\[45\] Its English FAQ goes further: spinach cooked once should not be reheated.\[46\] German consumer advice generally allows careful reheating of properly chilled leftovers by adults, but **not for infants**, who are sensitive to nitrite.\[47\]\[48\]
- **Large batches** (stews, stocks). The main risk is slow cooling (*Clostridium perfringens*, *B. cereus*). Divide into shallow containers (FSIS, FSA).\[41\]

### Where authorities differ and what the assistant should do

- **Fridge life: 2 days (UK) vs. 3–4 days (US).** Show the user's local authority's figure.\[34\] With no locale, default to the **stricter 2-day rule** for leftovers and 24 h for rice.
- **Reheating standard: a temperature (US 74 °C; BfR 70 °C for 2 min; FSAI/Hong Kong 75 °C) vs. "steaming hot" (UK).** In recipes, give both: a probe temperature and the visual cue.
- **Number of reheats: UK, Hong Kong and German consumer advice say once; FSIS sets no limit.** Always advise reheating only the portion being eaten.
- **Rice:** the UK sets a rice-specific 24-hour limit, while the US treats rice as a general leftover.\[32\] Treat rice as a special case everywhere.

## 7. Ingredient Recognition from Photos

### What current benchmarks show (2025–2026)

**Naming common items is fairly good.**
- *Pic2Plate* (Soekamto et al., 2025, *Sensors*): GPT-4o's ingredient-detection module scored precision 0.83, recall 0.91, F1 0.86 and accuracy 0.77, beating Llama 3.2 Vision and FoodSAM.\[1\]\[49\] The evaluation mostly used dish images (FoodSeg103), not fridge interiors.\[50\]
- *January Food Benchmark* (2025; 1,000 meal images): GPT-4o reached an ingredient F1 of 0.737.\[51\]
- *FoodNExTDB* study (Romero-Tapiador et al., CVPR 2025 workshop): closed-source models exceeded 90% expert-weighted recall on images showing a single food product.\[52\]
- **None of these measures cluttered fridge or pantry scenes.** I found no peer-reviewed benchmark of current multimodal LLMs on real fridge or pantry photos. Older work, such as *The Multimodal and Modular AI Chef* (arXiv:2304.02016, 2023), trained a custom detector on staged fridge images (30 foods) rather than evaluating general VLMs.\[53\]

**Quantity is weak.**
- *SFOOD* (Xu et al., 2025, arXiv:2507.04412). Counting mean absolute error: GPT-4o 3.23 and Gemini-1.5-flash 7.40, against 0.46 for humans. For weight estimation, GPT-4o and Gemini gave no numerical answer 93.5% and 98% of the time. The authors note that models "tend to refuse to count the exact number in situations with a large quantity and make mistakes even with small quantities when the arrangement is challenging."\[2\]
- *NutriBench-Kitchen* (Wei et al., 2026, arXiv:2609.07135; 1,500 verified questions from 160 cooking videos).\[3\]
  - On ingredient entry (identifying an ingredient and estimating its quantity): Gemini 2.5 Pro scored 46.7% with hints and 14.7% without; GPT-4o 30.7% and 16.7%; humans 92.5% and 88.0%.\[3\]
  - Average across all tasks: Gemini 2.5 Pro 61.1%, GPT-4o 47.7%, humans 92.0%.\[3\]
  - Errors cluster in "quantitative ingredient estimation" and in tracking ingredients that were "partially occluded, transferred between containers, or visually ambiguous after mixing."\[3\]
- *OmniFood-Bench* (Jiang et al., 2026, arXiv:2607.08423; not peer-reviewed). Portion-weight error (MAPE) for raw fruit and vegetables was 146–196% for frontier models (GPT-5.1, Gemini-3-flash, Claude-Sonnet-4). The authors trace this to scale ambiguity: without a reference object, a model "cannot distinguish between a cherry tomato and a regular tomato." Weight-estimation accuracy collapsed as the number of items per image rose from 1 to 6.\[54\]

**Condition and freshness are unreliable.** In SFOOD, accuracy against human raters was:

| Judgment | GPT-4o | Gemini-1.5-flash | Best model | Humans |
|---|---|---|---|---|
| Ripeness / maturity | 0.50 | 0.64 | Qwen2-VL-72B 0.67 | 0.85\[2\] |
| Spoilage status | 0.67 | 0.77 | Qwen2-VL-7B 0.85 | 0.91\[2\] |
| Edibility recommendation | 0.54 | 0.67 | — | 0.87\[2\] |

SFOOD used single-fruit images, not fridge scenes, so real-world accuracy is likely lower.\[2\]

**Packaged goods and look-alikes are the main recognition failures.**
- OmniFood-Bench reports ingredient-match rates for packaged food of only 21–45% across models. The authors attribute this to packaging diversity and to reading labels (OCR) under variable lighting; this explanation is their hypothesis, not a tested result.\[54\]
- In retail product retrieval, a 2026 zero-shot study of 190 open-source VLMs (Maminta & Atienza, arXiv:2605.18029) found 94.5% Recall@5 but a 17.5-point drop at Recall@1. In other words, models get the category right but confuse near-identical products (similar sauces, yogurts, cheeses).\[55\]
- SFOOD likewise documents confusion between visually similar categories.\[2\]
- Typical look-alikes in fridges: cream vs. yogurt in unmarked tubs, parsley vs. cilantro, spring onion vs. leek, white miso vs. tahini in jars, cooked chicken vs. tofu in containers. This last group is practitioner observation consistent with the benchmark findings.

**Typical failure modes to design for:**
- occlusion (items behind or inside others)
- opaque containers and leftovers in tubs
- door shelves photographed at an angle
- poor fridge lighting and glare
- tiny or partial items
- regional products absent from training data (WorldCuisines, Winata et al., 2025, documents uneven performance across global cuisines)
- scale ambiguity
- hallucinating "typical" fridge items that aren't there

### Best practices for confirmation (practitioner recommendations built on the evidence above)

1. **Show a structured, editable inventory before suggesting any recipes.** Group it by confidence: "I can see: eggs, peppers, cheddar…", "I think: cream (or yogurt?)", "Not sure: two containers on the bottom shelf, what's in them?"
2. **Don't infer quantity or freshness for key ingredients; ask.** A question like "About how many eggs? Is the spinach still fresh?" is cheap, and the benchmarks show models are weakest exactly here.
3. **Ask only about what changes the decision.** Confirm items that will be main ingredients or that carry safety risk (cooked rice and its age, raw poultry or fish). Don't interrogate the user about condiments.
4. **Use labels when they're readable, but say when you're guessing.** If a label isn't legible, describe the item ("a jar of red paste, maybe harissa or gochujang?").
5. **Invite a second photo or a typed correction** for unclear areas (door shelves, the crisper drawer).
6. **Keep a persistent inventory** that is updated by confirmations and cooking events. NutriBench-Kitchen found that structured food-state memory raised a small model from 53.4% to 62.3% on average, which supports explicit inventory tracking over re-reading images each time.\[3\]
7. **Never decide food safety from a photo.** Phrase condition statements as prompts ("check the chicken's use-by date") rather than verdicts.

## 8. Presenting Options

### What the choice-overload research shows

- The well-known jam and chocolate studies (Iyengar & Lepper, 2000) found that 24–30 options reduced purchases or satisfaction compared with 6.
- A meta-analysis by Scheibehenne, Greifeneder & Todd (2010) found the *average* effect across studies to be "virtually zero."\[56\]
- Chernev, Böckenholt & Goodman (2015) analysed 99 observations (N = 7,202) and found that choice overload is real and significant **when moderators are taken into account**.\[4\]\[57\] The four moderators are:
  - choice-set complexity
  - decision-task difficulty
  - preference uncertainty
  - whether the person wants to minimize effort
- A fridge-clearing request triggers all four: options are multi-attribute (time, ingredients, missing items, cuisine), the user is often tired, preferences are vague ("something quick"), and the goal is to minimize effort.
- In food service specifically, Johns, Edwards & Hartwell (2013) found people's ideal number of choices per menu category was about **6 for quick-service** and **7–10 for fine dining**.\[58\] Those are menus to scan, though, not options to evaluate; an assistant's suggestions are each richer and harder to compare.

### Recommendations

- **Default to 3 suggestions, with a "show more" option (up to about 5).** *Evidence status:* the moderator evidence (Chernev et al., 2015) supports a small set for complex, effortful choices. The number 3 itself is a practitioner convention common in meal-kit and recipe apps, not an empirically derived optimum, and should be A/B tested.
- **Make the options differ in "shape", not just in flavor.** For example: one one-pan or stovetop dish, one oven or "hands-off" dish, and one cold or very fast dish. Or vary cuisine. Clearly different options reduce complexity; three near-identical stir-fries create overload without real choice.
- **Describe each option in a fixed, scannable format.** Name the dish plus a one-line sensory hook. Then:
  - ⏱ total time and active time
  - ✅ which of *your* ingredients it uses, with the priority ones highlighted
  - 🛒 what you'd need to buy (ideally "nothing")
  - difficulty
  - dietary tags

  A consistent format turns the comparison into an attribute grid, which lowers task difficulty (one of the four moderators).
- **Rank and recommend.** Put a clear "best match" first (uses the most at-risk items, needs no shopping). Choice research shows a dominant option reduces overload, and it supports the "use it up" nudge from Section 2.\[59\]
- **Reduce uncertainty with one optional question**, not a questionnaire: "Fancy something warm and comforting or fresh and light?" Ask it only when the inventory supports very different directions.
- **Generate the full recipe only after the user picks**, as the brief specifies. Keep the full recipe consistent with the confirmed inventory, the pantry assumptions and the user's local safety rules (Section 6).

## Recommendations (Implementation Summary)

1. **Pipeline:**
   - Get the input (text, mood, photo).
   - Draft an inventory with confidence levels.
   - Confirm key items, quantities and condition.
   - Tag each item's perishability tier.
   - Fill template slots, giving the priority items the main roles.
   - Score candidates by priority ingredients used, items to buy, time, and fit with stated mood.
   - Present 3 clearly different options.
   - Generate the full recipe with function-aware substitutions and local safety notes.
2. **Knowledge layers to build:**
   - a template library (slots, ratios, constraints, seasoning checklist)
   - an ingredient ontology with function tags, perishability tier and allergen flags
   - a substitution graph with "fails in" edges for baking, emulsions and set custards
   - a locale-aware safety rule table (FSIS / FSA / BfR)
   - per-user pantry and inventory memory
3. **Conservative defaults:**
   - With no locale, use the strictest safety rule.
   - Never make safety judgments from images.
   - Treat allergies as hard constraints with cross-contact warnings.
   - Use conservative substitution in baking.
4. **Measure:** run A/B tests on the number of options (3 vs. 5), confirmation friction, and "used the priority item" rates. The food-waste literature shows self-reported waste is biased, so use behavioral metrics.

## Caveats

- **Evidence quality varies across sections.**
  - Sections 6 (official guidance) and 7–8 (benchmarks, meta-analyses) are the best-sourced.
  - Templates, pantry assumptions and most substitution ratios come from culinary texts and test kitchens. They are well established in practice but not experimentally validated, and I have marked them "practitioner."
- **No peer-reviewed benchmark yet measures current multimodal LLMs on real fridge or pantry photos.** The recognition figures come from dish images, single-fruit images or cooking videos. Several key 2026 sources (NutriBench-Kitchen, OmniFood-Bench, the grocery-retrieval study) are arXiv preprints that have not been peer reviewed. Model rankings change quickly, so re-benchmark on your own labelled fridge-photo set before launch.
- **The food-waste intervention evidence relies mostly on non-randomised designs and self-reported waste.** No study has tested an AI cooking assistant as an intervention.
- **Safety guidance changes.** The figures here reflect the authorities' published consumer pages at the time of writing. Rules for vulnerable groups (pregnancy, infants, immunocompromised people) are stricter and should be handled explicitly.
- **BfR's own wording on reheating spinach is inconsistent:** a strict "do not reheat" in the English FAQ vs. "cool quickly and refrigerate" in the German material. The conservative reading is the safer default for an international product.

## Quellen

1. [Pic2Plate: A Vision-Language and Retrieval-Augmented Framework for Personalized Recipe Recommendations](https://doi.org/10.3390/s25020449)
2. <https://arxiv.org/pdf/2507.04412>
3. <https://arxiv.org/pdf/2609.07135>
4. [Choice Overload, Explained](https://www.thewhyweproject.com/concepts/choice-overload)
5. [Ratio](https://booksummaryproject.com/book31)
6. [Ratio PDF Michael Ruhlman](https://cdn.bookey.app/files/pdf/book/en/ratio.pdf)
7. [Cook Like a Chef: Use Ratios, Not Recipes \<\< Food Hacks :: WonderHowTo](https://food-hacks.wonderhowto.com/how-to/cook-like-chef-use-ratios-not-recipes-0155785/)
8. [Understanding household food waste in the UK: the Household Food Management Survey 2025](https://www.wrap.ngo/resources/report/understanding-household-food-waste-uk-household-food-management-survey-2025)
9. [What Nudge Techniques Work for Food Waste Behaviour Change at the Consumer Level? A Systematic Review](https://www.mdpi.com/2071-1050/13/19/11099)
10. [Aquafaba, wastewater from chickpea canning, functions as an egg replacer in sponge cake](https://academic.oup.com/ijfst/article/53/10/2247/7804983)
11. [Aquafaba as an egg white substitute in food foams and emulsions: Protein composition and functional behavior - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0268005X18321349)
12. [Study of the Technological Properties of Pedrosillano Chickpea Aquafaba and Its Application in the Production of Egg-Free Baked Meringues](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9957096/)
13. [Substituting whole wheat flour in yeasted bread recipes](https://www.kingarthurbaking.com/blog/2014/02/28/yeast-bread-rolls-and-pizza)
14. [Substitute whole wheat for all-purpose flour - Get the Good Stuff](https://goodstuff.recipes/substitute-whole-wheat/)
15. [Whole Grains](https://www.kingarthurbaking.com/learn/guides/whole-grains)
16. [King Arthur 100% Whole Wheat Flour](https://mycozyfarm.com/products/king-arthur-whole-wheat-flour-case-of-12-2)
17. [How to substitute whole wheat for white flour in baking](https://www.kingarthurbaking.com/blog/2020/06/22/how-to-substitute-whole-wheat-for-white-flour-in-baking)
18. [Whole Wheat Flour Swaps](https://culinaryjourneysllc.com/2026/02/04/whole-wheat-flour-swaps/)
19. [How to substitute Gluten-Free Bread Flour for regular flour](https://www.kingarthurbaking.com/blog/2023/06/13/how-to-substitute-gluten-free-bread-flour-for-regular-flour)
20. [7 Whole Wheat Flour Substitutes for White Flour](https://www.bakingsubs.com/blog/whole-wheat-flour-substitutes-for-white-flour)
21. [Staying Sweet with Less Sugar](https://bakerpedia.com/staying-sweet-with-less-sugar/)
22. [Texture, rising and binding hard to replicate when reducing sugar](https://www.bakingbusiness.com/articles/61612-texture-rising-and-binding-hard-to-replicate-when-reducing-sugar)
23. [Sugar reduction in bakery products: Current strategies and sourdough technology as a potential novel approach - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0963996919304612)
24. [Sugar reductions on the sensory characteristics, quality, and emotional profile of pound cakes](https://academic.oup.com/ijfst/article/61/2/vvag138/8732508)
25. [Bulking, modulation and mouthfeel: Why bakery sugar reduction needs more than a sweetener swap](https://www.foodingredientsfirst.com/news/bakery-sugar-reduction-kerry-adm-samyang.html)
26. [Sodium, but not potassium, blocks bitterness in simple model chicken broths](https://link.springer.com/article/10.1007/s13197-019-03770-1)
27. [Sodium Reduction Through Sensory Interactions With NaCl: Strategies and Underlying Mechanisms](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12231224/)
28. [Keeping the taste, reducing the salt](https://news.cahnrs.wsu.edu/article/keeping-the-taste-reducing-the-salt/)
29. [Reducing Sodium in Foods: The Effect on Flavor - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3257639/)
30. [How to chill, freeze and defrost food safely - GOV.UK](https://www.gov.uk/government/publications/how-to-chill-freeze-and-defrost-food-safely/how-to-chill-freeze-and-defrost-food-safely)
31. [1 of 4 Bacillus cereus MICROBIAL FACTSHEET SERIES](https://www.fsai.ie/getmedia/4f2f6561-441a-4692-a112-b03e660069ca/bacillus-cereus-factsheet-2016-final-accessible.pdf?ext=.pdf)
32. [Leftover rice in the fridge, how long it lasts and reheating](https://thecookinghacks.com/22356/leftover-rice-in-the-fridge-how-long-reheat/)
33. [Heat-stable Toxins from \<I\>Bacillus cereus\</I\> and \<I\>Staphylococcus aureus\</I\>: Why Cooked Food Should Not Be Left at Room Temperature for Too Long](https://www.cfs.gov.hk/english/multimedia/multimedia_pub/multimedia_pub_fsf_193_01.html)
34. [How long leftovers really last in the fridge · plate.](https://www.getplate.co/blog/how-long-do-leftovers-last)
35. [How to chill, freeze and defrost food safely](https://www.food.gov.uk/safety-hygiene/how-to-chill-freeze-and-defrost-food-safely)
36. [How Many Times Is It Safe to Reheat Food? UK Food Safety Tips](https://hcalondon.co.uk/blog/how-many-times-is-it-safe-to-reheat-food/)
37. [Darf man Spinat aufwärmen?](https://eatsmarter.de/ernaehrung/gesund-ernaehren/spinat-aufwaermen)
38. [Keep Food Safe! Food Safety Basics](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/steps-keep-food-safe)
39. [Home food fact checker](https://www.food.gov.uk/safety-hygiene/home-food-fact-checker)
40. [Bacillus cereus-Bakterien in Lebensmitteln können Magen- ...](https://www.bfr.bund.de/cm/343/bacillus-cereus-bakterien-in-lebensmitteln-koennen-magen-darm-erkrankungen-verursachen.pdf)
41. [Clostridium perfringens & Bacillus cereus: Cooling Controls](https://foodsafetyhq.com.au/food-safety-guides/clostridium-perfringens-bacillus-cereus-cooling)
42. [Bacillus cereus: Reis aufwärmen das ist zu beachten](https://www.pta-forum.de/reis-aufwaermen-das-ist-zu-beachten-165918/)
43. [Prevention of Foodborne Illness When Keeping Food Hot](https://zenodo.org/records/13736344)
44. [FAQ - Nitrat und Nitrit in Gemüse](https://www.bfr.bund.de/cm/343/fragen-und-antworten-zu-nitrat-und-nitrit-in-lebensmitteln.pdf)
45. [Diese Lebensmittel sollten Sie besser nicht wieder aufwärmen](https://www.gmx.net/magazine/ratgeber/essen-trinken/lebensmittel-aufwaermen-34462906)
46. [Nitrat und Nitrit in Gemüse: Abwechslungsreiche Auswahl ...](https://www.bfr.bund.de/en/service/frequently-asked-questions/topic/frequently-asked-questions-on-nitrate-and-nitrite-in-food/)
47. [Darf man Spinat wieder aufwärmen? - Spektrum der Wissenschaft](https://www.spektrum.de/frage/darf-man-spinat-wieder-aufwaermen/1550934)
48. [Darf man Spinat aufwärmen? - FITBOOK](https://www.fitbook.de/ernaehrung/spinat-aufwaermen)
49. [Pic2Plate: A Vision-Language and Retrieval-Augmented Framework for Personalized Recipe Recommendations](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11768646/)
50. [Pic2Plate: A Vision-Language and Retrieval-Augmented Framework for Personalized Recipe Recommendations - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11768646/)
51. [January Food Benchmark (JFB): A Public Benchmark Dataset and Evaluation Suite for Multimodal Food Analysis](https://arxiv.org/pdf/2508.09966)
52. [Are Vision-Language Models Ready for Dietary Assessment ...](https://openaccess.thecvf.com/content/CVPR2025W/MTF/papers/Romero-Tapiador_Are_Vision-Language_Models_Ready_for_Dietary_Assessment_Exploring_the_Next_CVPRW_2025_paper.pdf)
53. [THE MULTIMODAL AND MODULAR AI CHEF: COMPLEX RECIPE GENERATION FROM IMAGERY](https://arxiv.org/pdf/2304.02016)
54. <https://arxiv.org/pdf/2607.08423>
55. [\[2605.18029\] What Matters for Grocery Product Retrieval with Open Source Vision Language Models](https://arxiv.org/abs/2605.18029)
56. [409 2010 by JOURNAL OF CONSUMER RESEARCH, Inc. ●Vol. 37 ●October 2010](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf)
57. [Choice overload: A conceptual review and meta‐analysis - Chernev - 2015 - Journal of Consumer Psychology - Wiley Online Library](https://myscp.onlinelibrary.wiley.com/doi/abs/10.1016/j.jcps.2014.08.002)
58. [Menu Choice: Satisfaction or Overload?: Journal of Culinary Science & Technology: Vol 11 , No 3 - Get Access](https://www.tandfonline.com/doi/full/10.1080/15428052.2013.798564)
59. [Overchoice](https://en.wikipedia.org/wiki/Overchoice)
