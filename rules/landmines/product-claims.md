---
id: product-claims
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: cite-or-cut
applies_to: all
---

# Landmine: product claims

## 1. What this landmine is

Any sentence that says what the company's product does: a feature name, a tab, a button, a menu path,
what is saved where, what syncs, what is sent from which address or number, what happens after a click.
Example (the fictional product Acme Dispatch is the example throughout): "Job Thread keeps every text on the job card."

## 2. What it is not (hand-offs)

- "The product has no X", or a feature that exists announced as new (F3) → `research-absence`.
- Which plan has the feature, "every plan", "all plans", trial length → `pricing-plans`.
- How long setup takes, "right away", "nothing to set up", "we file it for you" → `setup-timelines`.
- Consent, STOP, call recording, data use, retention, export, sharing → `compliance-promises`.
- What a competitor's, a partner's or a gatekeeper's tools do → `competitors-partners`.
- Counts of articles, videos, posts → `numbers-and-sources`. "I checked every source" → `process-claims`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The company's help center or docs: article number and its updated date.
2. A CONFIRMED row in `project/facts.md`: source, date, and what was seen on screen.
3. The product itself: a trial account, a dated screenshot. Shown on screen is CONFIRMED;
   only said aloud is CLAIMED.
4. The company's blog, release notes and press releases, dated.
5. A `project/decisions.md` row owned by a named owner (for product mechanics, the person who owns the product).
6. For anything that depends on a gatekeeper (a registry, a carrier, a regulator, a platform), the gatekeeper's
   own documentation, dated.

When sources disagree, a later dated showing beats an earlier spoken claim, and the row says so.
Example: sending email straight from Job Thread was announced in a founder post dated 2026-01-08
("you can send emails from here now"), while a demo dated 2026-06-11 and help article 71 (2026-04-02)
show only "Open in Mail". The row is CLAIMED and the copy may not state it as fact.

Never a source: the brief or the task text; a competitor's feature; the model's memory of the product;
an earlier version of the piece; a reviewer's replacement text.

A new-release feature is never CONFIRMED: in copy it is A2 or A3.

## 4. Forbidden shapes (banned by shape)

- **F1 Product detail with no row.** An unbracketed feature name, tab, menu path, sending identity or
  post-click behaviour with no CONFIRMED row in the facts table. Cues: a menu path ending in a bare name
  (`→ Customer → **Thread**`), `<Name> tab`, `from your own address`, `from your own number`,
  `from the owner's own number`, `replies land`, `prefilled and submitted`. Class: invented-fact.
  Severity: major.
- **F2 CONFIRMED with no date.** A facts-table row labelled CONFIRMED with no date. Cue: a facts row
  containing `CONFIRMED` and no `YYYY-MM-DD`. Class: invented-fact. Severity: major.

## 5. Allowed with a row

- **A1** SOURCED: a claim with a CONFIRMED row (URL and date) in `facts.md`. Example:
  "Texts and calls on the job card (Pro and Crew)" matches help article 18 (2026-06-19) and the
  2026-08-27 launch post.
- **A2** PROPOSAL: a new-release name or behaviour in square brackets (`[Job Thread]`), listed in
  `claims.csv` with status PROPOSAL.
- **A3** TO-CONFIRM: a bracketed mechanism (`[replies land next to it]`) with a `decisions.md` row naming
  the owner (the person who owns product mechanics) and a date.

## 6. Detection

