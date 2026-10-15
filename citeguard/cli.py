"""CiteGuard CLI entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from citeguard import __version__
from citeguard.check import check_report
from citeguard.models import VERDICTS

DEFAULT_FAIL_ON = ",".join(v for v in VERDICTS if v != "clean")


def _pkg_fixtures() -> Path:
    return Path(__file__).resolve().parent.parent / "fixtures"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="citeguard",
        description="Check citations in Markdown research reports. Heuristics do not prove factual support.",
    )
    p.add_argument("--version", action="version", version=f"citeguard {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    check = sub.add_parser("check", help="Check citations in a Markdown file")
    check.add_argument("report", help="Path to the Markdown report")
    check.add_argument(
        "--fixtures", nargs="?", const="__default__", default=None,
        help="Offline fixture catalog directory (default: ./fixtures)",
    )
    check.add_argument("--no-overlap", action="store_true", help="Disable claim token overlap")
    check.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    check.add_argument(
        "--fail-on", default=DEFAULT_FAIL_ON,
        help="Comma-separated verdicts causing exit 1; default: all except clean",
    )
    check.add_argument("--timeout", type=float, default=12.0, help="HTTP timeout in seconds")
    check.add_argument(
        "--max-html-bytes", type=int, default=2 * 1024 * 1024,
        help="Maximum downloaded HTML bytes per URL (default: 2097152)",
    )
    check.add_argument(
        "--allow-private", action="store_true",
        help="DANGEROUS: allow localhost/private IP destinations for trusted local reports",
    )
    return p


def _print_human(result) -> None:
    print(f"CiteGuard — {result.path}")
    print(f"Summary: {result.summary}")
    print("-" * 60)
    for c in result.citations:
        flag = {
            "clean": "OK", "dead": "DEAD", "http_error": "ERR",
            "title_mismatch": "TITLE", "claim_weak": "WEAK",
            "redirect_suspect": "REDIR", "unresolved": "?",
            "unverifiable": "UNKNOWN", "unchecked": "UNCHECKED",
            "blocked": "BLOCKED",
        }.get(c.verdict, c.verdict.upper())
        title_bit = f' title="{c.page_title}"' if c.page_title else ""
        score_bit = ""
        if c.title_score is not None:
            score_bit += f" title_score={c.title_score}"
        if c.overlap_score is not None:
            score_bit += f" overlap={c.overlap_score}"
        print(f"[{flag}] L{c.line} {c.url}")
        if c.link_text:
            print(f"       link_text: {c.link_text}")
        if c.claim:
            print(f"       claim: {c.claim[:120]}")
        print(f"       status={c.status} final={c.final_url}{title_bit}{score_bit}")
        if c.reasons:
            print(f"       reasons: {'; '.join(c.reasons)}")
        print()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd != "check":
        parser.print_help()
        return 2

    if not (args.timeout > 0) or args.max_html_bytes <= 0:
        print("error: timeout and max-html-bytes must be positive", file=sys.stderr)
        return 2
    requested = {x.strip() for x in args.fail_on.split(",") if x.strip()}
    if unknown := requested.difference(VERDICTS):
        print(f"error: unknown --fail-on verdict(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    fixtures_root = None
    if args.fixtures is not None:
        if args.fixtures == "__default__":
            cand = Path("fixtures")
            fixtures_root = cand if cand.exists() else _pkg_fixtures()
        else:
            fixtures_root = Path(args.fixtures)
        if not (Path(fixtures_root) / "catalog.json").is_file():
            print(f"error: fixtures catalog missing: {fixtures_root}/catalog.json", file=sys.stderr)
            return 2

    try:
        result = check_report(
            args.report,
            fixtures_root=fixtures_root,
            check_overlap=not args.no_overlap,
            timeout=args.timeout,
            allow_private=args.allow_private,
            max_html_bytes=args.max_html_bytes,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: unable to check report: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        _print_human(result)

    if not result.citations:
        print("warning: no citations found; nothing was verified", file=sys.stderr)
        return 1
    return int(any(c.verdict in requested for c in result.citations))


if __name__ == "__main__":
    raise SystemExit(main())
