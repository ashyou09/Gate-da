# Notes playbook — how every subject on the site is made

Say **"make <subject> the same way"** and follow this file exactly.

## 0. Sources (all in this repo)
- `pyq/DA.PYQ.20{24,25,26} (1).pdf` + `pyq/DA.PYQ.Keys.*` — real questions + official keys
- `pyq/analysis/GATE_DA_2027_Prediction_and_Pattern_Report.pdf` — marks per subject, topic confidence
- `maths/prob_dpp/GATE_DA_2027_<Subject>_Revision_Sheet.pdf` — formula boxes
- `maths/prob_dpp/ques bank/` — extra practice
- Reference list: https://github.com/DS-AI-GATE/dsai-gate
- Extract text with `pdftotext -layout`.

## 1. Subject hub page — `src/content/docs/<subject>/index.md`
1. Official syllabus quote.
2. Table of **every PYQ from 2024–2026** for the subject: year, Q no., marks, type, topic, what it tested, official answer.
3. Frequency table: topic → number of questions → verdict tag (`high` / `med` / `low`).
4. Ordered list of topic pages (most frequent first).

## 2. One page per topic — `src/content/docs/<subject>/<topic>.md`
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
- Add the new pages to the `sidebar` in `astro.config.mjs` and update the status column on `src/content/docs/index.md`.
- `npm run build` must pass before committing.

## 4. Commit
Commit as the user (repo-local git config `user.name = ash_you09`). No co-author trailer.
