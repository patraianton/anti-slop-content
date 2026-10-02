# Misses log of this project

Kept by the editor. A miss is a defect that got past the line and was found later. Same format as `process/misses.md`.
Ids are prefixed with the project name so they never collide with the generic lessons (for example `ACME-M-01`).
`tools/check.py` does not read this file. A miss that shows a gap in a generic rule also gets a fixture in
`tools/fixtures/must_fire.jsonl` and an entry in `rules/CHANGELOG.md`.

| id | step | what went wrong | how it was found | the fixture or rule that now catches it |
|---|---|---|---|---|
