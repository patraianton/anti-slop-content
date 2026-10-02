# tools/

Python 3.11, standard library only. `.github/workflows/check.yml` runs the same commands on Linux.

| file | what it does |
|---|---|
| `check.py` | step 5 (Lint) and the step 8 release checks on one piece, its page, numbers file, facts table, coverage map, decision log and claims ledger |
| `selftest.py` | every fixture fires or stays silent as recorded; every forbidden shape has a passing fire fixture |
| `fixtures/pieces.json` | the synthetic piece types the fixtures use (the five Acme piece types). Only `selftest.py` loads it |
| `fixtures/must_fire.jsonl` | synthetic lines that must fire |
| `fixtures/must_not_fire.jsonl` | synthetic clean lines that must stay silent |

## Run

```
python tools/selftest.py
python tools/check.py path/to/draft.md --project path/to/project
python tools/check.py path/to/draft.md --project path/to/project --html path/to/page.html
python tools/check.py path/to/draft.md --project path/to/project --html page.html \
       --panel path/to/panel --reviewed-sha256 <hash> --stamp          # release (step 8)
python tools/check.py path/to/draft.md --project path/to/project --json
python tools/check.py note.md --piece-type email                       # a file that holds one piece
```

`selftest.py` takes `--verbose` (also print the fixtures that pass). It reads only `rules/` and `tools/fixtures/`.

## Flags of check.py

The one positional argument is the piece: a markdown file, or a page with the suffix `.html` or `.htm`.

| flag | default | meaning |
|---|---|---|
| `--project DIR` | `project/` in this repo | the project layer. Supplies the defaults of `--numbers`, `--facts`, `--coverage`, `--decisions` and `--claims`, and holds `voice.md` and `pieces.json`. A `DIR` that is not a folder is exit 2. The default folder is not tested for existence |
| `--numbers FILE` | `<project>/numbers.json` | records for the `numbers` check |
| `--facts FILE` | `<project>/facts.md` | the facts table |
| `--coverage FILE` | `<project>/coverage.md` | the coverage map |
| `--decisions FILE` | `<project>/decisions.md` | the decision log; only its killed-lines table is read |
| `--claims FILE` | `<project>/claims.csv` if that file exists | the claims ledger. A project ledger found by default is never required |
| `--html FILE` | none | the rendered page of the piece. Turns on `parity`, the label search, the dotted-span count and the tooltip read |
| `--panel DIR` | none | folder of `round-*.md` review reports (process-claims F3) |
| `--reviewed-sha256 HASH` | none | sha256 of the last reviewed version (`release-hash`, process-claims F4) |
| `--stamp` | off | append one stage-1 stamp per landmine to `<piece>.stamps.jsonl` (shape in `rules/README.md`, Detection) |
| `--landmines DIR` | `rules/landmines` | folder of landmine files (`README.md` in it is skipped) |
| `--voice FILE` | `rules/voice.md` | the generic voice file. `<project>/voice.md` is merged with it (read once if both are the same file) |
| `--max-marks N` | `max_marks` of `pieces.json`, else 7 | the mark limit per `##` section |
| `--dotted-class NAME` | `dotted_class` of `pieces.json`, else `tbc` | the HTML class of a dotted (to-confirm) span |
| `--piece-type ID` | none | tags a markdown file that holds one piece (see "How a piece is read"). When the project lists pieces, `ID` must be one of them, else exit 2 |
| `--require-all` | off | a check that was not requested also makes the exit 3 |
| `--json` | off | print JSON instead of lines and a table |

`pieces.json` and the project `voice.md` have no flag of their own: they are read from `--project`.

## Exit codes

`0` clean, `1` findings, `2` bad invocation, `3` not run. 3 outranks 1.

Exit 2: an unknown flag, a `--project` that is not a folder, a `--piece-type` that the project does not list.

Exit 3 comes from a check that is required and is `not_run`, `uncertain` or incomplete:

