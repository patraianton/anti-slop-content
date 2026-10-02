# rules/: general rules for every piece

Rules are general. A piece contributes data, never rules: its facts table, coverage map, claims ledger, numbers file and decision log. Everything specific to a company lives in the project layer (`project/`, see `project/README.md`).

| File | What it is | Version key in `manifest.json` |
|---|---|---|
| `manifest.json` | the only place versions are declared | none |
| `CHANGELOG.md` | dated entries: what changed, why, who asked | none |
| `voice.md` | the generic AI-tell list, the exception rule, the file formats shared with `project/voice.md` | `voice` |
| `landmines/<id>.md` | one landmine each: shapes, cues, fixtures | `landmines.<id>` |
| `examples/` | passages from the fictional project (Acme Dispatch) with a verdict: keep, remove or rewrite; each is also a fixture | none |

`tools/check.py` and `tools/selftest.py` execute the cues and fixtures; more fixtures are in `tools/fixtures/`. The self-test reads only `rules/` and `tools/fixtures/`.

## Landmines

A landmine is a kind of sentence where a wrong line costs the company something it cannot take back.

| id | what it covers | strictness |
|---|---|---|
| `product-claims` | what the product does today: features, screens, menu paths, who can use them | cite-or-cut |
| `compliance-promises` | consent, call recording, sender registration, record keeping, data handling | remove |
| `pricing-plans` | prices, plan names, plan contents, allowances, trials, "every plan" | cite-or-cut |
| `setup-timelines` | how fast or how easy: "right away", "nothing to set up", minutes and weeks | remove |
| `competitors-partners` | rivals, intermediaries, integration partners, gatekeepers, "kill X" framing | remove |
| `numbers-and-sources` | every count, rank, share and quoted figure, and the words around it ("about", "top three") | cite-or-cut |
| `research-absence` | "the product has no X", "X is missing", "nobody offers X", "for the first time" | cite-or-cut |
| `process-claims` | how the work was done: order of steps, what was checked, how many review rounds | cite-or-cut |
| `plain-language` | how copy explains a feature, a price or a step: sentence length, overloaded items, terms, side-note titles, grade | rewrite |

Every landmine has front matter: `id`, `version`, `changed`, `asked_by`, `strictness`, `applies_to`. `applies_to` is `all` (the default) or a list of piece ids from `project/pieces.json`.

Sections, in order: what it is; what it is not (hand-offs); source of truth; forbidden shapes; allowed with a row; detection; fixtures. A forbidden shape is written `- **F1 Name.** ... Class: <slop class>. Severity: <critical|major|minor>.`

## Labels

The label rates the claim, not the type of source.

- **CONFIRMED**: a company document, help article, screenshot or video shows it; URL and date recorded.
- **CLAIMED**: marketing text or an employee's words; nothing shown.
- **ABSENT**: searched where it should be and not found; the row names where it looked.
- **UNKNOWN**: cannot be known without product access.

ABSENT without a `project/coverage.md` row becomes UNKNOWN.

Claim statuses in `project/claims.csv`:

- **SOURCED**: has a row in the facts table.
- **PROPOSAL**: visibly marked on the page as ours, not the company's current product.
- **TO-CONFIRM**: visibly marked, with a named owner who accepted the row, and a date.
- **UNMARKED**: none of the above. Must be zero.

## Results

A check result is `pass | fail | not_run | uncertain`; `not_run` and `uncertain` are never `pass`. Exit codes: `tools/README.md`. Severity is `critical`, `major` or `minor`; no 1 to 10 scores.

Every forbidden shape has at least one `must_fire` fixture with its rule id; `tools/selftest.py` fails a shape without one, or without a severity.

## Strictness

- **remove**: cut the passage, or bracket it as PROPOSAL or TO-CONFIRM (owner and date). A facts row does not clear it: only a named person at the company can make these promises.
- **cite-or-cut**: stays with the right row (facts, numbers, coverage, git); otherwise cut or bracketed.
- **rewrite**: the facts stay; the sentence is split, simplified, or moved to a side note.

