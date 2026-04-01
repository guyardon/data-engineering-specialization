# Code Conventions

## File Naming

- camelCase with `.mjs` extension for scripts
- PascalCase for Astro components (`.astro`)
- kebab-case for page routes and content files

## Code Style

- TypeScript: strict mode, no `any`
- Indentation: 2 spaces
- Styling: Tailwind CSS utility classes
- Async/await throughout (no raw Promise chains)

## Import Organization

1. Astro utilities / framework imports
2. Node built-ins
3. Relative imports

## Type Validation

- Zod schemas used for content configuration (Astro content collections)

## Function Design

- Functions kept under 50 lines
- Descriptive variable names
- Optional chaining (`?.`) and nullish coalescing (`??`) preferred

## Error Handling

- Try-catch blocks for async operations
- Console-only logging (no framework)

## Comments

- Added for complex logic only
- No redundant inline comments
