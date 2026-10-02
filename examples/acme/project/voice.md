---
id: project-voice
version: 1
applies_to: all
---

# House voice, as data (Acme Dispatch, a fictional company)

Filled in step 1 of `process/LINE.md` by the editor, with an agent that counts. The checker reads this file together
with `rules/voice.md` (`--project examples/acme/project` points it here). Every count below is invented for the example.

What the checker reads here:

- every table with a column whose header contains "cue" (section 6): each cue becomes a banned cue;
- the fenced `allowed` block (section 4): the exceptions to `rules/voice.md`;
- the fenced `terms` block (section 7): the company's own terms, for check `plain`;
- the fenced `labels` block (section 8): stray labels to search for.

Everything else is for the agent and the editor. A number in this file comes from counting your own text.

This file covers naming and form only. Whether the product works stays a claim (`rules/landmines/product-claims.md`).

Scope: pieces with `voice: house` in `pieces.json` are in the company's voice. Pieces with `voice: author` are
in the editor's voice: the reader words, length and never-does rows apply, the exceptions in section 4 do not, and a
row may say it does not apply to them.

## 1. Where the counts come from

| slice | what it is | size | dates |
|---|---|---|---|
| blog | Acme Dispatch blog posts | 40 posts | 2022 to 2026-09 |
| social | Acme LinkedIn posts | 24 posts | 2024 to 2026-09 |
| site | home, pricing and feature pages | 9 pages | 2026-09 |

## 2. Forms and lengths

| form | norm |
|---|---|
| blog post | median about 360 words |
| LinkedIn post | 40 to 120 words |
| launch email | 150 to 250 words, one call to action |
| bullets per feature | 4 to 6 |

## 3. Reader words

| word | counts per slice (blog / social / site) | rule |
|---|---|---|
| you | 420 / 30 / 33 | the main word; write to "you" from the first line |
| owner(s) | 96 / 11 / 8 | the person who runs the company; used in the third person only when "you" does not fit |
| tech(s), crew | 61 / 9 / 12 | the people who work for the owner |
| customer(s) | 214 / 20 / 36 | the owner's customer, the homeowner; allowed |
| client(s), end user(s) | 0 / 0 / 0 | banned as words for the owner's customer |
| contractor | 0 / 0 / 0 | banned as a form of address for the owner |

## 4. Own recurring phrases, allowed even where they look like AI tells

The plan names come as a list of three in the corpus: "Starter, Pro and Crew". `rules/voice.md` VB1 selects every
list of three, so this one shape needs a row. Counts: blog 14, social 3, site 9. The shape appears in no other form.

```allowed
# regex | max per piece | piece ids or all
# Starter, Pro and Crew: 14 / 3 / 9 (blog / social / site); the three plan names, always in this order
\bStarter, Pro,? and Crew\b | 2 | page, partner-note
```

## 5. Words from the brief the company never uses

| word | count in corpus | use instead |
|---|---|---|
| workspace | 0 | "in one place" |
| operating system | 0 | "everything you need in one place" |
| unified communications | 0 | "texts, calls and emails" |
| engagement | 0 | name the action: "reply", "call" |

## 6. What the company never does

| id | never | evidence | cue |
|---|---|---|---|
| VN1 | names competitors in launch copy (the names are listed in the cue column only so the checker can find them) | DispatchPro and RouteKing: 0 mentions on the whole site | `DispatchPro` · `RouteKing`, in email, social, page, partner-note |
| VN2 | "coming soon", "roadmap", "beta", "in development" | 0 on the site | `coming soon` · `roadmap` · `beta` · `in development` |
| VN3 | a percentage lift from one feature | none in any announcement | regex `\b\d+(\.\d+)?%\s+(more|faster|higher|lift|increase|better)\b` |
| VN4 | apologies | removals are framed as "Due to low usage" | `sorry` · `apologize` · `apologies` · `unfortunately` |
| VN5 | first person "I" in house-voice pieces | only the founder, quoted | regex `(^|\s)I\s`, case-sensitive, in email, social, page, partner-note |
| VN6 | ALL CAPS runs and double exclamation marks | old 2022 posts only | `!!` · regex `\b[A-Z]{4,}(\s+[A-Z]{4,})+\b`, case-sensitive |
| VN7 | British spelling | the whole site is American | `recognised` · `personalised` · `organise` · `analyse` · `colour` · `centre` |
| VN8 | "client" or "end user" for the owner's customer | 0 in 40 posts, 24 social posts, 9 pages | regex `\bclients?\b` · `end user` · `end users` |
| VN9 | "contractor" as a form of address for the owner | 0 on the whole site | `contractor` · `contractors` |

## 7. The company's own terms

```terms
# term | count or source | plain words for a heading (regex), "-" for a name
Acme Dispatch | the company | -
Job Thread | the new feature, launch brief | \b(?:texts?|calls?|messages?)\b
LedgerLite | accounting partner, release note 9 | -
MapRoute | routing partner, release note 5 | -
```

## 8. Labels (optional)

```labels
TBD
{{
Lorem
```
