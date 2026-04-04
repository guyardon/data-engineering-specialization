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

### Theme switching (both libraries)
```html
<img src="...-dark.svg" alt="..." class="diagram diagram-dark" />
<img src="...svg" alt="..." class="diagram diagram-light" />
```
CSS in `src/styles/global.css` handles show/hide based on `[data-theme]`.

## Workflow
- Always run `npm run build` automatically after any content or style change — don't wait to be asked
- Commit frequently — after each logical unit of work (a diagram, a content change, a style fix). Break changes into multiple conventional commits grouped by context.

## Content conventions
- `backticks` for tools/products (S3, Airflow, dbt)
- **Bold** for key concepts
- `---` dividers between sub-topics within a section
- Sub-topic titles as `**bold text**` (not headings)
- Only `##` headings for numbered subsections (x.x.x)
