# GrattonPainting

Marketing website for **Gratton's Painting LLC** — a locally owned painting company serving Sarasota, Bradenton, and the Florida Gulf Coast.

**Phone:** (941) 773-3021

## What's included

| Path | Description |
|------|-------------|
| `index.html` | Design chooser — preview all five homepage options |
| `assets/` | Shared logo SVGs, `site.js`, and brand assets |
| `versions/v1-coastal-classic/` | Warm coastal layout with serif headlines |
| `versions/v2-sunset-bold/` | Bold sunset-orange hero, contractor tone |
| `versions/v3-clean-minimal/` | Minimal whitespace, upscale feel |
| `versions/v4-gallery-first/` | Photo gallery leads the page |
| `versions/v5-quote-focused/` | Conversion layout with sticky call bar |

## Quick start (local preview)

From this folder:

```bash
python3 -m http.server 8080
```

Then open:

- **Chooser:** http://localhost:8080
- **Version 1:** http://localhost:8080/versions/v1-coastal-classic/

## Logo

Replace `assets/logo.svg` and `assets/logo-mark.svg` with your final logo files, or add `assets/logo.png` and update the `<img>` tags in each version.

## Customize before launch

1. Swap gallery placeholders with real project photos.
2. Replace placeholder reviews with actual customer quotes.
3. Connect contact forms to Formspree, Netlify Forms, or your email backend (forms are demo-only today).
4. Pick one design version and promote it to the site root when ready.

## Publish as a standalone GitHub repo

From inside this folder:

```bash
git init
git branch -M main
git add .
git commit -m "Initial GrattonPainting website with five design options"
git remote add origin https://github.com/<your-username>/GrattonPainting.git
git push -u origin main
```

Repository name: **GrattonPainting**

## Deploy

Static hosting works on GitHub Pages, Netlify, or Cloudflare Pages. Point the host at this folder's root and set `index.html` as the entry page.
