# Design Redesign — DE Specialization Website

## Overview

Redesign the site's visual identity from a basic dark-theme documentation site to an editorial, typography-driven design inspired by markdown.engineering. Serif headings, monochrome palette with warm gold accent, card-based content layout, dark/light toggle, full-text search, and emoji-enhanced navigation.

## Design System

### Typography

| Role | Font | Source |
|------|------|--------|
| Headings (h1-h4) | Lora | Google Fonts |
| Body, UI, navigation | Inter | Google Fonts |
| Code blocks, inline code | JetBrains Mono | Google Fonts |

Sizing uses `clamp()` for fluid responsiveness:
- h1: `clamp(1.8rem, 4vw, 2.5rem)`
- h2: `clamp(1.2rem, 2.5vw, 1.5rem)`
- h3: `clamp(1.05rem, 2vw, 1.2rem)`
- Body: `1rem` at line-height `1.75`
- Small/meta text: `0.8rem`

Weight hierarchy: headings at 600-700, body at 400, navigation labels at 500-600.

### Color Palette

All colors defined as CSS custom properties on `:root` and `[data-theme="light"]`.

**Dark mode (default):**

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0a0a0b` | Page background |
| `--bg-card` | `#111113` | Card/section background |
| `--bg-hover` | `#1a1a1d` | Hover states |
| `--fg` | `#e8e8ea` | Primary text |
| `--fg-muted` | `#a0a0a8` | Secondary text |
| `--fg-soft` | `#65656e` | Tertiary text, borders |
| `--accent` | `#c9a84c` | Links, active states, highlights |
| `--accent-hover` | `#dabb65` | Accent hover |
| `--line` | `#2a2a2e` | Borders, dividers |
| `--line-strong` | `#3a3a3f` | Emphasized borders |
| `--shadow-soft` | `rgba(0,0,0,0.3)` | Card shadows |
| `--code-bg` | `#161618` | Code block background |

**Light mode:**

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#fafaf8` | Page background |
| `--bg-card` | `#ffffff` | Card/section background |
| `--bg-hover` | `#f0f0ee` | Hover states |
| `--fg` | `#1a1a1d` | Primary text |
| `--fg-muted` | `#5a5a63` | Secondary text |
| `--fg-soft` | `#9a9aa3` | Tertiary text |
| `--accent` | `#a08930` | Links, active states |
| `--accent-hover` | `#8a7528` | Accent hover |
| `--line` | `#e5e5e0` | Borders |
| `--line-strong` | `#d0d0ca` | Emphasized borders |
| `--shadow-soft` | `rgba(0,0,0,0.06)` | Card shadows |
| `--code-bg` | `#f5f5f0` | Code block background |

### Spacing

- Card padding: `clamp(1rem, 2vw, 1.5rem)`
- Card gap: `1.2rem`
- Card border-radius: `14px`
- Section spacing: `2rem` vertical
- Page padding: `clamp(1.5rem, 3vw, 2.5rem)`

### Interactive States

- Card hover: `translateY(-3px)` + accent border-color + shadow increase. Transition `0.18s ease`.
- Link hover: color shifts from `--accent` to `--accent-hover`, underline appears.
- Active sidebar item: left border `--accent`, background `--bg-hover`.

## Components

### 1. Theme Toggle

- Position: sidebar header, next to site logo
- Icons: sun/moon symbols (not emoji — use inline SVG for crisp rendering)
- Behavior:
  - First visit: respect `prefers-color-scheme`, default dark
  - Toggle sets `data-theme` attribute on `<html>` and persists to `localStorage`
  - Script in `<head>` (blocking) reads preference before paint to prevent flash

### 2. Logo

- Minimalist icon + text mark
- Icon: simple geometric symbol suggesting data flow or engineering (e.g., stylized bracket/pipeline icon, or a clean SVG glyph)
- Text: "DE Specialization" in Lora, semi-bold
- Replaces current emoji + text in sidebar header
- Also appears on home page hero

### 3. Home Page

**Structure (top to bottom):**

1. **Top bar**: Logo (left), theme toggle (right). Minimal, no heavy nav.
2. **Hero**: Large Lora heading: "Data Engineering Specialization". Subtitle in Inter muted: "Course notes and study guide for the DeepLearning.AI Data Engineering Professional Certificate." Centered, generous vertical padding.
3. **Search bar**: Centered below hero. Full width up to `max-width: 480px`. Rounded (10px), subtle border, placeholder "Search notes...". Powered by Pagefind.
4. **Course cards**: 2x2 grid on desktop (`max-width: 720px`), single column on mobile. Each card:
   - Emoji + "Course N" badge in small caps, `--fg-soft`
   - Title in Lora, `--fg`
   - One-line description in `--fg-muted`
   - Meta line: "N weeks · M sections" in `--fg-soft`
   - Hover: lift + accent border
