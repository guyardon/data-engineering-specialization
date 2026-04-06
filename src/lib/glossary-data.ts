/**
 * Pure data query functions for the glossary page.
 * No DOM dependencies — fully testable.
 */

export interface GlossaryCategory {
  category: string;
  icon: string;
  terms: GlossaryTerm[];
}

export interface GlossaryTerm {
  term: string;
  description?: string;
  diagram?: string;
  relatedTerms?: string[];
  notes: { slug: string; title: string; href: string }[];
}

export interface TermEntry {
  term: GlossaryTerm;
  ci: number;
  ti: number;
}

/** Build a flat, alphabetically sorted list of all terms across categories. */
export function buildAllTerms(data: GlossaryCategory[]): TermEntry[] {
  const entries: TermEntry[] = [];
  data.forEach((cat, ci) => {
    cat.terms.forEach((term, ti) => {
      entries.push({ term, ci, ti });
    });
  });
  entries.sort((a, b) => a.term.term.localeCompare(b.term.term));
  return entries;
}

/** Get terms for a specific category or all terms sorted. */
export function getTermsForCategory(
  data: GlossaryCategory[],
  category: "all" | number,
  allTerms: TermEntry[],
): TermEntry[] {
  if (category === "all") return allTerms;
  return data[category].terms.map((term, ti) => ({ term, ci: category, ti }));
}

/** Find a term entry by exact name across all categories. */
export function findTermByName(
  data: GlossaryCategory[],
  name: string,
): TermEntry | null {
  for (let ci = 0; ci < data.length; ci++) {
    const terms = data[ci].terms;
    for (let ti = 0; ti < terms.length; ti++) {
      if (terms[ti].term === name) return { term: terms[ti], ci, ti };
    }
  }
  return null;
}

/** Pick a random term from pool, excluding the one with the given key. */
export function pickRandomTerm(
  pool: TermEntry[],
  excludeKey: string | null,
): TermEntry | null {
  if (pool.length === 0) return null;
  const candidates = excludeKey
    ? pool.filter((e) => termKey(e.ci, e.ti) !== excludeKey)
    : pool;
  if (candidates.length === 0) return null;
  return candidates[Math.floor(Math.random() * candidates.length)];
}

/** Build the composite key used for term identity. */
export function termKey(ci: number, ti: number): string {
  return `${ci}-${ti}`;
}
