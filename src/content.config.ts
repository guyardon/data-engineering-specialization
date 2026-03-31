import { defineCollection } from "astro:content";
import { z } from "zod";
import { glob } from "astro/loaders";

const notes = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/notes" }),
  schema: z.object({
    title: z.string(),
    course: z.string(),
    courseSlug: z.string(),
    courseOrder: z.number(),
    week: z.string(),
    weekSlug: z.string(),
    weekOrder: z.number(),
    order: z.number(),
    notionId: z.string().optional(),
  }),
});

export const collections = { notes };
