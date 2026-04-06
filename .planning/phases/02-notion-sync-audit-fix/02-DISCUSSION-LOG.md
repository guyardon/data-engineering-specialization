# Phase 2: Notion Sync Audit & Fix - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-01
**Phase:** 02-notion-sync-audit-fix
**Areas discussed:** Hierarchy/Navigation Structure, Content Quality

---

## Hierarchy & Navigation Structure

| Option                   | Description                                                     | Selected |
| ------------------------ | --------------------------------------------------------------- | -------- |
| Flatten to week level    | Each week becomes one page with all sections inline             |          |
| Flatten to section level | Keep course→week→section, merge subsections into parent section | ✓        |
| Keep as-is               | Leave inconsistent nesting for AI to handle later               |          |

**User's choice:** Flatten to section level — subsections merge into parent section page. Sidebar shows Course > Week > Section.
**Notes:** User noted that early courses (1-2) are deeply nested (course→week→section→subsection) which is hard to navigate. Course 4 has everything at week level which is simpler. User wants sidebar to enable navigating through sections but subsections should be on the same page as their parent section.

---

## Content Quality

**User's choice:** Content is "raw" — AI will reformat later. Focus on structure, images, and frontmatter.
**Notes:** User explicitly said to use markdown files from Notion as "raw" pages. Images were placed strategically and must stay in original locations.

---

## Claude's Discretion

- Link handling (rt.href) — fix if encountered but not primary goal
- MDX escaping — fix obvious issues
- Callout format — keep as-is (raw content)

## Deferred Ideas

None
