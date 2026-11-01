# Building an AI Cooking Assistant for International Home Cooks: A Research Report

**Scope and evidence note.** This report separates, where possible, claims supported by peer-reviewed research, official authority guidance, and published benchmark studies from claims grounded in culinary practitioner experience or textbook codification. Those latter claims are marked “practitioner/textbook” or “practitioner heuristic.” The distinction matters for a cooking assistant: empirical findings can license confident defaults; practitioner heuristics should be surfaced as suggestions with rationale, not as rules.

## 1. FLEXIBLE DISH TEMPLATES

### 1.1 What a “template” is, and why it belongs in an AI assistant

Experienced cooks do not retrieve recipes; they instantiate structures. A template specifies (a) a **structural requirement**—what must be present for the dish to be that dish—and (b) a **flavor logic**—the acid–fat–salt–aroma architecture that prevents a random assemblage from tasting like a random assemblage. The most influential codification of this idea is Ruhlman’s _Ratio_, which argues that cooking is “not about recipes but rather about basic ratios and fundamental techniques,” giving 33 foundational ratios including pie dough at 3 parts flour : 2 parts fat : 1 part water, bread at 5 parts flour : 3 parts water, and cookie dough at 1 part sugar : 2 parts fat : 3 parts flour . Ruhlman’s ratios are practitioner synthesis rather than experimental findings, but they are widely used in culinary training and are a defensible basis for an assistant that needs to reason about structure without a recipe.

McGee’s _On Food and Cooking_ provides the complementary mechanistic layer: once a cook understands _why_ a method works, they can “modify it with intent, substituting ingredients, adjusting temperatures, or choosing alternate processes to reach a desired texture or flavor” . For an AI system, the practical translation is: represent each template as a set of **slots** (structural base, protein, vegetable bulk, fat, acid, umami, aromatic, textural finish) plus **constraints** (moisture budget, bind, leaven, set). Then match fridge contents to slots, flag empty slots, and propose the minimum purchase to close the gap.

### 1.2 Template-by-template structural and flavor requirements

The table below synthesizes culinary-textbook and practitioner knowledge; the “flavor logic” column reflects the acid–fat–salt–aroma framework that test kitchens and cookbook authors consistently use (e.g., the Samin Nosrat framework popularized in _Salt, Fat, Acid, Heat_; practitioner synthesis).

| Template                | Structural requirement                                                                                      | Ingredient categories accepted                                                                               | What makes it taste deliberate rather than random                                                                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Frittata / omelette** | Eggs as set matrix; fat for release; optional dairy for tenderness                                          | Vegetables (cooked or blanched first if watery), cooked potatoes, cheeses, cured meat, herbs, leftover pasta | Salt in the eggs _before_ cooking (practitioner/textbook: allows uniform seasoning and avoids weepy surface); a sharp finish (vinegar, lemon, herb oil); avoid raw watery vegetables that dilute the egg set |
| **Stir-fry**            | High heat, dry surface, fast cooking; protein and vegetables cut to uniform small size                      | Any quick-cooking protein, firm vegetables, aromatics, cooked noodles/rice added at the end                  | _Wok hei_–style browning requires a dry ingredient surface and adequate fat; a sauce with salt–acid–sweet–umami balance (soy, vinegar, sugar, fermented paste) rather than a single liquid                   |
| **Fried rice**          | Cooked, cooled, relatively dry rice; hot fat; fast toss                                                     | Leftover proteins, vegetables, eggs, aromatics                                                               | Day-old rice (practitioner/textbook) prevents steaming; fish sauce/soy + acid + white pepper; scallion added late for freshness                                                                              |
| **Soup**                | Liquid base (water, stock, tomato, dairy, tamarind, dashi); a body-building element                         | Almost anything, but starchy vegetables thicken; acid-sensitive dairy curdles at boil                        | Build an aromatic base first (onion/garlic/ginger/leek); salt in layers; finish with acid and a fat (olive oil, butter, sesame oil)                                                                          |
| **Stew**                | Low, slow, moist heat; collagen-bearing or fibrous protein/vegetable; enough liquid to braise but not drown | Tough cuts, root vegetables, legumes, dried fruit, spices                                                    | Brown the protein or vegetables first (Maillard); bloom spices in fat; acid (tomato, wine, vinegar) balances long-cooked flavors; salt early enough to penetrate                                             |
| **Curry**               | Aromatic base (allium + ginger + spice) cooked in fat; liquid; protein/vegetable                            | Meat, legumes, paneer, coconut milk, yogurt (stabilized), tomatoes, tamarind                                 | Frying the spice mix in fat (tadka/tempering) rather than dumping spices into liquid; acid and heat balanced; yogurt must be stabilized against splitting                                                    |
| **Gratin**              | Layers of vegetable or starch; a dairy or dairy-alternative sauce; a browned top                            | Potatoes, root vegetables, squash, greens, pasta, fish                                                       | Season each layer; the sauce must be salted and nutmeg/aromatic; the top needs fat and a starch or cheese to brown                                                                                           |
| **Pasta**               | Starch + enough water to hydrate; a sauce that clings                                                       | Vegetables, legumes, cheese, egg, cured meat, nuts                                                           | Emulsify the sauce with pasta water (starch + fat); finish pasta in the sauce; acid and salt at the end; do not overdrain                                                                                    |
| **Grain bowl**          | A cooked grain; a protein; a vegetable; a sauce                                                             | Almost any grain (rice, farro, millet, couscous), roasted/raw vegetables, legumes, eggs, tofu                | Contrasting textures (crunchy/creamy) and a sauce with acid + fat + salt; grains seasoned while warm                                                                                                         |
| **Savory pancake**      | Flour + liquid + binder + leavener (or a naturally setting batter such as chickpea flour)                   | Grated vegetables, herbs, leftover protein, cheese                                                           | Rest the batter (practitioner/textbook); cook hot enough to set before the center dries; serve with a sharp condiment                                                                                        |
| **Hash**                | Cooked starch + protein + fat + high heat for crust formation                                               | Leftover potatoes, meat, vegetables                                                                          | Do not crowd the pan (steam prevents crust); salt in stages; a fried egg or acid-based sauce on top                                                                                                          |
| **Pie / tart**          | Dough with sufficient fat and hydration; a filling with controlled moisture                                 | Vegetables, cheese, eggs, cured meat, fruit                                                                  | Blind-bake or par-bake watery fillings; season the filling more aggressively than you would eat it alone; a acid note in the filling                                                                         |
| **Salad**               | A base (leaf, grain, legume, or shredded vegetable); a dressing; a textural element                         | Raw or cooked vegetables, herbs, cheese, nuts, leftover protein, grains                                      | Dress leaves lightly and season them directly; acid–fat balance in the dressing; salt the watery components separately                                                                                       |

