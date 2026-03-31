# Data Engineering Specialization Website

## What This Is

A polished static documentation website for personal notes from the DeepLearning.ai Data Engineering Specialization (Coursera). Content originates in Notion (Courses → Weeks → Lessons, with images, tables, code blocks, and callouts), is synced once to markdown files, then served as a beautiful dark-mode reference site hosted on GitHub Pages.

## Core Value

Navigate and read course notes in a fast, well-designed interface — content over chrome.

## Requirements

### Validated

- [x] ESLint + Prettier configured with Astro plugin (Validated in Phase 1: Foundation & Tooling)
- [x] TypeScript strict mode passes with zero errors (Validated in Phase 1: Foundation & Tooling)
- [x] `npm run build` succeeds cleanly (Validated in Phase 1: Foundation & Tooling)

### Active

- [ ] Notion content fully synced to markdown files (all block types rendered correctly)
- [ ] Modern dark mode UI — intentional design, not generic
- [ ] Full content type support: images, tables, code blocks (with syntax highlighting), callouts, lists
- [ ] Sidebar navigation: Courses → Weeks → Lessons hierarchy
- [ ] Per-lesson table of contents
- [ ] Deployed to GitHub Pages via GitHub Actions CI/CD
- [ ] Responsive layout (desktop + mobile)

### Out of Scope

- Light mode toggle — dark mode only for now
- Search functionality — defer to v2
- Ongoing Notion sync — one-time pull, then edit markdown directly
- Comments or interactivity — purely static
- User authentication — public static site

## Context

**Existing codebase:** Astro 6.1.2 + TypeScript (strict) + TailwindCSS 4.2.2 + @notionhq/client. Project skeleton exists with content collection schema, `scripts/fetch-notion.mjs`, basic components (NoteLayout, Sidebar, TOC), and a GitHub Actions deploy workflow. Base path `/data-engineering-specialization-website` configured for GitHub Pages.

**Content:** Notion root page `139969a7aa018017b81fc3858c54fc8f`. Hierarchy: Root → Courses → Weeks → Sections → Subsections → `.md` files. Script handles paragraphs, headings, lists, tables, code blocks, images (downloaded to `public/images/`), callouts, toggles, equations.

**What needs work:** The UI components exist but need a full design overhaul. The fetch script likely needs auditing against the actual Notion content. Images not optimized via Astro Image component.

## Constraints

- **Tech stack:** Astro (static output) — no server runtime, no SSR
- **Hosting:** GitHub Pages sub-path (`/data-engineering-specialization-website`) — base path must stay in sync
- **Content source:** Notion API (read-only, `NOTION_TOKEN` secret) — one-time sync only
- **Design:** Dark mode only, Tailwind CSS 4 — no component library (custom design)
- **Node:** >= 22.12.0

## Key Decisions

| Decision                                    | Rationale                                                | Outcome   |
| ------------------------------------------- | -------------------------------------------------------- | --------- |
| Astro SSG                                   | Static site, no runtime needed, fast GitHub Pages deploy | — Pending |
| TailwindCSS 4                               | Already installed, modern utility CSS                    | — Pending |
| Markdown files as source of truth post-sync | Removes ongoing Notion API dependency, simpler workflow  | — Pending |
| Dark mode only                              | Intentional design choice, not missing feature           | — Pending |

---

_Last updated: 2026-03-31 — Phase 1 (Foundation & Tooling) complete_