- the piece file is missing;
- the landmines folder is missing or holds no landmine file;
- a landmine file with an error (a pattern that does not compile, matches the empty string or holds a control
  character; a bad `strictness`; an `applies_to` id that `pieces.json` does not list; a fixtures line that is not
  JSON), a landmine with no cues, or a `plain-language` file with no cue for F2, F5 or F7;
- the generic voice file is missing, has no banned cues, or either voice file has an error;
- `pieces.json` has an error (bad JSON, a regex that does not compile, a control character, a bad `voice` or
  `grade_scope` value, a duplicate id);
- a numbers file that cannot be read as JSON, or a `--numbers`, `--decisions` or `--claims` file that is missing;
- `--html` names a missing file, or `--panel` is not a folder;
- a landmine cue targets facts and the facts file is missing; a facts row says ABSENT and names a `COV-n` id and the
  coverage file is missing;
- a rank cue hits a line whose rank record names a table that `numbers.json` does not hold;
- a killed-lines row whose pattern does not compile.

Not run, and the exit code does not move:

- a default project file that is missing: `numbers.json`, `decisions.md`;
- no `--claims` and no `claims.csv` in the project;
- `parity` without `--html`; `release-hash` without `--reviewed-sha256`;
- a deleted `setup-timelines` or `plain-language` landmine (a note says it was skipped);
- a `decisions.md` with no killed-lines rows (the check passes with a note).

Findings in the project `claims.csv` still count when it is found by default. With `--require-all`, every check that
is not `pass` or `fail` makes the exit 3.

## Output

One line per finding, then a blank line, a table of the checks and `exit N`.

```
CHECK | severity | file:line | quote | rule-id
time-promises | major | drafts/v1.md:15 | There is nothing to set up, and texting starts right away. | setup-timelines/F1
```

A `|` inside a quote is printed as `/`. The quote is the sentence of the hit, shortened when it is long.

The table has one row for each of the 13 checks, in this order: `pieces`, `landmines`, `voice`, `numbers`, `parity`,
`stray-labels`, `repeats`, `time-promises`, `plain`, `claims`, `mark-budget`, `killed-lines`, `release-hash`. Each row
shows `pass`, `fail`, `not_run` or `uncertain`, the finding count and a note.

With `--json` the output is one object: `piece`, `exit`, `checks` (for each check: `result`, `findings`, `note`,
`required`, `incomplete`) and `findings` (each: `check`, `severity`, `file`, `line`, `quote`, `rule`).

## The checks

| check | what fails it | rule ids |
|---|---|---|
| `pieces` | `pieces.json` has an error (the check is then `uncertain`). A missing or blank file is a pass: the file is one untyped piece | none |
| `landmines` | a cue from `rules/landmines/*.md` (all but `setup-timelines` and `plain-language`) matches and no rescue applies; the facts-target cues; research-absence F2 and F4 on the facts and coverage files; process-claims F3 and F4 | `<landmine>/F1` ... |
| `voice` | a banned cue from either voice file matches, beyond its counted exception | `voice/VB3`, `voice/VN1` ..., `voice/allowed-over-count:<regex>` |
| `numbers` | a number with no record (F1); a value that a record lists under `conflicts` (F4); a record that is not `exact` printed without its hedge (F3) | `numbers-and-sources/F1`, `/F3`, `/F4` (without that landmine: `numbers/no-record`, `numbers/precision`, `numbers/two-values`) |
| `parity` | a sentence of 4 or more words in the piece and not on the page, or the reverse | `parity/piece-only`, `parity/page-only` |
| `stray-labels` | a word printed twice in a row ("offer offer"; `had` and `that` are allowed); a label string in the rendered page text, unless its whole sentence is also in the markdown | `stray/doubled-word`, `stray/label:<string>` |
| `repeats` | a run of 8 words that appears twice in the piece; URLs and link targets are blanked first | `repeats/8-words` |
| `time-promises` | a cue from `rules/landmines/setup-timelines.md` | `setup-timelines/F1` ... |
| `plain` | the shapes of `plain-language` F1 to F7 (see "How plain reads a piece") | `plain-language/F1` ... `/F7` |
| `claims` | a ledger row with status UNMARKED, blank or unknown; TO-CONFIRM with no owner (major), an owner written "proposed: ..." (minor) or no date (minor) | `claims/UNMARKED`, `claims/unknown-status`, `claims/TO-CONFIRM-no-owner`, `claims/TO-CONFIRM-owner-proposed`, `claims/TO-CONFIRM-no-date` |
| `mark-budget` | more than the limit of marks in one `##` section. On a page every dotted span counts. In markdown a bracket of three words or fewer is a merge field and is not counted | `marks/over-limit` |
| `killed-lines` | a pattern from the killed-lines table of the decision log matches the markdown or the page, and its row names no reversing decision | `killed/<id>` |
| `release-hash` | the sha256 of the piece file differs from `--reviewed-sha256` | `release/hash-mismatch` |