**Sources for the template concept:** Ruhlman (ratios and structure) ; McGee (mechanism) ; Bittman’s _Kitchen Matrix_ and Heather Crosby’s _Pantry to Plate_, both of which explicitly organize cooking around flexible templates rather than fixed recipes ; Pam Anderson’s _How to Cook Without a Book_ (ratio-based improvisation) .

### 1.3 Published approaches to improvisational cooking

Three families of published approach are relevant to an AI assistant:

1. **Ratio-based cooking** (Ruhlman; Anderson): the cook learns a small set of weight ratios and scales them. This is the most _computable_ approach and is therefore the easiest to implement in software, but it is strongest for doughs, batters, stocks, and sauces and weaker for dishes whose structure depends on the properties of specific ingredients (e.g., a frittata depends on egg-set behavior, not a simple ratio).
2. **Template/matrix cooking** (Bittman; Crosby): the cook chooses a template and fills slots. This is the most _natural_ approach for fridge-driven suggestion because it maps cleanly to the “what do I have?” question.
3. **Pantry cooking / leftovers cooking** (widely codified in consumer guidance from food-safety authorities and in cookbooks such as _Pantry to Plate_): the cook treats leftovers as ingredients with their own constraints (already cooked, already seasoned, already moist) rather than as neutral raw materials. EFSA’s Safe2Eat workshops and the UK FSA’s home food fact checker both explicitly frame leftovers as usable ingredients subject to safety rules rather than as waste .

**Recommendation for the assistant:** Use a hybrid. Represent a small library of 12–15 templates with slot constraints. For each template, pre-compute “flavor-logic checks” (does the proposed dish have a salt source, an acid source, a fat, and an aromatic/base note?). If a check fails, the assistant should either suggest the missing pantry item or explicitly say the dish will taste flat without it. This is a practitioner-informed design choice, not an empirically validated one, but it aligns with the ratio/template literature and with how test kitchens describe recipe development.

## 2. PRIORITIZING INGREDIENTS

### 2.1 Perishability and the decision to use first

A cooking assistant should not rank ingredients by “likelihood of use” but by **risk of loss**. The empirical literature on household food waste consistently identifies **overbuying, poor planning, and confusion over date labels** as major drivers, with fresh milk, meat, fish, fruit, vegetables, and bakery products among the most wasted categories . The assistant’s prioritization logic should therefore combine:

- **Category baseline shelf life** (fresh fish and shellfish: 1–2 days in the refrigerator; poultry and ground meat: 1–2 days; other red meat: 3–5 days; cooked leftovers: 3–4 days) .
- **Opened-state shelf life** (an opened jar of tomato sauce, a cut avocado, a opened carton of milk): these are _not_ the same as the unopened product’s date and should be treated as high-priority items.
- **Visible/olfactory age signals**: the UK FSA explicitly cautions that the “sniff test” is not safe for foods with a use-by date because the pathogens that cause food poisoning are not smellable; for best-before foods, smell and visual cues (mold, texture change) are legitimate quality indicators .
- **Date-label semantics**: “use by” is a safety date; “best before” is a quality date. The FSA states that food with a best-before date can be eaten after the date, though quality may suffer . The EU waste-reduction literature likewise identifies confusion between “use by” and “best before” as a contributor to household waste .

A practical ranking heuristic for the assistant (practitioner synthesis, consistent with the above):

1. Fresh fish, shellfish, and cut fruit/vegetables → highest priority.
2. Poultry, ground meat, fresh dairy opened >3–4 days, cooked leftovers at day 3–4.
3. Fresh herbs, leafy greens, soft fruit, bread.
4. Whole cuts of meat, hard cheese, root vegetables, hardy produce.
5. Pantry staples, frozen goods, unopened shelf-stable items.

### 2.2 Centering a dish around a priority ingredient

Centering is a culinary-practitioner concept with empirical support from the food-waste intervention literature. The most effective consumer-level interventions are not information-only campaigns; they are **multi-component** and include **self-reporting, coaching, and nudges** that make the user’s own waste visible and make the next action concrete . A cooking assistant that says “your spinach is the item most at risk; here are three dishes where spinach is the center rather than a garnish” is performing a coaching-and-nudging function, not merely a search function.

