# Runs

A run is one pass of the line (`process/LINE.md`) over one piece. Record it here so the next run has something to compare with.

## Where

One folder per run: `process/runs/YYYY-MM-DD-<piece>/`. The date is the day the run ended. `<piece>` is the piece id from `project/pieces.json`, or a short name for a set of pieces.

## Files

| File | Content |
|---|---|
| `before.txt` | The `tools/check.py` output on the first version of the run, exit code on the last line. |
| `after.txt` | The `tools/check.py` output on the shipped version, with the same flags, exit code on the last line. |
| `plain-pass.md` | The `was -> now` list from step 4.5. One line per changed sentence. |
| `panel/round-N.md` | One round report from step 6 per round, copied from `project/panel/round.md`. Pass or fail per slop class, severity critical, major or minor. `--panel` takes this folder. |
| `refute.md` | The other-family pass from step 3: each CONFIRMED and ABSENT row it tried to overturn, and the result. The verdicts are also written in the `refute` column of `project/facts.md`. |
| `README.md` | One page. The version hashes (first and shipped, sha256). The exit codes of `before.txt` and `after.txt`. What was not run, and why. |

Keep the exact command lines in `README.md`, so anyone can repeat `before.txt` and `after.txt`.

A step that was not run is named in `README.md`. A missing file with no note means the step did not happen.

## This repository

This repository ships no run of its own. The first run is yours. The fictional project in `examples/acme/` shows the inputs and the two expected exit codes, not a recorded run.
