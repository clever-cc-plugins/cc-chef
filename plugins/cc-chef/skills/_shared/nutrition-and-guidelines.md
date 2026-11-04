# Nutrition and personal guidelines

Use this file for everyday healthier cooking and for personal dietary guidelines: `dietary-guidelines` loads it to draft or update a household member's guideline document and to decide when to refuse or refer; `create-recipe` and `rework-recipe` load it to apply graded cooking levers, life-stage rules and allergen handling to a dish; `chef-onboarding` loads it for the screening questions, the one-time disclaimer and the nutrient-data setup; `research-prompt` loads it to build prompts that stay inside the boundaries below. It supports ordinary healthy eating, never medical nutrition therapy. Food-safety limits (leftovers, reheating, listeria and mercury lists, egg rules) live in `food-safety.md`; this file only points there. Section 1 gives the pattern core and the national-guidance differences, section 2 the graded cooking levers, section 3 life-stage nutrition rules, section 4 allergens and constraint classes, section 5 the guideline-document structure with a worked household example, section 6 referral triggers and the behaviour table, section 7 wording, the disclaimer and the myths filter, section 8 nutrient data, section 9 a checklist, section 10 the evidence notes.

Conventions: `(to verify)` marks a claim that only one research report made. "Default" is what the plugin does when reports disagree. Evidence tags: strong = authority recommendation graded strong or high-certainty trials and meta-analyses; moderate = controlled trials or meta-analyses with caveats, or authorised claim with a modest effect; low = observational, mechanistic or thin trial data; consensus = expert position without trial-level grading; design = a rule chosen for this plugin. A strong recommendation can rest on low-certainty evidence, so tags always name the outcome (LDL, blood pressure, events) and never stand for "this works".

## 0. Rules at a glance

- Healthy eating means the shared pattern core (section 1.2), expressed through the user's own cuisine and budget. Named diets are optional frameworks, not rival brands.
- Order of precedence when rules collide: declared allergies and clinician-set limits, then life-stage and country safety rules, then soft targets with evidence, then preferences. Never relax a higher tier to satisfy a lower one.
- Target LDL and the overall pattern. "Raise HDL" is not a valid dietary goal (section 2.1).
- Where the US Dietary Guidelines 2025-2030 diverge (protein, full-fat dairy, animal fats), the plugin follows WHO, AHA/ACC and the European guides, and says so (section 1.3).
- No therapeutic rules for referral conditions (section 6). Clinician-set limits are recorded as the user reports them, never invented or adjusted.
- Potassium-based salt substitutes are never a default and are never suggested before screening; they are unsafe in kidney disease and with certain medicines (section 2.4).
- Nutrient numbers are rounded ranges with a named source, and a user-registered food list wins over any database (section 8).
- Wording describes composition and substitution; it never promises a health effect (section 7).

## 1. The healthy-pattern core and national guidance

### 1.1 Named patterns, what they are good for, how sure the evidence is

| Pattern                     | Core idea                                                                                                      | Best-supported outcome and tag                                                                                                           | Caveat                                                                                                                                             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mediterranean               | Vegetables, fruit, legumes, whole grains, nuts, olive oil as main fat, fish; little red and processed meat     | Cardiovascular mortality in higher-risk adults: moderate (network meta-analysis). Primary prevention and other outcomes: low to moderate | Cochrane graded the hard-endpoint evidence low to moderate; the flagship trial was re-analysed after a retraction (Claude only, to verify)         |
| DASH                        | Vegetables, fruit, low-fat dairy, whole grains, legumes, nuts; less sweets, red meat, saturated fat and sodium | Blood pressure: moderate to high, a few mmHg systolic in meta-analyses                                                                   | Not clearly better than every alternative pattern in a 2026 review (DeepSeek only, to verify); stronger with sodium restriction                    |
| Portfolio                   | Low-saturated-fat base plus viscous fibre, plant sterols, nuts and soy or other plant protein                  | LDL: moderate to high, about 17 percent lower in a graded meta-analysis of 7 trials                                                      | Few trials; hard-event data come from cohorts only; one report called the evidence weak in an umbrella review (see section 10)                     |
| Nordic                      | Rye, oats, barley, berries, root vegetables, legumes, rapeseed oil, fish                                       | Cardiometabolic markers and mortality associations: low to moderate                                                                      | Mostly cohort data; LDL results varied between trials                                                                                              |
| EAT-Lancet planetary health | Plant-rich, small amounts of animal foods, built for environmental limits                                      | Mortality and cardiometabolic associations: moderate at best, observational                                                              | A 2026 review flagged possible shortfalls of B12, calcium, iron and zinc and affordability limits (two reports); not for young children as written |
| National guides             | Plate or circle models (Eatwell, Canada, DGE, NNR, US)                                                         | Indirect: moderate for the components they recommend, low for the visual tool as a behaviour-change instrument                           | Proportions apply across a day or week, not to every plate; Eatwell is not meant for under-twos                                                    |

### 1.2 The convergent core (the plugin default for "healthy")

| Element                                 | Cooking translation                                                                                        | Tag       |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------- |
| Plants as the base                      | Vegetables and fruit in most dishes; legumes, whole grains, nuts and seeds as regular components           | strong    |
| Unsaturated fat in place of saturated   | Rapeseed, olive, sunflower or soy oil for everyday cooking; fish and nuts; less butter, lard, coconut/palm | strong    |
| Less red and processed meat             | Smaller meat portions alongside legumes or vegetables; processed meat as an occasional item                | strong    |
| Less salt, added sugar, ultra-processed | Season with acid, herbs, spice and umami; cook from basic ingredients; water as the default drink          | strong    |
| Adapt to place and culture              | Use the user's own staples; the pattern is a direction, not a menu                                         | consensus |

Practical limits that follow from it: build plates as roughly half vegetables and fruit, a quarter whole grain or starchy food, a quarter protein food (Canada-style plate, consensus); count weekly rather than per meal (Eatwell logic).

### 1.3 Where national guidance differs

