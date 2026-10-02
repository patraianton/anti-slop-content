---
id: compliance-promises
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: remove
applies_to: all
---

# Landmine: compliance promises

## 1. What this landmine is

Any sentence that promises how the company handles a legal or trust question: consent to text, STOP and
opt-out handling, carrier or sender registration (who registers, in whose name), call recording (default,
who sets the rule, notice), use or sale of customer data, retention, export and off-boarding, sharing with
carriers, partners or AI providers, audit trails. Also any sentence that says what the law requires of the
reader.

Example (Acme Dispatch): "Texts go only to customers who've said yes, and a STOP reply ends texting."

Only a named owner at the company (CTO, founder or compliance lead) closes one of these.

## 2. What it is not (hand-offs)

- What the product does with no legal weight (a tab, a path, where a note is saved) -> `product-claims`.
- How long registration or porting takes, "we file it for you" -> `setup-timelines`.
- What calls and texts cost, which plan has them -> `pricing-plans`.
- What a competitor promises its users -> `competitors-partners`.
- A count of complaints about data lock-in -> `numbers-and-sources`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The company's own published policy or docs: privacy policy, terms, help center article. Needs URL, date
   and scope. Scope matters: a privacy policy line about messages the company sends its own users does not
   cover texts an owner sends to their customers from the product.
2. A CONFIRMED row in `project/facts.md` that names the promise, with source and date.
3. A `project/decisions.md` row: the question, the decided wording, the named owner, the date.
4. For what the law or a gatekeeper requires: the gatekeeper's own documentation (the carrier registry's
   rules, the statute or regulation text), with the population it binds. State call-recording consent laws
   differ by state, so one national sentence is never enough.

Never a source: the brief; a competitor's practice; the model's summary of the law; a reviewer's
replacement text; an earlier draft; the draft's own "To confirm" list (questions, not decisions).

## 4. Forbidden shapes (banned by shape)

- **F1 Promise with no decision row.** A promise on a compliance topic in customer copy with no
  `project/decisions.md` row (owner and date) and no CONFIRMED facts row. Brackets do not rescue it: a
  bracketed promise is TO-CONFIRM and still needs the row. Cues: `opted in`, `said yes`, `STOP reply`,
  `call recording is`, `recording is off`, `never sold`, `never shared`, `never used`, `export any time`,
  `nothing is held back`, `takes it all with you`, `kept on the record`, `registered in your own name`,
  `audit trail`, `compliant`, `compliance is covered`. Class: invented-fact. Severity: critical.
- **F2 Two rules for one topic.** Two different rules or statuses for one topic across pieces. Cues: the
  same topic (recording, consent, export, retention, data use) matched in two or more pieces with
  different text. Class: contradiction. Severity: critical.
- **F3 Legal duty without its population.** A sentence says what the law requires of a group without
  naming who the rule binds. Cues: `owners must keep`, `you must retain`, `crews are required to archive`.
  Class: invented-fact. Severity: major.
- **F4 Regulatory or safety status with no record.** A sentence that says a regulator, an insurer or an auditor
  stands behind the company or its product, or that a loss, fee or risk cannot happen. Cues: `FDIC insured`,
  `regulated by`, `licensed`, `bank-grade`, `SOC 2 certified`, `ISO certified`, `guaranteed`, `risk-free`. The status needs the regulator's or auditor's own public record (a register entry, a
  certificate, a report with its date and scope), in a CONFIRMED `project/facts.md` row or a
  `project/decisions.md` row with a named owner. A partner's status is not the company's: a partner bank's
  insurance covers the partner's accounts, and the copy says whose it is. Brackets do not rescue F4. Class:
  invented-fact. Severity: critical.

## 5. Allowed with a row

- **A1** A promise whose wording matches a `project/decisions.md` row verbatim, with a named owner and a
  date. The copy may drop the bracket once the row exists.
- **A2** The company's current published policy, quoted, dated, with its scope.
- **A3** A pointer with no promise: "your own legal advice still applies".
- **A4** A topic named as a question for the live Q&A, with no answer in the copy.

## 6. Detection

