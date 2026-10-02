#!/usr/bin/env python3
"""Self-test of the rules and of tools/check.py. Standard library only, Python 3.11.
Usage: python tools/selftest.py [--verbose]. What it loads and refuses: tools/README.md.
It reads only rules/ and tools/fixtures/. Nothing under project/ or examples/ is read."""
from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check as C  # noqa: E402

ROOT = C.ROOT
FIXTURES = ROOT / "tools" / "fixtures"
CHECK_ALIASES = {"time-promises": C.TIME_LANDMINE, "plain": C.PLAIN_LANDMINE}
RULE_PREFIX = {"stray-labels": "stray", "mark-budget": "marks", "repeats": "repeats", "parity": "parity",
               "claims": "claims", "numbers": "numbers", "voice": "voice", "killed-lines": "killed"}


@dataclass
class Ctx:
    landmines: dict[str, C.Landmine]
    voice: C.Voice | None
    pieces: C.Pieces
    labels: list[str]
    problems: list[str] = field(default_factory=list)
    plain: C.PlainRules | None = None


def front_matter_and_passage(md: Path) -> tuple[dict, str | None]:
    text = md.read_text(encoding="utf-8")
    fm = C.front_matter(text)
    m = re.search(r"^## Passage[^\n]*\n\s*((?:>.*\n?)+)", text, re.M)
    passage = " ".join(ln.lstrip(">").strip() for ln in m.group(1).splitlines()).strip() if m else None
    return fm, passage


def load_examples(ctx: Ctx) -> list[dict]:
    out = []
    d = ROOT / "rules" / "examples"
    if not d.is_dir():
        return out
    for md in sorted(d.glob("*.md")):
        if md.name.upper() in ("README.MD", "TEMPLATE.MD"):
            continue
        fm, passage = front_matter_and_passage(md)
        verdict = fm.get("verdict", "")
        if not passage:
            ctx.problems.append(f"example {md.name}: no '> ' passage under '## Passage'")
            continue
        if verdict not in ("remove", "rewrite", "keep"):
            ctx.problems.append(f"example {md.name}: verdict must be remove | rewrite | keep, got {verdict!r}")
            continue
        out.append({"id": f"example:{md.name}", "landmine": fm.get("landmine", ""),
                    "rule": "" if verdict == "keep" else fm.get("rule", ""),
                    "text": passage, "piece": fm.get("piece") or None,
                    "expect": "no_fire" if verdict == "keep" else "fire", "_from": f"rules/examples/{md.name}"})
    return out


def load_jsonl(path: Path, expect: str, ctx: Ctx) -> list[dict]:
    out = []
    if not path.is_file():
        ctx.problems.append(f"{path.relative_to(ROOT)} missing")
        return out
    for k, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            fx = json.loads(line)
        except json.JSONDecodeError as e:
            ctx.problems.append(f"{path.name} line {k}: not JSON ({e})")
            continue
        missing = [key for key in ("id", "landmine", "rule", "why", "file", "version") if key not in fx]
        if not any(key in fx for key in ("text", "texts", "html")):
            missing.append("text|texts|html")
        if missing:
            ctx.problems.append(f"{path.name} line {k} ({fx.get('id')}): missing {missing}")
            continue
        fx["expect"] = expect
        fx["_from"] = f"tools/fixtures/{path.name} line {k}"
        out.append(fx)
    return out


def fixture_problems(fx: dict, ctx: Ctx) -> list[str]:
    """Things a fixture may not do: use the retired "needs" field, or name a piece the synthetic config lacks."""
    out = []
    if "needs" in fx:
        out.append(f"{fx.get('id')} ({fx['_from']}): 'needs' is not accepted; carry the records inline in 'numbers'")
    ids = ctx.pieces.ids
    named = [fx.get("piece")] + [t.get("piece") for t in fx.get("texts") or []]
    for p in named:
        if p and ids and p not in ids:
            out.append(f"{fx.get('id')} ({fx['_from']}): piece {p!r} is not in tools/fixtures/pieces.json")
    return out


def fixture_numbers(fx: dict) -> C.Numbers:
    """The records a fixture carries inline in "numbers" (none: no records)."""
    return C.numbers_from(fx["numbers"] if isinstance(fx.get("numbers"), list) else [])


