---
id: pricing-plans
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: cite-or-cut
applies_to: all
---

# Landmine: pricing and plans

## 1. What this landmine is

Any sentence about plan names (in the Acme example: Starter, Pro, Crew), prices, fees, rates, usage allowances and what they buy, what a
plan includes, "every plan" or "all plans", trial length, and launch offers ("next month is on us").
It also covers plan names and prices that existed in the past.

## 2. What it is not (hand-offs)

- What the feature does is `product-claims`. When it switches on is `setup-timelines`.
- Promises about data, consent or recording, even when tied to a plan, are `compliance-promises`.
- A competitor's price is `competitors-partners`.
- "Billing is the second most frequent complaint" is `numbers-and-sources`.
- "The pricing page has no free tier" or any other statement that something is missing is `research-absence`.
- "We checked every plan" is `process-claims`.
- A price explained in long words is `plain-language`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The live pricing page of the company, with the date it was opened.
2. Web archive snapshots of that page, with the snapshot date, for any claim about the past.
3. The company's help center or docs, dated, for allowance and usage costs. When a help article
   disagrees with the pricing page, the pricing page wins and the row records the conflict
   (example: Acme's help article prints "Pro $948/year, $69/month"; 948 / 12 is 79, and the pricing
   page shows $79, so the article is stale).
4. A CONFIRMED row in `project/facts.md` for any plan fact the rows above do not cover.
5. A `decisions.md` row owned by a named owner for any new price, plan placement, trial or offer.

Each facts row has an "applies to" column: audience and trial can differ (example: owners get a 14-day
trial, a reseller program gets 30 days).

Never a source: a partner's words on a recorded session ("about 150 a month for the full set" is
CLAIMED); a forum post; the brief; a competitor's pricing; the model's memory of the company's prices.

## 4. Forbidden shapes (banned by shape)

- **F1 Plan coverage stated as fact.** "all plans", "every plan", "included in your plan" with no
  pricing-page row and no named owner's decision. Cues: `all plans`, `every plan`, `on every plan`,
  `included in your plan`. Class: invented-fact. Severity: major.
- **F2 Trial or offer for the wrong audience.** A trial length or offer put in front of an audience whose
  plan has a different one. Cues: `14-day trial`, `14-day free trial`, `30-day trial`.
  Class: invented-fact. Severity: minor.

- **F3 Fee, rate or yield stated as fact.** A sentence that denies a fee or states a rate, a yield or a
  ceiling ("up to") with no pricing-page row and no named owner's decision. Cues: `no fees`, `fee-free`,
  `zero fees`, `zero commission`, `no hidden`, a percentage followed by APY, APR, interest or cashback,
  `up to $N`, `up to N%`. Drafts carry placeholders such as `$X` or `N%` until the row exists. Class:
  invented-fact. Severity: major.

No shape yet for an undated price or allowance in other forms. Add a shape when a real violation appears.
Company, product and partner names are not in these cues. Project terms come from
`project/voice.md` (the checker reads banned cues from there).

## 5. Allowed with a row

- **A1** SOURCED: plan, price, allowance or trial with a pricing-page or archive row, its date and its audience.
- **A2** PROPOSAL: a plan placement in brackets, ours, listed in `claims.csv`
  (`[Scheduling and quotes come with every plan.]`).
- **A3** A question to the team about plans ("every plan, or Pro and up?"), with the dated history it rests on.

## 6. Detection

**Stage 1: cues.** Format and rescues: `tools/README.md`. F2 has no stage-1 rescue: the audience is only
visible in the facts row.

```cues
# rule | target | rescues                  | kind  | pattern
F1     | copy   | bracket,proposal,question | regex | (?i)\b(?:all|every) plans?\b|\bincluded in (?:your|every|all) plans?\b
F2     | copy   | none                     | regex | (?i)\b\d+[- ]day (?:free )?trial\b
F3     | copy   | bracket,proposal,question | regex | (?i)\b(?:no (?:monthly |annual |account |transaction |hidden )?fees?|no hidden (?:charges|costs)|fee[- ]free|zero (?:fees?|commission)|\d+(?:\.\d+)?% (?:APY|APR|interest|cash ?back)|up to \$\d[\d,.]*|up to \d+(?:\.\d+)?%)
```

**Stage 2** (`rules/README.md`, Detection) gets the passage, the pricing rows of the facts table (with
dates and the "applies to" column) and `decisions.md`. It answers: which row, which date, which audience,
and does the audience of this piece match.

## 7. Fixtures

```fixtures
{"id": "pricing-plans/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "Live on all plans from [date]; texting switches on as your number is verified [plan/rollout detail].", "source": "synthetic (Acme), shape: 'live on all plans' with no pricing-page row"}
{"id": "pricing-plans/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "Live on every plan from [date].", "source": "synthetic (Acme), shape: 'every plan' stated as fact, no brackets, no question"}
{"id": "pricing-plans/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "text": "Pricing, [attendee offer], 14-day free trial, next Wednesday's live demo", "source": "synthetic (Acme), shape: trial length on a page that also invites an audience with a different trial"}
{"id": "pricing-plans/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "Pay by card on the invoice with no fees, and earn up to $50 back on your first month.", "source": "synthetic (Acme), shape: a fee denial and an 'up to' amount with no pricing row"}
{"id": "pricing-plans/F3/02", "rule": "F3", "expect": "fire", "target": "copy", "text": "Hold your float in Acme Pay and earn 4.5% APY on every balance.", "source": "synthetic (Acme), shape: a yield figure stated as fact with no pricing row"}
{"id": "pricing-plans/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Pay by card on the invoice. [Fee: N% per payment, no monthly minimum.] The fee table is on the pricing page.", "source": "synthetic (Acme), shape: a fee as a bracketed placeholder with a pointer to the pricing page (A2)"}
{"id": "pricing-plans/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "- [Scheduling and quotes come with every plan.] Texts: [N texts a month included, then $X a text].", "source": "synthetic (Acme), shape: 'every plan' inside brackets, prices as N and $X placeholders (A2); rescued by design (bracket)"}
{"id": "pricing-plans/F1/n02", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "- Pricing: scheduling in every plan; texts with N included, then per text. A proposal, not Acme's price list. In 2024 texting sat on Pro and Crew only: every plan, or Pro and up?", "source": "synthetic (Acme), shape: 'every plan' marked as proposal and asked as a question (A2, A3); rescued by design (proposal, question)"}
{"id": "pricing-plans/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "if demo-to-trial doesn't move, the promise isn't ready.", "source": "synthetic (Acme), shape: the word 'trial' with no day count"}
```
