---
id: project-calibration
version: 1
applies_to: all
---

# Cue calibration on approved copy (blank template)

**When:** after `voice.md` and before the first draft. Again each quarter, and after a model change. The list of AI tells decays as models change (`rules/voice.md`, section 5).
**Who:** an agent runs the checker and fills the table. The editor reads it and decides each action.
**What the checker reads here:** nothing. This file is for the editor. Changes that follow from it are made in `voice.md`, `rules/CHANGELOG.md` or the note below.

A cue that fires on a large share of the company's approved, human-written copy is a house habit, not a tell. This file measures that share.

## How to run it

1. Collect at least 20 approved pieces that the company shipped before agents wrote its copy. Fewer than 20 means the rates are noise: use the "no corpus yet" mode in `project/README.md` and calibrate later.
2. Save each piece as a markdown file under one `##` heading that is its piece id from `pieces.json`, or tag it with `--piece-type`.
3. Run the checker on each piece:
   `python tools/check.py <piece>.md --project <your project folder> --piece-type <id>`
4. For each cue id in `rules/voice.md` section 2 and each cue row in your `voice.md` section 6, count the pieces on which it fired at least once.
5. Fill the table below. Rate is `fires on approved copy` divided by `pieces checked`.
6. The editor writes the threshold and the date, then picks an action for every row above it.

## Threshold

Set by the editor, with a date. A cue at or above it is reviewed. The threshold below is empty until the editor writes it.

| threshold | set on | set by |
|---|---|---|
| | | |

## Table

| cue id | fires on approved copy | pieces checked | rate | action |
|---|---|---|---|---|
| example: VB0 | 5 | 20 | 25% | add allowed row |

## Actions

- **keep:** the rate is below the threshold. The cue stays as it is.
- **add an allowed row:** the cue is a house habit. Add a row to the `allowed` block in `project/voice.md` (section 4), with the shape, a maximum per piece and the piece ids. Copy the counts from this table.
- **demote to stage 2 only:** the cue selects too many lines to read, but an agent can still judge them. The checker has no switch for this yet. List the id under "Stage-2-only ids" below, and the agent that adjudicates treats a hit on it as a question, not a finding, until the checker supports it.
- **retire:** the cue is noise on your copy. Remove it from your project and add an entry to `rules/CHANGELOG.md` with the date, the rate and the reason.

A form that appears once is not a habit (`rules/voice.md`, section 3). A rate that rests on fewer than 20 pieces is a guess.

## Stage-2-only ids

| cue id | since | note |
|---|---|---|
| | | |
