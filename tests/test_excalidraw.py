"""Tests for diagramlib.excalidraw — ExcalidrawDiagram class."""

import json
import math

from diagramlib.excalidraw import ExcalidrawDiagram


class TestInit:
    def test_creates_valid_excalidraw_structure(self):
        d = ExcalidrawDiagram()
        assert d.data["type"] == "excalidraw"
        assert d.data["version"] == 2
        assert d.data["source"] == "https://excalidraw.com"
        assert d.data["elements"] == []
        assert d.data["appState"]["viewBackgroundColor"] == "#ffffff"
        assert d.data["appState"]["gridSize"] is None
        assert d.data["files"] == {}

    def test_custom_seed(self):
        d = ExcalidrawDiagram(seed=5000)
        d.rect("r1", 0, 0, 100, 50, "#000", "#fff")
        # First _ns() call should return 5001
        el = d.elements[0]
        assert el["seed"] == 5001

    def test_elements_property_returns_list(self):
        d = ExcalidrawDiagram()
        assert isinstance(d.elements, list)
        assert d.elements is d.data["elements"]


class TestSeedGeneration:
    def test_increments_sequentially(self):
        d = ExcalidrawDiagram(seed=1000)
        # Each rect uses 2 seeds (seed + versionNonce)
        d.rect("r1", 0, 0, 100, 50, "#000", "#fff")
        assert d.elements[0]["seed"] == 1001
        assert d.elements[0]["versionNonce"] == 1002

    def test_unique_seeds_across_many_elements(self):
        d = ExcalidrawDiagram()
        for i in range(50):
            d.rect(f"r{i}", 0, 0, 10, 10, "#000", "#fff")
        all_seeds = []
        for el in d.elements:
            all_seeds.extend([el["seed"], el["versionNonce"]])
        assert len(all_seeds) == len(set(all_seeds))


class TestRect:
    def test_basic_rect(self):
        d = ExcalidrawDiagram()
        d.rect("box", 10, 20, 200, 100, "#1971c2", "#a5d8ff")
        el = d.elements[0]
        assert el["type"] == "rectangle"
        assert el["id"] == "box"
        assert el["x"] == 10
        assert el["y"] == 20
        assert el["width"] == 200
        assert el["height"] == 100
        assert el["strokeColor"] == "#1971c2"
        assert el["backgroundColor"] == "#a5d8ff"
        assert el["fillStyle"] == "solid"
        assert el["strokeWidth"] == 2
        assert el["strokeStyle"] == "solid"
        assert el["roughness"] == 1
        assert el["opacity"] == 100
        assert el["roundness"] == {"type": 3}
        assert el["isDeleted"] is False
        assert el["groupIds"] == []
        assert el["boundElements"] == []
        assert el["angle"] == 0

    def test_hachure_fill(self):
        d = ExcalidrawDiagram()
        d.rect("box", 0, 0, 100, 50, "#000", "#fff", fill="hachure")
        assert d.elements[0]["fillStyle"] == "hachure"

    def test_custom_stroke_width(self):
        d = ExcalidrawDiagram()
        d.rect("box", 0, 0, 100, 50, "#000", "#fff", sw=4)
        assert d.elements[0]["strokeWidth"] == 4

    def test_dashed(self):
        d = ExcalidrawDiagram()
        d.rect("box", 0, 0, 100, 50, "#000", "#fff", dashed=True)
        assert d.elements[0]["strokeStyle"] == "dashed"

    def test_opacity(self):
        d = ExcalidrawDiagram()
        d.rect("box", 0, 0, 100, 50, "#000", "#fff", opacity=30)
        assert d.elements[0]["opacity"] == 30

    def test_bound_elements(self):
        d = ExcalidrawDiagram()
        bnd = [{"id": "text-1", "type": "text"}]
        d.rect("box", 0, 0, 100, 50, "#000", "#fff", bnd=bnd)
        assert d.elements[0]["boundElements"] == bnd

    def test_bound_elements_default_not_shared(self):
        """Default bnd=None should create a new list each time."""
        d = ExcalidrawDiagram()
        d.rect("r1", 0, 0, 10, 10, "#000", "#fff")
        d.rect("r2", 0, 0, 10, 10, "#000", "#fff")
        assert d.elements[0]["boundElements"] is not d.elements[1]["boundElements"]


class TestTxt:
    def test_basic_text(self):
        d = ExcalidrawDiagram()
        d.txt("label", 10, 20, 200, 50, "Hello World", 24)
        el = d.elements[0]
        assert el["type"] == "text"
        assert el["id"] == "label"
        assert el["x"] == 10
        assert el["y"] == 20
        assert el["width"] == 200
        assert el["height"] == 50
        assert el["text"] == "Hello World"
        assert el["originalText"] == "Hello World"
        assert el["fontSize"] == 24
        assert el["fontFamily"] == 1
        assert el["textAlign"] == "center"
        assert el["verticalAlign"] == "middle"
        assert el["lineHeight"] == 1.25
        assert el["autoResize"] is True
        assert el["containerId"] is None
        assert el["strokeColor"] == "#1e1e1e"

    def test_custom_color(self):
        d = ExcalidrawDiagram()
        d.txt("t", 0, 0, 100, 50, "hi", 20, color="#ff0000")
        assert d.elements[0]["strokeColor"] == "#ff0000"

    def test_container_centering(self):
        """When cid is set, y and h should be recalculated for vertical centering."""
        d = ExcalidrawDiagram()
        box_y, box_h = 100, 80
        text = "Line 1\nLine 2"
        font_size = 20
        d.txt("t", 10, box_y, 200, box_h, text, font_size, cid="box")
        el = d.elements[0]
        assert el["containerId"] == "box"
        num_lines = 2
        actual_h = math.ceil(num_lines * font_size * 1.25)
        expected_y = box_y + (box_h - actual_h) // 2
        assert el["y"] == expected_y
        assert el["height"] == actual_h

    def test_no_container_preserves_y_and_h(self):
        d = ExcalidrawDiagram()
        d.txt("t", 10, 100, 200, 80, "text", 20)
        el = d.elements[0]
        assert el["y"] == 100
        assert el["height"] == 80

    def test_opacity(self):
        d = ExcalidrawDiagram()
        d.txt("t", 0, 0, 100, 50, "hi", 20, op=50)
        assert d.elements[0]["opacity"] == 50

    def test_custom_align(self):
        d = ExcalidrawDiagram()
        d.txt("t", 0, 0, 100, 50, "hi", 20, align="left")
        assert d.elements[0]["textAlign"] == "left"


