#!/usr/bin/env python3
"""Generate nosql-types.excalidraw diagram — 2x2 grid of NoSQL types + characteristic pills."""

import math

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, YELLOW, CYAN

d = ExcalidrawDiagram(seed=3000)

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
d.txt("title", PAD, TITLE_Y, CONTENT_W, TITLE_H, "NoSQL Database Types", TITLE_FSZ)

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
    d.rect(bid, x, y, PAIR_W, BOX_H, stroke, bg, bnd=[{"id": tid, "type": "text"}])
    # Title text (bound, centered) — shift up slightly to make room for subtitle
    d.txt(tid, x, y - 10, PAIR_W, BOX_H, title, 24, color="#1e1e1e", cid=bid)
    # Subtitle text (free, positioned below title)
    sub_h = math.ceil(1 * 17 * 1.25)
    d.txt(sid, x, y + BOX_H * 0.55, PAIR_W, sub_h, subtitle, 17, color=stroke)

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
    d.rect(
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
    d.txt(tid, px, PILL_Y, PILL_W, PILL_H, label, 22, color="#1e1e1e", cid=pid)

# ─── Write output ───
d.save("diagrams/artifacts/nosql-types.excalidraw")
print("Done! Wrote diagrams/nosql-types.excalidraw")
