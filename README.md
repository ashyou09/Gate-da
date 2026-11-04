# GATE DA 2027 — Notes website

Topic-wise GATE Data Science & AI notes, ordered by what the 2024–2026 papers asked.
Built with [Astro Starlight](https://starlight.astro.build) (static HTML, search, dark mode, KaTeX math).

## Run locally
```bash
npm install
npm run dev        # http://localhost:4321
```

## Deploy on Vercel (free, one time)
1. Go to https://vercel.com/new and sign in with GitHub.
2. Import the `ashyou09/Gate-da` repository. Vercel detects **Astro** automatically (settings are in `vercel.json`).
3. Click **Deploy**. Every later push to the production branch redeploys the site automatically.

## Adding notes
Follow `NOTES_PLAYBOOK.md`. Content lives in `src/content/docs/`.

## Folders
- `src/content/docs/` — the notes (Markdown + LaTeX)
- `pyq/` — GATE DA 2024–2026 papers, keys, prediction report, mock papers
- `maths/` — revision sheets and question banks
