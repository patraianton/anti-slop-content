---
id: process-claims
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: cite-or-cut
applies_to: all
---

# Landmine: claims about how the work was done

## 1. What this landmine is

Any sentence about the making of the piece: the order of steps ("before writing, I checked"), coverage
("every public source"), duration ("built in one night"), review ("three review rounds of five readers"),
headcount ("a crew of agents", "five reviewers").

Strictness `cite-or-cut`: a process claim is generated from the record on disk or checked against it.

## 2. What it is not (hand-offs)

- Counts inside the research ("335 complaints", "41 help center articles" as a total) go to
  `numbers-and-sources`. This file owns the counts of the process: rounds, readers, agents, scripts, hours.
- Where a feature was searched for, as evidence for an ABSENT, goes to `research-absence`. This file checks
  the sentence that describes coverage to the reader; both read `project/coverage.md`.
- What the product does or does not do goes to `product-claims`, even when the sentence starts with "I checked".
- How long the reader's setup takes goes to `setup-timelines`. This file owns how long the making took.
- A promise about review by a lawyer or another named function goes to `compliance-promises`.
- Sentence length and word choice in the how-made note go to `plain-language`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The version history of the piece's folder (`git log`, or the revision list of the tool that holds the
   piece): commit times and messages.
2. File times and contents on disk: research notes, fix scripts, `process/runs/<run>/panel/round-N.md`. One report file per
   round claimed.
3. `project/coverage.md`: `read fully` and `keyword-searched` per source type. "Every", "all" and
   "read" resolve here.
4. The release hash (`process/LINE.md` step 8): the sha256 of the shipped text against the hash of the
   version the last round reviewed.

Never a source: the writer's memory, a plan file that describes the intended order, a reviewer's summary
of the process, the previous version of the how-made section.

A process sentence that also states a product fact ("the app has had texting since 2021") is not resolved
here. That fact goes to the landmine that owns it, and its source is the company's help center or docs
(dated), a `CONFIRMED` row in `project/facts.md`, a `project/decisions.md` row owned by a named owner,
or the gatekeeper's own documentation.

## 4. Forbidden shapes (banned by shape)

- **F1 Order of work contradicted by timestamps.** "Before writing, I checked ..." where the file that did
  the checking is newer than the first draft commit. Class: invented-fact. Severity: critical.
- **F2 "Every" over a keyword scan.** "every source", "all the videos", "checked every" for a type where
  `project/coverage.md` shows part keyword-searched or not covered. Class: false-precision. Severity: major.
- **F3 Round count without a report per round.** "N review rounds" where the panel folder holds fewer than
  N `round-*.md` reports. Class: invented-fact. Severity: major.
- **F4 Review claim over unreviewed text.** A round count printed in a text whose sha256 differs from the
  version the last round reviewed. Class: contradiction. Severity: critical.
- **F5 Headcount that implies people or independence.** "five readers (a plumbing owner, an office manager ...)"
  for prompts of one model family on one research folder, without saying they are simulated roles.
  Class: invented-fact. Severity: major.
- **F6 Duration contradicted by timestamps.** "In one night" where commits and fix scripts span longer.
  Class: invented-fact. Severity: minor.

## 5. Allowed with a row

- **A1** An order claim that matches the version history: "git shows the order: draft first, audit second."
- **A2** A neutral coverage verb with counts from `project/coverage.md` ("all 41 help center articles" where
  the row says 41 of 41 opened).
- **A3** A round count equal to the report files, on the reviewed text, with what came after named:
  "three review rounds on v1 to v4; seven fix scripts after the last one, not reviewed".
- **A4** Simulated roles named as such: "five reader roles, one model family, one research folder".

## 6. Detection

**Stage 1.** Regex cues select the sentences. The cues name no company, product or partner. Project names
come from `project/voice.md`, and the checker reads those banned cues from there. Two lookups follow in
`tools/check.py`:
- F3: with `--panel <folder>`, the round count in the sentence is compared with the number of `round-*.md`
  files there. Equal or fewer: the hit is cleared. More: F3 stays, with both numbers. Without `--panel`
  every round count stays a hit.
- F4: with `--reviewed-sha256 <hash>`, every round-count sentence in a piece whose sha256 differs gets F4.

