# Rules changelog

Newest first. Each entry: date, rule set and version, what changed, why, who asked.

## 2026-10-02 · version 1.0

- Extracted from a company-specific repository and generalized. All rule versions reset to 1: `voice` and the nine landmines (`product-claims`, `compliance-promises`, `pricing-plans`, `setup-timelines`, `competitors-partners`, `numbers-and-sources`, `research-absence`, `process-claims`, `plain-language`); checks `repeats`, `stray-labels` and `plain`. Generic shapes for money copy were added in the same release: `compliance-promises` F4, `pricing-plans` F3 and money cues in `competitors-partners` F5.
- Project layer added: `project/` holds voice, piece types (`pieces.json`), facts, coverage, numbers, claims, decisions and personas. `rules/voice.md` keeps only the generic AI-tell list; the company's own exceptions and never-does rows moved to `project/voice.md`. `--project` sets the defaults of the file flags.
- Piece types are data in `project/pieces.json`, not code.
- Fixtures made synthetic: every text is an Acme Dispatch sentence with the same shape as the one it replaces. The self-test reads only `rules/` and `tools/fixtures/`.
- Why: the rules proved useful on one launch kit and are not specific to its company.
- Asked by: the editor.
