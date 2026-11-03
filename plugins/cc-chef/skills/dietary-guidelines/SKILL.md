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

## Step 1: Screening, before any content

Screening runs first, before any guideline content is drafted. Ask who the guideline is for (the household members, with life stage and country; reuse `Household` from the preferences if registered). Then screen each member with the referral conditions in section 6.1 of the imported nutrition file: medicines and food interactions, kidney disease, diabetes on insulin or sulfonylureas, anticoagulants, pregnancy and any complication, eating-disorder history, and allergies or anaphylaxis. Ask it as one plain question per topic group, and tell the user they can skip any of it.

A referral condition may also come up later, in research results or in passing. The rule applies at any point of the conversation.

## Step 2: Referral conditions

For a member with a referral condition, stop writing therapeutic rules for that member:

1. Say the limit once, calmly: this skill cannot write rules for that condition, and a doctor or registered dietitian should.
2. Offer to record limits the clinician has set, verbatim as the user reports them, as hard constraints with who set them and when (section 6.2). Never extend, round, adjust or "optimise" them, and never set limits of your own.
3. Offer an everyday-healthy guideline built on the shared core only when section 6.2 says that is safe for this condition. Eating-disorder history: no targets, calories, macros or food lists; use neutral language and signpost specialist help.
4. Never suggest a potassium-based salt substitute to anyone who has not been screened, and never at all with kidney disease, potassium-sparing diuretics, ACE inhibitors or ARBs.

Other household members proceed normally. If the user asks for a therapeutic guideline in a listed condition, section 6.2's last row applies.

## Step 3: Gather and draft

Build the guideline from an interview, from research results, or both. `$ARGUMENTS` or the user may supply research results as a file path or pasted text (for example the output of `/cc-chef:research-prompt`).

- Interview: for each member, only what the six parts of `guideline-template.md` need: life stage and age band, country, allergies with severity and cross-contact, intolerances, religious or ethical exclusions, the clinician-set limits of Step 2, preferences. No diagnoses or medical values beyond that.
- Research results: read them, then convert them into the template. Keep the evidence grading, mark single-source claims `(to verify)`, and name the origin of every target. Screening and referral limits still apply in full: researching a renal diet does not make this skill write one. A research claim that breaks the myths filter (section 7.2) or the claims to avoid (section 7.1) is left out and mentioned.
- Content defaults: the convergent healthy-pattern core (section 1.2), expressed in the member's own cuisine. Targets come from the member's official guide or a clinician, never from invention, as ranges over a day or week (target hygiene, section 5.1). Target LDL, never "raise HDL" (section 2.1). Where the US Dietary Guidelines 2025-2030 diverge (protein, full-fat dairy, animal fats), follow WHO, AHA/ACC and the European guides and say so in the guideline (section 1.3).
- Automatic safety rules: reference the rule in `food-safety.md` and section 3 of the nutrition file; do not restate limits.
- Households: apply base plus branch (section 5.2). Put the strictest hard and safety rule in a short "Shared base" note at the top of the household file, and each person's soft targets in their own section. Never average members into a fictional one and never apply one person's targets to a child.
- Wording is descriptive ("supports", "fits"), never a health claim (section 7.1).

Follow the checklist in section 9 of the nutrition file before presenting.

## Step 4: Check against the preferences

The guideline file is the detailed source of hard constraints. Compare its hard constraints with the preferences' `Allergies and hard exclusions`. When they disagree, name the difference and offer to align both, the guideline, the preferences or neither. Never align silently, and never edit the preferences without a yes.

## Step 5: Write and register

1. Show the draft in the output language and ask for corrections before writing.
2. Propose `context/dietary-guidelines.md` (the user may change it): one file with a section per household member, created from `guideline-template.md` (next to this SKILL.md), headings in English and values in the output language. Leave nothing as a placeholder; write "(none recorded)" or "(none triggered)" where a part is empty. If the path exists and is not the registered guideline, add `-2`, `-3`; never overwrite. For an update, edit only the changed sections and the review date.
3. Register in the `## Context files` table of the right `CLAUDE.md` (create the section if missing), columns `Label | File | Summary`, with the Summary "Dietary guidelines, allergens, hard constraints, nutrition targets". Do not add a duplicate row for a file already registered. Do not hand-edit the Key Config Files table.

## Step 6: Disclaimer, once

Show the health disclaimer once per run, in the output language and plain words, covering the six points of section 7.3. Do not repeat it elsewhere in the run or write it into the guideline.

Then summarise in a few lines what was written, what was left out and why, and where the review triggers are. End with the contract's Step 5 (feedback and learnings), tag `[cc-chef:dietary-guidelines]`.
