# STATUS.md — free-teacher-ai-classroom-guide-pack

**Date finished:** 2026-11-05
**Owner:** Asdale Dynamics, LLC

## What was built

A print-and-go paperwork pack for classroom teachers new to AI. Six unbranded,
print-ready HTML sheets (shared `sheets/print.css`, US Letter, black-and-white safe,
real fillable checkboxes and write-on lines) plus one local build script:

1. **00-how-to-use.html** — cover page: what's inside, editing/printing notes,
   district-policy reminder.
2. **01-syllabus-statements.html** — four syllabus statement templates (short,
   standard with the AI-Free / AI-Assisted / AI-Included levels, expanded for upper
   grades, one-liner for families) + optional student sign-off slip.
3. **02-assignment-guidelines.html** — three "level cards" to paste into any
   assignment, a student AI-use citation format with sample disclosures, a printable
   disclosure form, and grading reminders.
4. **03-parent-letter.html** — a short newsletter note, a full start-of-term letter
   with opt-out and accessibility-support language, and a likely-questions table.
5. **04-student-reflection.html** — double-sided student reflection sheet (checkbox
   timeline of actual AI use + four open "honest thinking" questions + teacher
   read-the-skim callout).
6. **05-access-equity-checklist.html** — choose-your-own checklist across five
   categories (devices/internet, language, accessibility, time/cost, privacy), each
   item paired with a concrete fallback, plus a termly three-minute self-audit.

Supporting files: `build.py` (single local build script), `requirements.txt`
(WeasyPrint), `tests/test_build.py` (10 tests), `README.md`, `LICENSE` (MIT,
Copyright (c) 2026 Asdale Dynamics, LLC), `.gitignore`.

## How to run it

```shell
pip install -r requirements.txt      # or: python3 build.py --engine chrome
python3 build.py                     # builds all 6 PDFs into pdf/
python3 build.py --list              # print the sheet registry
python3 -m pytest tests/ -v          # verification
```

Default engine is WeasyPrint (local pip install, fully offline); headless
Chrome/Chromium is a built-in fallback (`--engine chrome`). No accounts, no
signups, no API keys, no network access during builds.

## Verification results

- `python3 -m pytest tests/ -q` → **10 passed**:
  - sheet registry exactly matches files on disk,
  - every registered sheet renders a structurally valid PDF (correct `%PDF` header,
    `%%EOF`, size > 4 KB) with at least one page and its title text confirmed present
    in WeasyPrint's rendered page boxes,
  - public `build_all()` runs end to end and all six PDFs land in `pdf/`,
  - the CLI `python3 build.py` exits 0 with valid output, and `--list` works.
- `python3 build.py` → built all six PDFs successfully with WeasyPrint.
- Manual text scan of rendered output confirmed no typos or editing residue
  remained and no product/brand names appear in any sheet (unbranded requirement).

## Known gaps

- No branded cover or company logo by design (unbranded sheets); the LLC credit
  exists only in README/LICENSE.
- Grade-band variations are prose suggestions inside templates rather than separate
  per-grade files.
- The Chrome fallback engine is untested in CI-style automation (no renderer
  equivalence test); the default WeasyPrint path is what the tests verify.
- Sheet text assumes US Letter; A4 supports (a second `@media`/`@page` rule) not
  yet added.
- No PDF previews committed to the repo — `pdf/` is gitignored and regenerated
  locally with one command.
