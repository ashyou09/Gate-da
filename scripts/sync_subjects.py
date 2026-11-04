"""Keep per-subject folders in sync.

Run:  python3 scripts/sync_subjects.py

For every subject in scripts/subjects.json it
  1. creates src/content/docs/<slug>/index.md (subject hub) if it does not exist yet,
  2. regenerates subjects/<slug>/README.md (study material + list of notes pages).
Existing hub pages and topic pages are never overwritten.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/ashyou09/Gate-da/blob/main"
TAG = {"high": "★ HIGH", "med": "◆ MED", "low": "○ LOW"}
subjects = json.loads((ROOT / "scripts/subjects.json").read_text())


def front(path):
    """Return (title, sidebar order) from a markdown page's frontmatter."""
    text = path.read_text()
    title = re.search(r"^title:\s*(.+)$", text, re.M)
    label = re.search(r"^\s+label:\s*(.+)$", text, re.M)
    order = re.search(r"^\s+order:\s*(\d+)$", text, re.M)
    return ((label or title).group(1).strip(), int(order.group(1)) if order else 99)


for s in subjects:
    slug, name = s["slug"], s["name"]
    docs = ROOT / "src/content/docs" / slug
    mat = ROOT / "subjects" / slug
    docs.mkdir(parents=True, exist_ok=True)
    mat.mkdir(parents=True, exist_ok=True)
    m = s["marks"]
    mean = round(sum(m) / 3, 1)

    # ---- 1. hub page (only if missing) ----
    hub = docs / "index.md"
    created = not hub.exists()
    if created:
        files = sorted(p for p in mat.rglob("*") if p.is_file() and p.name != "README.md")
        mats = "\n".join(
            f"- [{p.relative_to(mat)}]({REPO}/subjects/{slug}/{p.relative_to(mat).as_posix()})" for p in files
        )
        hub.write_text(f"""---
title: {json.dumps(name, ensure_ascii=False)}
description: {json.dumps("GATE DA " + name + ": syllabus, weightage, topic plan and study material.", ensure_ascii=False)}
sidebar:
  label: Overview & topic plan
  order: 0
---

Notes for this subject are on the way. The topics above are in study order, and the full PYQ map comes with the first topic page.

## Official syllabus

> {s["syllabus"]}

## Study material in the repo

{mats}
""")

    # ---- 2. material README (always regenerated) ----
    pages = sorted(
        (front(p) + (p.stem,) for p in docs.glob("*.md") if p.name != "index.md"),
        key=lambda x: x[1],
    )
    notes = "\n".join(f"- {t} — `src/content/docs/{slug}/{stem}.md`" for t, _, stem in pages) or "- _Not started yet._"
    files = sorted(p for p in mat.rglob("*") if p.is_file() and p.name != "README.md")
    mats = "\n".join(f"- [`{p.relative_to(mat).as_posix()}`]({p.relative_to(mat).as_posix().replace(' ', '%20')})" for p in files)
    (mat / "README.md").write_text(f"""# {name}

**Marks in GATE DA:** 2024: {m[0]} · 2025: {m[1]} · 2026: {m[2]} · mean {mean}

{s["note"]}

## Study material in this folder

{mats}

## Notes on the website

Hub page: `src/content/docs/{slug}/index.md` (site URL `/{slug}/`)

{notes}

## Official syllabus

> {s["syllabus"]}
""")
    print(f"{slug:24s} hub={'new' if created else 'kept'} notes={len(pages)} files={len(files)}")
