#!/usr/bin/env python3
"""Generate Excalidraw diagram: Data Ingestion Continuum (Batch → Micro-batch → Streaming)."""

import json
import math
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diagrams",
)
os.makedirs(OUT_DIR, exist_ok=True)

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 1000


def ns():
    global seed
    seed += 1
    return seed


# === COLOR PALETTE ===
BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append({
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
        "strokeWidth": 2,
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
    })


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
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
        "textAlign": align,
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
    })


def line_el(id, x, y, pts, stroke, sw=2, dash=False, op=100, start_ah=None, end_ah=None):
    """Create a line or arrow element."""
    els.append({
        "type": "arrow" if end_ah else "line",
        "id": id,
        "x": x,
        "y": y,
        "width": max(p[0] for p in pts) - min(p[0] for p in pts),
        "height": max(p[1] for p in pts) - min(p[1] for p in pts),
        "angle": 0,
        "points": pts,
        "startArrowhead": start_ah,
        "endArrowhead": end_ah,
        "startBinding": None,
        "endBinding": None,
        "elbowed": False,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": sw,
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
    })


# === LAYOUT CONSTANTS ===
CANVAS_W = 800
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Pill boxes
PILL_W = 180
PILL_H = 60
PILL_Y = TITLE_Y + TITLE_H + 30  # pills below title

# Arrow line
ARROW_Y = PILL_Y + PILL_H + 20
ARROW_X = PAD_X + 40
ARROW_W = CONTENT_W - 80

# Three pills evenly spaced
pill_positions = [
    ARROW_X + 10,                          # Batch (left)
    ARROW_X + (ARROW_W - PILL_W) // 2,    # Micro-batch (center)
    ARROW_X + ARROW_W - PILL_W - 10,      # Streaming (right)
]

# Labels below arrow
LABEL_Y = ARROW_Y + 25
LABEL_H = math.ceil(1 * 20 * 1.25)

# Frequency labels
freq_labels = ["Semi-Frequent", "Frequent", "Very Frequent"]

# Data type labels below frequency
DATA_LABEL_Y = LABEL_Y + LABEL_H + 15
DATA_LABEL_H = math.ceil(1 * 17 * 1.25)
data_labels = ["Bounded Data", "Bounded / Unbounded", "Unbounded Data"]

# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Data Ingestion Continuum", 32, color="#1e1e1e")

# Main arrow line (horizontal)
line_el("arrow-main", ARROW_X, ARROW_Y, [[0, 0], [ARROW_W, 0]],
        GRAY[0], sw=3, end_ah="arrow")

# Pill boxes: Batch, Micro-batch, Streaming
pill_colors = [BLUE, YELLOW, RED]
pill_labels = ["Batch", "Micro-batch", "Streaming"]

for i, (px, label, color) in enumerate(zip(pill_positions, pill_labels, pill_colors)):
    box_id = f"pill-{i}"
    txt_id = f"pill-t-{i}"
    rect(box_id, px, PILL_Y, PILL_W, PILL_H, color[0], color[1],
         bnd=[{"id": txt_id, "type": "text"}])
    txt(txt_id, px, PILL_Y, PILL_W, PILL_H, label, 24, cid=box_id)

# Frequency labels below arrow
for i, (px, label) in enumerate(zip(pill_positions, freq_labels)):
    txt(f"freq-{i}", px, LABEL_Y, PILL_W, LABEL_H,
        label, 20, color=GRAY[0])

# Data type labels
for i, (px, label) in enumerate(zip(pill_positions, data_labels)):
    txt(f"data-{i}", px, DATA_LABEL_Y, PILL_W, DATA_LABEL_H,
        label, 17, color=pill_colors[i][0])

# === WRITE FILE ===
outfile = os.path.join(OUT_DIR, "ingestion-continuum.excalidraw")
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
