# Writing and Localizing Reliable Recipes

A reliable cooking assistant should treat a recipe as **a culinary specification with a separately configurable presentation layer**: changing the wording or layout is not the same as changing the quantities, ingredients, equipment, or cooking process. Editorial guidance supports consistent presentation, while test-kitchen practice shows why apparently minor measurement changes can alter results. [support.americastestkitchen](https://support.americastestkitchen.com/hc/en-us/articles/22914162910363-Flour-Volume-to-Weight)

### Evidence and scope

The report distinguishes four kinds of support:

- **Empirical evidence:** Controlled studies, observational research, or documented measurement experiments.
- **Standards and official guidance:** Measurement definitions and government food-safety guidance.
- **Editorial convention:** Established professional practice, which may differ between publishers.
- **Design recommendation:** A proposed rule for your assistant, informed by those sources but not itself experimentally validated.

Ostmann and Baker’s _The Recipe Writer’s Handbook_ and Jacob’s _Will Write for Food_ are important reference points, but their complete editions were not available for direct inspection here; specific handbook recommendations are therefore attributed only where publicly verifiable, including Jacob’s account of the handbook’s advice. Detailed editorial evidence comes from published institutional style guides and first-party discussions by professional recipe writers and editors—not generic recipe-blog advice. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)

All example wording below is illustrative, not a newly tested recipe.

## Anatomy of a Recipe

### Elements and purposes

The familiar title–ingredients–method structure is an editorial convention, not a scientifically established optimum; professional guides add yield, introductory material, notes, and other elements according to the publication’s audience and purpose. [owens.ecampus](https://owens.ecampus.com/recipe-writers-handbook-ostmann-barbara/bk/9780471172949)

| Element                 | Purpose and recommended treatment                                                                                                                                                                                                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Title**               | Identify the dish and its distinguishing ingredient, technique, or format. Prefer useful specificity over unsupported praise; Food Hero, for example, avoids jargon in recipe names. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)                                           |
| **Headnote**            | Explain what the dish is, why the approach matters, and any important context. A short introduction can carry personality and background without burdening the operational instructions. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)                                                                         |
| **Yield and servings**  | State what the recipe produces, not merely how many people it supposedly feeds. Institutional guidance distinguishes yield from serving size; a loaf, a quantity of soup, and a number of portions are different descriptions. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf) |
| **Active time**         | Estimate hands-on work realistically for the intended reader. Professional editors warn that developers and chefs may prepare ingredients much faster than ordinary readers. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)                                                                                   |
| **Total time**          | Represent elapsed time, including relevant waiting periods. Published baking recipes demonstrate why a short preparation time may coexist with several hours of total time. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/double-light-rye-bread-recipe)                                                                 |
| **Equipment**           | Identify equipment whose size, capacity, material, or function affects success. Institutional guides explicitly require pan and dish dimensions and favor readily available tools. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)                                             |
| **Ingredients**         | Specify the materials, quantities, forms, and preparation states needed to reproduce the result. The ingredient list also supports purchasing and preparation. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/)                                                                                                |
| **Method**              | Explain the procedure in a usable sequence, with clear actions, timing, and endpoint information. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)                                                                                                                                                                |
| **Notes**               | Separate supplementary guidance, storage information, make-ahead options, and variations from the main procedure. Their placement and ordering are house-style choices. [owens.ecampus](https://owens.ecampus.com/recipe-writers-handbook-ostmann-barbara/bk/9780471172949)                                                            |
| **Serving suggestions** | Offer optional accompaniments, presentation ideas, or drinks without making them appear to be mandatory ingredients. Such material belongs to the expressive and advisory layer of a recipe. [nycbar](https://www.nycbar.org/reports/secret-ingredients-how-to-protect-recipes/)                                                       |

**Design recommendation:** Store yield, portion count, and portion description separately. For example, “Makes 12 small rolls; serves 6 as an accompaniment” communicates more than “Serves 6,” without pretending that appetites are standardized.

### Timing deserves explicit definitions

**Editorial convention:** Preparation and cooking times should reflect the intended audience, and ranges are often more honest than single values; Suzanne Fass specifically recommends realistic ranges and sensory cues rather than unrealistic precision. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** Define the assistant’s timing fields explicitly:

- **Active time:** Hands-on work, including ingredient preparation unless explicitly excluded.
- **Cooking time:** Time under heat.
- **Waiting time:** Marinating, chilling, proving, soaking, resting, or cooling.
- **Total time:** Elapsed time along the actual schedule, accounting for overlap.
- **Advance requirement:** A separate flag for overnight or previous-day work.

Do not calculate total time by blindly adding every duration. Chopping during a simmer overlaps with cooking; chilling after baking does not.

### Where editors disagree

Professional practice contains genuine disagreements, not merely good and bad versions of one universal rule. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/)

| Question                                | Documented positions                                                                                                                                                                                                                                                                     | Recommended assistant policy                                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Whole produce or prepared quantity?** | The handbook, as reported by Jacob, favors describing ingredients as purchased, followed by preparation. Jacob argues that adding a whole-item equivalent to every prepared quantity can make lists cumbersome. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/) | Keep a controlling quantity and an optional purchasing approximation; identify which governs.                                            |
| **Explain every technique?**            | Editors differ over how much explanation becomes unnecessary hand-holding. [diannej](https://diannej.com/2010/whats-the-right-length-for-a-recipe/)                                                                                                                                      | Offer expandable technique help rather than making every reader read it.                                                                 |
| **Use “set aside” and “reserve”?**      | Judith Jones objected to empty uses of these expressions and to vague references such as “the mixture.” [diannej](https://diannej.com/2010/three-recipe-phrases-judith-jones-cant-stand/)                                                                                                | Remove redundant wording, but retain operationally necessary reservations: pasta water, divided ingredients, or components needed later. |
| **Spell out units?**                    | TCK Publishing recommends fully written unit names, while Food Hero applies its own capitalization and terminology rules. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)                                                                                          | Treat abbreviations and capitalization as locale-specific style settings, not culinary facts.                                            |

**Design recommendation:** A headnote must not conceal essential operational information. “Requires overnight chilling” belongs near the timing information, not only in an anecdote.

## The Ingredient List

### Order and component grouping

**Editorial convention:** List ingredients in order of first use. Both Food Hero’s institutional style guide and publishing guidance specify this order. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)

