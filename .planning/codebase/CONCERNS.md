# Technical Debt and Concerns

## Priority 1 -- Bugs and Correctness

### Node version mismatch between CI and local

`package.json` declares `"engines": { "node": ">=22.12.0" }` but the GitHub Actions deploy workflow (`.github/workflows/deploy.yml`) uses `node-version: 20`. The build runs on a Node version the project explicitly says it does not support. Either lower the engines requirement or bump the CI to Node 22.

### Duplicate Cmd/Ctrl+K keyboard shortcut handlers

Both `src/components/SearchBar.astro` (line 184) and `src/components/SearchModal.astro` (line 378) register global `keydown` listeners for Cmd/Ctrl+K. On note pages the Sidebar includes SearchModal while the home/glossary pages use SearchBar inline -- but if both components ever coexist on a page, the handler fires twice. Even today the two handlers do slightly different things (one focuses input, the other toggles a dialog), creating unpredictable behavior if the architecture changes.

### `detailSection` element is dead code in the glossary

`src/pages/glossary.astro` line 179 renders `<section id="detail-section">` and the script references it (line 279), but the section is only ever hidden -- it is never shown. All term detail now goes to `detailModal`. The HTML element, its CSS rule (`.detail-section { display: none; }` line 982), and the three JS lines that add `hidden` to it are dead code left over from a layout refactor.

### Duplicate `.prose h1` declarations in global CSS

`src/styles/global.css` defines `.prose h1` at both line 167 (font properties) and line 183 (sizing/margin). The second block silently overrides/extends the first. They should be merged into one rule.

## Priority 2 -- Security and Deprecation

### Pagefind excerpts set via element.innerHTML

`src/lib/search-ui.ts` line 41 sets `excerpt.innerHTML = result.excerpt`. A comment in the code notes the content comes from Pagefind's build-time index and only contains `<mark>` tags, which is correct today. However, any future change to how excerpts are generated could introduce an XSS vector. Worth noting but low risk given the static-site context.

### `navigator.platform` is deprecated

`src/lib/search-ui.ts` line 106 uses `navigator.platform` to detect Mac for shortcut display. This API is deprecated in modern browsers. Replace with `navigator.userAgentData?.platform` (with fallback) or `navigator.userAgent`.

### Custom `.env` parser in fetch-notion script

`scripts/fetch-notion.mjs` lines 24-30 implement a hand-rolled `.env` parser that splits on `=` and trims. It does not handle quoting, comments, multiline values, or `export` prefixes. Consider using `dotenv` or Node's built-in `--env-file` flag (Node 20.6+).

## Priority 3 -- Architecture and Maintainability

### Theme initialization script duplicated three times

The inline `<script>` that reads `localStorage.getItem("theme")` and sets `data-theme` is copy-pasted identically in three files:

- `src/layouts/NoteLayout.astro` (line 23-35)
- `src/pages/index.astro` (line 64-76)
- `src/pages/glossary.astro` (line 52-64)

Extract to a shared inline snippet or a `<ThemeInit />` component.

### Hardcoded base path in fetch-notion.mjs

`scripts/fetch-notion.mjs` line 167 hardcodes the image base path as `"/data-engineering-specialization/images"`. This must be kept in sync with `base` in `astro.config.mjs`. If the base path changes, all fetched content will have broken image URLs. Consider reading the base from the Astro config or a shared constant.

### Hardcoded Notion root page ID

`scripts/fetch-notion.mjs` line 40 hardcodes `ROOT_PAGE_ID = "139969a7aa018017b81fc3858c54fc8f"`. This should be an environment variable or CLI argument.

### Hardcoded emoji maps in Sidebar

`src/components/Sidebar.astro` lines 30-53 map course and week slugs to emojis using hardcoded `Record` objects. Adding a new course or week requires editing this component. Consider moving these to the content schema or a data file.

### `glossary.json` is a 3,159-line manually maintained data file

`src/data/glossary.json` is hand-maintained with term definitions, descriptions, related terms, and note slug references. The build-time validation in `src/pages/glossary.astro` (lines 14-24) catches invalid slugs, which is good, but there is no validation for orphaned `relatedTerms` (terms that reference names not present in the dataset).

### Large inline `<script>` block in glossary page

