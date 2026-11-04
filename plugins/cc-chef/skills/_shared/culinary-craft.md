# Culinary craft

Use this file for judging and improving the flavour quality of a recipe: when `create-recipe` drafts a dish or `rework-recipe` reviews one, apply the rules below so the result is grounded, cookable everyday food (comfort food, traditional fare, rustic home cooking) with one or two deliberate touches that make it worth remembering. It is not a source of star-chef technique or experimental pairings. Sections 1-3 give the craft rules, section 4 the tradition model, section 5 the review checklist and the AI failure modes, section 6 the evidence notes.

Conventions: `(to verify)` marks a claim that only one research report made. "Default" is what the plugin does when reports disagree. Evidence tags: strong = controlled experiments or solid physical chemistry; moderate = plausible mechanism, thin data on real dishes; practitioner = heuristic from chefs and test kitchens; design = a rule chosen for this plugin.

## 0. The one-paragraph recipe model

Start from the dish's familiar frame, execute its main component well, season in stages, build depth with two or three proven techniques (aromatics in fat, browning, blooming, reduction), balance with salt, acid, umami, fat and (only if needed) sweetness, then finish with exactly one contrasting element from the same or a neighbouring tradition. Everything that does not do a job is cut. Order of diagnosis for a flat dish: salt first, then acid, then fat and umami, then contrast.

## 1. Balance

### 1.1 What "balanced" means

| Rule                                | Detail                                                                                                                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Balance is proportion, not equality | A dish need not contain all five tastes; a pickle stays sour and a bitter-green dish may stay bitter. Balanced = nothing unintentionally dominates, nothing essential is missing, it fits the dish and the eater (design) |
| Diagnose before adding              | Taste a spoonful with a pinch of salt and another with a little acid before prescribing either; a tomato-based dish may already have enough acid                                                                          |
| Count salt already present          | Stock, cheese, cured meat, miso, soy, fish sauce, commercial curry paste and reduction all add salt; set the final adjustment after the dish is assembled                                                                 |
| Give each flavour a job             | If an ingredient or a repeated addition cannot be given a different purpose, remove it (design)                                                                                                                           |

### 1.2 The levers

| Lever                 | Does                                                                                                                       | Use in recipes                                                                                                                   | Watch out                                                                                                                                                     | Evidence                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Salt                  | Seasons, lifts existing flavour, suppresses bitterness more than sweetness so sweet and savoury notes show                 | Salt in stages: meat ahead, aromatics as they cook, cooking water, final adjustment                                              | Does not amplify everything equally; stacking salty ingredients over-salts                                                                                    | strong                                         |
| Acid                  | Adds contrast and freshness, changes how the bite is perceived, can raise or lower perceived saltiness depending on amount | Wine or tomato in the base, vinegar, citrus, yoghurt, tamarind or pickles at the end                                             | "Cuts fat" is a figure of speech, the fat is still there; too much acid or several acid finishes stacked taste sharp; a flat dish is often under-salted first | moderate                                       |
| Sweetness             | Rounds acid and bitterness; browning gives a natural sweet note                                                            | A pinch in tomato sauce, curry or braise; sweet vegetables in the base                                                           | Only to balance, never so the savoury dish tastes sweet; sugar does not remove acid                                                                           | strong (mixtures)                              |
| Bitterness            | Adds adult complexity (greens, char, citrus peel, cocoa, coffee)                                                           | Keep where the tradition wants it, soften with salt and fat                                                                      | Excess lowers liking                                                                                                                                          | moderate                                       |
| Umami                 | Savoury depth; glutamate plus nucleotide sources multiply each other                                                       | Tomato or tomato paste, mushrooms, aged cheese, anchovy, soy, fish sauce, miso, kombu with bonito, stock, cured meat             | Pick a source that fits the dish's identity (no miso in a Bolognese by reflex); one good source beats five                                                    | strong                                         |
| Kokumi (mouthfulness) | Makes existing tastes feel fuller and longer                                                                               | Long-simmered stock, aged cheese, fermented seasonings, slowly cooked onion and garlic                                           | A modulator, not a basic taste; do not claim "kokumi" for any rich dish                                                                                       | moderate; receptor work partly industry-linked |
| Fat                   | Carries fat-soluble aroma, lubricates, gives richness                                                                      | Cook aromatics and spices in it; finish with a fat that has its own aroma (olive oil, brown butter, sesame oil, ghee, chili oil) | Slows release of some aromas rather than boosting all; too much mutes bright notes; name the job of each fat                                                  | strong                                         |
| Heat / pungency       | Alertness, contrast with richness; a sensation, not a taste                                                                | Make it adjustable and optional; fat and sugar soften the burn                                                                   | Excess masks everything; use as accent                                                                                                                        | strong (physiology)                            |
| Aroma                 | Most of what people call flavour                                                                                           | Fresh herbs late, spices bloomed early, zest                                                                                     | Volatile; heat and long cooking drive it off                                                                                                                  | strong                                         |