| Topic                          | Position A                                                                                                          | Position B                                                                                                                                                                                                                                       | Plugin default                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Protein for healthy adults     | WHO, EU and UK reference values near 0.75-0.8 g per kg per day                                                      | US Dietary Guidelines 2025-2030 (released January 2026) advise 1.2-1.6 g per kg and protein at every meal                                                                                                                                        | Use the 0.8 g per kg reference for general adult cooking; higher figures only for older adults (section 3.4) or where a clinician or dietitian sets them; say the US guide differs |
| Full-fat dairy, butter, tallow | US 2025-2030 favours full-fat dairy and animal protein while keeping saturated fat at or below 10 percent of energy | WHO (strong), AHA/ACC, the 2025 US advisory committee and the European guides advise replacing saturated fat with unsaturated fat; ACC warned in January 2026 that the US food advice would exceed the 10 percent limit (Claude only, to verify) | Follow WHO/AHA/ACC for any cardiovascular goal; do not present butter or tallow as a heart-healthy choice; state the disagreement once, neutrally                                  |
| Meat limits                    | DGE 2024: at most 300 g meat and sausage a week (Claude, Perplexity); NNR2023: red meat up to 350 g a week          | Other guides give looser or no numbers                                                                                                                                                                                                           | Cite the user's national figure when a country is registered; otherwise "small portions, mostly plants"                                                                            |
| Dairy                          | DGE cut to two portions a day (Claude only, to verify)                                                              | Eatwell and Canada keep dairy or alternatives as a smaller group                                                                                                                                                                                 | Follow the user's country; dairy is optional in the core                                                                                                                           |
| Fibre target                   | 25-29 g a day gives the largest risk drop, more above 30 g (meta-analysis); UK guide 30 g                           | One report warns against any universal figure without jurisdiction and age                                                                                                                                                                       | Adults: aim for roughly 25-30 g, labelled with its source; never for infants; raise slowly and with fluids                                                                         |
| Salt                           | WHO: under 2 g sodium (about 5 g salt) a day (Claude only, to verify); UK: 6 g salt; US: under 2,300 mg sodium      | None disagree on direction                                                                                                                                                                                                                       | Say "about 5-6 g salt" for adults; count salt from stock, sauces, cheese, bread and cured meats, not only the salt shaker                                                          |
| Added sugar for children       | No added sugar in the first year (UK), none before age 2 (older US advice)                                          | A 2026 US CDC page is reported to say none under 11 years (Perplexity only, to verify)                                                                                                                                                           | Hard rule: none under 12 months. Under 2: none. Older children: follow the registered country                                                                                      |

Always record which edition of a guide a statement comes from. Do not serve the 2020-2025 US edition as the current one.

## 2. Graded cooking levers

Each lever lists what the cook does, the evidence tag for the named outcome, and the wording limit. A lever describes a change to the dish ("this version has less saturated fat than the original"), not a promised change in the eater's numbers.

### 2.1 Blood lipids (LDL)

| Lever                                 | What the cook does                                                                                                                | Tag and size                                                                                                                                                                                                                    |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unsaturated fat instead of saturated  | Rapeseed, olive, sunflower or soy oil for butter, ghee, lard, coconut or palm; skinless poultry, lean cuts; soft spread           | Strong. WHO: saturated fat at or below 10 percent of energy, replace with polyunsaturated (strong), plant monounsaturated or fibre-rich carbohydrate (conditional). Replacing with refined starch or sugar gives little benefit |
| No trans fat                          | Avoid partially hydrogenated fats                                                                                                 | Strong (WHO: under 1 percent of energy)                                                                                                                                                                                         |
| Viscous fibre                         | Oats, barley, psyllium, beans, lentils, aubergine, okra, apples and citrus                                                        | Moderate to high. About 3 g oat or barley beta-glucan a day is the amount behind the EU-authorised cholesterol claim, roughly 75-90 g oats (Claude only, to verify the gram range)                                              |
| Plant sterols and stanols             | Fortified spreads, yoghurt or drinks, 1.5-3 g a day                                                                               | High for LDL (about 7-12 percent), no outcome trials. Not for children under 5, pregnancy or breastfeeding (EU labelling, Claude only, to verify). A fortified product is a deliberate choice, not a family-recipe default      |
| Nuts                                  | About 25-30 g a day as snack or topping                                                                                           | Moderate; small LDL effect                                                                                                                                                                                                      |
| Soy and legumes                       | Tofu, tempeh, edamame, soy milk, beans and lentils replacing some meat                                                            | Moderate; each Portfolio food gave single-digit LDL falls (Claude, DeepSeek)                                                                                                                                                    |
| Coffee                                | Unfiltered brews (press, boiled) raise LDL moderately (Consensus only, to verify); paper-filtered coffee is the plain alternative | Moderate                                                                                                                                                                                                                        |
| Dietary cholesterol (eggs, shellfish) | Moderate amounts fit a pattern                                                                                                    | Low to moderate; saturated fat moves LDL more. No egg ban, no "unlimited eggs"                                                                                                                                                  |

HDL rule: the plugin does not offer "raise HDL" as a goal and never recommends alcohol or more saturated fat for it. HDL-raising drugs and genetic studies failed to show benefit (Claude, Copilot, DeepSeek agree; Perplexity: unverified, conservative). When a user registers it, reframe gently: cooking targets LDL, non-HDL and the pattern, and lipid targets belong with their clinician.

### 2.2 Fibre

- Levers: legumes in soups, sauces and mixed dishes; whole-grain swaps that keep the dish's function; skin-on vegetables; nuts, seeds, oats; fruit rather than juice. Tag: strong for bowel function and cardiometabolic associations.
- Practice: increase gradually, with fluids; spread over the day or week; set aside soft or low-residue needs for older adults and for IBS, IBD or low-FODMAP questions (dietitian).

### 2.3 Iron

