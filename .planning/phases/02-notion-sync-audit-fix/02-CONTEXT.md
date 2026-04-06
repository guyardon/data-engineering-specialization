# Phase 2: Notion Sync Audit & Fix - Context

**Gathered:** 2026-04-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Audit and fix `fetch-notion.mjs` so it produces correct, well-structured markdown files with proper image references. Content is treated as "raw" — AI will reformat the prose later. This phase focuses on **structure, images, and frontmatter correctness**, not markdown rendering polish.

</domain>

<decisions>
## Implementation Decisions

### Hierarchy & Navigation Structure

- **D-01:** Flatten page hierarchy to **Course → Week → Section** level. Subsections merge into their parent section page (rendered as headings within the same file).
- **D-02:** Sidebar navigation shows Course > Week > Section. Subsections are NOT separate sidebar entries — they're navigable via in-page TOC/anchored headings.
- **D-03:** Course 4's existing week-level pages (which already have sections inline) should remain as-is. The flattening primarily affects courses 1-2 where content is deeply nested (course→week→section→subsection).
- **D-04:** For weeks that have no child sections (already leaf pages), keep them as single pages.

### Content Quality

- **D-05:** Content is "raw" — do NOT spend time fixing markdown rendering details (callout formatting, code language tags, etc.). AI will reformat all prose later.
- **D-06:** Focus on: correct structure, working image references, valid frontmatter.

### Image Handling

- **D-07:** Images must remain in their original positions within the content. Their placement is intentional and should be preserved through any restructuring.
- **D-08:** Keep existing image naming (UUID-based) and flat `/images/` directory — no reorganization needed.

### Script Behavior

- **D-09:** Full wipe-and-rebuild (`cleanDir()`) is fine — this is a one-time sync, not ongoing.

### Claude's Discretion

- Link handling in richTextToMd (rt.href) — fix if encountered during audit, but not a primary goal
- MDX escape character handling — fix obvious issues but don't over-engineer

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Sync Script

- `scripts/fetch-notion.mjs` — The fetch script to audit and fix (566 lines)

### Content Schema

- `src/content.config.ts` — Zod schema that frontmatter must match
- `src/content/notes/` — Existing generated content (52 files across 4 courses)

### Requirements

- `.planning/REQUIREMENTS.md` — SYNC-01 through SYNC-08

### Codebase Context

- `.planning/codebase/STACK.md` — Tech stack overview
- `.planning/codebase/STRUCTURE.md` — Project file structure

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- `fetch-notion.mjs` already handles most block types (paragraph, headings, lists, code, tables, images, callouts, toggles, equations, embeds)
- `richTextToMd()` handles bold, italic, strikethrough, underline, code annotations
- `buildMdx()` generates frontmatter with all required fields

### Known Issues

- `richTextToMd()` does NOT handle `rt.href` — hyperlinks render as plain text
- `{ }` not escaped despite comment saying they are (MDX parse risk)
- Callouts render as simple blockquotes — acceptable for "raw" content
- Subsection merging logic exists for deep nesting but creates separate files per subsection instead of merging into parent

### Integration Points

- Content must match `content.config.ts` Zod schema
- Sidebar component reads from content collection
- Images referenced as `/images/{uuid}.png`

</code_context>

<specifics>
## Specific Ideas

- User plans to use AI to rewrite and nicely format all notes after this phase
- Images were placed strategically in original Notion pages — their positions must be preserved
- Course 4 pattern (everything at week level) is the desired simplicity target for navigation

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

_Phase: 02-notion-sync-audit-fix_
_Context gathered: 2026-04-01_
