/**
 * sql.js wrapper for the in-browser SQL sandbox.
 *
 * Loads sql.js from the official CDN on first use, creates a shared
 * in-memory SQLite database pre-populated with sample tables that
 * match the schemas referenced in the course notes.
 */
import { SETUP_SQL } from "./sample-data";

const SQLJS_VERSION = "1.13.0";
const SQLJS_CDN = `https://cdn.jsdelivr.net/npm/sql.js@${SQLJS_VERSION}/dist/`;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type SqlJsStatic = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type SqlDatabase = any;

declare global {
  interface Window {
    initSqlJs?: (opts: {
      locateFile: (file: string) => string;
    }) => Promise<SqlJsStatic>;
  }
}

let dbPromise: Promise<SqlDatabase> | null = null;

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(
      `script[data-src="${src}"]`,
    );
    if (existing) {
      if (existing.dataset.loaded === "true") {
        resolve();
        return;
      }
      existing.addEventListener("load", () => resolve());
      existing.addEventListener("error", () =>
        reject(new Error(`Failed to load ${src}`)),
      );
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.dataset.src = src;
    script.addEventListener("load", () => {
      script.dataset.loaded = "true";
      resolve();
    });
    script.addEventListener("error", () =>
      reject(new Error(`Failed to load ${src}`)),
    );
    document.head.appendChild(script);
  });
}

export async function initSQL(
  onProgress?: (message: string) => void,
): Promise<SqlDatabase> {
  if (dbPromise) return dbPromise;

  dbPromise = (async () => {
    onProgress?.("Downloading SQLite engine (~1MB, one-time)...");
    await loadScript(`${SQLJS_CDN}sql-wasm.js`);
    if (!window.initSqlJs) {
      throw new Error("sql.js failed to load");
    }
    onProgress?.("Initializing database...");
    const SQL = await window.initSqlJs({
      locateFile: (file: string) => `${SQLJS_CDN}${file}`,
    });
    const db = new SQL.Database();
    db.exec(SETUP_SQL);
    onProgress?.("Ready");
    return db;
  })();

  try {
    return await dbPromise;
  } catch (err) {
    dbPromise = null;
    throw err;
  }
}

export interface SqlResult {
  tables: Array<{ columns: string[]; rows: unknown[][] }>;
  error?: string;
  rowsAffected?: number;
}

/**
 * Execute SQL and return results as an array of result sets.
 * (A single script can contain multiple statements; each SELECT
 * produces its own result table.)
 */
export async function runSQL(
  query: string,
  onProgress?: (message: string) => void,
): Promise<SqlResult> {
  const db = await initSQL(onProgress);

  try {
    const results = db.exec(query) as Array<{
      columns: string[];
      values: unknown[][];
    }>;
    const tables = results.map((r) => ({
      columns: r.columns,
      rows: r.values,
    }));
    // If no SELECT produced rows but the query succeeded (e.g., INSERT),
    // report rows affected via sql.js `getRowsModified`.
    const rowsAffected =
      tables.length === 0
        ? (db.getRowsModified?.() as number | undefined)
        : undefined;
    return { tables, rowsAffected };
  } catch (err) {
    return {
      tables: [],
      error: err instanceof Error ? err.message : String(err),
    };
  }
}
