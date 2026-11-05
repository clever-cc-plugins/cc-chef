# Evidence-Based Nutrition for an International AI Cooking Assistant: A Technical Report

**Scope and standing disclaimer.** This report synthesises evidence suitable for a consumer-facing cooking assistant that supports _general healthier everyday eating_. It is **not** a clinical protocol. The assistant must not diagnose, treat, or replace individualised advice from a physician or registered dietitian. Where red flags appear—severe allergy, chronic kidney disease, eating disorders, pregnancy complications, food–drug interactions, or diagnosed diabetes on medication—the assistant should surface a clear referral message and stop short of therapeutic recommendations.

---

## 1. Evidence-Based Dietary Patterns

### 1.1 Mediterranean diet

**Core principles.** A plant-forward pattern emphasising vegetables, fruits, legumes, whole grains, nuts, olive oil as the principal added fat, moderate fish and poultry, low red and processed meat, and moderate dairy; meals are built around minimally processed foods and shared eating.

**Health outcomes evidenced.** An umbrella review of 18 meta-analyses of RCTs found that compared with usual care the Mediterranean diet was associated with reduced cardiovascular mortality (GRADE **low certainty**; risk ratio range 0.35–0.90) and reduced non-fatal myocardial infarction compared with active interventions. A BMJ network meta-analysis of structured dietary programmes found that for **cardiovascular mortality**, only Mediterranean dietary programmes were convincingly superior to minimal intervention, based on **moderate certainty** evidence (OR 0.55, 95% CI 0.39–0.78); for all-cause mortality the estimate was also moderate certainty (OR 0.72, 0.56–0.92). The apparent discrepancy is instructive: the umbrella review graded certainty conservatively because of methodological limitations in the underlying reviews, while the BMJ network meta-analysis applied GRADE to the direct randomised comparisons. For a cooking assistant, the defensible summary is: **moderate certainty for cardiovascular mortality reduction in higher-risk adults; lower certainty for primary prevention and for total mortality**.

**Strength of evidence.** Moderate for fatal cardiovascular outcomes in secondary prevention and high-risk primary prevention; low-to-moderate for other outcomes. The pattern is one of the best-evidenced whole-diet approaches.

### 1.2 DASH diet

**Core principles.** High intakes of vegetables, fruits, low-fat dairy, whole grains, poultry, fish, and nuts; reduced saturated fat, total fat, red and processed meat, sweets, and sodium. DASH is explicitly designed as a blood-pressure-lowering pattern.

**Health outcomes evidenced.** A systematic evidence map prepared for US federal review concluded that DASH reduced systolic and diastolic blood pressure in adults with or without hypertension ( **moderate certainty** ), and that higher DASH adherence was associated with lower all-cause mortality ( **moderate to high certainty** in cohort analyses). A network meta-analysis of 67 trials ranked DASH as the most effective dietary approach for reducing both systolic and diastolic blood pressure in hypertensive and pre-hypertensive patients ( **high certainty** ). A 2026 systematic review found that DASH was not _superior_ to all alternative dietary interventions for blood pressure, with certainty ranging from moderate to very low across outcomes; this does not overturn the core evidence but warns against overstating DASH’s unique superiority.

**Strength of evidence.** **Moderate-to-high** for blood pressure; **moderate** for mortality associations. DASH is the pattern with the most consistent RCT evidence for a single physiological outcome (BP).

### 1.3 Portfolio diet

**Core principles.** A plant-based pattern that deliberately combines four recognised cholesterol-lowering food components: nuts, plant protein (especially soy), viscous/soluble fibre, and plant sterols/stanols, on a background diet low in saturated fat.

**Health outcomes evidenced.** A systematic review and meta-analysis of controlled trials using GRADE found that the Portfolio pattern combined with an NCEP Step II diet reduced LDL cholesterol by approximately **17%** (MD −0.73 mmol/L, 95% CI −0.89 to −0.56) in adults with hyperlipidaemia, with improvements in non-HDL cholesterol, apolipoprotein B, triglycerides, and blood pressure. A separate network meta-analysis found that among popular named diets, the Mediterranean diet was most effective for LDL reduction with moderate certainty, while Portfolio was possibly the most effective among diets supported by only low or very low certainty. The most defensible reading is that the Portfolio _components_ have strong evidence individually, and the combined pattern produces clinically meaningful LDL lowering, but the certainty for the combined pattern is limited by the small number of trials.

**Strength of evidence.** **Moderate** for LDL lowering; lower for hard cardiovascular endpoints.

### 1.4 Nordic diet

**Core principles.** A regional plant-forward pattern emphasising Nordic foods: whole-grain rye, oats and barley, root vegetables, cabbage, berries, rapeseed (canola) oil, fish, legumes, and game; limited processed meat, added sugar, and salt.

**Health outcomes evidenced.** A 2025 GRADE-assessed systematic review and meta-analysis of 32 prospective cohorts and 15 RCTs found that higher Nordic diet adherence was associated with lower all-cause mortality (RR 0.78, 95% CI 0.71–0.86), cardiovascular mortality (RR 0.84, 0.79–0.80), cancer mortality (RR 0.86, 0.81–0.91), and lower incidence of type 2 diabetes (12%), cardiovascular disease (8%), coronary heart disease (11%), stroke (12%), and cancer (16%). RCTs showed improvements in fasting glucose, insulin, lipids, and blood pressure, but no effect on HDL cholesterol or C-reactive protein. A separate systematic review concluded that Nordic dietary patterns are associated with generally small but important reductions in major CVD outcomes and diabetes incidence, with similar or greater reductions in LDL cholesterol.

