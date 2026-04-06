# Design Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the DE Specialization website with serif/sans typography, warm monochrome palette, card-based content, dark/light toggle, and Pagefind search.

**Architecture:** CSS custom properties drive theming (dark default, light via `[data-theme="light"]`). Google Fonts loaded via `@import`. Content cards created by a client-side script that wraps `##` sections in `<div class="content-card">` elements using safe DOM APIs. Pagefind indexes the static build output.

**Tech Stack:** Astro 6, Tailwind 4, Google Fonts (Lora, Inter, JetBrains Mono), Pagefind, CSS custom properties.

**Spec:** `docs/superpowers/specs/2026-04-01-design-redesign.md`

---

## File Map

| File                                   | Responsibility                                                                    | Task |
| -------------------------------------- | --------------------------------------------------------------------------------- | ---- |
| `src/styles/global.css`                | CSS custom properties, font imports, prose styles, card styles, theme transitions | 1    |
| `src/components/ThemeToggle.astro`     | **New** — sun/moon toggle button with localStorage persistence                    | 2    |
| `src/components/Logo.astro`            | **New** — SVG logo + text mark                                                    | 2    |
| `src/components/Sidebar.astro`         | Emoji prefixes, CSS var colors, logo + toggle in header                           | 3    |
| `src/components/TableOfContents.astro` | CSS var colors                                                                    | 3    |
| `src/layouts/NoteLayout.astro`         | Theme script in head, card-wrapping script, updated styles                        | 4    |
| `src/pages/index.astro`                | Redesigned home page: hero, search placeholder, course cards, footer              | 5    |
| `astro.config.mjs`                     | No changes needed (Pagefind runs post-build)                                      | —    |
| `package.json`                         | Add pagefind dev dependency, update build script                                  | 6    |
| `src/components/SearchBar.astro`       | **New** — Pagefind UI wrapper with custom styles                                  | 6    |
| `public/favicon.svg`                   | Updated logo icon                                                                 | 2    |

---

### Task 1: Design System Foundation — CSS Custom Properties, Fonts, Prose Styles

**Files:**

- Modify: `src/styles/global.css` (complete rewrite)

- [ ] **Step 1: Rewrite global.css with CSS custom properties and font imports**

Replace the entire contents of `src/styles/global.css` with:

