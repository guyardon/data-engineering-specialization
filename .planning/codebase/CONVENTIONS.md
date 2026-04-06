# Coding Conventions

## Languages and Stack

| Layer            | Technology                                | Version     |
| ---------------- | ----------------------------------------- | ----------- |
| Site framework   | Astro 6 (static output)                   | `^6.1.2`    |
| Styling          | Tailwind CSS 4 (via Vite plugin)          | `^4.2.2`    |
| Markup           | Markdown + MDX (via `@astrojs/mdx`)       | -           |
| Client diagrams  | Mermaid (client-side render)              | `^11.14.0`  |
| TypeScript       | Strict (extends `astro/tsconfigs/strict`) | `^5.9.3`    |
| Python           | 3.13+                                     | `>=3.13`    |
| Node             | 22+                                       | `>=22.12.0` |
| Package managers | npm (JS), uv (Python)                     | -           |

---

## TypeScript / JavaScript Style

### ESLint Configuration

File: `eslint.config.mjs`

- Uses flat config format (`tseslint.config(...)`)
- Base: `js.configs.recommended` + `tseslint.configs.recommended` + `astro.configs.recommended`
- **`@typescript-eslint/no-explicit-any`: `"error"`** -- no `any` allowed
- Prettier runs as an ESLint rule (`prettier/prettier: "error"`) for `.ts`, `.mjs`, `.js`, `.cjs` files
- Prettier is **disabled** for `.astro` virtual script files (Astro processor creates `*.astro/*.ts` files that would break Prettier)
- Node globals enabled for `scripts/**/*.{mjs,js}` with `allowEmptyCatch: true`
- Ignores: `dist/**`, `node_modules/**`, `.astro/**`

### Prettier Configuration

File: `.prettierrc`

```json
{
  "plugins": ["prettier-plugin-astro"],
  "overrides": [
    {
      "files": "*.astro",
      "options": { "parser": "astro" }
    }
  ]
}
```

Uses default Prettier settings (no custom width, tabs, etc.) with the Astro parser plugin.

### TypeScript Configuration

File: `tsconfig.json`

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

Strict mode inherited from Astro's strict preset.

### Naming Conventions (TypeScript)

- **Files**: kebab-case (`glossary-data.ts`, `glossary-pagination.ts`, `search-engine.ts`)
- **Test files**: co-located with source, `*.test.ts` suffix (`glossary-data.test.ts`)
- **Interfaces**: PascalCase (`GlossaryCategory`, `GlossaryTerm`, `TermEntry`)
- **Functions**: camelCase (`buildAllTerms`, `findTermByName`, `pickRandomTerm`)
- **Constants**: camelCase for module-level (`BASE`), UPPER_SNAKE for true constants
- **Type aliases**: inline in function signatures or separate `interface` declarations

### Module Pattern

Pure logic modules export functions with JSDoc-style block comments:

```typescript
// src/lib/glossary-pagination.ts
/**
 * Generic pagination algorithm for the glossary page.
 * Pure logic -- DOM measurement injected via fitsOnPage callback (DIP).
 */
export function computePageBreaks(
  totalItems: number,
  fitsOnPage: (startIndex: number, count: number) => boolean,
): number[] { ... }
```

Key pattern: **separate pure logic from DOM**. Library files in `src/lib/` contain zero DOM dependencies so they can be unit-tested with Vitest in a Node environment.

---

## Python Style

### Ruff Configuration

Configured in `pyproject.toml` and `.pre-commit-config.yaml`:

- `ruff-check` with `--fix` (auto-fix lint issues)
- `ruff-format` (formatting)
- Single suppressed rule: `E731` (lambda assignment -- allowed)

### Mypy

- Runs only on `diagrams/diagramlib/` directory
- Version: `v1.20.0` (via `pre-commit/mirrors-mypy`)

### Pyright

Configured in `pyproject.toml`:

```toml
[tool.pyright]
venvPath = "."
venv = ".venv"
reportMissingModuleSource = false
reportMissingTypeStubs = false
reportUnusedExpression = false
```

### Naming Conventions (Python)

- **Modules**: snake_case (`aws_diagram.py`, `excalidraw.py`, `colors.py`)
- **Classes**: PascalCase (`ExcalidrawDiagram`)
- **Functions/methods**: snake_case (`graph_attrs`, `node_attrs`, `cluster_attrs`)
- **Constants**: UPPER_SNAKE (`CLUSTER_COLORS_LIGHT`, `BLUE`, `GREEN`, `OUT_DIR`)
- **Parameters**: short abbreviated names in builder APIs (`sw` for stroke width, `bg` for background, `cid` for container ID, `op` for opacity, `bnd` for bound elements, `sb`/`eb` for start/end binding)

