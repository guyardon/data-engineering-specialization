# Tech Stack

## Languages & Runtimes

| Language       | Version               | Usage                                            |
| -------------- | --------------------- | ------------------------------------------------ |
| TypeScript     | 5.9.3                 | Astro components, lib modules, config, tests     |
| JavaScript     | ES Modules            | Node scripts (`fetch-notion.mjs`), ESLint config |
| Python         | >= 3.13               | Diagram generation scripts, diagramlib package   |
| CSS            | Tailwind v4 + vanilla | Global styles, component-scoped styles           |
| HTML           | —                     | Astro templates                                  |
| Markdown / MDX | —                     | Content collection (course notes)                |

### Runtime requirements

- **Node.js >= 22.12.0** — enforced via `engines` in `package.json`
- **Python >= 3.13** — enforced via `requires-python` in `pyproject.toml`

---

## Frameworks & Core Libraries

### Frontend / Site Generator

| Package             | Version (locked) | Purpose                                                            |
| ------------------- | ---------------- | ------------------------------------------------------------------ |
| `astro`             | 6.1.2            | Static site generator (SSG mode, `output: "static"`)               |
| `@astrojs/mdx`      | ^5.0.3           | MDX integration — allows component imports in `.mdx` content files |
| `tailwindcss`       | 4.2.2            | Utility-first CSS framework (via Vite plugin)                      |
| `@tailwindcss/vite` | ^4.2.2           | Tailwind CSS Vite plugin integration                               |
| `mermaid`           | 11.14.0          | Client-side ER diagrams / data modeling charts                     |
| `zod`               | 4.3.6            | Schema validation for Astro content collections                    |

### Python Diagram Libraries

| Package    | Version (locked) | Purpose                                                                     |
| ---------- | ---------------- | --------------------------------------------------------------------------- |
| `diagrams` | 0.25.1           | AWS/cloud architecture diagram generation (depends on `graphviz`, `jinja2`) |

The project also has a custom `diagramlib` package at `diagrams/diagramlib/` with three modules:

- `aws_diagram.py` — standardized graph/node/edge/cluster attribute helpers for the `diagrams` library
- `excalidraw.py` — `ExcalidrawDiagram` class that builds `.excalidraw` JSON files programmatically
- `colors.py` — shared color palette constants (stroke, background tuples)

---

## Dependencies (JavaScript / npm)

### Production Dependencies

| Package             | Spec     | Locked  | Purpose                                     |
| ------------------- | -------- | ------- | ------------------------------------------- |
| `astro`             | ^6.1.2   | 6.1.2   | Static site framework                       |
| `@astrojs/mdx`      | ^5.0.3   | —       | MDX support for content collections         |
| `@tailwindcss/vite` | ^4.2.2   | —       | Tailwind CSS Vite plugin                    |
| `tailwindcss`       | ^4.2.2   | 4.2.2   | CSS framework                               |
| `mermaid`           | ^11.14.0 | 11.14.0 | Client-side diagram rendering (ER diagrams) |

### Dev Dependencies

