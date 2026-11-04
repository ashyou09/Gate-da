# Notes playbook — how every subject on the site is made

Say **"make <subject> the same way"** and follow this file exactly.

## 0. Sources (all in this repo)
- `pyq/papers/GATE-DA-20{24,25,26}.pdf` + `pyq/keys/GATE-DA-20xx-key.pdf` — real questions + official keys
- `pyq/analysis/prediction-and-pattern-report.pdf` — marks per subject, topic confidence
- `subjects/<slug>/revision-sheet.pdf` — formula boxes
- `subjects/<slug>/question-bank.pdf` — extra practice (books / extra notes also in that folder)
- Reference list: https://github.com/DS-AI-GATE/dsai-gate
- Extract text with `pdftotext -layout`.

## Folder layout (one folder per subject, same slug everywhere)

| Slug | Subject |
|---|---|
| `pdsa` | Programming, DS & Algorithms |
| `machine-learning` | Machine Learning |
| `dbms` | DBMS & Warehousing |
| `ai` | Artificial Intelligence |
| `probability-statistics` | Probability & Statistics |
| `linear-algebra` | Linear Algebra |
| `calculus-optimization` | Calculus & Optimization |
| `general-aptitude` | General Aptitude |

- Website notes: `src/content/docs/<slug>/` (hub `index.md` + one `.md` per topic)
- Study material: `subjects/<slug>/` (PDFs + auto-generated `README.md`)
- Subject metadata (marks, syllabus, topic plan): `scripts/subjects.json`
- The sidebar picks up new pages automatically (`astro.config.mjs` autogenerates one group per folder).

## 1. Subject hub page — `src/content/docs/<slug>/index.md`
A starter hub (syllabus, marks, topic plan) already exists for every subject. When starting a subject, replace it with:
1. Official syllabus quote.
2. Table of **every PYQ from 2024–2026** for the subject: year, Q no., marks, type, topic, what it tested, official answer.
3. Frequency table: topic → number of questions → verdict tag (`high` / `med` / `low`).
4. Ordered list of topic pages (most frequent first).

## 2. One page per topic — `src/content/docs/<slug>/<topic>.md`
Frontmatter must include `sidebar: { label: "N. Short name", order: N }` (hub is order 0).
Fixed order of sections:
1. Tags: `<span class="tag high">★ HIGH</span>` + `<span class="tag yr">2025 ×2</span>`, then **Why it matters** (which PYQs came from this topic).
2. `## Topic map` — `<div class="mindmap">` around a nested markdown list.
3. **Teach** sections `## N.1 …`, `## N.2 …` — basics first, intuition before formula, a small example after every rule. Formulas in `<div class="formula">`, traps in `<div class="trap">`. LaTeX with `$…$` / `$$…$$`.
4. `## Summary: important points` — numbered list inside `<div class="formula">`.
5. `## Test yourself (A): previous-year questions` — every PYQ on this topic, as `### GATE DA <year> Q<n> (<marks>, <type>)`, solution inside `<details><summary>Solution: answer …</summary> … </details>`.
6. `## Test yourself (B): predicted 2027-style questions` — 5–7 new MCQ/MSQ/NAT questions (F1, F2 …) in the same `<details>` format.

## 3. Quality rules
- **Verify every answer**: run code questions in Python; recompute every number; match PYQ answers against the official key.
- Blank line after every opening `<div …>` / `<details>` / `<summary>` line and before the closing tag, so markdown inside renders.
- Update the status column on `src/content/docs/index.md` and the root `README.md` status table.
- Run `python3 scripts/sync_subjects.py` to refresh `subjects/<slug>/README.md`.
- `npm run build` must pass before committing.

## 4. Commit
Commit as the user (repo-local git config `user.name = ash_you09`). No co-author trailer. Push straight to `main`.
