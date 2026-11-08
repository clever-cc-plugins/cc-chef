# Research Prompts

Ready-to-paste deep-research prompts that build the knowledge base for cc-chef's skills. Unlike sibling plugins, where research strengthened skills that already existed, here the research comes first: the plugin's skills are designed only after the results are in.

## Prompts

| #   | Research prompt                                                              | Feeds                                                                                      | Best suited tools                                                    |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| 1   | [culinary-craft.md](culinary-craft.md)                                       | The quality bar: grounded, cookable dishes with one deliberate touch                       | General deep-research tools                                          |
| 2   | [cooking-from-what-is-on-hand.md](cooking-from-what-is-on-hand.md)           | Ideation from ingredient lists and fridge photos; substitutions and their technique impact | General deep-research tools                                          |
| 3   | [recipe-writing.md](recipe-writing.md)                                       | Recipe structure, units, scaling, locale conventions; reworking found recipes              | General deep-research tools                                          |
| 4   | [nutrition-and-personal-guidelines.md](nutrition-and-personal-guidelines.md) | Opt-in dietary guidelines and their boundaries                                             | Tools with access to scientific databases, plus a general tool       |
| 5   | [recipe-app-formats.md](recipe-app-formats.md)                               | Export to recipe management apps                                                           | Any tool with good web search; technical docs and source code matter |

## Using a Prompt

1. Open the prompt file.
2. Paste the delimited prompt block into the deep-research feature of an AI tool (Claude, ChatGPT, Gemini, Perplexity, Consensus, Elicit, or similar). Running the same prompt in more than one tool and merging the results is encouraged, especially for prompt 4.
3. Save the response as Markdown under `docs/research/research-results-<prompt-file-name>-by-<tool>.md` (e.g. `docs/research/research-results-culinary-craft-by-claude.md`).
4. Once all five are in, the plugin design starts from `docs/skill-ideas.md` and the research files.
