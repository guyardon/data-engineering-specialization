# External Integrations

## Notion API

**Purpose:** Content source -- all course notes originate from a Notion workspace and are fetched at build time.

| Detail         | Value                                                           |
| -------------- | --------------------------------------------------------------- |
| Client library | `@notionhq/client` ^5.16.0                                      |
| Script         | `scripts/fetch-notion.mjs`                                      |
| Root page ID   | `139969a7aa018017b81fc3858c54fc8f`                              |
| Auth           | `NOTION_TOKEN` environment variable (or `.env` file)            |
| API operations | `blocks.children.list` (recursive page traversal)               |
| Output         | Markdown files in `src/content/notes/` with YAML frontmatter    |
| Image handling | Downloads Notion-hosted images to `public/images/`              |
| Invocation     | Manual (`node scripts/fetch-notion.mjs`) or CI (GitHub Actions) |

### Data flow

1. Script traverses the Notion page tree: root -> courses -> weeks -> sections -> subsections
2. Each block is converted to Markdown (headings, lists, code, tables, callouts, toggles, images, equations)
3. Images are downloaded from Notion's S3-backed URLs and saved locally
4. MDX special characters (`<`, `>`) are escaped
5. Subsections are merged into parent sections (flattened to max 3 heading levels)
6. Output: one `.md` file per section with structured frontmatter (`title`, `course`, `courseSlug`, `courseOrder`, `week`, `weekSlug`, `weekOrder`, `order`, `notionId`)

---

## GitHub Pages (Deployment Target)

**Purpose:** Static site hosting.

| Detail       | Value                                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------------------- |
| URL          | `https://guyardon.github.io/data-engineering-specialization`                                                  |
| Base path    | `/data-engineering-specialization`                                                                            |
| Workflow     | `.github/workflows/deploy.yml`                                                                                |
| Trigger      | Push to `main` branch or manual dispatch                                                                      |
| Actions used | `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4` |
| Node version | 20 (in CI)                                                                                                    |
| Build steps  | `npm ci` -> `node scripts/fetch-notion.mjs` -> `npm run build`                                                |
| Secrets      | `NOTION_TOKEN` (for content fetching during CI build)                                                         |

---

## GitHub Actions (CI/CD)

**Workflow file:** `.github/workflows/deploy.yml`

Single workflow with two jobs:

1. **build** — installs deps, fetches Notion content, builds Astro site, uploads artifact
2. **deploy** — deploys the artifact to GitHub Pages

Concurrency group: `pages` (cancel-in-progress: false).

Permissions: `contents: read`, `pages: write`, `id-token: write`.

---

## Google Fonts CDN

**Purpose:** Web font loading for the site's typography.

| Detail    | Value                                                       |
| --------- | ----------------------------------------------------------- |
| Endpoint  | `https://fonts.googleapis.com/css2`                         |
| Loaded in | `src/styles/global.css` via `@import url(...)`              |
| Fonts     | Poppins (300-700), Lora (400-700), JetBrains Mono (400-500) |

---

## Pagefind (Static Search)

**Purpose:** Client-side full-text search over the built site.

| Detail     | Value                                                                              |
| ---------- | ---------------------------------------------------------------------------------- |
| Package    | `pagefind` ^1.4.0 (dev dependency)                                                 |
| Index step | `npx pagefind --site dist --glob '**/*.html'` (runs after `astro build`)           |
| Client API | Dynamic import of `/pagefind/pagefind.js` at runtime                               |
| Wrapper    | `src/lib/search-engine.ts` — `initPagefind()`, `search()`                          |
| UI         | Custom implementation in `src/lib/search-ui.ts` + `src/components/SearchBar.astro` |
| Dev mode   | Falls back to a placeholder (index only exists after build)                        |

**Note:** Pagefind is not a hosted service -- it generates a static index at build time and runs entirely client-side. No network calls are made at search time.

---

## Vectorlogo.zone / Gilbarbara Logos

**Purpose:** Technology logo assets (SVG files) displayed on the homepage marquee and inline with content.

| Detail  | Value                                                                                                                        |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Sources | [vectorlogo.zone](https://www.vectorlogo.zone) (primary), [gilbarbara/logos](https://github.com/gilbarbara/logos) (fallback) |
| Storage | `public/images/logos/` — dark and light variants (`name.svg`, `name-dark.svg`)                                               |
| Usage   | `LogoMarquee.astro` component, inline `<div class="tech-logos">` blocks in content                                           |

Logos are downloaded manually and committed to the repo. No runtime API calls.

---

## Excalidraw (Diagram Export)

**Purpose:** Export hand-drawn style diagrams from `.excalidraw` JSON to SVG.

| Detail       | Value                                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------------------- |
| Tool         | `excalidraw-brute-export-cli` (external CLI, not in package.json)                                             |
| Source files | `diagrams/artifacts/*.excalidraw`                                                                             |
| Output       | `public/images/diagrams/*.svg` (light and dark variants)                                                      |
| Builder      | `diagrams/diagramlib/excalidraw.py` — `ExcalidrawDiagram` class generates `.excalidraw` JSON programmatically |
| Generation   | Python scripts in `diagrams/scripts/generate-*.py`                                                            |

Not a hosted service -- runs locally as a CLI tool to export SVG files.

---

## Graphviz (via `diagrams` Python library)

**Purpose:** Graph layout engine used by the `diagrams` Python library for AWS architecture diagrams.

| Detail        | Value                                                                  |
| ------------- | ---------------------------------------------------------------------- |
| Dependency of | `diagrams` 0.25.1 (Python)                                             |
| Output        | PNG files in `public/images/diagrams/` (light and dark variants)       |
| Config        | Standardized via `diagrams/diagramlib/aws_diagram.py` helper functions |
| DPI           | 150                                                                    |

Requires `graphviz` system package to be installed.

---

## Summary of External Communication

| Integration      | Direction        | When               | Auth / Secrets        |
| ---------------- | ---------------- | ------------------ | --------------------- |
| Notion API       | Outbound         | Build time (CI)    | `NOTION_TOKEN` secret |
| GitHub Pages     | Deployment       | CI on push to main | `id-token` (OIDC)     |
| Google Fonts CDN | Inbound (client) | Page load          | None (public)         |
| Vectorlogo.zone  | Manual download  | Dev time           | None (public)         |

**No runtime APIs, databases, auth providers, webhooks, or backend services.** The site is fully static -- all external data is fetched at build time and all search/interaction happens client-side.