| Package                            | Spec    | Locked | Purpose                                          |
| ---------------------------------- | ------- | ------ | ------------------------------------------------ |
| `@astrojs/check`                   | ^0.9.8  | —      | Astro type checking (`astro check`)              |
| `typescript`                       | ^5.9.3  | 5.9.3  | TypeScript compiler                              |
| `vitest`                           | ^4.1.2  | 4.1.2  | Unit test runner                                 |
| `jsdom`                            | ^29.0.1 | —      | DOM environment for tests                        |
| `eslint`                           | ^10.1.0 | —      | JavaScript/TypeScript linter                     |
| `@eslint/js`                       | ^10.0.1 | —      | ESLint core JS recommended rules                 |
| `@typescript-eslint/eslint-plugin` | ^8.58.0 | —      | TypeScript-specific ESLint rules                 |
| `@typescript-eslint/parser`        | ^8.58.0 | —      | TypeScript parser for ESLint                     |
| `typescript-eslint`                | ^8.58.0 | —      | Unified typescript-eslint config                 |
| `eslint-plugin-astro`              | ^1.6.0  | —      | ESLint rules for `.astro` files                  |
| `eslint-plugin-prettier`           | ^5.5.5  | —      | Run Prettier as an ESLint rule                   |
| `eslint-config-prettier`           | ^10.1.8 | —      | Disable ESLint rules that conflict with Prettier |
| `globals`                          | ^17.4.0 | —      | Global variable definitions for ESLint           |
| `prettier`                         | ^3.8.1  | —      | Code formatter                                   |
| `prettier-plugin-astro`            | ^0.14.1 | —      | Prettier support for `.astro` files              |
| `pagefind`                         | ^1.4.0  | 1.4.0  | Static search index generation (post-build)      |
| `@notionhq/client`                 | ^5.16.0 | —      | Notion API client for content fetching           |
| `node-fetch`                       | ^3.3.2  | —      | HTTP client (used in scripts)                    |
| `remark-gfm`                       | ^4.0.1  | —      | GitHub Flavored Markdown support (tables, etc.)  |
| `roughjs`                          | ^4.6.6  | —      | Hand-drawn style rendering (Excalidraw export)   |
| `zod`                              | ^4.3.6  | 4.3.6  | Runtime schema validation                        |

### Python Dependencies

| Package    | Spec     | Locked | Purpose                               |
| ---------- | -------- | ------ | ------------------------------------- |
| `diagrams` | >=0.25.1 | 0.25.1 | Cloud architecture diagram generation |
| `pytest`   | >=8.0    | —      | Python test runner (dev optional dep) |

Transitive Python dependencies (via `diagrams`): `graphviz`, `jinja2`, `pre-commit`.

---

## Package Managers

| Manager | Lockfile                 | Purpose                            |
| ------- | ------------------------ | ---------------------------------- |
| **npm** | `package-lock.json` (v3) | JavaScript/TypeScript dependencies |
| **uv**  | `uv.lock`                | Python dependencies                |

---

## Build Tools & Pipeline

### Build command

```
npm run build  →  astro build && npx pagefind --site dist --glob '**/*.html'
```

1. **Astro** compiles `.astro`, `.md`, `.mdx` into static HTML/CSS/JS in `dist/`
2. **Pagefind** indexes the built HTML for client-side search

### Vite (bundled with Astro)

- Tailwind CSS is loaded as a Vite plugin via `@tailwindcss/vite`
- Mermaid is bundled as a client-side ES module import

### Diagram generation (offline, not part of site build)

- Python scripts in `diagrams/scripts/generate-*.py` produce SVG/PNG files
- Excalidraw `.excalidraw` JSON files in `diagrams/artifacts/` are exported to SVG via `excalidraw-brute-export-cli` (external CLI tool, not in package.json)
- AWS architecture diagrams use the `diagrams` Python library to produce PNG files
- All diagram output goes to `public/images/diagrams/`

### Content pipeline (CI only)

- `scripts/fetch-notion.mjs` fetches content from Notion API and generates `.md` files into `src/content/notes/`

---

## Configuration Files

| File                      | Purpose                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------- |
| `astro.config.mjs`        | Astro config: site URL, base path, MDX integration, Shiki syntax highlighting, Tailwind Vite plugin |
| `tsconfig.json`           | TypeScript config — extends `astro/tsconfigs/strict`                                                |
| `vitest.config.ts`        | Vitest config — node environment, `src/**/*.test.ts` pattern                                        |
| `eslint.config.mjs`       | Flat ESLint config — TS recommended + Astro + Prettier integration                                  |
| `pyproject.toml`          | Python project config — ruff lint ignore rules, pyright settings                                    |
| `.pre-commit-config.yaml` | Pre-commit hooks (see below)                                                                        |
| `package.json`            | npm package metadata, scripts, dependencies                                                         |
| `package-lock.json`       | npm lockfile (v3)                                                                                   |
| `uv.lock`                 | uv Python lockfile                                                                                  |

---

## Linting, Formatting & Pre-commit Hooks

### Pre-commit hooks (`.pre-commit-config.yaml`)

