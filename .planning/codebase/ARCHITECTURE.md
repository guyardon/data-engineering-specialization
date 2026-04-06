# Architecture

## Pattern

**Static Site Generation (SSG)** using Astro 6 as the core framework, deployed to GitHub Pages. The site is a Multi-Page Application (MPA) where every page is pre-rendered at build time. There is no client-side routing or SPA behavior.

The project is a **dual-language monorepo**: the website itself is TypeScript/Astro, while diagram generation is Python. Both codebases live in the same repository with separate dependency management (`package.json` for Node, `pyproject.toml` + `uv.lock` for Python).

## Layers

### 1. Content Layer (Notion -> Markdown)

Content originates in a Notion workspace and is synced to the repo via `scripts/fetch-notion.mjs`. This script:

- Connects to Notion API using `@notionhq/client`
- Walks a page tree starting from root page `139969a7aa018017b81fc3858c54fc8f`
- Generates `.md` / `.mdx` files into `src/content/notes/`
- Downloads images into `public/images/`

The generated content files are **gitignored** (`src/content/notes/` and `public/images/` are in `.gitignore`) -- they are regenerated in CI. However, diagram outputs in `public/images/diagrams/` and logos in `public/images/logos/` are committed.

### 2. Content Collection Layer (Astro)

Astro's content collection system (`src/content.config.ts`) defines a `notes` collection using a glob loader:

```
loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/notes" })
```

Each note has a Zod-validated frontmatter schema:

- `title`, `course`, `courseSlug`, `courseOrder` -- identifies the course
- `week`, `weekSlug`, `weekOrder` -- identifies the week within a course
- `order` -- section ordering within a week
- `notionId` (optional) -- back-reference to Notion source

The content is organized as: `course-slug/week-slug/XX-section-slug.md` where `XX` is the two-digit order number (e.g., `11`, `12`, `21`).

### 3. Page Generation Layer

Two routing strategies:

- **Dynamic route**: `src/pages/notes/[...slug].astro` -- uses `getStaticPaths()` to generate one page per note. Sorts all notes by `courseOrder > weekOrder > order` and passes prev/next navigation props.
- **Static pages**: `src/pages/index.astro` (home), `src/pages/glossary.astro` (interactive glossary)

### 4. Layout & Component Layer

Single layout: `src/layouts/NoteLayout.astro` -- wraps every note page with sidebar navigation, table of contents, breadcrumbs (course/week), prev/next links, theme toggle, and search.

Components (`src/components/`):

- `Sidebar.astro` -- collapsible course/week/section navigation tree with search
- `TableOfContents.astro` -- auto-generated from heading hierarchy
- `ThemeToggle.astro` -- dark/light theme switcher using `data-theme` attribute on `<html>`
- `SearchBar.astro` -- Pagefind-powered search input with dropdown results
- `SearchModal.astro` -- modal overlay variant of search
- `Mermaid.astro` -- client-side Mermaid diagram renderer (for ER diagrams)
- `Logo.astro` -- site logo component
- `LogoMarquee.astro` -- scrolling tech logo showcase on home page

### 5. Styling Layer

- `src/styles/global.css` -- single CSS file with CSS custom properties for theming
- Tailwind CSS 4 loaded via Vite plugin (`@tailwindcss/vite`)
- Dark theme is default (`:root`), light theme via `[data-theme="light"]`
- Gold accent color: `#c9a84c` (dark) / `#a08930` (light)
- Font stack: Lora (serif headings), Poppins (sans body), JetBrains Mono (code)
- Code highlighting: Shiki with dual themes (`light-plus` / `dark-plus`)

### 6. Diagram Generation Layer (Python)

Two separate pipelines produce diagram assets:

**Excalidraw diagrams** (conceptual/teaching):

- Python scripts in `diagrams/scripts/generate-*.py` use `diagramlib.ExcalidrawDiagram` to programmatically build `.excalidraw` JSON
- Output: `diagrams/artifacts/*.excalidraw`
- External CLI tool `excalidraw-brute-export-cli` exports to SVG with both `--dark-mode 0` and `--dark-mode 1`
- Final output: `public/images/diagrams/*.svg` and `*-dark.svg`

**AWS architecture diagrams** (cloud infrastructure):

- Python scripts use the `diagrams` library (Graphviz-based) with helpers from `diagramlib.aws_diagram`
- Produce both light and dark PNGs directly
- Final output: `public/images/diagrams/*.png` and `*-dark.png`

**Shared library** (`diagrams/diagramlib/`):