### Type Annotations

Modern Python 3.13 syntax used throughout:

```python
def graph_attrs(*, dark: bool, title: str, rankdir: str = "LR") -> dict[str, str]:
```

- Uses `dict[str, str]` not `Dict[str, str]`
- Uses `list` not `List`
- Uses `int | float` union syntax
- Keyword-only arguments with `*` separator

### Docstrings

Single-line docstrings for module and function documentation:

```python
"""Helpers for AWS architecture diagrams using the `diagrams` library."""

def output_dir() -> str:
    """Return the standard output directory for AWS diagram PNGs."""
```

### Script Pattern

Diagram generation scripts follow a consistent pattern:

```python
#!/usr/bin/env python3
# pyright: reportArgumentType=false
"""Generate <NAME> diagram (light + dark) using diagrams library."""

from diagramlib.aws_diagram import (
    cluster_attrs, edge_attrs, graph_attrs, node_attrs, output_dir,
)

OUT_DIR = output_dir()

def gen(dark: bool):
    suffix = "-dark" if dark else ""
    # ... diagram construction ...

gen(dark=False)
gen(dark=True)
print("Done -- generated light and dark <name> diagrams")
```

Every script generates both light and dark variants. The `gen(dark)` function is the single entry point.

---

## File Organization

```
project-root/
  astro.config.mjs          # Astro config (base path, MDX, Tailwind)
  eslint.config.mjs          # ESLint flat config
  .prettierrc                # Prettier config
  pyproject.toml             # Python project + ruff/pyright config
  .pre-commit-config.yaml    # Pre-commit hooks
  vitest.config.ts           # Vitest config
  tsconfig.json              # TypeScript strict config

  src/
    components/              # Astro components (PascalCase .astro files)
      Logo.astro
      Mermaid.astro
      SearchBar.astro
      Sidebar.astro
      ThemeToggle.astro
      ...
    content/
      notes/                 # Markdown/MDX content files
        course-X-.../
          week-Y-.../
            XY-topic-name.md
    content.config.ts        # Content collection schema (Zod)
    data/                    # Static data files
    layouts/
      NoteLayout.astro       # Single layout file
    lib/                     # Pure logic modules (no DOM)
      base.ts
      glossary-data.ts
      glossary-pagination.ts
      glossary-data.test.ts  # Co-located tests
      glossary-pagination.test.ts
    pages/                   # Astro page routes
      index.astro
      glossary.astro
      notes/
    styles/
      global.css             # Single global stylesheet

  diagrams/
    diagramlib/              # Shared Python library
      __init__.py
      aws_diagram.py         # AWS diagram helpers
      colors.py              # Color palette constants
      excalidraw.py          # Excalidraw JSON builder
    scripts/                 # One script per diagram (generate-*.py)

  tests/                     # Python tests (pytest)
    __init__.py
    fixtures/                # Golden JSON fixtures
    test_aws_diagram.py
    test_colors.py
    test_excalidraw.py

  public/
    images/
      diagrams/              # Generated diagram output (SVG/PNG)
      logos/                 # Technology logos

  scripts/
    fetch-notion.mjs         # Notion content fetcher

  .github/workflows/
    deploy.yml               # GitHub Pages deployment
```

---

## Astro Component Patterns

### Component Structure

Astro components use the triple-section pattern:

```astro
---
// Frontmatter: imports, props interface, data fetching
interface Props {
  chart: string;
}
const { chart } = Astro.props;
---

<!-- Template: HTML markup -->
<div class="mermaid-diagram" data-chart={encodeURIComponent(chart.trim())}>
</div>

<style>
  /* Scoped styles */
</style>

<script>
  // Client-side JavaScript
</script>
```

### Props

Props are typed via `interface Props` in the frontmatter:

```astro
---
interface Props {
  chart: string;
}
const { chart } = Astro.props;
---
```

For collection data, types are cast inline: `Astro.props.currentSlug as string`.

### Theme Toggling

The site uses `data-theme="light"` on `<html>` for light mode, absent/removed for dark mode (dark is default). CSS selectors:

```css
:root:not([data-theme="light"]) .icon-moon {
  display: none;
}
[data-theme="light"] .icon-sun {
  display: none;
}
```