| Point               | Rule for the cook                                                                                                                                                                                   | Tag                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Heme vs non-heme    | Meat, fish and poultry supply heme iron, absorbed several times better and barely affected by other foods. Legumes, tofu, grains, seeds and greens supply non-heme iron, which dominates most diets | Strong                                                                     |
| Enhancers           | Put a vitamin C food (citrus, pepper, tomato, berries) into the same meal; a little meat or fish also helps non-heme iron                                                                           | Moderate to strong (meta-analysis, EFSA-authorised vitamin C claim)        |
| Tea and coffee      | Serve between meals rather than with an iron-focused meal                                                                                                                                           | Moderate; one report asked for more checking before a fixed interval       |
| Calcium             | Do not pair the main iron source with a large portion of milk or cheese; do not remove dairy from the diet, because effects shrink in mixed meals                                                   | Moderate, reports differ (default stated here)                             |
| Phytates            | Soaking, sprouting, fermenting and sourdough lower them; treat as helpful techniques, not guarantees                                                                                                | Low to moderate (the process-specific effect on iron status is unverified) |
| Spinach             | Not a reliable iron answer: iron content is not the same as absorbed iron                                                                                                                           | Moderate                                                                   |
| Diagnosis and doses | A recipe cannot show whether someone is iron deficient. Suspected deficiency, anaemia or a supplement request goes to a clinician; never state a dose                                               | Design                                                                     |

Reference values (US, not universal): 7 mg a day at ages 1-3, 11 mg at 7-12 months, 27 mg in pregnancy (Perplexity only, to verify). Cite them only with their country.

### 2.4 Blood pressure, sodium and potassium

| Lever                           | What the cook does                                                                                                                                                                                                                                                                 | Tag and size                                                                              |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Less sodium                     | Season in stages; acid, herbs, spices, garlic and umami carry flavour; limit stock cubes, soy sauce, cured meats, cheese; rinse canned beans; taste adapts over weeks                                                                                                              | Strong                                                                                    |
| DASH-style eating               | More vegetables, fruit, legumes, nuts, low-fat dairy, whole grains                                                                                                                                                                                                                 | Moderate to high; a few mmHg systolic                                                     |
| Potassium-rich foods            | Beans, leafy greens, potatoes, fruit, as part of the pattern                                                                                                                                                                                                                       | Moderate to high; not for kidney disease or potassium-limited care plans (section 6)      |
| Potassium-based salt substitute | Not suggested by default. WHO (January 2025) made a conditional recommendation for adults only, excluding pregnancy, children, kidney impairment and anything that impairs potassium excretion such as potassium-sparing diuretics, ACE inhibitors, ARBs and potassium supplements | Moderate for blood pressure (about 6 mmHg in one meta-analysis, DeepSeek only, to verify) |

Screening gate for any salt substitute: ask about kidney disease, relevant medicines, pregnancy and the age of everyone who eats the dish. If any answer is yes or unknown, do not mention it. If all are clear, it is an optional swap for adults at the table (a branch, not the shared base), never a universal recommendation. In shared dishes the base stays under-salted and each person seasons their own portion.

### 2.5 Blood glucose

- Levers: whole and intact grains, legumes and vegetables; fewer sugary drinks and refined starches; fibre; carbohydrate eaten with protein, fat or fibre; al dente pasta; cooled and reheated starches (resistant starch, modest, low certainty). Tag: moderate for carbohydrate quality and fibre, low for the cooking tricks.
- Oat and barley beta-glucan: the EU-authorised claim is about cholesterol; an EFSA opinion on post-meal glucose was published in January 2026 and the claim was not yet authorised (Claude only, to verify). Do not use glucose wording.
- Show carbohydrate per real serving as a range if the user wants it. Do not set carbohydrate targets, promise a glucose response or label a dish "diabetes-friendly". People on insulin or sulfonylureas: section 6.

### 2.6 Weight and energy

- Levers with some support: more vegetables and water-rich ingredients (lower energy density), enough protein and fibre for fullness, fewer sugary drinks and ultra-processed items, measured oil (1 tbsp is roughly 120 kcal), consistent portions. Tag: moderate for energy density, low for any single culinary trick; no macronutrient ratio wins in the long run.
- No calorie or weight targets for children, pregnancy, frail older adults or anyone with disordered-eating signals. Avoid moral labels such as clean, guilt-free, cheat.

### 2.7 Gut health

- Supported: a wide range of fibre-rich plants (strong for bowel function), fermented foods as part of a pattern (low to moderate). Not supported: "fix your microbiome", universal probiotics, gut-healing claims. Probiotic safety is uncertain for some vulnerable groups including premature infants.
- IBS, IBD, coeliac disease and low-FODMAP needs are individual dietetic matters.

### 2.8 Cooking methods

| Topic              | Guidance                                                                                                                                                                                                                                                                                                                                                                                                  | Tag                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Vitamin retention  | Steaming, microwaving, pressure cooking and stir-frying keep more vitamin C and folate than boiling in a lot of water (USDA factors: boiled and drained greens keep roughly half to 60 percent, steamed or stir-fried about 85 percent; boiling averages near -50 percent vitamin C and -68 percent folate in another review). Use little water and reuse it in soups; cut vegetables just before cooking | Moderate to strong                        |
| Minerals           | Mostly retained (about 85-100 percent) unless the cooking water is discarded                                                                                                                                                                                                                                                                                                                              | Moderate                                  |
| Legumes            | Long boiling cuts folate sharply; pressure cooking retains well                                                                                                                                                                                                                                                                                                                                           | Low to moderate (Claude, Copilot)         |
| Oils               | Choose by method: rapeseed, olive (including extra-virgin) and high-oleic sunflower suit everyday frying and roasting; keep omega-3-rich oils such as flax and walnut for cold use; do not reuse frying oil repeatedly. A high smoke point alone does not make an oil the healthiest                                                                                                                      | Moderate (design for the last clause)     |
| Charring           | Avoid heavy char and very hot grilling of meat; lower temperatures and marinades reduce heterocyclic amines                                                                                                                                                                                                                                                                                               | Low (mechanistic, Claude only, to verify) |
| Alcohol in cooking | It does not cook off fully: USDA factors give about 75 percent retained when flamed and about 5 percent after 2.5 hours of simmering. Matters for pregnancy, children, recovery and religious exclusions                                                                                                                                                                                                  | Strong (see `food-safety.md` section 6)   |
| Raw vs cooked      | Neither is always better; some carotenoids are easier to absorb after cooking, and raw items carry safety limits for vulnerable groups                                                                                                                                                                                                                                                                    | Moderate                                  |

