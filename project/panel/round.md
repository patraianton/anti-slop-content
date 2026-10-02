# Panel round N: <piece>, merged editor report

Step 6 of `process/LINE.md`. The agent merges the reader reports into this file. The editor reads only the
critical rows (about 10 minutes). Copy to `process/runs/<run>/panel/round-N.md` for each round, one folder per piece. A round without this file was not held.
`tools/check.py` counts the `round-*.md` files in the folder given by `--panel` (`process-claims` F3). The
hash in the header is the one `--reviewed-sha256` takes at release.

## Header

- Date:
- Version reviewed: (a version label and the git commit of the piece and the page).
- Personas: `project/panel/personas.md` version N. Roles that ran: (list ids).
- Kind of round: content | cuts only. On a cuts-only round, a fix that adds a sentence to customer copy is rejected.
- Lint before the round: `tools/check.py` exit code and finding count on this version. The round does not start on exit 3.
- sha256 of the reviewed piece: (the release hash in step 8 must equal this).
- Live reader from the audience: requested yes / no; answered yes / no.

## Counts: slop class by severity

Copy the numbers from the defects table below. No 1 to 10 scores: they measure the persona.

| class | critical | major | minor |
|---|---:|---:|---:|
| invented-fact | 0 | 0 | 0 |
| filler | 0 | 0 | 0 |
| empty-structure | 0 | 0 | 0 |
| false-precision | 0 | 0 | 0 |
| false-absence | 0 | 0 | 0 |
| voice-drift | 0 | 0 | 0 |
| contradiction | 0 | 0 | 0 |
| render-artifact | 0 | 0 | 0 |

## Defects

One row per defect, merged across roles. `lens` lists the roles that found it.

| # | class | severity | quote | file:line | fix | lens |
|---|---|---|---|---|---|---|
| 1 | example: invented-fact | major | "Texting starts the day you sign up." | draft.md v2:18 | cut; open a `decisions.md` row for number registration | sceptic, compliance-reader |

A replacement in the `fix` column cites the source line it rests on, or it is not applied. Steps 4 and 5 run
on it first.

## Counters

| counter | this round |
|---|---|
| false claims found | |
| promises removed | |
| sources added | |
| minutes | |

## Verdict

One sentence that names what changed. A sentence repeated from the previous round is rejected.

## Release gate for the last round

- critical = 0.
- New sentences in customer copy = 0.
- Every fix applied. The version after the fixes gets the release hash. If fixes ran after the last round,
  say so here, because no round saw the result.

## Decisions for the editor

Rows added to `decisions.md`, by id. Nothing is decided in this file.
