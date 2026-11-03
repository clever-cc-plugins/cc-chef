---
name: dietary-guidelines
description: >
  Use this skill when the user wants a personal dietary guideline that the other cc-chef skills apply: allergens, hard constraints, safety rules for a child or pregnancy, and everyday nutrition targets for each household member. Opt-in only. Invoke when the user says "make me a dietary guideline", "write dietary guidelines for my family", "record my allergies and nutrition targets", "turn this research into a guideline", "Ernährungsrichtlinie für meine Familie erstellen", or "update my dietary guideline". Accepts research results (a file path or pasted text, for example from /cc-chef:research-prompt) as input. Do NOT use it for general cooking preferences such as language, units, equipment or tastes (use chef-onboarding), or to get a research prompt (use research-prompt).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[optional: path to research results or an existing guideline to convert or update]"
---

@../\_shared/nutrition-and-guidelines.md **Read when:** screening (section 6), drafting any part of a guideline (sections 1-5), choosing wording (section 7) and showing the disclaimer (section 7.3)

@../\_shared/food-safety.md **Read when:** filling "Automatic safety rules" for a toddler, infant, pregnant or older-adult member

# Dietary Guidelines

This skill drafts an opt-in personal guideline context file and registers it. It follows `../_shared/skill-contract.md` (language, address form, tone and the step sequence); the steps below are its own work (Step 3 of the contract). Step 4 of the contract (output, save or export) here means writing and registering the guideline, not a recipe.

Ask one question at a time, offer a default where one makes sense, and wait for the answer. Never read anything under `docs/owner-inputs/`. Record only what the guideline needs; health details are sensitive.

## Step 1: Disclaimer, once

The user has opted in by asking for this skill. Show the health disclaimer once per run, now and before screening, so a run that ends at a referral still shows it. Use the output language and plain words, covering the six points of section 7.3. Do not repeat it later or write it into the guideline.

## Step 2: Screening, before any content

Screening runs before any guideline content is drafted. Ask who the guideline is for (the household members, with life stage and country; reuse `Household` from the preferences if registered). Then screen each member, one plain question per topic group, and tell the user they can skip any of it. Screening topics include medicines and food interactions, kidney disease, diabetes on insulin or sulfonylureas, anticoagulants, pregnancy and any complication, eating-disorder history, allergies or anaphylaxis, a child's faltering growth or feeding refusal, alarm signs (unintended weight loss, trouble swallowing, blood in stool), and requests for a medical diet or supplements, plus the other triggers in section 6.1 of the nutrition file.

A referral condition may also come up later, in research results or in passing. The rule applies at any point of the conversation. Not every screening topic is a referral condition: allergies without anaphylaxis, without multiple allergies in a child, without uncertain reactions and without a proposed home food challenge, and uncomplicated pregnancy, need no referral. They are handled by hard constraints and safety rules. The allergy guards of section 6.2 (never test tolerance, never accept "may contain", never guarantee allergen-free, ask to confirm labels) apply to every allergy, referred or not.

## Step 3: Referral conditions

For a member with a referral condition in section 6.1, apply that condition's row in section 6.2, both columns: what the skill does and what it never does. In particular:

1. Say the limit once, calmly, and point to the right professional (doctor, registered dietitian or pharmacist, as the row fits).
2. A referred member still gets Profile, Hard constraints, Automatic safety rules and Review triggers. Only the soft targets are withheld or limited, exactly as the row says. A referred pregnant member keeps every pregnancy safety rule and hard constraint.
3. Offer to record limits the clinician has set, verbatim as the user reports them, as hard constraints with who set them and when. Never extend, round, adjust or "optimise" them, and never set limits of your own.
4. Medicine-related food rules (section 6.2: grapefruit, steady vitamin K intake for vitamin K antagonists only, such as warfarin and phenprocoumon, since DOACs have no comparable food rule; potassium salts) are written as hard constraints for any member screened positive, even when the user gives no clinician numbers. For a medicine-interaction trigger such as a statin, flag the interaction (grapefruit) and refer the interaction question to the pharmacist or prescriber; the member keeps the everyday core and the graded levers of section 2.
5. Eating-disorder history: neutral language, no targets, calories, macros, food lists or body size; signpost specialist help.
6. Potassium-based salt substitutes follow the screening gate in section 2.4: never for pregnancy, children, kidney disease, potassium-sparing diuretics, ACE inhibitors, ARBs or potassium supplements, and never when any answer is unknown. At most an optional adult branch, never the shared base. If the gate is not clear, do not mention them.

