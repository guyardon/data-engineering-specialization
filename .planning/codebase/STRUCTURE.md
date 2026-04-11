# Directory Structure

## Root

```
data-engineering-specialization/
├── .github/workflows/         # CI/CD
├── .planning/                 # GSD workflow state
├── .vscode/                   # Editor settings
├── diagrams/                  # Python diagram generation (offline)
├── dist/                      # Build output (gitignored)
├── docs/                      # Planning documents
├── node_modules/              # Node dependencies (gitignored)
├── public/                    # Static assets (copied verbatim to dist/)
├── scripts/                   # Build/sync scripts
├── src/                       # Astro source code
├── tests/                     # Python tests
├── .env                       # Notion token (gitignored)
├── .env.example               # Template for .env
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hook config
├── .prettierrc                # Prettier config
├── .python-version            # Python 3.13
├── astro.config.mjs           # Astro framework config
├── CLAUDE.md                  # Claude Code project instructions
├── eslint.config.mjs          # ESLint config
├── package.json               # Node dependencies & scripts
├── package-lock.json
├── pyproject.toml             # Python dependencies & tool config
├── README.md
├── tsconfig.json              # TypeScript config
├── uv.lock                    # Python lockfile (uv)
└── vitest.config.ts           # Vitest test runner config
```

## `src/` -- Astro Source

```
src/
├── components/
│   ├── Logo.astro             # Site logo (SVG inline)
│   ├── LogoMarquee.astro      # Scrolling tech logo carousel (home page)
│   ├── Mermaid.astro          # Client-side Mermaid diagram renderer
│   ├── SearchBar.astro        # Pagefind search input with dropdown
│   ├── SearchModal.astro      # Full-screen search modal overlay
│   ├── Sidebar.astro          # Collapsible course/week/section nav tree
│   ├── TableOfContents.astro  # Auto-generated heading TOC
│   └── ThemeToggle.astro      # Dark/light theme switcher
├── content/
│   └── notes/                 # Markdown content (gitignored, synced from Notion)
│       ├── course-1-introduction-to-data-engineering/
│       │   ├── week-1-how-to-think-like-a-data-engineer/
│       │   │   ├── 11-how-to-think-like-a-data-engineer.md
│       │   │   └── 12-data-engineering-on-the-cloud.md
│       │   ├── week-2-.../
│       │   ├── week-3-.../
│       │   └── week-4-.../
│       ├── course-2-source-systems-data-ingestion-and-pipelines/
│       │   ├── week-1-working-with-source-systems/
│       │   ├── week-2-data-digestion/
│       │   ├── week-3-dataops/
│       │   └── week-4-orchestration-.../
│       ├── course-3-data-storage-and-queries/
│       │   ├── week-1-data-storage-deep-dive/
│       │   ├── week-2-storage-abstractions/
│       │   └── week-3-queries/
│       └── course-4-data-modeling-transformation-and-serving/
│           ├── week-1-data-modeling-transformations-for-analytics/
│           ├── week-2-data-modeling-transformations-for-machine-learning/
│           ├── week-3-data-transformations-technical-considerations/
│           └── week-4-serving-data-and-analytics-for-machine-learning/
├── content.config.ts          # Content collection schema (Zod validation)
├── data/
│   └── glossary.json          # Glossary terms database (~160KB, categorized)
├── layouts/
│   └── NoteLayout.astro       # Shared layout for all note pages
├── lib/
│   ├── base.ts                # BASE path constant for GitHub Pages
│   ├── glossary-data.ts       # Glossary data query functions
│   ├── glossary-data.test.ts  # Tests for glossary data
│   ├── glossary-detail.ts     # Glossary detail modal logic
│   ├── glossary-pagination.ts # Glossary pagination logic
│   ├── glossary-pagination.test.ts # Tests for pagination
│   ├── search-engine.ts       # Pagefind integration
│   └── search-ui.ts           # Search UI behavior
├── pages/
│   ├── index.astro            # Home page (course cards)
│   ├── glossary.astro         # Interactive glossary page
│   └── notes/
│       └── [...slug].astro    # Dynamic route for all note pages
└── styles/
    └── global.css             # Global styles, theme variables, component styles
```

### Content file counts

- 4 courses, 15 weeks, 45 markdown files total
- File naming: `{weekOrder}{sectionOrder}-slug.md` (e.g., `11-how-to-think-like-a-data-engineer.md`)

## `diagrams/` -- Diagram Generation (Python)