Severity. `release-hash` is critical. `stray-labels` and `killed-lines` are major. `repeats`, `mark-budget`, `parity`
and every `voice` finding are minor. `claims` rows are major or minor as listed above. A landmine cue takes the
`Severity:` written in its shape bullet, else the `severity` of the landmine's front matter, else major (critical for
`compliance-promises`). `plain` takes the same `Severity:` and otherwise F1, F2, F5, F6 and F7 are major and F3 and F4
are minor. One finding is reported for each rule on each line (landmines) or in each sentence (voice).

## How a piece is read

A page is read as rendered text. `script`, `style`, `head`, `title`, `svg`, `noscript`, `template` and `<sup>` are
dropped. Attributes such as `title=` are never text. Block tags end a line. A dotted span (an element whose class list
holds the dotted class) is wrapped in square brackets for cues and the mark count, and is plain text for parity and
stray labels. Line numbers on a page are the line of the HTML source where the text starts.

Markdown is read as it is, one line at a time. A `[square bracket]` is a mark. Link text `[x](url)` is not.
A blank line resets an open bracket. A cue with the `bracket` rescue does not fire when its whole match lies inside
one mark.

Pieces. A project lists its piece types in `pieces.json`. A `##` heading (`<h2>` on a page) tags everything after it,
up to the next `##` heading, with a piece id. The tag is found by trying, in this order:

1. an exact match: the whole heading equals a piece id, ignoring case;
2. each piece's `heading` regex, in file order; the first that finds a match wins.

A heading that matches no piece takes the `--piece-type` id, or no piece if there is none. `--piece-type` tags the
whole of a markdown file before and after its headings in this way. It does not tag a page: a page is tagged only by
its `<h2>` headings.

What a piece id changes:

- the landmines: a landmine with `applies_to` set to a list of ids runs only in those pieces. `applies_to: all` or no
  `applies_to` means every piece. A line that belongs to no piece is always in scope;
- the voice: a banned row written "in email, social" runs only in those pieces (see the voice file format);
- `plain`: the settings of the piece (`plain`, `grade_max`, `grade_scope`, `hook`);
- the topic cues compare what different pieces say about one topic.

A project with no pieces (a missing or blank `pieces.json`) has one untyped piece: it gets the plain check and no
grade limit. A project that lists pieces is stricter: a line that belongs to no piece is not read by `plain` at all.
Tag it with a matching `##` heading or `--piece-type`.

## How plain reads a piece

`plain` runs the shapes of `rules/landmines/plain-language.md` on markdown. The units are lines: paragraph lines, list
items (`- `, `1. `), table rows, bold-only lines and `###` headings, and the `**From:**`, `**To:**`, `**Subject:**`
and `**Preview:**` fields. Subject is read as a heading. From and To are skipped. A bold label at the start of an
item or paragraph is its own sentence. A line that starts with `>` is read without the `>`.