**Stage 1: cues.** Format: `tools/README.md`. F1 and F2 carry messaging shapes (STOP replies, call recording, number
registration) next to generic ones (data use, export, retention). F4 carries the shapes of regulated money copy. A project
in another domain deletes the cues that do not apply and adds its own as banned cues in `project/voice.md`. F2 (`kind: topic`) fires when two pieces carry different
text for one topic after brackets and case are removed. The cues below hold no company, product,
competitor or partner names. Names that must never appear come from `project/voice.md`, which the
checker reads as banned cues.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | none    | regex | (?i)\b(?:opted[ -]in|said yes|STOP (?:reply|message)|reply STOP|call recording (?:is|stays|follows)|recording is (?:off|on)|never (?:sold|shared|used)|exports? (?:any ?time|everything)|nothing is held back|takes it all with you|kept on the (?:case|record|file)|registered in (?:your|the (?:owner|company)'s) own name|audit trail|compliant|compliance is covered)\b
F2     | copy   | none    | topic | recording=(?i)\bcall recording\b|\brecording (?:is|stays|follows)\b
F2     | copy   | none    | topic | consent=(?i)\bopted[ -]in\b|\bsaid yes\b|\bconsent\b
F2     | copy   | none    | topic | export=(?i)\bexports? (?:any ?time|everything)\b|\bnothing is held back\b
F2     | copy   | none    | topic | data-use=(?i)\bnever (?:sold|shared|used)\b
F3     | copy   | none    | regex | (?i)\b(?:owners?|techs?|technicians?|crews?|staff|operators?|you) (?:must|are required to|have to|need to) (?:keep|retain|store|archive)\b
F4     | copy   | none    | regex | (?i)\b(?:FDIC[ -]insured|(?:fully )?insured by|regulated by|(?:fully |state )?licensed|bank[ -]grade|SOC ?2(?: Type (?:1|2|I|II))? (?:certified|compliant)|ISO ?\d+ certified|guaranteed|risk[ -]free)\b
```

**Stage 2** (`rules/README.md`, Detection) receives the passage, the facts table and `project/decisions.md`,
and answers: which decision row, which owner, which date; for F2, which of the two rules the row supports.

## 7. Fixtures

```fixtures
{"id": "compliance-promises/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "The audit trail writes itself.", "source": "synthetic (Acme), shape: a bare audit-trail promise with no decision row"}
{"id": "compliance-promises/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "- [Texts go only to customers who've said yes, and a STOP reply ends texting to them automatically.]", "source": "synthetic (Acme), shape: bracketed consent and STOP promise, no owner row"}
{"id": "compliance-promises/F1/03", "rule": "F1", "expect": "fire", "target": "copy", "text": "- [Your customers, messages, and recordings export any time; nothing is held back if you leave.]", "source": "synthetic (Acme), shape: bracketed export and off-boarding promise, no decision recorded"}
{"id": "compliance-promises/F1/04", "rule": "F1", "expect": "fire", "target": "copy", "text": "For your office manager: texts go only to customers who've opted in, [from a number registered in your own name]; a STOP reply ends texting on its own;", "source": "synthetic (Acme), shape: 'opted in' unbracketed in one place, registration promise bracketed in the same sentence"}
{"id": "compliance-promises/F1/05", "rule": "F1", "expect": "fire", "target": "copy", "text": "If you ever leave, one export takes it all with you [confirm].", "source": "synthetic (Acme), shape: off-boarding promise with a confirm marker but no decision row"}
{"id": "compliance-promises/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "texts": [{"piece": "email", "text": "- [Call recording is off unless you turn it on.]"}, {"piece": "partner-note", "text": "[call recording follows the rule your company sets]; [every message is kept on the job card]."}], "source": "synthetic (Acme), shape: two control models for one recording switch across two pieces"}
{"id": "compliance-promises/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "Recording laws differ by state, and owners must keep recordings for years.", "source": "synthetic (Acme), shape: a legal duty stated for a group without naming the rule or who it binds"}
{"id": "compliance-promises/F4/01", "rule": "F4", "expect": "fire", "target": "copy", "text": "Pay by card on the invoice. Your balance is FDIC insured and every payout is risk-free.", "source": "synthetic (Acme), shape: an insurer and a no-risk status claim with no record behind it"}
{"id": "compliance-promises/F4/02", "rule": "F4", "expect": "fire", "target": "copy", "text": "[Acme Pay is licensed in all 50 states, with bank-grade security.]", "source": "synthetic (Acme), shape: a licence and a security grade in one bracketed sentence, no owner row"}
{"id": "compliance-promises/F4/n01", "rule": "F4", "expect": "no_fire", "target": "copy", "text": "Card payments are processed by LedgerLite Pay. Banking services are provided by Example Bank, Member FDIC. Fees are listed on the pricing page.", "source": "synthetic (Acme), shape: a partner's own disclosure line worded as the partner states it, and a pointer to the fee table"}
{"id": "compliance-promises/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Can't join live? Sign up anyway and the recording comes to you.", "source": "synthetic (Acme), shape: 'recording' as an event replay, no compliance promise"}
{"id": "compliance-promises/F1/n02", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Live Q&A (7 min): texting rules, your data and what happens if you leave, and your questions", "source": "synthetic (Acme), shape: topics named as Q&A questions, no promise (A4)"}
{"id": "compliance-promises/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "texts": [{"piece": "email", "text": "- [Call recording is off unless you turn it on.]"}, {"piece": "page", "text": "Can't join live? Sign up anyway and the recording comes to you."}], "source": "synthetic (Acme), shape: the topic matches in one piece only"}
{"id": "compliance-promises/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Nothing changes in the tools you give your crews today.", "source": "synthetic (Acme), shape: no duty verb attached to a group"}
```
