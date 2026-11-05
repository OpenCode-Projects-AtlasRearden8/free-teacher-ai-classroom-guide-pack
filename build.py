#!/usr/bin/env python3
"""Build print-ready PDFs from the sheets/ directory using a single local command.

Usage:
    python3 build.py              build every sheet into pdf/
    python3 build.py --list       show the sheet list without building
    python3 build.py --engine chrome    force Chrome headless instead of WeasyPrint

No accounts, no signups, no network access. WeasyPrint (pip install weasyprint)
is the default engine; if it is missing, Chrome/Chromium headless is used as a
local fallback. Everything stays on your machine.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
OUT_DIR = ROOT / "pdf"

SHEETS: dict[str, str] = {
    "00-how-to-use.html": "How to Use This Pack",
    "01-syllabus-statements.html": "Syllabus Statement Templates",
    "02-assignment-guidelines.html": "Assignment Guidelines to Copy",
    "03-parent-letter.html": "Parent Letter Drafts",
    "04-student-reflection.html": "Student Reflection Sheet",
    "05-access-equity-checklist.html": "Access Equity Checklist — Choose Your Own",
}


def build_weasyprint(html: pathlib.Path, out: pathlib.Path) -> None:
    from weasyprint import HTML  # imported lazily so --engine chrome needs no install

    HTML(filename=str(html)).write_pdf(str(out))


def find_chrome() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def build_chrome(html: pathlib.Path, out: pathlib.Path, chrome: str) -> None:
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out}",
        html.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=120)
    if result.returncode != 0 and not out.exists():
        stderr = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"chrome exited {result.returncode}: {stderr}")


def build_all(engine: str = "auto") -> list[tuple[str, str, str]]:
    """Render every sheet to PDF. Returns (html, pdf, engine_used) tuples."""
    from weasyprint import __version__ as weasy_version  # noqa: F401  (import check)

    OUT_DIR.mkdir(exist_ok=True)
    htmls = list(SHEETS)
    results: list[tuple[str, str, str]] = []

    use_weasy = engine != "chrome"
    use_chrome = engine != "weasyprint"
    chrome_path = find_chrome() if use_chrome else None

    for name in htmls:
        html = SHEETS_DIR / name
        if not html.is_file():
            raise FileNotFoundError(f"missing sheet: {html}")
        out = OUT_DIR / (pathlib.Path(name).stem + ".pdf")

        used = "weasyprint"
        if use_weasy:
            try:
                build_weasyprint(html, out)
            except Exception:
                if not use_chrome or chrome_path is None:
                    raise
                used = "chrome"
                build_chrome(html, out, chrome_path)
        else:
            if chrome_path is None:
                raise RuntimeError("no chrome/chromium found; pip install weasyprint")
            used = "chrome"
            build_chrome(html, out, chrome_path)

        results.append((name, out.name, used))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="print the sheet list and exit")
    parser.add_argument("--engine", choices=("auto", "weasyprint", "chrome"), default="auto")
    args = parser.parse_args()

    if args.list:
        for name, title in SHEETS.items():
            print(f"{name}  ->  {SHEETS_DIR / name}")
        return 0

    try:
        results = build_all(args.engine)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Built {len(results)} PDF(s) into {OUT_DIR}/")
    for name, pdf, used in results:
        print(f"  {name} -> {pdf} [{used}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
