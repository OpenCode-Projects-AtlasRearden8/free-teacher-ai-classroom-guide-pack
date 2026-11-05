"""Tests: every sheet in build.py renders a valid, non-empty PDF.

Run with:  python3 -m pytest tests/ -v
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

import pytest


def test_sheet_registry_matches_disk():
    on_disk = {p.name for p in (ROOT / "sheets").glob("*.html")}
    registered = set(build.SHEETS)
    assert on_disk == registered, f"registry/disk mismatch: {on_disk ^ registered}"


def _readable_text(data: bytes) -> bytes:
    """Concatenate every FlateDecode content stream in the PDF (WeasyPrint 70
    packs page and object streams, so plain /Type /Page greps can miss them)."""
    parts = []
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end != -1:
            try:
                parts.append(zlib.decompress(data[start:end]))
            except zlib.error:
                parts.append(data[start:end])
    return b"\n".join(parts)


def _readable_text(data: bytes) -> bytes:
    """Concatenate every stream in the PDF, decompressing where possible."""
    parts = []
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end != -1:
            try:
                parts.append(zlib.decompress(data[start:end]))
            except zlib.error:
                parts.append(data[start:end])
    return b"\n".join(parts)


def _document_text(document) -> str:
    """Collect text from WeasyPrint's rendered page boxes (no extra deps)."""
    chunks = []
    for page in document.pages:
        for box in page._page_box.descendants():
            if type(box).__name__ == "TextBox" and box.text:
                chunks.append(box.text)
    return " ".join(chunks)


@pytest.mark.parametrize("html_name", sorted(build.SHEETS))
def test_sheet_renders_valid_pdf(html_name, tmp_path):
    """Every registered sheet must render a valid PDF with real pages and text."""
    from weasyprint import HTML

    out = tmp_path / "out"
    out.mkdir()
    html_path = ROOT / "sheets" / html_name
    pdf_path = out / (pathlib.Path(html_name).stem + ".pdf")
    assert html_path.is_file(), f"missing sheet file: {html_path}"

    # Render twice: the document object gives authoritative page/text checks.
    document = HTML(filename=str(html_path)).render()
    assert len(document.pages) >= 1, f"{html_name}: rendered zero pages"
    rendered_text = _document_text(document)
    assert build.SHEETS[html_name] in rendered_text, f"{html_name}: title not rendered"
    document.write_pdf(str(pdf_path))

    data = pdf_path.read_bytes()

    # Header and EOF markers present; non-trivially sized.
    assert data.startswith(b"%PDF-"), f"{html_name}: no PDF header"
    assert b"%%EOF" in data[-2048:], f"{html_name}: no EOF marker"
    assert len(data) > 4_000, f"{html_name}: suspiciously small PDF ({len(data)} bytes)"
    assert b"stream" in _readable_text(data), f"{html_name}: no content streams"


def test_main_builds_all_pdfs(tmp_path):
    """The public build_all() entry point runs cleanly end-to-end."""
    results = build.build_all("weasyprint")
    assert len(results) == len(build.SHEETS)
    for html_name, pdf_name, engine in results:
        assert engine == "weasyprint"
        pdf = build.OUT_DIR / pdf_name
        assert pdf.is_file() and pdf.stat().st_size > 4_000
        assert pdf.read_bytes().startswith(b"%PDF-")
        assert html_name in build.SHEETS


def test_build_cli(tmp_path):
    """`python3 build.py` exits 0 and writes every PDF."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py")],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    for html_name in build.SHEETS:
        pdf = build.OUT_DIR / (pathlib.Path(html_name).stem + ".pdf")
        assert pdf.is_file(), f"{pdf_name} not built"
        assert b"%%EOF" in pdf.read_bytes()[-2048:]


def test_cli_list_flag():
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--list"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0
    assert "01-syllabus-statements.html" in result.stdout
