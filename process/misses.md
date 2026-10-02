# Misses log

A miss is a defect that got past the line and was found later. Each miss gets one row. The row names the shape of the defect, not the piece it happened in, and points to what catches that shape now.

Format of a row:

| Column | Content |
|---|---|
| id | `M-01`, `M-02`, in order of entry. Never renumbered. |
| step | The step of `process/LINE.md` that should have caught it. |
| what went wrong | The shape of the defect in one or two sentences. No quote of the piece. |
| how it was found | A review round, a separate audit, an outside reader, an editor's read, or `tools/check.py`. |
| the fixture or rule that now catches it | A landmine id with the rule (for example `numbers-and-sources` F2), a named check, or a template. A fixture id from `tools/fixtures/` if one exists. "open" if nothing catches it yet. |

The first 18 rows (M-01 to M-18) are the lessons this repository started with, written as generic shapes. They stay as they are. A project keeps its own misses in `project/misses.md`, in this format, with ids prefixed by the project name (for example `ACME-M-01`), so two projects never share an id.

| id | step | what went wrong | how it was found | the fixture or rule that now catches it |
|---|---|---|---|---|
| M-01 | 4 | Invented product details written as plain fact: a named tab, a sender address, "live on all plans", a workflow that "does it for you", "nothing to set up". The writer had a brief and a voice guide but no claims ledger, so nothing counted unmarked claims before a reader saw the draft. | Review round | `product-claims` F1, `setup-timelines`, `pricing-plans`, `compliance-promises`. Step 4: UNMARKED = 0 in `project/claims.csv`. |
| M-02 | 1, 3 | The brief called several existing features absent. It had read the help center, the blog, the site and a few recordings, not the full video archive. Its confidence grade rated the type of source, not the claim. Review rounds read the same research folder and agreed with it. | Separate audit that opened the full archive | `research-absence` F1, F2, F4. `project/coverage.md`. Step 3, the refute pass before the draft. |
| M-03 | 5 | Stray label words printed as text in the rendered page, left by a markup rework. The check after the edit measured word counts and page height and never read the rendered text. The planned search for the strings stayed a sentence in a report. | Review round | `stray-labels` check in `tools/check.py` (rendered text against the source file, hits shown with context). |
| M-04 | 7 | Cut lines came back. A cut promise regrew in new words. A removed promise was added again. A new promise was added by a script with no review and no decision row. No list of killed lines existed, and review had already ended. | Process audit | `killed-lines` table in `project/decisions.md`, checked by `tools/check.py`. `setup-timelines` F2. The regrown wordings are `must_fire` fixtures. |
| M-05 | 8 | A process sentence ("before writing, I checked every public source") that the version log contradicts. The research file is dated after the first draft. Nothing compared process sentences with dates. | Outside reader and a hunt for slop | `process-claims` F1, F2. Step 8, the how-made note built from `project/coverage.md` and `git log`. |
| M-06 | 4 | A rank ("a top-ten complaint") typed by hand. The source table puts the item last. No counts file computed the rank. | Hunt for slop | `numbers-and-sources` F2. Ranks come from `project/numbers.json`. |
| M-07 | 4 | A round number ("about 500 posts") with no source file. The real counts were different and sat in a research note. A reviewer's replacement text had changed the number without a source. | Hunt for slop | `numbers-and-sources` F1, F4. `project/numbers.json`. |
| M-08 | 4 | One count with three versions in the research notes. The copy printed a fourth reading. Reviewers compared the copy with the note, not with the raw list the note came from. | Hunt for slop, outside reader | `numbers-and-sources` F1. One record per count in `project/numbers.json`, with its source row. |
| M-09 | 4 | A headline count shipped without the caveats the study attached to it: two lanes overlapped on one source set, part of the records came from the wrong audience. The caveat lived in the study, not next to the number. | Outside reader | `numbers-and-sources` F3. Approximate means "about", and the caveat travels with the number. |
| M-10 | 2 | A quote introduced as "one agent put it" when the speaker ran a team and had a different role. The quote was copied without the speaker's role. | Hunt for slop | `numbers-and-sources` F5. A quote row carries the speaker's role (Quotes table in `project/facts.md`). |
| M-11 | 4 | "None" in the copy where the study said "almost none" (three records). Checked against the study later, the absolute stood for the topic asked about. The risk is real: a softened qualifier becomes an absolute. | Hunt for slop | `numbers-and-sources`. The ledger row cites the exact count behind every "none". |
| M-12 | 5, 7 | Two different rules for one feature in two pieces. In one the rule was in brackets, in the other it was plain. Consent was bracketed in one and unbracketed in the other. Reviewers read pieces, not one claim across pieces, and no row said who decides. | Outside reader | `compliance-promises` F2, class `contradiction`. One decision row per feature rule in `project/decisions.md`. |
| M-13 | 5 | "Connect once and it works right away" next to an appendix that calls the same setup the heaviest build of the project. The appendix and the email were edited separately. | Outside reader | `setup-timelines` F1. |
| M-14 | 4, 7 | Far more "to confirm" marks in an email than the panel's own limit. The "To confirm" list had no owners and no dates. Edits after the last round were not recounted, and the limit was only a sentence in a report. | Process audit | TO-CONFIRM needs an owner and a date in `project/claims.csv`. `mark-budget` counts the marked spans per section against `max_marks` in `project/pieces.json`. `project/decisions.md`. |
| M-15 | 6, 8 | The page said "several review rounds" while many fix scripts had run after the last round and no review report existed after it. Nothing compared the shipped text with the last reviewed text. | Process audit | `process-claims` F3 and F4. `release-hash` with `--reviewed-sha256`. |
| M-16 | 6 | Review lenses were prompts on one model family reading one research folder. Every report said all lenses agreed. Personas drifted between rounds. Scores of 1-10 rose while false claims stayed in. Reviewers wrote errors of their own, and their replacement text was applied without the checks a draft gets. | Process audit, outside reader | `project/panel/personas.md` and `project/panel/round.md`. Step 6: another model family, a cold reviewer, an adversary with a quota, pass or fail per slop class, no scores. |
| M-17 | 1 | The copy argues against a rival and never says that the company depends on a product the rival's parent also sells. The rival's name was taken at face value. Nobody asked what it means inside the company. | Separate audit | `competitors-partners`. Step 1, the frame table. Open as a rule: no cue can find a missing admission. |
| M-18 | 5 | The first full run of the program on a text that review rounds had passed still found critical promise findings and many others. Reviewers had found some of the same lines by hand later. No list of landmines had been run on any version. | `tools/check.py`, run on the passed version | `tools/check.py` on every version at step 5. Record each run in `process/runs/`. |

## Counts

18 rows. Found by review rounds: 2 (M-01, M-03). Found by a separate audit, an outside reader or a hunt for slop after the last round: 15. Found by `tools/check.py`: 1 (M-18). Open as a rule: M-17.

A new miss in a project gets a row in `project/misses.md`. A miss that shows a gap in a generic rule gets a fixture in `tools/fixtures/must_fire.jsonl` and, if a rule changed, an entry in `rules/CHANGELOG.md`.