def fixture_voice(fx: dict, ctx: Ctx) -> tuple[C.Voice | None, str | None]:
    """The generic voice file, plus the voice the fixture carries inline: "voice" (voice-file markdown) and
    "voice_rows" (a list of {id, cue, scope} or bare cue regexes). Returns (voice, reason it could not load)."""
    if not ctx.voice:
        return None, "rules/voice.md missing"
    extra: list[C.Voice] = []
    if fx.get("voice"):
        extra.append(C.parse_voice(fx["voice"], "<fixture voice>", ctx.pieces.ids))
    errors: list[str] = []
    banned: list[C.Cue] = []
    for k, row in enumerate(fx.get("voice_rows") or [], start=1):
        row = {"cue": row} if isinstance(row, str) else row
        rid = row.get("id") or f"row{k}"
        rx = C.compile_rx(row["cue"], f"voice/{rid}", errors, re.IGNORECASE | re.MULTILINE)
        if rx:
            banned.append(C.Cue(f"voice/{rid}", rx, "minor", frozenset(), scope=list(row.get("scope") or []),
                                source=row["cue"]))
    if banned or errors:
        extra.append(C.Voice("<fixture voice_rows>", banned, [], [], errors))
    voice = C.merge_voice([ctx.voice] + extra) if extra else ctx.voice
    fx_errors = [e for v in extra for e in v.errors]
    return voice, (f"fixture voice does not load: {fx_errors}" if fx_errors else None)


def fixture_killed(fx: dict) -> tuple[list, str | None]:
    """"killed": [{id, pattern}] and/or "decisions": a decisions.md excerpt with a killed-lines table."""
    out, errors = [], []
    for k in fx.get("killed") or []:
        rx = C.compile_rx(k.get("pattern", ""), f"killed/{k.get('id')}", errors)
        if rx:
            out.append((str(k.get("id")), rx, str(k.get("reversed_by", ""))))
    if fx.get("decisions"):
        more, kerr = C.load_killed(fx["decisions"])
        out += more
        errors += kerr
    return out, (f"fixture killed lines do not load: {errors}" if errors else None)


def fixture_plain(fx: dict, ctx: Ctx) -> C.PlainRules | None:
    """The plain-language rules; "terms" gives the fixture its company terms (voice-file `terms` lines)."""
    if not ctx.plain:
        return None
    if not fx.get("terms"):
        return ctx.plain
    terms, errors = C.parse_terms("```terms\n" + "\n".join(fx["terms"]) + "\n```\n")
    return dataclasses.replace(ctx.plain, terms=terms, errors=ctx.plain.errors + errors)


def build_docs(fx: dict, ctx: Ctx):
    target = fx.get("target", "copy")
    dotted = ctx.pieces.dotted_class or C.DEFAULT_DOTTED
    if fx.get("texts"):
        text = "\n".join(f"## {t.get('piece', '')}\n{t['text']}" for t in fx["texts"])
        doc = C.md_doc(text, "<fixture>", None, ctx.pieces)
    elif target == "facts":
        doc = C.facts_doc(fx.get("text", ""), "<fixture>", ctx.pieces)
    else:
        doc = C.md_doc(fx.get("text", ""), "<fixture>", fx.get("piece"), ctx.pieces)
    plain = cues = None
    if fx.get("html"):
        plain = C.html_doc(fx["html"], "<fixture.html>", dotted, False, ctx.pieces)
        cues = C.html_doc(fx["html"], "<fixture.html>", dotted, True, ctx.pieces)
    return doc, plain, cues


def findings_for(fx: dict, ctx: Ctx, numbers: C.Numbers) -> tuple[list[C.Finding], str | None]:
    """Returns (findings, reason it could not run)."""
    name = CHECK_ALIASES.get(fx["landmine"], fx["landmine"])
    doc, plain, cue_page = build_docs(fx, ctx)
    target = fx.get("target", "copy")
    dotted = ctx.pieces.dotted_class or C.DEFAULT_DOTTED
    if name in ctx.landmines:
        lm = ctx.landmines[name]
        if not lm.cues:
            return [], f"landmine {name} has no cues"
        if name == C.PLAIN_LANDMINE:
            rules = fixture_plain(fx, ctx)
            if not rules or rules.errors:
                return [], f"plain rules not loaded: {rules.errors if rules else 'none'}"
            fs = C.check_plain(doc, rules, ctx.pieces)[0]
            if fx.get("html"):                     # tooltips of the page's dotted spans
                fs += C.check_plain_titles(fx["html"], "<fixture.html>", rules, dotted)[0]
            return fs, None
        fs: list[C.Finding] = []
        docs = [doc] + ([cue_page] if cue_page else []) if fx.get("text") or fx.get("texts") else [cue_page]
        for d in docs:
            if d is None:
                continue
            fs += C.check_cues(d, [lm], "fixture", numbers, target)[0]
            if name == C.NUMBERS_LANDMINE and target == "copy":
                fs += C.check_numbers(d, numbers, lm)
        if name == C.ABSENCE_LANDMINE and target == "facts":
            cov = C.coverage_rows(fx["coverage"]) if fx.get("coverage") else None
            fs += C.check_absence(fx.get("text", ""), "<fixture>", cov, lm)[0]
        if name == C.PROCESS_LANDMINE:
            fs = C.process_record(fs, lm, fx.get("panel_reports"), fx.get("piece_sha256"),
                                  fx.get("reviewed_sha256"))
        return fs, None
    if name in C.CHECKS or name == "numbers":
        if name == "voice":
            voice, why = fixture_voice(fx, ctx)
            return ([], why) if why or not voice else (C.check_voice(doc, voice, ctx.pieces), None)
        if name == "numbers":
            return C.check_numbers(doc, numbers, None), None
        if name == "stray-labels":
            labels = ctx.labels + [x for x in fx.get("labels") or [] if x not in ctx.labels]
            return C.check_stray(plain or doc, labels, doc if plain and fx.get("text") else None), None
        if name == "repeats":
            return C.check_repeats(doc), None
        if name == "parity":
            return (C.check_parity(doc, plain), None) if plain else ([], "parity fixture needs text and html")
        if name == "mark-budget":
            return C.check_marks(doc, int(fx.get("limit", ctx.pieces.max_marks or C.MAX_MARKS))), None
        if name == "claims":
            return C.check_claims(C.read_claims(fx.get("text", "")), "<fixture>"), None
        if name == "killed-lines":
            killed, why = fixture_killed(fx)
            if why or not killed:
                return [], why or "killed-lines fixture carries no 'killed' list or 'decisions' table"
            return C.check_killed(doc, killed), None
    return [], f"unknown landmine or check {fx['landmine']!r}"