`src/pages/glossary.astro` contains approximately 350 lines of inline TypeScript (lines 251-608) for glossary interactivity. This is the largest script block in the codebase and mixes state management, DOM manipulation, event handling, and pagination logic. The pure-logic parts were extracted to `glossary-data.ts`, `glossary-pagination.ts`, and `glossary-detail.ts`, but the orchestration/wiring remains monolithic and difficult to test.

### Non-null assertions in glossary script

The glossary page script uses the `!` non-null assertion operator extensively (e.g., `document.getElementById("terms-pills")!`). If the HTML structure changes but the script is not updated, these will throw at runtime with unhelpful errors rather than failing gracefully.

### Hardcoded `rgba()` values for shadows and overlays

Multiple components use raw `rgba(0, 0, 0, ...)` for shadows and backdrop overlays instead of CSS custom properties. Found in `SearchBar.astro`, `SearchModal.astro`, `NoteLayout.astro`, and `glossary.astro`. These do not adapt to the current theme and would need to be updated individually if the design system changes.

### `!important` overrides in CSS

11 total `!important` declarations across `global.css` (3), `SearchModal.astro` (8), and `LogoMarquee.astro` (1). The SearchModal ones (line 160-165) are used to override inherited `.search-input` styles, which suggests the base styles are too broadly scoped.

## Priority 4 -- Missing Features and Coverage

### No CI lint/test step

`.github/workflows/deploy.yml` only runs `npm ci`, fetches Notion content, and builds. It does not run `npm run lint`, `npm run typecheck`, or `npm run test:run`. Broken lint or type errors could be deployed.

### No tests for UI components or search

Unit tests exist only for `glossary-data.ts` and `glossary-pagination.ts`. There are no tests for:

- `search-engine.ts` (Pagefind integration)
- `search-ui.ts` (DOM rendering, keyboard navigation)
- `glossary-detail.ts` (detail card builder)
- Any Astro component behavior

### No OpenGraph/Twitter meta tags

None of the three page templates (`index.astro`, `NoteLayout.astro`, `glossary.astro`) include `og:title`, `og:description`, `og:image`, or `twitter:card` meta tags. Links shared on social media will have poor previews.

### No 404 page

There is no `src/pages/404.astro`. GitHub Pages will show a generic 404 for invalid URLs.

### No sitemap

No `@astrojs/sitemap` integration. The site has 45+ pages that would benefit from search engine discoverability.

### Content and images are gitignored

`.gitignore` includes both `src/content/notes/` and `public/images/`. All content is regenerated from Notion at build time. This means:

- Local development requires a valid `NOTION_TOKEN` and network access
- Content changes made directly to markdown files (e.g., diagram embeds, Mermaid components) are not tracked in git and will be overwritten on next fetch
- The `.mdx` file at `course-4/.../12-normalization.mdx` (the only `.mdx` file) is presumably manually maintained but would be lost on a clean clone + fetch

### Unused `getPageTitle` function

`scripts/fetch-notion.mjs` line 107 defines `getPageTitle()` which is never called (only defined). It is also marked with `eslint-disable-next-line @typescript-eslint/no-unused-vars`.

### Potentially unused devDependencies

- `roughjs` -- not imported anywhere in `src/` or `scripts/`
- `node-fetch` -- not imported anywhere (Node 22 has native fetch)
- `jsdom` -- not imported in any test or source file (may be needed by vitest but is not configured as the test environment)

### Empty CSS rule

`src/components/Sidebar.astro` line 308 has an empty `.week-details { }` rule block.

## Priority 5 -- Performance Observations

### Google Fonts loaded from CDN with no preconnect

`src/styles/global.css` line 4 imports three font families (Poppins, Lora, JetBrains Mono) from Google Fonts via `@import url(...)`. This is a render-blocking request with no `<link rel="preconnect">` hint. Consider self-hosting fonts or adding preconnect tags.

### Mermaid re-renders entire page on theme toggle

`src/components/Mermaid.astro` line 55 creates a `MutationObserver` that calls `renderMermaid()` whenever `data-theme` changes. This re-renders all Mermaid diagrams on the page, which can cause a visible flash. For a single `.mdx` page this is acceptable, but worth noting.

### All marquee logos load eagerly despite `loading="lazy"`

`src/components/LogoMarquee.astro` correctly sets `loading="lazy"` on images, but since all logos are above the fold in the hero section, the browser will load them all eagerly anyway. The `lazy` attribute has no effect here.
