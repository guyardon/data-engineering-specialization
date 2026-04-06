"""Tests for diagramlib.colors — color palette constants."""

import re

from diagramlib.colors import BLUE, CYAN, GRAY, GREEN, PURPLE, RED, YELLOW

HEX_RE = re.compile(r"^#[0-9a-f]{6}$")

ALL_COLORS = [
    ("BLUE", BLUE),
    ("GREEN", GREEN),
    ("YELLOW", YELLOW),
    ("PURPLE", PURPLE),
    ("RED", RED),
    ("CYAN", CYAN),
    ("GRAY", GRAY),
]


def test_all_colors_are_tuples_of_two_hex_strings():
    for name, color in ALL_COLORS:
        assert isinstance(color, tuple), f"{name} should be a tuple"
        assert len(color) == 2, f"{name} should have exactly 2 elements"
        stroke, bg = color
        assert HEX_RE.match(stroke), f"{name}[0] '{stroke}' is not a valid hex color"
        assert HEX_RE.match(bg), f"{name}[1] '{bg}' is not a valid hex color"


def test_stroke_is_darker_than_background():
    """Stroke colors should be darker (lower RGB values) than backgrounds."""
    for name, (stroke, bg) in ALL_COLORS:
        s_val = int(stroke[1:], 16)
        b_val = int(bg[1:], 16)
        # Background sum of RGB channels should be higher (lighter)
        s_sum = (s_val >> 16) + ((s_val >> 8) & 0xFF) + (s_val & 0xFF)
        b_sum = (b_val >> 16) + ((b_val >> 8) & 0xFF) + (b_val & 0xFF)
        assert b_sum > s_sum, f"{name} background should be lighter than stroke"


def test_expected_color_values():
    """Verify exact color values match the established palette."""
    assert BLUE == ("#1971c2", "#a5d8ff")
    assert GREEN == ("#2f9e44", "#b2f2bb")
    assert YELLOW == ("#e67700", "#ffec99")
    assert PURPLE == ("#6741d9", "#d0bfff")
    assert RED == ("#c92a2a", "#ffc9c9")
    assert CYAN == ("#0c8599", "#99e9f2")
    assert GRAY == ("#868e96", "#dee2e6")
