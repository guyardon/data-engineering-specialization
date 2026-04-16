/**
 * Pyodide wrapper for the in-browser Python sandbox.
 *
 * Loads Pyodide from the official CDN on first use, caches the singleton,
 * and exposes a simple `runPython` function that captures stdout/stderr.
 */

const PYODIDE_VERSION = "0.28.0";
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type PyodideInterface = any;

declare global {
  interface Window {
    loadPyodide?: (opts: { indexURL: string }) => Promise<PyodideInterface>;
  }
}

let pyodidePromise: Promise<PyodideInterface> | null = null;

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

export async function initPython(
  onProgress?: (message: string) => void,
): Promise<PyodideInterface> {
  if (pyodidePromise) return pyodidePromise;

  pyodidePromise = (async () => {
    onProgress?.("Downloading Python runtime (~7MB, one-time)...");
    await loadScript(`${PYODIDE_CDN}pyodide.js`);
    if (!window.loadPyodide) {
      throw new Error("Pyodide failed to load");
    }
    onProgress?.("Initializing Python...");
    const pyodide = await window.loadPyodide({ indexURL: PYODIDE_CDN });
    onProgress?.("Ready");
    return pyodide;
  })();

  try {
    return await pyodidePromise;
  } catch (err) {
    // Allow retry on failure
    pyodidePromise = null;
    throw err;
  }
}

export interface PythonResult {
  stdout: string;
  stderr: string;
  error?: string;
}

/**
 * Execute Python code and capture stdout/stderr.
 * Uses `io.StringIO` redirect so print() output is captured instead of
 * flooding the browser console.
 */
export async function runPython(
  code: string,
  onProgress?: (message: string) => void,
): Promise<PythonResult> {
  const pyodide = await initPython(onProgress);

  // Set up stdout/stderr capture.
  pyodide.runPython(`
import sys
import io
_sandbox_stdout = io.StringIO()
_sandbox_stderr = io.StringIO()
sys.stdout = _sandbox_stdout
sys.stderr = _sandbox_stderr
`);

  let errorMessage: string | undefined;
  try {
    await pyodide.runPythonAsync(code);
  } catch (err) {
    errorMessage = err instanceof Error ? err.message : String(err);
  }

  const stdout = pyodide.runPython("_sandbox_stdout.getvalue()") as string;
  const stderr = pyodide.runPython("_sandbox_stderr.getvalue()") as string;

  // Restore streams so subsequent runs start fresh.
  pyodide.runPython(`
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
`);

  return { stdout, stderr, error: errorMessage };
}