### Diagram Embedding

All diagrams require both dark and light variants with CSS-based show/hide:

```html
<img
  src="/data-engineering-specialization-website/images/diagrams/name-dark.svg"
  alt="..."
  class="diagram diagram-dark"
/>
<img
  src="/data-engineering-specialization-website/images/diagrams/name.svg"
  alt="..."
  class="diagram diagram-light"
/>
```

All asset paths **must** include the base path prefix `/data-engineering-specialization-website/`.

---

## Content Conventions (Markdown)

### Frontmatter Schema

Defined in `src/content.config.ts` using Zod:

```typescript
z.object({
  title: z.string(),
  course: z.string(),
  courseSlug: z.string(),
  courseOrder: z.number(),
  week: z.string(),
  weekSlug: z.string(),
  weekOrder: z.number(),
  order: z.number(),
  notionId: z.string().optional(),
});
```

### File Naming

`{courseOrder}{weekOrder}-topic-name-in-kebab-case.md`

Example: `11-how-to-think-like-a-data-engineer.md` = Course 1, Week 1, first note.

### Directory Structure

```
src/content/notes/
  course-1-introduction-to-data-engineering/
    week-1-how-to-think-like-a-data-engineer/
      11-how-to-think-like-a-data-engineer.md
      12-data-engineering-on-the-cloud.md
    week-2-.../
```

### Formatting Rules

- `backticks` for tools/products (S3, Airflow, dbt)
- **Bold** for key concepts
- `---` dividers between sub-topics within a section
- Sub-topic titles as `**bold text**` (not headings)
- Only `##` headings for numbered subsections (e.g., `## 1.1.1 The Data Engineering Lifecycle`)
- _Italics_ for definitions and quotes

---

## Commit Message Format

Conventional commits with gitmoji prefix:

```
<emoji> <type>: <description>
```

Examples from recent history:

```
🔧 chore: move diagramlib into diagrams/ directory
🧹 chore: clean up repo root -- remove redundant config files
🔧 chore: update uv.lock with dev dependencies
🔧 chore: add pre-commit hooks and fix lint/format issues
```

Types: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `style:`, `perf:`, `ci:`, `build:`

---

## Pre-commit Hooks

File: `.pre-commit-config.yaml`

Six hooks run on every commit:

| Hook          | Source                              | Scope                                 | What it does              |
| ------------- | ----------------------------------- | ------------------------------------- | ------------------------- |
| `ruff-check`  | `astral-sh/ruff-pre-commit` v0.15.9 | `*.py`                                | Lint Python with auto-fix |
| `ruff-format` | `astral-sh/ruff-pre-commit` v0.15.9 | `*.py`                                | Format Python             |
| `mypy`        | `pre-commit/mirrors-mypy` v1.20.0   | `diagrams/diagramlib/` only           | Type-check Python library |
| `eslint`      | local                               | `*.{js,mjs,ts,astro}`                 | Lint JS/TS with auto-fix  |
| `prettier`    | local                               | `*.{js,mjs,ts,astro,css,json,md,mdx}` | Format JS/TS/CSS/Markdown |
| `pytest`      | local                               | Always runs on `*.py` changes         | Run Python tests          |
| `vitest`      | local                               | Always runs on `*.{ts,js}` changes    | Run TypeScript tests      |

Both test suites (`pytest` and `vitest run`) are gate checks -- commits fail if tests fail.

---

## CI/CD

File: `.github/workflows/deploy.yml`

Single workflow: **Deploy to GitHub Pages**

- Triggers: push to `main`, manual dispatch
- Steps: checkout, setup Node 20, `npm ci`, fetch Notion content, `npm run build`, upload artifact, deploy to Pages
- Build command: `astro build && npx pagefind --site dist --glob '**/*.html'` (includes search index generation)
- No CI test step -- tests are enforced via pre-commit hooks locally

---

## Error Handling Patterns

### Python

No try/except blocks in the library code. Functions are simple data transformers that return dicts or write files. The `os.makedirs(..., exist_ok=True)` pattern is used for directory creation in `ExcalidrawDiagram.save()`.

### TypeScript

Functions return `null` for "not found" cases rather than throwing:

```typescript
export function findTermByName(...): TermEntry | null {
  // returns null for unknown term
}

export function pickRandomTerm(...): TermEntry | null {
  if (pool.length === 0) return null;
  // ...
}
```

No try/catch in library code. Error handling is deferred to the UI layer.