```css
@import "tailwindcss";

/* Google Fonts */
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap");

/* ===== Dark theme (default) ===== */
:root {
  --font-serif: "Lora", Georgia, serif;
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --bg: #0a0a0b;
  --bg-card: #111113;
  --bg-hover: #1a1a1d;
  --fg: #e8e8ea;
  --fg-muted: #a0a0a8;
  --fg-soft: #65656e;
  --accent: #c9a84c;
  --accent-hover: #dabb65;
  --line: #2a2a2e;
  --line-strong: #3a3a3f;
  --shadow-soft: rgba(0, 0, 0, 0.3);
  --code-bg: #161618;

  color-scheme: dark;
}

/* ===== Light theme ===== */
[data-theme="light"] {
  --bg: #fafaf8;
  --bg-card: #ffffff;
  --bg-hover: #f0f0ee;
  --fg: #1a1a1d;
  --fg-muted: #5a5a63;
  --fg-soft: #9a9aa3;
  --accent: #a08930;
  --accent-hover: #8a7528;
  --line: #e5e5e0;
  --line-strong: #d0d0ca;
  --shadow-soft: rgba(0, 0, 0, 0.06);
  --code-bg: #f5f5f0;

  color-scheme: light;
}

@layer base {
  body {
    background-color: var(--bg);
    color: var(--fg);
    font-family: var(--font-sans);
    line-height: 1.75;
    transition:
      background-color 0.2s ease,
      color 0.2s ease;
  }
}

@layer components {
  /* --- Content cards --- */
  .content-card {
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: clamp(1rem, 2vw, 1.5rem);
    box-shadow: 0 1px 3px var(--shadow-soft);
    margin-bottom: 1.2rem;
  }

  /* --- Prose styles --- */
  .prose {
    color: var(--fg);
    max-width: none;
    font-family: var(--font-sans);
  }

  .prose h1,
  .prose h2,
  .prose h3,
  .prose h4 {
    color: var(--fg);
    font-family: var(--font-serif);
    font-weight: 600;
    scroll-margin-top: 5rem;
  }

  .prose h1 {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    margin-top: 2rem;
    margin-bottom: 1rem;
  }
  .prose h2 {
    font-size: clamp(1.2rem, 2.5vw, 1.5rem);
    margin-top: 0;
    margin-bottom: 0.75rem;
    border-bottom: none;
    padding-bottom: 0;
  }
  .prose h3 {
    font-size: clamp(1.05rem, 2vw, 1.2rem);
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
  }

  .prose strong {
    color: var(--fg);
  }
  .prose em {
    color: var(--fg-muted);
  }

  .prose a {
    color: var(--accent);
    text-decoration: none;
    text-underline-offset: 2px;
  }
  .prose a:hover {
    color: var(--accent-hover);
    text-decoration: underline;
  }

  .prose p {
    line-height: 1.75;
    margin-bottom: 1rem;
  }

  .prose ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }
  .prose ol {
    list-style-type: decimal;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }
  .prose li {
    line-height: 1.75;
    margin-bottom: 0.25rem;
  }

  .prose ul ul,
  .prose ol ul {
    list-style-type: circle;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
  }
  .prose ul ul ul {
    list-style-type: square;
  }

  .prose blockquote {
    border-left: 4px solid var(--accent);
    padding-left: 1rem;
    font-style: italic;
    color: var(--fg-muted);
    margin: 1rem 0;
  }

  .prose code:not(pre code) {
    background-color: var(--code-bg);
    color: var(--accent);
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    font-size: 0.875em;
    font-family: var(--font-mono);
  }

  .prose pre {
    background-color: var(--code-bg);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem;
    overflow-x: auto;
    margin: 1rem 0;
  }

  .prose pre code {
    background: transparent;
    color: var(--fg);
    padding: 0;
    font-size: 0.875rem;
    font-family: var(--font-mono);
  }

  .prose img {
    border-radius: 14px;
    border: 1px solid var(--line);
    margin: 1rem 0;
    max-width: 100%;
  }

  .prose table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.875rem;
  }

  .prose th {
    background-color: var(--bg-hover);
    color: var(--fg);
    font-weight: 600;
    padding: 0.5rem 0.75rem;
    text-align: left;
    border: 1px solid var(--line);
  }

  .prose td {
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--line);
    color: var(--fg);
  }

  .prose tr:nth-child(even) td {
    background-color: var(--bg-hover);
  }

  .prose hr {
    border-color: var(--line);
    margin: 2rem 0;
  }
}
```

- [ ] **Step 2: Verify build passes**

Run: `npm run build 2>&1 | tail -5`
Expected: `Complete!` with no errors.

- [ ] **Step 3: Commit**

```bash
git add src/styles/global.css
git commit -m "style: design system foundation — CSS vars, fonts, prose styles"
```

---

### Task 2: Logo, Favicon, and ThemeToggle Components

**Files:**

- Create: `src/components/Logo.astro`
- Create: `src/components/ThemeToggle.astro`
- Modify: `public/favicon.svg`

- [ ] **Step 1: Create Logo.astro**

Create `src/components/Logo.astro`:

```astro
---
import { BASE } from "../lib/base";
const { size = "default" } = Astro.props;
const iconSize = size === "large" ? "28" : "20";
---

<a href={`${BASE}/`} class={`logo logo--${size}`}>
  <svg
    width={iconSize}
    height={iconSize}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="logo-icon"
  >
    <polyline points="4 17 10 11 4 5"></polyline>
    <line x1="12" y1="19" x2="20" y2="19"></line>
  </svg>
  <span class="logo-text">DE Specialization</span>
</a>

<style>
  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: var(--fg);
    transition: color 0.15s ease;
  }

  .logo:hover {
    color: var(--accent);
  }

  .logo-icon {
    flex-shrink: 0;
    color: var(--accent);
  }

  .logo-text {
    font-family: var(--font-serif);
    font-weight: 600;
    line-height: 1.3;
  }

  .logo--default .logo-text {
    font-size: 0.9rem;
  }

  .logo--large .logo-text {
    font-size: clamp(1.5rem, 3vw, 2rem);
  }
</style>
```

