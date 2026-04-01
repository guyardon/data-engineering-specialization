# Technical Concerns

**Analysis Date:** 2026-03-31

## Tech Debt

### No Test Coverage

- Zero test infrastructure (no Vitest, no Playwright, no Jest)
- No test scripts in `package.json`
- Risk: regressions during development go undetected
- Fix: set up Vitest + Playwright as part of early phases

### Manual Content Sync

- `scripts/fetch-notion.mjs` must be run manually before builds
- No automation hooks or CI integration for content refresh
- Risk: stale content deployed if developer forgets to run script
- Fix: add content sync step to GitHub Actions workflow

### No Linting / Formatting

- No `.eslintrc`, `.prettierrc`, or similar config detected
- Risk: inconsistent code style as project grows
- Fix: add ESLint + Prettier with Astro plugin

## Security

### NOTION_TOKEN in .env

- `.env` contains Notion API token — must never be committed
- `.gitignore` should exclude `.env` (standard, likely present)
- GitHub Actions must use repository secrets, not hardcoded values

### No Input Sanitization

- Content comes from Notion (trusted source), so low risk
- Markdown is rendered by Astro (safe), not raw HTML injection

## Performance

### Images Not Optimized

- Images downloaded from Notion stored in `public/images/` as-is
- Astro's `<Image>` component with optimization not used
- Risk: large images slow page loads
- Fix: use Astro image optimization or a CDN

### No Asset Hashing

- Depends on Astro default behavior — likely fine for static builds

## Fragile Areas

### Notion API Dependency

- Content pipeline entirely dependent on Notion structure
- If Notion page hierarchy changes, `fetch-notion.mjs` breaks
- No error recovery or partial-sync support

### Base Path Configuration

- `BASE` constant in `src/lib/base.ts` + `astro.config.mjs` base path must stay in sync
- Mismatch causes broken links in production (GitHub Pages sub-path)

### Generated Content in Source

- `src/content/notes/` contains generated files mixed into `src/`
- These may be committed to git, causing noise in diffs
- Consider: document whether `src/content/notes/` is gitignored or not

## Scaling Limits

- Static site — scales infinitely for reads
- Large Notion databases may slow `fetch-notion.mjs` significantly
- No pagination or incremental sync in fetch script
