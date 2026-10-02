---
landmine: setup-timelines
rule: F1
verdict: rewrite
slop_class: invented-fact
severity: major
piece: email
source: "synthetic (Acme), shape: a time promise ('right away') for a step that waits on a gatekeeper"
verdict_by: editor, review round 2
verdict_ref: synthetic
date: 2026-10-02
---

## Passage

> Texting with your customers starts right away.

## Why

Business texting in the US waits on carrier registration (A2P 10DLC) before the first message goes out.
"Right away" is false for every owner whose number is not yet registered. The wait is set by the
gatekeeper, not by Acme, and the facts table has no row that gives a time.

## What replaced it

> Texting with your customers starts as each number clears carrier registration.

The new sentence names the gate and promises no time (rule A2). It is checked again as a new passage and
stays silent under the same cue.