### 1.3 Well founded, overstated, myth

| Status                    | Statements                                                                                                                                                                                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Well founded              | Salt tames bitterness in eggplant, greens, coffee and chocolate; glutamate sources plus nucleotide sources (tomato or parmesan with meat, kombu with bonito, anchovy in a beef braise, soy with mushrooms) taste far more savoury; aged and fermented foods add umami and mouthfulness |
| Overstated                | "Acid always fixes a flat dish" (check salt first); "fat makes everything taste better" (too much dulls brightness); "salt always at the end" or "always early" (both have uses, see 1.4); "a balanced dish needs all five tastes"                                                     |
| Myth                      | Taste-zone map of the tongue; "searing seals in juices" (it builds browning flavour, not a moisture seal); fixed "golden ratios" of tastes; precise multipliers for umami synergy (concentration dependent, the often quoted 7-8x comes from an industry-linked source)                |
| Single report (to verify) | A raw potato does not pull salt out of an over-salted soup; fix with dilution, a little acid or sweetness instead (to verify)                                                                                                                                                          |

### 1.4 Salting timing: conflict between reports

| Position                                                                                          | Source                                                                                 |
| ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Salt meat 45 minutes to overnight ahead; it seasons deeper and helps browning and juiciness       | Claude, Gemini (as pre-salting of proteins and sweating aromatics)                     |
| Evidence for universal early salting is mixed and food dependent; late salting gives more control | DeepSeek, Perplexity (season components as prepared, then reassess the assembled dish) |
| Dried beans: salting the soak or cooking water softens them faster and evenly                     | Gemini only (to verify)                                                                |
| Dried beans: early salt or acid can toughen skins                                                 | DeepSeek only (to verify)                                                              |

Default: staged seasoning (a little at each step, final taste check after assembly), salting large cuts of meat ahead when time allows, and for dried beans neither forbid nor demand early salt: add acid late and salt once the beans are close to tender (to verify the bean question).

## 2. Depth

### 2.1 Aromatic bases

Almost every tradition starts by cooking a few aromatics in fat. Gentle heat softens them, turns sharp sulfur notes round and sweet, releases sugars that later brown, and moves fat-soluble aroma into the fat that coats the whole dish. Store bases as dish-specific procedures, not interchangeable ingredient lists: when someone says "sofrito" ask which region.

| Base                       | Tradition                        | Typical parts                                                              | Home-cook note                                                                                             |
| -------------------------- | -------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Mirepoix                   | French                           | Onion, carrot, celery (about 2:1:1 by weight)                              | Sweated for pale stocks and sauces, browned for brown ones                                                 |
| Soffritto                  | Italian                          | Onion, carrot, celery, olive oil or butter, sometimes pancetta             | Slow, 10-20 minutes, until soft and sweet; the heart of ragù, bean dishes and soups                        |
| Sofrito / sofregit         | Spanish, Catalan, Latin American | Onion, garlic, tomato, peppers; recaito and culantro in Caribbean versions | Grated tomato cooked jammy; regional versions differ a lot                                                 |
| Holy trinity               | Cajun, Creole                    | Onion, celery, green pepper                                                | Often cooked into a dark roux                                                                              |
| Tadka / tempering          | South Asian                      | Whole spices, curry leaf, dried chili, asafoetida in ghee or oil           | Done first, last or both; on dal the tadka poured over at the end is what people remember                   |
| Onion-ginger-garlic masala | Indian                           | Aromatics fried to a paste before the spices                               | Cook until the oil separates                                                                               |
| Ginger-garlic-scallion     | Chinese                          | Aromatics in hot oil, seconds not minutes                                  | Burnt garlic turns bitter                                                                                  |
| Curry and spice pastes     | Thai, Malay, Indonesian          | Lemongrass, galangal, chili, shallot, garlic                               | Fry the paste until fragrant; raw paste tastes harsh; quick oil method and coconut-cream method both exist |
| Pepper-tomato-onion base   | West African                     | Peppers, tomato, onion, scotch bonnet                                      | Fry down until darker and the oil separates                                                                |
| Ras el hanout, chermoula   | Maghrebi                         | Blends of many spices, frequently fried with the onion                                     | A gentle tagine braise softens their edges                                                                        |
| Onion-paprika base         | Hungarian, Central European      | A lot of onion in lard or oil, sweet paprika                               | Paprika goes in off the heat; it scorches and turns bitter                                                 |
| Wat preparations           | Ethiopian                        | Slow-cooked onion, spiced fat                                              | Keep the stated sequence; do not import European browning                                                  |