**Strength of evidence.** **Moderate** for mortality and cardiometabolic associations from cohort data; **low-to-moderate** for causal RCT outcomes.

### 1.5 EAT-Lancet planetary health diet

**Core principles.** A reference diet designed to operate within planetary boundaries: approximately half the plate (by energy) from vegetables and fruits, with substantial whole grains, plant proteins, nuts and seeds, unsaturated oils, moderate fish and poultry, and very low red meat, processed meat, added sugar, and starchy vegetables. It is explicitly a sustainability-oriented pattern.

**Health outcomes evidenced.** A 2026 multidisciplinary systematic review and meta-analysis of 227 studies (79 in meta-analysis) found that higher adherence to the EAT-Lancet diet was associated with lower all-cause mortality (pooled HR 0.80, 95% CI 0.76–0.85; 17 cohorts, >1 million participants), lower cardiovascular disease (0.83, 0.74–0.94), and lower type 2 diabetes risk, but not lower cancer or dementia risk. The same review found that, on a global average, the diet would induce deficiencies in vitamin B12, calcium, iron, and zinc in adults, especially pregnant women, and that 1.6–3.0 billion people could not afford it. The health evidence is therefore best described as **moderate for associations with mortality and cardiometabolic outcomes**, with an explicit caveat about nutrient adequacy and affordability in some populations.

**Strength of evidence.** **Moderate** for observational associations; **low** for causal long-term outcomes; **high certainty** that the diet is not universally micronutrient-sufficient without fortification or careful planning.

### 1.6 National food-based dietary guidelines (FBDGs)

**Core principles across exemplars.**

- **German DGE / Nutrition Circle.** Uses mathematical optimisation incorporating nutrition, health, and environmental impact; emphasises plant foods, whole grains, and limited animal foods, with sustainability integrated into the food-group proportions.
- **UK Eatwell Guide.** Built on WHO recommendations, independent advisory committee reports, national diet and nutrition survey data, and environmental impact assessment; emphasises vegetables and fruits, whole grains, beans and pulses, moderate dairy and animal protein, and limited foods high in fat, salt, and sugar.
- **US Dietary Guidelines.** Derived from systematic evidence reviews, Dietary Reference Intakes, and food-pattern modelling; the 2025–2030 edition continues a food-pattern approach across age groups and emphasises nutrient-dense foods and limited added sugars, saturated fat, and sodium.
- **Health Canada’s Food Guide (2019).** Moved away from food groups and serving sizes toward a pattern approach: regular intake of vegetables, fruit, whole grains, and protein foods, with **plant-based protein foods encouraged more often**; the plate model is ½ vegetables and fruits, ¼ protein foods, ¼ whole-grain foods.

**Health outcomes evidenced.** FBDGs are not usually tested as single interventions in RCTs. Their evidence base is a synthesis of the patterns above, food-pattern modelling, and prospective cohort evidence. The **certainty is therefore indirect**: moderate for the dietary components they recommend (vegetables, whole grains, plant proteins, limited sodium/saturated fat), but low for the specific national visual tool as a behaviour-change instrument.

**What they have in common.** All six emphasise **plant foods** (vegetables, fruits, legumes, nuts, whole grains), **unsaturated fats** over saturated fats, **limited processed foods** high in salt, sugar, and refined starch, and **moderation of animal-source foods**, especially red and processed meat. They differ in how explicitly they incorporate **sustainability** (Nordic, EAT-Lancet, German DGE, and UK Eatwell more explicitly; US and Canadian guides less so) and in **food-group classification** (e.g., Canada’s 2019 guide abolished discrete food groups and serving counts).

---

## 2. Cooking-Relevant Levers for Common Health Goals

### 2.1 Blood lipids: lowering LDL cholesterol

| Lever                                      | Practical cooking action                                                                                                                                      | Expected effect                                                                                                                                                                                                                                                                  | Certainty         |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| Replace saturated fat with unsaturated fat | Swap butter, lard, coconut oil, and fatty processed meat for olive, rapeseed, sunflower, or soybean oil; trim visible fat; choose poultry and fish more often | Replacing palmitic acid (16:0) with unsaturated fatty acids lowered LDL cholesterol by **−0.36 mmol/L** (95% CI −0.50 to −0.21); replacing with oleic acid lowered LDL by **−0.16 mmol/L**; replacing butter with unsaturated-rich oils lowered LDL by **−0.20 to −0.42 mmol/L** | **Moderate–high** |
| Increase soluble/viscous fibre             | Oats, barley, psyllium, legumes, apples, citrus; add oats to baking, use legume purées in sauces                                                              | Each **5 g/day** increase in soluble fibre lowered LDL by **−5.57 mg/dL**; overall soluble fibre supplementation lowered LDL by **−8.28 mg/dL**                                                                                                                                  | **Moderate**      |
| Plant sterols/stanols                      | Use fortified spreads, yoghurts, or drinks; 1.5–3 g/day                                                                                                       | **7–12%** LDL reduction at 1.5–3 g/day; ~**8.8%** at a mean 2.15 g/day                                                                                                                                                                                                           | **High**          |
| Nuts                                       | 30–45 g/day unsalted nuts as snack or topping                                                                                                                 | LDL **−0.12 mmol/L** (95% CI −0.14 to −0.09) in updated meta-analysis                                                                                                                                                                                                            | **Moderate**      |
| Legumes/pulses                             | Replace some meat with beans, lentils, chickpeas; add to soups and stews                                                                                      | LDL **−0.14 mmol/L**; linear dose response for beans up to 1 cup/day                                                                                                                                                                                                             | **Moderate**      |
| Soy protein                                | Tofu, tempeh, edamame, soy milk; isolated soy protein                                                                                                         | Isolated soy protein lowered LDL by **−0.15 mmol/L** (95% CI −0.18 to −0.12) in a 2026 meta-analysis                                                                                                                                                                             | **Moderate**      |

