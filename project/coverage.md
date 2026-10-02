# Frame and coverage map (step 1)

Filled by the agent before the first line of the draft. The editor gives the feature list, access to the
product if any, and the cost ceiling (about 5 minutes). `tools/check.py` reads the coverage table (the
`research-absence` landmine, rule F2). Its commit must be older than the first draft commit (check by hand with `git log`).
Every "I read N ..." sentence in the how-made note is copied from the coverage table, never typed.

## Frame: what the brief's words mean inside the company

One row per word in the brief or the research that names a product, a rival or a goal. A row that cannot be
filled goes to the decision log (step 7). The table ships empty. A filled example is in `examples/acme/project/coverage.md`.

| word | what it means inside the company | source | asked? |
|---|---|---|---|

Cost ceiling, set by the editor at this step: (write the amount, or "none was set").

## Rules

- One row per source type. Typical types: help center, every video (captions), short videos, site pages,
  pricing history, company and executive posts, third-party and partner videos or reviews, the product itself.
- A facts row labelled ABSENT names at least one covered row here by id. If it cannot, it becomes UNKNOWN.
- A type with nothing keyword-searched and not every item read in full allows no absence claim and says so
  in the last column. `tools/check.py` fires `research-absence` F2 on an ABSENT row that names it.
- The first column holds the id `COV-n`. The checker reads the columns `total`, `read fully` and `keyword-searched`.
  Keep those names.

## Table

The table ships empty. A filled example is in `examples/acme/project/coverage.md`.

| id | source type | total | read fully | keyword-searched | not covered | proof |
|---|---|---:|---|---|---|---|

## Sentences this table allows in the how-made note

Write them after the table is final.

- Allowed: (a sentence whose every number is copied from a row above, for example "all 41 help center articles").
- Not allowed: (a sentence that claims more than the rows show, for example "every public source" when a row lists a gap).