### 2.2 Browning, fond, deglazing

| Topic              | Rule                                                                                                                                                                                               | Evidence     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| Maillard browning  | Needs a dry surface well above boiling point: pat meat dry, do not crowd the pan, brown in batches; wet crowded food steams grey                                                                   | strong       |
| Caramelisation     | Sugar-only reaction, bittersweet and buttery notes; "caramelised onions" are mostly Maillard plus some caramelisation                                                                              | strong       |
| How much to brown  | Browning part of the meat well beats browning all of it badly; in a delicate or pale dish (blanquette, poached chicken, steamed Cantonese dishes, miso soup, nimono) do not add browning by reflex | practitioner |
| Fond and deglazing | Browned residue is concentrated flavour; loosen it with wine, stock, vinegar or water (wine is optional); about a minute of work; acrid black residue is not "extra depth"                         | strong       |
| Onion honesty      | Say what the target is (softened, golden, deeply browned) and give realistic time; "caramelise in 5 minutes" is a failure                                                                          | practitioner |

### 2.3 Blooming and toasting

| Technique                                         | Rule                                                                                                                                                                                                                         | Evidence         |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| Bloom in fat                                      | Many spice aromas dissolve in fat; heat ground or whole spices briefly (roughly 30-60 seconds) in oil or ghee over medium-low heat until fragrant, then add liquid. Worth it for dal, curry, chili, mole, tagine, spice rubs | strong mechanism |
| Not universal                                     | "All spices must be fried" is too crude; some compounds are lost or scorched; skip for spices used only as a quiet background note                                                                                           | design           |
| Give an endpoint                                  | "Until fragrant, do not let it darken sharply" is better than a bare time                                                                                                                                                    | design           |
| Dry toasting                                      | Whole seeds, dried chiles and nuts gain roasted aroma; toast each separately and briefly (burnt chiles turn bitter); not worth an extra pan for a pinch that vanishes in a strong sauce                                      | moderate         |
| Burn risk                                         | Ground paprika, garlic and cumin turn bitter within seconds                                                                                                                                                                  | practitioner     |
| "Up to 10 times more flavour" when bloomed in fat | Test-kitchen figure for fat-soluble herbs; direction is sound, the multiplier is not (to verify)                                                                                                                             |

### 2.4 Reduction and layered seasoning

| Rule                                                                             | Detail                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reduction concentrates salt, sugar, acid, glutamate, gelatin and some bitterness | It also loses volatile aroma: reduce stock or wine early, add delicate herbs late; separate "concentrate" from "thicken"; a sauce that is already salty needs thickening or a ratio change, not more reduction                 |
| Layering has a purpose per layer                                                 | Early: salt, hard aromatics (thyme, bay, rosemary), tomato paste, miso, dried mushrooms for extraction. Late: acid, tender herbs, raw oils, zest for top notes. A sauce salted only at the end tastes salty on top, flat below |
| Two-stage spice or herb                                                          | Part early for depth, part late for brightness: finishing tadka on dal, gremolata on osso buco, raw herbs on pho, fresh coriander on a long braise                                                                             |
| Herb timing                                                                      | Hardy herbs (rosemary, thyme, bay) early; tender herbs (parsley, coriander, basil, dill) at the end                                                                                                                            |

## 3. Contrast and finish

### 3.1 Finishing toolkit

Rule: exactly one finishing element, adding what the dish lacks (brightness for a braise, crunch for a soft dish, richness for a lean one), taken from the same or a neighbouring tradition, and stated with when and where it goes ("scatter over each bowl just before serving").