def rule_matches(f: C.Finding, fx: dict) -> bool:
    name = CHECK_ALIASES.get(fx["landmine"], fx["landmine"])
    rule = (fx.get("rule") or "").strip()
    if name in ctx_landmine_ids:
        return f.rule == f"{name}/{rule}" if rule else f.rule.startswith(name + "/")
    prefix = RULE_PREFIX.get(name, name)
    if not f.rule.startswith(prefix + "/") and f.check != name:
        return False
    if not rule:
        return True
    tail = f.rule.split("/", 1)[-1]
    return tail == rule or tail.startswith(rule + ":") or f.rule == rule


ctx_landmine_ids: set[str] = set()


def evaluate(fx: dict, ctx: Ctx) -> tuple[str, str]:
    """Returns (status, detail): status ok | FAIL | NOT_RUN."""
    numbers = fixture_numbers(fx)
    fs, why = findings_for(fx, ctx, numbers)
    if why:
        return "NOT_RUN", why
    # a facts fixture may also pin the counts check_absence prints ("N overturned")
    if isinstance(fx.get("stats"), dict):
        st = C.check_absence(fx.get("text", ""), "<fixture>", None, None)[1]
        bad = {k: (v, st.get(k)) for k, v in fx["stats"].items() if st.get(k) != v}
        if bad:
            return "FAIL", "stats " + ", ".join(f"{k}: expected {e}, got {g}" for k, (e, g) in bad.items())
    hits = [f for f in fs if rule_matches(f, fx)]
    if fx["expect"] == "fire" and not hits:
        other = sorted({f.rule for f in fs})
        return "FAIL", "did not fire" + (f" (fired instead: {', '.join(other)})" if other else "")
    if fx["expect"] == "no_fire" and hits:
        return "FAIL", f"fired: {hits[0].rule} on {hits[0].quote[:90]!r}"
    # twin: without its inline records a numbers no_fire fixture must fire F1
    name = CHECK_ALIASES.get(fx["landmine"], fx["landmine"])
    if fx["expect"] == "no_fire" and fx.get("numbers") and name == C.NUMBERS_LANDMINE \
            and fx.get("rule") in ("F1", "F3"):
        bare, _ = findings_for(fx, ctx, C.numbers_from([]))
        if not any(f.rule == f"{name}/F1" for f in bare):
            return "FAIL", "with its inline numbers removed it still does not fire F1: the check is not reading them"
    # twin: with equal hashes a process-claims F4 fire fixture must go silent
    if fx["expect"] == "fire" and name == C.PROCESS_LANDMINE and fx.get("rule") == "F4":
        same = dict(fx, reviewed_sha256=fx.get("piece_sha256"))
        again, _ = findings_for(same, ctx, numbers)
        if any(f.rule == f"{name}/F4" for f in again):
            return "FAIL", "with equal hashes it still fires F4: the check is not comparing hashes"
    return "ok", ""


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    problems: list[str] = []
    pieces_path = FIXTURES / "pieces.json"
    if not pieces_path.is_file():
        problems.append("tools/fixtures/pieces.json missing (the synthetic piece types the fixtures use)")
    pieces = C.load_pieces(pieces_path)
    problems += pieces.errors
    lms = C.load_landmines(ROOT / "rules" / "landmines", pieces.ids)
    voice_path = ROOT / "rules" / "voice.md"
    voice = C.load_voice([voice_path], pieces.ids) if voice_path.is_file() else None
    labels = list(pieces.labels)
    for lm in lms:
        labels += [x for x in lm.labels if x not in labels]
    if voice:
        labels += [x for x in voice.labels if x not in labels]
    ctx = Ctx({lm.id: lm for lm in lms}, voice, pieces, labels, problems)
    if C.PLAIN_LANDMINE in ctx.landmines:
        ctx.plain = C.plain_rules(ctx.landmines[C.PLAIN_LANDMINE], [])
        problems += [e for e in ctx.plain.errors if e not in ctx.landmines[C.PLAIN_LANDMINE].errors]
    ctx_landmine_ids.update(ctx.landmines)

    if not lms:
        problems.append("no landmine files in rules/landmines")
    manifest = {}
    mp = ROOT / "rules" / "manifest.json"
    if mp.is_file():
        manifest = json.loads(mp.read_text(encoding="utf-8")).get("landmines", {})
    else:
        problems.append("rules/manifest.json missing")
    for lm in lms:
        problems += [f"{lm.id}: {e}" for e in lm.errors]
        if not lm.cues:
            problems.append(f"{lm.id}: no cues (the landmine would be not_run)")
        fm = C.front_matter(Path(lm.path).read_text(encoding="utf-8"))
        if manifest and str(manifest.get(lm.id)) != fm.get("version"):
            problems.append(f"{lm.id}: version {fm.get('version')!r} in front matter, {manifest.get(lm.id)!r} in manifest")
    for lid in manifest:
        if lid not in ctx.landmines:
            problems.append(f"manifest lists {lid}, no rules/landmines/{lid}.md")
    if voice is None:
        problems.append("rules/voice.md missing")
    else:
        problems += voice.errors
        if not voice.banned:
            problems.append("rules/voice.md: no machine-readable banned cues")

    fixtures = load_jsonl(FIXTURES / "must_fire.jsonl", "fire", ctx)
    fixtures += load_jsonl(FIXTURES / "must_not_fire.jsonl", "no_fire", ctx)
    for lm in lms:
        for fx in lm.fixtures:
            if fx.get("expect") not in ("fire", "no_fire"):
                problems.append(f"{fx.get('id')} ({fx['_from']}): expect must be fire | no_fire")
                continue
            fixtures.append(fx)
    fixtures += load_examples(ctx)
    seen: dict[str, str] = {}
    for fx in fixtures:
        problems += fixture_problems(fx, ctx)
        if fx["id"] in seen and seen[fx["id"]] != fx["_from"]:
            problems.append(f"duplicate fixture id {fx['id']} ({seen[fx['id']]} and {fx['_from']})")
        seen[fx["id"]] = fx["_from"]

    counts: dict[str, list[int]] = {}
    fired_shapes: set[tuple[str, str]] = set()
    failures: list[str] = []
    not_run: list[str] = []
    for fx in fixtures:
        if "needs" in fx:                          # refused above; do not run on missing records
            status, detail = "NOT_RUN", "uses 'needs'"
        else:
            status, detail = evaluate(fx, ctx)
        name = CHECK_ALIASES.get(fx["landmine"], fx["landmine"])
        c = counts.setdefault(name, [0, 0, 0])
        c[0 if fx["expect"] == "fire" else 1] += 1
        if fx["expect"] == "fire" and status == "ok":
            fired_shapes.add((name, (fx.get("rule") or "").strip()))
        line = f"{status:<8} {fx['expect']:<8} {fx['id']}  [{fx['_from']}]  {detail}"
        if status == "FAIL":
            failures.append(line)
            c[2] += 1
        elif status == "NOT_RUN":
            not_run.append(line)
            c[2] += 1
        elif args.verbose:
            print(line)

    for lid, lm in ctx.landmines.items():
        if counts.get(lid, [0])[0] == 0:
            problems.append(f"{lid}: zero fire fixtures; a rule that has never fired has not been tested")
        for sid in C.shape_ids(lm):
            if sid not in lm.severities:
                problems.append(f"{lid}/{sid}: no 'Severity: critical|major|minor' in the shape bullet")
            if (lid, sid) not in fired_shapes:
                problems.append(f"{lid}/{sid}: no passing fire fixture for this shape")

    for p in problems:
        print(f"PROBLEM  {p}")
    for line in failures + not_run:
        print(line)
    print()
    print(f"{'landmine or check':<22} {'fire':>5} {'no_fire':>8} {'bad':>4}")
    for name in sorted(counts):
        f, n, bad = counts[name]
        print(f"{name:<22} {f:>5} {n:>8} {bad:>4}")
    total = len(fixtures)
    print(f"\n{total} fixtures, {len(failures)} failed, {len(not_run)} not run, {len(problems)} problems")
    ok = not (failures or not_run or problems)
    print("selftest: pass" if ok else "selftest: fail")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