**What the evidence says about raising HDL through diet.** Saturated fat raises HDL cholesterol, but it also raises LDL cholesterol, and the net effect on cardiovascular risk is unfavourable; current guidelines do **not** recommend increasing saturated fat to raise HDL. No dietary intervention has been shown to raise HDL cholesterol sufficiently to reduce cardiovascular events as a primary strategy. The cooking assistant should therefore **focus on LDL lowering and overall dietary pattern**, not on “HDL-boosting” claims. Certainty for a clinical benefit of diet-induced HDL raising: **low**.

### 2.2 Fibre intake

**Levers.** Increase vegetables, fruits, legumes, whole grains, nuts, and seeds; leave skins on where appropriate; use whole-grain flours and cereals; add legumes to mixed dishes; use fruit rather than juice. **Certainty: high** that higher fibre intake improves bowel function and is associated with lower risk of several chronic diseases; **moderate** for specific fibre types and health outcomes.

### 2.3 Iron

**Levers.** Heme iron (meat, poultry, fish) is more bioavailable than non-heme iron (legumes, cereals, vegetables). Non-heme iron absorption is enhanced by **vitamin C** and by meat/fish/poultry in the same meal, and inhibited by **phytates** (whole grains, legumes), **polyphenols** (tea, coffee, some vegetables), **calcium**, and some spices. Practical rules for the assistant: pair iron-rich plant foods with vitamin C-rich foods (citrus, peppers, tomatoes); advise **tea and coffee between meals rather than with iron-rich meals**; avoid adding large amounts of calcium-rich dairy to the main iron source at the same meal; use soaking, sprouting, or fermentation to reduce phytates where culturally appropriate. **Certainty: high** for mechanisms; **moderate** for clinical iron-status outcomes.

### 2.4 Blood pressure and sodium/potassium

**Levers.** Reduce added salt and high-sodium processed foods (bread, cheese, cured meats, sauces, stock cubes); use herbs, spices, citrus, and vinegar for flavour; increase potassium-rich foods (vegetables, fruits, legumes, nuts, potatoes). **Potassium-enriched, sodium-reduced salt substitutes** lowered systolic blood pressure by approximately **5.96 mmHg** in meta-analysis, with moderate certainty for blood-pressure reduction and less certain evidence for mortality and cardiovascular events. The assistant should note that salt substitutes are **not appropriate for people with kidney disease or on potassium-restricted diets** and should be framed as an optional swap, not a universal recommendation.

### 2.5 Blood glucose and type 2 diabetes

**Levers.** Choose whole grains over refined grains; higher whole-grain intake (50 g/day) is associated with a **24% lower risk** of type 2 diabetes (RR 0.761, 95% CI 0.700–0.828). Pair carbohydrates with protein, fat, and fibre; favour legumes, nuts, and non-starchy vegetables; limit sugar-sweetened beverages and refined starches. Cooking methods matter: **al dente** pasta and cooled/reheated starches can modestly lower glycaemic response, though the effect is smaller than overall pattern change. **Certainty: moderate** for whole grains and fibre; **moderate** for the plate model and portion control.

### 2.6 Weight management

**Levers.** Lower the energy density of meals by increasing vegetables and water-rich foods; use the plate model (½ non-starchy vegetables, ¼ protein, ¼ carbohydrate-rich food); control portion size with smaller plates and bowls; prioritise protein and fibre for satiety. Experimental evidence shows that serving **lower energy-dense foods** significantly reduces daily energy intake, and weight loss tends to be greater in lower energy-density conditions. Changing dietary energy density has **no significant effect on hunger but increases fullness** in meta-analysis. **Certainty: moderate** for energy density and portion size as levers.

### 2.7 Gut health

**Levers.** Diverse fibre sources (soluble and insoluble), fermented foods (yoghurt with live cultures, kefir, sauerkraut, kimchi, tempeh), and polyphenol-rich foods. Fibre is fermented by gut microbiota to short-chain fatty acids, which modulate gut barrier and immune function. Fermented-food consumption has been associated with modest improvements in gastrointestinal wellbeing, including bowel-movement frequency, and some trials suggest modest increases in microbial diversity. **Certainty: moderate** for fibre and bowel function; **low-to-moderate** for fermented foods and microbiota diversity; **insufficient** for specific “gut-healing” claims.

### 2.8 How cooking methods affect these levers

- **Water-soluble vitamins.** Boiling causes high losses: average **−51% vitamin C** and **−68% folates** on a fresh-matter basis, with smaller losses of carotenoids; steaming, microwaving, or pressure cooking generally retain more.
- **Minerals.** Retention varies by vegetable and method; microwave and grilling can give higher true retention for some minerals in some vegetables, while potatoes tend to lose more than other vegetables.
- **Frying and oil choice.** Frying adds fat and energy; the fatty-acid composition of the frying oil becomes part of the dish. For LDL lowering, unsaturated oils are preferable to butter, lard, or coconut oil. High-temperature frying can generate degradation products, so moderate temperatures and avoidance of repeated reheating of oils are prudent.
- ** Phytochemicals.** Steaming and stir-frying tend to retain higher levels of tannins, oxalates, and saponins than boiling or microwaving, while prolonged high-temperature frying can decrease flavonoids and phenolics.

