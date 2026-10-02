# rules/examples
Three passages from the fictional project Acme Dispatch, one per verdict: `remove`, `keep`, `rewrite`.
Each file shows how a landmine decides a real-looking sentence. They are also fixtures: `tools/selftest.py` runs the first `>` block of every file here.

Format of a file:
- Front matter: `landmine`, `rule`, `verdict` (`keep`, `remove` or `rewrite`), `slop_class`, `severity`, `piece`, `source`, `verdict_by`, `verdict_ref`, `date`.
- `## Passage`: the passage is the first `>` block under this heading. Later blocks are ignored.
- `## Why` and `## What replaced it`: required when the verdict is `remove` or `rewrite`. A `keep` file has `## Why` and `## What it shows`.

What the self-test checks:
- `remove` and `rewrite`: the rule named in `rule` must fire on the passage under the cues of `landmine`.
- `keep`: the landmine must stay silent on the passage.
- Any other verdict, or a file with no passage, is a self-test problem.

To add an example, copy one file, change the passage and the front matter, and run `python tools/selftest.py`.
The passage must be synthetic. Never paste text from a real project.
