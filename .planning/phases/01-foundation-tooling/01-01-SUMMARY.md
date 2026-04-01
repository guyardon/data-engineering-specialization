---
phase: 01-foundation-tooling
plan: "01"
subsystem: tooling
tags: [eslint, prettier, typescript-eslint, eslint-plugin-astro, eslint-plugin-prettier, prettier-plugin-astro]

requires: []
provides:
  - ESLint flat config (eslint.config.mjs) with typescript-eslint + astro + prettier layers
  - Prettier config (.prettierrc) with prettier-plugin-astro
  - Zero-error lint baseline across all .ts, .astro, .js source files
  - npm scripts: lint, lint:fix, typecheck, format
affects: [02-notion-sync-audit, 03-ui-design-system, 04-content-rendering, 05-deploy-cicd]

tech-stack:
  added: [eslint@10, @eslint/js, typescript-eslint, eslint-plugin-astro, eslint-plugin-prettier, eslint-config-prettier, prettier-plugin-astro, globals]
  patterns:
    - ESLint flat config (eslint.config.mjs) with tseslint.config() wrapper
    - prettier/prettier rule disabled for Astro virtual TS files (*.astro/*.ts glob)
    - Node globals scoped to scripts/ directory only

key-files:
  created:
    - eslint.config.mjs
    - .prettierrc
    - .prettierignore
  modified:
    - package.json
    - scripts/fetch-notion.mjs

key-decisions:
  - "prettier/prettier ESLint rule disabled for Astro virtual TS files: astro processor creates *.astro/*.ts virtual files that match **/*.ts glob, causing prettier to fail on TypeScript generics in script blocks. Formatting enforced via npm run format (prettier CLI) instead."
  - "globals package added as devDependency for Node.js environment in scripts/ directory"
  - "getPageTitle unused function in fetch-notion.mjs suppressed with eslint-disable comment (kept for future use)"

patterns-established:
  - "Flat config format (eslint.config.mjs) — no legacy .eslintrc files"
  - "Prettier as ESLint rule for TS/JS/MJS only, not .astro files"
  - "eslint-disable-next-line comments for intentionally unused utility functions"

requirements-completed: [TOOL-01]

duration: 35min
completed: 2026-03-31
---

# Phase 01 Plan 01: ESLint + Prettier Tooling Summary

**ESLint flat config with typescript-eslint, eslint-plugin-astro, and eslint-plugin-prettier installed and zero errors on all .ts, .astro, and .js source files**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-03-31T19:24:00Z
- **Completed:** 2026-03-31T20:00:00Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Installed 10 ESLint/Prettier devDependencies and moved 4 runtime deps to devDependencies
- Created `eslint.config.mjs` with three plugin layers: typescript-eslint recommended, eslint-plugin-astro recommended, eslint-plugin-prettier
- Achieved `npm run lint` exit 0 with zero errors across all source files
- Achieved `npm run format -- --check` exit 0 (all files already formatted)

## Task Commits

1. **Task 1: Install ESLint and Prettier packages** - `728e8ae` (chore)
2. **Task 2: Create eslint.config.mjs, .prettierrc, .prettierignore, and add scripts** - `0241962` (chore)
3. **Task 3: Run lint and format — achieve zero errors** - `7498b41` (chore)

## Files Created/Modified

- `eslint.config.mjs` - ESLint flat config: typescript-eslint + astro + prettier layers, node globals for scripts, virtual astro TS file override
- `.prettierrc` - Prettier config with prettier-plugin-astro and astro parser override
- `.prettierignore` - Excludes dist/, node_modules/, .astro/, public/
- `package.json` - 10 new devDependencies, 4 deps moved to devDependencies, 4 new scripts
- `scripts/fetch-notion.mjs` - Added eslint-disable comment for unused utility function

## Decisions Made

- Used `eslint-plugin-prettier` only for `**/*.ts`, `**/*.mjs`, `**/*.js`, `**/*.cjs` files — excluded `.astro` because the astro processor creates virtual `*.astro/*.ts` files that match the `**/*.ts` glob. Prettier fails to parse TypeScript generics in isolated script blocks without a full file context.
- Added an explicit `prettier/prettier: "off"` override for `**/*.astro/*.ts` and `**/*.astro/*.js` patterns (AFTER the prettier plugin config entry) to prevent the glob from re-enabling the rule.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added `globals` package for Node.js environment in scripts/**

- **Found during:** Task 3 (zero errors goal)
- **Issue:** `process`, `console` reported as undefined — no node globals configured
- **Fix:** Installed `globals` devDependency; added `languageOptions.globals: globals.node` for `scripts/**/*.mjs` in eslint.config.mjs
- **Files modified:** eslint.config.mjs, package.json, package-lock.json
- **Verification:** `npm run lint` reports no `no-undef` errors for scripts/
- **Committed in:** 7498b41 (Task 3 commit)

**2. [Rule 1 - Bug] Fixed eslint-plugin-prettier parse errors on Astro virtual TS files**

- **Found during:** Task 3 (zero errors goal)
- **Issue:** eslint-plugin-prettier configured for `**/*.ts` matches virtual `*.astro/*.ts` files created by the astro processor. Prettier fails to parse isolated TypeScript script content (e.g., `querySelectorAll<HTMLAnchorElement>`).
- **Fix:** Added explicit `prettier/prettier: "off"` config entry for `**/*.astro/*.ts` and `**/*.astro/*.js` patterns, placed AFTER the prettier plugin config entry to ensure override takes effect.
- **Files modified:** eslint.config.mjs
- **Verification:** `npm run lint` reports no prettier/prettier errors on .astro files
- **Committed in:** 7498b41 (Task 3 commit)

**3. [Rule 2 - Missing Critical] Suppressed unused `getPageTitle` function lint error**

- **Found during:** Task 3 (zero errors goal)
- **Issue:** `getPageTitle` defined but never called in scripts/fetch-notion.mjs
- **Fix:** Added `// eslint-disable-next-line @typescript-eslint/no-unused-vars` comment to suppress the error — function kept for future use
- **Files modified:** scripts/fetch-notion.mjs
- **Committed in:** 7498b41 (Task 3 commit)

---

**Total deviations:** 3 auto-fixed (1 blocking, 1 bug, 1 missing critical)
**Impact on plan:** All auto-fixes required to achieve zero-error lint baseline. The astro virtual TS file issue is an important discovery about eslint-plugin-prettier + astro processor interaction.

## Issues Encountered

- ESLint flat config plugin scope: in flat config, plugins registered in any file-scoped config entry become globally available to all files. This caused `prettier/prettier` errors to appear on `.astro` virtual files even when not intended. Required explicit per-pattern overrides placed in correct array order.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Lint/format tooling fully operational for all source files
- `npm run lint` is zero-error baseline — all future code must pass this check
- Ready for Phase 01 Plan 02 (GitHub Actions CI/CD)

---

_Phase: 01-foundation-tooling_
_Completed: 2026-03-31_
