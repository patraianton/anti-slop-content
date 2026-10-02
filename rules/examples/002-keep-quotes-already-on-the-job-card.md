---
landmine: product-claims
rule: A1
verdict: keep
slop_class: invented-fact
severity:
piece: email
source: "synthetic (Acme), shape: a present-state sentence with no cue words, backed by a CONFIRMED facts row"
verdict_by: editor, review round 2 ("do not change")
verdict_ref: synthetic
date: 2026-10-02
---

## Passage

> Every quote you have sent from Acme Dispatch is already on its job card.

## Why

The sentence says what exists today. A CONFIRMED row backs it:

| id | claim | source | date | label |
|----|-------|--------|------|-------|
| F-02 | A quote sent from Acme Dispatch is saved on the job card it was made for | help center article 18 | 2026-09-12 | CONFIRMED |

The claim is also row CL-01 in `claims.csv`, status SOURCED.

## What it shows

An unbracketed product sentence is fine when a CONFIRMED row with a date backs it. The sentence has no cue
words (no menu path, no "tab", no "from your own number"), so a cue that fires on it is wrong.