---

## 3. Life-Stage Requirements

### 3.1 Infants and toddlers

- **Iron.** WHO recommends starting complementary feeding with **iron-rich foods** at 6 months and avoiding cow’s milk as a drink before 12 months; where anaemia prevalence is high, daily iron supplementation of **10–12.5 mg elemental iron** for 3 consecutive months is recommended for infants and young children aged 6–23 months. The home-cooking implication is to include heme-iron foods (meat, fish, poultry) or well-absorbed plant iron with vitamin C at complementary meals.
- **Salt and added sugar.** Infant foods should not have added salt or sugar; kidneys cannot handle high sodium loads, and early preference formation matters. National guidance differs on the exact age thresholds for “no added salt” (usually under 12 months, with very low salt up to 2 years), but the direction is universal.
- **Honey under 12 months.** Honey must **never** be given to infants under 12 months because it may contain _Clostridium botulinum_ spores and cause infant botulism; this is consistent across WHO, US CDC, and national food-safety authorities.
- **Choking hazards and textures.** Avoid whole grapes, raw carrots, hard dried fruit, nuts, seeds, popcorn, and round candies for young children; foods should be cut into safe shapes, grated, mashed, or cooked to a soft texture. WHO explicitly advises avoiding foods in a form that may cause choking, such as whole grapes or raw carrots. The risk period extends to about **4–5 years** for hard round foods in many national guidance documents.
- **Textures.** Progress from puréed to mashed to lumpy to family foods, respecting developmental readiness; avoid force-feeding and respect hunger/fullness cues.

**Certainty: high** for honey avoidance, iron-rich complementary feeding, and choking-hazard avoidance; **moderate** for exact texture progression timing, where guidelines vary.

### 3.2 Children

Children generally can eat family meals with attention to: adequate iron and zinc (especially if plant-based), limited added sugar and salt, appropriate portion sizes, and avoidance of choking hazards up to school age. National authorities differ on the age at which low-fat dairy is appropriate (generally not before 2 years, and whole-fat dairy is often recommended in early childhood). The assistant should avoid rigid restriction unless a medical indication exists.

### 3.3 Pregnancy and breastfeeding

- **Listeria.** Avoid raw or unpasteurised dairy products, soft mould-ripened cheeses, pâté, refrigerated smoked seafood, and ready-to-eat deli meats unless reheated steaming hot. National lists differ in detail (e.g., some authorities allow certain pasteurised soft cheeses), but the **hard constraint** is avoidance of high-risk listeria foods.
- **Mercury in fish.** Avoid shark, swordfish, king mackerel, marlin, and tilefish; limit other large predatory fish; choose lower-mercury fish and cook seafood thoroughly. US FDA/EPA advice encourages **2–3 servings per week** of lower-mercury fish.
- **Raw or undercooked foods.** Avoid raw eggs unless they are pasteurised or “British Lion”–marked in the UK; avoid raw sprouts, raw seafood, and undercooked meat. National guidance differs on raw egg (UK NHS permits British Lion eggs for some pregnant women; US FDA advises against raw eggs for at-risk groups).
- **Alcohol and high-dose vitamin A.** Avoid alcohol; avoid liver and liver products because of preformed vitamin A.

**Certainty: high** for listeria and mercury avoidance; **high** for avoiding raw foods of animal origin; **moderate** for the exact composition of “safe fish” lists, which vary by country.

### 3.4 Older adults

- **Protein.** ESPEN and the PROT-AGE study group recommend **1.0–1.2 g/kg body weight/day** for healthy older adults (>65 years), and **1.2–1.5 g/kg/day** for those with acute or chronic illness, to support muscle mass and function and reduce sarcopenia risk. The home-cooking implication is to include a protein source at each meal and to favour soft, easy-to-chew protein foods (fish, eggs, dairy, legumes, minced meat) where dentition is poor.
- **Vitamin D and calcium.** Many national guidelines recommend supplementation of vitamin D in older adults, especially those with limited sun exposure; this is outside the cooking assistant’s remit but can be flagged as a common co-recommendation.
- **Energy and nutrient density.** Older adults may need **smaller portions but higher nutrient density**; fortifying meals with protein, healthy fats, and micronutrient-rich ingredients is a legitimate cooking lever.

**Certainty: moderate-to-high** for protein targets; **high** for the general principle of nutrient-dense, protein-sufficient meals in ageing.

### 3.5 Where national authorities differ

National differences exist in: the age at which low-fat dairy is introduced; the exact list of listeria-risk foods; whether raw eggs from certain assurance schemes are permitted in pregnancy; the recommended age for avoiding whole nuts and round foods (often 4–5 years, but some countries say 3 years); and vitamin D supplementation thresholds. The cooking assistant should therefore **ask for the user’s country** and apply the relevant national food-safety authority’s list rather than a single global rule for these contested details.

---

## 4. Allergies, Intolerances, and Preferences

### 4.1 Regulated major allergens

**EU list of 14 (Regulation 1169/2011, Annex II).** Cereals containing gluten (wheat, rye, barley, oats, spelt, kamut, and hybrids); crustaceans; eggs; fish; peanuts; soybeans; milk (including lactose); tree nuts (almonds, hazelnuts, walnuts, cashews, pecans, Brazil nuts, pistachios, macadamia nuts); celery; mustard; sesame seeds; sulphur dioxide and sulphites above 10 mg/kg or 10 mg/L; lupin; molluscs.

