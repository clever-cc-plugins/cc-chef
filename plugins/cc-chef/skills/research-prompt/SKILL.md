---
name: research-prompt
description: >
  Use this skill when the user wants a ready-to-paste research prompt for a "deep research" AI tool (Claude, ChatGPT, Gemini, Perplexity, DeepSeek or similar) about a diet, an intolerance, a condition-related eating pattern, a cultural or religious food practice, or a cooking constraint. Invoke when the user says "give me a research prompt for a low-FODMAP diet", "write a deep research prompt on histamine intolerance", "I need to research halal cooking before I set up guidelines", "research prompt for a gluten-free kitchen", or "Recherche-Prompt für eine Ernährungsform". It produces only the prompt text: it runs no research, calls no tool and saves nothing. Do NOT use it to write the guideline itself from research results (use dietary-guidelines).
allowed-tools: Read, Write, Bash
argument-hint: "[optional: diet, intolerance, practice or constraint to research]"
---

@../\_shared/nutrition-and-guidelines.md **Read when:** building the prompt, to keep it inside the boundaries of sections 6 and 7

# Research Prompt Generator

This skill produces one vendor-neutral prompt the user pastes into the deep-research feature of any AI tool. It runs no research, calls no tool or API, saves nothing and does not say where the user stores the result. No tool-specific phrasing and no "save this to context/" instructions inside the generated prompt. It follows `../_shared/skill-contract.md` (language, address form, tone and the step sequence); the steps below are its own work (Step 3 of the contract). Steps 1 and 2 of the contract are light here: read the preferences only for the output language and country; no personal data goes into the prompt. Step 4 of the contract does not apply: nothing is saved or exported.

## Step 1: Gather the topic

If `$ARGUMENTS` contains a topic, use it. Otherwise ask one question: "Which diet, intolerance, eating pattern, food practice or cooking constraint do you want researched?" Wait for the answer.

## Step 2: Refine scope (optional)

Ask once, offering a default: "Any specific angle, such as a life stage, a country, or a sub-question, or should I keep it a broad, practical overview of [topic]?" Fold a specific angle into the prompt as explicit coverage points. Without one, use the broad framing. If the topic is a medical condition, keep the prompt about everyday cooking and food choices, never about dosing, supplements or treatment.

## Step 3: Generate the prompt

Write the prompt in English unless the user wants the research in another language or country context; then name that context in the prompt. Structure:

- A role framing suited to the topic, for example "You are a research analyst on everyday dietary patterns...", naming no AI tool or vendor.
- The topic, scope, country or life-stage context and any exclusions from Step 2.
- A request for practical cooking guidance under headers: foods to prefer, limit and avoid; swaps and how each swap changes preparation (method, time, texture, seasoning); hidden sources of the restricted item in common products and dishes; safety notes (who it matters for, interactions with life stages or medicines, and when to see a doctor or registered dietitian).
- Evidence grading: for each recommendation, who recommends it (official guide, clinical society, trial, expert opinion), how certain the evidence is, and a mark for claims resting on a single source.
- Credible, verifiable sources throughout, with in-text citations and a source list in APA style at the end.
- Output as Markdown.

## Step 4: Present the prompt

Present it in a single delimited copy-paste block, in this form:

```
─────────────────────────────────────────────
Research prompt: <topic>
─────────────────────────────────────────────
<the generated prompt text>
─────────────────────────────────────────────
```

Follow it with one line, in the output language: "Paste this into the deep-research feature of whichever AI tool you use. To turn the result into a guideline the cc-chef skills apply, run `/cc-chef:dietary-guidelines` and give it the result (a file path or pasted text)."

## Step 5: Feedback

Use the contract's Step 5 (feedback and learnings), tag `[cc-chef:research-prompt]`. Qualifying observations are recurring scope or format preferences not already in context, such as always wanting a country-specific angle.
