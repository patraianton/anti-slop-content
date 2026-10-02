# Facts table (step 2, refuted in step 3)

Filled by agents in several lanes, one lane on another model family (step 2). A separate agent on another
model family then tries to overturn the CONFIRMED and ABSENT rows and writes the result in each row's `refute`
cell (step 3). One row per claim about the product, written before the draft. The draft may state a product
fact only if a row here backs it (`claims.csv` column `facts_row`). Numbers do not go here: they go to `numbers.json`.

`tools/check.py` reads every table that has the columns `claim` and `label`. It reads `label`, `where_searched`
and `refute`. An ABSENT row needs coverage ids that exist in `coverage.md` and were searched (`research-absence`
F2), and a filled `refute` cell (F4). A cell keeps its history, so only the last verdict word in it (`held`,
`overturned` or `unverifiable`) counts. The run prints how many rows are `overturned`.

This file is the Acme Dispatch example. Every source, date and speaker is invented.

## Labels

| label | means | row fails when |
|---|---|---|
| `CONFIRMED` | a company document, help article, screenshot or video shows it | no URL, or no date |
| `CLAIMED` | marketing text or an employee's words; nothing shown | the speaker's role is missing |
| `ABSENT` | searched where it should be and not found | `where_searched` names no `coverage.md` row; the row is then relabelled UNKNOWN |
| `UNKNOWN` | no source answers it without product access | never fails; it can only be bracketed in copy |

The label belongs to the claim, not the source type. A help article can say a thing is impossible while a
video shows it done. Grade each claim on what it shows.

## Columns

`id` · `claim` · `label` · `source` (URL and timestamp, or file:line) · `as_of` (the date the source shows,
not the date you looked) · `where_searched` (ABSENT and UNKNOWN only: coverage ids) · `applies_to` (plan,
reader, lead type) · `speaker` (for CLAIMED and quotes: who, role) · `refute` (step 3: who tried to overturn
it, on which model family, the result `held`, `overturned` or `unverifiable`, and the new label if it changed)

## Rows

| id | claim | label | source | as_of | where_searched | applies_to | speaker | refute |
|---|---|---|---|---|---|---|---|---|
| F-01 | A user on Pro or Crew can text a customer from the job card | CONFIRMED | https://acme.example/help/job-thread, "Send a text from any job card" (article 18) | 2026-07-09 | | Pro and Crew plans | | 2026-09-20, another model family: held |
| F-02 | Calls placed from the Acme app are logged on the job card | CONFIRMED | https://acme.example/help/calls, "Every call is logged" (article 19) | 2026-07-09 | | Pro and Crew plans | | 2026-09-20, another model family: held |
| F-03 | Texting is listed on Pro and Crew only; Starter has no texting | CONFIRMED | https://acme.example/pricing, plan table, row "Texting" | 2026-09-20 | | all owners | | 2026-09-21, another model family: held |
| F-04 | Plan prices: Starter $29, Pro $79, Crew $149 per month | CONFIRMED | https://acme.example/pricing, plan cards | 2026-09-20 | | all owners | | 2026-09-21, another model family: held |
| F-05 | The free trial is 14 days for owners who sign up on the site | CONFIRMED | https://acme.example/pricing, footnote 2 | 2026-09-20 | | owners | | 2026-09-21, another model family: held |
| F-06 | The LedgerLite import is one way, Acme to LedgerLite, and sends 6 fields | CONFIRMED | https://acme.example/help/ledgerlite (article 62) | 2026-08-02 | | all plans with the import | | 2026-09-20, another model family: held |
| F-07 | Emails sent to a job's address appear on that job card | CONFIRMED | https://acme.example/help/job-email (article 71), screenshot 3 | 2026-08-14 | | Pro and Crew plans | | 2026-09-20, another model family: held |
| F-08 | US carriers require registration for business texting (A2P 10DLC) | CONFIRMED | the carrier registry's public overview of business texting registration | 2026-08-12 | | any US business that texts | | 2026-09-22, another model family: held |
| F-09 | Call recording consent laws differ by state | CONFIRMED | a public state-by-state summary of recording consent laws, section "One-party and all-party states" | 2026-08-12 | | any US business that records calls | | 2026-09-22, another model family: held |
| F-10 | Before Job Thread, texting from a job card worked for open quotes only, from one shared number | CONFIRMED | Acme release note 7, "Quote texting" | 2026-03-12 | | Pro and Crew plans | | 2026-09-20, another model family: held |
| F-11 | Job Thread replies show up next to the text that was sent | CLAIMED | demo call recording, 31:40 | 2026-09-12 | | Pro and Crew plans | Acme sales rep, role: sales; no help article or screenshot shows it | |
| F-12 | Texts to customers go out within seconds | CLAIMED | founder post on the Acme blog | 2026-09-04 | | Pro and Crew plans | Maria Ortega, founder | |
| F-13 | Acme has no call recording feature | ABSENT | help center, release notes and webinar recordings, keyword "record" | 2026-09-15 | COV-01 COV-02 COV-04 | all plans | | 2026-09-22, another model family: held |
| F-14 | The LedgerLite import has no second direction from LedgerLite back to Acme | ABSENT | help center article 62 and release note 9, keyword "sync" | 2026-09-15 | COV-01 COV-02 | all plans with the import | | 2026-09-22, another model family: held |
| F-15 | Acme has no free plan | ABSENT | pricing page snapshots, keyword "free" | 2026-09-15 | COV-03 | all owners | | 2026-09-22, another model family: held |
| F-16 | Who is the registered sender of texts: the owner's business or Acme | UNKNOWN | no source answers it; needs a trial account or the founder | 2026-09-15 | COV-01 COV-04 | Pro and Crew plans | | |
| F-17 | How long carrier registration takes for a new Acme customer | UNKNOWN | the registry's overview gives no time for a new business | 2026-09-15 | COV-01 COV-05 | any US business that texts | | |

## Quotes

One record per quote. A quote without the speaker's role fails.

| id | text | speaker and role | where, date | weight | used in the piece as |
|---|---|---|---|---|---|
| Q-01 | "Half my day is texting people back." | owner of a four-person plumbing company | interview call, 2026-09-10 | high for the wording | social, shortened |
| Q-02 | "I want the text and the call in one place, on the job." | office manager of a landscaping company | interview call, 2026-09-11 | medium | not used yet |
