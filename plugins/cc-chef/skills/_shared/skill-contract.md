# cc-chef Skill Contract — Shared Reference

Every cc-chef skill follows the same step sequence. A SKILL.md references this file instead of restating it, so the steps cannot drift from skill to skill. A skill documents only its own specifics: its own work (Step 3), the files it reads or writes, and any extra context it looks for.

## Language, address form and tone

- Output language: the `Output language` field of the preferences, else the language of the conversation. Skill instructions are English; everything a skill shows or writes for the user is in the output language.
- German: address the user with "du" unless `Address form` says otherwise.
- Tone: clear, conversational, honest. No hype or advertising words, no flattery. Ask when a request is ambiguous; otherwise use sensible defaults.
- Health wording is descriptive, never a health claim. The health disclaimer appears only in `chef-onboarding` and `dietary-guidelines`, never on every recipe.

## Household: base plus branch

- A household with an infant or toddler gets base plus branch automatically, even without a registered guideline. This holds when the child is in `Household` and when the request names one, with or without preferences on file.
- Cook one shared base. Take the child's portion off before salt, chilli or other heat, honey, whole nuts or other restricted items go in, and say so in the method at that step.
- Until that split, the shared base gets no salt or salty seasoning (soy sauce, stock cube) at any stage, which overrides salting in stages for the base. Build it with aromatics, acid and herbs, and stage the salt in the others' portion after the split.
- Check the child's portion for texture and bones too.
- Apply the life-stage rules in `nutrition-and-guidelines.md` (sections 3 and 5.2) and `food-safety.md` (section 7) rather than restating them. A vulnerable member also means the stricter end of every food-safety range (`food-safety.md` section 1, rule 7).

## Finding context

Context files are Markdown documents registered in the `## Context files` table of a `CLAUDE.md`. The project may have more than one `CLAUDE.md` and its own `context/`-like folders, so never assume a single root file:

```bash
find . -name 'CLAUDE.md' -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
find . -type d -iname 'context' -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
```

For each `CLAUDE.md` found, read its `## Context files` table. Rows have three columns: `Label`, `File`, `Summary`. Match context by the Summary column (semantic match), never by label or filename:

| Context                     | Summary describes                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| Cooking preferences         | cooking preferences, units, language, household, recipe target, save folder                  |
| Personal dietary guidelines | a household member's dietary guideline: targets, limits, allergens, foods to favour or avoid |
| Food list                   | per-food nutrient or suitability values (for example iron, fibre, cholesterol suitability)   |

A food list registered by the user takes precedence over generic nutrient data.

## The sequence

0. **Recall learnings** (silent): read `.claude/learnings.md` if present, across all plugin tags. Apply relevant observations. Never announce this step; surface nothing unless it changes behaviour.
1. **Load context**: enrichment, never gating. Read the preferences, any registered guidelines and food lists, matched by Summary. If nothing matching is registered, do not block and do not interrogate: ask only what the task cannot proceed without (for example servings) and use defaults for the rest. Hard constraints are checked before any idea or recipe is shown, even when no guideline is registered. Their sources are the preferences' `Allergies and hard exclusions` field or allergies and exclusions named in the request, the `Household` life stages or life stages named in the request (applying the life-stage rules in `nutrition-and-guidelines.md`) and registered guidelines. A conflicting idea is never offered, or is adapted and says so. They are never relaxed for flavour.

   In every recipe-producing skill, apply the referral behaviour of `nutrition-and-guidelines.md` sections 6.1 and 6.2, with no disclaimer added. A request for a calorie, weight or carbohydrate-for-insulin target, or for a renal or other condition-specific diet, gets no such target: say so briefly, refer to a doctor or registered dietitian, and still offer to cook a normal dish.

2. **Framing**: before the first substantive question or result, state in one line whether the run is personalised and with which files ("Personalised with `context/cooking-preferences.md`.") or runs on defaults ("No cooking preferences on file, running with defaults. `/cc-chef:chef-onboarding` sets them up."). In the output language. `chef-onboarding` is exempt: it has nothing to personalise with yet.
3. **The skill's own work**: as described in the SKILL.md.
4. **Output and save or export**: present the result in the output language. A skill that produces a recipe does not save or export it itself: it hands the recipe to `export-recipe`, which saves it to the preferences' `Save folder` and converts it for the preferences' `Recipe target`. Never overwrite an existing Markdown recipe file; saving a recipe must work even without `python3` (the Markdown file is still written, and the skill says that validation and JSON-LD or Paprika export are unavailable).
5. **Feedback and learnings**.

### Step 5: Feedback and learnings

Auto-store phase. Before asking for feedback, review the run. For each qualifying observation, append one tagged line to `.claude/learnings.md` (create it with the standard header if missing):

```text
[cc-chef:<skill>] <concise observation> — <YYYY-MM-DD>
```

Qualifies: recurring preferences not already in the context files (for example "always wants the oven temperature in Celsius and Fahrenheit"); corrections the user made. Does not qualify: standard behaviour applied without deviation; facts already in context files or `CLAUDE.md`; facts equivalent to an existing entry under any plugin tag. When in doubt, skip.

Check for the file before appending: `ls .claude/learnings.md 2>/dev/null && echo "exists" || echo "missing"`. Standard header when creating it:

```markdown
# Learnings

Corrections and feedback collected during sessions.
Entries are tagged by skill and dated.

---
```

Explicit feedback. After the auto-store phase, ask once, in the output language: "Does this work for you? Any corrections, or press Enter to finish."

- If the user corrects something: append it as a tagged entry under the same criteria and confirm how many learnings were saved.
- If the user confirms or skips: if entries were auto-stored, confirm that, then finish. If nothing was stored, finish without comment.
