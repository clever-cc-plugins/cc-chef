# Recipe file format

Every saved recipe is one Markdown file in this fixed layout. Skills write it, `recipe_tool.py` validates it, and the export formats are derived from it. Write the recipe in the user's language; only the structural markers below are fixed.

## Layout

```text
---
cc-chef: 1
title: Rinderrouladen
language: de
servings: 4
prep-minutes: 40
cook-minutes: 120
tags: [Hauptgericht, Schmoren]
source: Adapted from <title>, <author>, <book or site>
source-url: https://...
signature: Ein Löffel Gurkenwasser in der Soße
oven: 160 °C Ober-/Unterhitze, 140 °C Umluft
---

# Rinderrouladen

<optional description paragraph(s)>

## <any heading, e.g. "Zubereitung">

### 1. Rouladen füllen

- **4 Scheiben** Rinderoberschale, je ca. 180 g
- **2 EL** Senf, mittelscharf
- Salz

<instruction paragraph(s) for this step>

### 2. ...

## <any heading, e.g. "Hinweise">

<free notes: serving, sides, drinks, conversions with originals, substitutions with originals>
```

## Rules

Frontmatter is a flat subset of YAML: `key: value` lines, inline lists such as `[a, b]`, and block lists (`tags:` followed by `- a` lines). Any other non-blank line is an error: a line without a colon, a nested (indented) key, or a list item outside a block list. Ascii digits-only values are numbers, surrounding quotes are stripped, unknown keys are kept, and a missing `cc-chef` key is read as version 1. The title comes from the frontmatter `title`, falling back to the `# ` heading; one of the two must exist.

A step is a `###` heading that starts with `<n>. `, numbered 1, 2, 3 in order. Only the bullet block directly under a step heading holds ingredients (blank lines between bullets are fine). Bullets after instruction text are part of the text. A step may have no ingredients. A step title is the component group (for example "Sauce" or "Filling"); there is no separate ingredient-section field. A `##` heading cannot sit between two steps: it is an error, so put such text in the notes after the last step. Inside the notes, don't use `### <n>.` headings; they read as steps.

An ingredient line is: an optional bold amount and unit, then the food up to the first `, `, then an optional note. The first token inside the bold part is the amount: digits, a decimal comma or point, a unicode fraction such as `½`, a fraction `a/b`, or a range with `-` or `–`. The rest of the bold part is the unit and may be empty (`**2** Eier`). Bold text that does not start with an amount (`**eine Prise** Salz`) is kept as the unit with no amount. A line without bold has no amount, as in `- Salz`.

The description is the text between the `#` heading and the first `##` or `###` heading. The notes are everything from the first `##` heading after the last step to the end of the file. `##` headings before the first step are free text in the user's language and are never parsed for meaning.

"Optional" goes in the ingredient note in the user's language; there is no separate flag. Original amounts of converted or substituted ingredients, and the conversion convention used, go into the notes section, not into extra fields. The ingredient overview is derived from the steps and never stored.

## File names

Name the file after the title: lowercase, `œ` becomes `oe`, `æ` becomes `ae`, `ß` becomes `ss`, accents are dropped (`ä` becomes `a`), every run of other characters that are not a-z or 0-9 becomes a single `-`, and leading and trailing `-` are removed. If nothing is left, use `recipe`. Add `.md`. If the file already exists, use `-2`, `-3` and so on before the extension. Example: `Bœuf bourguignon` becomes `boeuf-bourguignon.md`.

## Command line

Run the tool with Python 3.9 or newer; it needs only the standard library.

```text
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" validate <file>
python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/recipe_tool.py" newpath <folder> <title>
```

`validate` prints `OK: <title>, <n> steps, <m> ingredients` and exits 0, or prints `<file>:<line>: <message>` for the first problem it finds and exits 1. It reports a missing or unclosed frontmatter, a frontmatter line that is not `key: value`, a missing title, no steps, an unclosed `**` in an ingredient line, a `##` heading between steps, and step numbers that do not run 1..n. Fix the reported line and validate again. `newpath` prints a collision-free `.md` path for a title in a folder.

## Without python3

