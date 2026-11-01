Research Report: Designing an AI Cooking Assistant for “What Can I Cook With What I Have?”
Executive Summary

The most useful cooking assistants behave less like recipe search engines and more like experienced home cooks. Rather than matching ingredients to fixed recipes, they identify high-priority ingredients, map them into flexible dish templates, account for perishability and food safety, infer likely pantry staples, and present a small number of attractive options. This approach aligns with both culinary practice and consumer-behavior research on reducing food waste and decision fatigue. Empirical evidence strongly supports meal planning, inventory awareness, leftover use, and simplified decision-making as effective interventions for reducing household food waste.

1. FLEXIBLE DISH TEMPLATES
   Why Template Cooking Works

Professional and experienced home cooks often think in terms of structures rather than recipes. Improvisational cooking relies on understanding the functional roles of ingredients and the core architecture of dishes.

Ratio-based cooking, popularized by Michael Ruhlman, emphasizes that many dishes are built from stable ingredient relationships rather than exact recipes. Once cooks understand a template, they can generate many variations from available ingredients.

The assistant should classify ingredients into functional categories:

Aromatics (onion, garlic, ginger, celery)
Protein (eggs, meat, fish, tofu, legumes)
Vegetables
Starches/grains
Fat sources
Acids
Herbs/spices
Umami contributors
Garnishes/textural elements
Omelette / Frittata
Structural requirements
Eggs (or egg substitute)
Fat for cooking
Accepts
Almost any cooked vegetable
Cheese
Herbs
Leftover meat
Cooked potatoes
Legumes
What makes it good

Not ingredient quantity but balance:

Moderate moisture
Salt
Browning
Contrast between soft interior and flavorful fillings
Common cuisines
French omelette
Italian frittata
Spanish tortilla
Assistant value

One of the best high-food-waste-reduction formats because it can absorb small leftover quantities.

Stir-Fry
Structural requirements
High-heat cooking fat
Vegetables
Flavoring sauce
Accepts
Meat
Seafood
Tofu
Mushrooms
Noodles or rice
What makes it good
Similar cooking times
Strong seasoning
Moisture control
Browning (Maillard reactions)
Failure mode

Overcrowding causes steaming instead of browning.

Fried Rice
Structural requirements
Cooked chilled rice
Accepts
Eggs
Vegetables
Leftover proteins
Kimchi
Scallions
What makes it good
Dry rice
High heat
Salt + umami
Aromatics
Notable safety issue

Cooked rice requires special handling due to Bacillus cereus risk. UK FSA guidance is significantly stricter than many household practices.

Soup
Structural requirements
Liquid
Flavor base
Accepts

Nearly everything:

Vegetables
Beans
Meat
Grains
Dairy
What makes it good
Layered seasoning
Aromatic foundation
Proper body
Culinary parallels
Minestrone
Vegetable soup
Miso soup
Harira
Borscht
Stew / Braise
Structural requirements
Cooking liquid
Long cooking
Accepts
Tough meats
Legumes
Root vegetables
What makes it good

Time-dependent flavor development and collagen conversion.

Curry
Structural requirements
Aromatics
Fat
Spice base
Accepts

Almost any protein and vegetable.

What makes it good

Balanced:

Fat
Acidity
Spice
Salt
Aromatic complexity

Examples:

Thai green curry
Indian sabzi
Japanese curry
Pasta
Structural requirements
Pasta
Sauce vehicle
Accepts

Most vegetables and proteins.

What makes it good
Proper starch-water use
Acidity
Salt
Fat emulsification
Grain Bowl
Structural requirements
Base grain
Protein
Vegetables
Dressing
Accepts

Nearly unlimited combinations.

What makes it good

Attention to:

Texture contrast
Temperature contrast
Acidity

Examples:

Bibimbap
Buddha bowl
Poke-inspired bowls
Gratin / Casserole
Structural requirements
Main ingredient
Binder/sauce
Baking
Accepts
Potatoes
Vegetables
Leftover meat
Pasta
What makes it good
Browning
Fat
Moisture balance
Hash
Structural requirements
Chopped ingredients
High-heat cooking
Accepts
Potatoes
Meat
Vegetables
What makes it good

