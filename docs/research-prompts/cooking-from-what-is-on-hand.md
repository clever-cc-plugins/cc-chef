# Research Prompt: cooking from what is on hand

**For:** skills that suggest dishes from an ingredient list, a description, or a photo of the fridge, and skills that adapt recipes through substitutions.
**Why research helps:** the most common trigger for the plugin is "this is in the fridge and needs to be used". Good suggestions need flexible dish templates, a sense of which ingredients are urgent, sensible pantry assumptions, and substitutions that account for how a swap changes the technique. The research also covers how reliably current AI can recognize ingredients from photos.

Paste the prompt below into a deep-research AI tool. Save the response as `docs/research/cooking-from-what-is-on-hand.md`.

---

```text
─────────────────────────────────────────────
Research prompt: cooking from what is on hand
─────────────────────────────────────────────
You are a research analyst with expertise in culinary practice, food science, and consumer food behavior. I am building an AI cooking assistant used internationally by home cooks. A typical request is: "Here is what's in my fridge and needs to be used — what can I cook?" The input may be a typed ingredient list, a short description of what the person feels like eating, or a photo of their fridge or pantry. The assistant should suggest a few quick, approachable dishes that use as many of the given ingredients as possible and require as few additional purchases as possible, and later produce a full recipe for the one the person picks.

Provide a comprehensive, well-structured report using headers to separate these areas:

1. FLEXIBLE DISH TEMPLATES
   How experienced cooks build a meal from whatever is available. Cover "template" dishes that absorb many ingredients (e.g. frittata/omelette, stir-fry, fried rice, soup, stew, curry, gratin, pasta, grain bowl, savory pancake, hash, pie or tart, salad), and published approaches to improvisational cooking (e.g. ratio-based cooking, "pantry cooking", cooking with leftovers). For each template: what it needs structurally, which ingredient categories it accepts, and what it needs to taste good rather than like a random mix.

2. PRIORITIZING INGREDIENTS
   How to decide which ingredients should be used first (perishability, typical shelf life once opened, visible signs of age) and how to center a dish around them. Include research on household food waste and which interventions actually reduce it.

3. PANTRY ASSUMPTIONS
   What a typical household can be assumed to have (salt, oil, basic spices, etc.), how this differs between countries and cuisines, and how a cooking assistant should handle uncertainty about staples — ask, assume, or offer alternatives.

4. SUBSTITUTIONS AND THEIR CONSEQUENCES
   A systematic view of substitutions based on an ingredient's function in a dish (structure, moisture, fat, leavening, binding, emulsification, acidity, sweetness, flavor). Cover common categories: fats, dairy and plant-based dairy, eggs, flours (including whole-grain vs. refined — e.g. different liquid absorption), sweeteners, acids, proteins, alliums, fresh vs. dried herbs and spices. For each, describe how a swap changes technique, liquid ratios, cooking time, texture, or taste, and which swaps reliably fail.

5. DIETARY ADAPTATIONS
   What works and what breaks when adapting dishes to be vegetarian, vegan, gluten-free, lactose-free, lower in saturated fat, lower in sugar, or lower in salt — with the food-science reasons. Include allergen cross-contact basics where relevant.

6. FOOD SAFETY FOR LEFTOVERS
   Safe storage times, reheating rules, and high-risk items (e.g. cooked rice, poultry, seafood, cooked greens) according to official food-safety authorities (e.g. USDA FSIS, UK Food Standards Agency, German BfR, EFSA). Note where authorities differ.

7. INGREDIENT RECOGNITION FROM PHOTOS
   How reliably current multimodal AI models identify food items, their quantities, and their condition in photos of fridges and pantries. Cover published benchmarks and studies, typical failure modes (occlusion, packaged goods, look-alike items, lighting, estimating quantity or freshness), and best practices for confirming the recognized items with the user before cooking.

8. PRESENTING OPTIONS
   How many recipe ideas to offer at once and how to describe them so the person can choose quickly — research on choice overload and decision fatigue in food choices, and practices from meal-kit services or cooking apps.

Requirements:
- Use credible, verifiable sources throughout, with in-text citations: peer-reviewed food science and consumer research, official food-safety authorities, culinary textbooks, and well-established cookbook authors and test kitchens. Avoid generic food-blog content.
- Be explicit about which recommendations are backed by empirical research and which are practitioner experience.
- Use examples from multiple culinary traditions, not only one.
- Provide a formatted source list in APA style at the end.
- Respond in Markdown.
─────────────────────────────────────────────
```
