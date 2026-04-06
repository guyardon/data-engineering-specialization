import { describe, expect, it } from "vitest";
import {
  computePageBreaks,
  findPageForIndex,
  getPageRange,
} from "./glossary-pagination";

describe("computePageBreaks", () => {
  it("returns [0] when all items fit on one page", () => {
    const breaks = computePageBreaks(10, () => true);
    expect(breaks).toEqual([0]);
  });

  it("splits into pages based on fitsOnPage callback", () => {
    // Max 3 items per page, 8 total → pages at [0, 3, 6]
    const breaks = computePageBreaks(8, (_start, count) => count <= 3);
    expect(breaks).toEqual([0, 3, 6]);
  });

  it("handles zero items", () => {
    const breaks = computePageBreaks(0, () => true);
    expect(breaks).toEqual([0]);
  });

  it("handles exactly one page boundary", () => {
    // 6 items, max 3 per page → [0, 3]
    const breaks = computePageBreaks(6, (_start, count) => count <= 3);
    expect(breaks).toEqual([0, 3]);
  });

  it("handles single-item pages when callback is very restrictive", () => {
    // Only 1 item fits at a time
    const breaks = computePageBreaks(4, (_start, count) => count <= 1);
    expect(breaks).toEqual([0, 1, 2, 3]);
  });

  it("handles varying page sizes based on start position", () => {
    // First page fits 4, rest fit 3
    const breaks = computePageBreaks(10, (start, count) => {
      const max = start === 0 ? 4 : 3;
      return count <= max;
    });
    expect(breaks).toEqual([0, 4, 7]);
  });
});

describe("findPageForIndex", () => {
  const breaks = [0, 5, 10, 15];

  it("returns 0 for index on first page", () => {
    expect(findPageForIndex(breaks, 0)).toBe(0);
    expect(findPageForIndex(breaks, 4)).toBe(0);
  });

  it("returns correct page for mid-range index", () => {
    expect(findPageForIndex(breaks, 5)).toBe(1);
    expect(findPageForIndex(breaks, 9)).toBe(1);
    expect(findPageForIndex(breaks, 10)).toBe(2);
  });

  it("returns last page for final items", () => {
    expect(findPageForIndex(breaks, 15)).toBe(3);
    expect(findPageForIndex(breaks, 20)).toBe(3);
  });

  it("handles single-page case", () => {
    expect(findPageForIndex([0], 5)).toBe(0);
  });
});

describe("getPageRange", () => {
  const breaks = [0, 5, 10];
  const total = 13;

  it("returns [start, end) for first page", () => {
    expect(getPageRange(breaks, 0, total)).toEqual([0, 5]);
  });

  it("returns [start, end) for middle page", () => {
    expect(getPageRange(breaks, 1, total)).toEqual([5, 10]);
  });

  it("returns [lastBreak, totalItems) for last page", () => {
    expect(getPageRange(breaks, 2, total)).toEqual([10, 13]);
  });

  it("returns [0, totalItems) for single page", () => {
    expect(getPageRange([0], 0, 8)).toEqual([0, 8]);
  });
});