Crisp surfaces and concentrated flavors.

Savory Pancakes

Examples:

Okonomiyaki
Korean jeon
Vegetable fritters
Structural requirements
Batter
Mix-ins
Accepts

Small leftover quantities particularly well.

Salads
Structural requirements
Main vegetable component
Dressing
What makes it good

Research and culinary practice consistently show acidity and texture contrast are more important than ingredient count.

Pie / Tart / Galette
Structural requirements
Crust or topping
Filling
Accepts

Vegetables, cheese, meat, fruit.

Good assistant use case

When users possess many small leftovers.

Practical Recommendation

For fridge-cleanout scenarios, prioritize:

Frittata
Fried rice
Stir-fry
Soup
Grain bowl

These absorb the broadest ingredient variety with minimal additional purchases.

2. PRIORITIZING INGREDIENTS
   A Practical Priority Hierarchy
   Use Immediately (1-2 days)
   Fresh herbs
   Salad greens
   Berries
   Seafood
   Mushrooms
   Cut fruit
   Use Soon (2-5 days)
   Opened dairy
   Ground meat
   Tofu
   Soft cheeses
   Moderate Priority (up to 2 weeks)
   Bell peppers
   Cucumbers
   Zucchini
   Cooked leftovers
   Lower Priority
   Root vegetables
   Hard cheeses
   Dry goods
   Visible Signs of Aging
   Vegetables
   Wilting
   Shriveling
   Sliminess
   Fruit
   Soft spots
   Fermentation odors
   Dairy
   Separation
   Mold (except intended mold cheeses)
   Proteins
   Off odors
   Surface slime
   Discoloration

Note: smell is not a reliable food-safety test for many pathogens. Authorities caution against relying solely on smell or appearance.

Household Food Waste Research

Households generate more than half of food waste in the EU. Major causes include over-purchasing, poor planning, storage mistakes, and forgotten leftovers.

Interventions supported by research

Most effective:

Meal planning
Inventory tracking
Shopping lists
Leftover planning
Portion planning
Date-label education

EU evaluations of dozens of interventions found multi-component behavioral programs outperform awareness-only campaigns.

Implication for AI assistant

The assistant should:

Identify high-risk perishables.
Explicitly explain why they are prioritized.
Suggest dishes maximizing their use. 3. PANTRY ASSUMPTIONS
Reasonable Global Defaults

Safe assumptions:

Salt
Pepper
Cooking oil
Garlic or garlic powder
Onion
Sugar
Vinegar or lemon juice

Less safe assumptions:

Soy sauce
Fish sauce
Curry paste
Dijon mustard
Tahini
Regional Variation
North America

Common:

Vegetable oil
Flour
Canned tomatoes
Western Europe

Common:

Olive oil
Mustard
Vinegar
East Asia

Common:

Soy sauce
Rice
Sesame oil
South Asia

Common:

Turmeric
Cumin
Coriander
Latin America

Common:

Beans
Rice
Dried chilies
Assistant Strategy

Best practice:

Tier 1

Assume universal staples:

Salt
Oil
Water
Tier 2

Soft assumptions: "Assuming you have soy sauce or another savory seasoning."

Tier 3

Offer alternatives: "If you don't have soy sauce, use salt plus a splash of vinegar."

This reduces friction without creating recipe failures.

4. SUBSTITUTIONS AND THEIR CONSEQUENCES

The key principle is that ingredients perform functions, not merely provide flavor.

Eggs

Functions:

Binding
Structure
Emulsification
Leavening

Substitutions:

Replace ResultFlax egg More dense
Chia egg More gel-like
Aquafaba Good foaming
Silken tofu Dense structure

Failures:

Replacing eggs 1:1 with liquid in cakes typically collapses structure.
Fats

Functions:

Tenderizing
Flavor
Mouthfeel

Butter → oil:

Less water
Different flavor
Different browning

Olive oil → coconut oil:

More saturated fat
Different aroma
Dairy

Milk alternatives vary enormously:

Substitute Protein Typical effectSoy High Closest performance
Oat Low Sweeter
Almond Very low Thin texture

