---
id: project-calibration
version: 1
applies_to: all
---

# Cue calibration on approved copy (Acme Dispatch, a fictional company)

**When:** after `voice.md` and before the first draft. Again each quarter, and after a model change. The list of AI tells decays as models change (`rules/voice.md`, section 5).
**Who:** an agent runs the checker and fills the table. The editor reads it and decides each action.
**What the checker reads here:** nothing. This file is for the editor. Every number below is invented for the example.

A cue that fires on a large share of the company's approved, human-written copy is a house habit, not a tell. This file measures that share.

## Corpus

22 approved pieces that Acme Dispatch shipped in 2024 and 2025, before agents wrote its copy: 8 emails, 6 social posts, 4 pages and 4 partner notes. Each was checked with
`python tools/check.py <piece>.md --project examples/acme/project --piece-type <id>`.

## Threshold

| threshold | set on | set by |
|---|---|---|
| a cue that fires on more than 20% of approved pieces is reviewed | 2026-10-02 | the editor |

## Table

| cue id | fires on approved copy | pieces checked | rate | action |
|---|---|---|---|---|
| VB1 | 6 | 22 | 27% | add an allowed row (done: the plan-name list "Starter, Pro and Crew", `voice.md` section 4; it fired on 3 pages and 3 partner notes) |
| VB2 | 2 | 22 | 9% | keep |
| VB3 robust | 1 | 22 | 5% | keep (one piece is not a habit) |
| VB4 seamless | 0 | 22 | 0% | keep |
| VB5 | 0 | 22 | 0% | keep |
| VB6 | 5 | 22 | 23% | demote to stage 2 only |
| VB7 | 0 | 22 | 0% | keep |
| VB8 ensure | 9 | 22 | 41% | add an allowed row (proposed: `\bensure\b \| 1 \| all`; not yet in `voice.md`) |
| VB8 leverage, comprehensive, holistic, best practices | 0 | 22 | 0% | keep |
| VB10 | 0 | 22 | 0% | keep |
| VB11 | 1 | 22 | 5% | keep |
| VB12 | 2 | 22 | 9% | keep |

VB9 is not calibrated here: it compares a piece with its brief, and approved copy has no brief.

## Actions

- **keep:** the rate is below the threshold. The cue stays as it is.
- **add an allowed row:** the cue is a house habit. Add a row to the `allowed` block in `project/voice.md` (section 4), with the shape, a maximum per piece and the piece ids. Copy the counts from this table.
- **demote to stage 2 only:** the cue selects too many lines to read, but an agent can still judge them. The checker has no switch for this yet, so the id is listed below.
- **retire:** the cue is noise on the company's copy. Remove it and add an entry to `rules/CHANGELOG.md`.

## Stage-2-only ids

| cue id | since | note |
|---|---|---|
| VB6 | 2026-10-02 | "it's worth noting" and "needless to say" appear in 5 of 22 approved pieces. A hit is a question for the agent, not a finding, until the checker supports a stage-2-only list |
