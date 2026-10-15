#!/usr/bin/env python3
"""Validate Mu2e xCards offline, the way the xCard Registry does, plus Mu2e conventions.

    python3 scripts/validate.py                      # every card under cards/
    python3 scripts/validate.py cards/agents/x.md    # named cards
    python3 scripts/validate.py --strict ...         # Mu2e-convention warnings fail too

Needs PyYAML and jsonschema. Exit 0 = all valid, 1 = a card failed, 2 = usage or environment error.

Checks, in order:
  1. front matter: a leading `---` line, a closing `---` line, a non-empty YAML mapping (registry parser rules);
  2. schema: Draft 2020-12 validation against schema/xcard.schema.json, the registry's copy of the Genesis spine
     schema (provenance in schema/README.md), without format checking, as the registry does;
  3. registrability: card_type is one of agent, model, data/dataset, infrastructure (workflow cards are valid but go
     through storage, not the registry);
  4. Mu2e conventions (warnings; errors with --strict): id prefix and file name, directory per card type, keywords
     not all digits, last_updated an ISO date, no stale counts or sizes, sensitivity explicit, description long enough to be searchable, no template leftovers, no
     secrets or non-public paths.
Data cards with Genesis data card v2 content are additionally LinkML-validated by the registry; that stage is not
reproduced here, so register data cards against a local stack before publishing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    sys.exit(f"validate.py needs PyYAML and jsonschema ({exc.name} missing); use a python that has both")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "xcard.schema.json"
REGISTRABLE = {"agent": "agent_card", "model": "model_card", "data": "data_card", "dataset": "data_card",
               "infrastructure": "resource_card"}
DIR_FOR_TYPE = {"agent": "agents", "model": "models", "data": "datasets", "dataset": "datasets",
                "infrastructure": "infrastructure", "workflow": "workflows"}
TEMPLATE_LEFTOVERS = ("CHANGE ME", "My Example", "Your Organization", "Replace this", "example.org",
                      "0000-0000-0000-0000")
SECRET_PATTERNS = {
    "mikey key": re.compile(r"mikey_[0-9a-f]{16,}"),
    "bearer/JWT token": re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
    "API key": re.compile(r"\b(sk|ghp|gho|xox[bp])[-_][A-Za-z0-9]{16,}"),
    "non-public path": re.compile(r"/(exp|pnfs|nashome|cvmfs/mu2e\.opensciencegrid\.org/[^ ]*/users)/[A-Za-z0-9_./-]*"),
}
MIN_DESCRIPTION = 80  # below this the engine falls back to indexing the body
# Style: cards carry no counts, sizes or performance figures that go stale (README, "Conventions").
STALE_NUMBER = re.compile(r"(?<![\w./-])\d{1,3}(?:,\d{3})+(?![\w.])|(?<![\w./-])\d{3,}(?![\w./-])|\b\d+(?:\.\d+)?\s?(?:%|percent|GiB|GB|TB|MiB|kB|node-hours|CPU-hours|GPU-hours|cores|nodes)\b")
STALE_SKIP = re.compile(r"Mu2e-doc-\d+|docdb-\d+|20\d\d-\d\d-\d\d|https?://\S+|\b(?:19|20)\d\d\b|for example[^.;]*")


def parse_front_matter(text: str) -> tuple[dict | None, str | None]:
    lines = text.removeprefix("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "card must begin with a '---' YAML front matter line"
    close = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if close is None:
        return None, "YAML front matter is not terminated by a '---' line"
    try:
        fm = yaml.safe_load("\n".join(lines[1:close]))
    except yaml.YAMLError as exc:
        return None, f"YAML front matter is malformed: {exc}"
    if not isinstance(fm, dict) or not fm:
        return None, "YAML front matter must be a non-empty mapping"
    return fm, None


def jsonable(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def path_str(path) -> str:
    out = ""
    for p in path:
        out += f"[{p}]" if isinstance(p, int) else (f".{p}" if out else str(p))
    return out or "(top level)"


def conventions(card: Path, fm: dict, text: str) -> list[str]:
    warn = []
    ctype = str((fm.get("xCard") or {}).get("card_type", ""))
    cid = str(fm.get("id", ""))
    if not cid.startswith("mu2e-"):
        warn.append(f"id '{cid}' should start with 'mu2e-'")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", cid):
        warn.append(f"id '{cid}' should be lowercase letters, digits, '-' or '_'")
    if card.stem != cid:
        warn.append(f"file name '{card.name}' should be '{cid}.md'")
    want = DIR_FOR_TYPE.get(ctype)
    if want and card.parent.name != want:
        warn.append(f"a {ctype} card belongs in cards/{want}/")
    for i, kw in enumerate(fm.get("keywords") or []):
        if str(kw).strip().isdigit():
            warn.append(f"keywords[{i}] '{kw}' is all digits; the registry rejects it")
    try:
        dt.date.fromisoformat(str(fm.get("last_updated", "")))
    except ValueError:
        warn.append(f"last_updated '{fm.get('last_updated', '')}' is not an ISO date (YYYY-MM-DD)")
    if "sensitivity" not in fm:
        warn.append("sensitivity not set; the engine treats a missing value as visible to everyone")
    elif fm["sensitivity"] == "unreviewed":
        warn.append("sensitivity 'unreviewed' is shown to everyone; use general, reviewed or restricted")
    if len(str(fm.get("description", "")).strip()) < MIN_DESCRIPTION:
        warn.append(f"description under {MIN_DESCRIPTION} characters; search reads name, description, keywords "
                    "and skills, not the body")
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"\s*(last_updated|version):", line):
            continue
        hits = [m.group(0).strip() for m in STALE_NUMBER.finditer(STALE_SKIP.sub(" ", line))]
        if hits:
            warn.append(f"line {i}: {', '.join(repr(h) for h in hits)} look like counts or sizes that go stale")
    for s in TEMPLATE_LEFTOVERS:
        if s in text:
            warn.append(f"template text left in the card: '{s}'")
    return warn


def secrets(text: str) -> list[str]:
    return [f"{name} found: '{m.group(0)[:40]}'" for name, rx in SECRET_PATTERNS.items() for m in rx.finditer(text)]


def check(card: Path, validator: Draft202012Validator, strict: bool) -> bool:
    text = card.read_text(encoding="utf-8")
    fm, err = parse_front_matter(text)
    errors, warnings = [], []
    if err:
        errors.append(err)
    else:
        for e in sorted(validator.iter_errors(jsonable(fm)), key=lambda e: list(e.path)):
            errors.append(f"{path_str(e.path)}: {e.message}")
        ctype = str((fm.get("xCard") or {}).get("card_type", ""))
        if ctype and ctype not in REGISTRABLE and ctype != "workflow":
            errors.append(f"card_type '{ctype}' has no registry endpoint")
        warnings = conventions(card, fm, text)
    errors += secrets(text)  # public repository: always an error
    if strict:
        errors, warnings = errors + warnings, []
    status = "FAIL" if errors else ("ok (warnings)" if warnings else "ok")
    print(f"{status:14s} {card.relative_to(ROOT) if card.is_relative_to(ROOT) else card}")
    for m in errors:
        print(f"    error:   {m}")
    for m in warnings:
        print(f"    warning: {m}")
    return not errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cards", nargs="*", type=Path, help="card files (default: every cards/**/*.md)")
    ap.add_argument("--strict", action="store_true", help="treat Mu2e-convention warnings as errors")
    args = ap.parse_args(argv)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)  # no FormatChecker: the registry builds its validator the same way
    cards = [c.resolve() for c in args.cards] or sorted((ROOT / "cards").rglob("*.md"))
    missing = [c for c in cards if not c.is_file()]
    if missing:
        print("no such file: " + ", ".join(map(str, missing)), file=sys.stderr)
        return 2
    if not cards:
        print("no cards to validate")
        return 0
    results = [check(c, validator, args.strict) for c in cards]
    print(f"{sum(results)}/{len(results)} card(s) valid")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
