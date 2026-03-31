# Testing

## Status
No test framework configured. This is a static site generator focused on content delivery.

## What Exists
- No test files in source (only in `node_modules/`)
- No test scripts in `package.json`
- No test configuration (Vitest, Jest, etc.)
- No `.eslintrc`, `.prettierrc`, or linting setup detected

## Implications
- TDD will need to be set up as part of future phases
- Recommended: Vitest (compatible with Vite/Astro ecosystem)
- E2E testing could use Playwright (Astro officially supports it)

## Recommended Setup (future)
- Unit: Vitest
- E2E: Playwright
- Component: @testing-library/dom or Astro's built-in testing utilities
