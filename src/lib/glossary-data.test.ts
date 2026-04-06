import { describe, expect, it } from "vitest";
import {
  buildAllTerms,
  findTermByName,
  getTermsForCategory,
  pickRandomTerm,
  termKey,
  type GlossaryCategory,
} from "./glossary-data";

const TEST_DATA: GlossaryCategory[] = [
  {
    category: "Storage",
    icon: "💾",
    terms: [
      {
        term: "Data Lake",
        description: "A lake of data",
        notes: [{ slug: "s1", title: "S1", href: "/s1" }],
      },
      {
        term: "Data Warehouse",
        notes: [{ slug: "s2", title: "S2", href: "/s2" }],
      },
    ],
  },
  {
    category: "Processing",
    icon: "⚙️",
    terms: [
      {
        term: "Batch Processing",
        relatedTerms: ["Data Lake"],
        notes: [{ slug: "p1", title: "P1", href: "/p1" }],
      },
      {
        term: "Stream Processing",
        notes: [{ slug: "p2", title: "P2", href: "/p2" }],
      },
      {
        term: "ETL",
        notes: [],
      },
    ],
  },
];

describe("buildAllTerms", () => {
  it("returns flat list sorted alphabetically by term name", () => {
    const result = buildAllTerms(TEST_DATA);
    const names = result.map((e) => e.term.term);
    expect(names).toEqual([
      "Batch Processing",
      "Data Lake",
      "Data Warehouse",
      "ETL",
      "Stream Processing",
    ]);
  });

  it("preserves ci/ti indices correctly", () => {
    const result = buildAllTerms(TEST_DATA);
    const batchEntry = result.find((e) => e.term.term === "Batch Processing")!;
    expect(batchEntry.ci).toBe(1);
    expect(batchEntry.ti).toBe(0);

    const lakeEntry = result.find((e) => e.term.term === "Data Lake")!;
    expect(lakeEntry.ci).toBe(0);
    expect(lakeEntry.ti).toBe(0);
  });

  it("returns empty array for empty data", () => {
    expect(buildAllTerms([])).toEqual([]);
  });
});

describe("getTermsForCategory", () => {
  const allTerms = buildAllTerms(TEST_DATA);

  it('returns all terms sorted when category is "all"', () => {
    const result = getTermsForCategory(TEST_DATA, "all", allTerms);
    expect(result).toEqual(allTerms);
    expect(result.length).toBe(5);
  });

  it("returns only terms from specified category index", () => {
    const result = getTermsForCategory(TEST_DATA, 0, allTerms);
    const names = result.map((e) => e.term.term);
    expect(names).toEqual(["Data Lake", "Data Warehouse"]);
  });

  it("returns terms with correct ci/ti for numeric category", () => {
    const result = getTermsForCategory(TEST_DATA, 1, allTerms);
    expect(result[0].ci).toBe(1);
    expect(result[0].ti).toBe(0);
    expect(result[1].ci).toBe(1);
    expect(result[1].ti).toBe(1);
  });
});

describe("findTermByName", () => {
  it("finds term that exists", () => {
    const result = findTermByName(TEST_DATA, "ETL");
    expect(result).not.toBeNull();
    expect(result!.term.term).toBe("ETL");
    expect(result!.ci).toBe(1);
    expect(result!.ti).toBe(2);
  });

  it("returns null for unknown term name", () => {
    expect(findTermByName(TEST_DATA, "NonExistent")).toBeNull();
  });

  it("matches exact name (case-sensitive)", () => {
    expect(findTermByName(TEST_DATA, "etl")).toBeNull();
  });
});

describe("pickRandomTerm", () => {
  const pool = buildAllTerms(TEST_DATA);

  it("returns a term from the pool", () => {
    const result = pickRandomTerm(pool, null);
    expect(result).not.toBeNull();
    expect(pool).toContainEqual(result);
  });

  it("excludes the term matching excludeKey", () => {
    // Pool of 2 items, exclude one — must return the other
    const smallPool = pool.slice(0, 2);
    const excludeKey = termKey(smallPool[0].ci, smallPool[0].ti);
    const result = pickRandomTerm(smallPool, excludeKey);
    expect(result).not.toBeNull();
    expect(termKey(result!.ci, result!.ti)).not.toBe(excludeKey);
  });

  it("returns null for empty pool", () => {
    expect(pickRandomTerm([], null)).toBeNull();
  });

  it("returns null for single-item pool when that item is excluded", () => {
    const single = [pool[0]];
    const key = termKey(single[0].ci, single[0].ti);
    expect(pickRandomTerm(single, key)).toBeNull();
  });
});

describe("termKey", () => {
  it('returns "ci-ti" format string', () => {
    expect(termKey(2, 5)).toBe("2-5");
    expect(termKey(0, 0)).toBe("0-0");
  });
});
