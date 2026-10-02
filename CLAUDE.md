# CLAUDE.md: agent entry for anti-slop-content

Project folder: `project/` unless the editor names another folder; wherever this file says `project/`, use that folder and pass `--project <folder>` to the checker.

Read first: `process/LINE.md`, `rules/README.md`, `rules/voice.md`, `project/voice.md`, `project/pieces.json`, the landmine for every topic the piece touches, the file in `project/` for your step, `process/misses.md`.

## Hard rules

1. UNMARKED is zero: every factual sentence in customer copy is SOURCED, PROPOSAL or TO-CONFIRM (`project/claims.csv`).
2. ABSENT names where it looked; without a coverage row it is UNKNOWN (`project/coverage.md`).
3. Every number has a row in `project/numbers.json`; ranks and shares are computed; approximate counts say "about".
4. Promises on consent, call recording, retention, export and data sharing are closed only by a named owner at the company (`project/decisions.md`).
5. A cut line stays cut in any wording unless a decision row reverses it in the killed-lines table.
6. A sentence about how the work was done is checked against file dates and `git log`.
7. A check result is `pass | fail | not_run | uncertain`; only `pass` is pass; exit 3 outranks 1.
8. Reviewers use the pinned personas (`project/panel/personas.md`), report per slop class with severity critical, major or minor, no 1-10 scores; their replacement text passes steps 4 and 5 first.
9. Ship only the text whose sha256 equals the last reviewed version; only the editor sends it.
10. Voice comes from two files: `rules/voice.md` (the AI tells) and `project/voice.md` (the company's own words and exceptions). No em dashes (the one exception is `examples/acme/drafts/v1.md`, which holds one on purpose as test data; exclude that path from a repo-wide em dash search). No banned word without a counted exception in `project/voice.md`.

Piece types come from `project/pieces.json`, not from code. Do not add a piece type anywhere else.

## Conventions

- English. A sentence that adds nothing is cut.
- A rule changes only through the five steps in `rules/README.md`, "How to change a rule".
- A new miss goes to `project/misses.md` with the file that proves it. A miss that shows a gap in a generic rule also goes to `tools/fixtures/must_fire.jsonl`.
