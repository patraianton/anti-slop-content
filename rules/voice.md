---
id: voice
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
applies_to: all
---

# Voice rules, generic

## 1. What this file is

This file lists the sentence shapes that mark text as machine-written (the AI tells). The list is the same for every
project. `tools/check.py` reads the cues in section 2 and reports each hit as `voice/<id>`.

A company's own exceptions, forms, reader words and never-does rows do not live here. They live in `project/voice.md`.
The checker reads both files with one parser and merges them.

Stage 1 selects lines by cue. Stage 2 (an agent or the editor) decides whether a selected line is a real tell.

## 2. AI-tell list (banned)

| id | tell | cue | note |
|---|---|---|---|
| VB1 | triad of abstract nouns or adjectives ("fast, simple, and powerful") | regex `\b(?!(?:emails?\|calls?\|texts?\|meetings?),\s)\w+, \w+,? and \w+\b` | Selects every list of three. Stage 2 checks that the words are abstract. A list that opens with a channel noun, such as "calls, texts and meetings", is concrete and is not selected. A project may allow one triad shape in its `project/voice.md` |
| VB2 | "not X but Y" and "isn't just X, it's Y" | regex `\b(not\|isn't\|is not)\s+(just\|only\|merely)\b` · regex `\bnot\s+\w+(\s+\w+){0,3},\s+but\b` | No exception unless the project counts the shape in its own corpus |
| VB3 | robust | `robust` | |
| VB4 | seamlessly as filler | `seamless` · `seamlessly` | Banned unless `project/voice.md` has an allowed row for it and the piece is covered by that row |
| VB5 | stock openers | `in today's fast-paced` · `in today's digital` · `in an ever-changing` | |
| VB6 | throat-clearing | `it's worth noting` · `it is worth noting` · `it's important to note` · `needless to say` | |
| VB7 | em dashes | regex `\u2014` | Any em dash. Use a comma, a colon or two sentences |
| VB8 | consultant filler | `leverage` · `ensure` · `comprehensive` · `holistic` · `best practices` | |
| VB9 | mirrored brief phrases | any run of 5 or more words shared with the task brief; the brief words listed in section 5 of `project/voice.md` | Stage 2 compares the piece with the brief. The brief words come from `project/voice.md` |
| VB10 | chatbot residue: literal fragments that only a pasted chatbot answer carries | `oaicite` · `contentReference` · regex `turn\d+(?:search\|news\|image)\d+` · `utm_source=chatgpt` · `As an AI language model` · `I hope this helps` · regex `^Certainly!` · regex `\[(?-i:Insert\|Your)\b[^\]]*\]` | No judgment needed. Severity critical: stage 2 records it as critical, though `check.py` reports every voice cue as minor. No `allowed` row may excuse it, and brackets never rescue it: the bracket cue needs the word "Insert" or "Your" right after the bracket, so the repo's own bracket marks stay silent |
| VB11 | false subject: an abstraction doing a person's job | `the data tells us` · `the data shows us` · `this speaks to` · `the numbers speak for themselves` · `the results speak` · regex `\bit['\u2019]s clear that\b` · `it is clear that` · `this underscores` · `this highlights the importance` | Stage 2 checks whether a person or a source could be named instead |
| VB12 | empty assertion: a claim of weight with no object | `the stakes are high` · `the stakes have never been higher` · `the possibilities are endless` · `a game changer` · `at the end of the day` · `in a world where` · `now more than ever` · regex `\bthe future of \w+ is here\b` | Stage 2 asks what the sentence tells the reader to do. "A game changer" may be allowed by a row in `project/voice.md` |

## 3. Exception rule

A banned word or shape stays in a piece when `project/voice.md` has an `allowed` row for it with:

1. the exact shape (a regex);
2. its count per corpus slice, copied from the project's own text corpus, or the words "no number" with the quoted
   examples that show the habit;
3. the pieces it applies to, or `all`.

No row, no exception. The checker also counts uses: a piece that passes the "max per piece" number in the row gets a
finding. Adding a row is a rule change (`rules/README.md`, "How to change a rule"). A form with one example in the
corpus is not a habit and gets no row.

Pieces whose `voice` is `author` in `project/pieces.json` take no exception from `project/voice.md`.

## 4. File formats shared with project/voice.md

Both files use the same four structures. The parser reads them from either file.

Tables with a cue column. Any pipe table whose header has a cell containing "cue" is read. The first cell of a row is the
id. In the cue cell:

- a phrase in backticks is a literal, matched as a whole word or phrase, ignoring case;
- `regex` followed by a phrase in backticks is a regular expression;
- a cell that contains the words "case-sensitive" is matched with case;
- text after the last backtick that ends "in email, social" limits the cue to those piece ids;
- several cues in one cell are separated by a middle dot.

Regex alternation in a table cell is written `\|`: the parser reads `\|` as a pipe, inside or outside backticks, and GitHub renders the table whole. A bare pipe inside backticks still works for the parser but breaks the rendered table.

Fenced `banned` block. A code fence whose info string is `banned`. One regex per line, optionally preceded by an id and a
colon. Lines that start with `# ` are comments.

Fenced `allowed` block. A code fence whose info string is `allowed`. One exception per line with three columns:

    regex | max per piece | piece ids or all

Example line: `\bworkflow\b | 3 | email, social`. The middle column is a whole number, or `-` for no limit. The third column
is a comma-separated list of piece ids, or `all`.

Fenced `terms` block. A code fence whose info string is `terms`. One term per line:

    term | count or source | plain words regex or -

The term is matched with case. The third column is a regex for the plain words a heading must also carry, or `-` for a
name that needs no gloss (check `plain`, F4).

Fenced `labels` block. A code fence whose info string is `labels`. One stray label string per line. The checker searches
the rendered page for each one.

## 5. Dates and decay

This list was written on 2026-10-02 against the model generations of 2025 and 2026. Word lists lose power as models
change. A 2025 finding reports that a word list tuned on one model works near chance on another.

The editor reviews the list each quarter. A row that stops firing on new agent drafts is kept only if the project
corpus still shows the habit. VB10 does not decay: a pasted chatbot fragment is a tell in every model generation.
