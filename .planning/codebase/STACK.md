# Technology Stack

**Analysis Date:** 2026-03-31

## Languages

**Primary:**
- TypeScript (strict mode) - Configuration files, build setup, and type definitions
- JavaScript/ESM - Node.js scripts and Astro configuration

**Secondary:**
- MDX - Content files for notes (generated from Notion)
- Markdown - Manual content and documentation

## Runtime

**Environment:**
- Node.js 22.12.0 or higher (specified in `package.json` engines field)

**Package Manager:**
- npm
- Lockfile: `package-lock.json` present

## Frameworks

**Core:**
- Astro 6.1.2 - Static site generation and content collection framework
  - Config: `astro.config.mjs`
  - Output mode: Static HTML (no server runtime)

**Content Processing:**
- @astrojs/mdx 5.0.3 - MDX support for content integration
- remark-gfm 4.0.1 - GitHub Flavored Markdown plugin (tables, strikethrough, etc.)

**Styling:**
- TailwindCSS 4.2.2 - Utility-first CSS framework
- @tailwindcss/vite 4.2.2 - Vite plugin for TailwindCSS

## Key Dependencies

**Critical:**
- @notionhq/client 5.16.0 - Notion SDK for fetching content
  - Used in: `scripts/fetch-notion.mjs`
  - Purpose: Pulls course notes and markdown content from Notion database

**Utilities:**
- node-fetch 3.3.2 - Polyfill for fetch API in Node.js
  - Used in: `scripts/fetch-notion.mjs` for downloading images
- zod 4.3.6 - TypeScript-first schema validation
  - Used in: `src/content.config.ts` for content collection schema validation

## Configuration

**Environment:**
- Requires: `NOTION_TOKEN` environment variable (Notion API authentication token)
- Configuration location: `.env` or `.env.example`
- Purpose: Authenticate requests to Notion API when running `fetch-notion.mjs`

**Build:**
- TypeScript strict mode configuration in `tsconfig.json`
  - Extends: Astro's strict configuration preset
  - Includes: `.astro/types.d.ts` and all files
  - Excludes: `dist` directory

- Astro configuration in `astro.config.mjs`:
  - Base path: `/data-engineering-specialization-website` (GitHub Pages sub-path)
  - Site URL: `https://guyardon.github.io`
  - Static output mode
  - Markdown syntax highlighting: GitHub dark theme (Shiki)

## Platform Requirements

**Development:**
- Node.js >= 22.12.0
- npm (or compatible package manager)
- MacOS/Linux/Windows with standard shell

**Production:**
- Deployment target: GitHub Pages (static hosting)
- Output directory: `dist/`
- Build command: `npm run build`
- Preview command: `npm run preview`

## Development Scripts

```bash
npm run dev       # Start local development server (Astro dev)
npm run build     # Build static site (output to dist/)
npm run preview   # Preview built site locally
npm run astro     # Run Astro CLI directly
```

Note: `fetch-notion.mjs` is run manually with: `NOTION_TOKEN=<token> node scripts/fetch-notion.mjs`

---

*Stack analysis: 2026-03-31*