For a trigger without its own row in section 6.2 (a child's faltering growth or feeding refusal, cancer treatment, liver or pancreatic disease, malabsorption, MAOIs, immunosuppressants): decline therapeutic rules, refer, and apply the last (general) row.

Other household members proceed normally. If the user asks for a therapeutic guideline in a listed condition, the last row of section 6.2 applies.

## Step 4: Gather and draft

Build the guideline from an interview, from research results, or both. `$ARGUMENTS` or the user may supply research results as a file path or pasted text (for example the output of `/cc-chef:research-prompt`).

- Interview: for each member, only what the parts of `guideline-template.md` need: life stage and age band, country, allergies with severity and cross-contact, intolerances, religious or ethical exclusions, the clinician-set limits and medicine-related rules of Step 3, preferences. No diagnoses or medical values beyond that.
- Research results: read them, then convert them into the template. Keep the evidence grading, mark single-source claims `(to verify)`, and name the origin of every target. Screening and referral limits still apply in full: researching a renal diet does not make this skill write one. Leave out and mention anything that breaks the myths filter or the claims to avoid (section 7), and any supplement dose or medicine timing.
- Content defaults, for members without a referral or within what their section 6.2 row allows: the convergent healthy-pattern core (section 1.2), expressed in the member's own cuisine. For a referred member, nothing beyond that row; for kidney disease, never "more legumes", potassium-rich foods or protein for health. Targets come from the member's official guide, never from invention, as ranges over a day or week (target hygiene, section 5.1). Target LDL, never "raise HDL" (section 2.1). Where the US Dietary Guidelines 2025-2030 diverge (protein, full-fat dairy, animal fats), follow WHO, AHA/ACC and the European guides and say so in the guideline (section 1.3).
- No calorie, weight, carbohydrate-for-insulin or renal targets for anyone, whatever their origin. A clinician-set figure is recorded verbatim as a hard constraint only, never as a soft target. Soft targets with origin "user" are limited to non-therapeutic ones (frequency or food-group goals).
- Automatic safety rules: reference the rule in `food-safety.md` and section 3 of the nutrition file; do not restate limits.
- Households: apply base plus branch (section 5.2). The `## Shared base` block at the top of the file holds every hard constraint and safety rule of anyone at the table; each person's soft targets go in their own section. Never average members into a fictional one and never apply one person's targets to a child.
- Wording is descriptive ("supports", "fits"), never a health claim (section 7.1).

Follow the checklist in section 9 of the nutrition file before presenting.

## Step 5: Check against the preferences

The guideline file is the detailed source of hard constraints. Compare its hard constraints with the preferences' `Allergies and hard exclusions`. When they disagree, name the difference and offer to align both, the guideline, the preferences or neither. Never align silently, and never edit the preferences without a yes.

## Step 6: Write and register

1. Show the draft in the output language and ask for corrections before writing.
2. Propose `context/dietary-guidelines.md` (the user may change it): one file with a section per household member, created from `guideline-template.md` (next to this SKILL.md), headings in English and values in the output language. Leave nothing as a placeholder; write "(none recorded)" or "(none triggered)" where a part is empty. If the path exists and is not the registered guideline, add `-2`, `-3`; never overwrite. For an update, edit only the changed sections and the review date.
3. Register in the `## Context files` table of the right `CLAUDE.md` (the root, or the most specific nesting that applies; create the section if missing), columns `Label | File | Summary`:

   ```markdown
   | Label              | File                            | Summary                                                                                  |
   | ------------------ | ------------------------------- | ---------------------------------------------------------------------------------------- |
   | Dietary guidelines | `context/dietary-guidelines.md` | Dietary guidelines, allergens, hard constraints, nutrition targets, per household member |
   ```

   Do not add a duplicate row for a file already registered. Do not hand-edit the Key Config Files table.

Then summarise in a few lines what was written, what was left out and why, and where the review triggers are. End with the contract's Step 5 (feedback and learnings), tag `[cc-chef:dietary-guidelines]`.
