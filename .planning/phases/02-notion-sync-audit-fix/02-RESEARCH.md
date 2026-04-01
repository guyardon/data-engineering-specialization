# Phase 2: Notion Sync Audit & Fix - Research

**Researched:** 2026-03-31
**Domain:** Notion API to Markdown conversion (Node.js script)
**Confidence:** HIGH

## Summary

This phase fixes `scripts/fetch-notion.mjs` (566 lines) to produce correct, complete markdown. The script already works end-to-end (52 files, 120 images exist). The core changes are: (1) restructure traversal to flatten subsections into parent section pages per D-01, (2) fix `richTextToMd()` to handle `rt.href` links, (3) fix `{ }` escaping for MDX safety, and (4) ensure frontmatter matches `content.config.ts` schema with correct `order` values after flattening.

This is a single-file fix phase. No new dependencies needed. The Notion API client (`@notionhq/client`) is already installed and working.

**Primary recommendation:** Fix the traversal logic in `run()` to merge subsections into section-level pages, fix `richTextToMd()` href handling, and validate output against the Zod schema.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Flatten page hierarchy to Course -> Week -> Section level. Subsections merge into their parent section page (rendered as headings within the same file).
- **D-02:** Sidebar navigation shows Course > Week > Section. Subsections are NOT separate sidebar entries.
- **D-03:** Course 4's existing week-level pages remain as-is. Flattening primarily affects courses 1-2 where content is deeply nested.
- **D-04:** For weeks that have no child sections (already leaf pages), keep them as single pages.
- **D-05:** Content is "raw" -- do NOT spend time fixing markdown rendering details. AI will reformat later.
- **D-06:** Focus on: correct structure, working image references, valid frontmatter.
- **D-07:** Images must remain in their original positions within the content.
- **D-08:** Keep existing image naming (UUID-based) and flat /images/ directory.
- **D-09:** Full wipe-and-rebuild (cleanDir()) is fine -- one-time sync.

### Claude's Discretion
- Link handling in richTextToMd (rt.href) -- fix if encountered during audit
- MDX escape character handling -- fix obvious issues but don't over-engineer

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SYNC-01 | Running fetch-notion.mjs produces .md files for all courses/weeks/lessons | Traversal restructure (flatten subsections) |
| SYNC-02 | All text block types render correctly (paragraphs, headings, bold, italic, inline code) | Already working in richTextToMd(); add href fix |
| SYNC-03 | Code blocks render with correct language tag | Already working (line 256-258); Notion language field maps directly |
| SYNC-04 | Images download to public/images/ and reference correctly | Already working (120 images exist); preserve positions during merge |
| SYNC-05 | Tables render as valid markdown tables | Already working (lines 306-325) |
| SYNC-06 | Callouts/admonitions convert to consistent markdown | Already working as blockquotes (line 267-270); acceptable per D-05 |
| SYNC-07 | Nested lists render correctly | Already working with recursive depth (lines 196-229) |
| SYNC-08 | Frontmatter includes all required fields | buildMdx() already generates all fields; fix order values after flatten |
</phase_requirements>

## Standard Stack

No new dependencies. Existing stack:

| Library | Version | Purpose | Status |
|---------|---------|---------|--------|
| @notionhq/client | (installed) | Notion API access | Working |
| Node.js built-ins (fs, path, https) | N/A | File I/O, image download | Working |

## Architecture Patterns

### Current Script Structure (single file)
```
scripts/fetch-notion.mjs
  - Utility functions (slugify, downloadImage, extractImageUUID)
  - Notion API helpers (getPageTitle, getChildPages, getBlockChildren)
  - Block-to-markdown (richTextToMd, processBlocks)
  - Main traversal (run, fetchPageContent, buildMdx, cleanDir)
```

### Current Hierarchy Problem

The script currently creates **separate files per subsection** when a section has child pages (lines 482-519). Per D-01, subsections should be merged into their parent section as headings.

**Current behavior (courses 1-2):**
```
Course -> Week -> Section -> Subsection (each = separate .md file)
```
Week 1 of Course 1 has 12 separate files with order values like 101, 102...107, 201, 202...204 (section*100 + subsection).

**Desired behavior:**
```
Course -> Week -> Section (subsections merged as ## headings in section file)
```

### Fix Pattern for Traversal

The `else` branch at line 482 (when section has children) needs to change from creating separate files per subsection to:
1. Fetch section's own content
2. For each subsection: fetch content, prepend `## {subsection.title}`, append to section content
3. Write ONE file per section with merged content
4. Use `si + 1` for order (sequential within week), not `(si+1)*100+ssi+1`

**Image position preservation (D-07):** When merging subsection content, images are already inline in the markdown returned by `processBlocks()`. Concatenating section + subsection content preserves image positions naturally.

### Fix Pattern for richTextToMd href

Line 138-158: `rt.href` is never checked. Fix:
```javascript
// After annotation processing, before return:
if (rt.href) {
  text = `[${text}](${rt.href})`;
}
```

### Fix Pattern for { } Escaping

