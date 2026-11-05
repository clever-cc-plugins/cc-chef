Recipe Writing, Localization, and Adaptation: A Research-Based Report for AI Cooking Systems
Executive Summary

A modern recipe is both a culinary document and an instructional system. The strongest evidence-based practices come from three overlapping domains:

Recipe editorial practice (cookbook publishers, test kitchens, food magazines).
Measurement science and food science (especially baking).
Instructional design research (clarity, sequencing, cognitive load).

Authorities such as The Recipe Writer’s Handbook (Ostmann & Baker) and Dianne Jacob’s writings consistently emphasize three principles: accuracy, consistency, and clarity. turn1search11

A useful distinction for an AI recipe system:

Evidence-based recommendations: wighing ingredients, providing doneness cues, explicit sequencing, minimizing cognitive load.
Editorial conventions: ingredient ordering, section headings, formatting choices, house style, language register.

1. Anatomy of a Well-Written Recipe
   Core components
1. Title

Purpose:

Identifies the dish.
Sets expectations.
Improves discoverability.

Examples:

Classic French Onion Soup
30-Minute Thai Basil Chicken
Vegan Chocolate Layer Cake

Editorial convention favors specificity over creativity when clarity is important.

2. Headnote

A short introductory paragraph explaining:

Context or origin.
Flavor profile.
Difficulty.
Special techniques.
When to serve it.

Many# Recipe Architecture, Measurement, Localization, and Adaptation: A Research Report for AI Recipe Systems

Executive Summary

A high-quality recipe is both a culinary document and an instructional system. Professional recipe editors, test kitchens, and cookbook publishers generally optimize for three goals:

Accuracy (the recipe works repeatedly).
Clarity (the cook understands what to do).
Reproducibility (different cooks obtain similar results).

Across major recipe-writing authorities, including Ostmann & Baker, Dianne Jacob, test-kitchen editorial practice, and culinary publishing standards, there is broad agreement that recipes should be structured, precise, tested, and written in a way that minimizes ambiguity. Differences tend to concern style rather than substance. For example, some publishers prefer highly detailed instructional steps while others favor concise methods for experienced cooks. turn1search11

Throughout this report, recommendations are identified as either:

\*Evidence-based: supported by measurement science, instructional-design research, or testing practice.
Editorial convention: broadly adopted publishing practice rather than experimentally validated.

1. Anatomy of a Well-Written Recipe
   Core Components
1. Title

Purpose: Identify the dish and set expectations.

Good titles communicate:

Main ingredient(s)
Cooking method
Distinguishing characteristic

Examples:

Roast Chicken with Lemon and Thyme
Quick Weeknight Beef Stroganoff
Classic French Onion Soup

Editorial convention: Avoid cute or vague names unless audience context justifies them.

1.1 Headnote (Introduction)

Often called:

Headnote (US publishing)
Introduction
Recipe description

Purpose:

Explain origin or significance
Provide context
Highlight technique
Set expectations

A headnote is considered important by cookbook editors because it helps cooks decide whether to make the dish and builds trust with the author. turn1search12

Typical content:

Flavor profile
Difficulty level
Cultural background
Ingrediet notes
Make-ahead advice
1.2 Yield / Servings

Specify:

Servings
Portions
Yield by volume or quantity

Examples:

Serves 4
Makes 24 cookies
Makes 1 loaf (900 g)

Evidence-based rationale: Scaling and meal planning depend on clear yield information.

1.3 Time Information

Recommended fields:

Prep time
Cook time
Rest time
Active time
Total time

Example:

Prep: 20 min
Cook: 35 min
Rest: 10 min
Total: 65 min

Editorial disagreement: Some publishers prefer only total time because active-time estimates can vary significantly between cooks.

1.4 Equipment

Increasingly common in modern test-kitchen recipes.

Example:

28-cm skillet
Stand mixer
Digital thermometer
Baking sheet

Evidence-based benefit: Equipment affects outcomes and reproducibility.

1.5 Ingredient List

Should:

Be complete
Match method exactly
Be listed in order of use

This is one of the strongest areas of consensus among recipe editors. turn1search6