If `python3` is not available, both validation and the JSON-LD and Paprika export are unavailable, because they run through the tool. Saving still works: write the Markdown by hand following the rules above, including the slug rules for the file name and a check that the step numbers run 1..n and every `**` is closed. Tell the user once that the automatic check was skipped and that the export formats cannot be produced until Python 3.9 or newer is installed.

## Example (German)

```text
---
cc-chef: 1
title: Rinderrouladen
language: de
servings: 4
prep-minutes: 40
cook-minutes: 120
tags: [Hauptgericht, Schmoren]
source: Adapted from Rinderrouladen klassisch, Beispielautorin, beispiel-kochbuch.de
source-url: https://example.com/rinderrouladen
signature: Ein Löffel Gurkenwasser in der Soße
oven: 160 °C Ober-/Unterhitze, 140 °C Umluft
---

# Rinderrouladen

Klassische Sonntagsrouladen mit dunkler Soße, gefüllt mit Senf, Speck, Zwiebel und Gurke.

## Zubereitung

### 1. Rouladen füllen

- **4 Scheiben** Rinderoberschale, je ca. 180 g
- **2 EL** Senf, mittelscharf
- **4 Scheiben** Frühstücksspeck
- **2** Zwiebeln, in Streifen
- **2** Gewürzgurken, längs geviertelt
- Salz

Das Fleisch zwischen Folie dünn klopfen, mit etwas Salz und dem Senf bestreichen. Mit Speck, Zwiebelstreifen und Gurkenfächer belegen, aufrollen und mit Küchengarn fixieren.

### 2. Rouladen anbraten

- **2 EL** Butterschmalz
- **1** Zwiebel, grob gewürfelt
- **2 EL** Tomatenmark

Das Schmalz in einem Bräter stark erhitzen. Die Rouladen rundum 6 bis 8 Minuten braten, bis sie tiefbraun sind. Herausnehmen, Zwiebel und Tomatenmark im Bratfett 3 Minuten anrösten, bis das Tomatenmark dunkel riecht und am Boden ansetzt.

### 3. Schmoren

- **400 ml** Rinderfond
- **150 ml** Rotwein, trocken
- **1 TL** Gurkenwasser, aus dem Glas
- **1** Lorbeerblatt
- Salz, eine zweite kleine Prise zum Abschmecken
- Pfeffer, frisch gemahlen

Mit Rotwein ablöschen und fast vollständig einkochen lassen. Fond, Lorbeer und Gurkenwasser zugeben, die Rouladen wieder einlegen. Zugedeckt im vorgeheizten Ofen (160 °C Ober-/Unterhitze, 140 °C Umluft) etwa 2 Stunden schmoren, bis sich das Fleisch mit einer Gabel leicht zerteilen lässt. Die Soße abschmecken und mit Salz und Pfeffer nachwürzen.

## Hinweise

Dazu passen Kartoffelklöße und Rotkohl. Ein kräftiger Rotwein passt auch ins Glas.
```

## Example (English)

```text
---
cc-chef: 1
title: Shakshuka
language: en
servings: 2
prep-minutes: 10
cook-minutes: 25
tags: [Breakfast, One-pan]
signature: A spoon of harissa stirred into the onions
---

# Shakshuka

Eggs poached in a spiced tomato and pepper sauce.

## Method

### 1. Build the sauce

- **2 tbsp** olive oil
- **1** onion, finely diced
- **1** red bell pepper, diced
- **2 cloves** garlic, sliced
- **1 tsp** cumin, ground
- **1 tbsp** harissa
- **1 can** crushed tomatoes, 400 g
- Salt, a pinch at the start and the rest at the end

Heat the oil over medium heat and cook the onion and pepper with a pinch of salt for about 8 minutes, until soft and lightly golden. Add garlic, cumin and harissa and stir for 1 minute until fragrant. Add the tomatoes and simmer 10 minutes until thick enough that a spoon leaves a trail.

### 2. Poach the eggs

- **4** eggs
- **1 tsp** lemon juice
- Parsley, chopped

Make four wells in the sauce and crack in the eggs. Cover and cook 5 to 7 minutes, until the whites are set but the yolks still wobble. Finish with lemon juice and parsley.

## Notes

Serve straight from the pan with bread.
```