| Finish                    | Adds                                  | Classic fits                                                                                                 | Caution                                                                                          |
| ------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Fresh herbs               | Volatile top notes, colour            | Parsley or dill in Central and Eastern Europe; coriander, Thai basil, mint on pho; herbs on Levantine dishes | Pick the herb of the tradition, not automatic parsley; respect diner aversions                   |
| Acid squeeze              | Lift after long cooking               | Lemon over tagine or fried fish, lime with pho and tacos, a dash of vinegar in lentil soup or goulash                      | Taste first; do not stack several sour finishes                                                  |
| Aromatic fat              | Fresh fat-soluble aroma, gloss        | Olive oil on beans, brown butter, chili oil, ghee tadka, sesame oil on namul                                 | Avoid an oily surface or a second source of richness                                             |
| Herb sauce                | Herb, acid, fat and salt in one spoon | Gremolata (osso buco), salsa verde, chimichurri, zhoug, chermoula, Frankfurter Gruene Sosse                  | Families of sauces, not interchangeable names; lemon zest gives aroma, not the sourness of juice |
| Compound butter           | Fat-carried aroma                     | Maitre d'hotel butter on steak or fish, garlic-herb, miso butter                                             | A separate prep may not pay off for one portion                                                  |
| Crunch                    | Fracture and sound                    | Toasted nuts or seeds, pangrattato, fried shallots, crispy onions, dukkah, sesame                            | Add at the last moment; disclose allergens; does not belong on every dish                        |
| Pickled or fermented item | Acid, salt, crunch, sometimes umami   | Pickled red onion, cornichons, kimchi, achar, encurtido, sauerkraut                                          | Do not combine pickle, citrus, vinegar sauce and sour dairy                                      |

### 3.2 Contrast rules

| Rule                                                                                 | Detail                                                                                                                                                                    | Evidence                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Texture and temperature change during the bite raise palatability (dynamic contrast) | Crisp over creamy, cold over hot, fresh over cooked, bright over rich. Influential proposal, not a controlled experiment; not a law that every dish needs crunch          | practitioner / theory             |
| Preserve contrast the dish already has                                               | Crisp roast-potato edges may need better execution, not a nut topping                                                                                                     | design                            |
| Monotony fatigues                                                                    | Pleasantness of an eaten food drops faster than that of uneaten foods, so a contrasting garnish keeps the last bite as good as the first; useful for one-pot comfort food | strong (sensory-specific satiety) |
| Texture is remembered better than richness                                           | Crispness and thickness are recalled more than fattiness; a texture contrast makes a dish more memorable than extra fat                                                   | moderate                          |
| Temperature contrast                                                                 | A cool yoghurt or herb sauce over something hot, a cold pickle beside warm tacos; consistent with the theory but less studied; never mandatory                                        | practitioner                      |
| Delivery                                                                             | Crumbs soften in liquid, tender herbs wilt under heat; keep wet and crisp parts apart                                                                                     | practitioner                      |
| Do not force a checklist                                                             | A Japanese clear soup needs no added fat or crunch just to tick a box                                                                                                     | design                            |
| Finishing-touch inflation                                                            | Three garnishes on a dish that needs one is a common failure                                                                                                              | practitioner                      |

### 3.3 Pairing: molecules are not a basis

| Point | Detail |
| --- | --- |
| Shared-compound "food pairing" is not a basis for any pairing | A recipe-network study found Western recipes tend to combine ingredients with shared aroma compounds while East Asian recipes tend to avoid it (Southern European also avoiding: Claude and Gemini only, to verify); that describes habits, not what tastes good. A small blind tasting rejected the theory (one report only, small proceedings paper, to verify). Reviewers call it discredited as a predictor |
| Why it fails | Shared compounds are often below threshold or not characteristic; concentration, fat, water, cooking and mixture effects change what is perceived; culture and familiarity dominate |
| What to use instead | (1) The dish's own flavour principle; (2) pairings established in the tradition or in curated practitioner books (Flavor Bible, Flavour Thesaurus: culinary experience, not science, mostly Anglo-American and European); (3) balance logic: fat with acid, sweet with salt or heat, soft with crunch |
| Role of chemistry | At most an idea generator; never rank or justify a pairing by "shares molecules" |
| Food-bridging (pairs linked through a chain of shared compounds) | Proposed as a complement; contested (to verify) |

### 3.4 Memorable versus merely competent

