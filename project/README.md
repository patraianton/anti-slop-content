# project/: the project layer

The rules in `rules/` are the same for every company. This folder holds what is specific to yours: piece types,
voice, facts, numbers, decisions. It ships blank: every table is empty and no
rule in these files is active until you add a row, so the checker reads nothing company-specific from it. Each markdown file
has a header that says which step of `process/LINE.md` fills it, who fills it, and what `tools/check.py` reads from it. The
three data files cannot hold a header: `pieces.json` (format in `tools/README.md`), `numbers.json` (a list of records, format in
`tools/README.md`) and `claims.csv` (the columns listed under "Rules for filling"). A filled example with rows from the
fictional company Acme Dispatch is in `examples/acme/project/`.

Copy nothing from another company's project. `examples/acme/project/` shows the shape of a filled layer; do not
copy its rows. Fill these files in place, or copy this whole folder once to a new folder and pass it with
`--project <folder>`.

## Order and time

Times are estimates for a first project, with an agent doing the research and drafting. Later projects are faster.

| order | file | step | who fills it | time |
|---|---|---|---|---|
| 1 | `pieces.json` | before step 1 | editor | 5 minutes: keep the five piece types or edit them. Headings in a draft are written as the piece id, for example `## email` (see "Your first draft" in the root `README.md`) |
| 2 | `voice.md` | before step 1 | agent counts, editor approves | 1 to 2 hours with 20 or more real pieces from the company to count from. With fewer, use the "no corpus yet" mode below |
| 3 | `coverage.md` | 1 | agent | 30 to 60 minutes. The editor adds the feature list and the cost ceiling (5 minutes) |
| 4 | `facts.md` | 2 and 3 | agents, one on another model family | 1 to 3 hours, mostly research. The refute pass adds about 10 minutes |
| 5 | `numbers.json` | 4 | agent | 20 minutes at the start, then one record each time the draft prints a new count |
| 6 | `decisions.md` | 7 | agent prepares, editor decides | 10 to 15 minutes of the editor's time per piece |
| 7 | `panel/personas.md` | 6 | editor with an agent | 30 minutes, once. Then it stays pinned |
| 8 | `calibration.md` | before step 4 and each quarter | agent runs, editor reads | 30 minutes with 20 pieces |

### Calibrate before you trust the cues

Run the checker on the company's own approved, human-written copy and count how often each cue fires. A cue that fires on a large share of that copy is a house habit, so it gets an `allowed` row or a lower stage, not a ban. See `calibration.md`.

### No corpus yet

A new company, a new product line or a rebrand may have fewer than 20 pieces. Then fill `voice.md` in this order. Keep the
generic list in `rules/voice.md` and add no `allowed` row. In sections 2 and 3 write each form and reader word as a decision by
the editor, marked "decided, not counted", with no number. Fill section 5 from the brief. Leave sections 4 and 7 empty. Count
again after the first 20 pieces ship, and replace the decisions with counts.

Not read by the checker, but part of the line: `claims.csv` (step 4, filled with the draft), `misses.md` (a log of defects found late, same format as `process/misses.md`), `panel/round.md`
(a template; copy it to `process/runs/<run>/panel/round-N.md` for each round, so two pieces never share a panel folder), `plain-pass.md` (the prompt for step 4.5).

## What each check reads

| file | flag that overrides it | read by |
|---|---|---|
| `pieces.json` | `--project` only | every check that tags a piece by its `##` heading: `voice`, `plain` (which pieces, grade limits, hook), `mark-budget` (`max_marks`, `dotted_class`), `stray-labels` (`labels`) |
| `voice.md` | `--project` only (`--voice` takes the generic file) | `voice` (banned cues, `allowed` exceptions, the never-does table), `plain` F4 (the `terms` block), `stray-labels` (the `labels` block) |
| `coverage.md` | `--coverage` | `landmines`: `research-absence` F2 (an ABSENT row must name a covered row) |
| `facts.md` | `--facts` | `landmines` whose target is facts: `research-absence` F1, F2, F4; `product-claims` F2. Also the count of overturned rows |
| `numbers.json` | `--numbers` | `numbers` (`numbers-and-sources` F1, F3, F4) and the rank and share cues (F2) |
| `claims.csv` | `--claims` (not required) | `claims` (UNMARKED, TO-CONFIRM without owner or date) |
| `decisions.md` | `--decisions` | `killed-lines` (the `pattern` column of the Killed lines table) |
| the folder `process/runs/<run>/panel/` of `round-N.md` reports | `--panel` | `process-claims` F3 (round count against report files) |
| the hash in the last round report | `--reviewed-sha256` | `release-hash` and `process-claims` F4 |

`--project <folder>` sets the defaults of all the flags above to the files in that folder. The default is
`project/`. Exact flags, file formats and exit codes: `tools/README.md`.

## Rules for filling

- A blank table is fine. The checker marks a check `not_run` when its input is empty, and fails with exit 3 only
  when a landmine targets that file and the piece carries the cue.
- Do not rename a column the checker reads: `claim`, `label`, `where_searched` and `refute` (facts); `id`, `total`,
  `read fully` and `keyword-searched` (coverage); `pattern` and `reversed by` (killed lines);
  `id,claim,piece,status,facts_row,owner,due,where_in_text` (claims).
- Keep rows from another company out of your project. The rows in `examples/acme/project/` show the shape only.
- Every markdown file keeps its header. A reader who opens one file must learn which step fills it and who.
