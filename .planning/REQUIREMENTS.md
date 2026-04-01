# Requirements: Data Engineering Specialization Website

**Defined:** 2026-03-31
**Core Value:** Navigate and read course notes in a fast, well-designed interface — content over chrome.

## v1 Requirements

### Tooling & Foundation

- [x] **TOOL-01**: Project has ESLint + Prettier configured with Astro plugin
- [x] **TOOL-02**: TypeScript strict mode passes with zero errors across all source files
- [x] **TOOL-03**: `npm run build` succeeds cleanly from a fresh clone

### Notion Sync

- [x] **SYNC-01**: Running `fetch-notion.mjs` produces `.md` files for all courses, weeks, and lessons
- [x] **SYNC-02**: All text block types render correctly (paragraphs, headings h1-h3, bold, italic, inline code)
- [x] **SYNC-03**: Code blocks render with correct language tag for syntax highlighting
- [x] **SYNC-04**: Images download to `public/images/` and reference correctly in markdown
- [x] **SYNC-05**: Tables render as valid markdown tables
- [x] **SYNC-06**: Callouts/admonitions convert to a consistent markdown representation
- [x] **SYNC-07**: Nested lists render correctly
- [x] **SYNC-08**: Frontmatter includes: title, course, courseSlug, courseOrder, week, weekSlug, weekOrder, order, notionId

### UI Design & Layout

- [ ] **UI-01**: Dark mode color scheme — intentional, not generic
- [ ] **UI-02**: Typography system — readable body text, clear heading hierarchy
- [ ] **UI-03**: Sidebar shows full Courses → Weeks → Lessons hierarchy
- [ ] **UI-04**: Active lesson highlighted in sidebar
- [ ] **UI-05**: Per-lesson table of contents (anchored headings)
- [ ] **UI-06**: Responsive layout — sidebar collapses to mobile drawer/menu
- [ ] **UI-07**: Smooth scrolling and anchor navigation
- [ ] **UI-08**: Page transitions feel snappy (no layout shift)

### Content Rendering

- [ ] **CONT-01**: Code blocks rendered with syntax highlighting (Shiki, GitHub dark theme)
- [ ] **CONT-02**: Images displayed with Astro Image optimization (correct sizing, lazy loading)
- [ ] **CONT-03**: Tables styled and readable
- [ ] **CONT-04**: Callout/admonition blocks visually distinct (info, warning, tip styles)
- [ ] **CONT-05**: Inline code styled consistently
- [ ] **CONT-06**: Blockquotes styled

### Navigation

- [ ] **NAV-01**: Index page routes to first lesson automatically
- [ ] **NAV-02**: Previous/next lesson navigation within a week
- [ ] **NAV-03**: Breadcrumb showing Course → Week → Lesson
- [ ] **NAV-04**: Direct URL to any lesson works correctly with GitHub Pages base path

### Deployment

- [ ] **DEPLOY-01**: GitHub Actions workflow builds and deploys on push to `main`
- [ ] **DEPLOY-02**: `NOTION_TOKEN` stored as GitHub secret (not in code)
- [ ] **DEPLOY-03**: Site accessible at `https://guyardon.github.io/data-engineering-specialization-website`
- [ ] **DEPLOY-04**: All links work correctly under the `/data-engineering-specialization-website` base path

## v2 Requirements

### Search

- **SRCH-01**: Full-text search across all notes
- **SRCH-02**: Search results link directly to relevant section

### Content Management

- **CMGT-01**: CLI script to re-sync specific course from Notion
- **CMGT-02**: Incremental sync (only changed pages)

### Enhancements

- **ENH-01**: Light mode toggle
- **ENH-02**: Reading progress indicator
- **ENH-03**: Keyboard navigation shortcuts

## Out of Scope

| Feature                        | Reason                                |
| ------------------------------ | ------------------------------------- |
| Server-side rendering          | Static site, no runtime needed        |
| User authentication            | Public reference site                 |
| Comments / interactivity       | Static-only, no backend               |
| Ongoing Notion sync automation | One-time pull, edit markdown directly |
| Mobile app                     | Web-first                             |
| Light mode                     | Intentional dark-only design for v1   |

## Traceability

| Requirement | Phase   | Status   |
| ----------- | ------- | -------- |
| TOOL-01     | Phase 1 | Complete |
| TOOL-02     | Phase 1 | Pending  |
| TOOL-03     | Phase 1 | Pending  |
| SYNC-01     | Phase 2 | Complete |
| SYNC-02     | Phase 2 | Complete |
| SYNC-03     | Phase 2 | Complete |
| SYNC-04     | Phase 2 | Complete |
| SYNC-05     | Phase 2 | Complete |
| SYNC-06     | Phase 2 | Complete |
| SYNC-07     | Phase 2 | Complete |
| SYNC-08     | Phase 2 | Complete |
| UI-01       | Phase 3 | Pending  |
| UI-02       | Phase 3 | Pending  |
| UI-03       | Phase 3 | Pending  |
| UI-04       | Phase 3 | Pending  |
| UI-05       | Phase 3 | Pending  |
| UI-06       | Phase 3 | Pending  |
| UI-07       | Phase 3 | Pending  |
| UI-08       | Phase 3 | Pending  |
| CONT-01     | Phase 4 | Pending  |
| CONT-02     | Phase 4 | Pending  |
| CONT-03     | Phase 4 | Pending  |
| CONT-04     | Phase 4 | Pending  |
| CONT-05     | Phase 4 | Pending  |
| CONT-06     | Phase 4 | Pending  |
| NAV-01      | Phase 4 | Pending  |
| NAV-02      | Phase 4 | Pending  |
| NAV-03      | Phase 4 | Pending  |
| NAV-04      | Phase 4 | Pending  |
| DEPLOY-01   | Phase 5 | Pending  |
| DEPLOY-02   | Phase 5 | Pending  |
| DEPLOY-03   | Phase 5 | Pending  |
| DEPLOY-04   | Phase 5 | Pending  |

**Coverage:**

- v1 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0 ✓

---

_Requirements defined: 2026-03-31_
_Last updated: 2026-03-31 after initial definition_
