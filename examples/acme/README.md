# examples/acme/

A worked example for a fictional company, Acme Dispatch: scheduling, quotes and invoicing for small home-service
companies in the US. The launch is **Job Thread**, texts, calls and emails with a customer on the job card.
Every name, price, date and count is invented.

The example proves two things:

- the rules in `rules/` and the checker in `tools/` know nothing about Acme: everything specific to it is in `project/`;
- the checker separates a first draft written by an eager agent from the same kit after the fixes.

| path | what it is |
|---|---|
| `project/` | a filled project layer: every file of the blank `project/` at the repo root, with realistic Acme rows |
| `drafts/v1.md` | a first draft of five pieces (email, social, page, partner-note, how-made) with the usual agent mistakes |
| `drafts/final.md` | the same kit fixed |

## The two commands

Run both from the repo root.

```
python tools/check.py examples/acme/drafts/final.md --project examples/acme/project --claims examples/acme/project/claims.csv
python tools/check.py examples/acme/drafts/v1.md --project examples/acme/project
```

| command | expected exit | what it means |
|---|---|---|
| first | 0 | no finding in any check; `parity` and `release-hash` are `not_run` because no page, `--panel` or `--reviewed-sha256` was given, and the exit stays 0 without `--require-all` |
| second | 1 | 52 findings, listed below; exit 1 is findings, never exit 3 (a check that could not run) |

## Where each kind of finding in v1 comes from

One line per check. The file named is read from `examples/acme/project/` unless it says `rules/`.

| check | what v1 does | where the rule lives |
|---|---|---|
| `landmines`, competitors-partners F2 and F3 | the partner note gives the office "every owner's texts"; the page says "two-way sync" over a one-way import | `rules/landmines/competitors-partners.md`; the one-way fact is row F-06 and F-14 of `facts.md` |
| `landmines`, compliance-promises F1 | "kept on the job card" and "always opted in" with no owner | `rules/landmines/compliance-promises.md`; the open decision is D-01 in `decisions.md` |
| `landmines`, numbers-and-sources F2 | "second-largest complaint" and "top three" with no computed record | `rules/landmines/numbers-and-sources.md`; a rank holds only with a record like `R-mobile` in `numbers.json` |
| `landmines`, pricing-plans F1 and F2 | "included in every plan" and "14-day trial" in the email | `rules/landmines/pricing-plans.md`; the plans are rows F-03 to F-05 of `facts.md`, the choice is D-03 and D-04 |
| `landmines`, process-claims F1, F2, F3 | "before writing", "every public source", "three review rounds" with no round reports | `rules/landmines/process-claims.md`; the coverage gaps are in `coverage.md` |
| `landmines`, product-claims F1 | an invented menu path, "replies land on the job card" | `rules/landmines/product-claims.md`; row F-11 of `facts.md` is only CLAIMED |
| `landmines`, research-absence F3 | "for the first time" for texting that already worked on open quotes | `rules/landmines/research-absence.md`; row F-10 of `facts.md` |
| `time-promises` | "right away", "instantly", "nothing to set up", "no setup" | `rules/landmines/setup-timelines.md`; registration is row F-08, its length is UNKNOWN in F-17 |
| `plain` | sentences over 20 words, semicolons in list items, "because", an unexplained competitor name | `rules/landmines/plain-language.md`; the limits are in `pieces.json` |
| `voice` | an em dash, "seamlessly", "robust", "ensure", a triad of abstract adjectives, "not just ... it is", a named competitor, a percentage lift, a first person "I" in the partner note | `rules/voice.md` (VB1 to VB8) and `voice.md` section 6 (VN1, VN3, VN5) |
| `numbers` | "40%" and "60 forum threads" with no record; "38 help center articles" against the record of 41 that lists 38 under `conflicts` | `numbers.json`; `rules/landmines/numbers-and-sources.md` F1 and F4 |
| `repeats` | the same eight or more words twice: "Text any customer from your business number, right from the job card" and "every text, call and email with your customer" | built into `tools/check.py` |
| `stray-labels` | a doubled word: "the the" | built into `tools/check.py`; the labels in `voice.md` section 8 are searched only with `--html` |
| `killed-lines` | "Dispatch on autopilot" and "Never miss a job again" come back | the killed lines table of `decisions.md` (K-01, K-02) |
| `claims`, `mark-budget` | pass on v1: the ledger is for `final.md`, and v1 has no long brackets | `claims.csv` |

## What changed from v1 to final

| v1 | final |
|---|---|
| a price line and "every plan" in the email | no price in the email (D-03); Pro and Crew only (D-04); prices on the page, each in `numbers.json` |
| "Open Settings → Messaging → Job Thread" | cut; no facts row shows a menu path |
| "right away", "nothing to set up" | cut; the registration step is named and no time is promised |
| a promise about consent and data | cut; the open question is D-01 |
| "we will register the numbers for you" | `[Whether Acme or the owner submits the form is still open.]`, a PROPOSAL row in `claims.csv`, open decision D-02 |
| "replies land on the job card" | `[Replies show up next to the text you sent.]`, a TO-CONFIRM row owned by Dan Kowalski, due 2026-10-06 |
| "40% lift", "60 forum threads", "38 articles" | cut, or the counts in `numbers.json`: 41 articles, 12 release notes, 9 recordings |
| "second-largest complaint" with no table | "third-largest complaint" and "64% of all complaints", both computed from the review table in `numbers.json`, with "close, not exact" beside the count |
| a named competitor | "one competing scheduling product" |
| "I checked every public source before writing, in three review rounds" | "I opened 41 of 41 help center articles ..." and a step that lists what was not run: no page check, no panel check, no release hash check, no outside reader |

## Notes

- `drafts/v1.md` holds one em dash on purpose, so that `voice` VB7 has something to find. A grep for em dashes in `examples/`
  finds that one file and no other. Exclude it from any repo-wide em dash grep.
- Marks in `final.md` are `[square brackets]`: a bracket of four words or more counts against the limit of 7 per piece in
  `pieces.json`; `[First name]` and `[Partner name]` are merge fields and do not count.
- `final.md` passes check `plain` and the grade limits (email 9, partner-note 9, how-made 11). It says nothing about a
  panel round: the one filled round in `project/panel/round.md` was held on v1 only.
