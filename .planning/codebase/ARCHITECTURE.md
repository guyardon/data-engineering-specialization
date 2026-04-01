# Architecture

**Analysis Date:** 2026-03-31

## Pattern

Static Site Generator (SSG) with external content pipeline.

Content flows from Notion → Markdown files → Astro build → Static HTML deployed to GitHub Pages.

## Layers

### 1. Content Ingestion (pre-build)

- `scripts/fetch-notion.mjs` — manual script run before builds
- Authenticates to Notion API, traverses course hierarchy
- Converts Notion blocks → `.md` files with frontmatter
- Downloads images to `public/images/`
- Output: `src/content/notes/[courseSlug]/[weekSlug]/[section].md`

### 2. Content Schema

- `src/content.config.ts` — defines `notes` collection with Zod schema
- Fields: title, course, courseSlug, courseOrder, week, weekSlug, weekOrder, order, notionId

### 3. Routing & Pages

- `src/pages/index.astro` — redirects to first note
- `src/pages/notes/[...id].astro` (implied) — dynamic routes per note
- Route pattern: `/notes/[courseSlug]/[weekSlug]/[sectionSlug]/`

### 4. UI Components

- `src/layouts/NoteLayout.astro` — wraps note pages
- `src/components/Sidebar.astro` — course/week navigation
- `src/components/TableOfContents.astro` — per-note TOC

### 5. Build & Deploy

- `npm run build` → Astro SSG → `dist/`
- `.github/workflows/deploy.yml` → GitHub Actions → GitHub Pages
- Base path: `/data-engineering-specialization-website`

## Data Flow

```
Notion DB → fetch-notion.mjs → src/content/notes/*.md
                              → public/images/

src/content/notes/*.md → Astro build → dist/ → GitHub Pages
```

## Entry Points

- Dev: `npm run dev` → Astro dev server
- Content refresh: `NOTION_TOKEN=<token> node scripts/fetch-notion.mjs`
- Production build: `npm run build`

## Key Abstractions

- `src/lib/base.ts` — exports `BASE` path constant for GitHub Pages sub-path routing
- Content collection API (`astro:content`) — typed access to all notes
