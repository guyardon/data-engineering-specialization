#!/usr/bin/env python3
"""Generate nosql-types.excalidraw diagram — 2x2 grid of NoSQL types + characteristic pills."""

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


# ─── Colors ───
BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")

# ─── Layout constants ───
CANVAS_W = 800
PAD = 40
CONTENT_W = CANVAS_W - 2 * PAD
GAP = 30
PAIR_W = (CONTENT_W - GAP) // 2  # width of each grid cell
BOX_H = 105
VGAP = 40  # vertical gap between grid rows

# ─── Title ───
TITLE_Y = 20
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)  # 40
txt("title", PAD, TITLE_Y, CONTENT_W, TITLE_H, "NoSQL Database Types", TITLE_FSZ)

# ─── 2x2 Grid ───
GRID_Y = TITLE_Y + TITLE_H + 25


# Grid positions: (col, row) → (x, y)
def grid_pos(col, row):
    x = PAD + col * (PAIR_W + GAP)
    y = GRID_Y + row * (BOX_H + VGAP)
    return x, y


# Define the 4 types: (id, title, subtitle, color)
types = [
    ("kv", "Key-Value Stores", "e.g. caching user sessions", BLUE),
    ("doc", "Document Stores", "e.g. JSON documents, catalogs", GREEN),
    ("wcol", "Wide-Column Stores", "e.g. time-series, IoT data", PURPLE),
    ("graph", "Graph Databases", "e.g. social networks, fraud", YELLOW),
]

positions = [(0, 0), (1, 0), (0, 1), (1, 1)]

for (bid, title, subtitle, (stroke, bg)), (col, row) in zip(types, positions):
    x, y = grid_pos(col, row)
    tid = bid + "-title"
    sid = bid + "-sub"
    # Box bound to title text
    rect(bid, x, y, PAIR_W, BOX_H, stroke, bg, bnd=[{"id": tid, "type": "text"}])
    # Title text (bound, centered) — shift up slightly to make room for subtitle
    txt(tid, x, y - 10, PAIR_W, BOX_H, title, 24, color="#1e1e1e", cid=bid)
    # Subtitle text (free, positioned below title)
    sub_h = math.ceil(1 * 17 * 1.25)
    txt(sid, x, y + BOX_H * 0.55, PAIR_W, sub_h, subtitle, 17, color=stroke)

# ─── Characteristics pills row ───
PILL_Y = GRID_Y + 2 * (BOX_H + VGAP) + 30
PILL_H = 52
PILL_GAP = 20
NUM_PILLS = 3
PILL_W = (CONTENT_W - (NUM_PILLS - 1) * PILL_GAP) // NUM_PILLS

characteristics = [
    ("pill-schema", "No predefined schema", CYAN),
    ("pill-scale", "Horizontal scaling", CYAN),
    ("pill-consist", "Eventual consistency", CYAN),
]

for i, (pid, label, (stroke, bg)) in enumerate(characteristics):
    px = PAD + i * (PILL_W + PILL_GAP)
    tid = pid + "-t"
    rect(
        pid,
        px,
        PILL_Y,
        PILL_W,
        PILL_H,
        stroke,
        bg,
        dashed=True,
        bnd=[{"id": tid, "type": "text"}],
    )
    txt(tid, px, PILL_Y, PILL_W, PILL_H, label, 22, color="#1e1e1e", cid=pid)

# ─── Write output ───
out_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams"
)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "nosql-types.excalidraw")
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Done! Wrote {out_path}")
