---
id: research-absence
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: cite-or-cut
applies_to: all
---

# Landmine: "the product does not have X" (ABSENT)

## 1. What this landmine is

Any statement that a feature, page, integration or behaviour does not exist ("Acme has no phone dialer",
"techs cannot start a text", "no CSV import", "the customer timeline is empty"), and any launch line that
presents as new something that already exists. In the facts table this is the label ABSENT.

Strictness `cite-or-cut`: an ABSENT stays only with a `project/coverage.md` row that names where it
looked. ABSENT without a coverage row becomes UNKNOWN and is printed as a question or a bracket.

## 2. What it is not (hand-offs)

- A promise that the company will add something: `product-claims`.
- A zero inside a study ("one record in 1,927"): `numbers-and-sources`.
- A competitor's missing feature ("DispatchPro has no quoting"): the evidence is checked here, whether the
  line may be printed at all is `competitors-partners`.
- "Acme never shares your data with a third party" is a promise: `compliance-promises`.
- A plan that lacks a feature ("texting is not on Starter"): `pricing-plans`.
- A step the customer does not have to do ("nothing to set up"): `setup-timelines`.
- "I checked every source": `process-claims`.
- A sentence too hard to read: `plain-language`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. `project/coverage.md`: one row per source type (`id | source type | total | read fully |
   keyword-searched | not covered | proof`). An ABSENT row in `project/facts.md` names the covered rows by
   id (`COV-01, COV-02`) in `where_searched`. A type with nothing searched and not all read allows no
   absence claim.
2. A dated statement of absence from the company itself, CONFIRMED with a URL: a help center article, a
   docs page, a release note, or the documentation of the gatekeeper that sets the rule.
3. A row in `project/decisions.md` owned by a named owner who states that the feature does not exist today,
   with the date.
4. The refute pass (`process/LINE.md`): a second agent on a different model family gets only the facts
   table and tries to overturn every ABSENT row. It writes the result in the row's `refute` cell: who,
   which model family, `held` or `overturned`, and the new label.

Never a source: one help article (one source type), the reliability grade of the source instead of the
claim (a "high" grade on "Techs cannot start a text" from a single help article), "I didn't see it", a
reviewer who read the same research folder and agreed.

## 4. Forbidden shapes (banned by shape)