## 3. Life-stage nutrition rules

Hazard limits (listeria foods, mercury lists, egg rules by country, reheating, nitrate-rich vegetables) are in `food-safety.md` sections 6 and 7; the rows below hold the nutrition and feeding rules. Rules marked hard are never relaxed and never overridden by a preference. Where countries differ, ask for the country and use its authority; never average national rules.

### 3.1 Infants (under 12 months) and toddlers

| Topic                 | Rule                                                                                                                                                                                                                                                                                                                                                                                                                                              | Class and tag                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Honey                 | None before 12 months, cooked-in honey included (botulism spores)                                                                                                                                                                                                                                                                                                                                                                                 | Hard; strong, every report               |
| Added salt            | None in food or cooking water; UK: under 1 g salt a day below 12 months, no more than 2 g a day at 1-3 years. Avoid stock cubes, gravy, bacon, crisps. Set the child's portion aside before seasoning                                                                                                                                                                                                                                             | Hard for infants; official               |
| Added sugar           | None in the first year; none before age 2 in older US advice; later ages follow the country (see section 1.3)                                                                                                                                                                                                                                                                                                                                     | Hard under 12 months; country beyond     |
| Iron                  | Stores run low around 6 months. Offer iron-rich foods from the start of complementary feeding (meat, fish, egg, legumes, fortified infant cereal) with a vitamin C food; keep cow's milk from displacing meals. No iron supplement advice                                                                                                                                                                                                         | Strong; no doses from the plugin         |
| Cow's milk            | Small amounts in cooking are usual; as the main drink only from 12 months. WHO allows animal milk for some non-breastfed 6-11 month olds on low-certainty evidence, multi-society bodies disagree. Default: not as a drink before 12 months; plant "rice drinks" are not suitable (NHS)                                                                                                                                                           | Hard as a drink; countries differ        |
| Choking and textures  | No whole nuts under 5 (smooth nut butter or ground nuts instead; a spoonful of nut butter alone is also a hazard); halve grapes and cherry tomatoes lengthways; flatten blueberries; no popcorn, hard sweets or raw hard carrot; check shape, hardness, stickiness and bones, not only the ingredient name. Upright, seated, supervised. Progress from smooth around 6 months to lumpy and finger foods by 7-9 months to family food by 12 months | Hard; official, ages 3-5 vary by country |
| Allergen introduction | Introduce common allergens (egg, peanut as thinned butter or ground, others) one at a time from about 6 months and keep offering tolerated ones. Severe eczema or a known allergy means clinician advice first. "Contains an allergen" is not "exclude for every infant"                                                                                                                                                                          | Moderate to strong; official             |
| Other                 | Unpasteurised cheese, raw shellfish, shark, swordfish and marlin are unsuitable (see `food-safety.md` section 7). WHO recommends daily animal-source foods, fruit and vegetables for 6-23 months (strong recommendation, low-certainty evidence)                                                                                                                                                                                                  | Official                                 |
| Low-fat foods         | Whole-fat dairy is usual in early childhood; low-fat versions are generally not before age 2, with national differences                                                                                                                                                                                                                                                                                                                           | Consensus (DeepSeek only, to verify)     |

### 3.2 Children

- Same healthy pattern in smaller portions; growth, iron, zinc, calcium, fibre and enough energy come first. Eatwell proportions are for ages 2-5 onwards gradually, not for under-twos.
- Do not apply adult tools without professional input: low-fat diets, plant sterols, calorie deficits, high fibre targets, the US 1.2-1.6 g per kg protein figure.
- Limit sugary drinks and free sugars (honey, syrups and juices count). Persistent narrow eating, growth worries or many exclusions trigger a professional-review prompt, not ever-narrower recipes.
- Fish: use the lowest-mercury choices in age-appropriate portions (lists in `food-safety.md` section 7).

### 3.3 Pregnancy and breastfeeding

- Food-safety rules (listeria foods, raw and undercooked foods, eggs by country, mercury, liver, alcohol, caffeine) are in `food-safety.md` section 7. Do not restate or label a dish "safe in pregnancy".
- Nutrition notes: iron, folate, iodine and DHA need attention (Copilot, consensus); supplement choices are for a midwife, doctor or pharmacist. Energy and fluid needs rise in breastfeeding.
- Potassium-based salt substitutes are excluded in pregnancy (section 2.4). Plant sterol products are labelled unsuitable.
- Gestational diabetes, pre-eclampsia, hyperemesis and other complications: refer (section 6). No calorie or weight targets.

### 3.4 Older adults

| Topic          | Rule                                                                                                                                                                                                                                                                      | Tag                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Protein        | For healthy people over 65, 1.0-1.2 g per kg a day (PROT-AGE, ESPEN); 1.2-1.5 g per kg with acute or chronic illness; about 25-30 g per meal (Claude only, to verify). Severe kidney disease below eGFR 30 may need a lower figure, so never apply this to kidney disease | Consensus; moderate evidence |
| Texture        | Soft, moist, easy-to-chew options for poor dentition. Dysphagia needs a speech-language therapist and defined texture levels: refer                                                                                                                                       | Consensus                    |
| Energy density | Smaller, nutrient-dense meals when appetite is poor; fortify with protein and fats before cutting portions; unintended weight loss, swallowing problems or very low intake override "lighter meal" settings                                                               | Consensus                    |
| Taste changes  | Herbs, acid and spice instead of extra salt                                                                                                                                                                                                                               | Design                       |
| Micronutrients | Vitamin D and B12 are supplement decisions for a clinician; hydration and fibre with fluids                                                                                                                                                                               | Consensus                    |

## 4. Allergens, intolerances, preferences

### 4.1 Regulated lists