Bracketing changes the status from UNMARKED to PROPOSAL or TO-CONFIRM; it does not add facts. TO-CONFIRM marks per piece: `max_marks` in `project/pieces.json` (default 7).

## Slop classes and where each is checked

| class | checked by |
|---|---|
| `invented-fact` | `product-claims`, `pricing-plans`, `setup-timelines`, `compliance-promises`, `process-claims`, `numbers-and-sources` F1 and F5, `competitors-partners` F2 and F3 |
| `filler` | `rules/voice.md` AI-tell list; `plain-language` |
| `empty-structure` | stage 2: each section names the reader decision it serves, or it is cut |
| `false-precision` | `numbers-and-sources`, `process-claims` F2 |
| `false-absence` | `research-absence` |
| `voice-drift` | `project/voice.md` reader words, brief words, never-does list; `plain-language` F4; `competitors-partners` F1 and F5 |
| `contradiction` | `compliance-promises` F2 (one topic, two rules across pieces); `numbers-and-sources` F4; `process-claims` F4; `competitors-partners` F4 |
| `render-artifact` | `tools/check.py` on the rendered page text, with context shown for each hit |

## Versions

Versions are per landmine, plus one for the generic voice file. The `checks` block of `rules/manifest.json` lists the program's own checks (`repeats`, `stray-labels`, `plain`) with a version that is bumped when the program's behaviour for that check changes; nothing reads it yet. A piece is current for a landmine when its newest stamp for it has `result: pass` and `version >= manifest`. Release (`process/LINE.md` step 8) needs a current pass for every landmine the piece carries.

## Detection in three stages

1. **Cues** (`tools/check.py`). Recall-first regular expressions and lookups from each landmine's detection section and from the voice files select **passages**: the matched sentence with one sentence on each side. A cue hit is not a verdict.
2. **Adjudication.** One agent call per hit. It gets the passage, the files the landmine's detection section names (facts table, numbers file, coverage map, decision log, a `git log` printout) and the landmine's forbidden and allowed lists, not what the piece is trying to say. The prompt says: "Do not invent a defect to look useful. Do not soften a real one. If the passage is clean, say so." It returns `{rule, result: pass|fail|uncertain, quote, severity, action: cut|bracket|cite|keep, row}`. `uncertain` goes to the editor. An agent never writes a decision row or its own stamp.
3. **Stamp.** One JSON line in `<piece>.stamps.jsonl` next to the draft: `{landmine, version, date, result, hits, by, piece_sha256}`. `python tools/check.py <piece> --stamp` writes stage-1 stamps (`by: "tools/check.py stage 1"`; `pass` only with zero hits). Stage 2 appends one stamp per landmine, `by` naming the model, `pass` only when every stage-1 hit has a stage-2 `pass`. Optional keys: `hits_cleared`, `rows`, `git_head`.

This repository ships no stage-2 stamp. Stage 2 is run by an agent call or by the editor on your own pieces.

## How to change a rule

1. Edit the landmine file and its fixtures together.
2. Bump `version` in the front matter and in `rules/manifest.json`.
3. Add a `rules/CHANGELOG.md` entry: what changed, why, who asked.
4. `python tools/selftest.py` exits 0.
5. One rule change per commit; if a hard rule changed, update `CLAUDE.md` in the same commit.

Fixtures are synthetic: an Acme Dispatch sentence with the same shape the rule tests, with `source` set to `synthetic (Acme), shape: <one clause>`. A real miss from your own project becomes a fixture rewritten the same way, with no company text in it.

## What rules are not

- Not a fact check: a wrong CONFIRMED row passes every cue; rows are challenged in `process/LINE.md` step 3.
- Not a score: a piece passes or fails per landmine.
- Not a project: no company name, price, number or decision belongs in `rules/`; it belongs in `project/`.
