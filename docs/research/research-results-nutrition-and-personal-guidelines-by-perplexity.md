# Nutrition evidence for an AI cooking assistant

The safest foundation is **pattern-based recipe support with explicit, person-specific constraints**, not automated treatment: improve ingredient choices and meal composition, preserve food safety, and implement clinician-provided instructions without inventing therapeutic targets.

**Verification limitation:** This is a substantial but **incomplete evidence-and-design report**, not a completed systematic review. The sources available support the sections on dietary patterns, iron, complementary feeding, and selected national guidelines particularly well; current database licensing, complete allergen legislation, several clinical interventions, and detailed regulatory requirements could not be fully verified. Those gaps are identified rather than filled with unsupported certainty.

## Evidence interpretation

Two distinctions should govern the assistant’s knowledge base:

- **Evidence certainty is outcome-specific.** Evidence that a diet lowers LDL cholesterol is not automatically evidence that it prevents heart attacks.
- **Recommendation strength is not evidence certainty.** WHO’s complementary-feeding guideline includes strong recommendations supported by low-certainty evidence; practical considerations and the balance of potential benefits and harms also inform recommendations. [iris.who](https://iris.who.int/bitstream/handle/10665/373358/9789240081864-eng.pdf)

The report uses these labels:

| Label                             | Meaning here                                                                                             |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Source-graded**                 | The cited source explicitly reports GRADE or another evidence assessment.                                |
| **Supported; ungraded here**      | The source supports the statement, but a formal outcome-specific certainty rating has not been verified. |
| **Implementation recommendation** | A proposed product or recipe-engine rule, not a clinical finding.                                        |
| **Verification required**         | Insufficiently checked for production use; do not present it as established guidance.                    |

A production system should retain the source’s actual grading rather than generate a GRADE rating from the study design alone.

## 1. Evidence-based dietary patterns

### Patterns and outcomes

| Pattern                              | Core cooking principles                                                                                                                                                                                                             | Supported outcomes                                                                                                                                                                                                                                                                                     | Evidence assessment and limitations                                                                                                                                                                                                                                                             |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mediterranean**                    | Emphasize vegetables, fruit, legumes, whole grains, nuts, olive oil, and fish; reduce reliance on red and processed meat.                                                                                                           | The retrieved evidence describes favorable cardiovascular outcomes and intermediate cardiometabolic risk factors. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)                                                                                                                | **Supported; ungraded here.** An outcome-specific assessment of the primary trials and systematic reviews remains necessary before publishing numerical benefit estimates or a formal certainty label.                                                                                          |
| **DASH**                             | Operationally, build recipes around vegetables, fruit, whole grains, legumes, suitable dairy or alternatives, and lower-sodium ingredients.                                                                                         | The retrieved review identifies DASH among dietary patterns associated with improved cardiovascular outcomes and intermediate risk factors. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)                                                                                      | **Supported; ungraded here.** The specific blood-pressure effect, sodium interaction, and certainty grading were not independently verified for this report.                                                                                                                                    |
| **Portfolio**                        | Combine cholesterol-oriented food components rather than relying on one “cholesterol-lowering” ingredient: viscous-fiber foods, nuts, plant proteins, and, where appropriate, sterol-enriched products.                             | The retrieved literature identifies the Portfolio approach as a pattern with evidence concerning LDL and other cardiovascular risk factors. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)                                                                                      | **Supported; incompletely verified.** A controlled-trial meta-analysis is identified in the retrieved literature, but its complete results and grading should be checked before encoding quantitative doses or promises. Do not equate LDL lowering with proven cardiovascular-event reduction. |
| **Nordic**                           | Whole-grain rye, oats and barley; berries and temperate fruit; root and cruciferous vegetables; legumes; nuts; fish; rapeseed/canola oil; and suitable dairy. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/) | A systematic review included 15 prospective cohorts and six randomized trials. It found favorable associations with cardiovascular outcomes and diabetes incidence, alongside improvements in several intermediate risk factors. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/) | **Source-graded:** low certainty for total cardiovascular-disease incidence and LDL lowering; moderate certainty for cardiovascular mortality; other outcomes varied. LDL results were heterogeneous. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)                     |
| **EAT–Lancet planetary health diet** | Treat this as a proposed health-and-sustainability framework requiring separate verification of food-group quantities, nutritional adequacy, and population applicability.                                                          | **Verification required:** the original commission, subsequent updates, and outcome reviews were not sufficiently verified here.                                                                                                                                                                       | Do not describe the framework as though it were a single clinically tested prescription, or apply adult reference quantities directly to young children.                                                                                                                                        |