The intervention evidence specifically supports:

- **Self-reporting** of wasted food, which produced reductions maintained five weeks after the intervention .
- **Coaching combined with self-reporting**, which was more effective than self-reporting alone .
- **Nudges** (choice-architecture changes), which are low-cost and effective especially in public settings, though the evidence in private households is less consistent .
- **Retailer-level interventions** that help consumers reduce waste at home .

One important negative finding: a 166-day household trial that compared purchasing-planning and cooking-planning interventions found that the interventions were **not effective beyond the reduction observed in the control group**, but there was evidence of a **mere-measurement effect**—households reduced waste simply because they were being measured . For an AI assistant, this is a caution: tracking and feedback may help, but the assistant should not overclaim that its suggestions _cause_ waste reduction. A more defensible framing is that the assistant reduces the **effort and cognitive load** of using at-risk ingredients, and that this is a plausible mechanism, not a proven one.

### 2.3 Signs of age and the assistant’s language

The assistant should use **hedged, safety-first language**:

- For use-by items: “This is past its use-by date; food-safety authorities advise not eating it.”
- For best-before items: “This is past its best-before date; it may still be safe but quality may be lower—check for mold or off odors.”
- For visible mold on soft foods: discard (practitioner/textbook; mold hyphae can penetrate soft matrices).
- For sprouting potatoes: the FSA allows eating after cutting off sprouts and removing green/rotten parts .

## 3. PANTRY ASSUMPTIONS

### 3.1 What can be assumed, and what cannot

There is no globally valid pantry baseline. Even the category “salt, oil, basic spices” varies substantially: a US pantry is likely to include baking soda at American quantities, measuring cups, and a high-variety spice rack; an Irish or UK pantry may include tinned tomatoes, good butter, porridge oats, and a brown sauce ; an East Asian pantry may include soy sauce, rice vinegar, sesame oil, and mirin; a South Asian pantry may include cumin, coriander, turmeric, ginger, and dried chilies . Cross-cultural flavor-mapping work notes that the **primary acid** is a powerful variable—switching from lemon (Mediterranean) to lime (Southeast Asian/Mexican) to rice vinegar (East Asian) “repositions the entire dish” .

A defensible three-tier assumption structure for the assistant (practitioner synthesis informed by the cross-cultural pantry literature):

**Tier 1 — near-universal, assume present unless told otherwise:** salt, a cooking oil, water, a heat source, a knife, a pan. Even here, the _type_ of oil (olive, neutral, coconut, mustard) and the _type_ of salt (fine, coarse, kosher) change results.

**Tier 2 — widely present but regionally variable:** onion, garlic, black pepper, sugar, flour, eggs, butter or a local fat, soy sauce or a local fermented seasoning, vinegar or citrus, a stock cube or bouillon, dried herbs.

**Tier 3 — cuisine-specific and unsafe to assume:** specific spices (cumin, coriander, smoked paprika, garam masala), specific acids (tamarind, sumac, rice vinegar), specific umami sources (fish sauce, miso, anchovy, dried shrimp), specific thickeners (cornstarch, arrowroot, gram flour), specific dairy (crème fraîche, labneh, paneer).

### 3.2 Ask, assume, or offer alternatives?

The assistant should use a **tiered interaction policy**:

- **Tier 1:** assume, but state the assumption in the response (“I’m assuming you have salt and a neutral oil”).
- **Tier 2:** assume with a visible, one-tap correction path (“I’m assuming you have onion and garlic—tap to remove”).
- **Tier 3:** **ask** before relying on it, or design the dish so that the cuisine-specific item is optional and offer a Tier-2 substitute. For example, instead of assuming fish sauce, offer “soy sauce or salt” as the umami layer, while noting that the flavor profile will shift.

This is a **practitioner recommendation**, not an empirically validated protocol. It is grounded in the observation that the cost of a wrong assumption is asymmetric: assuming salt is low-cost; assuming a cuisine-specific fermented paste is high-cost because the user may not have it and may not know what to do without it.

### 3.3 Uncertainty handling as a design principle

The assistant should never present a dish as “using only what you have” if it has silently assumed a Tier-3 item. A useful rule: **list every assumed item explicitly**, grouped as “assuming you have” and “you’ll need to buy.” This is consistent with the consumer-behavior finding that choice overload and confusion rise when options are complex and similar ; a short, clearly enumerated assumption list reduces decision complexity.

## 4. SUBSTITUTIONS AND THEIR CONSEQUENCES

### 4.1 The functional framework

The most reliable way to reason about substitutions is by **function**, not by name. A substitution is safe when the replacement performs the same techno-functional role in the matrix: structure, moisture, fat, leavening, binding, emulsification, acidity, sweetness, or flavor. This is the framework used in the food-science literature on egg replacers, fat replacers, and gluten-free baking . McGee’s mechanistic approach supports the same logic: once the cook understands why an ingredient works, substitution becomes intentional rather than trial-and-error .

### 4.2 Category-by-category consequences

**Fats.** Fat carries flavor, creates tenderness, conducts heat, and in baking shortens gluten and traps air during creaming. Replacing butter with a liquid oil in a cake changes the creaming step (liquid oil cannot trap air the same way) and typically produces a denser, moister crumb; replacing solid fat with a high-moisture purée (applesauce, prune purée) reduces fat but adds water and sugar, which can make cookies cakey and increase browning. Food-science reviews of fat replacers emphasize that starch- and mucilage-based replacers can mimic mouthfeel but not the full structural role of solid fat . **Reliable swaps:** olive oil for butter in sautéing and in rustic cakes (with texture change); neutral oil for melted butter in muffins. **Reliable failures:** substituting oil 1:1 for butter in laminated dough or buttercream; using water-based purées in shortbread.