| EU, Regulation 1169/2011 (14)                                                                                                                                | US, FALCPA and FASTER Act (9)                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Gluten cereals; crustaceans and molluscs; eggs; fish; milk; peanuts, tree nuts, sesame, soybeans and lupin; celery and mustard; sulphites above 10 mg per kg | Milk; eggs; fish; crustacean shellfish; peanuts and tree nuts; wheat; soybeans; sesame (added from 1 January 2023) |

- Canada, Australia and New Zealand and others keep their own lists. Default: handle the union of all lists plus anything the user names; lists are a labelling framework, not everything a person may need to avoid.
- Track the actual ingredient, not just an "EU allergen" flag. Resolve compound items: stock (celery), dressings (mustard), tahini (sesame), whey or casein (milk), glazes (egg), Worcestershire sauce (fish), some gluten-free flours (lupin).
- US bakeries have added sesame on purpose to avoid cross-contact rules, which FDA has criticised but not banned (Claude only, to verify): treat bakery items as sesame-uncertain.

### 4.2 Constraint classes

| Class                                                                      | Treatment                                                                                                                                                                    |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allergy (immune-mediated, any trace can matter), incl. anaphylaxis history | Hard. Trace-level avoidance with cross-contact notes. Never test tolerance, never suggest "a little is fine", never rely on cooking to destroy an allergen, never "pick out" |
| Coeliac disease, and gluten sensitivity when declared                      | Hard, strict avoidance                                                                                                                                                       |
| Intolerance (non-immune, usually dose-based)                               | Hard at the threshold the user or clinician states; never invent a safe dose. Default when no threshold is given: exclude                                                    |
| Religious or ethical exclusion declared absolute (halal, kosher, vegan)    | Hard; not a safety matter but breaking it breaks trust                                                                                                                       |
| Clinician-prescribed restriction                                           | Hard, recorded as reported (section 6)                                                                                                                                       |
| Dislikes, cuisines, budget, time, equipment                                | Soft preference; changes only with the user's informed consent                                                                                                               |

- Substitution rule: never swap an allergen for a "related" food (one tree nut for another, crustacean for mollusc) unless the user confirms tolerance. Re-check every substitution against the registered exclusions.
- Cross-contact basics: cook the allergen-free dish first, clean pans, boards and utensils, wash hands, no shared frying oil, toasters or grills, read every label each time because products change, treat "may contain" as no for severe allergy, and ask the user to check the label. Separate ingredient exclusion from handling notes.
- Never promise "allergen-free" from a recipe alone. For a suspected reaction, name the local emergency number rather than assuming one.

## 5. The personal guideline document

### 5.1 Structure (one document per household member)

| Part                      | Content                                                                                                                                                                                                                     | Rules                                                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1. Profile                | Life stage with age band (from infant through older adult, including pregnant and breastfeeding), country (selects safety and guide edition), review date; body size only if needed                                         | Country and life stage choose the rule set                                                                                        |
| 2. Hard constraints       | Allergies with severity and cross-contact sensitivity, coeliac disease, intolerance thresholds, absolute religious or ethical exclusions, clinician-set limits quoted as the user reports them, medicine-related food rules | Never relaxed, never inferred. Record the source (user, clinician, label)                                                         |
| 3. Automatic safety rules | Triggered by the profile: for a toddler no added salt, no honey, choking-safe shapes; for pregnancy the `food-safety.md` rules; for infants the section 3.1 list                                                            | Reference the rule, do not restate limits                                                                                         |
| 4. Soft targets           | Quantified or frequency targets such as "fibre about 25-30 g a day", "saturated fat under 10 percent of energy", "an iron food plus a vitamin C food at lunch and dinner"                                                   | Each target carries evidence source, certainty tag, unit, time horizon (day or week) and origin (official guide, clinician, user) |
| 5. Preferences            | Cuisines, dislikes, time, budget, equipment, skill                                                                                                                                                                          | Soft; honoured by default                                                                                                         |
| 6. Review triggers        | Events that reopen the document: new diagnosis, medicine change, pregnancy, a birthday that changes a rule (6 months, 12 months, 2 years, 5 years), new allergy, new guide edition, any referral trigger in section 6       | Stop and refer where section 6 says so                                                                                            |

Target hygiene: numbers come from the user's official guide or a clinician, never from the plugin's invention. Express targets over a day or week, not per recipe. Say "supports" and "fits", not "treats". Use ranges for numeric targets where the source gives them.

### 5.2 Households: base plus branch

1. Cook one shared base that satisfies the strictest hard and safety rule of anyone at the table (no added salt, no honey, no allergen, soft or splittable texture).
2. Set the most restricted person's portion aside before seasoning or adding risky parts.
3. Meet each person's soft targets through branches: seasoning, toppings, sides, portion size, a fat or protein add-on.
4. Never average the household's needs into a fictional member, and never apply one person's targets (energy restriction, fibre push) to a child.
5. Re-check allergens and age rules for every branch ingredient.

### 5.3 Worked example: high LDL for the adult, iron for the toddler, one pot

| Step              | Shared base                                                                                                                                                    | Adult branch (LDL levers)                                                                             | Toddler branch (iron, salt, choking rules)                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Pot               | Lentil and lean beef ragu (half and half keeps saturated fat down) in rapeseed oil, with tomato and red pepper for vitamin C. No salt, no stock cube, no honey | -                                                                                                     | Same pot                                                                                |
| Before seasoning  | Take the toddler's portion out                                                                                                                                 | -                                                                                                     | Mash or chop to a soft, safe texture; no whole nuts or hard pieces                      |
| Season            | -                                                                                                                                                              | Salt to taste, or acid and herbs; a potassium salt only if screening was clear (usually leave it out) | No salt; a squeeze of lemon or herbs is fine                                            |
| Serve with        | -                                                                                                                                                              | Barley or whole-grain pasta (viscous fibre), side salad with walnuts and olive oil                    | Soft pasta or rice; water to drink; no tea, and not a large glass of milk with the meal |
| Why it meets both | The pot uses fibre-rich ingredients such as lentils and unsaturated fat from rapeseed oil, and gives heme plus non-heme iron with vitamin C                                                                 | Matches fibre, unsaturated fat and nut levers; no butter or cheese needed                             | Iron food with vitamin C, salt and choking rules met; portion not energy-restricted     |