For distinct components—such as pastry, filling, and glaze—group ingredients under component headings and use corresponding names in the method; this is a documented publishing convention. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)

**Design recommendation:**

- Use component groups when they help readers allocate ingredients correctly.
- Keep ingredient order synchronized with the selected method presentation.
- Do not alphabetize the operational ingredient list; use a separate shopping-list view for that.
- If several ingredients enter together, use a consistent secondary order. Descending quantity is one publisher’s recommendation, not a universal law. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)

A component heading should identify a culinary object: **For the sauce**, not an ambiguous **Part 2**.

### Precision should match sensitivity

Professional editors emphasize specifying ingredient forms and package sizes, but they also recognize that extra detail can make a recipe look unnecessarily complicated. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** Distinguish three kinds of information:

1. **Quantity:** How much is needed?
2. **Identity and properties:** What exactly is needed?
3. **Preparation state:** In what condition is it measured or used?

For example, “flour” may need a type; “butter” may need a salt specification or temperature; “beans” may need a cooked, drained, or canned state. Add detail when it changes the result, not merely to make the line look technical.

Avoid false precision. An exact-looking conversion cannot repair a vague original ingredient.

### Preparation notes change meaning

**Editorial convention:** A preparation descriptor before the ingredient usually means that preparation happens before measurement; a descriptor after the ingredient means measurement comes first. Food Hero states this rule explicitly. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)

| Wording                 | Intended interpretation                                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 cup chopped nuts**  | Chop first, then measure the chopped nuts. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)        |
| **1 cup nuts, chopped** | Measure the nuts first, then chop them. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)           |
| **1 cup sifted flour**  | Apply the same convention: sift before measuring. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf) |
| **1 cup flour, sifted** | Measure before sifting. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)                           |

**Important qualification:** “1 onion, finely chopped” and “1 finely chopped onion” do not normally specify different amounts: both count one onion. The consequential distinction arises principally with quantities whose measured amount changes with preparation, especially volume; professional editors illustrate this with chopped parsley and sliced vegetables. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

Mass measurement removes many volume ambiguities, but not all preparation-state ambiguities. **Design recommendation:** Explicitly distinguish purchased weight from peeled, trimmed, drained, or cooked weight whenever that distinction matters.

For an AI system, punctuation should be a rendering choice—not the only place where measurement semantics exist.

### “To taste” and optional ingredients

Published test-kitchen recipes sometimes combine a starting range with “to taste,” rather than leaving the reader with no guidance at all. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/gluten-free-baked-doughnuts-recipe)

**Design recommendation:**

- Use **“to taste”** for genuinely adjustable seasoning, with a tested starting amount where possible.
- Tell readers **when** to taste, especially after a reduction or after adding salty ingredients.
- Do not treat structurally important salt, sugar, acid, or leavening as an unrestricted taste adjustment.
- Do not instruct readers to taste raw mixtures that require cooking; a tested forcemeat recipe, for example, recommends cooking a sample before judging seasoning. [seriouseats](https://www.seriouseats.com/gefilte-fish-recipe-8635884)

**Editorial convention:** Mark an optional ingredient in the ingredient list and reflect its optional status in the method; Food Hero uses “optional” in the list and “if desired” in the directions. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)

**Design recommendation:** Distinguish an optional garnish from an optional ingredient whose omission changes texture, cooking behavior, or balance. “Optional” should mean the recipe still works without it.

### Ingredients used repeatedly

**Editorial convention:** One approach is to list the total once, add **“divided,”** and state the allocation at each use. For distinct components, publishers may instead repeat the ingredient under the relevant component headings. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)

Illustrative wording:

> 3 tablespoons olive oil, divided  
> Use 2 tablespoons for the vegetables and the remaining tablespoon for the sauce.

**Design recommendation:** Store the total and every allocation separately, then validate that the allocations add up. Never leave “divided” unexplained, and do not confuse “additional oil for greasing” with an amount already included in the total.

Water also requires an explicit house rule: institutional recipes list it when it is a measured ingredient, while some recipe traditions treat it differently. For an assistant, listing measured water is the clearer default; unmeasured water for washing or boiling can remain an operational instruction. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/classic-baguettes-recipe)

## Units and Measurement

### Weight versus volume

