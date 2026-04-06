#!/usr/bin/env python3
"""Generate monolith-modular.excalidraw — side-by-side comparison diagram."""

import math

from diagramlib import ExcalidrawDiagram

d = ExcalidrawDiagram(seed=6000)

# ─── Colors ───
RED_S, RED_B = "#c92a2a", "#ffc9c9"
GREEN_S, GREEN_B = "#2f9e44", "#b2f2bb"
GRAY_S, GRAY_B = "#868e96", "#dee2e6"
ARROW_COLOR = "#495057"

# ─── Layout constants ───
TOTAL_W = 700
COL_GAP = 80  # gap between left and right columns

# Monolith block
MONO_W = 220
MONO_H = 250

# Modular small boxes
MOD_W = 100
MOD_H = 55
MOD_GAP_X = 20  # horizontal gap between modular boxes
MOD_GAP_Y = 20  # vertical gap between modular rows

# Starting position
START_X = 50
START_Y = 0

# ─── Title ───
title_w = TOTAL_W
title_h = math.ceil(1 * 28 * 1.25)
title_x = START_X
title_y = START_Y
d.txt(
    "title",
    title_x,
    title_y,
    title_w,
    title_h,
    "Monolith vs. Modular Systems",
    28,
    color="#1e1e1e",
)

# ─── Column positions ───
content_y = title_y + title_h + 25  # 25px gap below title

# Left column: Monolith
left_x = START_X
# Right column: Modular — center it in the right half
right_col_start = START_X + MONO_W + COL_GAP

# ─── Left column: "Monolith" label ───
mono_label_h = math.ceil(1 * 22 * 1.25)
mono_label_x = left_x
mono_label_y = content_y
d.txt(
    "mono_label",
    mono_label_x,
    mono_label_y,
    MONO_W,
    mono_label_h,
    "Monolith",
    22,
    color=RED_S,
)

# ─── Monolith big rectangle ───
mono_rect_y = mono_label_y + mono_label_h + 15
d.rect("mono_rect", left_x, mono_rect_y, MONO_W, MONO_H, RED_S, RED_B)

# ─── Internal component dividers (dashed lines as thin rects) + labels ───
# Divide the monolith into 4 sections: UI, API, Business Logic, Data Layer
# Each section is ~62.5h (250/4), use dashed separator lines between them
section_h = MONO_H // 4
components = ["UI", "API", "Business\nLogic", "Data Layer"]

for i, comp in enumerate(components):
    comp_y = mono_rect_y + i * section_h
    comp_h = section_h

    # Dashed separator line (except for first section)
    if i > 0:
        d.rect(
            f"mono_sep_{i}",
            left_x + 10,
            comp_y,
            MONO_W - 20,
            0,
            GRAY_S,
            "transparent",
            dashed=True,
            sw=1,
        )

    # Component label — free text (not bound to monolith rect)
    num_lines = comp.count("\n") + 1
    label_h = math.ceil(num_lines * 16 * 1.25)
    label_y = comp_y + (comp_h - label_h) // 2
    d.txt(f"mono_comp_{i}", left_x, label_y, MONO_W, label_h, comp, 16, color=GRAY_S)

# ─── Monolith subtitle ───
mono_sub_y = mono_rect_y + MONO_H + 15
mono_sub_h = math.ceil(2 * 16 * 1.25)
d.txt(
    "mono_sub",
    left_x,
    mono_sub_y,
    MONO_W,
    mono_sub_h,
    "Single codebase,\ntightly coupled",
    16,
    color=RED_S,
)

# ─── Right column: "Modular" label ───
# Calculate modular grid width: 3 columns of boxes
mod_grid_w = 3 * MOD_W + 2 * MOD_GAP_X  # 340
mod_label_h = math.ceil(1 * 22 * 1.25)
mod_label_x = right_col_start
mod_label_y = content_y
d.txt(
    "mod_label",
    mod_label_x,
    mod_label_y,
    mod_grid_w,
    mod_label_h,
    "Modular",
    22,
    color=GREEN_S,
)

