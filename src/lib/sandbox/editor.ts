/**
 * CodeMirror 6 wrapper for the sandbox.
 *
 * Creates an editor tuned for short snippets: line numbers, syntax
 * highlighting, Ctrl/Cmd+Enter to run, and a theme that follows the
 * site's [data-theme] attribute (same pattern as Mermaid.astro).
 */
import { EditorState, Compartment } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLine } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { bracketMatching, indentOnInput } from "@codemirror/language";
import { python } from "@codemirror/lang-python";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

export type EditorLanguage = "python" | "sql";

export interface EditorHandle {
  view: EditorView;
  getCode: () => string;
  destroy: () => void;
}

const themeCompartment = new Compartment();

function isDark(): boolean {
  return document.documentElement.getAttribute("data-theme") !== "light";
}

function themeExtension() {
  return isDark() ? oneDark : [];
}

export function createEditor(
  container: HTMLElement,
  code: string,
  language: EditorLanguage,
  onRun: () => void,
): EditorHandle {
  const langExt = language === "python" ? python() : sql();

  const state = EditorState.create({
    doc: code,
    extensions: [
      lineNumbers(),
      highlightActiveLine(),
      history(),
      bracketMatching(),
      indentOnInput(),
      langExt,
      themeCompartment.of(themeExtension()),
      keymap.of([
        ...defaultKeymap,
        ...historyKeymap,
        {
          key: "Mod-Enter",
          run: () => {
            onRun();
            return true;
          },
        },
      ]),
      EditorView.theme({
        "&": { fontSize: "0.8rem", borderRadius: "0" },
        ".cm-scroller": { fontFamily: "var(--font-mono)" },
        ".cm-content": { padding: "0.75rem 0" },
      }),
    ],
  });

  const view = new EditorView({ state, parent: container });

  // Keep editor theme in sync with site theme.
  const observer = new MutationObserver(() => {
    view.dispatch({
      effects: themeCompartment.reconfigure(themeExtension()),
    });
  });
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });

  return {
    view,
    getCode: () => view.state.doc.toString(),
    destroy: () => {
      observer.disconnect();
      view.destroy();
    },
  };
}
