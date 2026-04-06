/**
 * Generic pagination algorithm for the glossary page.
 * Pure logic — DOM measurement injected via fitsOnPage callback (DIP).
 */

/**
 * Compute page break indices.
 *
 * @param totalItems - Number of items to paginate
 * @param fitsOnPage - Callback: (startIndex, count) => true if `count` items
 *   starting at `startIndex` fit within the allowed space.
 *   The caller provides DOM measurement here.
 * @returns Array of start indices for each page, e.g. [0, 5, 10]
 */
export function computePageBreaks(
  totalItems: number,
  fitsOnPage: (startIndex: number, count: number) => boolean,
): number[] {
  if (totalItems === 0) return [0];

  const breaks: number[] = [0];
  let cursor = 0;

  while (cursor < totalItems) {
    // Find how many items fit starting at cursor
    let count = 1;
    while (cursor + count < totalItems && fitsOnPage(cursor, count + 1)) {
      count++;
    }
    cursor += count;
    if (cursor < totalItems) {
      breaks.push(cursor);
    }
  }

  return breaks;
}

/** Given pageBreaks and an item index, return the page number containing it. */
export function findPageForIndex(pageBreaks: number[], index: number): number {
  for (let pg = pageBreaks.length - 1; pg >= 0; pg--) {
    if (pageBreaks[pg] <= index) return pg;
  }
  return 0;
}

/** Given pageBreaks and a page number, return [startIndex, endIndex). */
export function getPageRange(
  pageBreaks: number[],
  page: number,
  totalItems: number,
): [number, number] {
  const start = pageBreaks[page];
  const end = page + 1 < pageBreaks.length ? pageBreaks[page + 1] : totalItems;
  return [start, end];
}
