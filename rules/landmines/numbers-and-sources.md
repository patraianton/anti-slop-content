---
id: numbers-and-sources
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: cite-or-cut
applies_to: all
---

# Landmine: numbers, ranks, shares, superlatives and quotes

## 1. What this landmine is

Every count, rank, share, superlative and quote put in front of a reader: "41 help-center articles",
"third-largest complaint", "64% of all complaints", "the most frequent complaint", "as one owner put it".

Strictness `cite-or-cut`: a number stays only with a record in `project/numbers.json`, printed at the
precision that record allows.

## 2. What it is not (hand-offs)

- Prices, minutes, texts and plan limits: `pricing-plans`. Setup times: `setup-timelines`.
- Counts of the process itself ("three review rounds", "five readers", "seven fix scripts"): `process-claims`.
- "The company has no X", "nobody asks for Y": `research-absence`. A zero inside a study ("None about
  invoicing") stays here and needs a record with value 0.
- What a feature does or how it works: `product-claims`. A named competitor or partner, and anything
  said about them that is not a count, rank or quote: `competitors-partners`. A rank about a competitor
  stays here.
- Retention periods, consent and recording promises: `compliance-promises`.
- A true number in a sentence the reader cannot parse: `plain-language`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. `project/numbers.json`: `{id, value, unit, what, precision, source_file, source_line, caveat}`.
   `precision` is `exact | approximate | double-counted | lane-stopped`. `approximate` renders as
   "about N". `double-counted` and `lane-stopped` (a source stopped before it was read in full) render
   with "about" or with the caveat, in the same sentence or in an earlier sentence of the same `##`
   section. When two files give different counts for one quantity, the record keeps the value it trusts
   and lists the others under `conflicts`.
2. Ranks and shares are computed by `tools/check.py` from a `kind: table` record (for example the
   review table `T-reviews`) and a `kind: rank | share` record that names the table, the row and the
   result. A rank holds on a double-counted table (the order of rows survives counts that are close); a
   share does not, so a share inherits the table's precision. Table rows are inputs: a row count printed
   in copy needs its own record.
3. Quotes are rows of the Quotes table in `project/facts.md`: text, speaker and role, where, date,
   weight. The text may be shortened; the role and the weight travel with it.

A record's `source_file` and `source_line` point to one of these, in this order of trust:

1. The company's own help center or docs, with the date opened.
2. A CONFIRMED row in `project/facts.md`.
3. A `project/decisions.md` row owned by a named owner (for a count the company chooses to publish).
4. The gatekeeper's own documentation (for a count about a registry, a carrier rule or a law).

Never a source: a number in an earlier draft, a reviewer's replacement text, a public page built from the
same research (a consumer of `numbers.json`), a number the writer remembers.

## 4. Forbidden shapes (banned by shape)

- **F1 Number with no record.** A count in the text that `numbers.json` does not hold. Class: invented-fact.
  Severity: major.
- **F2 Typed rank or superlative.** "top-ten", "third-largest", "most frequent", "number one" with no
  computed row, or a computed row that disagrees. Class: false-precision. Severity: critical.
- **F3 Precision dropped.** A record that is not `exact`, printed bare. Class: false-precision. Severity: major.
- **F4 Two values for one quantity.** A value that a record lists under `conflicts` ("38 articles"
  against a record of 41 articles that lists 38). Class: contradiction. Severity: major.
- **F5 Quote reframed.** The role in the text differs from the record ("one owner" for a crew lead of 8).
  Class: invented-fact. Severity: major.
- **F6 Generalisation from n=1.** "Their posts open X" over a habit seen once. Class: false-precision.
  Severity: minor.

## 5. Allowed with a row

- **A1** An exact count with its record ("all 41 help-center articles", "9 video recordings").
- **A2** An approximate count as "about N" ("about 60 forum threads").
- **A3** A double-counted total with its caveat ("counts are close, not exact: two sources cover the
  same review sites").
- **A4** A rank that matches its computed row ("the mobile app is the third-largest complaint in the
  review table").
- **A5** A quote with its recorded role ("as one crew lead put it").

## 6. Detection

**Stage 1.** `number` cues: `tools/check.py` takes each number in the line, skipping placeholders (`[N]`,
`$X`), years, times of day, a list number at line start, and anything inside quotation marks. It looks the
number up in `numbers.json` by value (the unit word after it picks between records with the same value).
No record: F1, or F4 when a record lists the value under `conflicts`. A record that is not `exact` and no
hedge in the line or in an earlier line of the same `##` section: F3. A number right after "about",
"around", "roughly" or "~" is hedged on its own. `rank` cues: a hit unless a computed record whose `phrase`
occurs in the line recomputes from its table. A percentage needs a record with unit `%` or a computed
`share` record whose phrase is in the line. No `numbers.json`, or a rank record whose table is missing:
`not_run`.

The F5 role words below are generic reader roles. Company and product names are not in these patterns;
names a project bans come from `project/voice.md`, which the checker reads.

```cues
# rule | target | rescues | kind   | pattern
F1     | copy   | bracket | number | \b\d{1,3}(?:,\d{3})+\b|\b\d+(?:\.\d+)?\b
F3     | copy   | bracket | number | (?i)\bclose, not exact\b|\bcounted twice\b|\bdouble[- ]counted\b|\b(?:lane|source) (?:was )?stopped\b
F2     | copy   | none    | rank   | (?i)\btop[- ](?:three|five|ten|\d+)\b
F2     | copy   | none    | rank   | (?i)\b(?:second|third|fourth|fifth)[- ]largest\b
F2     | copy   | none    | rank   | (?i)\bmost (?:frequent|common|named|cited)\b
F2     | copy   | none    | rank   | (?i)\b(?:number one|no\. ?1|#1)\b
F5     | copy   | none    | regex  | (?i)\b(?:as )?(?:one|an?) (?:owner|tech|technician|dispatcher|user|customer|reviewer|member|person|operator|manager|pro|founder|controller|CFO|cardholder|merchant|advisor|buyer|admin|developer) (?:put it|said|wrote)\b
F6     | copy   | none    | regex  | (?i)\btheir (?:posts|emails|launches) (?:open|start|end)\b
```

**Stage 2** (`rules/README.md`) gets the sentence, the matched record and its source line. It answers:
same quantity or not, precision kept or not, role kept or not.

## 7. Fixtures

`must_fire` rows are synthetic Acme sentences with the shape of the rule. Records a row is judged against
travel inline in `numbers`. With the records present, every `no_fire` row passes; remove its records and
the first `no_fire` row of F1 must fire F1. The F1 `number` cue matches every digit in a `no_fire` text
by design: the record, not the pattern, rescues it.

```fixtures
{"id": "numbers-and-sources/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "The owner portrait comes from about 600 plumber-forum posts, 41 help-center articles and 9 video recordings.", "source": "synthetic (Acme), shape: a rounded count that no record holds, next to counts that have records", "numbers": [{"id": "N-01", "value": 41, "unit": "articles", "precision": "exact"}, {"id": "N-03", "value": 9, "unit": "recordings", "precision": "exact"}]}
{"id": "numbers-and-sources/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "412 plumber posts and ~20 forum threads where owners discuss quotes and follow-ups; 100 supplier websites for free tools", "source": "synthetic (Acme), shape: a list of counts with no record at all, one of them written with a tilde", "numbers": []}
{"id": "numbers-and-sources/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "text": "Export: jobs, messages and recordings export any time, and nothing is held back if a tech leaves (missed callbacks are a top-ten complaint in the review table).", "source": "synthetic (Acme), shape: a typed top-N rank with no computed row behind it", "numbers": [{"id": "T-reviews", "kind": "table", "rows": {"Support": 120, "Billing": 95, "Mobile app": 80, "Scheduling": 40}}]}
{"id": "numbers-and-sources/F4/01", "rule": "F4", "expect": "fire", "target": "copy", "text": "Help center: 38 articles listed", "source": "synthetic (Acme), shape: a value the record lists under conflicts, printed instead of the trusted value", "numbers": [{"id": "N-01", "value": 41, "unit": "articles", "precision": "exact", "conflicts": [38]}]}
{"id": "numbers-and-sources/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "The research covers 4,120 public reviews and 2,310 complaints sorted by area:", "source": "synthetic (Acme), shape: a double-counted total printed bare, next to an exact count", "numbers": [{"id": "N-07", "value": 4120, "unit": "reviews", "precision": "exact"}, {"id": "N-08", "value": 2310, "unit": "complaints", "precision": "double-counted", "caveat": "two sources cover the same review sites"}]}
{"id": "numbers-and-sources/F5/01", "rule": "F5", "expect": "fire", "target": "copy", "text": "the rule that every feature line says where it is saved, because, as one owner put it in a trade-forum thread, \"A schedule that is 60% current is worse than a whiteboard everyone trusts.\"", "source": "synthetic (Acme), shape: the speaker is named by a broader or different role than the quotes table records (a crew lead of 8 techs)", "numbers": []}
{"id": "numbers-and-sources/F6/01", "rule": "F6", "expect": "fire", "target": "copy", "text": "their posts open \"New this week:\" and end on a link or a question", "source": "synthetic (Acme), shape: a pattern claimed about all of someone's posts from a single sighting", "numbers": []}
{"id": "numbers-and-sources/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "the owner portrait built from 41 help-center articles, about 60 owner-forum threads, 12 release notes and 9 video recordings matched it", "source": "synthetic (Acme), shape: every count has a record, and the approximate one is hedged with about", "numbers": [{"id": "N-01", "value": 41, "unit": "articles", "precision": "exact"}, {"id": "N-02", "value": 60, "unit": "threads", "precision": "approximate"}, {"id": "N-05", "value": 12, "unit": "release notes", "precision": "exact"}, {"id": "N-03", "value": 9, "unit": "recordings", "precision": "exact"}]}
{"id": "numbers-and-sources/F1/n02", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Read the public record: all 41 help-center articles", "source": "synthetic (Acme), shape: one exact count with its record", "numbers": [{"id": "N-01", "value": 41, "unit": "articles", "precision": "exact"}]}
{"id": "numbers-and-sources/F1/n03", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Owners blame the company before the features: support and billing are 64% of all complaints", "source": "synthetic (Acme), shape: a percentage backed by a computed share record, (120 + 95) / 335 = 64.2%", "numbers": [{"id": "T-reviews", "kind": "table", "rows": {"Support": 120, "Billing": 95, "Mobile app": 80, "Scheduling": 40}}, {"id": "S-support-billing", "kind": "share", "phrase": "64% of all complaints", "table": "T-reviews", "rows": ["Support", "Billing"], "result": 64, "precision": "exact"}]}
{"id": "numbers-and-sources/F4/n01", "rule": "F4", "expect": "no_fire", "target": "copy", "text": "all 41 help-center articles, the 12 release notes and 9 video recordings", "source": "synthetic (Acme), shape: the trusted value is printed, the conflicting value (38) is not", "numbers": [{"id": "N-01", "value": 41, "unit": "articles", "precision": "exact", "conflicts": [38]}, {"id": "N-05", "value": 12, "unit": "release notes", "precision": "exact"}, {"id": "N-03", "value": 9, "unit": "recordings", "precision": "exact"}]}
{"id": "numbers-and-sources/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "sorted 2,310 complaints by area (counts are close, not exact: two sources cover the same review sites):", "source": "synthetic (Acme), shape: a double-counted total printed with its caveat in the same sentence", "numbers": [{"id": "N-08", "value": 2310, "unit": "complaints", "precision": "double-counted", "caveat": "two sources cover the same review sites"}]}
{"id": "numbers-and-sources/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "4. The mobile app is the third-largest complaint in the review table.", "source": "synthetic (Acme), shape: a typed rank that matches its computed row (3 of 4)", "numbers": [{"id": "T-reviews", "kind": "table", "rows": {"Support": 120, "Billing": 95, "Mobile app": 80, "Scheduling": 40}}, {"id": "R-mobile", "kind": "rank", "phrase": "third-largest complaint", "table": "T-reviews", "row": "Mobile app", "result": 3}]}
{"id": "numbers-and-sources/F5/n01", "rule": "F5", "expect": "no_fire", "target": "copy", "text": "because, as one crew lead put it in a trade-forum thread, _\"A schedule that is 60% current is worse than a whiteboard everyone trusts.\"_", "source": "synthetic (Acme), shape: the role in the text is the role in the quotes table", "numbers": []}
```

Fixtures test stage 1 only. Stage 2 receives the sentence, the matched record and its source line, and nothing else from the file.