# ─── Modular service boxes ───
# Layout: row 1 = Auth, API, Data; row 2 = Analytics, UI (centered)
services = [
    ("Auth", 0, 0),
    ("API", 1, 0),
    ("Data", 2, 0),
    ("Analytics", 0, 1),
    ("UI", 1, 1),
]

mod_start_y = mod_label_y + mod_label_h + 15
# Offset row 2 to be slightly shifted for visual interest
# Row 2 has 2 items — center them under 3-col grid
row2_offset = (MOD_W + MOD_GAP_X) // 2

service_positions = {}  # store {name: (cx, cy, x, y, w, h)} for arrow connections

for name, col, row in services:
    if row == 1:
        bx = right_col_start + row2_offset + col * (MOD_W + MOD_GAP_X)
    else:
        bx = right_col_start + col * (MOD_W + MOD_GAP_X)
    by = mod_start_y + row * (MOD_H + MOD_GAP_Y)

    box_id = f"mod_{name.lower()}"
    txt_id = f"mod_{name.lower()}_t"

    d.rect(
        box_id,
        bx,
        by,
        MOD_W,
        MOD_H,
        GREEN_S,
        GREEN_B,
        bnd=[{"type": "text", "id": txt_id}],
    )
    d.txt(txt_id, bx, by, MOD_W, MOD_H, name, 20, color="#1e1e1e", cid=box_id)

    # Store center and bounds for arrows
    service_positions[name] = {
        "x": bx,
        "y": by,
        "w": MOD_W,
        "h": MOD_H,
        "cx": bx + MOD_W // 2,
        "cy": by + MOD_H // 2,
        "id": box_id,
    }

# ─── Arrows between modular services ───
# Connections: Auth->API, API->Data, Data->Analytics, API->UI
connections = [
    ("Auth", "API", "right", "left"),  # Auth right edge -> API left edge
    ("API", "Data", "right", "left"),  # API right edge -> Data left edge
    ("Data", "Analytics", "bottom", "top"),  # Data bottom -> Analytics top
    ("API", "UI", "bottom", "top"),  # API bottom -> UI top
]

arr_gap = 5  # gap from box edge to arrow start/end

for i, (src, dst, src_side, dst_side) in enumerate(connections):
    s = service_positions[src]
    dd = service_positions[dst]

    # Calculate start point based on side
    if src_side == "right":
        sx = s["x"] + s["w"] + arr_gap
        sy = s["cy"]
    elif src_side == "bottom":
        sx = s["cx"]
        sy = s["y"] + s["h"] + arr_gap
    elif src_side == "left":
        sx = s["x"] - arr_gap
        sy = s["cy"]
    else:  # top
        sx = s["cx"]
        sy = s["y"] - arr_gap

    # Calculate end point
    if dst_side == "left":
        ex = dd["x"] - arr_gap
        ey = dd["cy"]
    elif dst_side == "top":
        ex = dd["cx"]
        ey = dd["y"] - arr_gap
    elif dst_side == "right":
        ex = dd["x"] + dd["w"] + arr_gap
        ey = dd["cy"]
    else:  # bottom
        ex = dd["cx"]
        ey = dd["y"] + dd["h"] + arr_gap

    # Arrow points are relative to start
    pts = [[0, 0], [ex - sx, ey - sy]]

    sb = {"elementId": s["id"], "focus": 0, "gap": arr_gap}
    eb = {"elementId": dd["id"], "focus": 0, "gap": arr_gap}

    d.arr(f"arr_{i}", sx, sy, pts, ARROW_COLOR, sb=sb, eb=eb)

# ─── Modular subtitle ───
# Position below the second row of boxes
mod_sub_y = mod_start_y + 2 * (MOD_H + MOD_GAP_Y) - MOD_GAP_Y + 15
mod_sub_h = math.ceil(2 * 16 * 1.25)
d.txt(
    "mod_sub",
    right_col_start,
    mod_sub_y,
    mod_grid_w,
    mod_sub_h,
    "Independent services,\nloosely coupled",
    16,
    color=GREEN_S,
)

# ─── Write output ───
outfile = "diagrams/artifacts/monolith-modular.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
print(f"  {len(d.elements)} elements")
