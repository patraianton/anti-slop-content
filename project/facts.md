# Facts table (step 2, refuted in step 3)

Filled by agents in several lanes, one lane on another model family (step 2). A separate agent on another
model family then tries to overturn the CONFIRMED and ABSENT rows and writes the result in each row's `refute`
cell (step 3). One row per claim about the product, written before the draft. The draft may state a product
fact only if a row here backs it (`claims.csv` column `facts_row`). Numbers do not go here: they go to `numbers.json`.

`tools/check.py` reads every table that has the columns `claim` and `label`. It reads `label`, `where_searched`
and `refute`. An ABSENT row needs coverage ids that exist in `coverage.md` and were searched (`research-absence`
F2), and a filled `refute` cell (F4). A cell keeps its history, so only the last verdict word in it (`held`,
`overturned` or `unverifiable`) counts. The run prints how many rows are `overturned`.

## Labels

| label | means | row fails when |
|---|---|---|
| `CONFIRMED` | a company document, help article, screenshot or video shows it | no URL, or no date |
| `CLAIMED` | marketing text or an employee's words; nothing shown | the speaker's role is missing |
| `ABSENT` | searched where it should be and not found | `where_searched` names no `coverage.md` row; the row is then relabelled UNKNOWN |
| `UNKNOWN` | cannot be known without product access | never fails; it can only be bracketed in copy |

The label belongs to the claim, not the source type. A help article can say a thing is impossible while a
video shows it done. Grade each claim on what it shows.

## Columns

`id` · `claim` · `label` · `source` (URL and timestamp, or file:line) · `as_of` (the date the source shows,
not the date you looked) · `where_searched` (ABSENT and UNKNOWN only: coverage ids) · `applies_to` (plan,
reader, lead type) · `speaker` (for CLAIMED and quotes: who, role) · `refute` (step 3: who tried to overturn
it, on which model family, the result `held`, `overturned` or `unverifiable`, and the new label if it changed)

## Rows

The table ships empty. A filled example is in `examples/acme/project/facts.md`.

| id | claim | label | source | as_of | where_searched | applies_to | speaker | refute |
|---|---|---|---|---|---|---|---|---|

## Quotes

One record per quote. A quote without the speaker's role fails. The table ships empty.

| id | text | speaker and role | where, date | weight | used in the piece as |
|---|---|---|---|---|---|
