---
id: setup-timelines
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: remove
applies_to: all
---

# Landmine: setup effort and timing

## 1. What this landmine is

Any sentence about how long setup takes or how much work it is: "right away", "day one", "in minutes",
"nothing to set up", "not another system to set up", a step the reader must wait for (a registry, a regulator, a bank
partner, a platform review, moving a number or an account), and work the company promises to do for the reader ("we file it
for you"). Examples: Acme Dispatch waits for the registry that approves business texting; a money product waits for an
identity check or a bank partner's onboarding before an account opens.

## 2. What it is not (hand-offs)

- Whether the feature exists or what it does → `product-claims`.
- Who registers the number and in whose name, consent and opt-out handling → `compliance-promises`.
- Which plan includes a feature, "live on all plans" → `pricing-plans`.
- A competitor's setup complaints ("registration rejected or stuck for weeks" in review sites) →
  `competitors-partners`, and their counts → `numbers-and-sources`.
- How the sentence reads, grade level, filler → `plain-language`.
- A claim about how the work was done, or a step of the line → `process-claims`.
- An absence claim such as "we found no mention of setup" → `research-absence`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The gatekeeper's own documentation, dated: a registry's or regulator's docs, the onboarding rules of a
   bank partner, the porting rules of a provider, the review policy of the platform that gates the step
   (in the Acme example: the carrier registry's docs for business texting).
2. The company's help center or docs, dated, for what is set up today (data already in the account, an
   import that exists).
3. A CONFIRMED row in `project/facts.md` for what is done today.
4. A `project/decisions.md` row owned by a named owner for what ships on launch day and for any work the
   company does for the reader.

Never a source: the brief; a reviewer's estimate; a competitor's marketing; the model's memory.

## 4. Forbidden shapes (banned by shape)

- **F1 Time promise with no row.** "right away", "on day one", "from day one", "instantly",
  "immediately", "in 15 minutes", "starts as soon as", or a range of days or weeks. Class: invented-fact.
  Severity: major.
- **F2 Denial of setup effort.** "nothing to set up", "not another system to set up", "no setup",
  "out of the box". Brackets do not rescue it.
  Class: invented-fact. Severity: major.
- **F3 Work the company does for the reader, undecided.** "we file it for you", "Acme files the
  registration", "we port it for you" with no decision row. Brackets do not rescue it: TO-CONFIRM needs an
  owner and a date.
  Class: invented-fact. Severity: major.

## 5. Allowed with a row

- **A1** A wait quoted from the gatekeeper's documentation, with source and date ("The carrier registry
  quotes up to 5 business days per campaign").
- **A2** A gated statement with no time in it: "texting from your own number as each one clears
  registration".
- **A3** What is already done today, CONFIRMED: "Every customer you have quoted in Acme is already here."
- **A4** A time inside brackets as TO-CONFIRM, with a `decisions.md` row: `[bring your office line over]`.

## 6. Detection

**Stage 1: cues.** Format: `tools/README.md`. Run by the `time-promises` check. Cues carry no company,
product or partner names. Names of the project's own product and of competitors come from `project/voice.md`,
which the checker reads for banned cues.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | bracket | regex | (?i)\bright away\b|\b(?:on|from) day one\b|\binstantly\b|\bimmediately\b|\bin (?:\d+|a few) minutes\b|\bstarts? as soon as\b|\b\d+\s*(?:–|-|to)\s*\d+\s+(?:business\s+)?(?:days|weeks)\b
F2     | copy   | none    | regex | (?i)\b(?:nothing|not another (?:system|tool|app|platform)|no (?:new )?(?:system|tool|app)) to (?:set up|setup|learn)\b|\bno set-?up\b|\bout of the box\b
F3     | copy   | none    | regex | (?i)\bwe(?:'ll| will)? (?:file|register|port|move) (?:it|them|your \w+) for you\b|(?-i:\b[A-Z][a-z]+) (?:files|registers|ports) (?:the|your) (?:registration|number|line)\b
```

**Stage 2** (`rules/README.md`, Detection) gets the passage, the facts table and `decisions.md`. It
answers: which gate this step passes (registration, porting, platform review, none), which row gives its
time, who decided the company does the work.

## 7. Fixtures

```fixtures
{"id": "setup-timelines/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "Texting starts right away.", "source": "synthetic (Acme), shape: a feature stated as instant when a registration wait sits in front of it"}
{"id": "setup-timelines/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "2. Choose a local number and start texting right away - or [move your office line across].", "source": "synthetic (Acme), shape: a time promise next to a bracketed TO-CONFIRM; the bracket covers only the second half"}
{"id": "setup-timelines/F1/03", "rule": "F1", "expect": "fire", "target": "copy", "text": "1. Connect your email once - email and quotes work right away.", "source": "synthetic (Acme), shape: a time promise on a step that a platform review can gate"}
{"id": "setup-timelines/F1/04", "rule": "F1", "expect": "fire", "target": "copy", "text": "Quotes and invoices work from day one - connect your calendar once.", "source": "synthetic (Acme), shape: from day one in a numbered setup step"}
{"id": "setup-timelines/F1/05", "rule": "F1", "expect": "fire", "target": "copy", "text": "Watch Us Take a Customer from Quote to Invoice in 15 Minutes (Live Demo)", "source": "synthetic (Acme), shape: a minutes figure in a page title, added by a reviewer"}
{"id": "setup-timelines/F1/06", "rule": "F1", "expect": "fire", "target": "copy", "text": "Texting needs each crew's number registered with the carriers first (10–15 business days);", "source": "synthetic (Acme), shape: a range of business days that is in no gatekeeper document"}
{"id": "setup-timelines/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "text": "**Nothing to set up.** Your customers and jobs are already here.", "source": "synthetic (Acme), shape: bold denial of setup effort at the top of a section"}
{"id": "setup-timelines/F2/02", "rule": "F2", "expect": "fire", "target": "copy", "text": "> Not another system to set up. The same job card you already use - now with the call, the text and the email on it.", "source": "synthetic (Acme), shape: not-another-system line in a quoted block"}
{"id": "setup-timelines/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "3. Texting switches on after the one-time registration every US business texting line needs - we file it for you [typical wait: confirm].", "source": "synthetic (Acme), shape: work promised for the reader with only a wait in brackets, no decision row"}
{"id": "setup-timelines/F3/02", "rule": "F3", "expect": "fire", "target": "copy", "text": "Text any customer from your own number. Acme files the registration. Opt-outs handled. Every text on the job.", "source": "synthetic (Acme), shape: third-person company name as the subject of the work, in a table cell"}
{"id": "setup-timelines/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "By Friday you are piecing together who said what before you call the customer back.", "source": "synthetic (Acme), shape: a time span in a scene, not a promise about setup"}
{"id": "setup-timelines/F1/n02", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "From [date], owners on Acme can email, call and book jobs from the customer's card, with texting from your own number as each one clears registration.", "source": "synthetic (Acme), shape: a gated statement with no time in it (A2)"}
{"id": "setup-timelines/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "**Getting started.** Every customer you have quoted in Acme is already here.", "source": "synthetic (Acme), shape: what is already done today, CONFIRMED (A3)"}
{"id": "setup-timelines/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Already on LedgerLite? Keep it for your books - bring any invoice in with one click, as you do today.", "source": "synthetic (Acme), shape: reader keeps their tool and imports with a click, no work promised"}
```
