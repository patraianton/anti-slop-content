# Frame and coverage map (step 1)

Filled by the agent before the first line of the draft. The editor gives the feature list, access to the
product if any, and the cost ceiling (about 5 minutes). `tools/check.py` reads the coverage table (the
`research-absence` landmine, rule F2). Its commit must be older than the first draft commit (check by hand with `git log`).
Every "I read N ..." sentence in the how-made note is copied from the coverage table, never typed.

This file is the Acme Dispatch example. Every source and count is invented.

## Frame: what the brief's words mean inside the company

One row per word in the brief or the research that names a product, a rival or a goal. A row that cannot be
filled goes to the decision log (step 7).

| word | what it means inside the company | source | asked? |
|---|---|---|---|
| "Job Thread" | Acme's name for the texts, calls and emails with one customer, shown on the job card | Acme release note 11 | yes, asked the founder |
| "job card" | the record of one job: customer, address, quote, invoice | help center article 3 | no, the help center defines it |
| "texting" | texts sent from the job card to the customer's phone, Pro and Crew only | pricing page, help article 18 | yes, asked the head of product |
| "registration" | US carrier registration for business texting (A2P 10DLC) | the carrier registry's public overview | no, a gatekeeper word |

Cost ceiling, set by the editor at this step: none was set.

## Rules

- One row per source type. Typical types: help center, every video (captions), short videos, site pages,
  pricing history, company and executive posts, third-party and partner videos or reviews, the product itself.
- A facts row labelled ABSENT names at least one covered row here by id. If it cannot, it becomes UNKNOWN.
- A type with nothing keyword-searched and not every item read in full allows no absence claim and says so
  in the last column. `tools/check.py` fires `research-absence` F2 on an ABSENT row that names it.
- The first column holds the id `COV-n`. The checker reads the columns `total`, `read fully` and `keyword-searched`.
  Keep those names.

## Table

| id | source type | total | read fully | keyword-searched | not covered | proof |
|---|---|---:|---|---|---|---|
| COV-01 | Acme help center articles | 41 | 41 | 41 | none | research/help-center-index.md |
| COV-02 | Acme release notes | 12 | 12 | 12 | none | research/release-notes-index.md |
| COV-03 | Acme pricing page snapshots (web archive) | 6 | 6 | 6 | none | research/pricing-snapshots.md |
| COV-04 | Acme webinar recordings (captions) | 9 | 9 | 9 | the screen shares have no captions; text on screen was not read | research/webinar-captions.md |
| COV-05 | LedgerLite and MapRoute partner documentation pages | 8 | 3 | none | 5 pages unread; no absence claim about either partner | research/partner-docs.md |

## Sentences this table allows in the how-made note

Write them after the table is final.

- Allowed: "I opened 41 of 41 help center articles, 12 of 12 release notes and 9 of 9 webinar recordings."
- Allowed: "I read 3 of 8 partner documentation pages."
- Not allowed: "I read every public source." Row COV-05 lists a gap and COV-04 skips the screen shares.
