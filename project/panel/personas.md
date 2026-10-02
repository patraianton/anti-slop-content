---
version: 1
changed: (date)
asked_by: (the editor's name)
---

# Panel personas (step 6)

Written once by the editor with an agent, before the first round, and then pinned. Used by the blind check and
the review round (step 6 of `process/LINE.md`). `tools/check.py` does not read this file. Each round report
names the version of this file it used.

A persona is a measuring instrument: change it and round-over-round results measure the persona, not the text.

Rules
- Personas never change between rounds of one piece. A change is a new `version` of this file with a
  `rules/CHANGELOG.md` entry, and counts from rounds on different versions are not compared.
- Each round report names the `personas.md` version it used.
- Every persona gets its listed seed files and nothing else. A finding that cites a file outside the seeds
  is marked `uncertain`.
- Replacement text from any persona goes through steps 4 and 5 (claims ledger, lint) before it is applied.
- Pin every attribute a persona uses (age, region, tools, size of company). An attribute added in round 2 makes a different persona.
- Readers that share one model family and one research folder share every gap in that folder. Run at least
  one role on another model family, and one role with no research folder.

## Reader roles

Replace the Acme definitions with your own readers. Keep the role ids, or rename them once and keep the new names.

| id | pinned definition | reads | seeds |
|---|---|---|---|
| owner-buyer | example: owner of a 6-person plumbing company in Ohio, pays for software out of pocket, has used paper job cards for 11 years | the customer copy | the reader portrait; the product brief section on buyers |
| sceptic | example: owner who left a competitor (DispatchPro) after a year and distrusts launch emails | the customer copy | competitor reviews; `facts.md` |
| compliance-reader | example: person who knows US business texting registration and call recording consent rules and checks every promise against them | the customer copy, `decisions.md` | `facts.md`; `decisions.md` |
| voice-editor | the company's house voice | the customer copy | `project/voice.md`; `rules/voice.md` |
| fact-checker | blind: checks claims, never sees the draft | `claims.csv`, `facts.md`, `numbers.json` | the sources linked from those rows |

## Added readers

These three catch what the roles above share.

| id | model | reads | job |
|---|---|---|---|
| other-family | another model family | the customer copy and `facts.md` | the same defect list as the roles above, so a gap shared by one family shows up as a disagreement |
| cold-reader | the main family | the customer copy only: no research, no brief, no facts table | marks every sentence it would ask "says who?" about; each mark must map to a `claims.csv` row or it becomes a defect |
| adversary | another model family | `facts.md`, `coverage.md`, the customer copy | quota: three false claims, each with the row and the source that breaks it, or a written reason per piece why there are none. Tries ABSENT rows first. It is the step 3 refuter run again on the draft. |

## Optional

- A design critic for a rendered page (a phone width, a desktop width, and the printed PDF).
- A live reader from the audience. Request one at step 7. The release record says whether one answered.