| Point | Detail |
| --- | --- |
| Execution before embellishment | A signature cannot rescue dry chicken, gritty lentils, scorched garlic or a too-salty sauce; test kitchens define great as reliability plus maximum flavour from technique, one clever fix per recipe |
| Formula | Familiar foundation + excellent execution + one distinctive element that supports the dish |
| Signature test | It can be named in one sentence and the dish still reads as itself; examples: roast chicken with preserved-lemon butter, lentil soup with crisp chili oil, rice bowl with a herb sauce, well-browned onions in a lentil-and-grain dish |
| Familiarity | Liking rises with exposure and follows an inverted U against novelty; neophobia is a stable trait, so a family recipe with an unfamiliar main ingredient risks refusal |
| Novelty dose: conflict | Copilot: about 80-90 percent familiar, 10-20 percent distinct. Gemini: 80/20 with no source. Perplexity: no sound basis for a numeric novelty allowance, tolerance depends on diner, presentation and what is familiar. Claude and DeepSeek give no number. Default: do not state a percentage; one deliberate deviation per dish, small, optional or served on the side where possible |
| Memory research | Peak and end effects for meals are weak; the worst moment predicts remembered enjoyment better than the best (Perplexity only, students, to verify). Practical consequence: remove conspicuous failures before adding a flourish |
| Test that separates | Liking now, remembering later and wanting to cook it again are different outcomes |

### 3.5 Refinement versus experiment

| Refinement (in scope) | Experiment (out of scope unless asked, then labelled) |
| --- | --- |
| Better technique for the same dish: salting ahead, browning, blooming | Swapping the defining technique (sous-vide paella, foam on goulash) |
| One finishing touch from the same or a neighbouring tradition | Fusion without culinary logic as a default (miso carbonara) |
| A spice the tradition already knows (marjoram and caraway in goulash, a little cinnamon in Greek tomato sauce, smoked paprika in a Spanish stew) | Specialty ingredients most home cooks cannot buy |
| Modest ratio changes (extra onion, a dash of vinegar) | Plated multi-part constructions, gels, spherification |
| A single signature element | Three or more new ideas in the same dish |
| Adds little burden or replaces an existing step | Adds several preparations |
| Dish keeps its name | Needs "inspired by" or a new name |

Minimum-effective-change rule (design): for every proposed improvement answer purpose (what weakness), fit (why this dish), cost (time, equipment, shopping, skill) and evidence base; prefer the smallest change that fixes the diagnosed problem. A mushroom gravy that lacks character first needs better mushroom browning, not miso, balsamic, smoked paprika, cream and truffle oil together.

## 4. Traditional dishes: identity core, regional variables, finesse levers

### 4.1 The model

| Layer | Definition | Rule |
| --- | --- | --- |
| Identity core | Defining ingredients, flavour principle, defining technique, texture, serving context and name | Change only with explicit labelling as a variation; if a change removes or replaces a core element, flag it or refuse |
| Regional or household variables | Places where authentic versions themselves differ (protein cut, souring agent, tempering spice, local pepper) | Choose one named version or state the regional scope; never merge national versions or call one "the" version |
| Finesse levers | Technique and finishing improvements that leave identity intact: better browning, correct salting stages, blooming, deglazing, a traditional finish, a well-made stock, freshly toasted spices | Use freely; borrow finishes from the same tradition first, then a neighbouring one |

Test: would a good home cook from that tradition recognise the dish and call it a very good version? Yes = refinement. "Interesting, but that is not X" = a variation, and it must be labelled as one ("paella-style rice with chorizo", "goulash with smoked paprika", "inspired by").

Recognised variation, functional substitution and reinterpretation are different things; all can taste good, none may be described as the same thing. Judge a substitution twice: does it keep the function (sourness, fat, salt) and does it keep the defining aroma? Say so ("keeps the sourness, changes the characteristic aroma").

General rules: do not push a tradition toward a Western default (cream in carbonara, sugar in dal, dropping fish sauce from pho because it is strong); stay humble about "authentic", since many canonical versions are recent codifications of living, regionally varied traditions; never write "authentic" on a modified recipe; keep local ingredient names and specifications rather than flattening them into a broad label.

### 4.2 Worked examples

