#!/usr/bin/env python3
"""Generate batch-streaming.excalidraw diagram — vertical flows, side by side."""

import json
import math
import os

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 3000


def ns():
    global seed
    seed += 1
    return seed


def rect(
    id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2
):
    els.append(
        {
            "type": "rectangle",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": sw,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 3},
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append(
        {
            "type": "text",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "text": t,
            "originalText": t,
            "fontSize": sz,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "lineHeight": 1.25,
            "autoResize": True,
            "containerId": cid,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# ─── Layout constants ───
BOX_W = 160
BOX_H = 55
VGAP = 50  # vertical gap between boxes (arrow space)
COL_GAP = 80  # horizontal gap between columns
ARR_GAP = 5  # gap from box edge to arrow tip
ARROW_COLOR = "#495057"

# Colors (stroke, background)
BLUE_S, BLUE_B = "#1971c2", "#a5d8ff"
PURPLE_S, PURPLE_B = "#6741d9", "#d0bfff"
GREEN_S, GREEN_B = "#2f9e44", "#b2f2bb"
YELLOW_S, YELLOW_B = "#e67700", "#ffec99"
CYAN_S, CYAN_B = "#0c8599", "#99e9f2"
GRAY_S, GRAY_B = "#868e96", "#dee2e6"

# Column X positions
COL1_X = 40  # ETL
COL2_X = COL1_X + BOX_W + COL_GAP  # ELT
COL3_X = COL2_X + BOX_W + COL_GAP  # Streaming

# ─── Title ───
TITLE_Y = 10
total_w = COL3_X + BOX_W - COL1_X
txt("title", COL1_X, TITLE_Y, total_w, 35, "Batch & Streaming Architectures", 28)

# ─── Column labels ───
LABEL_Y = TITLE_Y + 55
txt("etl-label", COL1_X, LABEL_Y, BOX_W, 28, "ETL", 22, color=BLUE_S)
txt("elt-label", COL2_X, LABEL_Y, BOX_W, 28, "ELT", 22, color=PURPLE_S)
txt("str-label", COL3_X, LABEL_Y, BOX_W, 28, "Streaming", 22, color=GREEN_S)


# ─── Helper: create a box with text ───
def box(id, label, x, y, w, h, stroke, bg):
    tid = id + "-t"
    rect(id, x, y, w, h, stroke, bg, bnd=[{"id": tid, "type": "text"}])
    txt(tid, x, y, w, h, label, 20, cid=id)


# ─── Helper: vertical arrow between two boxes ───
def varrow(aid, src_id, sx, sy, sw, sh, dst_id, dx, dy, dw, dh, color=ARROW_COLOR):
    x = sx + sw // 2
    y1 = sy + sh + ARR_GAP
    y2 = dy - ARR_GAP
    sb = {"elementId": src_id, "focus": 0, "gap": ARR_GAP, "fixedPoint": [0.5, 1]}
    eb = {"elementId": dst_id, "focus": 0, "gap": ARR_GAP, "fixedPoint": [0.5, 0]}
    arr(aid, x, y1, [[0, 0], [0, y2 - y1]], color, sb=sb, eb=eb)


# ─── Helper: horizontal arrow between two boxes ───
def harrow(aid, src_id, sx, sy, sw, sh, dst_id, dx, dy, dw, dh, color=ARROW_COLOR):
    x1 = sx + sw + ARR_GAP
    y = sy + sh // 2
    x2 = dx - ARR_GAP
    sb = {"elementId": src_id, "focus": 0, "gap": ARR_GAP, "fixedPoint": [1, 0.5]}
    eb = {"elementId": dst_id, "focus": 0, "gap": ARR_GAP, "fixedPoint": [0, 0.5]}
    arr(aid, x1, y, [[0, 0], [x2 - x1, 0]], color, sb=sb, eb=eb)


# ─── Start Y for first box row ───
START_Y = LABEL_Y + 45

# ─── ETL Column (6 boxes + Data Mart branch) ───
etl_steps = [
    ("etl-src", "Source", GRAY_S, GRAY_B),
    ("etl-ext", "Extract", BLUE_S, BLUE_B),
    ("etl-xfm", "Transform", BLUE_S, BLUE_B),
    ("etl-load", "Load", BLUE_S, BLUE_B),
    ("etl-dw", "Data\nWarehouse", YELLOW_S, YELLOW_B),
    ("etl-srv", "Serving", GRAY_S, GRAY_B),
]

etl_positions = []
y = START_Y
for bid, label, sc, bc in etl_steps:
    box(bid, label, COL1_X, y, BOX_W, BOX_H, sc, bc)
    etl_positions.append((COL1_X, y, BOX_W, BOX_H))
    y += BOX_H + VGAP

# ETL vertical arrows
for i in range(len(etl_steps) - 1):
    sx, sy, sw, sh = etl_positions[i]
    dx, dy, dw, dh = etl_positions[i + 1]
    varrow(
        f"etl-a{i}",
        etl_steps[i][0],
        sx,
        sy,
        sw,
        sh,
        etl_steps[i + 1][0],
        dx,
        dy,
        dw,
        dh,
    )

# ─── ELT Column (5 boxes) ───
elt_steps = [
    ("elt-src", "Source", GRAY_S, GRAY_B),
    ("elt-ext", "Extract", PURPLE_S, PURPLE_B),
    ("elt-load", "Load", PURPLE_S, PURPLE_B),
    ("elt-dw", "Transform\nin DW", YELLOW_S, YELLOW_B),
    ("elt-srv", "Serving", GRAY_S, GRAY_B),
]

elt_positions = []
y = START_Y
for bid, label, sc, bc in elt_steps:
    box(bid, label, COL2_X, y, BOX_W, BOX_H, sc, bc)
    elt_positions.append((COL2_X, y, BOX_W, BOX_H))
    y += BOX_H + VGAP

# ELT vertical arrows
for i in range(len(elt_steps) - 1):
    sx, sy, sw, sh = elt_positions[i]
    dx, dy, dw, dh = elt_positions[i + 1]
    varrow(
        f"elt-a{i}",
        elt_steps[i][0],
        sx,
        sy,
        sw,
        sh,
        elt_steps[i + 1][0],
        dx,
        dy,
        dw,
        dh,
    )

# ─── Streaming Column (3 boxes + 2 side-by-side below) ───
str_steps = [
    ("str-prod", "Event\nProducer", GREEN_S, GREEN_B),
    ("str-broker", "Streaming\nBroker", GREEN_S, GREEN_B),
    ("str-cons", "Event\nConsumer", GREEN_S, GREEN_B),
]

str_positions = []
y = START_Y
for bid, label, sc, bc in str_steps:
    box(bid, label, COL3_X, y, BOX_W, BOX_H, sc, bc)
    str_positions.append((COL3_X, y, BOX_W, BOX_H))
    y += BOX_H + VGAP

# Streaming vertical arrows
for i in range(len(str_steps) - 1):
    sx, sy, sw, sh = str_positions[i]
    dx, dy, dw, dh = str_positions[i + 1]
    varrow(
        f"str-a{i}",
        str_steps[i][0],
        sx,
        sy,
        sw,
        sh,
        str_steps[i + 1][0],
        dx,
        dy,
        dw,
        dh,
    )

# Two side-by-side boxes below Consumer
SIDE_W = 130
SIDE_GAP = 10
side_y = str_positions[2][1] + BOX_H + VGAP
# Center the two boxes under the column
pair_total = SIDE_W * 2 + SIDE_GAP
pair_x = COL3_X + (BOX_W - pair_total) // 2

box(
    "str-analytics",
    "Real-time\nAnalytics",
    pair_x,
    side_y,
    SIDE_W,
    BOX_H,
    GREEN_S,
    GREEN_B,
)
box(
    "str-ml",
    "Machine\nLearning",
    pair_x + SIDE_W + SIDE_GAP,
    side_y,
    SIDE_W,
    BOX_H,
    GREEN_S,
    GREEN_B,
)

# Arrows from Consumer to both side boxes
# Left branch: consumer center -> analytics center
cons_pos = str_positions[2]
cons_cx = cons_pos[0] + cons_pos[2] // 2
cons_bottom = cons_pos[1] + cons_pos[3] + ARR_GAP

analytics_cx = pair_x + SIDE_W // 2
analytics_top = side_y - ARR_GAP

# Arrow to analytics (down-left)
sb_cons = {
    "elementId": "str-cons",
    "focus": 0.3,
    "gap": ARR_GAP,
    "fixedPoint": [0.35, 1],
}
eb_ana = {
    "elementId": "str-analytics",
    "focus": 0,
    "gap": ARR_GAP,
    "fixedPoint": [0.5, 0],
}
arr(
    "str-a-ana",
    cons_cx - 15,
    cons_bottom,
    [[0, 0], [analytics_cx - (cons_cx - 15), analytics_top - cons_bottom]],
    ARROW_COLOR,
    sb=sb_cons,
    eb=eb_ana,
)

# Arrow to ML (down-right)
ml_cx = pair_x + SIDE_W + SIDE_GAP + SIDE_W // 2
ml_top = side_y - ARR_GAP

sb_cons2 = {
    "elementId": "str-cons",
    "focus": -0.3,
    "gap": ARR_GAP,
    "fixedPoint": [0.65, 1],
}
eb_ml = {"elementId": "str-ml", "focus": 0, "gap": ARR_GAP, "fixedPoint": [0.5, 0]}
arr(
    "str-a-ml",
    cons_cx + 15,
    cons_bottom,
    [[0, 0], [ml_cx - (cons_cx + 15), ml_top - cons_bottom]],
    ARROW_COLOR,
    sb=sb_cons2,
    eb=eb_ml,
)

# ─── Note at bottom ───
# Find the lowest element across all columns
etl_bottom = etl_positions[-1][1] + BOX_H  # ETL Serving bottom
elt_bottom = elt_positions[-1][1] + BOX_H  # ELT Serving bottom
str_bottom = side_y + BOX_H  # Streaming side boxes bottom
max_bottom = max(etl_bottom, elt_bottom, str_bottom)
note_y = max_bottom + 50

# Center note across the full diagram width (leftmost col start to rightmost element end)
diagram_left = COL1_X
diagram_right = max(COL3_X + BOX_W, pair_x + SIDE_W * 2 + SIDE_GAP)
full_width = diagram_right - diagram_left
NOTE_W = total_w  # keep the note box the same width as before
NOTE_H = 45
note_x = diagram_left + (full_width - NOTE_W) // 2

rect(
    "note-box",
    note_x,
    note_y,
    NOTE_W,
    NOTE_H,
    GRAY_S,
    "#f8f9fa",
    dashed=True,
    opacity=80,
    bnd=[{"id": "note-t", "type": "text"}],
)
txt(
    "note-t",
    note_x,
    note_y,
    NOTE_W,
    NOTE_H,
    '"Batch is a special case of streaming"',
    20,
    color="#495057",
    cid="note-box",
    op=80,
)

# ─── Write output ───
out_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams"
)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "batch-streaming.excalidraw")
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Done! Wrote {out_path}")