- [ ] **Step 2: Create ThemeToggle.astro**

Create `src/components/ThemeToggle.astro`:

```astro
<button
  id="theme-toggle"
  class="theme-toggle"
  aria-label="Toggle dark/light mode"
  type="button"
>
  <svg
    class="icon-sun"
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <circle cx="12" cy="12" r="5"></circle>
    <line x1="12" y1="1" x2="12" y2="3"></line>
    <line x1="12" y1="21" x2="12" y2="23"></line>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
    <line x1="1" y1="12" x2="3" y2="12"></line>
    <line x1="21" y1="12" x2="23" y2="12"></line>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
  </svg>
  <svg
    class="icon-moon"
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
  </svg>
</button>

<style>
  .theme-toggle {
    background: none;
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--fg-muted);
    cursor: pointer;
    padding: 0.35rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition:
      color 0.15s ease,
      border-color 0.15s ease;
  }

  .theme-toggle:hover {
    color: var(--accent);
    border-color: var(--accent);
  }

  /* Dark mode: show sun (to switch to light), hide moon */
  :root:not([data-theme="light"]) .icon-moon {
    display: none;
  }
  :root:not([data-theme="light"]) .icon-sun {
    display: block;
  }

  /* Light mode: show moon (to switch to dark), hide sun */
  [data-theme="light"] .icon-sun {
    display: none;
  }
  [data-theme="light"] .icon-moon {
    display: block;
  }
</style>

<script>
  const toggle = document.getElementById("theme-toggle");
  toggle?.addEventListener("click", () => {
    const isLight =
      document.documentElement.getAttribute("data-theme") === "light";
    const next = isLight ? "dark" : "light";
    if (next === "light") {
      document.documentElement.setAttribute("data-theme", "light");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    localStorage.setItem("theme", next);
  });
</script>
```

- [ ] **Step 3: Update favicon.svg**

Replace `public/favicon.svg` with a matching terminal/bracket icon:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#c9a84c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="4 17 10 11 4 5"></polyline>
  <line x1="12" y1="19" x2="20" y2="19"></line>
