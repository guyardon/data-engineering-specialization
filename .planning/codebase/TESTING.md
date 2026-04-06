# Testing Patterns

## Test Frameworks

| Framework | Language   | Version                  | Config File        |
| --------- | ---------- | ------------------------ | ------------------ |
| pytest    | Python     | `>=8.0` (dev dependency) | `pyproject.toml`   |
| Vitest    | TypeScript | `^4.1.2`                 | `vitest.config.ts` |

---

## How to Run Tests

### Python (pytest)

```bash
# From project root, using the venv
.venv/bin/pytest --tb=short -q

# Or via uv
uv run pytest
```

### TypeScript (Vitest)

```bash
# Watch mode (default)
npm test

# Single run
npm run test:run

# Or directly
npx vitest run
```

### Via Pre-commit (both at once)

```bash
# Runs all hooks including both test suites
pre-commit run --all-files
```

---

## Vitest Configuration

File: `vitest.config.ts`

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.ts"],
    environment: "node",
  },
});
```

- Test discovery: `src/**/*.test.ts` (co-located with source files)
- Environment: `node` (not jsdom) -- tests target pure logic, not DOM
- No setup files or global config

---

## Test File Locations

### Python Tests

All in `tests/` directory at the project root:

| Test File                   | Tests For                            |
| --------------------------- | ------------------------------------ |
| `tests/test_aws_diagram.py` | `diagrams/diagramlib/aws_diagram.py` |
| `tests/test_colors.py`      | `diagrams/diagramlib/colors.py`      |
| `tests/test_excalidraw.py`  | `diagrams/diagramlib/excalidraw.py`  |

Supporting files:

- `tests/__init__.py` -- makes tests a package
- `tests/fixtures/` -- golden JSON files (e.g., `golden-batch-vs-streaming.json`)

### TypeScript Tests

Co-located with source in `src/lib/`:

| Test File                             | Tests For                        |
| ------------------------------------- | -------------------------------- |
| `src/lib/glossary-data.test.ts`       | `src/lib/glossary-data.ts`       |
| `src/lib/glossary-pagination.test.ts` | `src/lib/glossary-pagination.ts` |

---

## Python Test Patterns

### Test Organization

Tests use **class-based grouping** with descriptive class names. No `conftest.py` files exist.

```python
# tests/test_aws_diagram.py
class TestThemeColors:
    def test_light_cluster_colors_have_required_keys(self): ...
    def test_dark_cluster_colors_have_required_keys(self): ...
    def test_same_color_names_in_both_themes(self): ...
    def test_has_standard_colors(self): ...

class TestGraphAttrs:
    def test_light_mode(self): ...
    def test_dark_mode(self): ...
    def test_custom_rankdir(self): ...
```

### Assertion Style

Plain `assert` with descriptive failure messages in loops:

```python
def test_light_cluster_colors_have_required_keys(self):
    for name, c in CLUSTER_COLORS_LIGHT.items():
        assert "bg" in c, f"Light {name} missing 'bg'"
        assert "fc" in c, f"Light {name} missing 'fc'"
        assert "border" in c, f"Light {name} missing 'border'"
```

### Testing Return Values

Functions are tested by calling them with known inputs and asserting specific dict keys:

```python
def test_light_mode(self):
    attrs = graph_attrs(dark=False, title="Test Diagram")
    assert attrs["bgcolor"] == "white"
    assert attrs["fontcolor"] == "#1e1e1e"
    assert attrs["label"] == "Test Diagram\n\n"
    assert attrs["labelloc"] == "t"
    assert attrs["dpi"] == "150"
    assert attrs["rankdir"] == "LR"
```

### Dark/Light Variant Testing

Many tests verify both theme variants, often in separate test methods:

```python
def test_dark_uses_dark_colors(self):
    light = cluster_attrs("blue", dark=False)
    dark = cluster_attrs("blue", dark=True)
    assert light["bgcolor"] != dark["bgcolor"]
    assert light["fontcolor"] != dark["fontcolor"]
