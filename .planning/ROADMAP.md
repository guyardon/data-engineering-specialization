# Roadmap: Data Engineering Specialization Website

**Project:** Data Engineering Specialization Website
**Milestone:** v1 — Content online, beautifully designed, deployed
**Created:** 2026-03-31

---

## Phase 1 — Foundation & Tooling

**Goal:** Clean, buildable project with proper tooling in place.

**Plans:**
1. Add ESLint + Prettier with Astro plugin; fix any existing lint errors
2. Audit TypeScript — resolve strict mode errors, clean up `any` types
3. Verify `npm run build` succeeds end-to-end from a fresh state

**Requirements:** TOOL-01, TOOL-02, TOOL-03
**Depends on:** nothing

---

## Phase 2 — Notion Sync Audit & Fix

**Goal:** Running `fetch-notion.mjs` produces correct, complete markdown for all block types.

**Plans:**
1. Run the fetch script against the live Notion workspace; audit output quality
2. Fix block type handling: code blocks (language tags), tables, callouts, nested lists
3. Fix image handling: correct paths, filenames, markdown references
4. Validate frontmatter schema matches `content.config.ts` for all generated files

**Requirements:** SYNC-01 through SYNC-08
**Depends on:** Phase 1

---

## Phase 3 — UI Design System & Layout

**Goal:** Full visual redesign — dark mode, intentional typography, clean layout with sidebar + TOC.

**Plans:**
1. Define design tokens: color palette (dark), typography scale, spacing
2. Redesign NoteLayout — two-column (sidebar + content + TOC), responsive
3. Redesign Sidebar component — collapsible hierarchy, active state, mobile drawer
4. Redesign TableOfContents component — sticky, scroll-spy active heading
5. Add breadcrumb, previous/next navigation, smooth scroll

**Requirements:** UI-01 through UI-08, NAV-01 through NAV-04
**Depends on:** Phase 1

---

## Phase 4 — Content Rendering Components

**Goal:** Every content block type renders beautifully and correctly.

**Plans:**
1. Custom MDX components: Callout/Admonition (info, warning, tip, note)
2. Code block styling — Shiki GitHub dark, copy button, language label
3. Table styling — readable, scrollable on mobile
4. Image component — Astro Image optimization, captions, lazy loading
5. Typography polish — inline code, blockquotes, list styles

**Requirements:** CONT-01 through CONT-06
**Depends on:** Phase 2, Phase 3

---

## Phase 5 — Deploy & CI/CD

**Goal:** Site live on GitHub Pages, auto-deploys on push to main.

**Plans:**
1. Audit and finalize GitHub Actions workflow (build + deploy)
2. Configure `NOTION_TOKEN` as GitHub secret; document content refresh process
3. Smoke test all routes under base path `/data-engineering-specialization-website`
4. Performance check — image sizes, build output, Core Web Vitals

**Requirements:** DEPLOY-01 through DEPLOY-04
**Depends on:** Phase 4

---

## Milestone Complete When

- [ ] All 32 v1 requirements checked off in REQUIREMENTS.md
- [ ] Site live at `https://guyardon.github.io/data-engineering-specialization-website`
- [ ] All content types render correctly
- [ ] Build passes in CI without errors