</svg>
```

- [ ] **Step 4: Verify build passes**

Run: `npm run build 2>&1 | tail -5`
Expected: `Complete!` — new components don't need to be imported yet, just must not break build.

- [ ] **Step 5: Commit**

```bash
git add src/components/Logo.astro src/components/ThemeToggle.astro public/favicon.svg
git commit -m "feat: add Logo, ThemeToggle components and updated favicon"
```

---

### Task 3: Sidebar and TableOfContents Restyle

**Files:**

- Modify: `src/components/Sidebar.astro`
- Modify: `src/components/TableOfContents.astro`

- [ ] **Step 1: Rewrite Sidebar.astro**

Replace the entire contents of `src/components/Sidebar.astro`. The component keeps the same tree-building logic but adds:

- Imports for Logo and ThemeToggle components
- Emoji maps for courses and weeks (using Unicode escapes)
- CSS vars replacing all hardcoded `rgb()` colors
- Sidebar header with Logo + ThemeToggle + close button
- `var(--accent)` for active states instead of `sky-400`

Key changes from current file:

- Line 1-5 imports: add `Logo` and `ThemeToggle`
- New `courseEmojis` and `weekEmojis` Record maps after the type definitions
- Sidebar header: `<Logo />` and `<ThemeToggle />` replace the emoji + text link
- All `rgb(...)` color values in `<style>` replaced with `var(--*)` tokens
- `.note-link.active` uses `var(--accent)` instead of `rgb(56 189 248)`
- All `font-family` declarations use `var(--font-sans)`

Course emoji assignments:

- course-1: `\u{1F4CA}` (bar chart)
- course-2: `\u{1F50C}` (electric plug)
- course-3: `\u{1F5C4}` (file cabinet)
- course-4: `\u{2699}` (gear)

Week emoji assignments (15 weeks total — use contextual emojis like thinking face, refresh, construction, memo, link, inbox, gear, music, floppy, package, magnifying glass, triangular ruler, robot, lightning, satellite).

Full component code: see the Sidebar.astro rewrite in the spec's component section. The template structure is identical to current — only styling and header change.

- [ ] **Step 2: Rewrite TableOfContents.astro**

Replace all hardcoded `rgb()` values with CSS var equivalents:

- `rgb(113 113 122)` -> `var(--fg-soft)`
- `rgb(39 39 42)` -> `var(--line)`
- `rgb(212 212 216)` -> `var(--fg)`
- `rgb(56 189 248)` -> `var(--accent)`

Add `font-family: var(--font-sans)` to `.toc-title` and `.toc-link`.

The script and HTML template remain identical.

- [ ] **Step 3: Verify build passes**

Run: `npm run build 2>&1 | tail -5`
Expected: `Complete!`

- [ ] **Step 4: Commit**

```bash
git add src/components/Sidebar.astro src/components/TableOfContents.astro
git commit -m "style: restyle Sidebar and ToC with design system vars and emojis"
```

---

### Task 4: NoteLayout — Theme Script, Content Cards, Updated Styles

**Files:**

- Modify: `src/layouts/NoteLayout.astro`

- [ ] **Step 1: Rewrite NoteLayout.astro**

Key changes from current file:

**In `<head>`:** Add a blocking inline script that reads the saved theme from localStorage and sets `data-theme="light"` on `<html>` before paint. This prevents the flash of wrong theme:

```html
<script is:inline>
  (function () {
    var saved = localStorage.getItem("theme");
    if (saved === "light") {
      document.documentElement.setAttribute("data-theme", "light");
    } else if (
      !saved &&
      window.matchMedia("(prefers-color-scheme: light)").matches
    ) {
      document.documentElement.setAttribute("data-theme", "light");
    }
  })();
</script>
```

**Add content card wrapping script** before the closing `</body>`. This script uses safe DOM APIs (createElement, appendChild) — no innerHTML:

```html
<script>
  function wrapSectionsInCards() {
    const prose = document.getElementById("prose-content");
    if (!prose) return;

    const children = Array.from(prose.children);
    if (children.length === 0) return;

    const hasH2 = children.some(function (c) {
      return c.tagName === "H2";
    });
    if (!hasH2) return;

    const fragments = [];
    var current = [];

    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (child.tagName === "H2" && current.length > 0) {
        fragments.push(current);
        current = [];
      }
      current.push(child);
    }
    if (current.length > 0) fragments.push(current);

    while (prose.firstChild) prose.removeChild(prose.firstChild);

    for (var f = 0; f < fragments.length; f++) {
      var group = fragments[f];
      if (group[0].tagName !== "H2") {
        for (var j = 0; j < group.length; j++) prose.appendChild(group[j]);
        continue;
      }
      var card = document.createElement("div");
      card.className = "content-card";
      for (var k = 0; k < group.length; k++) card.appendChild(group[k]);
      prose.appendChild(card);
    }
  }

  wrapSectionsInCards();
