# Roadmap: Data Engineering Specialization Website

## Overview

Brownfield Astro project that fetches course notes from Notion and serves them as a polished dark-mode static website on GitHub Pages. Starting from a working skeleton, we add proper tooling, fix the Notion sync, redesign the UI, build content rendering components, then deploy with CI/CD.

## Phases

- [ ] **Phase 1: Foundation & Tooling** - ESLint, Prettier, TypeScript clean build
- [ ] **Phase 2: Notion Sync Audit & Fix** - All block types produce correct markdown
- [ ] **Phase 3: UI Design System & Layout** - Dark theme, sidebar, TOC, responsive layout
- [ ] **Phase 4: Content Rendering Components** - Callouts, code blocks, tables, image optimization
- [ ] **Phase 5: Deploy & CI/CD** - GitHub Actions, live on GitHub Pages

## Phase Details

### Phase 1: Foundation & Tooling

**Goal**: Clean, buildable project with ESLint, Prettier, and TypeScript passing with zero errors.
**Depends on**: Nothing (first phase)
**Requirements**: TOOL-01, TOOL-02, TOOL-03
**Success Criteria** (what must be TRUE):

1. `npm run lint` passes with zero errors on all source files
2. `npm run build` succeeds from a clean checkout
3. TypeScript strict mode reports zero errors
   **Plans**: 3 plans

Plans:

- [x] 01-01: Add ESLint + Prettier with Astro plugin; configure rules
- [x] 01-02: Audit and fix TypeScript strict mode errors across all source files
- [ ] 01-03: Verify clean build end-to-end; add lint/typecheck to package.json scripts

### Phase 2: Notion Sync Audit & Fix

**Goal**: Running `fetch-notion.mjs` produces correct, complete markdown for all Notion block types.
**Depends on**: Phase 1
**Requirements**: SYNC-01, SYNC-02, SYNC-03, SYNC-04, SYNC-05, SYNC-06, SYNC-07, SYNC-08
**Success Criteria** (what must be TRUE):

1. Script runs without errors and generates .md files for all courses/weeks/lessons
2. All block types (code, tables, callouts, images, nested lists) render as valid markdown
3. All images download to public/images/ and are correctly referenced in markdown
4. Frontmatter matches content.config.ts schema for every generated file
   **Plans**: 2 plans

Plans:

- [x] 02-01-PLAN.md — Fix richTextToMd href, table separator, and flatten subsection traversal
- [ ] 02-02-PLAN.md — Run script, validate output, verify all block types and frontmatter

### Phase 3: UI Design System & Layout

**Goal**: Full visual redesign — intentional dark mode, readable typography, sidebar + TOC layout, responsive.
**Depends on**: Phase 1
**Requirements**: UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, UI-07, UI-08, NAV-01, NAV-02, NAV-03, NAV-04
**Success Criteria** (what must be TRUE):

1. Dark color scheme applied consistently across all pages
2. Sidebar shows Courses → Weeks → Lessons hierarchy with active state
3. Table of contents updates as user scrolls (scroll-spy)
4. Layout is usable on mobile (sidebar collapses)
5. Breadcrumb, prev/next navigation present on every lesson page
   **Plans**: 5 plans

Plans:

- [ ] 03-01: Define design tokens (colors, typography, spacing) in Tailwind config
- [ ] 03-02: Redesign NoteLayout — two-column responsive shell
- [ ] 03-03: Redesign Sidebar — hierarchy navigation, active state, mobile drawer
- [ ] 03-04: Redesign TableOfContents — sticky, scroll-spy
- [ ] 03-05: Add breadcrumb, prev/next lesson navigation, smooth scroll

### Phase 4: Content Rendering Components

**Goal**: Every content block type (images, tables, code, callouts) renders beautifully with custom components.
**Depends on**: Phase 2, Phase 3
**Requirements**: CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06
**Success Criteria** (what must be TRUE):

1. Code blocks render with Shiki syntax highlighting and a copy button
2. Images use Astro Image component with lazy loading and correct sizing
3. Callout/admonition blocks are visually distinct by type (info, warning, tip)
4. Tables are readable and scroll horizontally on mobile
   **Plans**: 5 plans

Plans:

- [ ] 04-01: Callout/Admonition component (info, warning, tip, note variants)
- [ ] 04-02: Code block styling — Shiki GitHub dark, copy button, language label
- [ ] 04-03: Table component — styled, horizontally scrollable on mobile
- [ ] 04-04: Image component — Astro Image optimization, captions, lazy loading
- [ ] 04-05: Typography polish — inline code, blockquotes, list styles, overall prose

### Phase 5: Deploy & CI/CD

**Goal**: Site live on GitHub Pages, auto-deploys on every push to main.
**Depends on**: Phase 4
**Requirements**: DEPLOY-01, DEPLOY-02, DEPLOY-03, DEPLOY-04
**Success Criteria** (what must be TRUE):

1. Push to main triggers GitHub Actions build and deploy automatically
2. Site is accessible at https://guyardon.github.io/data-engineering-specialization-website
3. All internal links work correctly under the base path
4. Build passes in CI with zero errors
   **Plans**: 4 plans

Plans:

- [ ] 05-01: Audit and finalize GitHub Actions deploy workflow
- [ ] 05-02: Configure NOTION_TOKEN as GitHub secret; document content refresh steps
- [ ] 05-03: Smoke test all routes and links under base path
- [ ] 05-04: Performance check — image sizes, Lighthouse, build output size