The strict rule sits in the base, the personal targets sit in the branches. A meal does not prove nutritional adequacy: describe its contribution only.

## 6. Referral triggers and behaviour table

### 6.1 Referral triggers (stop, name the limit, point to a doctor, registered dietitian or pharmacist)

- Chronic kidney disease or any prescribed potassium, phosphorus, sodium, protein or fluid limit.
- Diabetes treated with insulin or sulfonylureas (hypoglycaemia risk), or any change to a medicine-linked meal plan.
- Anticoagulants (warfarin and similar), MAOIs, immunosuppressants, statins and other medicines with food interactions; grapefruit, Seville orange and pomelo with relevant medicines; potassium-sparing diuretics, ACE inhibitors and ARBs (potassium).
- Pregnancy complications (gestational diabetes, pre-eclampsia, hyperemesis, multiple or high-risk pregnancy).
- Eating-disorder history or current signs (severe restriction, purging, rapid weight loss, distress around food).
- Anaphylaxis history, multiple food allergies in a child, uncertain reactions, or a proposed home food challenge.
- Infants or children with faltering growth, feeding refusal or very restricted intake; suspected botulism signs after honey (urgent care).
- Unintended weight loss, trouble swallowing, persistent or severe gut symptoms, blood in stool, signs of anaemia, malnutrition in an older adult.
- Cancer treatment, liver or pancreatic disease, malabsorption, complex gut disease.
- Very-low-calorie, ketogenic or extended-fasting plans; high-dose supplements; any supplement or dose request.

### 6.2 Behaviour table

| Condition or situation                                        | What the skill does                                                                                                                                                                                       | What it never does                                                            |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Kidney disease                                                | Declines therapeutic rules; asks for the care plan; records the limits the user gives, verbatim, as hard constraints; refers to a renal dietitian; ordinary recipes may still be made within those limits | Suggests potassium salt, legumes or protein "for health", sets its own limits |
| Insulin or sulfonylurea                                       | Makes ordinary recipes; can show carbohydrate per serving as an estimate, never a basis for insulin dosing; points to the care team for any plan change                                                                                     | Sets carbohydrate targets, low-carb plans, or medicine timing                 |
| Anticoagulant                                                 | For vitamin K antagonists (warfarin, phenprocoumon) only: advises steady day-to-day intake of vitamin K foods rather than avoiding greens; records the clinician's instruction; refers to the prescriber or anticoagulation clinic for specifics (Claude); DOACs have no comparable rule (Claude, DeepSeek)                                    | Names gram targets or bans greens                                             |
| Grapefruit and relevant medicine                              | Flags it and says to check with a pharmacist; records a clinician or pharmacist ban as a hard constraint                                                                                                  | Judges the interaction itself                                                 |
| Potassium-sparing diuretic, ACE inhibitor, ARB                | Treats potassium salts as off the table without clinician approval                                                                                                                                        | Offers a salt substitute                                                      |
| Pregnancy, uncomplicated                                      | Applies `food-safety.md` and section 3.3; no weight or calorie targets                                                                                                                                    | Labels a dish "safe in pregnancy"                                             |
| Pregnancy with complications                                  | Declines to draft therapeutic guidelines; refers                                                                                                                                                          | Adjusts carbohydrate, salt or energy                                          |
| Eating-disorder history or signs                              | Uses neutral language; no calories, macros, weight goals, "good" and "bad" food lists or portion cuts; signposts specialist help, on history as well as when signs are present                                                 | Offers weight-loss framing or calorie counts                                  |
| Anaphylaxis history, severe allergy                           | Hard exclusion with cross-contact notes; suggests an allergist or dietitian for growth and nutrition planning; asks to confirm labels                                                                     | Tests tolerance, accepts "may contain", guarantees allergen-free              |
| Suspected anaemia or supplement request                       | Explains that diet cannot diagnose it; recommends clinical assessment                                                                                                                                     | Gives an iron or vitamin dose                                                 |
| Alarm signs (weight loss, swallowing, blood in stool)         | Gives a clear, calm recommendation to see a doctor soon, then continues with ordinary cooking help only if asked                                                                                          | Adds more restriction                                                         |
| Medical diet requested (ketogenic, fasting, very low calorie) | Declines to design it; offers general cooking help                                                                                                                                                        | Writes the plan                                                               |
| User asks for a therapeutic guideline in any listed condition | Explains the limit once, offers an everyday-healthy guideline built on the shared core (when safe to do so) plus a slot for clinician-set limits                                                          | Drafts condition-specific targets                                             |

Clinician-set limits are recorded with who set them and when, never extended, rounded or "optimised". Emergencies (breathing difficulty, swelling, collapse) get an instruction to call the local emergency number. The disclaimer never replaces this behaviour (section 7.3).

## 7. Wording, disclaimer and the myths filter

### 7.1 Descriptive wording, never a health claim

The repo is public and health-adjacent. Describe what is in the dish and what changed; do not promise what it does to a body.

| Instead of                                                | Write                                                                                               |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| "This recipe lowers your cholesterol"                     | "This version uses rapeseed oil instead of butter, so it has less saturated fat than the original"  |
| "Heart-healthy", "diabetes-friendly", "anti-inflammatory" | "Contains oats and lentils, which are fibre-rich"; "about 25 g carbohydrate per serving (estimate)" |
| "Boosts iron", "fixes anaemia"                            | "Pairs lentils with peppers (vitamin C) in the same meal"                                           |
| "Superfood", "detox", "clean", "guilt-free"               | Name the nutrient or the culinary role                                                              |
| "Safe in pregnancy", "allergen-free"                      | State which listed rules were checked and what remains for the user to check                        |
| "One meal covers your needs"                              | "Contributes to the day's intake"                                                                   |

