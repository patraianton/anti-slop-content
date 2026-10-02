---
id: plain-language
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: rewrite
applies_to: all
---

# Landmine: plain language

## 1. What this landmine is
Copy that explains a feature, a price or a step with more words, or harder words, than its meaning needs. One idea per sentence.

Example (Acme Dispatch): "Text any customer from your business number." Not: "Texting is available for outreach to any customer record, subject to your plan."

## 2. What it is not (hand-offs)
- Whether the sentence is true: `product-claims`, `pricing-plans`, `setup-timelines`, `compliance-promises`, `process-claims`, `research-absence`.
- A number, rank, share or quote: `numbers-and-sources`.
- A competitor or partner named or described: `competitors-partners`.
- Banned words and the company's own recurring phrases: `rules/voice.md` and `project/voice.md`.

## 3. Source of truth (resolution order; stop at the first that resolves)
1. A `project/decisions.md` row with an agreed rewrite: the old wording, the new wording, the named owner, the date.
2. The `terms` block of `project/voice.md`: the company's own terms, each with the plain words that explain it.
3. The company's help center or docs, dated, for the plain words of a product term.
4. For a gatekeeper term (carrier registration, number porting, consent law): the gatekeeper's own documentation, dated.
5. A CONFIRMED row in `project/facts.md`, when the plain words state a fact.

If none resolves, the term fails F4 until the sentence explains it. Never a source: the brief; a reviewer's replacement text; an earlier draft; the model's idea of what readers know.

## 4. Forbidden shapes
Scope: every piece whose entry in `project/pieces.json` has `plain: true`. F6 runs only on pieces with a `grade_max`, over the part named by `grade_scope`. Skipped: the hook of a piece (the paragraph marked by `hook` in `pieces.json`) and quoted speech, which counts as one word.

- **F1 Long sentence.** More than 20 words. Was "Job Thread drafts each reminder from the quote you sent and your notes from the call, and it waits on the job card for you to edit, send, or skip." → now two sentences. Class: filler. Severity: major.
- **F2 Overloaded item.** A list item or agenda row with a semicolon, two dash asides, or more than three sentences after its bold label and more than 30 words. Was "Calls, texts, emails: all from the job card." with five clauses → now "**Calls, texts, emails.** Call from your phone. Text any customer [from your business number]. Send your booking link. Each call, text and email is saved on the job card." (four short sentences, under 30 words). Class: filler. Severity: major.
- **F3 Repeated phrase.** One 3-word phrase 3 times in one item or paragraph; a changed preposition is the same phrase. Was "from the job card ... on the job card ... on the job card" in one bullet → now once. Class: filler. Severity: minor.
- **F4 Term not explained.** A term outside the project's `terms` block and plain English, with no plain words in its sentence or the one before; a project term in a heading with no plain words on the same line. Was "Lead to 10DLC Approval" → now "from first call to a texted quote". Class: voice-drift. Severity: minor.
- **F5 Side-note title as shorthand.** "=", "X, not Y" with no subject, "line" for a line of the email. Was "Quote line = send, not chase." → now "Job Thread: the owner sends, the crew does not watch." Class: filler. Severity: major.
- **F6 Hard section.** Flesch-Kincaid grade above the `grade_max` of the piece in `project/pieces.json`. Was numbered how-made steps at grade 15.8 → now 6.2, one fact per sentence. Class: filler. Severity: major.
- **F7 Feature with history or reason.** "until now", "as before", "because", "so that" in feature copy. Was "Text any customer - until now, texting was for new leads only." → now "Text any customer." and the history in a side note. Class: filler. Severity: major.

## 5. Allowed with a row
- **A1** The company's own terms in body copy, when they are in the `terms` block of `project/voice.md`.
- **A2** History and reasons in side notes.
- **A3** A short casual opener such as "So, we fixed it."
- **A4** A list of short actions in one item.

