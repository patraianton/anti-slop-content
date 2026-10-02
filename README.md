# anti-slop-content

Rules, a checker and an eight-step line for agent-written marketing copy: launch emails, posts, landing pages, partner notes and "how this was made" notes. Each rule is a landmine: a kind of sentence agents get wrong, with its source of truth, regex cues and fixtures. A Python program (standard library only) runs the cues. The rules are the same for every product. Everything specific to a company lives in one folder, `project/`. It is for anyone who ships copy that an agent wrote and a person signs.

## How it works

1. **Landmines are data.** Each file in `rules/landmines/` holds the forbidden shapes, the allowed exceptions, the cues and the fixtures. The checker reads them; nothing is hard-coded.
2. **Cues, then adjudication, then stamp.** Cues select passages. An agent or the editor decides each hit. A stamp records the result per landmine, version and piece hash.
3. **The line has eight steps, plus a plain pass 4.5** (`process/LINE.md`): from framing the brief to a release whose hash matches the last review. Each step has an artifact and a check.
4. **The project layer holds the company.** Voice, piece types, facts, numbers, decisions and reviewer personas sit in `project/`. A fictional company in `examples/acme/` shows a filled layer.

## Run it

```
python tools/selftest.py
python tools/check.py examples/acme/drafts/final.md --project examples/acme/project --claims examples/acme/project/claims.csv
python tools/check.py examples/acme/drafts/v1.md --project examples/acme/project
```

| command | exit | meaning |
|---|---|---|
| `selftest.py` | 0 | every cue and fixture holds |
| `check.py` on `final.md` | 0 | no findings |
| `check.py` on `v1.md` | 1 | findings in at least five landmines, plus voice, numbers and killed lines |

Exit 0 is clean, 1 is findings, 3 is a check that could not run. Flags and file formats: `tools/README.md`.

## Set it up for your product

Follow `project/README.md`. It lists the files in order, who fills each one and what the checker reads from it. Expect about half a day for a first project when the company has a corpus of past copy to count from, mostly agent research; a company with none uses the "no corpus yet" mode there. The editor's own time is the feature list, the cost ceiling and the decisions.

Before the first draft, calibrate the cues on the company's own approved copy with `project/calibration.md`.

## Your first run

1. Copy `project/` to `projects/<name>/` (one folder per product) and fill the files in the order of `project/README.md`.
2. Write the draft (next section).
3. Run `python tools/check.py process/runs/<date>-<piece>/draft.md --project projects/<name> --claims projects/<name>/claims.csv`.
4. Read the exit code: 0 clean, 1 findings to fix or explain, 3 a check could not run, so the step is not done.

`--project` is needed for any folder other than `project/`. `CLAUDE.md` and `AGENTS.md` say `project/`: read it as your project folder.

## Your first draft

Put the draft at `process/runs/YYYY-MM-DD-<piece>/draft.md`. Write one `##` heading per piece, and write the heading as the piece id from `pieces.json`: `## email`, `## social`, `## page`, `## partner-note`, `## how-made`. Text outside a `##` heading belongs to no piece, so the `plain` check does not read it. A file with no piece heading can be tagged with `--piece-type <id>`. After a run, read the `plain` line of the summary: "grade none" means nothing was read, and the check has not passed in any useful sense.

```
## email
Hi [First name],

Your first paragraph, the hook. One idea per sentence.

## social
Your post.
```

Copy `examples/acme/drafts/final.md` for a longer shape.

## The eight steps (and the plain pass)

1. Frame and coverage: map every source type before the first line of copy.
2. Facts table: each fact CONFIRMED, CLAIMED, ABSENT or UNKNOWN, with a date.
3. Refute pass: an agent on another model family tries to overturn the facts.
4. Draft with a claims ledger and a numbers file; no unmarked claim.
4.5. Plain pass: one idea per sentence, in the company's words.
5. Lint: `tools/check.py` on every version, exit 0 before anyone reads.
6. Blind check and one review round: pinned personas, severities, no scores.
7. Decision log: a promise in the company's name is closed by a named owner.
8. Release with hash match: the shipped text equals the last reviewed text.

## The nine landmines

- `product-claims` (cite-or-cut): what the product does today.
- `compliance-promises` (remove): consent, recording, registration, retention, data use.
- `pricing-plans` (cite-or-cut): prices, plan names, plan contents, trials.
- `setup-timelines` (remove): "right away", "nothing to set up", minutes and weeks.
- `competitors-partners` (remove): rivals, intermediaries, integration partners, gatekeepers.
- `numbers-and-sources` (cite-or-cut): every count, rank, share and quote.
- `research-absence` (cite-or-cut): "the product has no X" without where it looked.
- `process-claims` (cite-or-cut): how the work was done, coverage, review rounds.
- `plain-language` (rewrite): long sentences, overloaded items, unexplained terms.

## Origin

Built in 2026 for one real B2B launch. The company is not named. The first checker run on the text gave 189 findings on a version that earlier review rounds had passed. The released version gave 0. The rules, cues and fixtures were then extracted, generalized and made synthetic, and the company data moved into the project layer.

## Limits

- The checker matches words and numbers, not meaning. A false sentence with no number and no banned word passes it.
- One model family wrote and reviewed the first piece. Use a second family at steps 3 and 6.
- Nothing here measures whether copy works on readers.
- The AI-tell list decays as models change. Calibrate on your own approved copy and review quarterly (`rules/voice.md`, section 5).

## Related work

Neighbouring projects check how text sounds: word lists, style rules and scores. This repo adds a check on whether a sentence may be said at all: a source of truth, a claims ledger, a log of killed lines, and a release whose hash matches the last review. They solve different problems, and several do their part better. Use them next to this repo.

- [slopscore](https://github.com/jman4162/slopscore): a Python checker with a 0 to 100 score; every hit carries a quote and its rule source. Its table of false positives on clean human text is the model for `project/calibration.md`.
- [snifftest](https://github.com/DanRWilloughby/snifftest): 15 rules in one YAML file, some by regex and some by model judge. Its per-rule "do not count" field is better than ours.
- [sloplint](https://github.com/benjaminjackson/sloplint): 84 regex rules with severity and confidence, an optional model judge and exit code 3 when the judge is down. It describes a similar three-stage design; we have not read its code.
- [quiron](https://github.com/ilien-dev/quiron): compares a text with norm bands taken from 324 human texts written before 2022. Use it for bands instead of blind word lists.
- [plain-english](https://github.com/nordscope-fi/plain-english): 88 YAML rules with exceptions and a source for each rule. Weak signals count only in a pile; use it for exceptions.
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing): a skill and a detector with a folder of 376 human texts. It sets thresholds from data: threshold 0 rejects 31.4% of human texts, threshold 6 rejects 1.9%.
- [Vale with the Microsoft and Google packages](https://github.com/vale-cli/Microsoft): style-guide rules in YAML, with test samples next to each rule. Use it for general style and grammar.
- [blader/humanizer](https://github.com/blader/humanizer): the most used "remove AI style" skill, 26 patterns taken from Wikipedia. It marks weak patterns as weak and has a "when not to touch" block.
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): a field guide by editors, with real examples and tells dated by model era. The source most of the above cite.
- [claude-for-legal: marketing-claims-review](https://github.com/anthropics/claude-for-legal/blob/main/product-legal/skills/marketing-claims-review/SKILL.md): pulls out each claim, sorts it by type (vague, comparative, implied, absolute) and looks for proof. Use its claim types as a start for your own landmines.

## Licence

MIT. See `LICENSE`.