1.6 Method (Directions)

The procedural core of the recipe.

Should communicat:

Sequence
Timing
Temperatures
Doneness cues
Safety considerations
1.7 Notes

Common categories:

Make-ahead
Storage
Freezing
Variations
Ingredient substitutions

These are increasingly expected in digital recipe publishing.

1.8 Serving Suggestions

May include:

Side dishes
Garnishes
Condiments
Drink pairings

These improve user experience but are typically treated as optional editorial content.

Areas of Disagreement
Minimalist vs Detailed Writing

Some publishers favor:

Bake 25 minutes.

Others prefer:

Bake until golden brown and a thermometer inserted into the center reads 93°C/200°F, about 25 minutes.

Test kitchens generally prefer the second approach because outcomes vary by equipment and ingredients.

2. The Ingredient List
   Order of Ingredients
   Standard Convention

Ingredients appear in order of use.

Example:

2 tbsp olive oil
1 onion, finely chopped
2 cloves garlic, minced
400 g tomatoes

This is among the most widely adopted conventions in professional recipe writing. turn1search6

Component Grouping

For complex dishes:

For the sauce
For the filling
or serving

Benefits:

Reduced cognitive load
Easier mise en place
Better scaling
Ingredient Preparation Notes
Preferred
1 onion, finely chopped

Not Preferred
1 finely chopped onion

Reason:

The first instruction means:

Measure one onion.
Then chop it.

The second can imply measuring after chopping.

This distinction becomes important when ingredients are measured volumetrically.

Editorial convention with practical reproducibility benefits.

Ingredients Used Multiple Times

Best practice:

4 tbsp butter, divided

or

6 tbsp olive oil, divided

Avoid making cooks search ahead.

Optional Ingredients

Standard notation:

1 tsp red-pepper flakes (optional)

or

Optional:

- Chopped parsley

“To Taste”

Appropriate for:

Salt
Pepper
Acid adjustment

Less appropriate for:

Baking powder
Flour
Major structural ingredients

Professional recipes often provide a starting amount:

Salt, to taste (start with 1/2 tsp)

Precision

Recommended precision depends on ingredient function.

High precision:

7 g yeast

Lower precision:

1 medium onion

3. Units and Measurement
   Weight vs Volume
   Evidence

Baking organizations and recipe developers strongly recommend weight measurements for reproducibility. King Arthur Baking explicitly advises using scales and provides gram weights for recipes because flour volume measurements vary substantially depending on technique. turn1search16

One cup of flour may vary dramatically depending on packing and measuring method, intrducing significant error. turn1search16

Recommendation

For AI-generated recipes:

Use weights whenever possible.

Exaple:

300 g flour

rather than

2½ cups flour

especially in baking.

Regional Systems
United States

Common:

Cups
Tablespoons
Teaspoons
Fahrenheit

US cup:

236.6 mL (customary)
Often rounded to 240 mL turn1search21
Metric Countries

Common:

Grams
Kilograms
Milliliters
Liters
Celsis
Australia

Important difference:

Cup = 250 mL
Tablespoon = 20 mL

not 15 mL. turn1search19

This is one of the biggest localization traps.

UK

Modern recipes are mostlymetric.

Older recipes may contain:

Imperial units
Gas marks
Dual Units

Recommended format:

500 g (1 lb 2 oz) potatoes

or

240 mL (1 US cup) milk

Generate values from a tested source, not simple arithmetic conversion where precision matters.

Common Conversion Pitfalls
Flour

Cup weights differ by publisher and measuring method. turn1search18

Butter

US recipes:

1 stick butter

Requires localization.

Equivalen:

113 g butter

Eggs

One country's "large egg" does not perfectly match another's grading system.

Best practice:

2 large eggs (about 100 g out of shell)

Onions

"1 onion" is highly variable.

Prefer:

1 medium onion (about 150 g)

Can Sizes

Dangerous to convert automatically.

Example:

1 can tomatoes

may mean:

400 g
411 g
425 g
14 oz

depending on market.

Localization should identify local package equivalents.

Count-Based Ingredients