**Dairy and plant-based dairy.** Milk contributes water, lactose (browning), and protein; cream contributes fat and emulsified structure. Plant milks vary enormously: almond milk is low-protein and can curdle in acid; oat milk is higher in starch and browns more; soy milk is closest to dairy milk in protein and is the most reliable 1:1 swap in custards and sauces (practitioner/textbook). Coconut milk adds fat and a distinct flavor; it is not a neutral swap in béchamel. **Reliable failures:** using a low-fat plant milk in a high-acid sauce without stabilization; swapping coconut milk for dairy milk in a delicate pastry cream.

**Eggs.** Eggs are the hardest multi-functional ingredient to replace because they foam, emulsify, gel, and bind . In cakes, egg replacers that work for binding (flax egg, chia egg) do not provide the same aeration as whipped egg whites; aquafaba can whip and provide lift but its foam is less stable than egg-white foam and is sensitive to fat and acid . The peer-reviewed review on egg functionality concludes that traditional egg replacement is trial-and-error and that a mechanistic, colloidal-structure approach is needed because plant proteins interact unpredictably with batter components . **Reliable swaps:** flax egg (1 tbsp ground flax + 3 tbsp water) for binding in cookies and muffins; aquafaba (3 tbsp = 1 egg) for lift in light cakes and meringue-style preparations, with the caveat that stability is lower . **Reliable failures:** replacing eggs in a custard or a quiche where the egg is the setting agent; replacing whole eggs with egg whites in a recipe that depends on yolk fat for tenderness.

**Flours (including whole-grain vs. refined).** Whole-grain flours absorb more water than refined flour because of bran and germ, so a 1:1 swap by volume typically produces a dry, dense result; the practical adjustment is to increase liquid or reduce the flour weight, and to rest the batter to allow hydration (practitioner/textbook; consistent with McGee’s hydration discussion). Gluten-free baking is a matrix problem: gluten provides elasticity and gas retention, so gluten-free blends require a hydrocolloid binder (xanthan gum at roughly 0.2–0.5% of flour weight, or psyllium) and often a starch blend (60–70% whole-grain flour + 20–30% starch + 5–10% binder) . Gluten-free batters typically run **80–110% hydration on flour weight**, far higher than wheat doughs, because the flours lack gluten’s water-binding network . **Reliable failures:** substituting gluten-free flour 1:1 by volume without a binder and without increasing hydration; using whole-grain flour 1:1 for refined flour in a delicate sponge.

**Sweeteners.** Sugar contributes sweetness, tenderness, browning (Maillard and caramelization), and in baking, structure and spread. Replacing sugar with a liquid sweetener (honey, maple, agave) adds water and browns faster; replacing it with a high-intensity sweetener (stevia, sucralose) removes the bulk that creaming and spreading depend on, so cookies may not spread and cakes may collapse (practitioner/textbook; food-science principle). **Reliable swaps:** honey for sugar with a ~25% liquid reduction and a lower oven temperature; brown sugar for white in rustic baked goods. **Reliable failures:** high-intensity sweeteners 1:1 by volume in creamed cakes; molasses 1:1 for sugar without adjusting leavening and liquid.

**Acids.** Acid balances fat and sweetness, brightens flavor, and in some systems (buttermilk, yogurt, citrus) contributes to leavening when combined with baking soda. Swapping lemon juice for vinegar is generally safe in dressings and sauces but changes aroma; swapping a mild acid (rice vinegar) for a strong one (distilled white vinegar) can overpower a delicate dish. In dairy systems, acid can curdle milk; in marinades, acid denatures protein and can make fish mushy if overdone (practitioner/textbook). **Reliable failures:** using a high-acid liquid as a 1:1 milk substitute in a béchamel without stabilization.

**Proteins.** Meat provides texture, fat, and umami; plant proteins provide varying degrees of structure and umami but often less juiciness. Hybrid meat–plant products research shows that at low substitution levels (under ~15%) plant proteins can maintain or even enhance juiciness, tenderness, and umami, but higher levels disrupt the meat matrix and can increase sourness and bitterness while diminishing umami . Mushrooms provide chitin-based bite and glutamate-driven umami, making them a strong partial substitute for ground meat in sauces and fillings . **Reliable swaps:** lentils or mushrooms for part of the ground meat in a Bolognese; firm tofu for paneer in a curry (with pressing and frying). **Reliable failures:** substituting a plant protein 1:1 for a whole cut of meat in a dry-heat roast without adjusting time and moisture.

**Alliums.** Onion, garlic, leek, shallot, and scallion are aromatic bases, but they differ in sulfur intensity and sugar content. Shallots are milder and sweeter than yellow onions; leeks are milder still and add bulk; garlic burns faster than onion. **Reliable swaps:** shallot for onion (use more); leek for onion (use more and cook longer); garlic powder for fresh garlic (use less, add later). **Reliable failures:** substituting raw garlic for cooked garlic in a long-simmered dish (it turns bitter); using scallion whites as a 1:1 substitute for onion in a caramelized-onion application.

