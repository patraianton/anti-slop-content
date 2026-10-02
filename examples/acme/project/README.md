# examples/acme/project/: a filled project layer

This folder is the project layer of a fictional company, Acme Dispatch: scheduling, quotes and invoicing for small
home-service companies in the US. Every file of `project/` is here, filled with realistic rows. Every name, price, date,
article number and count is invented and consistent across the files.

Use it to see the shape of a filled layer. Do not copy its rows into your own project. The blank templates are in
`project/` at the root of the repo, and `project/README.md` there says what to fill, in which order and how long it takes.

## What is filled

| file | what is in it |
|---|---|
| `pieces.json` | the five piece types: email, social, page, partner-note, how-made |
| `voice.md` | corpus slices, forms, reader words, one allowed phrase shape, nine never-does rows with cues, four terms |
| `coverage.md` | 5 source types: help center, release notes, pricing snapshots, webinar recordings, partner docs (one partly read) |
| `facts.md` | 17 rows with all four labels (CONFIRMED, CLAIMED, ABSENT, UNKNOWN), refuted by another model family, and 2 quotes |
| `numbers.json` | 12 printed counts, the DispatchPro complaints table, one rank record and one share record |
| `claims.csv` | 12 rows for `drafts/final.md`: SOURCED, PROPOSAL and TO-CONFIRM with an owner and a date |
| `decisions.md` | 6 decisions (2 open), 3 killed lines with patterns, a release record |
| `panel/personas.md` | pinned reader roles and the three added readers |
| `panel/round.md` | one filled round on `drafts/v1.md` |
| `plain-pass.md` | the plain pass prompt with the Acme terms and limits |

## The people

Maria Ortega, founder. Dan Kowalski, head of product. Priya Shah, support and compliance lead. They are the named
owners in `decisions.md` and `claims.csv`.

## Run it

From the repo root:

```
python tools/check.py examples/acme/drafts/final.md --project examples/acme/project --claims examples/acme/project/claims.csv
python tools/check.py examples/acme/drafts/v1.md --project examples/acme/project
```

The first exits 0. The second exits 1. `examples/acme/README.md` says why.
