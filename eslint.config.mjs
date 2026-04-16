// @ts-check
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import astro from "eslint-plugin-astro";
import prettierPlugin from "eslint-plugin-prettier";
import prettierConfig from "eslint-config-prettier";
import globals from "globals";

export default tseslint.config(
  // Base JS recommended rules
  js.configs.recommended,

  // TypeScript recommended rules
  ...tseslint.configs.recommended,

  // Astro recommended rules (handles .astro parsing)
  // Note: this also sets prettier/prettier: "off" for *.astro/*.ts virtual files
  ...astro.configs.recommended,

  // Prettier config — turns off ESLint formatting rules that conflict with Prettier
  prettierConfig,

  // Prettier as ESLint rule for TS/JS/MJS/CJS files only.
  // Excluded from .astro files: the astro processor creates virtual *.astro/*.ts
  // files that match **/*.ts — we override those back to "off" below.
  {
    files: ["**/*.ts", "**/*.mjs", "**/*.js", "**/*.cjs"],
    plugins: {
      prettier: prettierPlugin,
    },
    rules: {
      "prettier/prettier": "error",
    },
  },

  // Re-disable prettier/prettier for Astro virtual script files.
  // The astro processor creates virtual files like *.astro/*.ts and *.astro/*.js.
  // These match the **/*.ts glob above, so we must explicitly turn them off here
  // (AFTER the prettier plugin config) to prevent parse errors from prettier
  // not understanding the isolated script content.
  {
    files: [
      "**/*.astro/*.ts",
      "*.astro/*.ts",
      "**/*.astro/*.js",
      "*.astro/*.js",
    ],
    rules: {
      "prettier/prettier": "off",
    },
  },

  // Node.js scripts — add node globals
  {
    files: ["scripts/**/*.mjs", "scripts/**/*.js"],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    rules: {
      // Allow empty catch blocks in Node scripts (common pattern)
      "no-empty": ["error", { allowEmptyCatch: true }],
    },
  },

  // Project-wide settings
  {
    rules: {
      // Keep everything else at recommended (error) level
      "@typescript-eslint/no-explicit-any": "error",
    },
  },

  // Ignore generated/build output
  {
    ignores: ["dist/**", "node_modules/**", ".astro/**"],
  },
);
