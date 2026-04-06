"""Helpers for AWS architecture diagrams using the `diagrams` library."""

import os

CLUSTER_COLORS_LIGHT: dict[str, dict[str, str]] = {
    "green": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
    "blue": {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
    "yellow": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
    "purple": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
    "red": {"bg": "#ffc9c940", "fc": "#c92a2a", "border": "#c92a2a"},
    "cyan": {"bg": "#99e9f240", "fc": "#0c8599", "border": "#0c8599"},
}

CLUSTER_COLORS_DARK: dict[str, dict[str, str]] = {
    "green": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
    "blue": {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
    "yellow": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
    "purple": {"bg": "#1a1a2a", "fc": "#c4b5fd", "border": "#6741d9"},
    "red": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
    "cyan": {"bg": "#1a2a2a", "fc": "#67e8f9", "border": "#0c8599"},
}


def graph_attrs(*, dark: bool, title: str, rankdir: str = "LR") -> dict[str, str]:
    """Standard graph attributes for a `diagrams.Diagram`."""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    return {
        "bgcolor": bg,
        "fontcolor": fc,
        "fontsize": "18",
        "fontname": "Helvetica Bold",
        "pad": "0.3",
        "nodesep": "0.3",
        "ranksep": "1.2",
        "dpi": "150",
        "label": f"{title}\n\n",
        "labelloc": "t",
        "rankdir": rankdir,
        "compound": "true",
    }


def node_attrs(dark: bool) -> dict[str, str]:
    """Standard node attributes."""
    fc = "#e8e8ea" if dark else "#1e1e1e"
    return {
        "fontsize": "12",
        "fontname": "Helvetica",
        "fontcolor": fc,
        "height": "1.1",
    }


def edge_attrs(dark: bool) -> dict[str, str]:
    """Standard edge attributes."""
    edge_color = "#65656e" if dark else "#495057"
    return {
        "color": edge_color,
        "penwidth": "2.0",
    }


def cluster_attrs(color_key: str, *, dark: bool) -> dict[str, str]:
    """Standard cluster attributes for a named color."""
    palette = CLUSTER_COLORS_DARK if dark else CLUSTER_COLORS_LIGHT
    c = palette[color_key]
    return {
        "fontsize": "14",
        "fontname": "Helvetica Bold",
        "penwidth": "1.5",
        "labeljust": "c",
        "labelloc": "t",
        "style": "dashed,rounded",
        "margin": "14",
        "bgcolor": c["bg"],
        "fontcolor": c["fc"],
        "pencolor": c["border"],
    }


def output_dir() -> str:
    """Return the standard output directory for AWS diagram PNGs."""
    # diagrams/diagramlib/aws_diagram.py → up 3 levels to project root
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.join(project_root, "public", "images", "diagrams")
