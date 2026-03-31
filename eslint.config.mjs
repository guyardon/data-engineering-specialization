// @ts-check
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import astro from 'eslint-plugin-astro';
import prettier from 'eslint-plugin-prettier/recommended';

export default tseslint.config(
  // Base JS recommended rules
  js.configs.recommended,

  // TypeScript recommended rules
  ...tseslint.configs.recommended,

  // Astro recommended rules (handles .astro parsing)
  ...astro.configs.recommended,

  // Prettier as ESLint rule — must be last to override formatting rules
  prettier,

  // Project-wide settings
  {
    rules: {
      // Downgrade TypeScript hints that would be noisy to off
      // Keep everything else at recommended (error) level
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },

  // Ignore generated/build output
  {
    ignores: ['dist/**', 'node_modules/**', '.astro/**'],
  },
);
