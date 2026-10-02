# The line: eight steps from brief to send

Every piece (email, post, page, partner note, how-made note) goes through these steps in order. A step is done when its check passes. `not_run` and `uncertain` do not count.

Roles: **agent** writes and fills files. **Program** is `tools/check.py`. **The editor** is the human running the line and the only one who decides. **The named owner** is the person at the company who closes a row.

Proposed owners, by role: the owner of the product area for what the product does, the legal or compliance owner for any promise a regulator could read, the finance owner for prices and rates, the founder or brand owner for company promises. The editor writes the real names in `project/decisions.md`; a small company may have one person for several roles. A row is closed only after the person has accepted it.

The editor never hands off: promises in the company's name, prices, named speakers, legal lines, the final read, the send.

## Two ways to run the line

- **Outside writer.** The editor works for the company from outside and reads only public sources. The source types of step 1 are the help center, every video with captions, the pricing archive, blog and posts, third-party demos and the product (a trial, if any). The how-made note is part of the kit.
- **In-house.** The editor works inside the company. The source types of step 1 are the product spec, the pricing and legal sheet, the live product and the support tickets. There is no video archive to cover. The how-made note is optional: remove the `how-made` piece from `project/pieces.json` and the line skips every sentence about how the work was done. Step 8 then needs no how-made note.

Either way, write the source types you chose into `project/coverage.md` at step 1.

## Time

The editor's time per piece is spent at steps 1, 3, 6, 7 and 8. This is an estimate until a project measures it. Once a quarter, add the time to mark 20 reviewer findings agree or disagree.

## 1. Frame and coverage

Before the first line of copy: what the brief's words mean inside the company, and a coverage map of sources (type | total | read in full | searched by keyword | not covered).

- **Who:** agent builds it. The editor gives the feature list, trial access if any, and the cost ceiling (5 min).
- **Artifact:** `project/coverage.md` (frame table, ceiling line, coverage table).
- **Check:** every source type of your way of running the line has a row (see "Two ways to run the line"). A type that was neither searched nor read in full carries "no absence claims for this type". `tools/check.py` fires research-absence F2 on an ABSENT row that names it. The file's commit is older than the first draft commit (checked by hand with `git log`). Any "I checked N ..." sentence in the how-made note takes N from this file.

## 2. Facts table

One row per fact, labelled CONFIRMED, CLAIMED, ABSENT or UNKNOWN, with an "as of" date and "applies to" (which plan, which seat). A quote is one row of the Quotes table: text, speaker, speaker's role, weight. The label rates the claim, not the type of source.

- **Who:** agents, several lanes, one lane on a different model family.
- **Artifact:** `project/facts.md`.
- **Check:** ABSENT without a coverage id fails (research-absence F1). CONFIRMED without a date fails (product-claims F2). A quote without the speaker's role fails (stage 2).

## 3. Refute pass

Before any draft exists, a separate agent on another model family gets only the facts table and tries to overturn CONFIRMED and ABSENT rows. It writes the result in each row's `refute` cell. Each overturned row is logged as a miss in `process/misses.md`.

- **Who:** agent (different model family). The editor reads only the overturned rows (10 min).
- **Artifact:** the `refute` column of `project/facts.md`; `process/misses.md`.
- **Check:** an ABSENT row with an empty `refute` cell fails (research-absence F4). `tools/check.py` prints the number of rows marked `overturned`. The pass is run again until a run overturns none. That count goes into the how-made note.

## 4. Draft with claims ledger and numbers file

The draft is written from the facts table. Every factual sentence gets a ledger row with a status: SOURCED, PROPOSAL, TO-CONFIRM (owner, date). Every count lives in one numbers file with its source row and a flag: exact, approximate, double-counted, lane stopped. Ranks and shares are computed by the program. Every section names the reader decision it serves.

- **Who:** agent writes and fills. Program computes. The editor spends 0 min.
- **Artifact:** `project/claims.csv`, `project/numbers.json`.
- **Check:** UNMARKED = 0 and every TO-CONFIRM has an accepted owner and a date (`claims`). A number in the text not found in `numbers.json` fails (numbers-and-sources F1, F4). "Approximate" in the source means "about" in the text (F3). A rank or share without a computed row fails (F2). At most `max_marks` TO-CONFIRM marks in one section, set in `project/pieces.json` (`mark-budget`). A section with no named reader decision is cut (stage 2).

## 4.5. Plain pass

The draft is rewritten in plain words, one idea per sentence, before the lint. Long sentences are split, overloaded items are cut down, terms are explained, history and reasons move to side notes. Facts, marks and structure stay. The hook and quoted speech are not touched.

- **Who:** agent with `project/plain-pass.md`. The editor spends 0 min.
- **Artifact:** `plain-pass.md` in the run folder (`process/runs/<run>/`): the `was -> now` list, one line per changed sentence.
- **Check:** `tools/check.py` check `plain` at 0 (`rules/landmines/plain-language.md` F1-F7, with the grade per section in the summary).

## 5. Lint

`tools/check.py` runs on every version before any reviewer. It covers:

- landmine cues;
- banned words and shapes from `rules/voice.md` and `project/voice.md`;
- stray label words in the rendered page text (shown with context, not as a bare count);
- sentence-level diff between the text file and the page;
- repeats of 8 words or more;
- one feature with one rule in every piece (compliance-promises F2);
- lines cut by an earlier decision (`killed-lines`, from the table in `project/decisions.md`).

`python tools/selftest.py` runs the fixtures after every change to the rules or the program.

Before the first lint of a new project, run the calibration in `project/calibration.md`, so the editor knows which cues are house habits.