- **F1 ABSENT without a coverage row.** A facts row that says a thing does not exist ("cannot", "is
  empty", "not found", or the label ABSENT) and names no `COV-` row. A row labelled CONFIRMED is exempt from
  the word cues: it carries a dated source that states the limit (source 2 above, and A4). Class:
  false-absence. Severity: critical.
- **F2 ABSENT on an uncovered type.** The row names a `COV-` row that does not exist in `coverage.md`, or
  one whose type was neither keyword-searched nor read in full. Class: false-absence. Severity: critical.
- **F3 "New" for something that existed.** A launch line that presents as new a feature with a CONFIRMED
  past or present row. Class: false-absence. Severity: major.
- **F4 ABSENT that skipped the refute pass.** An ABSENT row whose `refute` cell is empty.
  Class: false-absence. Severity: major.

## 5. Allowed with a row

- **A1** ABSENT with every named coverage row searched or read in full.
- **A2** A dated statement of absence from the company ("a CSV import (Acme has none today)").
- **A3** UNKNOWN printed as a question in the "To confirm" list ("Do they still exist, and does the
  follow-up plan become them?").
- **A4** A narrow CONFIRMED with its limit ("Texting with open quotes only, from one shared number").

## 6. Detection

**Stage 1.** Absence is checked in the facts table, not in copy. F1 and F3 are cues
(`facts` target: the data rows of the facts table, refute column blanked; `copy` as in `product-claims.md`).
F2 and F4 are lookups in `tools/check.py` (`check_absence`): for each ABSENT row it reads the named `COV-`
rows from `--coverage` (default `project/coverage.md`) and the row's `refute` cell. ABSENT rows that name
coverage while `coverage.md` is missing make the check `not_run`. The same pass prints how many rows the
refute column marks `overturned`.

The F3 cues are generic launch words. Names of features that already shipped are project data: add each
one as a banned cue in `project/voice.md` (the checker reads banned cues from there).

```cues
# rule | target | rescues | kind  | pattern
F1     | facts  | none    | regex | ^(?!.*\bCOV-\d+\b).*\|\s*ABSENT\s*\|
F1     | facts  | none    | regex | (?i)^(?!.*\bCOV-\d+\b)(?!.*\|\s*CONFIRMED\s*\|)\|.*\b(?:cannot|can't|is empty|not found)\b
F3     | copy   | bracket | regex | (?i)\bnow shows? up\b
F3     | copy   | bracket | regex | (?i)\bfor the first time\b
```

**Stage 2** (`rules/README.md`) gets the row or sentence and the named coverage rows, not the draft. It
answers: which source types would show this feature, were they searched, did the refute pass try.

## 7. Fixtures

`must_fire` rows for F1, F2 and F4 are synthetic Acme facts rows in the shape of a first-pass brief: no
coverage ids, no refute pass, one source type read. `must_not_fire` rows are synthetic Acme ABSENT rows
that name their coverage ids and carry a refute verdict.

```fixtures
{"id": "research-absence/F1/01", "rule": "F1", "expect": "fire", "target": "facts", "text": "| 6 | Texting: inbound only. The customer confirms a phone with a code on the owner's page; \"Techs cannot start a text from the app\"; messages go from (555) 010-0142 | help article 17 | high |", "source": "synthetic (Acme), shape: a facts row that says cannot or inbound only, with no COV id and a source-quality grade instead of coverage"}
{"id": "research-absence/F1/02", "rule": "F1", "expect": "fire", "target": "facts", "text": "| 5 | Everything created under a selected customer saves to the card; the activity timeline exists per tech only, on the customer it is empty | help articles 9, 23 | high |", "source": "synthetic (Acme), shape: a facts row that says a view is empty, with no COV id"}
{"id": "research-absence/F1/03", "rule": "F1", "expect": "fire", "target": "facts", "text": "| Public description of recorded calls, in-app meetings, mail sync, recurring tasks and quote stages | not found | ABSENT |", "source": "synthetic (Acme), shape: an ABSENT row with a broad list of missing features and no COV id"}
{"id": "research-absence/F2/01", "rule": "F2", "expect": "fire", "target": "facts", "text": "| id | claim | label | where_searched | refute |\n|---|---|---|---|---|\n| B-6 | Techs cannot start a text from the app; texting is customer-initiated only | ABSENT | COV-22 | |", "coverage": "| id | source type | total | read fully | keyword-searched | not covered | proof |\n|---|---|---|---|---|---|---|\n| COV-22 | Acme training videos, as the first-pass brief covered them | not recorded | 3 videos | 0 | the other videos, not opened | the brief's \"What was read\" lists 3 videos and no other video |", "source": "synthetic (Acme), shape: an ABSENT row that names a COV id whose type had nothing searched and no full read; the proof that overturns the claim sits in the type that was not opened"}
{"id": "research-absence/F4/01", "rule": "F4", "expect": "fire", "target": "facts", "text": "| id | claim | label | where_searched | refute |\n|---|---|---|---|---|\n| B-1.3 | Public description of recorded calls, in-app meetings, mail sync, recurring tasks and quote stages | ABSENT | COV-21, COV-22 | |", "source": "synthetic (Acme), shape: an ABSENT row with an empty refute cell"}
{"id": "research-absence/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "- **Follow-ups that don't slip.** Acme's follow-up plan now shows up on the job as reminders.", "source": "synthetic (Acme), shape: a launch line that presents as new a feature with a CONFIRMED past row, using 'now shows up'"}
{"id": "research-absence/F3/02", "rule": "F3", "expect": "fire", "target": "copy", "text": "- **Texts on the job.** Text any customer from the job card for the first time, and the reply lands on the same card.", "source": "synthetic (Acme), shape: a launch line that presents as new a feature with a CONFIRMED past row, using 'for the first time'"}
{"id": "research-absence/F1/n01", "rule": "F1", "expect": "no_fire", "target": "facts", "text": "| Recorded calls, own calendar, mail sync, quote stages, campaigns | not found in 41 help articles, 9 captioned recordings, 12 release notes, 60 site pages, DNS records and app routes | ABSENT | COV-01, COV-02, COV-03, COV-04, COV-05 |", "source": "synthetic (Acme), shape: an ABSENT row that carries a 'not found' and names its COV ids"}
{"id": "research-absence/F1/n02", "rule": "F1", "expect": "no_fire", "target": "facts", "text": "| Meetings: own calendar, availability, sync with Google or Outlook | /calendar, /meetings, /jobs/calendar return 404; 'calendar' in two unrelated help articles only | ABSENT | COV-01, COV-05 |", "source": "synthetic (Acme), shape: an ABSENT row that names its COV ids and lists the addresses that were tried"}
{"id": "research-absence/F1/n04", "rule": "F1", "expect": "no_fire", "target": "facts", "text": "| F-12 | Starter cannot send texts; texting is listed on Pro and Crew only | CONFIRMED | https://acme.example/pricing, plan table | 2026-09-20 |", "source": "synthetic (Acme), shape: a CONFIRMED row with a dated source that states a limit with the word cannot"}
{"id": "research-absence/F2/n01", "rule": "F2", "expect": "no_fire", "target": "facts", "text": "| id | claim | label | where_searched | refute |\n|---|---|---|---|---|\n| F-07 | Acme syncs the owner's inbox (Gmail, Outlook) and logs email on the job | ABSENT | COV-01, COV-02 (9 captioned recordings), COV-04 (60 site pages), COV-05 (/email, /inbox, /jobs/emails return 404) | held (second model family, confidence high) |", "coverage": "| id | source type | total | read fully | keyword-searched | not covered | proof |\n|---|---|---:|---|---|---|---|\n| COV-01 | Acme help center articles | 41 | 41 | 41, plus about 30 queries in the help center search | videos embedded in articles 8, 19, 33 | audit summary |\n| COV-02 | Acme training videos | 9 | 4 | 9, by captions | 1 without captions | audit summary |\n| COV-04 | Acme site pages in the sitemap | 60 | 0 stated | 60 loaded and searched | none listed | audit summary |\n| COV-05 | App addresses, DNS records, certificates | about 40 address checks | 0 | all | anything behind login | audit summary |", "source": "synthetic (Acme), shape: an ABSENT row where every named COV row was keyword-searched or read in full, with a refute verdict"}
{"id": "research-absence/F4/n01", "rule": "F4", "expect": "no_fire", "target": "facts", "text": "| id | claim | label | where_searched | refute |\n|---|---|---|---|---|\n| F-06 | Acme has calling: a dialer, click to call, a call log, call recording | ABSENT | COV-01, COV-02, COV-04, COV-05 | held; the 2021 voicemail drop is a separate fact |", "source": "synthetic (Acme), shape: an ABSENT row with a filled refute cell"}
{"id": "research-absence/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "- **Follow-ups that don't slip.** Acme's follow-up plan [becomes dated reminders on the job], each drafted by Acme from the quote you sent and your call notes.", "source": "synthetic (Acme), shape: a launch line about a new behaviour, printed in square brackets as a proposal, with no 'new' cue"}
{"id": "research-absence/F3/n02", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Text any customer - not only open quotes - [from your own number].", "source": "synthetic (Acme), shape: a launch line that names a narrow addition inside square brackets, with no 'new' cue"}
{"id": "research-absence/F1/n03", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "- Reminders: tasks with a due date and a repeat appear in an old training video and nowhere in the current materials. Do they still exist, and does the follow-up plan become them?", "source": "synthetic (Acme), shape: UNKNOWN printed as a question in the 'To confirm' list, in copy, not in the facts table"}
```