**Stage 1: cues.** Cue format, unit of text (one visible line; a dotted span reads as `[…]`) and rescues:
`tools/README.md`. Cues name no company, product or partner. Project names (product, feature, plan,
partner, competitor) come from `project/voice.md`, which the checker reads for banned cues.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | bracket | regex | →\s*\*{0,2}(?!\[)[A-Z][A-Za-z ]*[a-z]\*{0,2}\s*[.,;:]
F1     | copy   | bracket | regex | \b(?:[A-Z][A-Za-z]+ )+tab\b
# example domain: messaging (sender address, number, replies); keep, swap or delete for your product
F1     | copy   | bracket | regex | (?i)\bfrom (?:your|the (?:owner|tech|crew|company)'s|their) own (?:address|email|number|line|phone)\b
F1     | copy   | bracket | regex | (?i)\breplies (?:land|show up|appear)\b
F1     | copy   | bracket | regex | (?i)\bprefilled and submitted\b
F2     | facts  | none    | regex | ^(?!.*\b20\d\d-\d\d-\d\d\b).*\|\s*CONFIRMED\s*\|
```

**Stage 2** (`rules/README.md`, Detection) gets the passage and the facts table, not the draft or the
brief. It answers: which row supports this, what label, what date.

## 7. Fixtures

```fixtures
{"id": "product-claims/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "**Where to find it:** open any job → Customer → **Thread**.", "source": "synthetic (Acme), shape: menu path ending in a bare, unbracketed feature name"}
{"id": "product-claims/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "Attach a 20-second screen recording of the Job Thread tab.", "source": "synthetic (Acme), shape: named tab in an instruction"}
{"id": "product-claims/F1/03", "rule": "F1", "expect": "fire", "target": "copy", "text": "Meet the Job Thread tab: texts, calls and emails with the customer on one job card", "source": "synthetic (Acme), shape: named tab in a page agenda row"}
{"id": "product-claims/F1/04", "rule": "F1", "expect": "fire", "target": "copy", "text": "from Acme Dispatch, from your own address.", "source": "synthetic (Acme), shape: sending identity stated as fact"}
{"id": "product-claims/F1/05", "rule": "F1", "expect": "fire", "target": "copy", "text": "Replies land on the customer's job card.", "source": "synthetic (Acme), shape: post-send behaviour that needs inbox sync"}
{"id": "product-claims/F1/06", "rule": "F1", "expect": "fire", "target": "copy", "text": "Quote approved, job scheduled, invoice prefilled and submitted", "source": "synthetic (Acme), shape: submission step that no source shows"}
{"id": "product-claims/F1/07", "rule": "F1", "expect": "fire", "target": "copy", "text": "Send the quote and the follow-up from your own number.", "source": "synthetic (Acme), shape: sending identity that is CLAIMED, not CONFIRMED, left unbracketed"}
{"id": "product-claims/F2/01", "rule": "F2", "expect": "fire", "target": "facts", "text": "| 5 | Everything a tech logs on a job saves to the customer card; the thread exists per job only, empty for the customer | help article 33, 47 | CONFIRMED |", "source": "synthetic (Acme), shape: facts row labelled CONFIRMED with no date"}
{"id": "product-claims/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "**Where to find it:** open any job → Customer → **[Job Thread]**.", "source": "synthetic (Acme), shape: proposed name in brackets after the arrow, a marked PROPOSAL"}
{"id": "product-claims/F1/n02", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Text any customer, not only the ones who booked online, [from your own number].", "source": "synthetic (Acme), shape: sending identity inside brackets, the cue matches and the bracket rescue silences it by design"}
{"id": "product-claims/F1/n03", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Every email is saved on the job card, and [replies land next to it].", "source": "synthetic (Acme), shape: unconfirmed mechanism in brackets, rescued by design"}
{"id": "product-claims/F1/n04", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Quote approved → job on the calendar → Invoice export to LedgerLite (one-way, 6 fields, where your plan has it)", "source": "synthetic (Acme), shape: arrow chain whose last item is followed by a qualifier in parentheses, backed by a CONFIRMED row"}
{"id": "product-claims/F2/n01", "rule": "F2", "expect": "no_fire", "target": "facts", "text": "| Booking link on the owner's website, Pro and Crew only | help.acmedispatch.example/articles/booking-link | 2026-08-13 | CONFIRMED |", "source": "synthetic (Acme), shape: facts row labelled CONFIRMED with a date"}
```