**Stage 2** (`rules/README.md`). F1 and F6 need dates the script does not read: stage 2 gets the sentence,
the output of `git log --format="%h %ad %s" --date=iso -- <piece folder>` and the file times of the
research notes named nearby, run by hand, and answers: does the order or duration in the sentence match
the record. F2 gets the `project/coverage.md` rows. Stage 2 receives only the sentences stage 1 selected,
plus these records.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | none    | regex | (?i)\bbefore (?:writing|drafting|the first line)\b
F1     | copy   | none    | regex | (?i)\b(?:first|step one)[,:]? (?:I|we) (?:checked|read|audited|went through)\b
F2     | copy   | none    | regex | (?i)\b(?:checked|read|reviewed) (?:every|each|all)\b
F2     | copy   | none    | regex | (?i)\bevery (?:public )?(?:source|video|article|post|review|page|thread)s?\b
F3     | copy   | none    | regex | (?i)\b(?:two|three|four|five|six|\d+) (?:review |panel )?rounds?\b
F5     | copy   | none    | regex | (?i)\b(?:of|by|with|rounds?|review) (?:two|three|four|five|six|seven|eight|\d+) (?:readers|reviewers|experts)\b
F5     | copy   | none    | regex | (?i)\bcrew of\b
F6     | copy   | none    | regex | (?i)\b(?:in|over) (?:one|a single) (?:night|day|hour|evening)\b
```

## 7. Fixtures

All texts are synthetic Acme Dispatch sentences. `piece_sha256` stands for the sha256 of the shipped text
and `reviewed_sha256` for the sha256 of the version the last round reviewed (in a real run, from
`git show <commit>:<path> | sha256sum`). `panel_reports` is the count of `round-*.md` files in the panel folder.

```fixtures
{"id": "process-claims/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "1. **Step one: what the app does today.** Before writing, I checked every public source: all 41 help center articles, the 9 recordings on Acme Dispatch's channel,", "source": "synthetic (Acme), shape: 'before writing, I checked' over a check that the files show came later", "record": "draft v1 committed 2026-05-06 09:10; app-audit-notes.md file time 2026-05-07 14:20; coverage: 3 recordings read fully, about 6 keyword-searched"}
{"id": "process-claims/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "Before writing a launch for new texting features, I checked what the app does today, from public sources only, so the launch calls new only what is new.", "source": "synthetic (Acme), shape: order-of-work claim in a published audit note", "record": "draft v1 committed 2026-05-06 09:10"}
{"id": "process-claims/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "text": "Before writing, I checked every public source: all 41 help center articles, the 9 recordings on Acme Dispatch's channel,", "source": "synthetic (Acme), shape: 'checked every' over a source type that was only keyword-searched", "record": "coverage.md COV-02: 3 of 9 recordings read fully, the rest searched by captions; COV-09 the mobile app: not covered"}
{"id": "process-claims/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "then put through three review rounds of five readers each", "source": "synthetic (Acme), shape: round count with no --panel given, so the count is not checked and the hit stays"}
{"id": "process-claims/F4/01", "rule": "F4", "expect": "fire", "target": "copy", "text": "then put through three review rounds of five readers each", "source": "synthetic (Acme), shape: round count printed in a text that differs from the version the rounds reviewed", "panel_reports": 3, "piece_sha256": "aa4d2baf496512b5a62a50bbe484bc019cac20380358fe2e6e41c961ff90b6d4", "reviewed_sha256": "520e25676b7e4be144de309d26008aa0348774213a147217bdbbf094c4c189d5"}
{"id": "process-claims/F5/01", "rule": "F5", "expect": "fire", "target": "copy", "text": "Built in one night, May 6 to May 7, by a crew of drafting and checking agents I run, then put through three review rounds of five readers each (a plumbing owner, an office manager, a crew lead, Acme Dispatch's house voice, a fact-checker), with fixes applied between rounds.", "source": "synthetic (Acme), shape: headcount of named human roles for prompts of one model family", "record": "the five readers were prompts on one model family (panel/round-1.md to round-3.md)"}
{"id": "process-claims/F6/01", "rule": "F6", "expect": "fire", "target": "copy", "text": "Built in one night, May 6 to May 7, by a team of drafting and checking agents I run,", "source": "synthetic (Acme), shape: 'in one night' over work the timestamps spread across days", "record": "v1 committed 2026-05-06 09:10; 7 fix scripts on 2026-05-08 15:43 to 22:51"}
{"id": "process-claims/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "I read 335 public reviews of two competitor apps from three source types and sorted 335 complaints by module (counts are close, not exact: two lanes read the same review sites):", "source": "synthetic (Acme), shape: research counts with no round count"}
{"id": "process-claims/F3/n02", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "then put through three review rounds of five readers each", "source": "synthetic (Acme), shape: round count equal to the report files, so the count itself holds (F4 is the problem with this line)", "panel_reports": 3}
{"id": "process-claims/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "I caught it a day later by asking \"are we sure?\" and running a six-lane audit with four labels, CONFIRMED, CLAIMED, ABSENT, UNKNOWN, where ABSENT has to say where it looked; it produced twelve corrections, including \"since 2023\" to \"since 2021\", and git shows the order: draft first, audit second.", "source": "synthetic (Acme), shape: A1 order claim that points at the version history"}
{"id": "process-claims/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "1. **Step one: what the app does today.** I went through the public record: all 41 help center articles, the 9 recordings on Acme Dispatch's channel, 58 site pages and 30 snapshots of the pricing page since 2019,", "source": "synthetic (Acme), shape: A2 neutral coverage verb with counts, no 'checked every'"}
{"id": "process-claims/F5/n01", "rule": "F5", "expect": "no_fire", "target": "copy", "text": "**Three readers, one message:** the owner who runs a one-truck shop · the owner who came through a franchise · the franchise's front desk (its own note, below).", "source": "synthetic (Acme), shape: audience segments, not a review claim"}
{"id": "process-claims/F3/n03", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Check after the fix: copy the rendered text of the page and search it for `offer offer`, `sync.`, `export.`, `number.`, `wait.`, `switch.`, `shared.`. Expect zero hits.", "source": "synthetic (Acme), shape: reviewer instruction listing strings to search, no round count"}
```