**US list of 9 (FALCPA as amended by the FASTER Act 2021).** Milk, eggs, fish (e.g., bass, flounder, cod), crustacean shellfish (crab, lobster, shrimp), tree nuts (almonds, walnuts, pecans), peanuts, wheat, soybeans, and **sesame** (effective 1 January 2023).

**Cross-contact basics.** For a cooking assistant, cross-contact advice must be conservative: separate utensils, cutting boards, and pans; wash hands and surfaces; avoid shared fryers, grills, or toasters; read labels for “may contain” statements; and never assume that removing an allergen ingredient from a recipe makes it safe if the ingredient was present during cooking or preparation.

### 4.2 Allergy vs. intolerance vs. preference

- **Allergy** is an immune-mediated reaction that can be immediate and life-threatening (IgE-mediated anaphylaxis) or delayed (non-IgE-mediated). It is a **hard constraint**: never relax, never “test”, never suggest that a small amount is acceptable.
- **Intolerance** is a non-immune adverse reaction (e.g., lactose intolerance, histamine intolerance). It is also a **hard constraint in practice** for the assistant, because the user has told the assistant that the food causes symptoms; the mechanism does not make the constraint optional.
- **Preference** is a voluntary choice (vegan, halal, kosher, low-carbon, dislike of mushrooms). It should be respected as a **soft or hard constraint depending on the user’s framing**, but it is not a safety constraint unless the user says it is absolute.

### 4.3 Which constraints must never be relaxed

The assistant must treat the following as **inviolable hard constraints**:

- Any user-declared **IgE-mediated food allergy** (peanut, tree nut, shellfish, fish, egg, milk, sesame, soy, wheat, etc.).
- **Coeliac disease** and **non-coeliac gluten sensitivity** when declared—gluten must be treated as a strict avoidance, not a preference.
- **Severe intolerance** with a declared risk of significant symptoms (e.g., severe lactose intolerance, sulphite sensitivity).
- **Anaphylaxis history** to any food.
- **Religious or ethical constraints** that the user has marked as absolute (e.g., halal, kosher, vegan).

The assistant should **never** suggest “may contain” foods to an allergy user, never suggest that cooking destroys an allergen (it usually does not), and never provide a recipe that requires the user to “pick out” an allergen.

---

## 5. From Goals to Practical Cooking Rules

### 5.1 How dietitians translate guidelines

Dietitians use several practical tools that can be built directly into a cooking assistant:

- **Prefer / limit / avoid lists.** For each food group, a three-tier list allows flexibility while preserving the direction of the evidence. Example for LDL lowering: _prefer_ oats, barley, legumes, nuts, fatty fish, olive/rapeseed oil; _limit_ butter, fatty cheese, red meat, pastries; _avoid_ trans fats, processed meats, and coconut oil in routine cooking.
- **Swap lists.** Specific, gram-for-gram or household-measure swaps that preserve the role of an ingredient: butter → olive oil; white rice → brown rice or barley; minced beef → lentils or a lentil–beef blend; regular cheese → smaller amount of strong-flavoured cheese; salt → herbs, citrus, vinegar, spices.
- **Plate models.** The most widely used is **½ plate non-starchy vegetables, ¼ protein foods, ¼ whole-grain or starchy foods**; this is used by Health Canada, the American Diabetes Association, and many European dietetic associations. It is a **portion and proportion heuristic**, not a nutrient prescription, and it adapts well to mixed dishes.
- **Portion guides.** Hand measures (palm of protein, fist of vegetables, cupped hand of carbohydrates, thumb of fats) are useful for users who do not weigh food. They are less precise but more acceptable for everyday cooking.
- **Food lists with frequency guidance.** “Oily fish 1–2 times per week”, “legumes 3–4 times per week”, “red meat ≤ 1 time per week” are examples of frequency-based rules that translate evidence into cooking rotation.

### 5.2 Structuring a personal guideline document for cooking

A well-designed personal guideline for a cooking assistant should separate **hard constraints, targets, and preferences** in a machine-readable way:

| Layer                | Definition                                            | Example                                                                                                                           | Assistant behaviour                                                                                                       |
| -------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Hard constraints** | Absolute exclusions; never relax                      | “Peanut allergy”; “Coeliac disease”; “Vegan”; “Halal”                                                                             | Recipe must not contain the ingredient or any cross-contact risk; if a recipe cannot be made safe, suggest an alternative |
| **Targets**          | Quantitative or frequency goals                       | “LDL lowering: ≥10 g soluble fibre/day”; “Iron: red meat 2×/week + vitamin C at meals”; “Sodium <2 g/day”; “Protein 1.2 g/kg/day” | Optimise recipes toward the target; show approximate contribution; do not claim therapeutic effect                        |
| **Preferences**      | Soft constraints; may be overridden for a good reason | “Prefer chicken over beef”; “Dislike mushrooms”; “Low-carbon”                                                                     | Respect by default; may offer a justification if an exception would meaningfully improve the target                       |

The document should also record **country**, because food-safety and fortification rules differ; **life stage**; **allergies/intolerances**; **medications with food interactions** (see §7); and **cooking constraints** (equipment, time, budget).

### 5.3 Cooking one meal for several people with different needs

**Worked example: an adult with high LDL and a toddler who needs iron.**

The trap is to design two separate meals. The better approach is to **build a base meal that is safe and suitable for everyone, then apply modular additions**.