- A `**Side notes...**` line opens a side-notes block. `---` or the next `##` heading closes it. Side notes are not
  graded, and F7 skips them. F5 reads the bold labels inside them.
- A greeting is a line that starts with `Hi`, `Hello` or `Dear` and ends with a comma.
- Quoted text (`"..."`) counts as one word. Link targets, URLs, file-name link texts, code spans, tags and hashtags
  are dropped.

The shapes:

| shape | what it counts |
|---|---|
| F1 | a sentence of more than 20 words |
| F2 | a list item or table row with a semicolon, with two or more dash asides, or with more than three sentences after its label and more than 30 words. The semicolon and dash tests are the F2 cues of the landmine file |
| F3 | a 3-word phrase 3 times in one paragraph or item group; a changed preposition counts as the same phrase |
| F4 | a term with no plain words in its sentence or the one before: an abbreviation-shaped word (two capitals, a letter and a digit mixed, a digit and a letter mixed) or a word from the landmine's `jargon` block, unless the word is in its `plain-ok` block or is a project term. A project term with a plain-words pattern in a heading or a Subject field, with no match of that pattern on the line. "Explained" means the term sits inside parentheses next to its plain words, or is followed by `(`, `:`, `, a`, `, an`, `, the`, `is`, `are`, `means` or `stands for` |
| F5 | the bold label of a side-note item matches an F5 cue |
| F7 | a sentence outside the side notes matches an F7 cue |
| F6 | the Flesch-Kincaid grade of a section is above the `grade_max` of its piece |

Which units are read depends on the piece:

- A piece with `plain: false` skips F1 to F5 and F7. It is still graded for F6 when it has a `grade_max`.
- `hook: "after-greeting"` marks the first paragraph after the greeting (or after the header fields) as the hook. The
  hook is skipped by every shape and by the grade. Any piece may use it.
- The grade covers the graded units of one `##` section. With `grade_scope: "body"` (the default) the graded text is
  every line outside side notes and outside the hook. When the piece has a hook, the graded text must also follow a
  greeting or header field. With `grade_scope: "numbered-steps"` only list items are graded.
- A grade counts words that hold a letter (numbers are not words) and syllables by vowel groups, with a silent final
  `e` dropped. The note prints `grade <piece> <grade>` per section, with `(max N)` when the piece has a limit.
  A section with no graded words prints nothing.
- With `--html`, the `title` attribute of each dotted span of the page is also read for F4 and F5, and reported at
  the line of the span.

## Numbers skipped as non-claims

The `numbers` check ignores: years (19xx, 20xx, written bare); times of day and agenda minutes (`10:30`, `9 AM`);
phone numbers; dates (`2026-10-02`, `2.10.2026`, `May 4`, `4th May`); list and heading numbers (`1.`, `## 3`);
"section 4", "step 2", "round 3", "page 5", "version 2" and the other words of that kind; ids such as `F8`, `D3`,
`v2`; product versions ("Acme 2.0"); anything inside quotation marks (a quote has its own record); a price inside
a bracket; hashtags; URLs and link targets; code spans; HTML tags. A number that is part of a word (`A2`, `10DLC`),
or follows a dash, a slash, `#` or `,`, is not read as a separate number.

How a number is matched. `1,927` and `1927` are the same value. A `k` or `M` suffix multiplies (`5k` is 5000; a `k`
number also matches a record of 5). A `%` needs a record with unit `%` or `percent`, or a share record (see below)
whose `phrase` is in the same line and whose result is within 0.5 of the printed value. A share record with no
`precision` counts as `approximate`.

## File formats the scripts read

### Cues: a fenced `cues` block in each landmine file

One cue per line, five columns split on the first four `|` (the pattern may contain `|`). A line that starts with
`# ` is a comment.

