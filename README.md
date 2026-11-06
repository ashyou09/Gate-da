# GATE DA 2027 — Notes website

Topic-wise notes for **GATE Data Science & Artificial Intelligence 2027**, ordered by what the 2024–2026 papers actually asked.
Every topic page has a topic map, teaching from basics, a summary, solved PYQs and predicted 2027 questions.

Built with [Astro Starlight](https://starlight.astro.build): static HTML pages with search, dark mode and KaTeX math.

## Subjects

Same folder name (slug) everywhere: website notes in `src/content/docs/<slug>/`, study material in `subjects/<slug>/`.

| # | Subject | Slug | Marks 24 / 25 / 26 | Notes status |
|---|---|---|---|---|
| 1 | Programming, DS & Algorithms | [`pdsa`](subjects/pdsa) | 17 / 16 / 16 | **complete: 9 of 9 topics** |
| 2 | Machine Learning | [`machine-learning`](subjects/machine-learning) | 11 / 14 / 16 | **complete: 12 of 12 topics, with diagrams** |
| 3 | DBMS & Warehousing | [`dbms`](subjects/dbms) | 8 / 9 / 18 | **complete: 7 of 7 topics, with diagrams** |
| 4 | Artificial Intelligence | [`ai`](subjects/ai) | 11 / 3 / 8 | **complete: 7 of 7 topics, with diagrams** |
| 5 | Probability & Statistics | [`probability-statistics`](subjects/probability-statistics) | 16 / 18 / 13 | topic plan ready |
| 6 | Linear Algebra | [`linear-algebra`](subjects/linear-algebra) | 10 / 17 / 8 | topic plan ready |
| 7 | Calculus & Optimization | [`calculus-optimization`](subjects/calculus-optimization) | 8 / 8 / 7 | topic plan ready |
| 8 | General Aptitude | [`general-aptitude`](subjects/general-aptitude) | 15 / 15 / 15 | complete: 8 of 8 topics, with diagrams |

## Repository layout

```
Gate-da/
├── src/content/docs/          ← the website notes (Markdown + LaTeX)
│   ├── index.md, roadmap.md, references.md
│   └── <slug>/                ← one folder per subject
│       ├── index.md           ← subject hub: syllabus, PYQ map, topic plan
│       └── <topic>.md         ← one page per topic
├── subjects/                  ← study material, one folder per subject
│   └── <slug>/
│       ├── README.md          ← auto-generated: files + notes list + syllabus
│       ├── revision-sheet.pdf
│       ├── question-bank.pdf
│       └── books/ or notes/   ← extra material (where present)
├── pyq/
│   ├── papers/                ← GATE DA 2024–2026 question papers
│   ├── keys/                  ← official answer keys
│   └── analysis/              ← 2027 prediction report + 2 predicted mock papers
├── scripts/
│   ├── subjects.json          ← marks, syllabus, topic plan per subject
│   └── sync_subjects.py       ← creates hub pages + regenerates subjects/*/README.md
├── src/styles/custom.css      ← formula / trap / mind-map boxes
├── astro.config.mjs           ← site config; sidebar auto-builds one group per subject
├── NOTES_PLAYBOOK.md          ← exact recipe for writing every subject
└── vercel.json
```

## Run locally

```bash
npm install
npm run dev        # http://localhost:4321
```

## Deploy on Vercel (free, one time)

1. Go to https://vercel.com/new and sign in with GitHub.
2. Import `ashyou09/Gate-da`. Vercel detects **Astro** automatically (`vercel.json`).
3. Click **Deploy**. Every push to `main` redeploys the site.

## Adding notes

1. Follow [`NOTES_PLAYBOOK.md`](NOTES_PLAYBOOK.md).
2. Put topic pages in `src/content/docs/<slug>/` with `sidebar.order` in the frontmatter; the sidebar updates itself.
3. Run `python3 scripts/sync_subjects.py` to refresh the subject README, then `npm run build`.