| Tradition | Dish | Identity core | Regional variables | Finesse levers | Do not |
| --- | --- | --- | --- | --- | --- |
| Italian | Ragu alla bolognese | Meat-forward with little tomato, soffritto, wine, milk, long simmer (about two hours), served with tagliatelle; a 1982 Accademia reference recipe exists but is one codification (to verify details) | Cuts of meat, nutmeg, optional cream | Brown the meat properly, cook the soffritto slowly, salt in stages, good parmesan at the table | Garlic- and herb-heavy "spag bol" sold as authentic |
| Italian (Roman) | Carbonara | Guanciale (pancetta common), eggs or yolks, pecorino, black pepper, pasta water, no cream | Pecorino and parmesan blend | Render fat slowly, toast the pepper, emulsify with starchy water off the heat so the egg does not scramble | Add cream or peas |
| Italian | Osso buco | Braised cross-cut shank, regional sauce, gremolata association | Tomato or not | Tender meat, sauce consistency, gremolata made fresh | Different protein with unrelated sauce under the same name |
| Italian | Risotto | Rice texture, gradual cooking, starchy creaminess | Stock and flavouring | Herb oil, lemon zest, toasted hazelnuts as finish | Break the stirring-and-stock method |
| Spanish | Paella valenciana | Wide thin pan, no stirring once the rice is in, socarrat crust; survey of Valencian home cooks gives ten agreed core items (chicken, rabbit, flat green beans, garrofo beans, tomato, saffron, rice, water, salt, olive oil) (to verify) | Snails, rosemary, artichoke accepted; chorizo, peas, onion considered non-traditional | Brown the meat deeply, cook the sofrito with grated tomato and paprika, rosemary at the end | Call seafood rice "paella valenciana" (it is arroz de marisco) |
| German | Rouladen | Thin beef rolled around mustard, bacon, onion, pickle; browned and braised | Pickle and mustard type | Sear well, deglaze with red wine, pickle brine sparingly, finish gravy with cold butter | Skip the pickle: it is the built-in acid contrast |
| Central European | Goulash / gulyas | Lots of onion cooked down, sweet paprika off the heat, beef, caraway, marjoram | Hungarian gulyas is soupy, Austrian and German Gulasch a thick stew | Brown in batches, vinegar or lemon zest at the end, sour cream where regional | Scorch the paprika |
| French | Coq au vin / boeuf bourguignon | Wine braise, long cooking, mirepoix, lardons, bouquet garni | Mushroom treatment | Deglaze the fond fully, a splash of sherry vinegar or lemon-parsley at the end (Gemini example, to verify) | Skip browning |
| French | Potato gratin | Potato treatment, cooking medium, texture, regional version | Cream or stock, cheese or not | Even slices, proper seasoning, controlled browning | Treat bacon, cheese or spice as mandatory |
| Vietnamese | Pho | Clear beef or chicken broth, charred onion and ginger, star anise, cinnamon, clove, cardamom, fish sauce, rice noodles, table herbs, lime, chili | Beef cut, regional herbs | Char the aromatics, blanch bones for clarity, toast spices, fish sauce at the end | Thicken, add heavy soy or fusion garnish; the table herbs are the finish |
| South Asian | Dal | Lentils cooked soft with turmeric and salt, plus a tadka | Lentil type; southern tempering with mustard seed and curry leaf, northern with cumin, garlic and chili, Bengali with panch phoron; sour note from tamarind, kokum, tomato or lemon | Double tadka (start and sizzling at the end), lemon, fresh coriander | Turn it into generic lentil soup with curry powder |
| Chinese | Mapo tofu | Doubanjiang and Sichuan pepper define it (DeepSeek only, to verify) | Tofu type | Fry the paste until the oil turns red | Replace the defining pastes |
| Thai | Red or green curry | Paste character, coconut sauce, fish sauce, Thai basil | Brand saltiness of paste | Fry the paste properly (cracked coconut cream or quick oil method), finish with Thai basil and lime off heat; adjust final seasoning to the paste's salt | Change the defining aromatics without saying so |
| Japanese | Miso soup | Dashi, miso, modest garnish | Seasonal garnish | Good broth, add miso off the boil to keep its aroma | Cream, browned onions, crunchy topping |
| West African | Jollof rice | Rice cooked in a reduced tomato-pepper-onion base with stock, thyme, bay; scotch bonnet; Nigerian, Ghanaian and Senegalese versions are distinct (Senegal's ceebu jen is a fish-and-rice dish on UNESCO's list since 2021, to verify) | National style, smoky party-jollof crust | Fry the base until darker and the oil separates; optionally char the peppers first (Gemini only, to verify) | Merge national versions or call one "the" jollof |
| West African | Groundnut (peanut) stew | Peanut richness, regional spice base | Protein and vegetables | Herb garnish, a crunch element, bright acidic side (Copilot only, to verify) | Generic "curry" |
| East African | Injera and wat | Teff fermentation; stew onion and spiced-fat sequence | Stew choice varies widely | Follow the intended sequence and endpoints | Call generic curry equivalent |
| Latin American (Mexican) | Mole | Toasted dried chiles, seeds or nuts, spices, often a little chocolate, fried as a paste then simmered | Chile mix by region | Toast each chile separately and briefly, fry the paste in lard or oil until it darkens, balance with salt and a touch of sugar | Burn the chiles |
| Latin American | Beans (Mexican, Brazilian feijoada) | Bean character, regional aromatics; feijoada: black beans, pork, bay | Pork cuts, cooking liquor, herbs | Tender beans, well-seasoned broth, pickled onions, herb salsa, citrus finish | Insist lime, coriander, cheese and chili all appear |
| Middle Eastern | Hummus | Chickpeas, tahini, lemon, garlic | Garnish | Chili oil, pine nuts, herbs, browned-butter nuts | Drop the tahini |
| Middle Eastern | Shakshuka | Eggs poached in spiced tomato-pepper sauce | Harissa, preserved lemon | Bloom spices in oil, reduce the sauce until jammy before adding eggs, herbs and yoghurt or crumbled cheese on top | Add eggs to thin sauce |
| Middle Eastern | Mujaddara | Lentils, rice or bulgur, prominently cooked onions | Grain | Cook the onions properly, good grain-lentil texture | Cream sauce |
| Maghrebi | Tagine | Slow braise, spice blend, sweet-sour-salty contrast such as preserved lemon and olives or prunes and almonds | Vegetables and meat by season | Gentle heat, preserved lemon near the end, toasted almonds or sesame on top (Gemini adds dry-toasted spices, bloom 45 seconds, sumac, to verify) | Rush the braise |