```cues
# rule | target | rescues | kind  | pattern
F1     | copy   | bracket | regex | (?i)\bright away\b|\bfrom day one\b
F2     | copy   | none    | topic | recording=(?i)\bcall recording\b
F2     | copy   | none    | rank  | (?i)\btop[- ](?:three|five|ten)\b
F1     | copy   | bracket | number| \b\d{1,3}(?:,\d{3})+\b|\b\d+\b
F3     | copy   | bracket | number| (?i)\b(?:about|around|roughly)\b
F1     | facts  | none    | regex | ^(?!.*\bCOV-\d+\b).*\|\s*ABSENT\s*\|
```

- `target`: `copy` runs on the piece and the page. `facts` runs on the data rows of every table with a `claim` column in
  the facts file, with the `refute` column blanked. A facts file with no such table is read whole.
- `rescues`: `none`, or a comma list of `bracket` (the match lies wholly inside one mark), `proposal` (the line says
  "my proposal"), `question` (the line holds a `?`).
- `kind`: `regex` (a match is a hit); `topic` (`name=pattern`: matching lines are grouped by piece and the clause
  around the match is compared; it fires when two or more pieces carry two or more different clauses); `rank` (a
  hit unless `numbers.json` holds a rank record whose `phrase` is in the line and whose result recomputes from its
  table); `number` (read by the `numbers` check, not by the cue scan).
- A `number` cue is read by rule id. The cue with id `F1` gives the rule id and severity of "number with no record";
  its pattern is not used. Any other `number` cue gives the rule id and severity of "printed without its hedge", and
  its pattern is the hedge. With no such cue the hedge is `about`, `around`, `roughly`, `nearly`, `almost`, `close, not
  exact`, `counted twice`, `double-counted`, `stopped` or `~` before a digit. The hedge may stand in the line or in an
  earlier line of the same `##` section.
- Patterns are Python `re` with `MULTILINE`, case-sensitive unless they start with `(?i)`. A pattern that does not
  compile, holds a control character or matches the empty string is refused.
- Short forms, also accepted: `F1: <pattern>` or a bare pattern per line (target `copy`, rescue `bracket`).
- When a landmine file has no cue line at all, cues are taken from `Cues: ` followed by backticked patterns in an
  F-bullet. Those match without regard to case.
- Severity comes from `Severity: <level>` in the shape's bullet (`- **F1 Name.** ... Severity: major.`).
- Front matter keys read: `id` (default: the file name), `version`, `strictness` (`remove`, `cite-or-cut` or
  `rewrite`), `severity`, `applies_to`.
- Extra stray-label strings: a fenced `labels` block, one literal per line, in any landmine file, in either voice file
  or in the `labels` list of `pieces.json`.
- `plain-language` also reads a fenced `plain-ok` block (words that need no explanation, split on spaces, matched
  with case) and a fenced `jargon` block (one regex per line, matched without regard to case). Both blocks are also
  read from either voice file, so a project adds its own accepted abbreviations and its own jargon in `project/voice.md`
  (the lists of the landmine and of the project are merged).

### pieces.json

```json
{
  "pieces": [
    {"id": "email", "heading": "(?i)\\bemail\\b", "voice": "house", "plain": true, "grade_max": 9, "hook": "after-greeting"},
    {"id": "how-made", "heading": "(?i)how (?:this|it) was made", "voice": "author", "plain": false,
     "grade_max": 11, "grade_scope": "numbered-steps"}
  ],
  "labels": [],
  "max_marks": 7,
  "dotted_class": "tbc"
}
```