- **Who:** program. The editor does not read the text until this step is clean.
- **Artifact:** the `tools/check.py` report for the version, kept next to the draft in `process/runs/<run>/`. With `--stamp`, one record per landmine in `<piece>.stamps.jsonl`.
- **Check:** exit 0, or a written reason per finding. An exception to the banned list exists only as a line in an `allowed` block of `project/voice.md`, with the company's own usage count.

## 6. Blind check and one review round

The fact check reads the claims ledger and sources, not the draft. A separate lane compares each factual sentence with its source row for meaning (lost caveats, ranges). Reader personas are written down once and do not change. One reviewer is from another model family. One is cold (no research folder). One is an adversary with a quota: three false claims, or a written reason there are none. Results are pass or fail per slop class with severity critical, major or minor. No 1-10 scores. Replacement text from reviewers goes through steps 4 and 5 before it is applied. A second round, if any, only cuts.

- **Who:** agents. The editor reads only the critical rows (10 min).
- **Artifact:** `project/panel/personas.md` (pinned once) and one report per round, `process/runs/<run>/panel/round-N.md`, copied from `project/panel/round.md`. Release step 8 passes that folder to `--panel`.
- **Check:** a verdict repeated word for word from a previous round is not accepted. A replacement without a source line is not applied. A round without a report file did not happen. At the last round, critical = 0 and new customer-copy sentences = 0.

## 7. Decision log

The only place the editor decides. Everything a source cannot close goes here: promises in the company's name, prices, people on stage, consent capture, call recording, number registration, data sharing and export. A cut line goes to the killed-lines table. A live reader from the audience is requested here.

- **Who:** agent prepares rows. The editor decides their own and proposes owners for the rest (10-15 min). The named owners close theirs, once they accept.
- **Artifact:** `project/decisions.md` (decisions, killed lines, release record). The "To confirm" list in the copy is generated from it.
- **Check:** customer copy has 0 rows without a decision or an owner. Legal and company-promise rows are closed by a named person, not an agent. A killed line comes back only with a decision id in `reversed by`. The release record says whether a live reader was asked and answered. If not, the page says so.

## 8. Release with hash match

The hash of the shipped text equals the hash of the last reviewed version. If the piece set has a how-made note, it is built from `project/coverage.md`, the refute count, the round reports and `git log`, not from memory. The spend is written next to the ceiling from step 1.

- **Who:** program and agent. The editor spends 5 min on the final read and the send.
- **Artifact:** the release record in `project/decisions.md`. A line in the how-made note: "reviewed version vN, sha256 ...". A one-page index for a reviewer at the company, `process/runs/<run>/index.md`, with five links: facts table, claims ledger, round reports, decision log, version log (the version log is `git log` of the run folder).
- **Check:** (`--html` is optional. The page is any HTML export of the draft, with each TO-CONFIRM mark in `<span class="tbc">`. Without it `parity` and `stray-labels` are `not_run`.) `python tools/check.py <piece> --html <page> --claims <ledger> --panel <panel folder> --reviewed-sha256 <hash in the last round report>`. A hash mismatch fails `release-hash` and gives process-claims F4 on every round-count sentence. Send is blocked. A round count above the number of `round-*.md` reports fails process-claims F3. Sentences about the order of work are checked against `git log` by hand (process-claims F1, F6). Spend over the ceiling is the editor's call, written in the release record.

## What the line counts

| Measure | Target | Measured by | Why it is measured |
|---|---|---|---|
| UNMARKED claims in customer copy | 0 | `claims` check on the ledger | An unmarked claim reaches a reader with no source and no owner. |
| TO-CONFIRM marks in one email | at most `max_marks`, each with an owner | `mark-budget`; `claims` | Too many open marks mean the piece is not ready, and a mark with no owner never closes. |
| Numbers not found in the numbers file | 0 | `numbers` | A count typed by hand drifts from its source. |
| ABSENT rows overturned before the draft | 0 after the last refute run | `landmines` note: "N overturned" | A false "the company does not have X" is the costliest error in the copy. |
| Audit corrections to finished copy | at most 2 | by hand, from the corrections listed in the run `README.md` | Many late corrections show that steps 1 to 5 did not work. |
| Errors written by reviewers | 0 | by hand, from the round reports | A reviewer's replacement text can add a new false claim. |
| Cut lines that came back | 0 | `killed-lines` | A line cut once returns when nobody keeps the list. |
| Shipped hash = last reviewed hash | yes | `release-hash` | Edits after the last review ship unread. |
| Live reader before send | yes, or the page says no | by hand, release record | Simulated readers are not a live reader. |
| `tools/check.py` findings on the shipped version | 0, or a written reason per finding | `tools/check.py` | The program is the only check that reads every line of every version. |
| Spend against the ceiling from step 1 | at or under | release record | The line adds agent time, and a ceiling keeps it a choice. |
| Reviewer findings the editor agrees with, on 20 marked findings | threshold set after the first marking | by hand, once a quarter | It shows whether reviewers find real problems or noise. |

## Limits

- The program matches numbers, words, repeats and mismatches, not meaning. A false sentence with no number and no banned word passes it. Steps 3 and 6 carry the rest.
- The facts table and claims ledger are filled by a model. What is not written down as a row is not checked.
- Without product access part of the facts table stays UNKNOWN, and those lines stay marked in the copy.
- Personas are simulated readers, not a live reader.
- One model family wrote and reviewed the first piece. Use a second family at steps 3 and 6, or the line shares one set of blind spots.
- Steps 1 and 3 and a review of the shipped version add agent time per piece.
- Legal and company-promise rows wait for named people at the company.
- Nothing here measures whether the copy works on readers.
- The steps were written after the first piece they cover. Record the first run from step 1 to step 8 in `process/runs/`, or the order is untested.