```

### Fixtures (pytest built-in)

`tmp_path` is used for file I/O tests:

```python
class TestSave:
    def test_writes_valid_json(self, tmp_path):
        d = ExcalidrawDiagram()
        d.rect("r1", 0, 0, 100, 50, "#000", "#fff")
        path = tmp_path / "test.excalidraw"
        d.save(str(path))
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["type"] == "excalidraw"
        assert len(loaded["elements"]) == 1
```

### Color Validation Pattern

Regex-based validation for hex color format:

```python
HEX_RE = re.compile(r"^#[0-9a-f]{6}$")

def test_all_colors_are_tuples_of_two_hex_strings():
    for name, color in ALL_COLORS:
        assert isinstance(color, tuple), f"{name} should be a tuple"
        assert len(color) == 2, f"{name} should have exactly 2 elements"
        stroke, bg = color
        assert HEX_RE.match(stroke), f"{name}[0] '{stroke}' is not a valid hex color"
```

### Property-Style Tests

Some tests verify invariants rather than exact values:

```python
def test_stroke_is_darker_than_background():
    """Stroke colors should be darker (lower RGB values) than backgrounds."""
    for name, (stroke, bg) in ALL_COLORS:
        s_val = int(stroke[1:], 16)
        b_val = int(bg[1:], 16)
        s_sum = (s_val >> 16) + ((s_val >> 8) & 0xFF) + (s_val & 0xFF)
        b_sum = (b_val >> 16) + ((b_val >> 8) & 0xFF) + (b_val & 0xFF)
        assert b_sum > s_sum, f"{name} background should be lighter than stroke"
```

### ExcalidrawDiagram Test Coverage

The `test_excalidraw.py` file is the most comprehensive, testing:

- **Initialization**: valid structure, custom seed, elements property
- **Seed generation**: sequential increments, uniqueness across 50 elements
- **Each element type**: `rect`, `txt`, `arr`, `line`, `diamond` with basic and optional params
- **Builder options**: fill style, stroke width, dashing, opacity, bound elements, bindings
- **Container text centering**: math verification of vertical centering calculation
- **Default isolation**: bound elements default `[]` not shared across instances
- **Serialization**: valid JSON output, parent directory creation, indent formatting
- **Accumulation**: multiple element types in order

---

## TypeScript Test Patterns

### Test Organization

Tests use **`describe`/`it` blocks** (Vitest's BDD API):

```typescript
import { describe, expect, it } from "vitest";

describe("buildAllTerms", () => {
  it("returns flat list sorted alphabetically by term name", () => { ... });
  it("preserves ci/ti indices correctly", () => { ... });
  it("returns empty array for empty data", () => { ... });
});
```

### Test Data

Inline test data constants defined at module level:

```typescript
const TEST_DATA: GlossaryCategory[] = [
  {
    category: "Storage",
    icon: "disk-emoji",
    terms: [
      {
        term: "Data Lake",
        description: "A lake of data",
        notes: [{ slug: "s1", title: "S1", href: "/s1" }],
      },
      // ...
    ],
  },
  // ...
];
```

### Assertion Style

Vitest's `expect` with `.toEqual`, `.toBe`, `.not.toBeNull()`, `.toContainEqual`:

```typescript
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
```

### Edge Cases

Both test files cover edge cases systematically:

```typescript
it("returns empty array for empty data", () => {
  expect(buildAllTerms([])).toEqual([]);
});

it("returns null for empty pool", () => {
  expect(pickRandomTerm([], null)).toBeNull();
});

