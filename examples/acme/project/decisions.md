# Decision log (step 7)

Agents prepare the rows. The editor decides the editor's rows and proposes owners for the rest (about 10 to 15
minutes). The named owners at the company close theirs, once they accept. It is the only place where a person
decides. A row goes here when no source can close it: a promise the company would make, a price, a person on
stage, consent, recording, number registration, data handling. The "To confirm" list printed with a piece is
generated from the open rows.

`tools/check.py` reads the killed lines table (`killed-lines` check). The other tables are for people and for
the release gate in step 8.

This file is the Acme Dispatch example. The people are invented: Maria Ortega (founder), Dan Kowalski (head of
product), Priya Shah (support and compliance lead).

Rules
- `owner` is a named person who has agreed to decide. An agent is never an owner. Blank means nobody has.
- `proposed owner` is a guess by role (founder, product lead, compliance owner). Nobody owns a row until they say so.
- A row about the law or a company promise is closed only by its owner, with a date.
- A cut line goes to the killed lines table. It comes back only through a new decision row, named in `reversed by`.

## Decisions

| № | question | recommendation | copy if yes | copy if no | proposed owner | owner | decision | date | round |
|---|---|---|---|---|---|---|---|---|---|
| D-01 | Promise that Job Thread texts are never used for marketing? | keep, bracketed; ask the founder | "[Your customers' texts stay between you and them.]" | cut the sentence | founder | | open | | round 1 |
| D-02 | Who files US carrier registration for a new Pro or Crew owner: Acme or the owner? | leave open in copy; say only that registration is needed | "[Acme files the registration for you.]" | "Each owner registers their own business." | head of product | Dan Kowalski | open, due 2026-10-06 | | round 1 |
| D-03 | Does the launch email carry a price line? | no; prices and the trial live on the page | a price line in the email | prices on the page only | founder | Maria Ortega | no price line in the email | 2026-09-25 | round 1 |
| D-04 | Which plans does the launch email name as having texting? | Pro and Crew only, as the pricing page shows | "Texting is on the Pro and Crew plans." | "Texting is on every plan." | head of product | Dan Kowalski | Pro and Crew only | 2026-09-25 | round 1 |
| D-05 | Is LedgerLite named in launch copy? | yes, in the page and the partner note only | name LedgerLite | "your accounting app" | founder | Maria Ortega | yes, page and partner note only | 2026-09-26 | round 1 |
| D-06 | Does any piece say anything about call recording? | no promise; the page may say the laws differ by state | "Call recording rules differ by state." | cut the sentence | support and compliance lead | Priya Shah | no promise; one neutral sentence on the page | 2026-09-26 | round 1 |

## Killed lines

`tools/check.py` (`killed-lines`) searches the piece and the page for the `pattern` column (a Python regex
between backticks; write a table pipe as `\|`), brackets included. It skips a row whose `reversed by` cell holds a
decision id (`D-n`).

| id | cut line | pattern | cut in | reversed by | came back |
|---|---|---|---|---|---|
| K-01 | "Dispatch on autopilot" | `(?i)\bdispatch on autopilot\b` | round 1, three readers: owners do not want to hand over their day | | |
| K-02 | "Never miss a job again" | `(?i)\bnever miss a (?:job\|call\|text)\b` | round 1, the sceptic and the compliance reader: a promise nobody can keep | | |
| K-03 | "Your whole business in one thread" | `(?i)\bwhole business in one (?:thread\|place)\b` | round 1, the voice editor: not in the corpus | | |

## Release record (step 8)

One block per shipped piece.

| field | value | source |
|---|---|---|
| cost ceiling, set at step 1 | none was set | `coverage.md` |
| spend | not measured | |
| last reviewed version (sha256) | not recorded in this example | the last `process/runs/<run>/panel/round-N.md` |
| shipped version (sha256) | not recorded in this example | `sha256sum <piece>` |
| hash match | not run | the two lines above |
| round reports = rounds claimed | not run; no round is claimed in the final draft | `--panel` |
| check exit | 0 with `--claims`; not run with `--html`, `--panel`, `--reviewed-sha256` | `tools/check.py` |
| open decision rows | 2: D-01 and D-02; the marks D-02 backs are PROPOSAL rows in `claims.csv` | this file |
| live reader requested | no | |
| live reader answered | no; the how-made note says so | |
