"""CiteGuard CLI entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from citeguard import __version__
from citeguard.check import check_report


def _pkg_fixtures() -> Path:
    # Default fixtures live next to the project when running from source
    here = Path(__file__).resolve().parent.parent / "fixtures"
    return here


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="citeguard",
        description="Verify citations in agent/deep-research Markdown reports (local, no API keys).",
    )
    p.add_argument("--version", action="version", version=f"citeguard {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check", help="Check citations in a Markdown file")
    check.add_argument("report", help="Path to Markdown report")
    check.add_argument(
        "--fixtures",
        nargs="?",
        const="__default__",
        default=None,
        help="Offline mode: use fixtures catalog (optional path; default: ./fixtures)",
    )
    check.add_argument(
        "--no-overlap",
        action="store_true",
        help="Skip claim–source token overlap check",
    )
    check.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )
    check.add_argument(
        "--fail-on",
        default="dead,http_error,title_mismatch,claim_weak,redirect_suspect",
        help="Comma-separated verdicts that make exit code 1 (default: all bad)",
    )
    check.add_argument("--timeout", type=float, default=12.0, help="HTTP timeout seconds")
    return p


def _print_human(result) -> None:
    print(f"CiteGuard — {result.path}")
    print(f"Summary: {result.summary}")
    print("-" * 60)
    for c in result.citations:
        flag = {
            "clean": "OK",
            "dead": "DEAD",
            "http_error": "ERR",
            "title_mismatch": "TITLE",
            "claim_weak": "WEAK",
            "redirect_suspect": "REDIR",
            "unresolved": "?",
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

    if args.cmd == "check":
        fixtures_root = None
        if args.fixtures is not None:
            if args.fixtures == "__default__":
                cand = Path("fixtures")
                fixtures_root = cand if cand.exists() else _pkg_fixtures()
            else:
                fixtures_root = Path(args.fixtures)
            if not (Path(fixtures_root) / "catalog.json").exists():
                print(
                    f"error: fixtures catalog not found at {fixtures_root}/catalog.json",
                    file=sys.stderr,
                )
                return 2

        result = check_report(
            args.report,
            fixtures_root=fixtures_root,
            check_overlap=not args.no_overlap,
            timeout=args.timeout,
        )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            _print_human(result)

        fail_on = {x.strip() for x in args.fail_on.split(",") if x.strip()}
        bad = [c for c in result.citations if c.verdict in fail_on]
        return 1 if bad else 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