| Hook          | Tool / Version               | Scope                                                          |
| ------------- | ---------------------------- | -------------------------------------------------------------- |
| `ruff-check`  | ruff-pre-commit v0.15.9      | Python files (lint + fix)                                      |
| `ruff-format` | ruff-pre-commit v0.15.9      | Python files (format)                                          |
| `mypy`        | mirrors-mypy v1.20.0         | `diagrams/diagramlib/` only                                    |
| `eslint`      | local (npx eslint --fix)     | `.js`, `.mjs`, `.ts`, `.astro`                                 |
| `prettier`    | local (npx prettier --write) | `.js`, `.mjs`, `.ts`, `.astro`, `.css`, `.json`, `.md`, `.mdx` |
| `pytest`      | local (.venv/bin/pytest)     | Python files (always run)                                      |
| `vitest`      | local (npx vitest run)       | TS/JS files (always run)                                       |

### Syntax highlighting

- **Shiki** (built into Astro) with dual themes: `light-plus` / `dark-plus`
- Theme switching via CSS variables (`--shiki-dark`, `--shiki-light`) keyed on `[data-theme]`

---

## Testing

| Framework  | Config file        | Test location                                                                                       | Scope                   |
| ---------- | ------------------ | --------------------------------------------------------------------------------------------------- | ----------------------- |
| **Vitest** | `vitest.config.ts` | `src/**/*.test.ts` (also `src/lib/glossary-data.test.ts`, `src/lib/glossary-pagination.test.ts`)    | TypeScript unit tests   |
| **Pytest** | `pyproject.toml`   | `tests/test_*.py` (`tests/test_aws_diagram.py`, `tests/test_colors.py`, `tests/test_excalidraw.py`) | Python diagramlib tests |

---

## CI/CD

### GitHub Actions (`.github/workflows/deploy.yml`)

- **Trigger:** push to `main` or manual dispatch
- **Build job:** checkout -> setup Node 20 -> `npm ci` -> fetch Notion content -> `npm run build` -> upload pages artifact
- **Deploy job:** deploys to GitHub Pages via `actions/deploy-pages@v4`
- **Permissions:** `contents: read`, `pages: write`, `id-token: write`

---

## Deployment Target

- **GitHub Pages** at `https://guyardon.github.io/data-engineering-specialization`
- Base path: `/data-engineering-specialization`
- Static output only (no server-side rendering)

---

## Fonts (loaded via Google Fonts CDN)

| Font           | Weights  | Usage                    |
| -------------- | -------- | ------------------------ |
| Poppins        | 300-700  | Sans-serif body, UI text |
| Lora           | 400-700  | Serif headings           |
| JetBrains Mono | 400, 500 | Code blocks              |

---

## Project Structure

```
├── .github/workflows/deploy.yml    # CI/CD
├── .pre-commit-config.yaml         # Pre-commit hooks
├── astro.config.mjs                # Astro configuration
├── diagrams/
│   ├── artifacts/                  # .excalidraw source files
│   ├── diagramlib/                 # Python diagram helper library
│   └── scripts/                    # ~80 diagram generation scripts
├── dist/                           # Build output (gitignored)
├── package.json                    # npm config
├── public/
│   ├── images/diagrams/            # Generated diagram SVGs/PNGs
│   └── images/logos/               # Technology logos (SVG, dark/light variants)
├── pyproject.toml                  # Python project config
├── scripts/
│   └── fetch-notion.mjs            # Notion content fetcher
├── src/
│   ├── components/                 # Astro components (8 files)
│   ├── content/notes/              # Markdown content (generated from Notion)
│   ├── content.config.ts           # Content collection schema (Zod)
│   ├── data/glossary.json          # Glossary terms data
│   ├── layouts/NoteLayout.astro    # Note page layout
│   ├── lib/                        # TypeScript utilities (search, glossary, base path)
│   ├── pages/                      # Astro pages (index, glossary, notes/[...slug])
│   └── styles/global.css           # Global styles + Tailwind import
├── tests/                          # Python tests for diagramlib
├── tsconfig.json                   # TypeScript config
├── uv.lock                         # Python lockfile
└── vitest.config.ts                # Vitest config
```