| key | meaning |
|---|---|
| `id` | required, unique, a non-blank string |
| `heading` | a regex searched in the text of each `##` heading; optional (a piece may be reached by exact id or `--piece-type`) |
| `voice` | `house` (default) or `author`. In an `author` piece no exception from `allowed` blocks applies, so every banned cue stays; a project row opts out of such a piece only through its own "in <pieces>" scope |
| `plain` | `true` (default) or `false` |
| `grade_max` | the F6 limit; no key means no grade check |
| `grade_scope` | `body` (default) or `numbered-steps` |
| `hook` | `after-greeting` marks the first paragraph after a greeting as the hook; any other value does nothing |
| `labels` | stray label strings for the page search |
| `max_marks`, `dotted_class` | defaults of `--max-marks` and `--dotted-class` |

A backslash in a regex is written `\\` in JSON. `\b` written once is a control character, and the file is refused.

### Fixtures in landmine files

In a landmine file, a fenced `fixtures` block, one JSON object per line. The fields are listed below, with the
fields of the `tools/fixtures/*.jsonl` files.

| field | meaning |
|---|---|
| `id`, `rule`, `expect` | the fixture id; the rule id without the landmine prefix (`F1`, `VB3`, `K-01`; an empty string means any rule of that landmine or check); `fire` or `no_fire` |
| `target` | `copy` (default) or `facts` |
| `text` | one piece, as markdown. For `claims` it is a CSV |
| `texts` | a list of `{piece, text}`; each is placed under a `## <piece>` heading |
| `html` | page source. With `text`, cues run on both; `parity` needs both; the dotted-span tooltips are read for `plain` |
| `piece` | tags a one-piece fixture. Must be an id of `tools/fixtures/pieces.json` |
| `numbers` | a list of `numbers.json` records the fixture runs with. Without it the fixture has no records |
| `coverage`, `stats` | a coverage table (research-absence F2); the counts that a facts fixture must produce (`rows`, `absent`, `overturned`, `f2_not_run`) |
| `panel_reports`, `piece_sha256`, `reviewed_sha256` | the number of round reports; the two hashes (process-claims F3 and F4) |
| `killed` | a list of `{id, pattern, reversed_by}` for `killed-lines` |
| `decisions` | a decisions.md excerpt with a killed-lines table, for `killed-lines` |
| `voice` | voice-file markdown, merged with the generic voice file for the fixture |
| `voice_rows` | a list of `{id, cue, scope}` (scope: a list of piece ids), or bare regexes; each is one banned cue |
| `terms` | a list of `terms` lines (`term | count | plain words`) for `plain` |
| `labels` | extra stray-label strings |
| `limit` | the mark limit for a `mark-budget` fixture (default: `max_marks` of `fixtures/pieces.json`, else 7) |
| `source` | free text: where the shape comes from |

In `tools/fixtures/*.jsonl` each line also carries `landmine` (a landmine id or a check name: `voice`, `numbers`,
`parity`, `stray-labels`, `repeats`, `claims`, `mark-budget`, `killed-lines`; `plain` is read as `plain-language`
and `time-promises` as `setup-timelines`), `why`, `file` and `version`. These six keys are required: `id`, `landmine`,
`rule`, `why`, `file`, `version`, and one of `text`, `texts` or `html`. `line` is allowed and is not read. The file
decides the expectation. In a landmine file `landmine` defaults to the file's own id.

In `rules/examples/*.md`: front matter `landmine`, `rule`, `verdict` and an optional `piece`; the passage is the first
`>` block under `## Passage`. `remove` and `rewrite` must fire their rule. `keep` must fire no shape of its landmine.
`README.md` and `TEMPLATE.md` in that folder are skipped.

### numbers.json

A list of records, or an object that holds lists of records. A record has a `value` (a number, or a string such as
`"$1,927"`, `"~40"`, `"12%"`, `"5k"`) and may have `id`, `unit`, `precision` and `conflicts`. `precision` is `exact`
by default. Any other word (`approximate`, for example) means the value needs a hedge when printed. `conflicts` lists
other values that other files give for the same quantity. When several records share a value, the one whose `unit`
(lowercased, without a trailing `s`) appears in the 40 characters after the number is used, else the first. Computed
rows:

