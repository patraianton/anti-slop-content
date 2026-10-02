# Decision log (step 7)

Agents prepare the rows. The editor decides the editor's rows and proposes owners for the rest (about 10 to 15
minutes). The named owners at the company close theirs, once they accept. It is the only place where a person
decides. A row goes here when no source can close it: a promise the company would make, a price, a person on
stage, consent, recording, number registration, data handling. The "To confirm" list printed with a piece is
generated from the open rows.

`tools/check.py` reads the killed lines table (`killed-lines` check). The other tables are for people and for
the release gate in step 8.

Rules
- `owner` is a named person who has agreed to decide. An agent is never an owner. Blank means nobody has.
- `proposed owner` is a guess by role (founder, product lead, compliance owner). Nobody owns a row until they say so.
- A row about the law or a company promise is closed only by its owner, with a date.
- A cut line goes to the killed lines table. It comes back only through a new decision row, named in `reversed by`.

## Decisions

The tables ship empty. A filled example is in `examples/acme/project/decisions.md`.

| № | question | recommendation | copy if yes | copy if no | proposed owner | owner | decision | date | round |
|---|---|---|---|---|---|---|---|---|---|

## Killed lines

`tools/check.py` (`killed-lines`) searches the piece and the page for the `pattern` column (a Python regex
between backticks; write a table pipe as `\|`), brackets included. It skips a row whose `reversed by` cell holds a
decision id (`D-n`).

| id | cut line | pattern | cut in | reversed by | came back |
|---|---|---|---|---|---|

## Release record (step 8)

One block per shipped piece.

| field | value | source |
|---|---|---|
| cost ceiling, set at step 1 | | `coverage.md` |
| spend | | |
| last reviewed version (sha256) | | the last `process/runs/<run>/panel/round-N.md` |
| shipped version (sha256) | | `sha256sum <piece>` |
| hash match | yes / no | the two lines above |
| round reports = rounds claimed | yes / no | `--panel` |
| check exit | | `tools/check.py` with `--html`, `--claims`, `--panel`, `--reviewed-sha256` |
| open decision rows | | this file |
| live reader requested | yes / no | |
| live reader answered | yes / no; the page says so if no | |