**Fresh vs. dried herbs and spices.** Dried herbs are more concentrated by weight but lose volatile aromatics; the general conversion is 1 part dried to 3 parts fresh (practitioner/textbook, not a precise scientific rule). Whole spices retain volatiles better than ground; blooming ground spices in fat extracts fat-soluble aromas and is a standard technique across South Asian, Middle Eastern, and Latin American cooking. **Reliable failures:** substituting dried basil for fresh in a dish where fresh basil is a finishing herb (the aroma is different); adding ground spices to a cold liquid rather than blooming them in fat.

## 5. DIETARY ADAPTATIONS

### 5.1 What works and what breaks

**Vegetarian.** The main technical challenges are **structure** (meat provides chew and bind), **umami** (meat provides glutamate and nucleotides), and **fat** (meat provides saturated fat that carries flavor). Mushrooms, tomatoes, aged cheese, soy sauce, miso, and nutritional yeast are reliable umami sources; lentils, beans, and tofu provide structure; eggs and dairy provide bind and fat if allowed. The food-science literature on hybrid meat products shows that partial substitution is more reliable than total substitution: plant proteins at under ~15% can maintain sensory quality, while higher levels alter texture and flavor . **Breaks:** replacing a whole roast chicken with a plant-based analogue at the same time and temperature; replacing gelatin in a set dessert with a plant protein without a hydrocolloid.

**Vegan.** Vegan baking removes both eggs and dairy, which means removing the foaming/emulsifying/gelling functions of eggs and the fat/structure of dairy. Aquafaba and flax eggs are the two most reliable egg replacers for gluten-free and vegan baking because they add binding and moisture without altering flavor, but aquafaba foams are less stable than egg-white foams . The peer-reviewed egg-functionality review emphasizes that plant-based egg replacement is challenging because egg proteins have multiple simultaneous functions and interact with batter lipids, emulsifiers, wheat proteins, and starch in ways that are not fully mechanistically understood . **Breaks:** vegan custards and quiches without a setting agent (starch or hydrocolloid); vegan buttercreams made with a low-fat plant milk.

**Gluten-free.** The defining technical problem is the loss of gluten’s elastic gas-retaining network. Reliable gluten-free baking uses a **blend** of whole-grain gluten-free flours, starches, and a hydrocolloid binder, with substantially higher hydration than wheat baking . **Breaks:** 1:1 volume substitution of gluten-free flour for wheat flour without a binder; gluten-free bread without a binder and without increased hydration; using gluten-free flour in a roux without accounting for its different thickening behavior.

**Lactose-free.** Lactose is a sugar, not a structural component; lactose-free milk is typically made by adding lactase, so it behaves almost identically to regular milk in cooking (practitioner/textbook). The harder case is **dairy-free**, which removes casein and whey proteins and butterfat, changing browning, structure, and flavor. **Breaks:** dairy-free milk in a high-acid sauce without stabilization; dairy-free butter in laminated dough.

**Lower in saturated fat.** Replacing saturated fat with unsaturated fat changes melting behavior and mouthfeel. In baking, liquid oils produce denser, moister crumbs than solid fats; in frying, unsaturated oils are less stable at high heat. Food-science reviews of fat replacers note that starch- and mucilage-based replacers can approximate mouthfeel but not the full structural role of solid fat . **Breaks:** replacing butter with oil 1:1 in a buttercream or laminated dough; replacing all fat with a water-based purée in a shortbread.

**Lower in sugar.** Sugar provides bulk, tenderness, browning, and spread. Reducing sugar without replacing bulk can make cakes dry and cookies crumbly; high-intensity sweeteners do not provide bulk. **Breaks:** reducing sugar by more than ~20–25% in a creamed cake without adding a bulking agent (practitioner/textbook; food-science principle).

**Lower in salt.** Salt contributes flavor, preserves, and in bread, strengthens gluten and controls fermentation. Partial substitution of NaCl with KCl is a well-researched sodium-reduction strategy; WHO conditionally recommends lower-sodium salt substitutes containing potassium for the general adult population, and studies show that ~30% KCl substitution can be effective in some foods . However, KCl has a metallic/bitter note at higher substitution levels and is unsafe for people with certain kidney conditions (practitioner/medical caution). **Breaks:** replacing all salt with KCl in fermented foods where salt also controls microbial growth; salt-free bread where salt’s gluten-strengthening role is absent.

### 5.2 Allergen cross-contact basics

Allergen cross-contact is a **surface and equipment** problem, not only an ingredient problem. Studies of school and food-service kitchens have detected milk, egg, and gluten residues on “clean” food-contact surfaces, and research on manual vs. mechanical warewashing has evaluated how effectively different cleaning methods remove allergen and gluten residues . For a home-cooking assistant, the practical implications are:

- If the user declares a severe allergy, the assistant should **not** rely on “just pick it out” or “the same pan is fine.”
- The assistant should recommend dedicated equipment or a full wash–rinse–sanitize–air-dry cycle where possible, and should flag that shared toasters, colanders, and wooden boards are high-risk shared surfaces (practitioner/allergen-bureau guidance).
- The assistant should avoid suggesting “may contain” packaged foods as safe without the user checking the label.

## 6. FOOD SAFETY FOR LEFTOVERS

### 6.1 Core rules from official authorities

**USDA FSIS.** Refrigerate perishable leftovers within **2 hours** of cooking, or within **1 hour** if the ambient temperature is above 90°F (32°C) . Store most cooked leftovers for **3 to 4 days** in the refrigerator . Reheat to **165°F (74°C)** throughout . Freezing extends safety indefinitely, though quality degrades after a few months . The FSIS notes that after each reheating, leftovers are safe in the refrigerator for an additional 3–4 days, but quality decreases with each cycle, so reheat only the amount needed .

