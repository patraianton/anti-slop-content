---
id: competitors-partners
version: 1
changed: 2026-10-02
asked_by: Anton Patrai
strictness: remove
applies_to: all
---

# Landmine: competitors, intermediaries, integration partners, gatekeepers

## 1. What this landmine is

Any line that names or implies another company the reader works with or buys from:

- a competitor, including its white labels;
- the reader's intermediary: the franchise office, reseller, association or network that hands the reader
  tools or sits above the reader's account;
- an integration partner (in the example project: an accounting import, a routing app);
- a gatekeeper the reader must pass (a registry, a carrier, a regulator) when the line names it loosely.

Strictness `remove`. Positioning against a partner is never kept on a citation alone.

## 2. What it is not (hand-offs)

- The product's own depth ("calls from the job card") → `product-claims`.
- What data the product shares with a partner or intermediary ("never shared with partners") → `compliance-promises`.
- Plan and price lines for intermediary or enterprise accounts → `pricing-plans`.
- Counts about a competitor ("335 complaints", "third-largest complaint") → `numbers-and-sources`.
- "The product has no X" set against a competitor → `research-absence` for the ABSENT; this file owns the frame.
- The bare competitor name cue → the never-does row for competitor names in `project/voice.md`.

## 3. Source of truth (resolution order; stop at the first that resolves)

1. The company's own rule on naming others: the never-does row for competitor names in `project/voice.md`.
2. A CONFIRMED row in `project/facts.md` from the company's help center or docs, or from the partner's own
   documentation, with URL and date. It sets the depth of an integration: direction (one-way or two-way),
   number of fields, what comes back, whether the partner has an integration page or only a support article.
   A line may go no deeper than its row.
3. For a gatekeeper: the gatekeeper's own documentation, dated.
4. A `project/decisions.md` row owned by a named owner at the company, on how the company positions an
   intermediary or a partner. Agents prepare the row; they do not close it.

Never a source: a partner logo strip ("Works with tools you already use"), the company's comparison pages,
a reviewer persona ("20-year plumber on LedgerLite"), reviewer replacement text, the brief's internal wording.

## 4. Forbidden shapes (banned by shape)

- **F1 Competitor framing.** A competitor named in a house-voice piece (cue: the never-does row in
  `project/voice.md`), or the "kill" or "replace" framing on any page that may be public: "kill the
  competition", "replace your scheduling app". In a piece in the author's voice, naming a competitor as a
  research subject is allowed (A4). Class: voice-drift. Severity: major.
- **F2 "Leave your intermediary's tools".** A line telling a reader who came through an intermediary to stop
  using or route around the tools the intermediary hands out, or giving the intermediary's office blanket
  sight of every member's conversations. Class: invented-fact. Severity: critical. Cues: `leave your
  franchisor`, `switch from your network`, `every owner's emails`, `your regional managers`.
- **F3 Integration deeper than the facts row.** "Book of record", "two-way", "posts back", "both list us in
  their catalogs" over a one-way import or a support article. Class: invented-fact. Severity: major.
- **F4 "One place" next to a kept partner.** "No jumping between systems", "one place for every customer
  conversation" in a piece that also says "keep LedgerLite". The phrase may be the company's own voice; the
  voice allowance does not clear a contradiction. Class: contradiction. Severity: major.
- **F5 Gatekeeper named loosely.** The gatekeeper called by a plural or a word that hides what it is: "registered
  with the carriers" for one registration with one registry and one texting provider. Use the word the
  gatekeeper's own documentation uses, or the reader word set in `project/voice.md`. The same shape covers
  money copy: "approved by the banks", "cleared by the regulators", or a partner bank's or processor's service
  described as the company's own ("our bank", "we are a bank") when the partner provides it. Class: voice-drift.
  Severity: minor.

## 5. Allowed with a row

- **A1** "Already on LedgerLite? Keep it for your books", with the import at the facts-row depth.
- **A2** "Your franchise office sees more": the office gets what the owner chooses to send with a request.
- **A3** "Nothing changes in the tools [Franchise name] gives you."
- **A4** In a piece in the author's voice only: a competitor named as a research subject, white labels named as
  findings.
- **A5** A partner named with its condition ("where your account has the import switched on").

## 6. Detection