- **Base:** a lentil–tomato stew with onions, garlic, carrots, and spices, served with whole-grain flatbread or rice. This is low in saturated fat, high in soluble fibre and legumes (LDL-lowering), and provides non-heme iron.
- **Adult LDL module:** top with a small handful of unsalted nuts; use olive oil for cooking; add a side of steamed green vegetables; no butter or cheese. The adult’s LDL target is supported by the legume base, nuts, and unsaturated oil.
- **Toddler iron module:** add a small portion of shredded cooked chicken or minced beef to the toddler’s serving, plus a spoon of tomato purée or a few strips of red pepper (vitamin C) to enhance non-heme iron absorption; **do not add salt** to the toddler’s portion; cut the flatbread into soft strips and ensure the lentil pieces are soft and mashable.
- **Shared safety:** the dish contains no honey, no whole nuts for the toddler (nuts are used only for the adult, and the toddler’s portion is served before the nuts are added), and no added salt until the toddler’s portion is removed.

This modular method respects the **adult’s LDL target**, the **toddler’s iron need and choking/salt constraints**, and the **shared meal** that makes home cooking sustainable.

---

## 6. Nutrient Data

### 6.1 Reliable food composition databases

| Database                                                                       | Country/region | Accessibility and licensing                                                                                                                         | Notes for a commercial cooking assistant                                            |
| ------------------------------------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **USDA FoodData Central**                                                      | USA            | Public domain, **CC0 1.0 Universal**; free API key from data.gov; no permission needed, attribution requested as a courtesy                         | Best for US foods and branded items; large and API-friendly; not a global database  |
| **German Bundeslebensmittelschlüssel (BLS)**                                   | Germany        | Since December 2025, **free of charge and without licence barriers**; data available under **CC BY 4.0**; >7,000 foods                              | Strong for German/European foods; good micronutrient coverage; attribution required |
| **UK CoFID (McCance and Widdowson’s Composition of Foods Integrated Dataset)** | UK             | Free from the UK government web archive; data subject to the **Open Government Licence for Public Sector Information**; source must be acknowledged | Strong for UK foods and recipes; updated periodically; API available via FN-NBRI    |
| **French Ciqual**                                                              | France         | Published by ANSES; **Licence Ouverte 2.0** (Open Licence 2.0)                                                                                      | Strong for French foods; good for European composite dishes; attribution required   |

**Other useful sources.** The FAO/INFOODS network provides harmonised datasets and guidance on recipe calculation; the European Food Safety Authority (EFSA) publishes retention factors and recipe-calculation procedures that are useful for estimating cooked dishes.

### 6.2 Accuracy limits of estimating nutrient content of a home-cooked recipe

Even with a perfect database, recipe-level nutrient estimates carry **substantial uncertainty**. The main sources are:

1. **Natural variability of ingredients.** The nutrient content of a tomato, a cut of meat, or a handful of lentils varies with variety, season, soil, feed, and storage. Database values are means, not guarantees.
2. **Cooking losses and retention factors.** Vitamins are destroyed or leached; minerals may be lost in cooking water or concentrated by water loss. Retention factors are available for only a limited set of food-group/cooking-method combinations and rarely account for home-kitchen variables such as pan material, lid use, or exact temperature.
3. **Recipe calculation methods.** The FAO mixed-method approach—weight change at the whole-recipe level, nutrient retention at the ingredient level—is preferred, but it still requires assumptions about edible portion, yield, and retention.
4. **Portion size.** Users estimate portions poorly; a “cup” of cooked rice or a “tablespoon” of oil can vary by 20–50%. The assistant should present nutrient values as **approximate and directional**, not as precise measurements.
5. **Database mismatch.** A food in one national database may differ substantially from the same-named food in another; using a database from a different country introduces error.

**Practical rule for the assistant.** Use nutrient data to **rank and compare recipes**, to check that a target is plausibly met, and to flag large differences. Do **not** present nutrient values as exact or as a basis for medical decisions. Add a note that home-cooked values may differ by ±20–30% or more for micronutrients and by ±10–20% for energy and macronutrients.

---

## 7. Boundaries and Red Flags

### 7.1 Where general healthy-eating support ends and medical nutrition therapy begins

The assistant must recognise the following as **outside its scope** and route the user to a doctor or registered dietitian:

- **Chronic kidney disease (CKD).** Protein, potassium, phosphorus, sodium, and fluid targets are individualised and change with disease stage and dialysis status. The US NIDDK explicitly recommends referral to a registered dietitian with CKD expertise for medical nutrition therapy, which can delay progression. A generic “healthy” diet can be dangerous in CKD (e.g., high-potassium salt substitutes, high-protein advice).
- **Diagnosed diabetes on medication** (insulin or sulfonylureas). Carbohydrate consistency and hypoglycaemia risk require individualisation; the assistant can support general healthy eating but must not adjust medication or set therapeutic carbohydrate targets.
- **Eating disorders and disordered eating.** Nutritional advice can inadvertently reinforce restriction or binge–purge cycles. Red flags include BMI <16 kg/m², unintentional weight loss >15% in 3–6 months, little or no intake for days, electrolyte abnormalities, and purging behaviours. The assistant should not provide calorie targets, “safe food” lists, or weight-loss plans to a user who discloses an eating disorder; it should encourage professional support.
- **Food–drug interactions.**
  - **Vitamin K and vitamin K antagonists (warfarin, phenprocoumon).** Patients are advised to keep vitamin K intake **consistent day to day**, not to avoid green vegetables altogether; sudden increases or decreases in vitamin K–rich foods can destabilise anticoagulation. The assistant should flag this and recommend consistency, not a specific gram target.
  - **Grapefruit and CYP3A4.** Grapefruit, Seville oranges, pomelo, and some limes inhibit intestinal CYP3A4 and can raise blood levels of many drugs (statins, calcium-channel blockers, immunosuppressants, some psychiatric drugs). The FDA requires warnings on affected drugs; the assistant should treat grapefruit as a **potential hard constraint** when the user lists a relevant medication and should advise checking with a pharmacist.