Preferred:

2 garlic cloves
1 lime
4 scallions

Optionally add weight:

1 medium avocado (about 200 g)

4. Writing the Method
   One Main Action Per Step

Evidence from instructional-design research suggests that chunking information and reducing unnecessary cognitive load improves task execution. Cognitive Load Theory emphasizes limited working-memory capacity and recommends organizing instructions into manageable units. turn1search28

Prefer:

1. Heat the oil.
2. Add the onion and cook until softened.

Insted of:

Heat oil, add onion, garlic and celery, stir often while seasoning...

Logical Sequencing

Order should mirror execution.

Bad:

Add onion.
Chop onion.

Good:

Chop onion.
Add onion.

Separate Preparation from Cooking

Helpful structure:

Preparation
Chop vegetables
Measure ingredients
Cooking
Sauté
Simmer
Bake

This reduces task-switching and cognitive burden.

Parallel Tasks

Explicitly identify overlap.

Example:

While the sauce simmers, cook the pasta.

Times Plus Sensory Cues

Best practice:

Cook 8–10 minutes, until lightly browned.

or

Bake 30–35 minutes, until the center reaches 93°C/200°F.

Time alone is insufficient because equipment varies.

Warnings at Point of Use

Example:

Add the garlic and cook for 30 seconds. Do not let it brown.

More effective than a warning buried elsewhere.

5. Heat and Equipment
   Oven Temperatures
   Conventional vs Fan/Convection

General rule:

Fan oven ≈ conventional oven − 20°C

or

−25°F

Editorial convention accepted across many publishers.

Recommended Format
180°C conventional
160°C fan
350°F
Gas Mark 4

for international audiences.

Stovetop Heat

Avoid:

Cook over medium heat.

alone.

Prefer:

Cook over medium heat until the onions soften and begin turning translucent, 6–8 minutes.

Pan Sizes

Pan size changes:

Evaporation
Browning
Depth
Cooking time

Specify:

30-cm / 12-inch skillet

Equipment-Tolerant Writing

Instead of:

Use a cast-iron skillet.

Prefer:

Use a heavy skillet, preferably cast iron.

unless outcome truly depends on the equipment.

6. Scaling
   Ingredients That Scale Well

Generally linear:

Meat
Vegetables
Stocks
Sauces (before reduction)
Ingredients That Often Do Not Scale Linearly
Salt

Perception changes with batch size.

Large batches often require slightly less than perfect linear scaling.

Spices

Flavor extraction changes with cooking geometry and time.

Leavening

Baking powder and baking soda often need adjustment after major scaling.

Large increases can create:

Over-expansion
Collapse
Off flavors
Thickened Sauces

Surface area affects evaporation.

Linear scaling often fails.

Cooking Time

Doubling quantity rarely doubles time.

Heat-transfer physics dominates.

Examples:

Soup volume ↑ modest time increase.
Roast weight ↑ significant time increase.
Pan Geometry

Cake recipes often require recalculation based on pan area and depth.

7. Language and Locale
   Instruction Style
   English

Usually imperative:

Heat the oil.
Add the onion.

German

Often imperative plural/formal:

Erhitzen Sie das Öl.

or cookbook style:

Öl erhitzen.

French

Often infinitive:

Faire chauffer l'huile.
Ajouter l'oignon.

Spanish

Often imperative:

Calienta el aceite.
Añade la cebolla.

Section Headings
English
Ingredients
Method
Notes
German
Zutaten
Zubereitung
Hinweise
French
Ingrédients
Préparation
Conseils
Ingredient Mapping Problems

Many products lack exact equivalents.

Examples:

Source ProblemUS sour cream Not identical to many European products
US half-and-half No direct equivalent in many countries
UK double cream No exact US equivalent
French crème fraîche Varies globally
Quark Unknown in many English-speaking markets

Localization requires ingredient substitution logic, not translation alone.

Package and Produce Size Differences

Examples:

Butter sold as sticks in US.
Butter sold in 250 g blocks in much of Europe.
Onion size assumptions differ.
Coconut milk can sizes differ.
Translation Pitfalls