**Implementation recommendation:** Offer named patterns as optional recipe-selection frameworks, not as competing brands of “the healthiest diet.” Users should be able to obtain equivalent practical changes using affordable, culturally familiar ingredients.

### National food-based guidelines

| Jurisdiction                          | Verified guidance relevant to cooking                                                                                                                                                                                                                                                                                                                                                                                                      | Product implications                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Germany: DGE**                      | The 2024 recommendations emphasize a greater plant-food share, explicitly highlight legumes and nuts, and recommend no more than 300 g meat and processed meat per week and one to two fish portions weekly. [dge](https://www.dge.de/presse/meldungen/2024/gut-essen-und-trinken-dge-stellt-neue-lebensmittelbezogene-ernaehrungsempfehlungen-fuer-deutschland-vor/&rut=2205166fd7d93ac466eb524386ee0428f32c035825aaf1ccfcd41a6e071b5979) | Store the recommendation’s edition and intended population. Do not automatically translate adult weekly quantities into toddler portions.        |
| **United Kingdom: Eatwell Guide**     | The guide describes proportions across a day or week—not necessarily each meal—and does not apply directly to children under two; children aged two to five gradually move toward its proportions. [assets.publishing.service.gov](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/742750/Eatwell_Guide_booklet_2018v4.pdf?ContensisTextOnly=true)                                         | Avoid rejecting a meal simply because one plate does not reproduce the diagram. Use age-specific logic.                                          |
| **Canada: Food Guide**                | The plate model allocates half the plate to vegetables and fruit, one quarter to whole-grain foods, and one quarter to protein foods. [canada](https://www.canada.ca/en/health-canada/services/video/food-nutrition/plate-healthy-snacks.html)                                                                                                                                                                                             | Use this as a visual planning aid, not a precise nutrient calculation or mandatory distribution for every individual.                            |
| **United States: Dietary Guidelines** | The **2025–2030 edition was released in January 2026**. The official announcement emphasizes protein, full-fat dairy without added sugar, vegetables, fruit, whole grains, and reduced highly processed foods. [hhs](https://www.hhs.gov/maha/kennedy-rollins-unveil-historic-reset-nutrition-policy-real-food-back-center-health/index.html)                                                                                              | Do not silently serve the 2020–2025 edition as current. Distinguish the final policy document from the preceding scientific advisory report.     |
| **US advisory evidence**              | The 2025 advisory committee reaffirmed replacing saturated fat with unsaturated fat, particularly polyunsaturated fat, and replacing some meat with plant proteins, whole grains, or vegetables. [dietaryguidelines](https://www.dietaryguidelines.gov/sites/default/files/2024-12/Part%20D_Ch%204_Food%20Sources%20of%20Saturated%20Fat_FINAL_508.pdf)                                                                                    | Preserve disagreement between scientific-review recommendations and final policy messaging rather than merging them into a fictitious consensus. |

### Shared principles

The verified sources repeatedly emphasize vegetables, fruit, whole grains, legumes, nuts, and improved fat quality, although they differ in food-group proportions and treatment of animal foods. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)

**Implementation recommendation:** Build the default engine around that shared core. Make national guidance a versioned layer above it, and apply age, allergy, and clinician-specified rules before adult dietary-pattern preferences.

## 2. Cooking-relevant health levers

### LDL cholesterol

| Lever                              | Practical recipe changes                                                                                                                | Evidence assessment                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Replace saturated fat**          | Replace some butter, cream, and fatty meat with unsaturated plant oils, legumes, nuts, seeds, or appropriate plant-protein ingredients. | The US advisory review supports replacing saturated fat with unsaturated fat, particularly polyunsaturated fat, and identifies favorable cardiovascular outcomes for relevant food substitutions. **Supported; formal grading not verified here.** [dietaryguidelines](https://www.dietaryguidelines.gov/sites/default/files/2024-12/Part%20D_Ch%204_Food%20Sources%20of%20Saturated%20Fat_FINAL_508.pdf) |
| **Replace some meat**              | Use lentils in mince sauces; beans in stews; tofu in stir-fries; or smaller meat portions alongside legumes.                            | The advisory report identifies favorable cardiovascular associations for replacing meat with plant proteins, whole grains, or vegetables. **Supported; ungraded here.** [dietaryguidelines](https://www.dietaryguidelines.gov/sites/default/files/2024-12/Part%20D_Ch%204_Food%20Sources%20of%20Saturated%20Fat_FINAL_508.pdf)                                                                            |
| **Increase viscous-fiber foods**   | Incorporate oats, barley, legumes, and suitable recipe applications of other viscous-fiber ingredients.                                 | These are relevant components of cholesterol-oriented dietary patterns, but ingredient-specific effect sizes and doses require direct verification before production use.                                                                                                                                                                                                                                 |
| **Use nuts and soy appropriately** | Substitute rather than merely add: for example, replace some cheese or processed meat with an appropriate nut- or soy-based component.  | The broader pattern evidence is supportive; isolated effects, doses, and certainty were not fully verified here. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC9630197/)                                                                                                                                                                                                                    |
| **Plant sterols**                  | Treat sterol-enriched products as a separate, explicitly authorized intervention—not an automatic family-recipe upgrade.                | **Verification required:** dose, eligible populations, labeling, contraindications, and cardiovascular-outcome evidence.                                                                                                                                                                                                                                                                                  |

The assistant should describe a substitution precisely: **“This version uses less saturated fat than the original”** is a different claim from **“This will lower your LDL by a specified amount.”**

**HDL:** Do not optimize recipes to raise HDL as an independent treatment goal, recommend alcohol for that purpose, or assume that an HDL increase proves cardiovascular benefit. The necessary outcome-specific evidence was not adequately verified here; this should remain a conservative product rule pending a dedicated lipid-evidence review.

### Fiber intake

**Implementation recommendations:**

- Offer whole-grain substitutions that preserve the recipe’s function.
- Add legumes to soups, sauces, salads, and mixed dishes.
- Retain edible skins where suitable.
- Increase fiber progressively rather than maximizing it in every recipe.
- Keep adequate-energy and texture requirements separate from adult fiber goals.
- Express targets over the day or week; do not require each meal to hit an arbitrary fraction.

Do not publish a universal fiber target without specifying the jurisdiction, age group, reference system, and whether the number is a recommended intake, adequate intake, or another benchmark. The age-specific numerical targets were not sufficiently verified for this report.

### Iron and bioavailability

Heme iron occurs in meat, seafood, and poultry; plant foods and fortified foods supply non-heme iron, while animal foods can contain both forms. Heme iron generally has higher bioavailability. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

| Factor                               | Cooking translation                                                                            | Evidence and qualification                                                                                                                                                                                                                                                                                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vitamin C**                        | Pair legumes, tofu, or fortified foods with suitable vitamin-C-containing fruit or vegetables. | NIH identifies vitamin C as an enhancer of non-heme iron absorption. **Supported; ungraded here.** [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                                                                      |
| **Meat, poultry, seafood**           | Where compatible with the person’s diet, combine modest quantities with plant iron sources.    | These foods can enhance non-heme iron absorption as well as provide iron themselves. **Supported; ungraded here.** [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                                                      |
| **Phytate and some polyphenols**     | Do not assume that all iron listed in a grain- or legume-based meal is absorbed.               | NIH identifies phytate and certain polyphenols as inhibitors; however, meal-level effects do not translate straightforwardly into long-term iron status. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                |
| **Calcium**                          | Avoid a blanket rule that removes calcium-rich foods from an iron-conscious diet.              | Calcium may reduce iron absorption, but NIH notes uncertainty and attenuation of enhancer/inhibitor effects in mixed diets. Guidance on separating calcium and iron supplements is more specific than a rule to avoid dairy with meals. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/) |
| **Tea and coffee**                   | A dedicated evidence check is needed before encoding a universal timing interval around meals. | **Verification required:** beverage-specific effects, timing, and relevance to different risk groups.                                                                                                                                                                                                            |
| **Soaking, sprouting, fermentation** | Consider these as recipe techniques, not guaranteed fixes for iron adequacy.                   | **Verification required:** process-specific changes in phytate and demonstrated effects on iron status.                                                                                                                                                                                                          |

NIH lists US iron RDAs of **11 mg/day at 7–12 months, 7 mg/day at 1–3 years, and 27 mg/day in pregnancy**; these are US reference values, not universal international targets or supplement prescriptions. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

A recipe’s iron content cannot establish whether someone is iron deficient; diagnosis depends on clinical assessment and blood measurements interpreted in context. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

### Blood pressure

The UK guidance provides directly usable sodium-reduction techniques: select lower-salt products, limit salty sauces and cured foods, and use herbs, spices, garlic, and lemon for flavor. [nhs](https://www.nhs.uk/live-well/eat-well/food-types/salt-in-your-diet/)

**Implementation recommendations:**

- Calculate sodium from stock, sauces, cheese, bread, and other packaged ingredients—not only added salt.
- Distinguish sodium from salt in the data model and display units explicitly.
- Treat “reduced salt” as a comparison claim, not proof that a product is low in sodium.
- Do not automatically recommend potassium-containing salt substitutes.
- Require medical review before generating potassium targets for users with relevant disease or medication constraints.

**Verification required:** WHO sodium and potassium targets, the clinical effect sizes of sodium reduction, and the eligibility and safety rules for potassium-enriched salt substitutes.

### Glucose and diabetes

**Proposed recipe support:**

- Show estimated carbohydrate per actual serving, with uncertainty.
- Offer unsweetened beverage and ingredient alternatives.
- Make carbohydrate portions adjustable.
- Use legumes, vegetables, and suitable whole-grain ingredients without promising a specific glucose response.
- Preserve clinician-provided meal timing and carbohydrate instructions.
- Never change insulin or other medication advice.

The evidence for low-glycemic-index diets, carbohydrate restriction, diabetes prevention, remission, and long-term outcomes requires a dedicated verified review before assigning certainty labels. A generic “diabetes-friendly” badge would conceal important differences between people and treatments.

### Weight management

**Proposed recipe support:**

- Offer portion options without making smaller portions the default for everyone.
- Adjust energy density while preserving protein, micronutrients, flavor, and satisfaction.
- Distinguish replacing an ingredient from adding an ostensibly healthy ingredient.
- Avoid moral labels such as “clean,” “guilt-free,” and “cheat meal.”
- Do not apply adult energy-reduction goals to children, pregnancy, or frail older adults.

**Verification required:** comparative effectiveness and certainty for portion-size interventions, energy-density changes, different dietary patterns, and long-term weight outcomes.

### Gut health

A small randomized dietary study reported different microbiome and inflammatory-marker responses to high-fermented-food and high-fiber interventions; this is not proof that fermented foods prevent or treat a particular disease. [cell](<https://www.cell.com/cell/pdf/S0092-8674(21)00754-6.pdf>)

NCCIH states that probiotic benefits and safety remain uncertain for many uses, and reports serious safety concerns in some vulnerable populations, including premature infants. [nccih.nih](https://www.nccih.nih.gov/health/probiotics-usefulness-and-safety)

**Implementation recommendations:**

- Prefer concrete goals—such as increasing tolerated fiber-rich foods—over “optimize your microbiome.”
- Do not infer clinical benefit from microbial diversity alone.
- Do not recommend probiotic supplements as interchangeable with ordinary fermented foods.
- Account separately for sodium, added sugar, allergens, pasteurization, and food safety.

### Cooking methods

**Verification required:** nutrient-specific retention factors, comparative vitamin losses, effects of cooling and reheating starches, and oil stability under defined temperatures and reuse conditions.

Until that evidence is curated, the assistant should avoid rules such as “steaming always preserves all nutrients,” “cold-pressed oil must never be heated,” or “a high smoke point proves an oil is healthiest.” Nutrient retention and oil-use claims should be tied to a particular food, process, temperature, and outcome.

## 3. Life-stage requirements

### Infants and toddlers

WHO recommends complementary foods from about six months while breastfeeding continues, and emphasizes dietary diversity and responsive feeding. [who](https://www.who.int/data/nutrition/nlis/info/infant-and-young-child-feeding)

| Area                      | Verified guidance                                                                                                                                                                                                                                                                                                              | Assistant behavior                                                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dietary diversity**     | WHO recommends daily animal-source foods and fruit and vegetables; the recommendations are strong despite low-certainty evidence. Frequent pulses, nuts, and seeds receive a conditional recommendation with very-low-certainty evidence. [iris.who](https://iris.who.int/bitstream/handle/10665/373358/9789240081864-eng.pdf) | Do not mistake “strong recommendation” for “high-certainty trials.” Provide safe, culturally suitable alternatives and flag restricted diets for professional review. |
| **Iron**                  | Infants and young children are at risk of inadequate iron; US reference values differ substantially by age. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                                                                           | Register age in months and the applicable national reference system. Do not prescribe iron supplements.                                                               |
| **Salt**                  | UK guidance specifies less than 1 g salt/day under one year and no more than 2 g/day at one to three years. [nhs](https://www.nhs.uk/live-well/eat-well/food-types/salt-in-your-diet/)                                                                                                                                         | Count salt from all ingredients. Remove a child’s portion before adding adult salty condiments.                                                                       |
| **Honey**                 | NHS guidance says not to give honey under one year. [nhslanarkshire.scot.nhs](https://www.nhslanarkshire.scot.nhs.uk/patient-information-leaflets/nutrition-dietetics/pil-weanig-16-07658-l/?highlight=98.7%20the%20spot)                                                                                                      | Encode this as a non-negotiable age-based safety constraint.                                                                                                          |
| **Choking**               | CDC identifies risks from whole or unsuitable pieces of nuts, grapes, hard raw produce, meat, cheese, nut butter, and other foods; preparation and developmental readiness matter. [cdc](https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/choking-hazards.html/)                                                  | Validate shape, hardness, stickiness, size, bones, and supervision instructions—not just ingredient names.                                                            |
| **Textures**              | CDC recommends developmentally appropriate shape, size, and texture and attentive supervision while the child eats upright. [cdc](https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/choking-hazards.html/)                                                                                                         | Store feeding-development information separately from chronological age.                                                                                              |
| **Allergen introduction** | NHS guidance supports introducing potential allergens individually in small amounts from around six months and continuing tolerated foods; higher-risk situations warrant professional advice. [nhs](https://www.nhs.uk/best-start-in-life/baby/weaning/safe-weaning/food-allergies/)                                          | Never confuse “contains an allergen” with “must be excluded from every infant’s diet.” Known allergy remains a separate hard constraint.                              |

### Important national differences

WHO conditionally allows either formula or animal milk for some non-breastfed infants aged 6–11 months, based on low-certainty evidence; a multisociety response argues that this advice should be context-specific and notes that many countries advise against cow’s milk as the main drink before 12 months. [onlinelibrary.wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/jpn3.12248?msockid=16d670fd05e36e6b3c0b6705045c6f9a)

**Implementation recommendation:** Never construct infant-feeding guidance by averaging national rules. Select the relevant jurisdiction and clinical context, and distinguish a milk used as a drink from a small amount used in cooking.

Current US CDC material also differs from older widely circulated wording: its April 2026 page advises no added sugars for children younger than 11 years. This should be checked against the full current US guideline before deployment rather than silently replaced with an older “under two” rule. [cdc](https://www.cdc.gov/nutrition/features/good-nutrition-starts-early.html)

### Children

The Eatwell Guide is not intended directly for children under two; between two and five, children gradually move toward its proportions. [assets.publishing.service.gov](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/742750/Eatwell_Guide_booklet_2018v4.pdf?ContensisTextOnly=true)

**Implementation recommendations:** Preserve growth and adequate intake, use age-appropriate portions, and avoid applying adult weight-loss, low-fat, or high-fiber optimization indiscriminately. Persistent restricted intake, growth concerns, or complex exclusions should trigger professional review rather than progressively narrower recipe suggestions.

### Pregnancy and breastfeeding

Iron needs and supplementation guidance require particular care: NIH reports differing recommendations among professional organizations, including disagreement about routine screening and supplementation in asymptomatic pregnancy. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

**Verification required before production:**

- Country-specific listeria and refrigerated ready-to-eat food advice.
- Fish species, mercury categories, and portion limits.
- Raw or undercooked meat, fish, shellfish, and egg rules.
- Local exceptions involving egg-production standards or pasteurization.
- Liver and preformed vitamin A guidance.
- Caffeine, alcohol, iodine, folate, vitamin D, and supplement policies.
- Distinctions between pregnancy and breastfeeding restrictions.

The assistant should not turn an unverified international food-safety summary into a personalized “safe in pregnancy” guarantee.

### Older adults

**Verification required:** official age-specific protein recommendations, evidence for higher protein intakes in healthy versus frail adults, and exceptions involving kidney disease.

**Implementation recommendations:** Support protein-containing meals, practical preparation, suitable textures, hydration preferences, and adequate energy. Unintentional weight loss, swallowing problems, or very limited intake should override generic weight-management or “lighter meal” settings.

## 4. Allergies, intolerances, preferences

### Constraint policy

The following is a **recommended product policy**, not a substitute for an allergist’s assessment:

| Registered information                                               | Recommended treatment                                                                                                                |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Confirmed or suspected food allergy                                  | Hard ingredient-exclusion constraint; require clarification and professional guidance where diagnosis or safe exposure is uncertain. |
| Clinician-specified exclusion, including celiac-related requirements | Hard constraint according to the actual instruction.                                                                                 |
| Intolerance with a user- or clinician-defined threshold              | Respect the stated threshold; never invent a safe dose.                                                                              |
| Religious or ethical exclusion                                       | Hard constraint unless the user explicitly changes it.                                                                               |
| Ordinary dislike                                                     | Preference, unless the user marks it as non-negotiable.                                                                              |
| Budget, convenience, cuisine                                         | Optimization preferences, subordinate to safety and explicit exclusions.                                                             |

“Preference” must not mean “permission for the assistant to ignore it.” Safety constraints are never relaxed; other exclusions change only with informed user authorization.

### Allergen lists and cross-contact

**Verification gap:** The complete current EU list of 14 regulated allergens, US list of nine, exemptions, and labeling requirements were not checked against the governing official texts here. They should therefore not be represented as a validated production reference in this report.

**Implementation requirements:**

- Import and version jurisdiction-specific official lists.
- Retain the actual allergenic ingredient—not merely an “EU allergen” flag.
- Resolve compound ingredients, sauces, stocks, garnishes, and substitutions.
- Re-check every substitution.
- Ask users to verify current product labels.
- Separate ingredient exclusion from cross-contact controls.
- Never promise “allergen-free” based on a recipe alone.
- Require an explicit handling plan where shared equipment, preparation surfaces, storage, or serving utensils are relevant.

A national major-allergen list should be treated as a labeling framework, not the complete universe of foods an individual could need to avoid.

## 5. Practical cooking rules

### Translate advice into actions

**Proposed translation framework:**

| Tool                             | Suitable use                                        | Failure to prevent                                                                  |
| -------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Prefer / limit / avoid lists** | Fast ingredient filtering and shopping support      | Turning “limit” into an absolute ban or “prefer” into unlimited portions            |
| **Swap lists**                   | Replace an ingredient with a functional alternative | A substitution that meets one goal but introduces an allergen or undermines another |
| **Plate models**                 | Explain overall meal composition                    | Applying adult proportions rigidly to infants or every individual meal              |
| **Portion guides**               | Communicate serving flexibility                     | Treating a household measure as an exact nutrient quantity                          |
| **Daily or weekly targets**      | Evaluate dietary patterns over time                 | Demanding that every recipe independently satisfy every target                      |

The UK guide explicitly describes proportions across a day or week, while the Canadian plate provides a simple food-group distribution; neither should be mistaken for a laboratory nutrient analysis. [canada](https://www.canada.ca/en/health-canada/services/video/food-nutrition/plate-healthy-snacks.html)

### Personal guideline structure

The following is a **proposed schema**, not an official clinical standard:

```yaml
profile:
  person_id: adult_1
  jurisdiction: DE
  life_stage: adult
  reference_system: explicitly_selected
  reviewed_on: YYYY-MM-DD

hard_constraints:
  allergies: []
  clinician_prescribed_exclusions: []
  food_safety_rules: []
  religious_or_ethical_exclusions: []

clinical_instructions:
  supplied_by: null
  instructions: []
  assistant_may_change: false

goals:
  - goal: support_lower_LDL
    source: user_stated
    strategy: replace_some_saturated_fat_with_unsaturated_fat
    numeric_target: null

targets:
  daily: []
  weekly: []
  units_required: true

preferences:
  cuisines: []
  dislikes: []
  budget: null
  preparation_time: null

uncertainty:
  unresolved_ingredients: []
  missing_product_labels: []
  nutrient_estimate_quality: null

review:
  referral_needed: false
  reasons: []
```

Every numerical target should additionally carry its source, jurisdiction, population, unit, time horizon, and whether it was supplied by a clinician, selected from official guidance, or entered by the user.

### One meal, different needs

**Illustrative meal:** a low-salt lentil-and-vegetable sauce with grain or pasta, with person-specific finishing and portioning.

| Component          | Adult seeking lower LDL                                 | Toddler needing iron-conscious meals                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Shared base        | Legumes, vegetables, and an appropriate unsaturated oil | Same base if ingredients and texture are suitable                                                                                                                                                            |
| Portion            | Adjust to the adult’s appetite and registered goals     | Offer a developmentally suitable amount without imposing adult energy restriction                                                                                                                            |
| Iron support       | Legumes contribute non-heme iron                        | Include an iron-containing component and a suitable vitamin-C-containing accompaniment; do not claim that one meal proves adequacy. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/) |
| Texture            | Ordinary adult texture                                  | Mash, soften, or otherwise adapt to the child’s development; inspect for choking hazards. [cdc](https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/choking-hazards.html/)                         |
| Seasoning          | Add individual condiments after serving if appropriate  | Keep within the child’s applicable salt guidance. [nhs](https://www.nhs.uk/live-well/eat-well/food-types/salt-in-your-diet/)                                                                                 |
| Optional additions | Re-check against lipid goals and exclusions             | Re-check age, allergen status, texture, and nutritional role                                                                                                                                                 |

**Implementation recommendation:** Optimize the shared base first, then use portion-specific additions. Never average the household’s nutrient requirements into a fictional “family member.”

## 6. Nutrient data

### Candidate databases

These are the databases requested in the brief; **their current access conditions and commercial licensing were not verified**.

| Database                               | Required checks before integration                                                                                                 |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **USDA FoodData Central**              | Dataset type, analytical versus label-derived values, API and bulk access, attribution, redistribution terms, branded-food updates |
| **German Bundeslebensmittelschlüssel** | Current release, access route, commercial-use and redistribution rights, recipe and processing conventions                         |
| **UK CoFID**                           | Current release, download format, applicable reuse license and attribution                                                         |
| **French Ciqual**                      | Current release, export/API availability, reuse license and attribution                                                            |

“Publicly viewable” must not be treated as equivalent to “licensed for embedding, redistribution, or commercial use.” Obtain and retain the actual applicable license for each release.

### Recipe estimation model

**Proposed calculation pipeline:**

1. Identify the correct food and preparation state.
2. Convert quantities to edible weights.
3. Distinguish raw, cooked, drained, and reconstituted ingredients.
4. Account for discarded liquid, bones, peel, and other non-edible fractions where relevant.
5. Apply suitable yield and retention factors when available.
6. Record the final cooked recipe weight.
7. Allocate nutrients to the actual serving weight.
8. Preserve uncertainty and missing data.

**Verification required:** authoritative retention-factor tables and the evidence supporting any chosen uncertainty range.

The assistant should never present database arithmetic as a measurement of the actual meal. Proposed display wording:

> “Estimated nutrients per serving, based on the listed ingredients and assumed serving size. Product choice, preparation, and the amount actually eaten can change these values.”

### Data-quality rules

**Implementation recommendations:**

- Missing values remain missing; they are not zero.
- Record database, release, food identifier, and preparation state.
- Keep brand-specific fortification separate from generic-food values.
- Specify fiber definitions and nutrient units.
- Avoid adding guessed nutrient values merely to complete a table.
- Do not compute “absorbed iron” using a fixed universal percentage.
- Report sensible precision rather than decimals unsupported by the inputs.
- Distinguish recipe composition from a person’s nutritional status.

## 7. Boundaries and red flags

### Support versus treatment

**Recommended boundary:** The assistant may explain general guidance, adapt recipes to explicit instructions, and estimate recipe composition. It should not diagnose deficiency or disease, interpret laboratory results as a treatment decision, prescribe supplements, or alter medication.

Iron illustrates the distinction: NIH describes both the limitations of individual blood measurements and the clinical complexity of deficiency assessment; a calculated dietary intake is not a diagnosis. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

### Referral policy

The following is a **proposed conservative escalation policy**. It requires clinical review before implementation.

| Situation                                                                                                   | Assistant response                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Chronic kidney disease or prescribed electrolyte/fluid restrictions                                         | Request the existing care-plan instructions; do not generate independent protein, potassium, sodium, phosphorus, or fluid targets. |
| Diabetes treated with medication                                                                            | Preserve the care plan; do not recommend medication changes or abrupt therapeutic dietary changes.                                 |
| Suspected eating disorder or harmful restriction                                                            | Stop weight-loss optimization and encourage appropriate professional support.                                                      |
| Severe allergy, uncertain reaction, or proposed food challenge                                              | Do not test tolerance or invent a safe exposure level.                                                                             |
| Pregnancy complications                                                                                     | Refer dietary treatment questions to the relevant maternity clinician or dietitian.                                                |
| Suspected iron deficiency, anemia, or supplement request                                                    | Recommend clinical assessment rather than prescribing an iron dose.                                                                |
| Unintentional weight loss, poor growth, persistent vomiting, swallowing problems, or very restricted intake | Recommend timely professional assessment rather than further automatic restriction.                                                |
| Food–drug questions                                                                                         | Direct the user to a pharmacist or prescriber and preserve verified medication-specific instructions.                              |

**Emergency handling:** NHS guidance identifies breathing difficulty and swelling among possible serious allergic-reaction signs and advises immediate emergency help for suspected anaphylaxis. The app must localize the emergency number rather than universally displaying the UK number. [nhs](https://www.nhs.uk/best-start-in-life/baby/weaning/safe-weaning/food-allergies/)

### Food–drug interactions

**Implementation recommendations:**

- Store the actual medication and verified instruction, not a broad “blood thinner” category.
- Do not infer that all anticoagulants require identical food rules.
- Do not eliminate vitamin-K-containing foods automatically.
- Do not assume grapefruit affects every medicine.
- Separate food advice from instructions about supplement timing.
- Refer unresolved interaction questions to a pharmacist.

NIH specifically identifies interactions involving iron supplements and medicines including levodopa and levothyroxine, and notes that proton-pump inhibitors can reduce iron absorption. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)

### Regulatory and ethical checks

**Verification gap:** Current EU and US health-claim law, medical-device classification, privacy obligations, and the legal status of particular marketing claims were not sufficiently reviewed here. This section is therefore a compliance worklist, not legal advice.

Before launch, obtain jurisdiction-specific review of:

- Nutrition claims versus disease-risk-reduction or therapeutic claims.
- Product marketing, app-store descriptions, onboarding, and conversational output.
- Whether intended purpose and functionality create medical-device obligations.
- Handling of sensitive health information and children’s data.
- Consent, retention, deletion, security, and secondary use.
- Advertising, affiliate recommendations, and conflicts of interest.
- Accessibility, affordability, and cultural suitability.

A disclaimer should not be used to justify behavior that otherwise crosses the product’s stated boundary.

### Suggested disclaimer

**Proposed wording for legal and clinical review:**

> This assistant supports everyday meal planning and cooking. It does not diagnose conditions, prescribe treatment, or replace a doctor, registered dietitian, or pharmacist. Nutrient values are estimates. Follow your clinician’s instructions for medical conditions, medicines, supplements, pregnancy complications, and prescribed diets. Check ingredient labels and preparation conditions when allergies or other strict exclusions apply. Seek urgent medical help for a suspected emergency.

The operational behavior must match that wording: no supplement prescribing behind a “not medical advice” footer.

## 8. Popular claims to avoid

The table below is a **recommended claim-control policy**. Several examples require further claim-specific systematic-review verification before the assistant should provide detailed explanations.

| Claim pattern                                              | Safer assistant behavior                                                                                                                                                                                                                                                                              |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| “This is a superfood.”                                     | Describe the relevant nutrients or culinary role without assigning exceptional disease-preventing powers.                                                                                                                                                                                             |
| “This detoxes your body.”                                  | Do not claim toxin removal without specifying the substance, mechanism, and credible clinical evidence.                                                                                                                                                                                               |
| “This raises good cholesterol, so it protects your heart.” | Do not treat an HDL change as sufficient proof of cardiovascular benefit.                                                                                                                                                                                                                             |
| “This oil is toxic” or “this oil is always healthiest.”    | Evaluate the actual comparison, dietary substitution, quantity, and cooking conditions; avoid universal oil rankings.                                                                                                                                                                                 |
| “Plant-based means cholesterol-friendly.”                  | Check the recipe’s ingredients rather than relying on a label; the relevant advisory guidance emphasizes the replacement food and fat quality. [dietaryguidelines](https://www.dietaryguidelines.gov/sites/default/files/2024-12/Part%20D_Ch%204_Food%20Sources%20of%20Saturated%20Fat_FINAL_508.pdf) |
| “Fermented food fixes your microbiome.”                    | Explain that small studies of microbiome and inflammatory markers do not establish a universal clinical benefit. [cell](<https://www.cell.com/cell/pdf/S0092-8674(21)00754-6.pdf>)                                                                                                                    |
| “Everyone should take probiotics.”                         | Avoid blanket recommendations; benefits and safety vary, and vulnerable populations need particular care. [nccih.nih](https://www.nccih.nih.gov/health/probiotics-usefulness-and-safety)                                                                                                              |
| “Spinach solves iron deficiency.”                          | Distinguish iron content, bioavailability, total intake, and clinical diagnosis; NIH notes relatively low iron bioavailability from spinach. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                 |
| “Calcium cancels out all the iron in a meal.”              | Explain the uncertainty and mixed-diet context; do not remove calcium-rich foods indiscriminately. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                                                           |
| “Natural supplements are automatically safe.”              | Do not infer safety from origin; for example, excessive iron supplementation can cause serious harm. [ods.od.nih](https://ods.od.nih.gov/factsheets/iron-HealthProfessional/)                                                                                                                         |
| “This recipe treats diabetes/high cholesterol/anemia.”     | Describe the concrete composition or substitution and stay within the registered care plan.                                                                                                                                                                                                           |
| “One meal meets your nutritional needs.”                   | Describe contribution to intake, not guaranteed nutritional adequacy or clinical status.                                                                                                                                                                                                              |

### Production acceptance tests

These are proposed engineering checks:

- A nut substitution must fail when it conflicts with a registered nut allergy.
- An adult LDL goal must not automatically impose an energy-restricted toddler portion.
- Missing nutrient data must never become a favorable zero.
- A recipe must not receive a “safe in pregnancy” label from incomplete food-safety data.
- A new jurisdiction must trigger the correct guideline version rather than inherit another country’s rules.
- A user request to “raise HDL” must not produce an alcohol recommendation.
- A request for iron supplementation must not produce an individualized dose.
- A medical constraint must not be silently dropped to make a recipe feasible.
- Any unresolved safety conflict must produce an explanation and a safe alternative—or no recipe—rather than a best guess.
