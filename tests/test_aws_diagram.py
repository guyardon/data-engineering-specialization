"""Tests for diagramlib.aws_diagram — AWS Diagrams library helpers."""

from diagramlib.aws_diagram import (
    CLUSTER_COLORS_DARK,
    CLUSTER_COLORS_LIGHT,
    cluster_attrs,
    edge_attrs,
    graph_attrs,
    node_attrs,
    output_dir,
)


class TestThemeColors:
    def test_light_cluster_colors_have_required_keys(self):
        for name, c in CLUSTER_COLORS_LIGHT.items():
            assert "bg" in c, f"Light {name} missing 'bg'"
            assert "fc" in c, f"Light {name} missing 'fc'"
            assert "border" in c, f"Light {name} missing 'border'"

    def test_dark_cluster_colors_have_required_keys(self):
        for name, c in CLUSTER_COLORS_DARK.items():
            assert "bg" in c, f"Dark {name} missing 'bg'"
            assert "fc" in c, f"Dark {name} missing 'fc'"
            assert "border" in c, f"Dark {name} missing 'border'"

    def test_same_color_names_in_both_themes(self):
        assert set(CLUSTER_COLORS_LIGHT.keys()) == set(CLUSTER_COLORS_DARK.keys())

    def test_has_standard_colors(self):
        for name in ["green", "blue", "yellow", "purple", "red", "cyan"]:
            assert name in CLUSTER_COLORS_LIGHT, f"Missing color {name}"


class TestGraphAttrs:
    def test_light_mode(self):
        attrs = graph_attrs(dark=False, title="Test Diagram")
        assert attrs["bgcolor"] == "white"
        assert attrs["fontcolor"] == "#1e1e1e"
        assert attrs["label"] == "Test Diagram\n\n"
        assert attrs["labelloc"] == "t"
        assert attrs["dpi"] == "150"
        assert attrs["rankdir"] == "LR"

    def test_dark_mode(self):
        attrs = graph_attrs(dark=True, title="Test")
        assert attrs["bgcolor"] == "#0f0f13"
        assert attrs["fontcolor"] == "#e8e8ea"

    def test_custom_rankdir(self):
        attrs = graph_attrs(dark=False, title="X", rankdir="TB")
        assert attrs["rankdir"] == "TB"


class TestNodeAttrs:
    def test_light_mode(self):
        attrs = node_attrs(dark=False)
        assert attrs["fontsize"] == "12"
        assert attrs["fontname"] == "Helvetica"
        assert attrs["fontcolor"] == "#1e1e1e"
        assert attrs["height"] == "1.1"

    def test_dark_mode(self):
        attrs = node_attrs(dark=True)
        assert attrs["fontcolor"] == "#e8e8ea"


class TestEdgeAttrs:
    def test_light_mode(self):
        attrs = edge_attrs(dark=False)
        assert attrs["color"] == "#495057"
        assert attrs["penwidth"] == "2.0"

    def test_dark_mode(self):
        attrs = edge_attrs(dark=True)
        assert attrs["color"] == "#65656e"


class TestClusterAttrs:
    def test_structure(self):
        attrs = cluster_attrs("green", dark=False)
        assert attrs["fontsize"] == "14"
        assert attrs["fontname"] == "Helvetica Bold"
        assert attrs["penwidth"] == "1.5"
        assert attrs["labeljust"] == "c"
        assert attrs["labelloc"] == "t"
        assert attrs["style"] == "dashed,rounded"
        assert attrs["margin"] == "14"
        assert "bgcolor" in attrs
        assert "fontcolor" in attrs
        assert "pencolor" in attrs

    def test_dark_uses_dark_colors(self):
        light = cluster_attrs("blue", dark=False)
        dark = cluster_attrs("blue", dark=True)
        assert light["bgcolor"] != dark["bgcolor"]
        assert light["fontcolor"] != dark["fontcolor"]


class TestOutputDir:
    def test_ends_with_expected_path(self):
        path = output_dir()
        assert path.endswith("public/images/diagrams")
