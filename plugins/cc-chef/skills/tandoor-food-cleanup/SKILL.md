---
name: tandoor-food-cleanup
description: >
  Use this skill to clean up the food and unit database of the user's Tandoor instance: find duplicate foods and units, find foods whose names hold quantities or preparation details, and merge them group by group after the user approves each group. Invoke when the user says "clean up my Tandoor foods", "merge duplicate foods in Tandoor", "my Tandoor food list is a mess", "Tandoor Zutaten aufräumen", or "fix the units in Tandoor". Needs a configured Tandoor instance (TANDOOR_URL and TANDOOR_TOKEN). Changes nothing before the user approves a group, and merges cannot be undone. Do NOT use it to upload a recipe (use export-recipe) or to restructure a recipe (use rework-recipe).
allowed-tools: Read, Write, Bash, Glob
argument-hint: "[optional: food or unit to start with]"
---

@../\_shared/tandoor-api.md **Read when:** always: the commands, the plan files and what a merge deletes

# Tandoor Food Cleanup

This skill cleans up the food and unit database of the user's Tandoor instance: duplicates are merged into one kept entry, details that sit in a food name move into the notes of the recipe ingredients that use it, and an alias keeps future imports clean. It follows `../_shared/skill-contract.md` (language, address form, tone and the framing line included); the steps below are its own work. Everything shown to the user is in the output language. All Tandoor access goes through `tandoor.py`; never use `curl`, never read or print the token, never edit a plan file by hand. In the commands below, `<tandoor>` stands for `python3 "${CLAUDE_SKILL_DIR}/../_shared/scripts/tandoor.py"`.

## Step 1: Check the connection

Run `<tandoor> check`. On exit 3 or 1, explain in one line why (the script's message), point to the setup in `tandoor-api.md` section 1, and stop. Do not ask for the token in the chat; if the user pastes one, do not repeat or store it and tell them to create a new one.

## Step 2: Backup advice

Before the first write, say in the user's language, in plain words: merges cannot be undone; a merge deletes the merged entry together with its nutrition values and unit conversions; nothing changes until they approve a group. Recommend a backup of the instance now (the database or the Tandoor export) and wait for a clear answer. Without a clear yes to go on, stop.

## Step 3: Read the database

Run `<tandoor> foods-report -o "<report.json>"` with the report in the system temp folder (for example `${TMPDIR:-/tmp}/cc-chef-foods-report.json`), never in the project. It prints only counts. Read the file with Read instead of printing it: it can hold thousands of entries. Delete the report and any plan files when the run ends.

## Step 4: Review in batches

Work through `groups` in the file's order (most recipes first), 5 groups per batch. For each group show: its id (`f1`, `u2`), the members with their recipe counts, whether a member has nutrition properties or an open-data origin, the entry the script suggests to keep and why (properties first, then open-data origin, then most recipes), and the confidence. `same` means an equal name core or plural. `maybe` means a near-identical spelling: never treat a `maybe` group as duplicates without the user's word on each one.

Also read the `polluted` list and the member names yourself. The script finds details after a comma, in brackets or as a leading quantity with a unit, but cannot find words like `gehackte Zwiebel` in every language. When a name holds preparation, a quantity or a qualifier that the script missed, say so and pass it by hand later with `--detail <id>=<text>`. A food with details in its name and no clean partner can be renamed instead: `--rename "<clean name>"` with the polluted food as `--keep` and an empty `--merge`.

The user decides per group: approve with a different entry to keep, skip, or stop. Never approve for them.

## Step 5: One group at a time

For each approved group:

1. `<tandoor> group-plan "<report.json>" --kind food|unit --keep <id> --merge <id>[,<id>] [--detail <id>=<text>] [--rename "<name>"] -o "<plan.json>"`. It re-reads the entries from the instance; entries that vanished since the report are dropped.
2. `<tandoor> group-preview "<plan.json>"`. Show it in the user's language: the notes before and after per affected recipe ingredient, the merges, the aliases, and every warning in plain words (nutrition values and unit conversions that the merge deletes, recipes the token cannot see). With a problem the preview exits 1 and prints no code: explain it and offer to fix the group or skip it.
3. Ask for an explicit OK for exactly this plan. A changed answer means a new plan and a new preview.
4. On OK: `<tandoor> group-apply "<plan.json>" --confirm <code>` with the code from that preview. It moves the notes first, then merges, then adds the alias, and stops at the first failure. On a failure, say what was done and what failed, and offer to run `group-plan` again for the same group: a rerun continues without doubling a note.

A group the user declines is never merged.

## Step 6: Summary after each batch

Say what happened in the batch: merged, renamed, aliases added, skipped, failed. Offer to continue with the next 5 groups or to stop. Units go through the same steps with `--kind unit`; they have no notes to move.

## Step 7: Feedback

Use the contract's Step 5 (feedback and learnings), tag `[cc-chef:tandoor-food-cleanup]`. Qualifying observations are recurring cleanup preferences not already in context, such as a language's preparation words the script missed or a keep rule the user always overrides.