Protein-rich dairy substitutes behave more predictably in cooking.

Flour

Whole grain flour absorbs more water because bran and fiber bind moisture.

Implications:

Often needs extra liquid.
Produces denser products.
Longer hydration helps.
Sweeteners

Honey:

Adds moisture
More browning

Maple syrup:

Distinct flavor

Sugar alcohols:

Alter texture
Reduced browning
Acids

Lemon, lime, vinegar, yogurt, tamarind all provide acidity but different flavors.

Substitution usually succeeds in savory dishes if acidity level is adjusted.

Alliums
Original SubstituteOnion Shallot
Shallot Onion
Garlic Garlic powder

Failures: Raw onion cannot fully replace garlic flavor character.

Herbs

Rule of thumb:

1 part dried ≈ 3 parts fresh

Exceptions:

Basil
Cilantro
Parsley

Fresh versions provide volatile aromas difficult to replicate.

Proteins

Meat ↔ beans:

Usually works in soups and stews.
Less effective in dishes relying on meat texture.

Tofu works best when replacing neutral proteins rather than heavily marbled meats.

5. DIETARY ADAPTATIONS
   Vegetarian

Usually straightforward:

Replace meat with legumes, mushrooms, tofu.

Main challenge: Maintaining umami.

Useful ingredients:

Mushrooms
Soy sauce
Miso
Tomato paste
Vegan

Most difficult substitutions:

Eggs
Cheese

Food-science reason: These contribute structural proteins, emulsification, and fat simultaneously.

Gluten-Free

Challenges: Gluten provides elasticity and gas retention.

Consequences:

Crumblier texture
Reduced rise
Different hydration

Successful recipes usually require reformulation, not simple flour swaps.

Lactose-Free

Usually easy.

Lactose-free dairy products perform nearly identically in cooking because proteins and fats remain largely unchanged.

Lower Saturated Fat

Replace:

Butter
Cream
Fatty meat

With:

Olive oil
Legumes
Yogurt

Main tradeoff: Less richness and mouthfeel.

Lower Sugar

Sugar contributes:

Sweetness
Moisture retention
Browning
Structure

Reducing sugar alters more than sweetness.

Lower Sodium

Challenges: Salt affects flavor perception and bitterness suppression.

Common compensations:

Acidity
Herbs
Spices
Umami ingredients
Allergen Cross-Contact Basics

Important assistant reminders:

Separate utensils and boards.
Check packaged ingredients.
Avoid assuming absence of allergens from appearance alone.
Severe allergy users should be directed to manufacturer labeling. 6. FOOD SAFETY FOR LEFTOVERS
Consensus Rules
Refrigeration

USDA:

Refrigerate within 2 hours
Within 1 hour if ambient temperature exceeds 32°C (90°F).
Refrigerator Storage

USDA:

Most leftovers: 3–4 days.
Reheating

USDA guidance:

Reheat thoroughly to 74°C / 165°F.

UK guidance similarly emphasizes reheating until piping hot throughout and generally reheating only once.

High-Risk Foods
Cooked Rice

Particular concern: Bacillus cereus.

UK FSA:

Cool quickly.
Refrigerate promptly.
Consume within 24 hours.
Reheat only once.

This is stricter than common U.S. household practice.

Poultry

High risk due to common pathogen contamination.

Generally:

Refrigerated leftovers 3–4 days.
Seafood

Higher spoilage rates and should receive elevated assistant priority.

Cooked Leafy Greens

Not uniquely hazardous when handled correctly but deteriorate rapidly and should be prioritized for consumption.

Assistant Recommendation

When cooking from leftovers:

Ask when items were cooked.
Flag rice, seafood, poultry.
Prefer disposal over uncertain safety. 7. INGREDIENT RECOGNITION FROM PHOTOS
Current Capability

Modern multimodal systems are surprisingly effective at:

Identifying common produce
Recognizing packaged foods
Recognizing meal components

Food-recognition research commonly uses benchmarks such as Food-101, containing over 100,000 images across 101 food categories.

What AI Does Well

Generally reliable:

Apples vs oranges
Broccoli vs cauliflower
Eggs
Milk cartons
Bottled condiments
Common Failure Modes
Occlusion

