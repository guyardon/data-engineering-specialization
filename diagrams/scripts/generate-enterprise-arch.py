#!/usr/bin/env python3
"""Generate Enterprise Architecture Domains excalidraw diagram — layered design."""

import math

from diagramlib import ExcalidrawDiagram

d = ExcalidrawDiagram(seed=1000)

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
LAYER_W = 500
LAYER_H = 80
LAYER_GAP = 12

MARGIN_LEFT = 30

FONT_MAIN_TITLE = 28
FONT_TITLE = 24
FONT_SUBTITLE = 16
FONT_DECISION_TITLE = 22
FONT_DOOR = 20

# Title/subtitle positioning within each layer box (80h)
TITLE_TEXT_H = math.ceil(1 * FONT_TITLE * 1.25)  # 30
SUBTITLE_TEXT_H = math.ceil(1 * FONT_SUBTITLE * 1.25)  # 20
TITLE_SUBTITLE_GAP = 8
COMBINED_H = TITLE_TEXT_H + TITLE_SUBTITLE_GAP + SUBTITLE_TEXT_H  # 58

TITLE_Y = 20
TITLE_H = math.ceil(FONT_MAIN_TITLE * 1.25)

STACK_TOP = TITLE_Y + TITLE_H + 30

# ---------------------------------------------------------------------------
# Main title (free text, centered over full layer width)
# ---------------------------------------------------------------------------
title_text = "Enterprise Architecture"
title_w = math.ceil(len(title_text) * FONT_MAIN_TITLE * 0.65 + 40)
title_center_x = MARGIN_LEFT + LAYER_W // 2
d.txt(
    "title",
    title_center_x - title_w // 2,
    TITLE_Y,
    title_w,
    TITLE_H,
    title_text,
    FONT_MAIN_TITLE,
)

# ---------------------------------------------------------------------------
# 4 layers — each with bound title text + free subtitle text
# ---------------------------------------------------------------------------
layers = [
    # (id, title, subtitle, stroke, bg, strokeWidth)
    (
        "biz",
        "Business Architecture",
        "Product & service strategy",
        "#1971c2",
        "#a5d8ff",
        2,
    ),
    (
        "app",
        "Application Architecture",
        "App structure & interaction",
        "#6741d9",
        "#d0bfff",
        2,
    ),
    (
        "tech",
        "Technical Architecture",
        "Software & hardware components",
        "#0c8599",
        "#99e9f2",
        2,
    ),
    ("data", "Data Architecture", "Evolving data needs", "#e67700", "#ffec99", 3),
]

for i, (lid, title, subtitle, stroke, bg, sw) in enumerate(layers):
    layer_y = STACK_TOP + i * (LAYER_H + LAYER_GAP)
    rect_id = f"{lid}-rect"
    title_id = f"{lid}-title"
    subtitle_id = f"{lid}-sub"

    # Rectangle — only the title text is bound
    d.rect(
        rect_id,
        MARGIN_LEFT,
        layer_y,
        LAYER_W,
        LAYER_H,
        stroke,
        bg,
        sw=sw,
        bnd=[{"id": title_id, "type": "text"}],
    )

    # Bound title text (containerId = rect_id)
    # y = box_y + (80 - 58) // 2 = box_y + 11
    t_y = layer_y + (LAYER_H - COMBINED_H) // 2
    d.txt(
        title_id,
        MARGIN_LEFT,
        t_y,
        LAYER_W,
        TITLE_TEXT_H,
        title,
        FONT_TITLE,
        color="#1e1e1e",
        cid=rect_id,
        valign="middle",
    )

    # Free subtitle text (containerId = None, positioned inside the box)
    # y = title_y + 30 + 8 = box_y + 49
    s_y = t_y + TITLE_TEXT_H + TITLE_SUBTITLE_GAP
    d.txt(
        subtitle_id,
        MARGIN_LEFT,
        s_y,
        LAYER_W,
        SUBTITLE_TEXT_H,
        subtitle,
        FONT_SUBTITLE,
        color=stroke,
        valign="middle",
    )

# ---------------------------------------------------------------------------
# Decision Categories section (below layers)
# ---------------------------------------------------------------------------
stack_bottom = STACK_TOP + 4 * (LAYER_H + LAYER_GAP) - LAYER_GAP

decision_title_y = stack_bottom + 40
decision_title_h = math.ceil(FONT_DECISION_TITLE * 1.25)
decision_text = "Decision Categories"
decision_w = math.ceil(len(decision_text) * FONT_DECISION_TITLE * 0.65 + 40)
d.txt(
    "dec-title",
    title_center_x - decision_w // 2,
    decision_title_y,
    decision_w,
    decision_title_h,
    decision_text,
    FONT_DECISION_TITLE,
)

# ---------------------------------------------------------------------------
# One-Way / Two-Way Door boxes (centered below decision title)
# ---------------------------------------------------------------------------
DOOR_W = 200
DOOR_H = 65
DOOR_GAP = 30

doors_total_w = 2 * DOOR_W + DOOR_GAP
doors_x_start = MARGIN_LEFT + (LAYER_W - doors_total_w) // 2
doors_y = decision_title_y + decision_title_h + 15

doors = [
    ("ow", "One-Way Door\nIrreversible", "#c92a2a", "#ffc9c9"),
    ("tw", "Two-Way Door\nReversible", "#2f9e44", "#b2f2bb"),
]

for i, (did, label, stroke, bg) in enumerate(doors):
    dx = doors_x_start + i * (DOOR_W + DOOR_GAP)
    tid = f"{did}-t"

    d.rect(
        did, dx, doors_y, DOOR_W, DOOR_H, stroke, bg, bnd=[{"id": tid, "type": "text"}]
    )

    # Bound door text — use standard center positioning
    num_lines = label.count("\n") + 1
    actual_h = math.ceil(num_lines * FONT_DOOR * 1.25)
    door_txt_y = doors_y + (DOOR_H - actual_h) // 2
    d.txt(tid, dx, door_txt_y, DOOR_W, actual_h, label, FONT_DOOR, cid=did)

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
outfile = "diagrams/artifacts/enterprise-architecture.excalidraw"
d.save(outfile)
print(f"Done! Wrote {outfile}")
