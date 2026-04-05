# Data Engineering Specialization Website

Astro 6 static site for data engineering course notes. Dark/light theme with gold accent (`#c9a84c`).

## Diagrams

This project uses two diagram libraries. Choose based on the diagram type:

### Excalidraw — Conceptual diagrams
Use for: flowcharts, timelines, comparison charts, radial layouts, stacked blocks, any conceptual/teaching diagram.

- Hand-drawn aesthetic with Virgil font
- Generate `.excalidraw` JSON → export via `excalidraw-brute-export-cli` → embed SVG
- Export both `--dark-mode 0` and `--dark-mode 1` versions
- See `~/.claude/skills/excalidraw-diagrams/SKILL.md` for all layout rules
- Skill source repo: `/Users/guyardon/Repositories/excalidraw-diagrams-skill`
- Source files: `diagrams/*.excalidraw`
- Output: `public/images/diagrams/*.svg`

### Python `diagrams` — Cloud architecture diagrams
Use for: AWS/GCP/Azure architecture diagrams, infrastructure diagrams, anything that benefits from real cloud service icons.

- Real AWS service icons (RDS, S3, Glue, Redshift, etc.)
- Generate via Python script with `from diagrams import Diagram`
- Export both light (white bg) and dark (`#0f0f13` bg) PNG versions
- Output: `public/images/diagrams/*.png` and `*-dark.png`
- Skill source repo: `/Users/guyardon/Repositories/aws-diagrams-skill`
- Reference scripts: `scripts/generate-batch-pipeline-aws.py`, `scripts/generate-streaming-pipeline-aws.py`
- **Graph attributes:**
  - DPI: `150`
  - Diagram title: `18px Helvetica Bold`, at top (`labelloc: "t"`), add `\n\n` after title text for spacing
  - Padding: `pad: "0.3"`
  - Spacing: `nodesep: "0.3"`, `ranksep: "1.2"` (wide horizontal gaps between clusters)
  - Pipeline diagrams use `rankdir: "LR"` with `compound: "true"`
- **Node attributes:**
  - Font: `12px Helvetica`
  - Height: `1.1` (compact icons)
  - Short labels — just the service name (e.g. "RDS", "Lambda", "S3"), no descriptions
- **Edge attributes:**
  - Penwidth: `2.0`
  - Use `lhead`/`ltail` on every inter-cluster edge so arrows start/end at cluster borders
  - Pattern: `e = lambda **kw: Edge(color=edge_color, **kw)` then `node >> e(lhead="cluster_X", ltail="cluster_Y") >> node`
- **Cluster attributes:**
  - Font: `14px Helvetica Bold`
  - Labels: centered at top (`labeljust: "c"`, `labelloc: "t"`)
  - Border: `style: "dashed,rounded"`, `penwidth: "1.5"`
  - Margin: `14`
- **Colors:**
  - Dark mode: bg `#0f0f13`, fontcolor `#e8e8ea`, edge color `#65656e`
  - Light mode: bg `white`, fontcolor `#1e1e1e`, edge color `#495057`
  - Light cluster backgrounds: stroke color + `40` opacity suffix (e.g. `#b2f2bb40`)
  - Dark cluster backgrounds: dark tinted variants (e.g. `#1a2a1a`)
- **CSS note:** `.diagram` has `max-height: 500px; object-fit: contain` — diagrams scale down to fit
- **Critical: all `diagrams` library diagrams on the same page must share identical style config** — extract colors and attrs into a shared `gen(dark)` function. Only the content/connections should differ between diagrams.

### Mermaid — Data modeling diagrams
Use for: ER diagrams, table schemas, PK/FK relationships, normalization examples.

- Rendered client-side via `mermaid` npm package
- Component: `src/components/Mermaid.astro` — pass chart code as `chart` prop
- Requires `.mdx` file (not `.md`) to use the component import
- Content collection glob in `src/content.config.ts` accepts both `**/*.{md,mdx}`
- Auto-switches between dark/light themes by observing `data-theme` on `<html>`
- Use `erDiagram` syntax with `PK`/`FK` column annotations and crow's foot relationships

### Technology logos
Use when introducing a set of technologies — show their logos side by side for visual context.

- Source: full-color logos with text from [vectorlogo.zone](https://www.vectorlogo.zone) (`-ar21.svg` for 2:1 icon+text variants), or [gilbarbara/logos](https://github.com/gilbarbara/logos) as fallback
- Prefer full logos (icon + name text) over icon-only versions
- Store in: `public/images/logos/`
- Always add a `<span>` label below each logo regardless of whether the logo contains text
- CSS class `.tech-logos` handles layout: centered row, equal flex sizing, `100px` height
- White background with rounded corners (`border-radius: 12px; padding: 8px`) so logos look correct on both dark and light themes
- HTML pattern:
```html
<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization-website/images/logos/name.svg" alt="Name" />
    <span>Display Name</span>
  </div>
</div>
```

### Search
Powered by Pagefind (indexed at build time via `npx pagefind`). Component: `src/components/SearchBar.astro`.

- **Loading:** Pagefind UI is an IIFE (not ES module) — load via `<script>` tag, not `import()`. Access `window.PagefindUI` after load.
- **Testing:** Search only works after `npm run build` + `npm run preview`. The dev server shows a placeholder fallback.
- **Results dropdown:** Absolute-positioned card below input with rounded corners (14px), card background, shadow. Results are hoverable rows (not bordered list items). Each result is fully clickable via `::after` overlay on the link.
- **Sidebar variant:** Compact results — `excerptLength: 15` (vs 30 on main page), excerpt clamped to 2 lines, smaller font sizes, tighter padding.
- **Clear button:** Minimal "x" inside the input, no border, hover background.

### Theme switching (both libraries)
The site uses `base: "/data-engineering-specialization-website"` — all image `src` paths must include this prefix.
```html
<img src="/data-engineering-specialization-website/images/diagrams/name-dark.svg" alt="..." class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/name.svg" alt="..." class="diagram diagram-light" />
```
CSS in `src/styles/global.css` handles show/hide based on `[data-theme]`.

## Workflow
- At the start of each session, kill any existing Astro dev servers (`kill $(lsof -ti :4321 2>/dev/null)`) then run `npm run dev` in the background so the user can preview changes live. Note the port in case it auto-increments.
- Always run `npm run build` automatically after any content or style change — don't wait to be asked
- Commit frequently — after each logical unit of work (a diagram, a content change, a style fix). Break changes into multiple conventional commits grouped by context.
- For diagrams: build, embed, and rebuild the site, then wait for user review before committing.
- **Critical:** All asset paths in markdown must include the base path prefix `/data-engineering-specialization-website/`. Never use bare `/images/...` paths — they will 404.

## Content conventions
- `backticks` for tools/products (S3, Airflow, dbt)
- **Bold** for key concepts
- `---` dividers between sub-topics within a section
- Sub-topic titles as `**bold text**` (not headings)
- Only `##` headings for numbered subsections (x.x.x)