5. **Quick links**: Small horizontal strip below courses. Slots for "All Sections" and future additions. Keeps home page extensible.
6. **Footer**: Minimal — "Built with Astro" or source link.

**No sidebar on home page.** Clean, focused entry point.

### 4. Sidebar (Note Pages)

**Structure unchanged**, styling updated:

- Header: Logo (links home) + theme toggle
- Course entries: emoji prefix + title
  - Course 1: data flow emoji + "Intro to DE"
  - Course 2: plug emoji + "Source Systems & Pipelines"
  - Course 3: database emoji + "Storage & Queries"
  - Course 4: gear emoji + "Modeling & Serving"
- Week entries: contextual emoji prefix (e.g., cloud for AWS week, puzzle for architecture)
- Section links: Inter, `--fg-soft`, active state uses `--accent` left-border + `--bg-hover` background
- All blue (`sky-400`) replaced with `--accent` (warm gold)
- Typography tightened: course titles 600 weight, week titles 500, section links 400

### 5. Note Page Content — Card Sections

Each `##` heading and its content rendered inside a card:

- Card: `--bg-card` background, `1px solid var(--line)` border, `14px` border-radius, `var(--shadow-soft)` box-shadow
- Cards stack vertically with `1.2rem` gap
- `##` heading renders as the card title (Lora, `--fg`, 600 weight)
- All content within (paragraphs, lists, code blocks, images, tables) styled inside the card
- Cards provide visual grouping — each section is a digestible block

**Breadcrumb**: Course name in Lora (serif), separator and week in Inter. Uses `--fg-muted`.

**Prev/Next nav**: Restyled as cards with the new system — `--bg-card`, accent border on hover, Lora for the page title.

**Table of Contents (right sidebar)**: Stays, styled with `--fg-soft` links, `--accent` active state, `--line` left border.

### 6. Search (Pagefind)

- Integration: Pagefind (build-time static search indexing)
- Install: `@pagefind/default-ui` package
- Build: runs after Astro build to index the `dist/` output
- UI: custom-styled to match the design system (override Pagefind default CSS with custom properties)
- Scope: full-text search across all note content
- Results: show page title, breadcrumb (course > week), and text snippet

### 7. Prose Styles (Updated)

All current prose styles updated to use CSS custom properties:
- Headings: Lora, `--fg`
- Body: Inter, `--fg` primary, `--fg-muted` for secondary
- Links: `--accent`, underline on hover
- Code inline: `--code-bg` background, `--accent` text
- Code blocks: `--code-bg` background, `--line` border
- Images: `--line` border, `14px` radius (match cards)
- Tables: `--line` borders, alternating row `--bg-hover`
- Blockquotes: `--accent` left border (replacing sky-blue)
- `<hr>`: `--line`

## Responsive Behavior

| Breakpoint | Behavior |
|-----------|----------|
| > 1200px | Full 3-column: sidebar + content cards + ToC |
| 768-1200px | 2-column: sidebar + content cards (ToC hidden) |
| < 768px | Single column: mobile topbar + slide-out sidebar, full-width cards |

Home page: 2x2 course grid > 768px, single column below.

## Files Affected

| File | Change |
|------|--------|
| `src/styles/global.css` | Complete rewrite — CSS custom properties, Lora/Inter imports, prose in cards, theme toggle |
| `src/pages/index.astro` | Redesigned home page with hero, search, course cards, footer |
| `src/layouts/NoteLayout.astro` | Card wrapper around sections, updated breadcrumb, theme toggle script |
| `src/components/Sidebar.astro` | Emoji prefixes, gold accent, logo, theme toggle button, CSS var colors |
| `src/components/TableOfContents.astro` | Updated colors to CSS vars |
| `src/components/ThemeToggle.astro` | **New** — toggle button component |
| `src/components/SearchBar.astro` | **New** — Pagefind search UI wrapper |
| `src/components/Logo.astro` | **New** — SVG logo component |
| `src/components/ContentCard.astro` | **New** — card wrapper for `##` sections (used via remark plugin or layout JS) |
| `public/favicon.svg` | Updated to match new logo |
| `astro.config.mjs` | Add Pagefind integration |
| `package.json` | Add `@pagefind/default-ui`, Google Fonts dependencies |

## What This Does NOT Change

- Content structure (markdown files, frontmatter schema, directory layout)
- Routing (`/notes/[...slug]`)
- Sidebar navigation tree logic (courses > weeks > sections)
- Build output (static site)

## Success Criteria

- [ ] All pages render with Lora headings, Inter body, JetBrains Mono code
- [ ] Dark/light toggle works with no flash on load
- [ ] Home page has logo, search, course cards, is not cluttered
- [ ] Sidebar has emoji prefixes and warm gold active states
- [ ] Note content sections wrapped in cards with proper spacing
- [ ] Pagefind search returns results across all notes
- [ ] All existing content displays correctly (images, code blocks, tables)
- [ ] Responsive at all three breakpoints
- [ ] No blue (`sky-400`) remaining anywhere