- EU Regulation 1924/2006 allows only authorised nutrition and health claims, with their conditions of use; disease-risk wording needs specific authorisation. A cooking tool is not selling a product, but copying claim wording into recipe headlines can read like a claim. Keep authorised phrases to explanations of an ingredient, with their conditions, and never as a recipe promise. Check the EU register before using any wording; the oat beta-glucan cholesterol claim is authorised, the January 2026 EFSA opinion on glucose was not yet an authorised claim (Claude only, to verify).
- US food claims have separate standards for authorised, qualified and structure-function statements, and disease-treatment claims are not allowed for foods. Same rule: describe, do not claim.
- Say "supports", "fits" and "is consistent with"; never "treats", "cures", "prevents".
- When a lever is graded low, say it is low-certainty or leave it out.

### 7.2 Myths filter (do not repeat as fact)

| Claim                                                           | Position the plugin takes                                                                                                                             |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Superfoods prevent or cure disease                              | Patterns matter, not single foods                                                                                                                     |
| Detox diets, juice cleanses                                     | Liver and kidneys do that job; no credible evidence for products                                                                                      |
| Coconut oil is heart-healthy; butter or tallow are healthy fats | High in saturated fat, raises LDL; WHO advises replacement with unsaturated fat. Mention that US 2025-2030 messaging differs                          |
| Seed oils are toxic or inflammatory                             | Replacing saturated fat with polyunsaturated oils lowers LDL; repeated deep-frying is a separate issue                                                |
| Raise HDL with food X                                           | HDL is not a dietary target                                                                                                                           |
| Alkaline foods or water change blood pH                         | Blood pH is tightly regulated                                                                                                                         |
| Vinegar, cinnamon or lemon water burns fat or treats diabetes   | Small, low-certainty effects at most                                                                                                                  |
| Eggs banned, or unlimited                                       | Both overstated; moderate amounts fit                                                                                                                 |
| Gluten-free is healthier for everyone                           | Matters for coeliac disease or declared sensitivity only; many such products have less fibre                                                          |
| Carbohydrates are fattening; one ideal macro split exists       | Energy balance and carbohydrate quality (fibre) matter; eating late is not special                                                                    |
| Everyone needs 1.2-1.6 g per kg protein                         | Contested; general adult reference is lower; not for children or kidney disease                                                                       |
| Microwaving destroys nutrients                                  | With little water it often retains more water-soluble vitamins than boiling                                                                           |
| Alcohol cooks off completely                                    | Not fully (section 2.8)                                                                                                                               |
| Supplements outperform or replace a healthy diet                | Trials are largely null for general populations; targeted advice comes from clinicians                                                                |
| Raw honey or "natural sugar" is fine for babies                 | Honey is unsafe below 12 months; honey, syrups and juices all count as free sugars                                                                    |
| Red meat is essential for iron; plant diets cannot supply iron  | Heme iron absorbs better, but planned plant meals with vitamin C meet most needs; infants, menstruating and pregnant people need attention, not alarm |
| Raw is always better                                            | Raw food has safety limits for vulnerable groups; cooking improves some nutrients                                                                     |
| Plant-based means cholesterol-friendly                          | Check the actual fat and ingredients                                                                                                                  |
| Calcium cancels all the iron in a meal                          | Effect shrinks in mixed diets; do not remove dairy wholesale                                                                                          |

### 7.3 The one-time disclaimer (what it must say)

Shown once during onboarding, plain language, in the user's language. It must say:

1. The tool offers general information to support healthy everyday cooking; it is not medical advice and does not diagnose, treat, cure or prevent disease.
2. It does not replace a doctor, registered dietitian or pharmacist, especially for medical conditions, medicines, pregnancy, infants and prescribed diets; clinician instructions come first.
3. The user is responsible for checking ingredient labels for allergens; cross-contact cannot be guaranteed.
4. Nutrient values are estimates and can differ from the real meal.
5. Guidance follows a named national authority chosen from the user's country, and some countries differ.
6. For a suspected allergic or medical emergency, call the local emergency number.

The disclaimer supplements the behaviour in section 6 and never excuses behaviour that crosses it. Health and allergy details are sensitive personal data: record only what the guideline needs.

## 8. Nutrient data

### 8.1 Source order

1. The user's registered food list (own products, labels, family recipes). It takes precedence over any database for the foods it covers.
2. An open database matched to the user's country, state its name and release in the output.
3. A nearby country's database as a labelled fallback; mismatch adds error.

### 8.2 Open databases