```json
{"id": "T-reviews", "kind": "table", "rows": {"Support": 120, "Billing": 95, "Mobile app": 80, "Scheduling": 40}}
{"id": "R-mobile", "kind": "rank", "phrase": "third-largest complaint", "table": "T-reviews", "row": "Mobile app", "result": 3}
{"id": "S-two", "kind": "share", "phrase": "64% of all complaints", "table": "T-reviews", "rows": ["Support", "Billing"],
 "result": 64, "precision": "approximate"}
```

A rank is the row's place by value, largest first. A share is the rows' sum over the table's sum, in percent, within
0.5. `rows` of a table may also be a list of `{row, value}` objects. Table rows are inputs for ranks and shares, not
records of printed counts. A file with no `value` key, no table and no rank or share record is read as a bare list of
numbers: every number in it counts, except under keys ending in `line`, `version`, `year`, `page` or `id`.

### facts.md and coverage.md

`check_absence` reads every table of the facts file with a `label` column and a column whose header holds `claim`.
For each ABSENT row it takes the `COV-n` ids in the row (outside the `refute` column) and looks them up in every
table of `coverage.md` whose first column holds `COV-n`. A row is uncovered when its `keyword-searched` column
(any header holding `search`) is blank, `0`, `no`, `none` or `-`, and its `read` count is not at or above its
`total` count. An ABSENT row with an empty `refute` cell is research-absence F4. The check also counts rows whose
`refute` cell ends on `overturned`: a cell keeps its history, so only the last verdict word in it (`held`,
`overturned` or `unverifiable`) counts. The note prints the counts.

### decisions.md: killed lines

