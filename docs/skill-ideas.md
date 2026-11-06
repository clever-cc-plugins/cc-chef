# cc-chef: skill ideas (working note)

Captured during brainstorming on 2026-11-01. This is not a design. The plugin design starts once the research in `docs/research/` is in (see `docs/research-prompts/README.md`).

## Status (2026-11-02)

- Done: brainstorming on intent and scope; five research prompts in `docs/research-prompts/`; research results in `docs/research/`.
- Done: plugin design, approved by the owner on 2026-11-02: [docs/superpowers/specs/2026-11-02-cc-chef-design.md](superpowers/specs/2026-11-02-cc-chef-design.md). It supersedes this note wherever they differ.
- Next: implementation plan (superpowers:writing-plans), then build per the [cc-plugin-repo-guideline](https://github.com/clever-cc-plugins/marketplace/blob/main/docs/cc-plugin-repo-guideline.md).
- 2026-11-04: phase 1 built on `feat/phase-1-core` (six skills, knowledge base, recipe format, `recipe_tool.py`); next is the phase 2 plan for Tandoor.
- 2026-11-06: phase 2 (Tandoor) merged as v0.2.0 (PR #4): upload, in-place rework and `tandoor-food-cleanup`, tested against a fake server and checked against a live Tandoor 2.7.2 test instance, which has since been removed. No further phase is planned; the design's non-goals list the candidates, Mealie being the most likely next adapter.

## Intent

A public plugin in the clever-cc-plugins marketplace for creating, adapting, and improving recipes. It grew out of two Claude.ai project prompts the owner used. Their output was doable but lacked culinary finesse.

**Quality bar:** grounded, cookable everyday food — comfort food, traditional fare, rustic home cooking — with one or two deliberate touches (a spice, a finishing element, a contrast) that make a dish worth remembering. Not experimental, not star-chef complexity. Grounding ideas in researched real recipes is part of how it gets there.

## Ideas to carry into the design

- **Language-agnostic.** Works in any language; output language is a user preference.
- **Recipe ideas from different inputs:** a description of what the person feels like, an ingredient list (typically: what's in the fridge and needs to be used), or a photo of the fridge or pantry. Open question: does photo analysis need a specific model (e.g. Opus) for reliable recognition? See research prompt 2, section 7.
- **Flow carried over from the Claude.ai prompts:** a few short ideas first (up to five, quick, few extra ingredients), the person picks one, then the full recipe. Full recipe with servings up front, sections for ingredients / preparation / cooking, weights preferred, oven details, closing notes on serving, side dishes, and drinks. These are the owner's defaults, not necessarily the plugin's.
- **Context and preferences** following the context-management approach of the other clever-cc-plugins (a `## Context files` table in the user's CLAUDE.md; skills use registered context if present and work without it). Examples: ingredients to prefer or avoid, language, preferred recipe structure, units of measurement.
- **Onboarding skill** to set up those preferences and register existing context files (e.g. the owner's food list with cholesterol, iron, and fiber values, kept in their personal assistant repo).
- **Dietary guidelines are opt-in.** Skills apply registered guidelines when present and work fine without. Users without guidelines can get help creating them — only if they ask for it. Clear statement that the plugin supports healthier eating and does not replace medical or dietetic advice.
- **Adapting recipes for guidelines:** swap hindering ingredients for helpful ones and point out how a swap changes the preparation (e.g. whole-grain flour absorbs more liquid).
- **Reworking found recipes:** take a recipe from a magazine, cookbook, or website and restructure it to match the user's configured preferences.
- **Export:** save recipes in a format ready to import into recipe management apps (Tandoor, ManageMeals, Recipya, kitshn, and others). See research prompt 5.
- **Possibly: managing recipes** (mentioned as "perhaps" — scope to be decided in the design).

## Inputs from the owner

- `project-prompt-1.md` — general recipe-creation prompt (Claude.ai project).
- `project-prompt-2.md` — health-focused variant (LDL/HDL, fiber, toddler iron; Mediterranean and DASH patterns) using `Lebensmittelliste.csv` as context.
