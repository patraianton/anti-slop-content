# Panel round 1: Job Thread launch kit v1, merged editor report

Step 6 of `process/LINE.md`. The agent merges the reader reports into this file. The editor reads only the
critical rows (about 10 minutes). In a real project this file is copied to `process/runs/<run>/panel/round-N.md` for each round; here the
filled round 1 keeps the template name. A round without its file was not held.
`tools/check.py` counts the `round-*.md` files in the folder given by `--panel` (`process-claims` F3). The
hash in the header is the one `--reviewed-sha256` takes at release.

This file is the Acme Dispatch example. The readers are the pinned roles in `personas.md`. Every finding is a reader role's, none is a real person's.

## Header

- Date: 2026-09-24
- Version reviewed: `examples/acme/drafts/v1.md`, the first draft.
- Personas: `project/panel/personas.md` version 1. Roles that ran: owner-buyer, sceptic, compliance-reader, voice-editor, fact-checker, other-family, cold-reader, adversary.
- Kind of round: content.
- Lint before the round: `tools/check.py` exit 1, 52 findings on this version. The round does not start on exit 3.
- sha256 of the reviewed piece: 93c8269f5a368fe12ff247f89244aa9a01b8d2aa3fad26a817b4d0ec728b8c99
- Live reader from the audience: requested no; answered no.

## Counts: slop class by severity

Copy the numbers from the defects table below. No 1 to 10 scores: they measure the persona.

| class | critical | major | minor |
|---|---:|---:|---:|
| invented-fact | 2 | 4 | 0 |
| filler | 0 | 0 | 1 |
| empty-structure | 0 | 0 | 0 |
| false-precision | 1 | 0 | 0 |
| false-absence | 0 | 0 | 0 |
| voice-drift | 0 | 0 | 1 |
| contradiction | 0 | 1 | 0 |
| render-artifact | 0 | 0 | 0 |

## Defects

One row per defect, merged across roles. `lens` lists the roles that found it.

| # | class | severity | quote | file:line | fix | lens |
|---|---|---|---|---|---|---|
| 1 | invented-fact | critical | "Every text, call and email with your customer is kept on the job card, so nothing is lost and your customers are always opted in." | v1.md:17 | cut the promise; open `decisions.md` row D-01 | compliance-reader, sceptic |
| 2 | invented-fact | critical | "Early users report a 40% lift in booked jobs." | v1.md:19 | cut; no source and no record in `numbers.json` | sceptic, fact-checker, cold-reader |
| 3 | false-precision | critical | "Billing is the second-largest complaint in public reviews of DispatchPro" | v1.md:74 | cut, or add a computed rank row from the review table | adversary |
| 4 | invented-fact | major | "Open Settings → Messaging → Job Thread." | v1.md:15 | cut; no facts row shows a menu path | fact-checker |
| 5 | invented-fact | major | "There is nothing to set up, and texting starts right away." | v1.md:15 | cut; business texting waits on registration (F-08) | compliance-reader, owner-buyer |
| 6 | invented-fact | major | "Job Thread is included in every plan, from $29 a month, with a 14-day trial." | v1.md:21 | rewrite as Pro and Crew only (D-04); prices go to the page (D-03) | sceptic, fact-checker |
| 7 | invented-fact | major | "We will register the numbers for you and handle the carrier approvals" | v1.md:63 | cut; open D-02 | compliance-reader |
| 8 | contradiction | major | "Two-way sync with LedgerLite keeps every invoice in step" | v1.md:51 | rewrite: one way, 6 fields (F-06, F-14) | adversary, fact-checker |
| 9 | voice-drift | minor | "Dispatch on autopilot" and the name "DispatchPro" | v1.md:8, 19, 29, 35 | cut; K-01 and VN1 | voice-editor |
| 10 | filler | minor | "a robust, comprehensive way to ensure that every owner leverages best practices" | v1.md:65 | cut | voice-editor |

A replacement in the `fix` column cites the source line it rests on, or it is not applied. Steps 4 and 5 run
on it first.

## Counters

| counter | this round |
|---|---|
| false claims found | 8 |
| promises removed | 3 |
| sources added | 0 |
| minutes | 40 |

## Verdict

Round 1 removed three promises and one invented number from the customer copy and moved the prices to the page.

## Release gate for the last round

- critical = 0.
- New sentences in customer copy = 0.
- Every fix applied. The version after the fixes gets the release hash. If fixes ran after the last round,
  say so here, because no round saw the result.

Not met after round 1: three critical rows. `drafts/final.md` is the version after the fixes. No second round was held on it.

## Decisions for the editor

Rows added to `decisions.md`: D-01, D-02, D-03, D-04. Nothing is decided in this file.
