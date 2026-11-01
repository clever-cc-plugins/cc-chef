# Research Prompt: nutrition and personal guidelines

**For:** the opt-in dietary-guidelines support — helping users who want it to create their own guidelines, and applying registered guidelines (e.g. a food list with cholesterol, iron, and fiber values) when creating or adapting recipes.
**Why research helps:** this is the area where mistakes matter most. The plugin supports healthier eating but does not replace medical or dietetic advice. The skills need evidence-graded knowledge of dietary patterns and cooking-relevant levers, hard constraints (allergies, life-stage rules), and a clear line where they must defer to a doctor or registered dietitian.

Best run in tools with access to scientific databases (e.g. Consensus, Elicit, Scite, or a general tool with academic search), plus at least one general deep-research tool. Save the responses as `docs/research/nutrition-and-personal-guidelines.md` (or one file per tool, see the README).

---

```text
─────────────────────────────────────────────
Research prompt: evidence-based nutrition for a home-cooking assistant
─────────────────────────────────────────────
You are a research analyst with expertise in nutrition science, public-health dietetics, and food science. I am building an AI cooking assistant used internationally by home cooks. Users can optionally register personal dietary guidelines (e.g. "lower LDL cholesterol and increase fiber for one adult; sufficient iron for a toddler") and the assistant then creates and adapts recipes accordingly. Users without guidelines can ask the assistant to help them draft some. The assistant supports healthier everyday eating; it does NOT diagnose, treat, or replace advice from a doctor or registered dietitian, and it must know where that line is.

Provide a comprehensive, well-structured report using headers to separate these areas:

1. EVIDENCE-BASED DIETARY PATTERNS
   Mediterranean diet, DASH, the Portfolio diet, the Nordic diet, the EAT-Lancet planetary health diet, and national food-based dietary guidelines (e.g. German DGE, UK Eatwell Guide, US Dietary Guidelines, Health Canada's Food Guide). For each: core principles, the health outcomes it is evidenced for, and the strength of that evidence. Summarize what they have in common.

2. COOKING-RELEVANT LEVERS FOR COMMON HEALTH GOALS
   For each goal, the dietary levers a home cook can actually pull (ingredient choices, swaps, cooking methods, portioning) and the certainty of evidence for each: blood lipids (LDL lowering — e.g. saturated vs. unsaturated fat, soluble fiber, plant sterols, nuts, legumes, soy; and what the evidence says about raising HDL through diet), fiber intake, iron (heme vs. non-heme, bioavailability enhancers such as vitamin C, inhibitors such as tea, coffee, calcium, phytates), blood pressure and sodium/potassium, blood glucose and type 2 diabetes, weight management, and gut health. Note how cooking methods affect these (e.g. nutrient losses, oil choice for heating).

3. LIFE-STAGE REQUIREMENTS
   Official guidance relevant to cooking for infants and toddlers (iron, salt, added sugar, honey under 12 months, choking hazards, textures), children, pregnancy and breastfeeding (e.g. listeria, mercury in fish, raw or undercooked foods), and older adults (e.g. protein). Note where national authorities differ.

4. ALLERGIES, INTOLERANCES, AND PREFERENCES
   The regulated major allergens (EU list of 14, US list of 9) and cross-contact basics; the difference between allergy, intolerance, and preference; and which of these a cooking assistant must treat as hard constraints that are never relaxed.

5. FROM GOALS TO PRACTICAL COOKING RULES
   How dietitians translate guidelines into practical tools: food lists ("prefer / limit / avoid"), swap lists, plate models, portion guides. How to structure a personal guideline document so it is usable for cooking — e.g. separating hard constraints, targets, and preferences — and how to cook one meal for several people with different needs (e.g. an adult with high LDL and a toddler who needs iron).

6. NUTRIENT DATA
   Reliable food composition databases (e.g. USDA FoodData Central, the German Bundeslebensmittelschlüssel, UK CoFID, French Ciqual), their accessibility and licensing, and the accuracy limits of estimating nutrient content of a home-cooked recipe (natural variability, cooking losses, retention factors, portion size).

7. BOUNDARIES AND RED FLAGS
   Where general healthy-eating support ends and individual medical nutrition therapy begins — e.g. chronic kidney disease, diagnosed diabetes on medication, eating disorders, food–drug interactions (e.g. vitamin K and anticoagulants, grapefruit), severe allergies, pregnancy complications. Which signals should prompt a referral to a doctor or registered dietitian. Regulatory and ethical considerations for consumer nutrition tools (e.g. health-claim regulations in the EU and US) and what an appropriate disclaimer covers.

8. POPULAR CLAIMS TO AVOID
   Widely circulated nutrition claims that the evidence does not support or that are overstated (e.g. "superfoods", "detox", specific claims about individual oils or supplements) — so the assistant does not repeat them.

Requirements:
- Prioritize systematic reviews, meta-analyses, randomized controlled trials, and official guidelines from health authorities and professional bodies (e.g. WHO, EFSA, national nutrition societies, dietetic associations). Use in-text citations throughout.
- State the certainty of evidence for each recommendation (e.g. using GRADE levels or the source's own grading) and flag where evidence is mixed or guidelines conflict.
- Keep the scope international; note country-specific differences.
- Provide a formatted source list in APA style at the end.
- Respond in Markdown.
─────────────────────────────────────────────
```