it("returns null for single-item pool when that item is excluded", () => {
  const single = [pool[0]];
  const key = termKey(single[0].ci, single[0].ti);
  expect(pickRandomTerm(single, key)).toBeNull();
});
```

### Callback-Based Testing

The pagination tests inject behavior via callbacks to test the algorithm:

```typescript
it("splits into pages based on fitsOnPage callback", () => {
  // Max 3 items per page, 8 total -> pages at [0, 3, 6]
  const breaks = computePageBreaks(8, (_start, count) => count <= 3);
  expect(breaks).toEqual([0, 3, 6]);
});

it("handles varying page sizes based on start position", () => {
  const breaks = computePageBreaks(10, (start, count) => {
    const max = start === 0 ? 4 : 3;
    return count <= max;
  });
  expect(breaks).toEqual([0, 4, 7]);
});
```

---

## Mocking Approaches

**No mocking is used anywhere in the codebase.** Both Python and TypeScript tests operate on pure functions that:

- Accept data inputs and return data outputs
- Have no external dependencies (no HTTP, no filesystem reads, no DOM)
- Use pytest's `tmp_path` for the only I/O test (Excalidraw file save)

This is by design: the `src/lib/` modules are explicitly documented as "Pure logic -- DOM measurement injected via callback (DIP)" and the Python `diagramlib` modules are stateless helper functions and a builder class.

---

## What Is Tested

### Python (3 test files, ~100 test cases)

| Module           | What's tested                                                                                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `aws_diagram.py` | Theme color dictionaries (required keys, matching names, standard colors), graph/node/edge/cluster attribute factories for both themes, output directory path                                                          |
| `colors.py`      | Color tuple structure (2-element tuples of hex strings), hex format validation, stroke-vs-background brightness invariant, exact palette values                                                                        |
| `excalidraw.py`  | Diagram initialization, seed generation (sequential, unique), all 5 element types (rect, txt, arr, line, diamond) with every optional parameter, container text centering math, JSON serialization, directory creation |

### TypeScript (2 test files, ~25 test cases)

| Module                   | What's tested                                                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `glossary-data.ts`       | Flat term building, alphabetical sorting, category filtering, term lookup by name, random term selection with exclusion, term key format |
| `glossary-pagination.ts` | Page break computation, page lookup by index, page range extraction, edge cases (0 items, 1 item, varying page sizes)                    |

---

## What Is NOT Tested

- **Astro components** (`src/components/*.astro`) -- no component tests
- **Page routes** (`src/pages/*.astro`) -- no integration tests
- **CSS/styling** (`src/styles/global.css`) -- no visual regression tests
- **Diagram generation scripts** (`diagrams/scripts/generate-*.py`) -- scripts are run manually, not tested
- **DOM-dependent code** (`src/lib/search-engine.ts`, `src/lib/search-ui.ts`, `src/lib/glossary-detail.ts`) -- these interact with the DOM and are not unit tested
- **Notion fetch script** (`scripts/fetch-notion.mjs`) -- external API integration, not tested
- **Build pipeline** -- no CI test step in GitHub Actions; tests are enforced only via pre-commit hooks locally
- **Mermaid rendering** -- client-side, no test coverage

---

## Golden Fixtures

Directory: `tests/fixtures/`

Contains `.json` snapshots of expected Excalidraw diagram output:

- `golden-airflow-components.json`
- `golden-batch-vs-streaming.json`
- `golden-cost-optimization.json`
- `golden-data-marts.json`
- `golden-iam-permissions.json`

These are stored but **not currently referenced by any test**. They appear to be retained for future snapshot/regression testing or manual comparison.

---

## Adding New Tests

### Python

1. Create `tests/test_<module>.py`
2. Import from `diagramlib.<module>`
3. Use class-based grouping (`class TestFeatureName:`)
4. Use plain `assert` with f-string messages for loops
5. Tests run automatically on commit via pre-commit hook

### TypeScript

1. Create `src/lib/<module>.test.ts` next to the source file
2. Import from `vitest` (`describe`, `expect`, `it`)
3. Define inline `TEST_DATA` constants
4. Use `describe`/`it` blocks
5. Tests run automatically on commit via pre-commit hook
