# Research Prompt: recipe writing

**For:** every skill that outputs a recipe, and the skill that restructures recipes found in magazines or online to match the user's preferences.
**Why research helps:** a recipe is a set of instructions that has to work in someone else's kitchen. Structure, units, precision, and conventions vary by language and country, and the plugin must work in any language. This research gives the skills a well-founded default structure and the knowledge to adapt it to each user's configured preferences (language, units, sections, level of detail).

Paste the prompt below into a deep-research AI tool. Save the response as `docs/research/recipe-writing.md`.

---

```text
─────────────────────────────────────────────
Research prompt: how to write recipes that work
─────────────────────────────────────────────
You are a research analyst with expertise in recipe development, culinary publishing, and technical/instructional writing. I am building an AI cooking assistant that writes recipes for home cooks in many languages and countries, and that can also restructure existing recipes (from cookbooks, magazines, or websites) to match a user's preferred format — e.g. their language, unit system, and section structure (such as separating "preparation" from "cooking").

Provide a comprehensive, well-structured report using headers to separate these areas:

1. ANATOMY OF A WELL-WRITTEN RECIPE
   The elements of a recipe and their purpose: title, headnote, yield/servings, active and total time, equipment, ingredient list, method, notes (make-ahead, storage, variations), and serving suggestions (side dishes, drinks). Draw on established recipe-writing guides (e.g. "The Recipe Writer's Handbook" by Ostmann & Baker, Dianne Jacob's "Will Write for Food"), publisher and test-kitchen style guides, and editorial practice. Note where experts disagree.

2. THE INGREDIENT LIST
   Conventions for order (order of use), grouping by component (e.g. "for the sauce"), precision, and prep notes (e.g. "1 onion, finely chopped" vs. "1 finely chopped onion" — and why the difference matters). Cover how to handle "to taste", optional ingredients, and ingredients used in several steps.

3. UNITS AND MEASUREMENT
   Weight vs. volume: evidence on accuracy and reproducibility (especially in baking). Regional conventions (metric, US customary, UK, Australia — including differing cup and tablespoon sizes), conventions for presenting dual units, and common conversion pitfalls (e.g. flour and butter by volume, "a stick of butter", size of an egg or an onion, can sizes). Cover how to express quantities for items usually counted rather than weighed.

4. WRITING THE METHOD
   Best practices for instructional steps: one main action per step, sequencing, separating preparation (mise en place) from cooking, parallel tasks and timing, sensory doneness cues alongside times and temperatures, and warnings at the point they matter. Include findings from research on procedural instructions and cognitive load where applicable.

5. HEAT AND EQUIPMENT
   Oven conventions (conventional vs. fan/convection and conversion rules, gas marks, Fahrenheit vs. Celsius), describing stovetop heat levels, pan sizes and how they affect results, and how to write recipes that tolerate equipment differences.

6. SCALING
   What scales linearly and what does not when changing the number of servings (e.g. salt, spices, leavening, liquids in reductions, cooking times, pan size, baking times), with the reasons.

7. LANGUAGE AND LOCALE
   How recipe conventions differ between languages and countries — e.g. grammatical mood of instructions (imperative vs. infinitive, as in German and French recipes), typical section headings, ingredient naming differences (e.g. dairy products that don't map one-to-one across countries, British vs. US terms), typical produce sizes and package sizes, and pitfalls when translating or localizing recipes.

8. RESTRUCTURING EXISTING RECIPES
   How editors adapt recipes from another source to a house style: what can be changed freely (structure, wording, units), what requires re-testing or care (quantities after unit conversion, substitutions, scaling), and the ethics and copyright norms of adapting recipes (ingredient lists vs. expressive text, attribution practices such as "adapted from").

9. READABILITY AND ACCESSIBILITY
   What makes recipes easy to follow for beginners vs. experienced cooks, and how to serve both (e.g. optional detail, technique notes).

Requirements:
- Use credible, verifiable sources throughout, with in-text citations: recipe-writing handbooks, publisher and test-kitchen style guides, measurement standards bodies, and research on instructional design. Avoid generic food-blog content.
- Be explicit about which recommendations are evidence-based and which are editorial convention.
- Give examples from several languages and countries.
- Provide a formatted source list in APA style at the end.
- Respond in Markdown.
─────────────────────────────────────────────
```