**Empirical evidence:** America’s Test Kitchen reports that measuring technique can produce up to a 20% difference in the weight of a cup of flour; its published comparison of dry and liquid measuring cups involved 18 participants. [americastestkitchen](https://www.americastestkitchen.com/how_tos/5450-dry-versus-liquid-measuring-cups)

**Standards-based guidance:** NIST promotes measuring recipe ingredients by mass with an appropriate kitchen scale to improve accuracy, including both solid and liquid ingredients. [nist](https://www.nist.gov/pml/owm/nist-metric-recipes-sp-1290)

**Design recommendation:** Prefer mass for reproducibility-sensitive ingredients, particularly baking ingredients. Retain volume where it is practical and sufficiently precise, but do not assume that “metric” automatically means “accurate”: an inappropriate scale or an ambiguous ingredient state can still produce poor measurements.

### A cup of flour has no universal mass

Different authoritative test kitchens deliberately use different flour baselines:

| Source                     | Published baseline or method                                                                                                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **King Arthur Baking**     | Its recipes commonly specify 1 cup all-purpose flour as 120 g and instruct readers to spoon gently into the cup and level it. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/whole-grain-banana-bread-recipe)                        |
| **America’s Test Kitchen** | Its standard is 5 ounces, approximately 142 g, based on its dip-and-sweep approach and measurements by volunteers. [support.americastestkitchen](https://support.americastestkitchen.com/hc/en-us/articles/22914162910363-Flour-Volume-to-Weight) |

These figures are not interchangeable universal constants: the test kitchens use different measurement practices. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/whole-grain-banana-bread-recipe)

**Design recommendation:** Use this conversion hierarchy:

1. The source recipe’s own tested mass.
2. The source publisher’s ingredient-weight table and measurement method.
3. A clearly identified ingredient-specific reference.
4. An explicitly labeled estimate.
5. No conversion if the uncertainty would be consequential.

Replacing every flour cup with one preferred gram value can change the formula rather than merely localize it.

### Regional volume conventions

| Context                             | Published convention                                                                                                                                                                                                                                                                                                       | Consequence                                                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **US household measures**           | NIST gives approximately 237 mL per cup, 15 mL per tablespoon, and 5 mL per teaspoon; these are rounded household equivalents. [nist](https://www.nist.gov/pml/owm/metric-household)                                                                                                                                       | Do not confuse a rounded conversion with an exact definition.                                                 |
| **US nutrition labeling**           | Federal labeling rules use 240 mL per cup, 15 mL per tablespoon, and 5 mL per teaspoon. [govinfo](https://www.govinfo.gov/content/pkg/CFR-2025-title21-vol2/xml/CFR-2025-title21-vol2-sec101-9.xml)                                                                                                                        | Nutrition-label definitions do not establish the measuring practice of every US recipe.                       |
| **Australian publisher convention** | Taste’s chart specifies a 250 mL cup, 20 mL tablespoon, and 5 mL teaspoon. [taste.com](https://www.taste.com.au/images/common/Taste-Weights-Measurements-A3-V3.pdf)                                                                                                                                                        | An Australian tablespoon is not interchangeable with a 15 mL tablespoon.                                      |
| **UK-facing localization**          | The appropriate editorial policy is to retain metric or Imperial units explicitly and verify any spoon or cup convention against the source publication, rather than inferring it from English-language text alone. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/chapter/units-of-measurement/) | Treat “UK” as a locale requiring a style profile, not as a sufficient definition of every historical measure. |

Some cooking charts deliberately round fractional measures: Taste lists a 250 mL cup but rounds one-third cup to 80 mL. That is convenient cooking guidance, not an exact mathematical identity. [taste.com](https://www.taste.com.au/images/common/Taste-Weights-Measurements-A3-V3.pdf)

**Design recommendation:** Store the source measurement standard independently of the reader’s destination locale. An Australian recipe rendered for a US reader still begins with Australian source quantities.

### Presenting dual units

Publishing guidance favors consistency, and professional culinary teaching warns that working between measurement systems can introduce inaccuracies. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/chapter/units-of-measurement/)

**Design recommendation:**

- Choose one controlling system for each rendered version.
- Put secondary units consistently in parentheses.
- Convert from unrounded stored quantities, not previously rounded display values.
- Round according to ingredient sensitivity and available measuring tools.
- Encourage readers to follow one coherent measurement track.
- Label conversions that have not been tested.

A digital unit switch is generally cleaner than showing grams, ounces, cups, and whole-item approximations on every line. That is a usability recommendation, not a finding from a recipe-specific controlled trial.

### Common conversion traps

| Trap                    | Recommended handling                                                                                                                                                                                                                                                             |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flour by volume**     | Preserve the source’s measurement method and weight baseline; authoritative test kitchens differ. [support.americastestkitchen](https://support.americastestkitchen.com/hc/en-us/articles/22914162910363-Flour-Volume-to-Weight)                                                 |
| **Butter by volume**    | Use the source’s stated mass where available. Published recipes often supply mass alongside tablespoons, avoiding dependence on packaging conventions. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/gluten-free-baked-doughnuts-recipe)                           |
| **“A stick of butter”** | Treat “stick” as a source-market packaging unit. Verify its mass before translating; never replace it with an unspecified local packet.                                                                                                                                          |
| **Ounces**              | Require an explicit distinction between mass and fluid volume before conversion.                                                                                                                                                                                                 |
| **Salt by spoon**       | Preserve the specified product or use its verified mass. One tested Serious Eats recipe explicitly identifies Diamond Crystal kosher salt and gives its tablespoon weight. [seriouseats](https://www.seriouseats.com/gefilte-fish-recipe-8635884)                                |
| **Egg size**            | Preserve the source-market size specification until a market-specific grading or edible-mass reference is available. Do not invent an exact gram equivalent.                                                                                                                     |
| **Onion size**          | Use count for forgiving applications; use a controlling prepared weight or volume when reproducibility matters. Editors explicitly disagree over the value of adding whole-item equivalents everywhere. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/) |
| **Can or jar**          | Specify package quantity and whether contents are drained, rinsed, or used with liquid. Institutional style guidance gives these distinctions explicitly. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)                |
| **Bunch or handful**    | Treat these as intentionally approximate unless the recipe supplies a controlling quantity; Jacob’s editorial discussion highlights variation in bunch sizes. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/)                                           |

The sources reviewed do not establish a universal egg-size, onion-size, or butter-package conversion table. Those mappings require additional product- and market-specific references.

### Counted ingredients

**Design recommendation:** Retain counts where they correspond to a meaningful culinary unit:

- “2 garlic cloves, crushed”
- “4 individual fish fillets”
- “1 lemon, plus extra wedges for serving”

Add a tested weight, thickness, or size range when it affects cooking. Count alone is insufficient if a fillet’s thickness controls doneness.

For fractional eggs in a scaled recipe, require a tested handling instruction or edible-mass approach; do not silently round the ingredient up or down.

## Writing the Method

### Write task-sized steps

**Editorial convention:** Begin a new step when a new task begins; professional publishing guidance does not require a new numbered step for every individual verb. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)