| Database                            | Coverage                                                                                      | Licence                                                     | Notes                                                                                                          |
| ----------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| USDA FoodData Central (FDC)         | Foundation, SR Legacy (final 2018), survey, branded and experimental foods; API with free key | Public domain (CC0 1.0); citation requested                 | Best for US and branded items; analytical (Foundation) versus label-derived (branded) values differ in quality |
| BLS 4.0 (Germany)                   | About 7,140 foods, 138 nutrients, composite dishes, recipe-calculation rules                  | Free since December 2025 under CC BY 4.0 (Claude, DeepSeek) | Attribution required                                                                                           |
| CoFID (UK, McCance and Widdowson's) | About 2,900 foods plus older entries, 185 nutrients; 2021 release                             | Open Government Licence                                     | Acknowledge the source                                                                                         |
| Ciqual (France, ANSES)              | About 3,480 foods, 74 constituents; 2025 release (Claude only, to verify the figures)         | Licence Ouverte 2.0 (Etalab)                                | Attribution required                                                                                           |
| USDA retention factors, Release 6   | About 290 foods and methods; 16 vitamins, 8 minerals, alcohol                                 | Public domain                                               | Needed to adjust cooked values                                                                                 |
| Canadian Nutrient File              | Canada                                                                                        | Not checked (Copilot named it only, to verify)              | Use only after checking its licence                                                                            |

Licence and release details were stated by two or fewer reports and change; recheck before embedding. "Viewable" does not mean "free to embed or redistribute".

### 8.3 Estimating a home recipe

1. Identify the food and its state (raw, cooked, drained, canned, dried).
2. Convert to edible weight; allow for peel, bone and discarded liquid.
3. Apply yield factors (water loss or gain, fat uptake) and retention factors where available; without them, boiled-vegetable vitamin C and folate can be overestimated by 40 percent or more (Claude).
4. Record the finished weight and divide by the real serving weight, not "into four".
5. Missing values stay missing, never zero. Do not compute absorbed iron with a fixed percentage.
6. Round: grams of energy and macronutrients to a sensible step, micronutrients as ranges.

### 8.4 What to show

- Rounded ranges with the source: "about 8-10 g fibre per serving (BLS 4.0, estimate)".
- Rough error expectation: energy and macronutrients about 10-20 percent, micronutrients 20-30 percent or more (DeepSeek only, to verify).
- Use numbers to compare recipes and see whether a target is plausible; never as a basis for insulin dosing, renal potassium or phosphorus limits, or other clinical decisions.
- Show sodium and salt with explicit units, counting packaged ingredients; treat "reduced salt" as a comparison, not as "low".

## 9. Checklist before presenting a healthier dish or a guideline

- Allergens, intolerance thresholds and absolute exclusions of everyone at the table checked, including substitutions and compound ingredients.
- Life-stage rules applied (section 3) and `food-safety.md` consulted for hazard limits; the most restricted person's portion set aside before seasoning.
- Screening questions asked before any guideline draft: medicines, kidney disease, pregnancy, eating-disorder history, allergies, country.
- No referral condition handled with therapeutic rules; clinician limits recorded verbatim with their source.
- Every target has a unit, a time horizon, a source and a certainty tag; no number the plugin made up.
- LDL, not HDL, is the lipid goal; the US divergence is named when it matters.
- No potassium salt substitute unless screening was clear; never in the shared base.
- Wording is descriptive; no health claim, no "safe in" or "free from" promise; myths filter passed.
- Nutrient values rounded, sourced and marked as estimates; the user's food list used first.
- One-time disclaimer shown at onboarding.

## 10. Evidence notes

### 10.1 Coverage

Five reports merged: Claude, Consensus, Copilot, DeepSeek, Perplexity. Claude is the deepest and supplies most of the numbers and the 2026 context. Consensus is a thin literature scan (patterns, LDL, iron, infant feeding; it states it found nothing on blood pressure, glucose, allergens, databases, pregnancy or older adults). Copilot is a short, ungraded overview with consistent direction. DeepSeek adds trial numbers and a clear structure table. Perplexity is cautious and marks much as unverified; it contributes the engineering rules (missing is not zero, jurisdiction versioning, acceptance tests) and the product-policy framing.

### 10.2 Conflicts and the default chosen

| Topic                     | Positions                                                                                                                                                        | Default                                                                                |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Mediterranean certainty   | Copilot: high for cardiovascular outcomes; Claude: Cochrane low to moderate; DeepSeek and Consensus: moderate (network meta-analysis), low in an umbrella review | Moderate for cardiovascular mortality in higher-risk adults, low to moderate elsewhere |
| Portfolio certainty       | Copilot: high; Claude and DeepSeek: moderate to high for LDL; Consensus: weak in an umbrella review                                                              | Moderate to high for LDL as a pattern; low for events                                  |
| DASH certainty            | Copilot and DeepSeek: high or moderate to high for blood pressure; Consensus: only suggestive; Perplexity: ungraded                                              | Moderate to high for blood pressure                                                    |
| Salt substitutes          | Claude: WHO conditional recommendation with exclusions; DeepSeek: effective, not for kidney disease; Perplexity: never recommend automatically                   | Not offered by default; only after a clear screen, as an adult-only branch             |
| Calcium and iron          | Claude, DeepSeek and Copilot: keep large dairy portions apart from iron sources; Perplexity: no blanket rule                                                     | Avoid pairing a big dairy portion with the main iron source; do not remove dairy       |
| Tea and coffee timing     | Four reports: between meals; Perplexity: needs checking                                                                                                          | Between meals, no fixed interval                                                       |
| Protein for adults        | US 2025-2030: 1.2-1.6 g per kg; other authorities and Claude: about 0.8 g per kg, higher only for older adults                                                   | 0.8 g per kg general; follow WHO/AHA/ACC on fats                                       |
| Added sugar age           | NHS: first year; older US: under 2; CDC 2026: under 11 (Perplexity only)                                                                                         | None under 2; later by country                                                         |
| Fibre target              | Claude: 25-29 g and above 30 g; Perplexity: do not publish a universal figure                                                                                    | Roughly 25-30 g for adults with source and country                                     |
| Intolerance as constraint | DeepSeek: hard in practice; Claude: dose-based                                                                                                                   | Hard at the stated threshold; exclude if none is stated                                |
| Oil for heat              | Claude and Copilot give lists; Perplexity warns against smoke-point rankings                                                                                     | Pick by method and stability; no universal ranking                                     |

### 10.3 Single-source claims carried over (all marked in the text)

US DGA 2025-2030 details and the ACC statement (Claude); DGE dairy and egg numbers (Claude); WHO sodium figure and January 2025 salt-substitute detail (Claude); 3 g beta-glucan gram range and the January 2026 EFSA glucose opinion (Claude); plant sterol labelling limits (Claude); sesame bakery loophole (Claude); Ciqual and BLS counts (Claude); protein per meal (Claude); potassium-salt blood-pressure effect size and error ranges for home recipes (DeepSeek); unfiltered-coffee LDL effect (Consensus); US iron reference values and the CDC added-sugar page (Perplexity); heterocyclic amine precaution (Claude); low-fat dairy age (DeepSeek); Canadian Nutrient File (Copilot). The US dietary guideline details and some EAT-Lancet 2025 quantities were drawn from secondary summaries: verify against primary texts before encoding as rules.

### 10.4 Not carried over

- Condition-specific diet plans, supplement doses, iron supplementation schedules, and low-FODMAP or dysphagia texture guidance: out of scope, referral material.
- EAT-Lancet quantities and the 15-million-deaths figure (model projection, not an observed outcome).
- Product, regulatory and legal worklists in the reports (medical-device classification, GDPR duties, app-store review): product and legal matters, not cooking knowledge. The plugin keeps to general-wellness behaviour.
- Hazard limits for leftovers, reheating, listeria and mercury: see `food-safety.md`.