class TestArr:
    def test_basic_arrow(self):
        d = ExcalidrawDiagram()
        pts = [[0, 0], [100, 50]]
        d.arr("a1", 10, 20, pts, "#000")
        el = d.elements[0]
        assert el["type"] == "arrow"
        assert el["id"] == "a1"
        assert el["x"] == 10
        assert el["y"] == 20
        assert el["points"] == pts
        assert el["startArrowhead"] is None
        assert el["endArrowhead"] == "arrow"
        assert el["strokeColor"] == "#000"
        assert el["width"] == 100
        assert el["height"] == 50

    def test_dashed_arrow(self):
        d = ExcalidrawDiagram()
        d.arr("a1", 0, 0, [[0, 0], [50, 0]], "#000", dash=True)
        assert d.elements[0]["strokeStyle"] == "dashed"

    def test_bindings(self):
        d = ExcalidrawDiagram()
        sb = {"elementId": "box1", "focus": 0, "gap": 5, "fixedPoint": None}
        eb = {"elementId": "box2", "focus": 0, "gap": 5, "fixedPoint": None}
        d.arr("a1", 0, 0, [[0, 0], [100, 0]], "#000", sb=sb, eb=eb)
        el = d.elements[0]
        assert el["startBinding"] == sb
        assert el["endBinding"] == eb

    def test_opacity(self):
        d = ExcalidrawDiagram()
        d.arr("a1", 0, 0, [[0, 0], [10, 0]], "#000", op=50)
        assert d.elements[0]["opacity"] == 50


class TestLine:
    def test_basic_line(self):
        d = ExcalidrawDiagram()
        pts = [[0, 0], [100, 0]]
        d.line("l1", 10, 20, pts, "#000")
        el = d.elements[0]
        assert el["type"] == "line"
        assert el["id"] == "l1"
        assert el["points"] == pts
        assert el["startArrowhead"] is None
        assert el["endArrowhead"] is None
        assert el["strokeWidth"] == 2

    def test_custom_stroke_width(self):
        d = ExcalidrawDiagram()
        d.line("l1", 0, 0, [[0, 0], [50, 0]], "#000", sw=4)
        assert d.elements[0]["strokeWidth"] == 4

    def test_dash(self):
        d = ExcalidrawDiagram()
        d.line("l1", 0, 0, [[0, 0], [50, 0]], "#000", dash=True)
        assert d.elements[0]["strokeStyle"] == "dashed"


class TestDiamond:
    def test_basic_diamond(self):
        d = ExcalidrawDiagram()
        d.diamond("d1", 10, 20, 80, 60, "#000", "#fff")
        el = d.elements[0]
        assert el["type"] == "diamond"
        assert el["id"] == "d1"
        assert el["x"] == 10
        assert el["y"] == 20
        assert el["width"] == 80
        assert el["height"] == 60
        assert el["roundness"] == {"type": 2}
        assert el["fillStyle"] == "solid"

    def test_bound_elements(self):
        d = ExcalidrawDiagram()
        bnd = [{"id": "t1", "type": "text"}]
        d.diamond("d1", 0, 0, 50, 50, "#000", "#fff", bnd=bnd)
        assert d.elements[0]["boundElements"] == bnd


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

    def test_creates_parent_directories(self, tmp_path):
        d = ExcalidrawDiagram()
        path = tmp_path / "sub" / "dir" / "test.excalidraw"
        d.save(str(path))
        assert path.exists()

    def test_indent_2(self, tmp_path):
        d = ExcalidrawDiagram()
        path = tmp_path / "test.excalidraw"
        d.save(str(path))
        content = path.read_text()
        # json.dump with indent=2 produces lines starting with "  "
        assert "\n  " in content


class TestElementsAccumulate:
    def test_multiple_element_types(self):
        d = ExcalidrawDiagram()
        d.rect("r1", 0, 0, 100, 50, "#000", "#fff")
        d.txt("t1", 0, 0, 100, 50, "hi", 20)
        d.arr("a1", 0, 0, [[0, 0], [10, 0]], "#000")
        d.line("l1", 0, 0, [[0, 0], [10, 0]], "#000")
        d.diamond("d1", 0, 0, 50, 50, "#000", "#fff")
        assert len(d.elements) == 5
        types = [el["type"] for el in d.elements]
        assert types == ["rectangle", "text", "arrow", "line", "diamond"]