**Design recommendation:** Use **one main objective per step**, allowing closely connected actions together.

> Heat the oil over medium heat. Add the onion and cook, stirring occasionally, until softened.

This is one coherent cooking task. By contrast, making a dressing, checking a roast, and preparing a garnish generally deserve separate steps.

**Editorial convention:** Use active verbs and stable terminology. Fass favors direct constructions such as “Beat the eggs” and warns against inconsistent descriptions of the same operation. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

### Separate preparation carefully

A preparation section can make advance tasks visible, but moving every preparation action to the beginning is not necessarily a harmless formatting change. Professional editors specifically warn against starting ovens or boiling water hours before they are needed. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** Classify tasks by dependency rather than by their verb alone:

| Task type                               | Appropriate treatment                                                                            |
| --------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Must precede cooking**                | Place in preparation: measure ingredients, make a required paste, or prepare a pan.              |
| **Can overlap safely**                  | Keep near the relevant waiting period, with an explicit “while…” relationship.                   |
| **Needs freshness**                     | Keep close to use unless the tested recipe permits advance preparation.                          |
| **Requires a preceding transformation** | Do not move earlier: cooling, slicing cooked food, or reserving liquid generated during cooking. |
| **Introduces a safety constraint**      | Preserve the required handling order and warning.                                                |

No robust evidence located for this report establishes that a separate mise-en-place section is always superior. It is a presentation option whose usefulness depends on the dish and reader.

### Make parallel work explicit

**Editorial convention:** Actions should appear when they are needed, rather than following a mechanical “preheat first” template. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** State both the opportunity and the dependency:

> While the lentils simmer, prepare the dressing.  
> Have the dressing ready before draining the lentils.

For an experienced cook, overlapping tasks may reduce elapsed time. For a beginner, the assistant can offer a sequential version—but must recalculate the timing rather than preserving an incompatible total-time claim.

Internally, represent the method as a dependency graph; section headings should be views of that graph, not the underlying cooking logic.

### Give endpoint cues

Professional editors recommend sensory descriptions alongside time ranges because ingredients and appliances differ. Published test-kitchen recipes combine time with observations such as puffiness, browning, texture, and internal temperature. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/double-light-rye-bread-recipe)

A useful instruction pattern is:

> **Action + equipment/heat + time range + observable endpoint + adjustment if needed.**

Illustrative wording:

> Cook over medium-low heat until the onion is soft and translucent, stirring regularly; lower the heat if it begins browning before softening.

**Design recommendation:** Specify relevant dimensions before the cooking step: thickness, dice size, portion size, and starting state can matter more than an exact-looking time.

### Separate quality from safety

**Empirical evidence:** A study of 226 egg-dish recipes found that time appeared in 92%, while only two recipes provided endpoint temperatures. In preparation trials, an egg casserole did not consistently reach the recommended temperature when its appearance suggested that it was done. [pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC5302401/)