- **Severe allergies and anaphylaxis.** Already covered in §4; the assistant must not relax these constraints and should encourage an emergency action plan.
- **Pregnancy complications** (gestational diabetes, pre-eclampsia, hyperemesis, multiple pregnancy, previous pregnancy loss, severe anaemia). These require obstetric and dietetic input; general pregnancy food-safety advice is not sufficient.

### 7.2 Signals that should prompt a referral

The assistant should surface a clear referral message when the user reports any of the following:

- **Unintentional weight loss** (>5% in 1 month, >10% in 6 months) or **failure to thrive** in a child.
- **Persistent GI symptoms** (diarrhoea, constipation, bloating, pain) that are severe, new, or associated with weight loss or bleeding.
- **Dysphagia** (difficulty swallowing) or **choking episodes**.
- **Known or suspected food allergy** with any systemic reaction (hives, swelling, breathing difficulty, hypotension).
- **Diagnosis of CKD, liver disease, pancreatitis, or active cancer**.
- **Medication use** that interacts with food (warfarin, MAOIs, immunosuppressants, some antibiotics, grapefruit-sensitive drugs).
- **Pregnancy** with any complication or with a pre-existing medical condition.
- **Eating-disorder red flags** (see above).
- **Infant under 12 months** with suspected botulism symptoms (constipation, weak suck, lethargy, poor feeding) after honey exposure—urgent medical assessment.
- **Severe malnutrition** or **refeeding risk** (low BMI, low electrolytes, little intake for >5–10 days).

### 7.3 Regulatory and ethical considerations for consumer nutrition tools

- **EU health-claim regulation (EC) No 1924/2006.** Nutrition and health claims on foods must be scientifically substantiated; EFSA assesses the evidence and the Commission authorises claims. A cooking assistant that is not selling a food product has more latitude, but it should avoid making **disease-risk-reduction claims** or **therapeutic claims** for recipes. The safe formulation is “supports” or “contributes to” a dietary pattern, with a clear statement that the evidence is general and not individual medical advice.
- **US structure/function claims and DSHEA disclaimer.** For dietary supplements, structure/function claims must carry the disclaimer: “This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.” A cooking assistant does not sell supplements, but the same ethical principle applies: do not imply diagnosis, treatment, cure, or prevention.
- **General disclaimer for a cooking assistant.** A suitable disclaimer covers: (i) the assistant provides general information, not medical advice; (ii) it does not diagnose, treat, cure, or prevent any disease; (iii) users with medical conditions, allergies, pregnancy, or medication use should consult a qualified professional; (iv) nutrient values are estimates and may vary; (v) the assistant is not a substitute for a registered dietitian or physician.

---

## 8. Popular Claims to Avoid

The assistant should **not repeat** the following claims, or should reframe them with explicit uncertainty:

| Claim                                                      | Why it is problematic                                                                                                                                                                                                                            | What to say instead                                                                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **“Superfood”**                                            | No regulatory definition; implies a single food has exceptional health powers. The evidence supports **dietary patterns**, not magic bullets. Authorities note that “superfood” products are often insufficiently studied for health evaluation. | “This food is a good source of [nutrient/fibre]; it fits well within a plant-forward pattern.”                                                  |
| **“Detox” / “cleansing” / “removing toxins”**              | No scientific evidence that commercial detox products remove toxins; the body’s liver and kidneys perform detoxification. German authorities state that there is no scientific proof of efficacy for detox cures.                                | “The body detoxifies itself; a varied diet supports normal liver and kidney function.”                                                          |
| **Specific oil “cures” or “best oil” claims**              | Oils differ in fatty-acid composition and suitability for heating, but no single oil is a cure. Claims that one oil “unclogs arteries” or “burns fat” are unsupported.                                                                           | “For LDL lowering, replace saturated fats with unsaturated oils such as olive or rapeseed oil; use oils within overall energy needs.”           |
| **“Raising HDL is the key to heart health”**               | Saturated fat raises HDL but also LDL; no dietary intervention has reliably reduced cardiovascular events by raising HDL as a primary strategy.                                                                                                  | “Focus on lowering LDL and improving the overall pattern; HDL is not a reliable target for dietary change.”                                     |
| **Supplement claims that exceed authorised health claims** | Many supplements make claims not authorised under EU Regulation 1924/2006 or not supported by FDA-level evidence.                                                                                                                                | “Supplements may be appropriate for specific deficiencies or life stages on professional advice; they are not a substitute for a healthy diet.” |
| **“Gluten-free is healthier for everyone”**                | For people without coeliac disease or gluten sensitivity, there is no evidence that a gluten-free diet is healthier; it can reduce fibre and increase cost.                                                                                      | “Gluten avoidance is essential for coeliac disease; for others, whole grains are generally beneficial.”                                         |
| **“Raw is always better”**                                 | Raw foods carry food-safety risks (especially for pregnancy, young children, older adults, and immunocompromised people), and some nutrients are more bioavailable after cooking (e.g., lycopene, beta-carotene).                                | “Both raw and cooked foods have a place; food safety and bioavailability matter.”                                                               |