A table with a column whose header contains `pattern`. The first cell of a row is its id. The pattern is a Python
regex, written between backticks; `\|` (a table's escaped pipe) is read as `|`. It is matched with case unless it
starts with `(?i)`. A row whose `reversed` column holds a `D-n` id is skipped. Each pattern is reported once for each
line it matches.

### claims.csv

Columns are found by part of the header: `status`, `owner`, `due` or `date`, and `claim` (or `text`, `quote`,
`sentence`). Lines that start with `#` are dropped before parsing. Statuses: `SOURCED`, `PROPOSAL`, `TO-CONFIRM`,
`UNMARKED`. A status is read in capitals with spaces and underscores turned into hyphens. A finding's line is the
row's place among the data rows, counted with the header as line 1.

### The voice files

`rules/voice.md` (the generic file) and `<project>/voice.md` are read by one parser and merged.

Banned cues come from every table with a column whose header contains "cue", and from every fenced `banned` block
in either file. In a table, the first cell of a row is its id. In the cue cell:

- a phrase in backticks is a literal, matched as a whole word or phrase, ignoring case;
- `regex` before a backticked phrase makes it a regular expression;
- a cell that says "case-sensitive" is matched with case;
- text after the last backtick that ends "in email, social" limits the row to those piece ids (ids that the project
  lists; with no pieces the row has no limit);
- several cues in one cell are separated by a middle dot, a comma, a semicolon, a pipe or "or". A backticked phrase
  that is part of a sentence in the cell is not read as a cue.

A pipe in a regex inside a table cell is written `\|`; the parser reads `\|` as a pipe anywhere in the row (GitHub splits a table cell on a bare pipe even inside backticks). A `banned` block holds one regex per line, optionally written
`VB3: <regex>`; it is read without regard to case. Lines that start with `# ` are comments. Every voice finding is
minor.

Exceptions come from a fenced `allowed` block:

```allowed
# regex | max per piece | piece ids or all
\bworkflow\b | 3 | email, social
```

The middle column is a whole number (`max 3` is also read), or `-` for no limit. The third is a comma list of piece ids
or `all`. The older forms `N | regex`, `regex | max N` and `regex (max N)` are also read, and mean every piece. A
banned hit is excused when an `allowed` regex matches in the same sentence, overlapping the hit, in a piece the row
lists, and the piece is not an `author` piece. Uses are counted for each row and each piece. A use over the count is
a finding, `voice/allowed-over-count:<regex>`. An id that `pieces.json` does not list is an error.

A fenced `terms` block holds the project's own terms, one line each: `term | count or source | plain words regex`
(`-` for a name that needs no plain words). The term is matched with case, as a whole word or phrase. A project with
no `terms` block has no terms, and that is not an error. A fenced `labels` block holds stray-label strings.
Fenced `plain-ok` and `jargon` blocks in a voice file extend the lists of the `plain-language` landmine.

## What selftest refuses

It loads `tools/fixtures/pieces.json`, `rules/landmines/*.md`, `rules/voice.md`, `rules/manifest.json`,
`rules/examples/*.md` and `tools/fixtures/*.jsonl`. It reads nothing under `project/` or `examples/`. It prints a
`PROBLEM` line for each of these, runs the fixtures anyway, and exits 1:

- a missing `fixtures/pieces.json`, or an error in it; a missing manifest, voice file or landmine folder;
- a landmine with no cues, or with any load error; a front-matter `version` that differs from `rules/manifest.json`;
  a manifest entry with no landmine file;
- a voice file with no banned cues, or with an error;
- a fixture file that is missing, a line that is not JSON, a missing required key; an `expect` that is not `fire` or
  `no_fire`; an example with no passage or a bad `verdict`;
- a fixture that uses `needs` (the field is not accepted: carry the records inline in `numbers`; the fixture is not
  run); a fixture whose `piece` or `texts[].piece` is not in `tools/fixtures/pieces.json`; a duplicate fixture id;
- a landmine with zero fire fixtures; a forbidden shape (`- **F1 ...`) with no `Severity:` or with no passing fire
  fixture under its rule id.

A fixture that fails, or could not run (an unknown landmine or check, a landmine with no cues, a voice fixture that
does not load, a `killed-lines` fixture with no `killed` or `decisions`, a `parity` fixture without both `text` and
`html`), also gives exit 1.

Two twin runs show that a lookup is read. A `no_fire` fixture of F1 or F3 of `numbers-and-sources` with inline
`numbers` is run again without them and must fire F1. A process-claims F4 `fire` fixture is run again with equal
hashes and must not fire. `selftest.py` writes no `__pycache__`.

## Known limits

- String checks catch words and numbers, not meaning. A false sentence with no number and no cue passes. Stage 2 and
  the review round carry the rest; they are agent steps (`rules/README.md`, Detection).
- The order-of-work and duration checks (process-claims F1, F6) need `git log` dates. The script does not read git.
  They are stage-2 steps.
- Stage 1 over-selects. Voice VB1 selects every list of three that does not open with a channel noun. The `numbers`
  check flags every bare number with no record, including planned values and step counts that are not in a skipped
  form. Bracketed promises are selected by design where a cue says brackets do not rescue them.
- Label strings hit real sentence ends. The check skips a hit whose whole sentence is also in the markdown, but only
  when the piece is markdown.
- `--piece-type` does not tag a page. A page piece is tagged by its `<h2>` headings only.
- With pieces defined, a line outside every piece is not read by `plain`. The run still passes, with `grade none` in
  the note.
- A cue with `\s` in it can match across a line break.
- On a page given as the piece, `plain` reads rendered lines where inline tags glue words. Run it on the markdown;
  `parity` holds the page to it.
- `claims` checks the ledger rows, not whether every claim in the piece has a row.
- F4 for numbers catches only the conflicting values a record lists. An unlisted second value is F1.
- Cue hits on the page repeat the hits on the markdown when both carry the same text.
- The project `claims.csv` is picked up only by its default name. The decision log and the numbers file need a
  `--project` or a flag to be found elsewhere.