Sensory cues therefore help readers judge culinary quality, but they cannot universally replace appropriate safety criteria. [krex.k-state](https://krex.k-state.edu/items/abc208cf-0595-4922-9527-3aaf8cb44771)

**Design recommendation:** Store quality endpoints and safety endpoints separately. Use the relevant jurisdiction’s verified guidance for the dish rather than deriving safety from color or from a generic conversion.

### Put warnings at the action

**Empirical evidence:** Research involving 186 consumers found improved food-safety behavior when relevant instructions were embedded in the poultry recipes they followed. Health Canada consequently provides a recipe style guide for integrating food-safety guidance into recipes. [foodprotection](https://www.foodprotection.org/upl/downloads/meeting/archive/57bf1df5dcd7e01e9cbf3.pdf)

**Design recommendation:** Place a warning before or within the action it constrains—not only in an endnote. Necessary handling instructions should remain visible in both concise and detailed recipe modes.

### Cognitive-load implications

Chandler and Sweller’s experiments found benefits from integrating information that learners otherwise had to mentally combine, but also found that unnecessary explanatory material could hinder learning. [tandfonline](https://www.tandfonline.com/servlet/linkout?url=https://dx.doi.org/10.1207%252Fs1532690xci0804_2&type=Scholix)

**Application to recipes—an inference, not a direct experimental result:** Show essential quantities, warnings, and technique cues near the relevant action, while making nonessential explanation optional. Repeating a step’s allocated ingredient quantity may reduce backtracking, provided the value is generated from the same data as the ingredient list.

## Heat and Equipment

### State the oven mode

**Editorial convention:** An oven temperature is incomplete unless the reader knows the intended mode. Australian publishing guidance explicitly separates conventional electric, fan-forced, Fahrenheit, and gas settings. [taste.com](https://www.taste.com.au/images/common/Taste-Weights-Measurements-A3-V3.pdf)

**Design recommendation:** Store these independently:

- Temperature value and unit
- Oven mode
- Rack position
- Preheating requirement
- Tested alternative settings

Do not infer that a Fahrenheit temperature means conventional heat or that a Celsius temperature means fan heat.

### Conversion rules are approximations

Taste’s chart commonly pairs conventional and fan-forced settings with a 20°C difference; for example, it pairs 250°C conventional with 230°C fan-forced, 500°F, and gas mark 9. [taste.com](https://www.taste.com.au/images/common/Taste-Weights-Measurements-A3-V3.pdf)

That is a published cooking convention, not proof that one adjustment produces equivalent results for every dish and oven.

**Design recommendation:**

- Convert Fahrenheit and Celsius mathematically, then round sensibly for the appliance.
- Treat gas marks as chart mappings, not as another directly interchangeable numeric unit.
- Keep a temperature-unit conversion separate from an oven-mode adaptation.
- Prefer tested settings or manufacturer-specific advice over an assumed universal fan adjustment.
- Label untested mode conversions.

The temperature-unit relationship is:

\[
^\circ C = (^\circ F - 32)\times\frac{5}{9}
\]

Changing units does not, by itself, justify changing the cooking mode.

### Describe stovetop behavior

Professional editors recommend describing what the cook should observe rather than relying exclusively on elapsed time. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** Pair stovetop levels with behavior:

| Heat label | Useful accompanying instruction                                                         |
| ---------- | --------------------------------------------------------------------------------------- |
| **Low**    | Describe the intended gentle activity or absence of browning.                           |
| **Medium** | Specify the desired sizzle, softening, or steady cooking behavior.                      |
| **High**   | Describe the intended rapid boil or browning, plus the relevant overheating warning.    |
| **Simmer** | Explain the desired bubbling behavior rather than treating it as a fixed knob position. |

Do not translate “medium heat” into one universally valid induction setting, wattage, or pan-surface temperature.

### Specify consequential equipment

Institutional guidance requires pan dimensions, and test-kitchen adaptations demonstrate that changing pan size changes thickness and baking time. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/small-batch-brownies-recipe)

**Design recommendation:** Specify:

- Internal pan dimensions or useful capacity
- Shape and depth where relevant
- Material or finish when the tested recipe depends on it
- Lid status
- Number of pans or batches
- Any required equipment capability

“Large pan” can be adequate for an experienced cook making a forgiving soup. It is poor specification when crowding, depth, or capacity controls the result.

### Tolerate differences explicitly

King Arthur’s published brownie adaptation gives different baking times for different pans and explains the resulting differences in thickness. This is stronger guidance than suggesting that every pan of roughly similar capacity is interchangeable. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/small-batch-brownies-recipe)

**Design recommendation:** Offer verified alternatives, tell readers what changes, and provide adjustment cues. Do not present microwave, pressure-cooker, air-fryer, and conventional-oven methods as equivalent layout variants.

## Scaling

### Begin with proportional quantities

Professional culinary teaching uses a conversion factor based on required yield divided by original yield, then multiplies ingredient quantities accordingly. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/open/download?type=print_pdf)

\[
k=\frac{\text{desired yield}}{\text{original yield}}
\]

\[
\text{new ingredient quantity}=k\times\text{original quantity}
\]

For bread formulas, baker’s percentages express ingredients relative to flour weight and provide an established proportional-scaling framework. [kingarthurbaking](https://www.kingarthurbaking.com/pro/reference/bakers-percentage)

**Important correction:** Salt, spices, yeast, and chemical leaveners are not automatically exceptions to proportional scaling. The appropriate question is whether the **formula, geometry, process, and intended endpoint remain equivalent**, not whether an ingredient appears on a folklore list of things that “never double.” [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/open/download?type=print_pdf)

### What changes with scale

| Item                      | Starting treatment                                                                                                                                                            | Why further adjustment may be needed                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Main ingredients**      | Scale proportionally by mass. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/open/download?type=print_pdf)                                           | Equipment capacity and cooking geometry may no longer match.                                                                                                                                                                               |
| **Salt**                  | Preserve the formula’s proportion unless there is a recipe-specific reason to change it. [kingarthurbaking](https://www.kingarthurbaking.com/pro/reference/bakers-percentage) | Final concentration, salty ingredient brands, reductions, and taste preferences require separate consideration.                                                                                                                            |
| **Spices and flavorings** | Start proportionally; validate the result. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/open/download?type=print_pdf)                              | Do not assume a universal “use half as much when doubling” rule.                                                                                                                                                                           |
| **Chemical leavening**    | Start with proportional formula scaling. [opentextbc](https://opentextbc.ca/basickitchenandfoodservicemanagement/open/download?type=print_pdf)                                | A much deeper or differently shaped product is a process change, not merely a larger batch.                                                                                                                                                |
| **Yeast**                 | Preserve the formula when reproducing the same process. [kingarthurbaking](https://www.kingarthurbaking.com/pro/reference/bakers-percentage)                                  | Yeast quantity, temperature, and fermentation schedule interact; published alternatives change time and conditions together. [kingarthurbaking](https://www.kingarthurbaking.com/recipes/king-arthurs-classic-white-sandwich-bread-recipe) |
| **Reduction liquids**     | Do not assume that multiplying the liquid alone preserves the result.                                                                                                         | **Design inference:** Vessel geometry, exposed area, and the required final concentration must be considered together.                                                                                                                     |
| **Oil for a pan**         | Treat separately from oil incorporated into the food.                                                                                                                         | **Design inference:** Coating a surface is not the same scaling problem as maintaining a formula percentage.                                                                                                                               |
| **Cooking time**          | Do not multiply by the servings factor.                                                                                                                                       | Published pan adaptations use revised times tied to the changed format. [kingarthurbaking](https://www.kingarthurbaking.com/blog/2022/09/28/how-to-turn-any-cake-recipe-into-6-inch-mini-cakes)                                            |
| **Preparation time**      | Re-estimate rather than multiplying mechanically.                                                                                                                             | **Design inference:** Some tasks repeat per item; others have fixed setup time or can be batched.                                                                                                                                          |

The formula is the starting point; the cooking system still needs validation.

### Pan geometry matters

King Arthur’s guidance for converting cakes to smaller pans explicitly discusses changes in cake height and advises checking doneness earlier. [kingarthurbaking](https://www.kingarthurbaking.com/blog/2022/09/28/how-to-turn-any-cake-recipe-into-6-inch-mini-cakes)

**Geometric inference:** To preserve batter depth, scale the pan’s base area with batter quantity—not its diameter. For geometrically similar round pans:

\[
d*{\text{new}}=d*{\text{old}}\sqrt{k}
\]

This is a geometry calculation, not a tested guarantee of equivalent baking. Pan material, shape, oven loading, and heat transfer remain relevant.

**Design recommendation:** When feasible, repeat the original unit—two original-size cakes, for example—rather than producing one substantially deeper cake and assuming the old method still applies.

### Batch size changes the process

Published bread-machine guidance scales ingredients to machine capacity and also recognizes that the machine’s fermentation conditions may require recipe-specific adjustment. [kingarthurbaking](https://www.kingarthurbaking.com/blog/2018/04/30/how-to-convert-recipes-to-a-bread-machine)

**Design recommendation:** Check scaling against:

- Pan and vessel capacity
- Mixer capacity
- Batch count
- Oven space and loading
- Portion dimensions
- Holding and cooling requirements
- The recipe’s tested scaling range

Never label a calculated scale-up as tested merely because its arithmetic is correct.

For preservation recipes, apply an especially conservative policy: retain validated procedures and require expert review rather than inventing processing changes; extension guidance emphasizes current, safe preservation methods. [extension.k-state](https://extension.k-state.edu/news-and-publications/news/stories/2024/03/food-safety-publication-update.html)

## Language and Locale

### Separate language from country

Professional food-writing guidance recognizes that spelling, measurements, terminology, and house style vary by publication and market. Regional volume conventions independently demonstrate why language alone cannot determine quantities. [bcyukonbookprizes](https://bcyukonbookprizes.com/wp-content/uploads/2022/11/Food-Writing-101.pdf)

**Design recommendation:** Maintain separate fields for:

- Language and regional locale
- Source measurement standard
- Destination measurement preference
- Terminology profile
- Instructional grammatical style
- Ingredient-market mappings
- Equipment assumptions
- Food-safety jurisdiction

An English recipe is not necessarily an American recipe. A German translation does not make its source quantities German quantities.

### Mood and instructional voice

Official Canadian French guidance accepts both infinitive and imperative instructions, identifies different tones, and emphasizes consistency within a text. [nos-langues.canada](https://nos-langues.canada.ca/fr/cles-de-la-redaction/infinitif-imperatif)

The following are **original house-style examples**, not claims that every publication in a country uses the same form:

| Language/profile           | Example                       | Treatment                     |
| -------------------------- | ----------------------------- | ----------------------------- |
| **English**                | “Finely chop the onion.”      | Direct imperative.            |
| **German, impersonal**     | “Die Zwiebel fein hacken.”    | Infinitive-style instruction. |
| **German, direct address** | “Hacke die Zwiebel fein.”     | Familiar singular imperative. |
| **French, impersonal**     | “Hacher finement l’oignon.”   | Infinitive.                   |
| **French, direct address** | “Hachez finement l’oignon.”   | Plural/formal imperative.     |
| **Spanish, impersonal**    | “Picar finamente la cebolla.” | Infinitive-style instruction. |

**Design recommendation:** Choose a consistent register and instructional pattern for each locale. Do not mistake normal subordinate clauses—such as explanations of what should happen—for inconsistent instruction mood.

### Section headings are mappings

Institutional recipes already demonstrate different headings and ordering conventions, while French instructional materials distinguish ingredients, equipment, preparation/cooking time, and the sequence of actions. [assistancescolaire](https://www.assistancescolaire.com/eleve/CE2/francais/reviser-une-lecon/9le02/print?print=2&printSheet=1)

A proposed heading map might be:

| Function       | English     | German       | French               | Spanish            |
| -------------- | ----------- | ------------ | -------------------- | ------------------ |
| Ingredients    | Ingredients | Zutaten      | Ingrédients          | Ingredientes       |
| Advance tasks  | Preparation | Vorbereitung | Préparatifs          | Preparación previa |
| Main procedure | Method      | Zubereitung  | Préparation / Étapes | Elaboración        |
| Advice         | Notes       | Hinweise     | Conseils             | Notas              |

**Design recommendation:** Map functions, not strings. A French _préparation_ heading may contain the entire procedure; it must not automatically become only the advance-preparation subsection.

### Ingredient translation needs functional checks

Professional editors explicitly warn that familiar ingredients and package sizes may be unavailable or unfamiliar in another region, and recommend suitable alternatives with quantities where appropriate. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

**Design recommendation:** Classify a proposed localization as one of three things:

1. **Naming change:** Same ingredient, different regional name.
2. **Product-equivalence mapping:** Similar category, but relevant properties must be checked.
3. **Substitution:** A different ingredient requiring culinary validation.

Dairy is a useful test case. Do not automatically equate quark, fromage blanc, cream cheese, sour cream, crème fraîche, or locally named cream products merely because a dictionary places them in a neighboring category. Require relevant product information—such as fat, moisture, acidity, texture, and heating behavior—before approving the substitution.

Likewise, flour names require more than a lexical match. A localized name should preserve the ingredient’s intended function, not simply resemble the source label.

### Packages and produce

Professional editorial guidance treats unavailable package sizes and unspecified package quantities as practical recipe defects. Jacob’s discussion also shows why produce counts and bunches can be poor substitutes for controlling quantities. [diannej](https://diannej.com/2014/questions-from-a-recipe-copy-editor/)

**Design recommendation:** Preserve the culinary amount independently of the purchasing format:

- The recipe specifies the required contents.
- The shopping view translates that amount into local packages.
- Excess package contents do not automatically enter the recipe.
- Drained quantity and package net quantity remain separate.
- Produce counts can be approximate shopping guidance rather than the controlling amount.

A country-level default can help, but the assistant should allow product-level overrides.

## Restructuring Existing Recipes

### Separate editing from adaptation

Copy editors correct wording, consistency, missing information, and cross-references, but substantive quantity changes should be queried rather than silently imposed. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)

| Transformation                              | Risk and appropriate treatment                                                                                                                                                                                                      |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Spelling, punctuation, typography**       | Usually editorial, provided meaning remains unchanged. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)                                                                                                      |
| **Consistent naming of components**         | Editorial improvement when referents remain correct. [diannej](https://diannej.com/2010/three-recipe-phrases-judith-jones-cant-stand/)                                                                                              |
| **Adding headings or numbering**            | Usually presentational, but verify that task relationships remain intact. [tckpublishing](https://www.tckpublishing.com/how-to-write-a-recipe/)                                                                                     |
| **Rewriting into clearer original wording** | Preserve every operational constraint; separately assess rights in protected expression. [nycbar](https://www.nycbar.org/reports/secret-ingredients-how-to-protect-recipes/)                                                        |
| **Moving prep notes into steps**            | Check for duplicate or omitted preparation and preserve the measurement state. [foodhero](https://foodhero.org/sites/foodhero-prod/files/health-tools/FHRecipeStyleGuide_092523_3.pdf)                                              |
| **Changing units**                          | Preserve the source quantity and its measurement assumptions; flour conversions illustrate the risk. [support.americastestkitchen](https://support.americastestkitchen.com/hc/en-us/articles/22914162910363-Flour-Volume-to-Weight) |
| **Substituting ingredients**                | Treat as culinary adaptation, not translation alone. [diannej](https://diannej.com/2016/10-pet-peeves-cookbook-copy-editor/)                                                                                                        |
| **Scaling or changing pans**                | Reassess equipment, depth, timings, and endpoints. [kingarthurbaking](https://www.kingarthurbaking.com/blog/2022/09/28/how-to-turn-any-cake-recipe-into-6-inch-mini-cakes)                                                          |
| **Changing appliance or oven mode**         | Treat as a process change requiring specific guidance or testing. [taste.com](https://www.taste.com.au/images/common/Taste-Weights-Measurements-A3-V3.pdf)                                                                          |

**Design recommendation:** “Changed freely” should mean **low culinary risk after semantic verification**, not “no review required.”

### Preserve an auditable original

A proposed adaptation workflow:

1. Retain the source text and provenance separately from the rendered recipe.
2. Extract ingredients, quantities, preparation states, equipment, and steps.
3. Flag ambiguity rather than resolving it invisibly.
4. Build ingredient allocations and task dependencies.
5. Apply the requested style and locale.
6. Classify every change as presentational, interpretive, or culinary.
7. Reconcile all ingredient uses, temperatures, times, and warnings.
8. Record testing status for the resulting version.

This is a **design recommendation**, not a published universal editorial workflow.

Useful status labels include:

- **Reformatted; culinary quantities unchanged**
- **Units converted; converted version not retested**
- **Adapted with substitutions; not retested**
- **Tested in the stated locale and equipment configuration**

The status belongs to the version, not merely to the original recipe.

### Copyright: distinguish layers

**US legal guidance:** A mere ingredient list and a simple set of functional directions are not copyrightable, while original explanatory text, commentary, photographs, and other expressive material may be protected. [nycbar](https://www.nycbar.org/reports/secret-ingredients-how-to-protect-recipes/)

That does not mean an entire recipe page or cookbook can be freely copied; protected expression and potentially protected compilation elements require separate analysis. [copyright](https://www.copyright.gov/comp3/docs/compendium.pdf)

**German official guidance:** Copyright protection depends on a personal intellectual creation, and protected texts, photographs, and other works generally require authorization unless an applicable exception permits their use. [dpma](https://www.dpma.de/service/schutzrechte_kurz_erklaert/urheberrecht/index.html)

**Design recommendation:** Do not export a US ingredient-list rule as a worldwide clearance policy. Translation, paraphrasing, and reformatting should not be treated as automatic permission to reproduce protected material.

### Attribution and adaptation labels

Attribution does not replace authorization where authorization is required. [urheberrecht](https://www.urheberrecht.de/rezepte/)

**Editorial recommendation:** Use a clear provenance statement when substantive reliance warrants it:

> Adapted from [author], _[title]_ ([year]), [page or URL]. Quantities retained; units converted and preparation separated from cooking. Converted version not retested.

Distinguish:

- **From / reproduced with permission:** Authorized reproduction.
- **Adapted from:** Acknowledged reliance with stated changes.
- **Inspired by:** Influence acknowledged, without implying permission or a particular legal status.

There is no sound reason to encode a “change three ingredients” shortcut: copyright analysis concerns the nature of what is used, including protected expression—not a recipe-edit counter. [nycbar](https://www.nycbar.org/reports/secret-ingredients-how-to-protect-recipes/)

For a commercial assistant, obtain separate legal review of source access, licenses, translations, database use, and republication. A provenance field is necessary editorial infrastructure, not a rights-clearance mechanism.

## Readability and Accessibility

### Support different experience levels

**Empirical evidence:** The expertise-reversal literature finds that instructional methods useful to novices can become redundant or counterproductive for more knowledgeable learners. However, results depend on the task; research on less structured tasks has not always reproduced the effect. [tandfonline](https://www.tandfonline.com/doi/full/10.1207/S15326985EP3801_4)

These findings support adaptable instructional detail, not a claim that every experienced cook should always receive the shortest possible recipe.

| Information     | Beginner view                                 | Experienced view                             |
| --------------- | --------------------------------------------- | -------------------------------------------- |
| Technique       | Short explanation and optional demonstration  | Familiar technique term                      |
| Preparation     | Explicit size, sequence, and readiness checks | Concise specifications                       |
| Timing          | Clear dependencies and suggested order        | Compact scheduling cues                      |
| Doneness        | Concrete observations                         | Same essential endpoints, fewer explanations |
| Safety          | Fully visible                                 | Fully visible                                |
| Troubleshooting | Point-of-use help                             | Expandable help                              |

The table is a **design proposal**, informed by the research rather than directly tested as a recipe interface.

### Use progressive detail

Professional editors balance explanatory detail against readability and page constraints, and disagree about where that balance should fall. [diannej](https://diannej.com/2010/whats-the-right-length-for-a-recipe/)

**Design recommendation:** Provide three layers:

1. **Core instruction:** Everything required to execute the recipe correctly and safely.
2. **Technique help:** Expandable explanations of unfamiliar actions.
3. **Background:** Culinary science, history, variations, and further reading.

Do not hide required temperatures, ingredient allocations, or warnings inside optional help.

### Accessibility recommendations

The following are proposed product requirements, not a claim of compliance with a particular accessibility standard:

- Use semantic headings and ordered steps.
- Offer a linear reading order rather than relying on a two-column layout.
- Keep essential information in text, not only in photographs or icons.
- Provide text explanations for technique images.
- Do not communicate warnings through color alone.
- Make fractions and unit abbreviations understandable in speech output.
- Give timers meaningful names.
- Allow users to repeat the current step and retrieve its ingredients.
- Support adjustable text size and a low-distraction cooking view.
- Keep optional explanation from interrupting the action sequence.

The cognitive-load rationale is to reduce unnecessary searching and mental integration, while avoiding redundant material that competes with the task. [tandfonline](https://www.tandfonline.com/servlet/linkout?url=https://dx.doi.org/10.1207%252Fs1532690xci0804_2&type=Scholix)

### Plain language without losing precision

Editors recommend consistent terms and caution against unexplained technical language, while also warning that vague verbs can conceal important technique. [diannej](https://diannej.com/2010/three-recipe-phrases-judith-jones-cant-stand/)

**Design recommendation:** Explain the technique instead of merely replacing it with “cook” or “mix.”

For example:

> Stir gently with a spatula, lifting from the bottom, until no dry flour remains.

This can be more useful than either unexplained “fold” or underspecified “mix.” Keep precise component names—**batter**, **dressing**, **cooked lentils**—rather than repeatedly referring to “the mixture.”

### Validate with actual cooks

Recipe development benefits from consumer evaluation: a recent public-sector collaboration tested recipes for novice home cooks and used feedback on practicality, taste, and affordability to guide revisions. [teagasc](https://teagasc.ie/about/research-innovation/engage-with-us/case-studies/safefood-providing-easy-and-nutritious-recipes-for-novice-home-cooks/)

**Design recommendation:** Test the assistant’s output at two levels:

| Validation level                   | Checks                                                                                                                                                                                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Automated specification checks** | Every ingredient is used; allocations reconcile; optional ingredients remain optional; units are dimensionally compatible; dependencies survive restructuring; quantities match between list and method; provenance and testing status remain attached. |
| **Human cooking checks**           | Readers identify missing information, confusing terminology, unrealistic times, equipment mismatches, inaccessible ingredients, and unexpected results. Include target-locale cooks and both novice and experienced users.                              |

A recipe can be grammatically polished and internally consistent yet still fail in a kitchen. Automated validation should therefore establish what the assistant has preserved or calculated—not imply that the dish has been cooked and verified.