**Stage 1.** Cue format as in `product-claims.md`. The cues marked "example domain" below fit the Acme example
(a franchise network, a texting registry). A project in another domain keeps the generic cues and swaps the
example-domain ones for its own intermediaries and gatekeepers (a partner bank, a card network, a payment processor). F1 and F2 are never rescued. The cues name no company,
product or partner. Project names (competitors, intermediaries, partners) come from `project/voice.md`,
which the checker reads for banned cues.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | none    | regex | (?i)\bkill(?:s|ing)?\b.{0,30}\b(?:competitors?|competition|rivals?|incumbents?)\b
F1     | copy   | none    | regex | (?i)\breplace (?:your|their) (?:(?:scheduling|invoicing|billing|booking|dispatch|quoting) )?(?:software|app|apps|system|tool|tools|stack)\b
# example domain: franchise network
F2     | copy   | none    | regex | (?i)\b(?:leave|ditch|drop|switch from|instead of) your (?:franchisor|franchise|reseller|association|network|distributor|head office|parent company)(?:'s)?\b
F2     | copy   | none    | regex | (?i)\bevery (?:owner|member|franchisee|tech)'s (?:emails?|calls?|texts?)\b
F2     | copy   | none    | regex | (?i)\byour (?:marketers|regional managers|area managers|franchise managers)\b
# generic: integration depth
F3     | copy   | bracket | regex | (?i)\bbook of record\b
F3     | copy   | bracket | regex | (?i)\b(?:two-way|bi-?directional) (?:sync|integration|import)\b
F3     | copy   | bracket | regex | (?i)\bposts? back to\b
F3     | copy   | bracket | regex | (?i)\bboth list [^.;)]{1,40} in their (?:catalogs?|marketplaces?|directories|app stores?)\b
F4     | copy   | bracket | regex | (?i)\bno (?:jumping|switching) between (?:systems|apps|tools)\b
F4     | copy   | bracket | regex | (?i)\bone place for every\b
# example domain: texting registry
F5     | copy   | bracket | regex | (?i)\bregistered with the carriers\b
F5     | copy   | bracket | regex | (?i)\bcarrier (?:approval|registration)\b
# generic: money copy
F5     | copy   | bracket | regex | (?i)\b(?:approved|cleared|authori[sz]ed|licensed) (?:by|with) the (?:banks|regulators|authorities|card networks|processors)\b
F5     | copy   | bracket | regex | (?i)\b(?:we are a bank|our bank)\b
```

**Stage 2** (`rules/README.md`) gets the passage, the piece name and the `facts.md` rows for the named
company. It answers: is the company named in a piece that allows it, and does the line stay at the depth
of its row.

## 7. Fixtures

Every row is a synthetic Acme sentence with the shape the rule tests.

```fixtures
{"id": "competitors-partners/F3/01", "rule": "F3", "expect": "fire", "target": "copy", "text": "Your customers and jobs are already here. Keep LedgerLite as your book of record", "source": "synthetic (Acme), shape: partner called the book of record over a one-way import"}
{"id": "competitors-partners/F3/02", "rule": "F3", "expect": "fire", "target": "copy", "text": "> Nothing to set up. Your customers are already here. LedgerLite stays your book of record.", "source": "synthetic (Acme), shape: book of record in a social post"}
{"id": "competitors-partners/F3/03", "rule": "F3", "expect": "fire", "target": "copy", "text": "Day to day, owners lose the thread in the inbox, a spreadsheet, LedgerLite or MapRoute (both list Acme in their catalogs)", "source": "synthetic (Acme), shape: catalog claim over a partner that has a support article only"}
{"id": "competitors-partners/F3/04", "rule": "F3", "expect": "fire", "target": "copy", "text": "The LedgerLite link is a two-way sync, so paid invoices post back to the job card.", "source": "synthetic (Acme), shape: two-way and posts-back claim over a one-way import"}
{"id": "competitors-partners/F2/01", "rule": "F2", "expect": "fire", "target": "copy", "text": "**Run a franchise or a dispatch desk?** Every owner's emails, calls and texts land on the shared job, so your regional managers see the full story without the email thread.", "source": "synthetic (Acme), shape: blanket visibility for the intermediary's office"}
{"id": "competitors-partners/F2/02", "rule": "F2", "expect": "fire", "target": "copy", "text": "Owners who want a cleaner setup can leave your franchisor's tools behind and work in Acme only.", "source": "synthetic (Acme), shape: telling an intermediary-sourced reader to drop the intermediary's tools"}
{"id": "competitors-partners/F4/01", "rule": "F4", "expect": "fire", "target": "copy", "text": "> No jumping between systems. One place for every customer conversation, from first call to final invoice. Already on LedgerLite? Keep it.", "source": "synthetic (Acme), shape: one-place promise next to a kept partner"}
{"id": "competitors-partners/F5/01", "rule": "F5", "expect": "fire", "target": "copy", "text": "Texting needs each number registered with the carriers first (10 to 15 business days); today's LedgerLite link is a one-way import.", "source": "synthetic (Acme), shape: gatekeeper named with a loose plural"}
{"id": "competitors-partners/F1/01", "rule": "F1", "expect": "fire", "target": "copy", "text": "**Deliberately left out.** \"Kill / replace the other apps\" or any competitor by name; \"replace your scheduling app\";", "source": "synthetic (Acme), shape: replace-your-tool framing on a page that may be public"}
{"id": "competitors-partners/F1/02", "rule": "F1", "expect": "fire", "target": "copy", "text": "Job Thread will kill the competition for your customers' attention.", "source": "synthetic (Acme), shape: kill framing against competitors"}
{"id": "competitors-partners/F3/n01", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Already on LedgerLite? Keep it for your books - bring any invoice in with one click, as you do today.", "source": "synthetic (Acme), shape: partner kept, import at the facts-row depth, no depth word"}
{"id": "competitors-partners/F3/n02", "rule": "F3", "expect": "no_fire", "target": "copy", "text": "Keep LedgerLite as [your book of record] and import the six fields.", "source": "synthetic (Acme), shape: depth word inside brackets, the cue matches and the bracket rescue silences it by design"}
{"id": "competitors-partners/F2/n01", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "- [Owners on a franchise account only] **Quotes with the whole story.** Click Request Quote as you do today and [pick the texts and call notes that go with it] - [Franchise name]'s office quotes for what the customer actually asked. Nothing changes in the tools [Franchise name] gives you.", "source": "synthetic (Acme), shape: intermediary office named, nothing taken away, owner chooses what is sent"}
{"id": "competitors-partners/F2/n02", "rule": "F2", "expect": "no_fire", "target": "copy", "text": "- Nothing changes in the tools you give your owners today. [You decide whether calling and texting are switched on for your franchise account, and who pays for them.]", "source": "synthetic (Acme), shape: partner-note line that leaves the intermediary's tools alone"}
{"id": "competitors-partners/F1/n01", "rule": "F1", "expect": "no_fire", "target": "copy", "text": "Owners meet the same pain under other app names (DispatchPro, RouteKing), so the launch copy names no competitor; it answers the complaints one component at a time.", "source": "synthetic (Acme), shape: how-made note naming competitors as research findings, no kill or replace framing"}
{"id": "competitors-partners/F4/n01", "rule": "F4", "expect": "no_fire", "target": "copy", "text": "Texts, calls and emails with a customer stay on the job card. Keep LedgerLite for your books.", "source": "synthetic (Acme), shape: partner kept with no one-place promise"}
{"id": "competitors-partners/F5/03", "rule": "F5", "expect": "fire", "target": "copy", "text": "Acme Pay is approved by the regulators, so you can take cards on day one.", "source": "synthetic (Acme), shape: money-copy gatekeeper hidden behind a loose plural"}
{"id": "competitors-partners/F5/04", "rule": "F5", "expect": "fire", "target": "copy", "text": "Your float sits in our bank, not in a spreadsheet.", "source": "synthetic (Acme), shape: a partner bank's service described as the company's own"}
{"id": "competitors-partners/F5/n03", "rule": "F5", "expect": "no_fire", "target": "copy", "text": "Your float sits in an account at Example Bank, our partner bank, and Acme is not a bank.", "source": "synthetic (Acme), shape: the partner bank named with its role, no loose plural"}
{"id": "competitors-partners/F5/n01", "rule": "F5", "expect": "no_fire", "target": "copy", "text": "| 0:17 | Job booked, notes on the job card, invoice prefilled (LedgerLite, where your account has the import switched on) |", "source": "synthetic (Acme), shape: partner named with its condition, no gatekeeper word"}
{"id": "competitors-partners/F5/n02", "rule": "F5", "expect": "no_fire", "target": "copy", "text": "Texting needs each number on the carrier registry first (10 to 15 business days).", "source": "synthetic (Acme), shape: gatekeeper named with the registry word, not the loose plural"}
```