</script>
```

**Add `id="prose-content"`** to the prose div: `<div class="prose" id="prose-content">`

**Update `<style>` block:** Replace all hardcoded `rgb()` values with CSS var tokens:

- All backgrounds: `var(--bg)`, `var(--bg-card)`, `var(--bg-hover)`
- All text colors: `var(--fg)`, `var(--fg-muted)`, `var(--fg-soft)`
- All borders: `var(--line)`, `var(--line-strong)`
- Active/accent: `var(--accent)`
- Shadows: `var(--shadow-soft)`

**Update typography:**

- `.page-title`: add `font-family: var(--font-serif)`, use `clamp(1.8rem, 4vw, 2.5rem)`
- `.breadcrumb-course`: add `font-family: var(--font-serif)`
- `.breadcrumb-week`: add `font-family: var(--font-sans)`
- `.mobile-title`: add `font-family: var(--font-serif)`
- `.page-nav-title`: add `font-family: var(--font-serif)`
- `.page-nav-label`: add `font-family: var(--font-sans)`

**Update nav card styles:**

- `.page-nav-link`: background `var(--bg-card)`, border-radius `14px`, hover adds `translateY(-3px)` + `var(--accent)` border + `var(--shadow-soft)`

- [ ] **Step 2: Verify build passes**

Run: `npm run build 2>&1 | tail -5`
Expected: `Complete!`

- [ ] **Step 3: Start dev server and visually verify**

Run: `npx astro dev`

Check:

- Dark mode loads by default (no flash)
- Theme toggle in sidebar switches between dark/light
- Serif headings (Lora) render on page titles and `##` headings
- Content sections are wrapped in cards with subtle borders
- Sidebar has emoji prefixes and gold accent active state
- Prev/next nav uses card styling
- All three breakpoints work (resize browser)

- [ ] **Step 4: Commit**

```bash
git add src/layouts/NoteLayout.astro
git commit -m "feat: NoteLayout with theme script, content cards, and design system"
```

---

### Task 5: Home Page Redesign

**Files:**

- Modify: `src/pages/index.astro`

- [ ] **Step 1: Rewrite index.astro**

Replace the entire file. Key structure:

**Frontmatter:** Import `global.css`, `BASE`, `getCollection`, `Logo`, `ThemeToggle`. Build a `getCourseStats()` function that counts weeks and sections per course from the notes collection. Define 4 course objects with emoji, title, description, href (to first section of each course), and stats.

**Template:**

1. Theme script in `<head>` (same as NoteLayout — prevents flash)
2. `.home` wrapper div: `max-width: 760px`, centered, flex column
3. `.home-topbar`: Logo left, ThemeToggle right, border-bottom
4. `.home-hero`: centered `<h1>` in Lora + subtitle `<p>` in Inter muted
5. `.home-search`: placeholder div (replaced with Pagefind in Task 6). Uses a search icon SVG + "Search notes..." text, styled as a rounded input-like container
6. `.home-courses`: 2x2 grid of course cards. Each card is an `<a>` with: emoji + "Course N" badge, Lora title, Inter description, "N weeks . M sections" meta line. Hover: translateY(-3px) + accent border + shadow
7. `.home-footer`: minimal, border-top, "Built with Astro" text

**Styles:** All using CSS vars. Cards have `border-radius: 14px`, `var(--bg-card)` background. Grid collapses to single column at 640px.

Course href values — update to point to the correct first section file for each course:

- Course 1: `.../week-1-.../11-how-to-think-like-a-data-engineer/`
- Course 2: `.../week-1-.../11-introduction-to-source-systems/`
- Course 3: `.../week-1-.../11-storage-fundamentals/`
- Course 4: `.../week-1-.../11-data-modeling-fundamentals/`

- [ ] **Step 2: Verify build passes**

Run: `npm run build 2>&1 | tail -5`
Expected: `Complete!`

- [ ] **Step 3: Start dev server and visually verify home page**

Run: `npx astro dev`

Check at the root URL:

