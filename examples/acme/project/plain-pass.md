# Plain pass: the prompt (`process/LINE.md` step 4.5)

Give this prompt to an agent after the draft and before the lint. This copy is filled for Acme Dispatch.
`tools/check.py` check `plain` reads the result, not this file. `pieces.json` says which pieces are
checked (`plain`) and their grade limit (`grade_max`): email 9, partner-note 9, how-made 11 (numbered steps only).

You get the piece, `rules/landmines/plain-language.md`, the company's terms in `project/voice.md`
section 7 (Acme Dispatch, Job Thread, LedgerLite, MapRoute) and the `plain` lines of `tools/check.py`.
Rewrite only the language. One idea per sentence, the company's words, no new facts, hook untouched (the first
paragraph after "Hi [First name]," in the email), quoted speech untouched.

1. F1: a sentence over 20 words becomes two or three sentences.
2. F2: a list item with a semicolon, two dash asides, or more than three long sentences is split or cut down.
3. F3: a 3-word phrase said three times in one item or paragraph is said once.
4. F4: a term that is not the company's and not plain English gets plain words in the same sentence. A
   heading with a company term also says it in plain words ("Job Thread: texts and calls on the job card").
5. F5: a side-note title is a full sentence or a plain noun phrase: no "=", no "X, not Y", no "line".
6. F6: each piece reads at or below its `grade_max` from `pieces.json`.
7. F7: "until now", "as before", "because", "so that" leave the feature sentence for a side note.

Keep every fact, number, name and bracketed mark. A history remark moves to a side note. It does
not vanish. Do not restructure, add or cut. Change the page the same way (parity). Write the list as
`was -> now`, one line per changed sentence, in `plain-pass.md` in the run folder (`process/runs/<run>/`).
Done when check `plain` is 0.

Example line:

`Texting, which is included on Pro and Crew, lets you reply from the job card; calls stay in the same thread. -> Texting is on the Pro and Crew plans. You reply from the job card. Calls stay in the same thread.`
