# Free Teacher AI Classroom — Guide Pack

A print-and-go paperwork pack for classroom teachers who are new to AI. Every sheet is
plain HTML/CSS, sized for US Letter, unbranded, and renders to PDF with one local command.
No accounts, no signups, no API keys, no network access at build time.

**Distinction from related packs:** this repo builds *paperwork* (syllabus text, letters,
forms, checklists). See `ai-workshop-lesson-plans-guide` for full lesson plans, and
`student-papers-ai-ethics-guide` for student-facing ethics material.

## Contents

| Sheet | PDF | What it is |
|---|---|---|
| [How to Use This Pack](sheets/00-how-to-use.html) | [PDF](pdf/00-how-to-use.pdf) | One-page cover: what's inside, printing notes, district-policy reminder |
| [Syllabus Statement Templates](sheets/01-syllabus-statements.html) | [PDF](pdf/01-syllabus-statements.pdf) | Four ready-to-edit syllabus statements (short / standard / expanded / one-liner) plus an optional student sign-off slip |
| [Assignment Guidelines to Copy](sheets/02-assignment-guidelines.html) | [PDF](pdf/02-assignment-guidelines.pdf) | Three "level cards" (AI-Free / AI-Assisted / AI-Included), a student AI-use citation format, a printable disclosure form, and grading reminders |
| [Parent Letter Drafts](sheets/03-parent-letter.html) | [PDF](pdf/03-parent-letter.pdf) | A short newsletter note, a full start-of-term letter with an opt-out line, and a table of likely family questions |
| [Student Reflection Sheet](sheets/04-student-reflection.html) | [PDF](pdf/04-student-reflection.pdf) | Double-sided printable: checkbox timeline of a student's actual AI use plus open "honest thinking" questions |
| [Access Equity Checklist — Choose Your Own](sheets/05-access-equity-checklist.html) | [PDF](pdf/05-access-equity-checklist.pdf) | Menu of class-level equity commitments (devices, language, accessibility, time, privacy) each with a concrete fallback |

## How it works

Everything lives in `sheets/`. The HTML uses a shared stylesheet
(`sheets/print.css`) so every page:

- sizes to US Letter (8.5 × 11 in) with safe margins,
- prints cleanly in black and white,
- draws real fillable checkboxes and write-on lines (`<span class="checkbox">`,
  `<span class="write-line">`) for pencil-and-paper use,
- keeps footer text ("Free to print and adapt for your classroom" + page numbers)
  in the print margin via CSS page boxes.

## Run the build

Requires Python 3 and One of:

```shell
pip install -r requirements.txt   # installs WeasyPrint (preferred engine)
python3 build.py                  # writes every PDF into pdf/
```

Or, with Chrome/Chromium already installed and no `pip` at all:

```shell
python3 build.py --engine chrome  # headless Chrome renders the same sheets
```

Helpful flags:

```shell
python3 build.py --list           # print the sheet registry without building
```

## Run the tests

```shell
python3 -m pytest tests/ -v
```

The tests verify that **every registered sheet renders a valid PDF**: correct header and
EOF markers, non-trivial size, at least one page, and — via WeasyPrint's rendered page
boxes — the sheet's title text actually present in the output. They also run the public
`build_all()` entry point and the command-line interface end to end.

## Design principles

- **Education only.** Nothing here is advice about AI for any non-classroom purpose, and
  no sheet gives medical, legal, or financial guidance. Classroom practice should defer
  to your school or district policy — the pack says so inside, too.
- **Unbranded.** No product names, no vendor links, no attribution inside the sheets.
  Teachers share or adapt them freely; the only credit lives in this README.
- **Local-first.** The build works fully offline; installing WeasyPrint is a local pip
  install. No telemetry, no accounts, no secrets anywhere in the repo.
- **Plain English.** Written the way a friend would explain it — step by step, never
  condescending.

## Credits

Created by **Asdale Dynamics, LLC** as part of Dylan Asdale's beginner-friendly AI
guides — including *The Massive AI Manual* and the hub at dylanasdale.github.io, which
explain AI tools, agents, and local AI "like a friend would."

Licensed MIT — see [LICENSE](LICENSE). © 2026 Asdale Dynamics, LLC.
