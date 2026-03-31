# Directory Structure

**Analysis Date:** 2026-03-31

## Top-Level Layout

```
data-engineering-specialization-website/
├── .astro/                    # Auto-generated Astro internals (do not edit)
├── .github/workflows/         # CI/CD — deploy.yml for GitHub Pages
├── .planning/                 # GSD planning directory
├── dist/                      # Build output (gitignored)
├── node_modules/              # Dependencies (gitignored)
├── public/                    # Static assets served as-is
│   └── images/                # Notion images downloaded by fetch script
├── scripts/                   # One-off scripts (not part of build)
│   └── fetch-notion.mjs       # Content ingestion from Notion
├── src/                       # Application source
│   ├── components/            # Reusable Astro components
│   │   ├── Sidebar.astro
│   │   └── TableOfContents.astro
│   ├── content/               # Content collections (generated)
│   │   └── notes/             # Markdown notes from Notion
│   │       └── [courseSlug]/[weekSlug]/[section].md
│   ├── layouts/               # Page layout wrappers
│   │   └── NoteLayout.astro
│   ├── lib/                   # Shared utilities
│   │   └── base.ts            # BASE path constant
│   ├── pages/                 # File-based routing
│   │   ├── index.astro        # Redirect to first note
│   │   └── notes/             # Note pages (dynamic routes)
│   ├── styles/                # Global CSS
│   └── content.config.ts      # Content collection schema (Zod)
├── astro.config.mjs           # Astro configuration
├── tsconfig.json              # TypeScript configuration
├── package.json               # Dependencies and scripts
└── .env / .env.example        # Environment variables
```

## Key Locations

| Purpose | Path |
|---------|------|
| Astro config | `astro.config.mjs` |
| Content schema | `src/content.config.ts` |
| Notion fetch script | `scripts/fetch-notion.mjs` |
| BASE path utility | `src/lib/base.ts` |
| Generated notes | `src/content/notes/` |
| Downloaded images | `public/images/` |
| GitHub Pages deploy | `.github/workflows/deploy.yml` |

## Naming Conventions
- Components: PascalCase `.astro` (e.g. `Sidebar.astro`)
- Scripts: camelCase `.mjs` (e.g. `fetch-notion.mjs`)
- Content files: kebab-case `.md`
- Route segments: kebab-case slugs
