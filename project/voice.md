---
id: project-voice
version: 1
applies_to: all
---

# House voice, as data (blank template)

Filled before step 1 of `process/LINE.md` by the editor, with an agent that counts. The checker reads this file together
with `rules/voice.md` (`--project DIR` points it here). Every table ships empty and every block holds only comments, so
nothing here is active until you add a row. A filled version, with rows from the fictional company Acme Dispatch, is in
`examples/acme/project/voice.md`.

What the checker reads here:

- every table with a column whose header contains "cue" (section 6): each cue becomes a banned cue;
- the fenced `allowed` block (section 4): the exceptions to `rules/voice.md`;
- the fenced `terms` block (section 7): the company's own terms, for check `plain`;
- the fenced `labels` block (section 8): stray labels to search for.

Everything else is for the agent and the editor. A number in this file comes from counting your own text. Where you have
examples but no count, write "no number" and quote the examples. Never write a count you did not make.

This file covers naming and form only. Whether the product works stays a claim (`rules/landmines/product-claims.md`).

Scope: pieces with `voice: house` in `project/pieces.json` are in the company's voice. Pieces with `voice: author` are
in the editor's voice: the reader words, length and never-does rows apply, the exceptions in section 4 do not, and a
row may say it does not apply to them.

No corpus yet: a company with fewer than 20 pieces cannot count. Keep the generic list in `rules/voice.md`, add no `allowed`
row, and write each row in sections 2 and 3 as a decision by the editor, marked "decided, not counted", with no number. Fill
section 5 from the brief. Count again after the first 20 pieces ship, and replace the decisions with counts.

## 1. Where the counts come from

List the corpus slices you counted over: what they are, how many items, the date range. Name each slice with one short word
so later tables can use it as a column.

| slice | what it is | size | dates |
|---|---|---|---|

## 2. Forms and lengths

One row per form the company publishes. Give the norm from your own text. A piece that runs past its row is a `filler`
finding unless `project/decisions.md` records why.

| form | norm |
|---|---|

## 3. Reader words

One row per word the company uses for a reader or a person in the story. Count it in each slice. The rule column says
when the word is allowed and when it is banned as a word for someone. Banned words also go into section 6 as cues.

| word | counts per slice (blog / social / site) | rule |
|---|---|---|

## 4. Own recurring phrases, allowed even where they look like AI tells

A phrase that `rules/voice.md` bans stays only with a row here. One line per phrase in the block below, with three
columns: `regex | max per piece | piece ids or all`. For each row, record in a comment line above it the exact shape and the
count per slice (or "no number" and the quoted examples). No row, no exception (`rules/voice.md`, section 3).

```allowed
# regex | max per piece | piece ids or all
# example: workflow, Acme uses it 22 / 8 / 2 (blog / social / site)
# example: \bworkflow\b | 3 | email, social
```

## 5. Words from the brief the company never uses

Words the brief or the product team uses that the company's own text never uses. Check VB9 and the `voice-drift` finding
use this table: a brief word, or a run of five or more brief words, in customer copy is a finding unless the word has a
row here with a count above zero.

| word | count in corpus | use instead |
|---|---|---|

## 6. What the company never does

One row per habit the company avoids. The evidence column holds your count or a quote. The cue column holds what stage 1
searches for: a phrase in backticks, `regex` plus a pattern in backticks, "case-sensitive" for a match with case, and
"in email, social" after the last backtick to limit the row to those pieces. A row with no cue is for stage 2 only. The
rows in the Acme example are suggested starting points: never naming competitors, no "coming soon", no percentage lift
from one feature, no apologies, no first person "I" in house voice, no ALL CAPS runs, one spelling variant. Copy the ones
that fit your company and fill the competitor cell with your competitors' names.

| id | never | evidence | cue |
|---|---|---|---|

## 7. The company's own terms

Terms allowed in copy without a gloss, except in a heading: there the same line also says it in plain words (check `plain`,
F4). One line per term: the term, its count or where it is shown, and a regex for the plain words that may stand in a
heading (`-` for a name). A term listed here with `-` is accepted anywhere without a gloss, which is how you clear
a known abbreviation that check `plain` would flag (F4). Two more optional blocks extend the lists of
`rules/landmines/plain-language.md`: a fenced `plain-ok` block (words that need no explanation, split on spaces) and a
fenced `jargon` block (one regex per line for words your readers do not know).

```terms
# term | count or source | plain words for a heading (regex), "-" for a name
# example: Acme Dispatch | the company | -
# example: Job Thread | the new feature, launch brief | \b(?:texts?|calls?|messages?)\b
```

## 8. Labels (optional)

Strings that must never show up on the rendered page, one per line: unfilled merge fields, "TBD", an internal id. Leave the
block empty if there are none. The checker searches the rendered page for each line.

```labels
# example: [first name]
```