**UK Food Standards Agency.** For **rice**, the FSA is substantially stricter than the USDA. Cooked rice should be cooled quickly (ideally within **1 hour**), refrigerated, and consumed within **24 hours**; it should **never be reheated more than once**, and reheated rice must be **steaming hot all the way through** . The FSA explains the hazard mechanism: uncooked rice can contain _Bacillus cereus_ spores that survive cooking; the longer cooked rice is left at room temperature, the more likely the bacteria or toxins are to make it unsafe, and the problem is **storage before reheating**, not reheating itself . _Bacillus cereus_ toxins are heat-stable, so reheating does not neutralize them (widely reported food-safety guidance; the FSA’s own page emphasizes the storage window) .

**German BfR.** The BfR recommends a maximum refrigerator temperature of **7°C (5°C better)** and reheating food to **at least 70°C for 2 minutes** at all points . BfR guidance on meal prep emphasizes rapid cooling, portioning to avoid repeated reheating, and strict hygiene to prevent cross-contamination .

**EFSA.** EFSA’s consumer-facing work (e.g., the Safe2Eat campaign) emphasizes the five keys to safer food—cleanliness, separation of raw and cooked, thorough cooking, safe temperatures, and safe water/raw materials—and frames leftovers as usable if stored and handled safely . EFSA’s materials are more general than the USDA/FS­IS and FSA commodity-specific rules; the assistant should treat EFSA as a framework authority and the national authorities as the source of specific time/temperature limits.

### 6.2 Where authorities differ, and what the assistant should do

The most consequential divergence is **rice**: the USDA’s general 3–4-day leftover window does not align with the FSA’s 24-hour rice rule. The assistant should adopt the **more protective** rule for high-risk items and say so: “For cooked rice, UK FSA guidance is stricter than general US leftover guidance—cool within 1 hour, refrigerate, and use within 24 hours; do not reheat more than once.” This is not a case where “both are valid”; it is a case where the hazard (_Bacillus cereus_ spores and heat-stable toxins) justifies the stricter rule.

Other high-risk items and recommended assistant behavior:

- **Poultry and seafood**: 3–4 days refrigerated under USDA; reheat to 165°F. Seafood is more perishable raw; cook and refrigerate promptly.
- **Cooked greens and mushrooms**: BfR and German consumer guidance discuss reheating mushrooms and spinach with the same 70°C/2 min rule, and emphasize rapid cooling; the old absolute prohibition is not supported by BfR, but the rapid-cooling and single-reheating conditions are .
- **Large pots of stew/soup**: divide into shallow containers (≤2 inches deep) to cool quickly .
- **Reheating in a microwave**: spread food evenly, cover, stir, and check for cold spots; steam or bubbling at the edges is not a reliable indicator of uniform internal temperature .

### 6.3 How the assistant should phrase safety advice

The assistant should distinguish **“safe by authority guidance”** from **“quality preference.”** For example:

- “This is within the USDA 3–4-day window, so it is safe by that standard.”
- “The FSA advises against reheating rice more than once—this is a safety rule, not a quality preference.”
- “If you are pregnant, elderly, immunocompromised, or preparing food for someone in those groups, use the stricter end of every range” (BfR explicitly notes that meal prep is less suitable for these groups) .

## 7. INGREDIENT RECOGNITION FROM PHOTOS

### 7.1 How reliable are current models?

The evidence is mixed and depends heavily on the **task definition** and the **image condition**.

**Positive results in constrained conditions.** A 2024 _Frontiers in Artificial Intelligence_ study on refrigerator food recognition reported that a BroadFPN-YOLACT model achieved **mAP50 of 95.0%** at 60–100 cm, and 95.0–96.6% across closer distances, with precision and recall in the 0.90–0.97 range on a custom dataset of small food items . A CNN study on pantry status classification reported **97.5% validation accuracy** for fresh-vs-rotten binary classification and approximately **97%** for half-filled vs. full milk-carton classification . These results show that _narrow, well-defined recognition tasks_ can be highly accurate.

**Vision-language models (VLMs) on broader food recognition.** The FoodNExTDB benchmark (9,263 expert-labeled images; 10 categories, 62 subcategories, 9 cooking styles; 50k nutritional labels) evaluated six VLMs—ChatGPT, Gemini, Claude, Moondream, DeepSeek, and LLaVA—using an Expert-Weighted Recall (EWR) metric . Closed-source models achieved **over 90% EWR** in recognizing food products in images containing a **single product**, but the study explicitly concludes that current VLMs “face challenges in fine-grained food recognition, particularly in distinguishing subtle differences in cooking styles and visually similar food items,” limiting their reliability for automatic dietary assessment . A separate CVPR 2025 study reported **77.76% EWR for ChatGPT** and **70.16% average EWR for Gemini** on a related evaluation, reinforcing that performance drops as task granularity increases .

**Real-world fridge-scanning app testing.** A practitioner test of consumer AI fridge-scanning apps reported **88–92% accuracy** on a well-lit, organized pantry with standard packaged goods, dropping to **65–75%** in a crowded fridge with mixed produce, open containers, and occlusion . The same test identified four dominant failure modes: visually similar produce (shallots as small onions, green onions as leeks, chiles as generic “chili pepper”), partially hidden items, quantity estimation, and generic category labeling (“cheese” rather than “Parmesan”) . This is practitioner testing, not a peer-reviewed benchmark, but it is consistent with the peer-reviewed finding that occlusion and visual similarity are core failure modes .