## 5. Review tools

### 5.1 Draft-recipe review checklist

Run in this order; fix the first failing group before polishing later ones. Take the unticked items into the rewrite.

| Group | Check |
| --- | --- |
| A. Identity | Is the identity core intact (defining ingredients, flavour principle, technique, name)? Are variations labelled as variations? Are modifications culturally plausible? |
| B. Main component | Will the main component work (doneness, tenderness, hydration, crispness)? Is the technique matched to cut, thickness and desired texture? |
| C. Seasoning | Is salt given as concrete amounts or a starting amount plus a tasting cue, at several stages, with salty ingredients accounted for? Is there a final taste-and-adjust step? Is there an acid source in the base or as a finish? An umami source suited to the cuisine? Does fat have a job? Is sweetness only balancing acid, bitterness or heat? Is heat deliberate and adjustable? |
| D. Depth | Is there a base suited to the tradition, cooked long enough (minutes for soffritto, seconds for Chinese aromatics) but not burnt? Spices bloomed or toasted where the cuisine does it? Browning where it fits, with dry food, no crowding, deglazed fond? Reduction only where flavour should concentrate? |
| E. Contrast and finish | Is there at least one contrast (texture, temperature, fresh versus cooked, rich versus bright)? Exactly one finishing element that fits the tradition, with when and where it goes? Does it survive service? |
| F. Signature and restraint | Can the signature touch be named in one sentence? Is it optional or adjustable for cautious eaters? Does every ingredient have a job (remove what changes nothing)? Does the dish stay recognisably itself? Would a home cook from the tradition approve? |
| G. Practicality | Normal supermarket in the user's region, with substitutions? Equipment, time, number of pans realistic? Honest times plus cues? Quantities, order and yield consistent? Allergens and safety treated as hard constraints, not flavour trade-offs |

### 5.2 AI-recipe failure modes and fixes