## 6. Detection
Check `plain` (`tools/README.md`): the cues below select F2, F5 and F7; code counts F1, F3, F4 and F6. The cues hold no company, product, competitor or partner names. Names that must never appear come from `project/voice.md`, which the checker reads as banned cues.
`plain-ok` lists abbreviations readers know; `jargon` lists words that need plain words next to them. A project adds its own terms in the `terms` block of `project/voice.md`.

Stage 2 receives the flagged passage with its rule id, the landmine's forbidden and allowed lists, and the `terms` block, and judges only that passage.

```cues
# rule | target | rescues | kind  | pattern
F2     | copy   | none    | regex | ;
F2     | copy   | none    | regex | \s[-\u2013\u2014]\s|\u2014
F5     | copy   | none    | regex | =
F5     | copy   | none    | regex | (?i)(?:^|[=:]\s*)(?:\w+\s+)?\w+,\s+not\s+\w+
F5     | copy   | none    | regex | (?i)(?<!office )(?<!phone )(?<!support )(?<!help )(?<!subject )(?<!bottom )\bline\b
F7     | copy   | none    | regex | (?i)\b(?:until now|until today|as before|no longer|previously|because|so that|which is why|that's why)\b|,\s+so\s+(?:you|your|they|their|the|it)\b
```

```plain-ok
AM PM PT CT ET MT US Q&A LIVE OK FAQ SMS PDF
```

```jargon
\bopt-?outs?\b
\bporting\b
\binbox sync\b
\bdeliverability\b
```

## 7. Fixtures

