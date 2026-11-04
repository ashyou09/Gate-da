# GATE DA 2027 notes site

Astro + Starlight static site (math via remark-math + rehype-katex), deployed on Vercel.
- One folder per subject, same slug everywhere: notes in `src/content/docs/<slug>/`, study material in `subjects/<slug>/`, metadata in `scripts/subjects.json`.
- Sidebar autogenerates one group per subject folder (`astro.config.mjs`); order pages with `sidebar.order`.
- After adding pages run `python3 scripts/sync_subjects.py` (refreshes `subjects/<slug>/README.md`). Styles: `src/styles/custom.css`.
- When asked to write notes for a subject or topic, follow `NOTES_PLAYBOOK.md` exactly.
- Commits: author is the user (`ash_you09`, repo-local git config). Do not add Co-Authored-By or session trailers. Push directly to `main` (owner request) — no feature branches.
- Build check: `npm run build`.