Never translate literally when food systems differ.

Example:

1 stick butter

should become:

113 g butter

not:

1 Butterstick

8. Restructuring Existing Recipes
   Changes Typically Safe
   Structure

Convert:

Ingredients + Directions

to

Equipment
Ingredients
Preparation
Cooking
Notes

Safe if meaning is preserved.

Wording

Clarifying instructions while retaining content is standard editorial practice.

Unit Conversion

Generally safe, but:

Round wisely.
Avoid false precision.

Example:

1 cup milk

→

240 mL milk

Changes Requiring Testing or Caution
Scaling

May alter:

Timing
Texture
Leavening
Ingredient Substitution

Generally requires validation.

Example:

buttermilk → yogurt

may affect hydration and acidity.

Large Quantity Conversions

Volume-to-weight conversions depend on ingredient density.

Copyright and Ethics
Important Legal Principle

In many jurisdictions:

Ingredient lists are generally considered factual information.
Functional procedures are often not copyrightable as such.
Expressive language surrounding them may be copyrighted.

Therefore:

Usually Safe
Rewriting
Reformatting
Converting units
Changing structure
Requires Care
Copying expressive prose
Reproducing headnotes verbatim
Republishing substantial text
Attribution Norms

Common editorial practice:

Adapted from Jane Doe's Classic Baking

or

Inspired by...

used when significant borrowing occurs.

9. Readability and Accessibility
   Beginner-Friendly Recipes

Require:

Defined terminology
Extra explanation
Equipment notes
Visual/sensory cues

Example:

Cook until translucent, meaning soft and slightly see-through.

Expert-Friendly Recipes

Prefer:

Concision
Minimal redundancy
Faster scanning
Layered Information Strategy

Best solution for AI systems:

Core Recipe

Short instructions.

Optional Expansions
Technique notes
Ingredient background
Troubleshooting

This serves both audiences.

Accessibility Recommendations

Use:

Numbered steps
Consistent units
High-contrast formatting
Clear headings
Short paragraphs

Avoid:

Long narrative blocks
Mixed measurement systems without labeling
Ambiguous pronouns ("it", "them") when multiple ingredients exist

Evidence from instructional-design research suggests that clear sequencing, chunking, and reduction of extraneous information decreases cognitive burden and improves task execution. turn1search25

Practical Recommendations for an AI Recipe Assistant

A robust international reipe model should store recipes internally as structured data:

title:
yield:
prep_time:
cook_time:
equipment:
ingredients:

- amount:
  unit:
  ingredient:
  preparation:
  method:
  notes:
  serving_suggestions:
  locale:
  measurement_system:

Then generate locale-specific outputs by:

Translating language and grammar.
Converting units.
Replacing culturally specific package references.
Adjusting section structure.
Preserving ingredient-function relationships.
Flagging conversions that require re-testing.

For baking recipes, store canonical ingredient weights whenever possible and treat volume measures as derived display values.

References (APA Style)

Baker, J. L., & Ostmann, B. G. (2002). The Recipe Writer's Handbook (Rev. ed.). John Wiley & Sons. turn1search6

Chandler, P., & Sweller, J. (1991). Cognitive load theory and the format of instruction Cognition and Instruction, 8(4), 293-332.

Jacob, D. (2015). Will Write for Food: The Complete Guide to Writing Cookbooks, Blogs, Memoir, Recipes, and More. Grand Central Publishing. citeturn1search11turn1search8

King Arthur Baking. (2015). Weighing ingredients: Your measure of success.

King Arthur Baking. (2023). How to measure flour the right way.

King Arthur Baking. (n.d.). Recipe Success Guide.

National Institute of Standards and Technology (NIST). (2026). Metric Kitchen: Cooking Measurement Equivalencies.

Sweller, J., Roussel, S., & Tricot, A. (2022). Cognitive Load Theory and Instructional Design for Language Learning. In The Cambridge Handbook of Working Memory and Language. Cambridge University Press.

Penn State University. (n.d.). Instructional Designer's Handbook: Cognitive Load.

NIST. (2026). Metric Kitchen.
