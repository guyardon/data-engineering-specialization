# Phase 1 Context: Foundation & Tooling

**Phase:** 1 — Foundation & Tooling
**Created:** 2026-03-31
**Status:** Ready for planning

## Decisions

### ESLint Configuration

- Use `eslint-plugin-astro` + `@typescript-eslint/eslint-plugin` with recommended rules
- Include `eslint-plugin-prettier` to run Prettier as an ESLint rule (single pass)
- Rule severity: **errors only** — no noisy style warnings beyond what Prettier handles
- Target: zero errors, not zero opinions. Keep config minimal and non-blocking.

### Prettier Configuration

- Use Prettier for all formatting (`.astro`, `.ts`, `.js`, `.md`)
- Include `prettier-plugin-astro` for `.astro` file formatting
- Default Prettier settings are fine (no custom overrides needed)

### TypeScript Path Aliases

- **No path aliases** — keep relative imports as-is
- The project is small; aliases add config complexity without clear benefit yet
- Can revisit in Phase 3 if component imports become unwieldy

### Dependency Cleanup

- Move `zod`, `remark-gfm`, `node-fetch` from `dependencies` → `devDependencies`
- These are build-time or script-time only; not needed in the deployed static output
- `@notionhq/client` also goes to `devDependencies` (only used in fetch script)

### package.json Scripts to Add

```json
"lint": "eslint . --ext .ts,.astro,.js",
"lint:fix": "eslint . --ext .ts,.astro,.js --fix",
"typecheck": "astro check",
"format": "prettier --write ."
```

### What to NOT touch in Phase 1

- No UI changes
- No Notion sync changes
- No content schema changes
- Don't add Vitest/testing yet (deferred — no logic to test until content pipeline is built)

## Canonical Refs

- `.planning/REQUIREMENTS.md` — TOOL-01, TOOL-02, TOOL-03
- `.planning/codebase/STACK.md` — existing dependency list
- `.planning/codebase/CONCERNS.md` — known tech debt (no linting, no formatting)
- `package.json` — current scripts and dependencies
- `tsconfig.json` — TypeScript config (extends astro/tsconfigs/strict)

## Deferred Ideas

- Vitest unit testing — deferred to after content pipeline is built (nothing to test yet)
- Husky pre-commit hooks — nice to have, can add later
- Path aliases (`@components/`) — revisit in Phase 3 if needed