Items hidden behind others.

Packaging

Cannot see contents.

Similar-looking foods

Examples:

Parsley vs cilantro
Greek yogurt vs sour cream
Green onions vs leeks
Lighting

Fridge lighting creates color distortions.

Quantity Estimation

Very difficult from a single image.

Freshness Estimation

Particularly unreliable.

A photo may reveal mold or severe wilting but not microbial safety. Freshness, spoilage, and remaining shelf life are substantially harder tasks than simple classification. Ingredient recognition studies emphasize dataset bias, visual variability, and category ambiguity as major challenges.

Best-Practice Workflow

The assistant should never immediately generate recipes from image recognition alone.

Recommended pattern:

Analyze image.
Produce inventory:
"I think I see..."
Ask for confirmation.
Allow corrections.
Generate dishes.

This substantially reduces downstream errors.

8. PRESENTING OPTIONS
   Choice Overload Research

The classic Iyengar & Lepper "jam study" found that larger assortments attracted attention but reduced purchasing behavior relative to smaller assortments. Subsequent work suggests excessive choice can increase cognitive burden and decision deferral.

For meal selection, this argues against presenting dozens of recipe ideas.

Recommended Number of Suggestions
Ideal

3-5 options.

Why

Enough variety:

Different cuisines
Different effort levels

Without forcing extensive comparison.

Supported primarily by consumer decision research and practitioner UX experience.

Recommended Presentation Format

Instead of:

Here are 12 recipes.

Use:

Option 1: Vegetable Frittata

Uses: eggs, spinach, mushrooms, cheese
Additional purchases: none
Time: 20 min

Option 2: Fried Rice

Uses: rice, carrots, peas, chicken
Additional purchases: soy sauce optional
Time: 15 min

Option 3: Coconut Vegetable Curry

Uses: zucchini, carrots, chickpeas
Additional purchases: coconut milk
Time: 30 min

Ranking Heuristic

Score dishes using:

Ingredients used (%)
High-priority perishables used
Additional purchases required
Cooking time
Dietary fit
User preference

Suggested weighting:

40% perishables used
25% ingredient utilization
15% purchase minimization
10% preparation time
10% preference match
Key Design Recommendation

A high-performing AI cooking assistant should operate in this sequence:

Inventory recognition (photo or text).
Perishability ranking.
Food-safety screening.
Mapping to flexible dish templates.
Generate 3-5 options only.
Show ingredient utilization and required purchases.
Generate a full recipe only after selection.

This design is supported by culinary practice, food-science principles, food-waste research, and consumer decision-making evidence.

References (APA)

Bossard, L., Guillaumin, M., & Van Gool, L. (2014). Food-101: Mining discriminative components with random forests. European Conference on Computer Vision.

European Food Safety Authority (EFSA). (2024). Reducing consumer food waste. https://www.efsa.europa.eu

Food Standards Agency. (2026). Home food fact checker. UK Government. https://www.food.gov.uk

Food Standards Australia New Zealand. (2025). Cooling and reheating food. https://www.foodstandards.gov.au

Iyengar, S. S., & Lepper, M. R. (2000). When choice is demotivating: Can one desire too much of a good thing? Journal of Personality and Social Psychology, 79(6), 995-1006.

Louro, J., Fidalgo, F., & Oliveira, Â. (2024). Recognition of food ingredients: Dataset analysis. Applied Sciences, 14(13), 5448.

Ruhlman, M. (2009). Ratio: The simple codes behind the craft of everyday cooking. Scribner.

Swannell, R., Bruns, H., Brüggemann, N., et al. (2023). Evaluation of Consumer Food Waste Prevention Interventions. Publications Office of the European Union.

U.S. Department of Agriculture, Food Safety and Inspection Service. (2025). Leftovers and food safety. https://www.fsis.usda.gov

U.S. Department of Agriculture, Food Safety and Inspection Service. (2025). How long can you keep leftovers in the refrigerator? https://ask.fsis.usda.gov

U.S. Department of Agriculture, Food Safety and Inspection Service. (2025). Keep Food Safe! Food Safety Basics. https://www.fsis.usda.gov