- Logo + theme toggle in top bar
- Serif hero title centered
- Search placeholder present (functional search in Task 6)
- 4 course cards in 2x2 grid with correct emoji, titles, week/section counts
- Cards lift on hover with gold border
- Footer at bottom
- Mobile: single column cards
- Light mode toggle works

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: redesign home page with hero, course cards, and search placeholder"
```

---

### Task 6: Pagefind Search Integration

**Files:**

- Modify: `package.json`
- Create: `src/components/SearchBar.astro`
- Modify: `src/pages/index.astro` (replace search placeholder)

- [ ] **Step 1: Install Pagefind**

Run: `npm install --save-dev pagefind`

- [ ] **Step 2: Update build script in package.json**

In `package.json`, change:

```json
"build": "astro build"
```

to:

```json
"build": "astro build && npx pagefind --site dist --glob '**/*.html'"
```

- [ ] **Step 3: Create SearchBar.astro**

Create `src/components/SearchBar.astro`. This component:

- Renders a `<div id="search">` container
- Has global styles overriding Pagefind UI defaults to match the design system (all using CSS vars)
- Has a `<script>` that dynamically imports `/pagefind/pagefind-ui.js` (generated at build time)
- In dev mode (where Pagefind index doesn't exist), catches the import error and renders a static placeholder using safe DOM APIs (createElement, textContent — no innerHTML)

Key Pagefind UI style overrides:

- `.pagefind-ui__search-input`: `var(--bg-card)` background, `var(--fg)` color, `var(--line)` border, `border-radius: 10px`, focus border `var(--accent)`
- `.pagefind-ui__result-link`: `var(--accent)` color, `var(--font-serif)` font
- `.pagefind-ui__result-excerpt`: `var(--fg-muted)` color
- `.pagefind-ui__result`: `var(--line)` border-top
- `mark`: `var(--accent)` color, transparent background, bold

- [ ] **Step 4: Update index.astro to use SearchBar**

In `src/pages/index.astro`:

- Add import: `import SearchBar from "../components/SearchBar.astro";`
- Replace the static search placeholder div with: `<div class="home-search"><SearchBar /></div>`

- [ ] **Step 5: Run full build and verify Pagefind indexes**

Run: `npm run build 2>&1 | tail -15`

Expected output includes:

- Astro build completes
- Pagefind output like: `Running Pagefind... Indexed N pages`

- [ ] **Step 6: Preview built site and test search**

Run: `npm run preview`

At the root URL:

- Search bar renders with Pagefind UI
- Type a term (e.g., "Spark") — results appear with page title and text excerpt
- Click a result — navigates to the correct note page
- Results highlight search terms in gold (accent color)

- [ ] **Step 7: Commit**

```bash
git add package.json src/components/SearchBar.astro src/pages/index.astro
git commit -m "feat: integrate Pagefind full-text search with styled UI"
```

---

### Task 7: Final Polish and Verification

**Files:**

- Various — checking all existing content renders correctly

- [ ] **Step 1: Full build check**

Run: `npm run build 2>&1 | tail -10`
Expected: `Complete!` with all 46+ pages built and Pagefind indexing.

- [ ] **Step 2: Visual verification checklist**

Run: `npm run preview`

Open the site and verify each item:

- [ ] Home page: logo, hero title in Lora, search bar, 4 course cards in 2x2 grid
- [ ] Home page: cards show correct emoji, week/section counts, hover lift effect
- [ ] Home page: theme toggle works (dark to light and back), no flash on reload
- [ ] Note page: sidebar with emoji prefixes, gold active state
- [ ] Note page: page title in Lora serif
- [ ] Note page: content wrapped in cards per `##` section
- [ ] Note page: code blocks render with JetBrains Mono in `--code-bg`
- [ ] Note page: images display correctly with rounded borders
- [ ] Note page: tables render with proper borders and alternating rows
- [ ] Note page: prev/next cards with hover lift
- [ ] Note page: ToC on right with gold active state
- [ ] Note page: breadcrumb shows course (serif) and week (sans)
- [ ] Light mode: all of the above renders correctly with light palette
- [ ] Mobile (resize below 768px): slide-out sidebar, no ToC, full-width cards
- [ ] Search: type "Spark" on home page, results appear, click navigates correctly
- [ ] No blue (sky-400, rgb(56 189 248), rgb(14 165 233)) visible anywhere

- [ ] **Step 3: Commit any remaining fixes**

```bash
git add -A
git commit -m "style: final polish and verification of design redesign"
```