- `colors.py` -- color palette constants (stroke, background tuples)
- `excalidraw.py` -- `ExcalidrawDiagram` class for building Excalidraw JSON documents
- `aws_diagram.py` -- standardized graph/node/edge/cluster attribute helpers for the `diagrams` library

### 7. Client-Side Libraries

Minimal JS on the client:

- **Mermaid** (`mermaid` npm package) -- renders ER diagrams client-side, theme-aware
- **Pagefind** -- build-time search indexing (`npx pagefind --site dist`), client-side search UI via IIFE script

### 8. Data Layer

- `src/data/glossary.json` -- large (160KB) JSON file containing categorized glossary terms with descriptions, related terms, diagram references, and note cross-references
- `src/lib/glossary-data.ts` -- pure data query functions for the glossary (building term lists, searching, random pick)
- `src/lib/glossary-detail.ts` -- detail view logic for glossary modal
- `src/lib/glossary-pagination.ts` -- pagination logic for term lists
- `src/lib/search-engine.ts` / `search-ui.ts` -- search integration code
- `src/lib/base.ts` -- exports `BASE` constant (resolved from `import.meta.env.BASE_URL`)

## Data Flow

```
Notion Workspace
      |
      v  (scripts/fetch-notion.mjs)
src/content/notes/**/*.md     public/images/ (downloaded)
      |
      v  (Astro content collection + glob loader)
Content Collection (Zod-validated frontmatter)
      |
      v  (getStaticPaths in [...slug].astro)
Static HTML pages (one per note)
      |
      v  (npm run build = astro build)
dist/                         (static HTML/CSS/JS)
      |
      v  (npx pagefind --site dist)
dist/_pagefind/               (search index)
      |
      v  (GitHub Actions deploy.yml)
GitHub Pages (guyardon.github.io/data-engineering-specialization-website)
```

Diagram generation is a separate offline pipeline:

```
diagrams/scripts/generate-*.py
      |
      v  (Python: diagramlib helpers)
diagrams/artifacts/*.excalidraw    (Excalidraw JSON)
      |
      v  (excalidraw-brute-export-cli)
public/images/diagrams/*.svg       (light + dark SVGs)

diagrams/scripts/generate-*-aws.py
      |
      v  (Python: diagrams library + diagramlib.aws_diagram)
public/images/diagrams/*.png       (light + dark PNGs)
```

## Key Abstractions

### Base Path

All asset references must include `/data-engineering-specialization-website` prefix because the site is deployed to a subdirectory on GitHub Pages. The `BASE` constant from `src/lib/base.ts` provides this at build time.

### Theme System

Dark-first design using `data-theme` attribute on `<html>`:

- CSS custom properties swap all colors
- Diagrams use paired `diagram-dark` / `diagram-light` CSS classes to show/hide the correct variant
- Mermaid auto-switches via `data-theme` observer
- An inline script in `<head>` reads `localStorage` before paint to prevent flash

### Content Ordering

The three-tier ordering system (`courseOrder` > `weekOrder` > `order`) determines both navigation structure and prev/next links. The sidebar builds its tree from this hierarchy.

## Entry Points

| Purpose         | File                              |
| --------------- | --------------------------------- |
| Astro config    | `astro.config.mjs`                |
| Content schema  | `src/content.config.ts`           |
| Home page       | `src/pages/index.astro`           |
| Note pages      | `src/pages/notes/[...slug].astro` |
| Glossary page   | `src/pages/glossary.astro`        |
| Note layout     | `src/layouts/NoteLayout.astro`    |
| Global styles   | `src/styles/global.css`           |
| Notion sync     | `scripts/fetch-notion.mjs`        |
| CI/CD           | `.github/workflows/deploy.yml`    |
| Diagram library | `diagrams/diagramlib/__init__.py` |

## Build Pipeline

1. `node scripts/fetch-notion.mjs` -- sync content from Notion (CI only; local content is pre-existing)
2. `astro build` -- compile Astro pages, process markdown, bundle CSS/JS into `dist/`
3. `npx pagefind --site dist --glob '**/*.html'` -- index all HTML for search
4. Deploy `dist/` to GitHub Pages via `actions/deploy-pages@v4`

## Quality Tooling

Pre-commit hooks (`.pre-commit-config.yaml`) run:

- **Python**: ruff (lint + format), mypy (type checking on `diagrams/diagramlib/`), pytest
- **JS/TS**: ESLint, Prettier, Vitest

Testing:

- `tests/` -- Python tests for `diagramlib` (pytest)
- `src/lib/*.test.ts` -- TypeScript tests co-located with source (Vitest)