### 7.2 What the evidence implies for product design

The assistant should treat photo recognition as **high-recall candidate generation, not authoritative inventory**. Recommended workflow:

1. **Scan and propose** a candidate ingredient list, grouped by confidence.
2. **Ask the user to confirm or edit** before generating recipes. The practitioner test found that the scan-and-verify workflow “still beats manual entry by a significant margin,” even though it requires an editing pass .
3. **Explicitly ask about quantities** for recipe-critical items (eggs, fats, aromatics) rather than inferring from pixels. Most apps identify _what_ something is, not _how much_ is there .
4. **Ask about condition** for fresh items: “Is the spinach still crisp or wilted?” “Is the chicken past its use-by date?” Image-based freshness classification is possible in narrow tasks (e.g., fresh-vs-rotten binary classification) but is not reliable for general household use .
5. **Use multiple angles** if the user is willing: photographing the fridge in sections rather than one wide shot reduces occlusion failure .
6. **Do not infer allergens or dietary suitability from a photo.** Packaged goods require label reading; cross-contact is invisible.

This workflow is a design recommendation grounded in the benchmark and practitioner evidence, not an experimentally validated protocol. Its justification is that the cost of a recognition error (a bad recipe, a safety issue) is higher than the cost of a confirmation step.

## 8. PRESENTING OPTIONS

### 8.1 How many options?

The empirical literature on choice overload provides a defensible anchor. Iyengar and Lepper’s classic jam study found that shoppers were more likely to stop at a display with 24 jams than with 6, but were far more likely to purchase when offered the **6-jam** array; the authors conclude that people are more likely to purchase when offered a **limited array of 6 choices** rather than 24 or 30 . A menu-design study using a 9-point “too little/too much” scale found an **ideal of 6 choices for quick-service items** and **7–10 for fine-dining items** . Later research in food sharing platforms found evidence of choice overload with very large assortments, with purchase probability peaking and then declining as assortment size increased .

**Recommendation:** offer **3–5 dish ideas**, not 10+. This is slightly below the “ideal” ratings in the menu study, for two reasons: (a) the cooking assistant’s user is not choosing from a menu they already want, but from a set of constraints, which adds cognitive load; and (b) the assistant needs room to explain _why_ each option is a good fit. The menu study’s “ideal” ratings are for restaurant menus, where the user is already in a consumption mindset; the cooking-assistant context is closer to a problem-solving task, where a smaller set is likely to be more usable. This is a practitioner inference from the empirical literature, not a direct experimental finding for cooking assistants.

### 8.2 How to describe options so the user can choose quickly

Research on choice overload shows that **attribute complexity and similar options** increase anxiety and confusion while decreasing decision satisfaction, and that **information nudging** (highlighting positive attributes) can mitigate these effects . The practical translation for recipe cards:

- **Lead with the decision-relevant differentiator**, not the cuisine name. “Crispy, 20 minutes, uses the spinach and the feta” is more useful than “Mediterranean spinach bake.”
- **State the time, the number of ingredients the user already has, and the number of items to buy** in a fixed, scannable format.
- **State the template** (“this is a frittata-style dish”) so the user can predict the texture and format.
- **State the flavor direction** (“sharp and herby,” “smoky and rich”) so the user can choose by appetite, not just by ingredients.
- **Flag any high-risk ingredient** (rice, seafood, poultry) with a short safety note.

This format is consistent with the “information nudging” finding—highlighting a few positive attributes reduces choice overload—and with the general principle that fewer, better-differentiated options improve decision quality .

### 8.3 Practices from meal-kit services and cooking apps

Meal-kit services and recipe apps converge on a small set of presentation patterns (practitioner observation of the industry, not peer-reviewed research):

- **Three to five “hero” recipes per week**, each with a photo, time, and difficulty label.
- **A short, fixed ingredient list** with the pantry items separated from the “buy” items.
- **A single “why this works” line** that connects the recipe to the user’s constraints.
- **A clear next action** (“pick one and I’ll write the full recipe”).

The last point matters for decision fatigue: the assistant should not end with “what would you like to do?” but with a narrower prompt—“Which one should I turn into a full recipe?”—that reduces the choice to a single step.

## 9. SYNTHESIS: DESIGN PRINCIPLES FOR THE ASSISTANT

1. **Template-first, recipe-second.** Represent dishes as structural slots and flavor checks, not as fixed ingredient lists. This is the most scalable way to handle international pantries and arbitrary fridge contents.
2. **Rank by risk of loss, not by likelihood of use.** Use category shelf life, opened-state, and visible/olfactory cues; treat use-by and best-before differently.
3. **Make assumptions visible and correctable.** Tier pantry assumptions; never silently assume a cuisine-specific staple.
4. **Reason about substitutions by function, not by name.** Warn when a swap changes structure, not just flavor.
5. **Adapt diets by identifying the function that is lost**, not by removing ingredients. The hardest cases are eggs and gluten because they are multi-functional.
6. **Use the stricter food-safety rule for high-risk items**, and say which authority you are following. Rice is the clearest case of authority divergence.
7. **Treat photo recognition as candidate generation**, not inventory. Confirm before cooking.
8. **Offer 3–5 options, differentiated by time, template, and flavor direction**, and end with a single next step.
9. **Separate empirical claims from practitioner heuristics in the assistant’s own language** (“research suggests” vs. “a common approach is”). This builds trust and avoids overclaiming.
10. **Measure what matters.** The food-waste literature cautions that measurement alone can change behavior; the assistant should track whether users actually cook the suggested dishes, not just whether they click on them .

