---
landmine: process-claims
rule: F3
verdict: remove
slop_class: invented-fact
severity: major
piece: email
source: "synthetic (Acme), shape: a round count and a reader count that write a review history into customer copy"
verdict_by: editor, review round 1
verdict_ref: synthetic
date: 2026-10-02
---

## Passage

> Job Thread went through three review rounds of five readers before it reached you.

## Why

The sentence gives the owner a review history. The panel folder holds one report, not three. A round count with
no report per round is F3. The five readers are prompts on one model family, so the headcount also implies
independent people (F5). The owner does not need either fact to decide whether Job Thread helps.

## What replaced it

The sentence was cut from the email. The count lives only in the `how-made` note, and only with the
`--panel` folder and the reviewed hash behind it (rule A3 and A4): "one review round on v1, five reader
roles, one model family, one research folder".
