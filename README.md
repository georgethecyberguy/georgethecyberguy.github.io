# georgethecyberguy.github.io

Personal site and blog. Built with Jekyll. Served via GitHub Pages at
[georgethecyberguy.github.io](https://georgethecyberguy.github.io).

## Deploying for the first time

1. Create a **new** repository on GitHub named **exactly**
   `georgethecyberguy.github.io`. The name has to match the username — that's
   what tells GitHub Pages to serve it as a user site at the bare domain.
2. Push this directory to the new repo:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/georgethecyberguy/georgethecyberguy.github.io.git
   git add .
   git commit -m "Initial site"
   git push -u origin main
   ```
3. In the repo's **Settings → Pages**, confirm:
   - Source: *Deploy from a branch*
   - Branch: `main`, folder `/ (root)`
4. Wait 1–2 minutes for the first build, then visit
   `https://georgethecyberguy.github.io`.

## Local development (optional)

If you want to preview locally before pushing:

```bash
# One-time setup
gem install bundler
bundle install

# Live preview at http://localhost:4000
bundle exec jekyll serve --livereload
```

The `Gemfile` pins to the `github-pages` meta-gem so what you see locally
matches what GitHub Pages produces in production.

## Adding content

### A new blog post

Create a Markdown file under `_posts/` named with the date pattern
`YYYY-MM-DD-slug.md`:

```markdown
---
title: Your post title
subtitle: Optional one-line subtitle.
date: 2026-05-15 09:00:00 -0500
tags: [walkthrough, detection]
---

Body in Markdown. Code fences, tables, blockquotes all work.
```

### A new project entry

Create a Markdown file under `_projects/`:

```markdown
---
title: Project name
order: 7
year: 2026
kind: Lab
status: In progress
role: Lead
stack:
  - Tool 1
  - Tool 2
repo: https://github.com/georgethecyberguy/repo-name
summary: One-line description.
---

Long-form description of the project here.
```

### Updating the `/now` page

Edit `now.md` whenever something material changes. The whole point of a
`/now` page is that it's freshly current — if it's stale, delete it.

## Site structure

```
.
├── _config.yml          # Site metadata, plugins, collections
├── _includes/           # Shared partials (head, header, footer)
├── _layouts/            # Page templates
├── _posts/              # Blog posts (date-prefixed filenames)
├── _projects/           # Project entries (collection)
├── assets/css/main.scss # All site styles
├── index.html           # Home page
├── about.md             # /about/
├── now.md               # /now/
├── projects.html        # /projects/ index
└── writing.html         # /writing/ archive
```

## Design notes

- Type system: **Instrument Serif** (display, italic) + **IBM Plex Sans**
  (body) + **IBM Plex Mono** (metadata, code).
- Single accent color: deep oxblood (`#6b1f24`). Adjust in
  `assets/css/main.scss` under `--accent`.
- Auto dark theme via `prefers-color-scheme`.
- All plugins used (`jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`)
  are on the GitHub Pages whitelist — no custom build action needed.