## SOURCE LIST (APA 7th edition)

Bittman, M. (2015). _Mark Bittman’s kitchen matrix: More than 700 simple recipes and techniques to mix and match for endless variety_. Clarkson Potter.

Bundesinstitut für Risikobewertung. (2014). _Germs in the kitchen: Tips on food hygiene_. German Federal Institute for Risk Assessment.

Bundesinstitut für Risikobewertung. (2025). _Pre-cooking for several days: What should I bear in mind?_ German Federal Institute for Risk Assessment.

Casonato, C., Stöckli, S., & Vittuari, M. (2023). _Nudging household food waste reduction: A systematic review_. [Note: cited within the systematic review below; see Casonato et al. as cited in the 2024 review.]

Crosby, H. (2017). _YumUniverse pantry to plate: Improvise meals you love—from what you have!_ The Experiment.

Dai, Y. (2024). Robust deep-learning based refrigerator food recognition. _Frontiers in Artificial Intelligence, 7_, Article 1442948. https://doi.org/10.3389/frai.2024.1442948

Delley, M., & Brunner, T. A. (2018). _Quantifying the prevention potential of avoidable food waste in households using a self-reporting approach_. [Cited in the 2024 systematic review.]

Food Standards Agency. (2026). _Home food fact checker_. UK Government. https://www.gov.uk/government/publications/home-food-fact-checker

Grandi, B., & Cardinali, M. G. (2021). Choice overload in the grocery setting: Results from a laboratory experiment. _International Business Research, 14_(1). [Cited in search results.]

Iyengar, S. S., & Lepper, M. R. (2000). When choice is demotivating: Can one desire too much of a good thing? _Journal of Personality and Social Psychology, 79_(6), 995–1006.

Kaushik, R., & Chawla, P. (2025). Application of mucilage-based functional and clean-label food ingredients as vegan fat replacers in different food products. _Current Opinion in Food Science, 62_.

Laursen, N. F., Pérez, B., Nielsen, K. E., Skovsgaard, M. B., Christensen, C. H., & Corredig, M. (2026). The functional role of eggs and plant-based alternatives in cake systems: Design considerations based on colloidal and structural dynamics. _Critical Reviews in Food Science and Nutrition_. https://doi.org/10.1080/10408398.2026.2714688

Leverenz, D., et al. (2019). _Self-reporting food waste in combination with coaching sessions_. [Cited in the 2024 systematic review.]

McGee, H. (2004). _On food and cooking: The science and lore of the kitchen_ (Rev. ed.). Scribner.

National Food Safety Authority. (2026). _Leftover food safety: Storage, reheating, and timelines_. https://nationalfoodsafetyauthority.com/leftovers-food-safety.html

Roe, B. E., et al. (2022). _Coaching using a behavioural toolbox approach_. [Cited in the Knowledge Auckland evidence summary.]

Romero-Tapiador, S., Tolosana, R., Lacruz-Pleguezuelos, B., Marcos-Zambrano, L. J., Bazan, G. X., Espinosa-Salinas, I., Fierrez, J., Ortega-Garcia, J., Carrillo de Santa Pau, E., & Morales, A. (2025). Are vision-language models ready for dietary assessment? Exploring the next frontier in AI-powered food image recognition. _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)_.

Ruhlman, M. (2009). _Ratio: The simple codes behind the craft of everyday cooking_. Scribner.

Shadeeb, S. H., & Hossain, S. (2024). _Machine learning to effectively monitor status of food items in pantry using convolution neural network models_ [Preprint]. TechRxiv. https://doi.org/10.36227/techrxiv.170629519.92560985/v1

Simões, J., et al. (2022). _Effectiveness of multi-component food waste interventions_. [Cited in the 2024 systematic review.]

Stöckli, S., et al. (2018). _Nudges for reducing consumer food waste_. [Cited in the 2024 systematic review.]

UK Food Standards Agency. (2025). _Revealed: The best ways to reheat your takeaways_ [Interview with Narriman Looch, Head of Food Hygiene]. Which?

USDA Food Safety and Inspection Service. (2025a). _How long will cooked food stay safe in the refrigerator?_ https://ask.fsis.usda.gov/article/How-long-will-cooked-food-stay-safe-in-the-refrigerator

USDA Food Safety and Inspection Service. (2025b). _How many times can I reheat foods?_ https://ask.fsis.usda.gov/article/How-many-times-can-I-reheat-foods

USDA Food Safety and Inspection Service. (2026). _Keep food safety in play this Super Bowl_ [Press release]. https://www.usda.gov/about-usda/news/press-releases/2026/01/28/keep-food-safety-play-super-bowl

van Herpen, E., Wijnen, T., Quested, T., Reynolds, C., & Sharda, N. (2023). _Household food waste intervention efficacy: A systematic review_. _Journal of Cleaner Production, 139604_. [Cited in the OUCI review.]

Vittuari, M., et al. (2023). _Multi-component interventions for consumer food waste_. [Cited in the 2024 systematic review.]

Zhang, et al. (2023). _Meta-analysis of nudges for reducing consumer food waste_. [Cited in the 2024 systematic review.]

_Systematic literature review of impactful food waste interventions at the consumer level._ (2024). _Sustainable Production and Consumption_. https://www.sciencedirect.com/science/article/pii/S235255092400335X