---

## Source List (APA Style)

Bakhshimoghaddam, F., et al. (2025). Nordic diet and chronic disease: A GRADE-assessed systematic review and meta-analysis of prospective cohorts and randomized controlled trials. _European Journal of Nutrition, 64_(7), 298. https://doi.org/10.1007/s00394-025-03820-9

Bensaaud, A., et al. (2025). Dietary Approaches to Stop Hypertension (DASH) for the primary and secondary prevention of cardiovascular diseases. _Cochrane Database of Systematic Reviews_.

Cai, Z., Wang, L., Zhang, B., & Zhu, A. (2024). Mediterranean diet for cardiovascular disease: An evidence mapping study. _Public Health Nutrition, 27_(1), e118. https://doi.org/10.1017/S1368980024000776

Chiavaroli, L., et al. (2018). Portfolio dietary pattern and cardiovascular disease: A systematic review and meta-analysis of controlled trials. _Progress in Cardiovascular Diseases, 61_(1), 43–53.

EFSA Panel on Dietetic Products, Nutrition and Allergies. (2010). Scientific opinion on dietary reference values for fats, including saturated fatty acids, polyunsaturated fatty acids, monounsaturated fatty acids, trans fatty acids, and cholesterol. _EFSA Journal, 8_(3), 1461.

European Commission. (2006). _Regulation (EC) No 1924/2006 of the European Parliament and of the Council of 20 December 2006 on nutrition and health claims made on foods_. Official Journal of the European Union.

European Parliament and Council. (2011). _Regulation (EU) No 1169/2011 on the provision of food information to consumers_. Official Journal of the European Union.

FAO/WHO. (2023). _WHO guideline for complementary feeding of infants and young children 6–23 months of age_. World Health Organization.

Filippou, C. D., et al. (2020). DASH diet and blood pressure: A systematic review and meta-analysis. _Advances in Nutrition, 11_(5), 1150–1163.

Food and Agriculture Organization of the United Nations. (2025). _Food-based dietary guidelines: Canada_. FAO.

Food and Drug Administration. (2023). _The FASTER Act: Sesame is the ninth major food allergen_. US Department of Health and Human Services.

Food and Drug Administration. (2024). _Structure/function and related claims in dietary supplement labeling_. US Department of Health and Human Services.

Food Standards Agency. (2021). _McCance and Widdowson’s The Composition of Foods Integrated Dataset (CoFID)_. UK Government.

German Federal Ministry of Food and Agriculture & Max Rubner-Institut. (2025). _Bundeslebensmittelschlüssel (BLS) 4.0 now freely available_.

Health Canada. (2019). _Canada’s dietary guidelines_. Government of Canada.

Hooper, L., et al. (2020). Reduction in saturated fat intake for cardiovascular disease. _Cochrane Database of Systematic Reviews_.

Jenkins, D. J. A., et al. (2018). Portfolio dietary pattern and cardiovascular disease: A systematic review and meta-analysis of controlled trials. _Progress in Cardiovascular Diseases, 61_(1), 43–53.

Jin, Y., et al. (2026). The health and environmental impacts, safety, and affordability of the EAT-Lancet planetary health diet: A multidisciplinary systematic review and meta-analysis. _Advances in Nutrition_.

Kris-Etherton, P. M., et al. (2026). Impact of soy protein on blood lipids: A systematic review and meta-analysis of randomized trials. _Journal of the American Heart Association_.

Lane, M. M., et al. (2023). Comparative effects of different dietary approaches on blood pressure: A systematic review and network meta-analysis. _Advances in Nutrition_.

Li, S., et al. (2023). Soluble fiber supplementation and serum lipid profile: A systematic review and dose-response meta-analysis of randomized controlled trials. _Frontiers in Nutrition, 10_, 1020167.

Massara, P., et al. (2022). Nordic dietary patterns and cardiometabolic outcomes: A systematic review and meta-analysis of prospective cohort studies and randomised controlled trials. _Diabetologia, 65_(12), 2011–2031.

National Institute of Diabetes and Digestive and Kidney Diseases. (2025). _Collaborate with a registered dietitian_. US Department of Health and Human Services.

National Health Service. (2024). _Foods to avoid in pregnancy_. UK Government.

Reynolds, A., et al. (2023). Effects of whole grains on glycemic control: A systematic review and dose-response meta-analysis of prospective cohort studies and randomized controlled trials. _European Journal of Nutrition_.

Schwingshackl, L., et al. (2018). Effects of oils and solid fats on blood lipids: A systematic review and network meta-analysis. _Journal of Lipid Research, 59_(9), 1771–1782.

Scientific Advisory Committee on Nutrition. (2023). _SACN report: Feeding young children aged 1 to 5 years_. UK Government.

US Department of Agriculture & US Department of Health and Human Services. (2025). _Dietary Guidelines for Americans, 2025–2030_.

USDA FoodData Central. (2024). _FoodData Central API guide: Licensing_. US Department of Agriculture.

World Health Organization. (2019). _Complementary feeding_. WHO.

World Health Organization. (2021). _WHO guideline: Daily iron supplementation in infants and young children_. WHO.

---

_Prepared for the design of a consumer-facing AI cooking assistant. All recommendations are general; users with medical conditions, allergies, pregnancy, or medication use should consult a qualified health professional._