Line 148 escapes `<` and `>` but NOT `{` and `}` despite a comment claiming otherwise. Since files are `.md` not `.mdx`, this is lower risk, but fix for safety:
```javascript
text = text.replace(/\{/g, "\\{").replace(/\}/g, "\\}");
```

Note: Since content.config.ts uses `glob({ pattern: "**/*.md" })`, these are standard markdown files processed by Astro's markdown pipeline, not MDX. Curly brace escaping may not be strictly necessary, but it prevents issues if files are ever treated as MDX.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Notion API pagination | Custom pagination | Existing `getBlockChildren()` loop | Already handles cursor-based pagination correctly |
| Image downloading | New download logic | Existing `downloadImage()` | Already handles redirects and deduplication |

## Common Pitfalls

### Pitfall 1: Lost Images During Subsection Merge
**What goes wrong:** When merging subsections into parent, images referenced in subsection content could get lost if content is re-fetched differently.
**How to avoid:** Use the same `processBlocks()` / `fetchPageContent()` for subsection content -- it already handles images inline. Just concatenate the markdown strings.

### Pitfall 2: Order Values After Flattening
**What goes wrong:** Current subsection order uses `(si+1)*100+ssi+1` (e.g., 101, 201). After flattening, sections should use simple sequential order (1, 2, 3...) within a week.
**How to avoid:** When sections are merged (subsections folded in), use `si + 1` for the section's order value.

### Pitfall 3: Duplicate Week-Level File
**What goes wrong:** Week 1 Course 1 has BOTH a `week-1-how-to-think-like-a-data-engineer.md` (order: 1) AND individual subsection files. After flattening, this needs to be resolved -- either the week page becomes the single page (if no sections) or sections replace it.
**How to avoid:** Audit current output to determine if the week-level .md file is a duplicate or contains unique content. The script's `if (weekChildren.length === 0)` branch creates this file only for leaf weeks -- but week 1 HAS children, so that file shouldn't exist. Investigate if it's from a previous run.

### Pitfall 4: Notion API Rate Limits
**What goes wrong:** Script makes many sequential API calls during deep traversal.
**How to avoid:** The script already works for 52 files + 120 images. Rate limiting is unlikely to be a new problem. No change needed.

### Pitfall 5: Table Without Header Row
**What goes wrong:** If `has_column_header` is false, no separator row is added, producing invalid markdown table.
**How to avoid:** Always add separator row after first row regardless of header flag. Markdown tables require the separator.

## Code Examples

### Subsection Merge (core change)
```javascript
// Replace lines 482-519 (subsection branch) with:
if (sectionChildren.length === 0) {
  // Section is a leaf -- existing logic is fine
} else {
  // Has subsections -- MERGE into parent section
  let content = await fetchPageContent(section.id);
  for (const sub of sectionChildren) {
    const subContent = await fetchPageContent(sub.id);
    content += `\n\n## ${sub.title}\n\n${subContent}`;
    // Check for deeper nesting
    const subChildren = await getChildPages(sub.id);
    for (const deep of subChildren) {
      const deepContent = await fetchPageContent(deep.id);
      content += `\n\n### ${deep.title}\n\n${deepContent}`;
    }
  }
  const sectionSlug = slugify(section.title.replace(/^[^\w]+/, ""));
  const mdxContent = buildMdx({
    title: section.title,
    course: course.title,
    courseSlug,
    courseOrder: ci + 1,
    week: week.title,
    weekSlug,
    weekOrder: wi + 1,
    order: si + 1,
    notionId: section.id,
    content,
  });
  fs.writeFileSync(path.join(weekDir, `${sectionSlug}.md`), mdxContent);
}
```

### href Fix in richTextToMd
```javascript
// Add after line 156 (before return text):
if (rt.href) {
  text = `[${text}](${rt.href})`;
}
```

## Open Questions

1. **Week-level page for Week 1 Course 1**
   - What we know: `week-1-how-to-think-like-a-data-engineer.md` exists with order: 1, alongside 12 subsection files
   - What's unclear: Does this file contain unique content or is it a leftover from a different traversal path?
   - Recommendation: Audit during implementation -- if it's empty/duplicate, remove it; if it has intro content, keep as order: 0 or merge into first section

2. **Heading levels after merge**
   - What we know: Subsection titles become `##` headings when merged. But subsections may already contain `##` headings in their content.
   - What's unclear: Will there be heading level conflicts?
   - Recommendation: Use `##` for subsection titles. If subsection content has `##`, bump those to `###`. Or accept as-is per D-05 (AI will reformat later).

## Sources

### Primary (HIGH confidence)
- `scripts/fetch-notion.mjs` -- direct code analysis (566 lines)
- `src/content.config.ts` -- Zod schema (direct read)
- Existing content output in `src/content/notes/` -- 52 files, 4 courses

### Secondary (MEDIUM confidence)
- `02-CONTEXT.md` -- user decisions from discussion phase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies, existing code works
- Architecture: HIGH -- changes are well-scoped to one file, patterns clear from code
- Pitfalls: HIGH -- identified from direct code reading, not speculation

**Research date:** 2026-03-31
**Valid until:** 2026-04-30 (stable -- single script, no external dependency changes)