```fixtures
{"id": "plain-language/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "piece": "email", "text": "- **Follow-ups that don't slip.** Job Thread drafts each reminder from the quote you sent and your notes from the call, and it waits on the job card for you to edit, send, or skip.", "source": "synthetic (Acme), shape: one list item whose single sentence runs past 20 words"}
{"id": "plain-language/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "piece": "email", "text": "- **Follow-ups that don't slip.** Job Thread drafts each reminder from the quote you sent and your notes from the call. The draft waits on the job card for you to edit, send, or skip.", "source": "synthetic (Acme), shape: the same item split into two sentences under 20 words"}
{"id": "plain-language/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "piece": "email", "text": "- **Calls, texts, emails: all from the job card.** Call from your phone. Text any customer [from your business number] - until now, texting was for new leads only. Send your booking link; the visit and its reminder land on the job card. All of it is saved on the job card automatically.", "source": "synthetic (Acme), shape: a list item with a semicolon and a dash aside"}
{"id": "plain-language/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "piece": "email", "text": "- **Calls, texts, emails.** Call from your phone. Text any customer [from your business number]. Send your booking link. Each call, text and email is saved on the job card.", "source": "synthetic (Acme), shape: the same item as four short sentences, no semicolon, no dash aside"}
{"id": "plain-language/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "piece": "email", "text": "- **Calls, texts, emails: all from the job card.** Call from your phone. Text any customer [from your business number] - until now, texting was for new leads only. Send your booking link; the visit and its reminder land on the job card. All of it is saved on the job card automatically.", "source": "synthetic (Acme), shape: one 3-word phrase three times in one item, once with a changed preposition"}
{"id": "plain-language/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "piece": "email", "text": "- **Calls, texts, emails.** Call from your phone. Text any customer [from your business number]. Send your booking link. Each call, text and email is saved on the job card.", "source": "synthetic (Acme), shape: the same item with the phrase used once"}
{"id": "plain-language/F4/01", "rule": "F4", "expect": "fire", "target": "copy", "piece": "page", "text": "**Watch Us Take a Customer from Lead to 10DLC Approval - Without Leaving Acme Dispatch (Live Demo)**", "source": "synthetic (Acme), shape: an abbreviation-shaped term in a heading with no plain words on the line"}
{"id": "plain-language/F4/n01", "rule": "F4", "expect": "no_fire", "target": "copy", "piece": "page", "text": "**Live demo: one customer, from first call to a texted quote, without leaving Acme Dispatch**", "source": "synthetic (Acme), shape: the heading restated in plain words, no abbreviation"}
{"id": "plain-language/F5/01", "rule": "F5", "expect": "fire", "target": "copy", "piece": "email", "text": "**Side notes: why it reads this way**\n4. **Quote line = send, not chase.** Job cards already exist; attaching the conversation to the quote is the new part.", "source": "synthetic (Acme), shape: side-note title built with =, an unsubjected \"X, not Y\" and \"line\" for a line of the email"}
{"id": "plain-language/F5/n01", "rule": "F5", "expect": "no_fire", "target": "copy", "piece": "email", "text": "**Side notes: why it reads this way**\n4. **Job Thread: the owner sends, the crew does not watch.** Job cards already exist in Acme Dispatch. New: the owner picks which texts and call notes go with the quote. The crew sees only what the owner sent.", "source": "synthetic (Acme), shape: side-note title as a full sentence with a subject"}
{"id": "plain-language/F6/01", "rule": "F6", "expect": "fire", "target": "copy", "piece": "how-made", "text": "The rules, the checker and the record of this run: [github.com/example/anti-slop-content](https://github.com/example/anti-slop-content)\n\n1. I went through the public record of Acme Dispatch: all 41 help-center articles, the 12 release notes and the 9 recorded demonstrations, which I searched by their captions and sorted by the product area that each of them describes: [research.html](https://example.com/research.html)\n2. I read 2,140 public customer reviews about two competing scheduling products and sorted 335 complaints by product area, with counts that are close but not exact because two research passes examined the same review sites: [complaints.html](https://example.com/complaints.html)\n3. The owner portrait is built from 155 forum threads, 769 job-board reviews and 98 company websites, and the house voice of Acme Dispatch comes from its own earlier launches: [voice.md](https://example.com/voice.md)\n4. Research and writing agents that I run produced the text between September 30 and October 2, and six simulated reader roles from one model family reviewed an earlier version in four rounds, after which the text changed and only the checker has examined this version: [misses.md](https://example.com/misses.md)", "source": "synthetic (Acme), shape: numbered how-made steps of long stacked sentences, grade above 11 (about 15.8)"}
{"id": "plain-language/F6/n01", "rule": "F6", "expect": "no_fire", "target": "copy", "piece": "how-made", "text": "1. I went through the public record of Acme Dispatch: all 41 help-center articles and the 12 release notes. I searched the 9 recorded demos by their captions. I sorted all of it by product area: [research.html](https://example.com/research.html)\n2. I read 2,140 public customer reviews about two competing scheduling products. I sorted 335 complaints by product area. The counts are close, not exact, because two research passes read the same review sites: [complaints.html](https://example.com/complaints.html)\n3. The owner portrait uses 155 forum threads, 769 job-board reviews and 98 company websites. The house voice comes from Acme Dispatch's own earlier launches: [voice.md](https://example.com/voice.md)\n4. AI agents I run did the research and wrote the text, September 30 to October 2. Six simulated readers from one AI model family reviewed an earlier version in four rounds. The text changed after that. Only the checker has examined this version: [misses.md](https://example.com/misses.md)", "source": "synthetic (Acme), shape: the same steps, one fact per sentence, grade below 11 (about 6.2)"}
{"id": "plain-language/F7/01", "rule": "F7", "expect": "fire", "target": "copy", "piece": "email", "text": "Text any customer [from your business number] - until now, texting was for new leads only.", "source": "synthetic (Acme), shape: history (\"until now\") inside feature copy"}
{"id": "plain-language/F7/n01", "rule": "F7", "expect": "no_fire", "target": "copy", "piece": "email", "text": "**Side notes: why it reads this way**\n3. **Texting before this launch.** Until now, texting was for new leads only.", "source": "synthetic (Acme), shape: the history moved to a side note, which the check skips by scope (a rescue by design)"}
```