| Failure mode | Symptom | Fix |
| --- | --- | --- |
| Vague or late-only salt ("salt and pepper to taste") | Flat dish, decisions pushed onto the cook | Salt at each stage with a starting amount; name salty ingredients; final check after assembly |
| Salt accumulation | Stock, cheese, fermented sauce and reduction each salted separately | Season the assembled dish; make final salt conditional on the salty ingredients |
| Missing acid | Heavy braises and creamy dishes taste dull | Wine or tomato in the base, vinegar or citrus at the end; test a small sample; acid is not compulsory in every dish |
| Acid stacking | Several reasonable sour finishes together | One primary acid, others optional |
| Missing umami in meatless dishes | Thin, "something is missing" | Tomato paste, mushrooms, soy, miso, parmesan, kombu; pick what fits the cuisine |
| Automatic umami additions | Miso or parmesan redirects the dish | Identity-compatible source or none |
| Too many competing ingredients | Many spices, herbs, sauces; muddy | Cuisine's flavour principle plus one signature; every ingredient needs a role; limit primary spices to a few coherent ones |
| Technique-dish mismatch | Browning a blanquette, stirring paella, cream in carbonara, long simmer for delicate fish | Check against the identity core; tie technique to the cut and desired texture; give doneness cues |
| Bland safe defaults | Garlic powder, generic "Italian seasoning", same onion-garlic-paprika everywhere | Use specific, cuisine-appropriate aromatics and spices; keep heat with an adjustable dial |
| No browning or crowded pan | Grey meat, weak sauce | Dry the food, brown in batches, deglaze; if the dish is meant to steam or simmer, say so honestly |
| Raw-tasting spices or pastes | Harsh, dusty flavour | Fry spices briefly in fat; cook pastes until they smell cooked and the oil pools |
| Burnt spices or garlic | Bitter | Give a sensory endpoint and a scorch warning, not only a time |
| Unrealistic timing | "Caramelise onions in 5 minutes" | Honest times with colour, texture and smell cues |
| Reduction as universal rescue | Salty, bitter, aroma-poor sauce | Diagnose dilution, thickness or seasoning first |
| No contrast | One-note, soft, monotone | Crunchy topping, fresh herb, pickle or sharp sauce; preserve contrast already present |
| No finishing step, or decorative garnish | Recipe ends at "serve hot", or garnish changes appearance only | One explicit finish that changes flavour or texture; state its purpose or drop it |
| Over-garnishing and fusion creep | Gochujang, truffle and feta on a traditional dish | One finish from the same or a neighbouring tradition; label any fusion |
| Crunch or herbs added at the wrong time | Soggy topping, brown herbs | Add crunch at the bowl; tender herbs last |
| Novelty on novelty | Several unfamiliar changes at once | Keep the base recognisable; one optional variation |
| Cultural pastiche | Italian dish with soy and coriander | Check core elements; label fusion |
| False equivalence in substitutions | Matching saltiness or acidity taken as matching flavour | Say what is kept and what changes |
| Inauthentic claims | "Authentic" on a modified recipe | "Inspired by" or "variation" wording |
| Unnecessary complexity | Chef-level reductions on a weeknight dish | Constrain by equipment, time, pans; remove low-return steps or mark them optional; a "weeknight" and a "project" version where useful |
| Untested precision | Exact numbers that imply a test happened | Ranges, doneness cues, honest testing status |

## 6. Evidence notes

| Topic | Strength and caveats |
| --- | --- |
| Taste interactions | Mostly from model solutions; direction holds in dishes but is less quantified. Mixtures usually suppress each other; enhancement appears mainly near threshold |
| Umami synergy | Robust; exact multipliers are concentration dependent, the 1:1, 7-8x figure is from an industry-linked source (Claude only) |
| Kokumi | Receptor-level evidence from a trained-panel study by researchers affiliated with a seasoning maker; do not label dishes "kokumi" without evidence (Perplexity) |
| Fat and aroma | Strong, but the effect in the nose is smaller than headspace tests suggest; fat can slow release |
| Dynamic contrast | Theory (1993), widely cited, not a controlled experiment; temperature contrast less studied |
| Food pairing | Network study descriptive; the direct tasting test is small and from proceedings (to verify); Spence's review calls the hypothesis discredited as a predictor |
| Liking and novelty | Inverted-U, mere exposure and neophobia are well studied but in Western, often student, samples; a cross-country study tested food names, not tasted dishes |
| Authenticity | Many reference recipes and ingredient lists are recent codifications; household variation is legitimate |
| Practitioner books | McGee, Nosrat, Lopez-Alt, CIA, Hazan, Jaffrey, Presilla and test kitchens are authoritative on technique, not on universal preference; Flavor Bible and Flavour Thesaurus are curated experience |
| Reports disagree on | Salting timing and dried beans (1.4); acid as universal fix (1.3); numeric novelty dose (3.4); Gemini's mechanistic claims about acid breaking lipid emulsions and sodium blocking bitter receptors are stated more strongly than other reports (to verify) |
| Coverage | Six reports merged: Claude, Consensus, Copilot, DeepSeek, Gemini, Perplexity. Consensus is shallow (taste science, checklist) and contributes mostly agreement on cross-modal salt, umami-nucleotide synergy and contrast |
