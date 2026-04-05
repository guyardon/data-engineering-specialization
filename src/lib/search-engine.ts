// Pagefind raw JS API wrapper
// Replaces PagefindUI (pre-built Svelte IIFE) with direct API access

interface PagefindResult {
  id: string;
  data: () => Promise<PagefindResultData>;
}

interface PagefindSubResult {
  title: string;
  url: string;
  excerpt: string;
}

interface PagefindResultData {
  url: string;
  meta: { title?: string };
  excerpt: string;
  sub_results: PagefindSubResult[];
}

export interface SearchResult {
  title: string;
  url: string;
  excerpt: string;
}

interface PagefindInstance {
  debouncedSearch: (
    query: string,
    options?: Record<string, unknown>,
  ) => Promise<{ results: PagefindResult[] } | null>;
}

let pagefind: PagefindInstance | null = null;

const BASE_URL =
  typeof import.meta !== "undefined" && import.meta.env?.BASE_URL
    ? import.meta.env.BASE_URL.replace(/\/$/, "")
    : "/data-engineering-specialization-website";

export async function initPagefind(): Promise<boolean> {
  try {
    pagefind = await import(
      /* @vite-ignore */ `${BASE_URL}/pagefind/pagefind.js`
    );
    return true;
  } catch {
    return false; // dev mode — index doesn't exist
  }
}

// Search and return flat list of sub-results (subsection titles)
// Returns empty array if no results, query is empty, or search was superseded
export async function search(query: string): Promise<SearchResult[]> {
  if (!pagefind || !query.trim()) return [];

  const response = await pagefind.debouncedSearch(query);
  if (!response) return []; // superseded by newer query

  const dataPromises = response.results.slice(0, 10).map((r) => r.data());
  const items = await Promise.all(dataPromises);

  const results: SearchResult[] = [];
  for (const item of items) {
    if (item.sub_results && item.sub_results.length > 0) {
      for (const sub of item.sub_results) {
        results.push({
          title: sub.title,
          url: sub.url,
          excerpt: sub.excerpt,
        });
      }
    } else {
      // Fallback: use parent result if no sub-results
      results.push({
        title: item.meta?.title || "",
        url: item.url,
        excerpt: item.excerpt,
      });
    }
  }
  return results;
}