```
diagrams/
├── artifacts/                 # Generated Excalidraw JSON files (88 files)
│   ├── acid-principles.excalidraw
│   ├── airflow-components.excalidraw
│   ├── batch-streaming.excalidraw
│   └── ... (88 total .excalidraw files)
├── diagramlib/                # Shared Python library
│   ├── __init__.py            # Re-exports: ExcalidrawDiagram, color constants
│   ├── aws_diagram.py         # AWS diagram helpers (graph/node/edge/cluster attrs)
│   ├── colors.py              # Color palette: BLUE, GREEN, YELLOW, PURPLE, RED, CYAN, GRAY
│   └── excalidraw.py          # ExcalidrawDiagram class (rect, txt, arr, line, diamond, save)
└── scripts/                   # Generation scripts (76 scripts)
    ├── generate-acid-principles.py
    ├── generate-batch-pipeline-aws.py   # AWS architecture diagram example
    ├── generate-streaming-pipeline-aws.py # AWS architecture diagram example
    └── ... (76 total generate-*.py scripts)
```

### Diagram types by script naming

- `generate-*-aws.py` -- AWS architecture diagrams (use `diagrams` library + `diagramlib.aws_diagram`)
- `generate-*.py` (all others) -- Excalidraw conceptual diagrams (use `diagramlib.ExcalidrawDiagram`)

## `public/` -- Static Assets

```
public/
├── favicon.svg
└── images/
    ├── diagrams/              # Diagram outputs (214 files)
    │   ├── *.svg              # Excalidraw light-mode SVGs
    │   ├── *-dark.svg         # Excalidraw dark-mode SVGs
    │   ├── *.png              # AWS diagram light-mode PNGs
    │   └── *-dark.png         # AWS diagram dark-mode PNGs
    └── logos/                 # Technology logos (102 files)
        ├── *.svg              # Light-mode logos (e.g., airflow.svg)
        ├── *-dark.svg         # Dark-mode logos (e.g., airflow-dark.svg)
        └── *.png              # Fallback PNGs where SVG unavailable
```

## `scripts/` -- Build Scripts

```
scripts/
└── fetch-notion.mjs           # Notion API sync: fetches pages -> generates markdown + images
```

## `tests/` -- Python Tests

```
tests/
├── __init__.py
├── fixtures/                  # Test fixture data
├── test_aws_diagram.py        # Tests for diagramlib.aws_diagram
├── test_colors.py             # Tests for diagramlib.colors
└── test_excalidraw.py         # Tests for diagramlib.excalidraw
```

TypeScript tests are co-located in `src/lib/` as `*.test.ts` files.

## `.github/workflows/`

```
.github/workflows/
└── deploy.yml                 # GitHub Pages deployment (build + deploy on push to main)
```

Pipeline: checkout -> install -> fetch Notion content -> build (Astro + Pagefind) -> deploy to Pages.

## `.planning/` -- GSD Workflow

```
.planning/
├── codebase/                  # Codebase documentation (this file lives here)
└── phases/                    # Phase plans
    ├── 01-foundation-tooling/
    └── 02-notion-sync-audit-fix/
```

## Key File Locations

| What                  | Path                                                         |
| --------------------- | ------------------------------------------------------------ |
| Astro config          | `astro.config.mjs`                                           |
| Content schema        | `src/content.config.ts`                                      |
| Theme variables       | `src/styles/global.css` (lines 1-44)                         |
| Diagram CSS           | `src/styles/global.css` (lines 59-79)                        |
| Base path helper      | `src/lib/base.ts`                                            |
| Glossary data         | `src/data/glossary.json`                                     |
| Sidebar navigation    | `src/components/Sidebar.astro`                               |
| Search integration    | `src/components/SearchBar.astro`, `src/lib/search-engine.ts` |
| Diagram color palette | `diagrams/diagramlib/colors.py`                              |
| AWS diagram helpers   | `diagrams/diagramlib/aws_diagram.py`                         |
| Excalidraw builder    | `diagrams/diagramlib/excalidraw.py`                          |
| Notion sync script    | `scripts/fetch-notion.mjs`                                   |
| CI/CD pipeline        | `.github/workflows/deploy.yml`                               |
| Pre-commit hooks      | `.pre-commit-config.yaml`                                    |
| Python config         | `pyproject.toml`                                             |
| Node config           | `package.json`                                               |

## Naming Conventions

- **Content files**: `{weekDigit}{sectionDigit}-kebab-case-title.md` (e.g., `32-choosing-the-right-technologies.md`)
- **Content dirs**: `course-{N}-kebab-title/week-{N}-kebab-title/`
- **Diagram scripts**: `generate-{kebab-name}.py` or `generate-{kebab-name}-aws.py`
- **Diagram artifacts**: `{kebab-name}.excalidraw`
- **Diagram outputs**: `{name}.svg` + `{name}-dark.svg` (Excalidraw), `{name}.png` + `{name}-dark.png` (AWS)
- **Logo files**: `{tool-name}.svg` + `{tool-name}-dark.svg`
- **Components**: `PascalCase.astro`
- **Lib files**: `kebab-case.ts` with co-located `kebab-case.test.ts`
