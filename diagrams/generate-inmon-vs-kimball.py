"""
Generate Inmon vs Kimball comparison diagram showing
the two warehouse data flow architectures side by side.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=11000)

# === LAYOUT ===
CANVAS_W = 680
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2
BOX_H = 55
ARROW_GAP = 50

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Inmon vs Kimball", 30, color="#1e1e1e")

# Column headers
HDR_Y = TITLE_Y + TITLE_H + 15
HDR_H = math.ceil(1 * 22 * 1.25)
d.txt("hdr_inmon", PAD_X, HDR_Y, COL_W, HDR_H, "Inmon (Top-Down)", 22, color=BLUE[0])
d.txt("hdr_kimball", PAD_X + COL_W + COL_GAP, HDR_Y, COL_W, HDR_H,
    "Kimball (Bottom-Up)", 22, color=GREEN[0])

# === INMON FLOW (left) ===
LEFT_X = PAD_X
y = HDR_Y + HDR_H + 20

inmon_steps = [
    ("i_src", "Source Systems", GRAY),
    ("i_etl", "ETL", YELLOW),
    ("i_wh", "3NF Warehouse", BLUE),
    ("i_mart", "Star Schema\nData Marts", PURPLE),
    ("i_users", "Business Users", CYAN),
]

for i, (bid, label, color) in enumerate(inmon_steps):
    h = BOX_H + 10 if "\n" in label else BOX_H
    d.rect(bid, LEFT_X, y, COL_W, h, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", LEFT_X, y, COL_W, h, label, 20, cid=bid)

    if i < len(inmon_steps) - 1:
        next_h = BOX_H + 10 if "\n" in inmon_steps[i + 1][1] else BOX_H
        d.arr(f"ai{i}", LEFT_X + COL_W // 2, y + h,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": inmon_steps[i + 1][0], "focus": 0, "gap": 4})
    y += h + ARROW_GAP

# === KIMBALL FLOW (right) ===
RIGHT_X = PAD_X + COL_W + COL_GAP
y = HDR_Y + HDR_H + 20

kimball_steps = [
    ("k_src", "Source Systems", GRAY),
    ("k_etl", "ETL", YELLOW),
    ("k_wh", "Star Schema\nWarehouse", GREEN),
    ("k_users", "Business Users", CYAN),
]

# We need to space Kimball to align bottom with Inmon
# Inmon has 5 steps, Kimball has 4 — add extra gap to align users row
kimball_gap = ARROW_GAP + (BOX_H + ARROW_GAP) // 3

for i, (bid, label, color) in enumerate(kimball_steps):
    h = BOX_H + 10 if "\n" in label else BOX_H
    d.rect(bid, RIGHT_X, y, COL_W, h, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", RIGHT_X, y, COL_W, h, label, 20, cid=bid)

    gap = kimball_gap if i == 1 else ARROW_GAP
    if i < len(kimball_steps) - 1:
        d.arr(f"ak{i}", RIGHT_X + COL_W // 2, y + h,
            [[0, 0], [0, gap]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": kimball_steps[i + 1][0], "focus": 0, "gap": 4})
    y += h + gap

# Key difference labels below
LABEL_Y = y + 10
LABEL_H = math.ceil(1 * 15 * 1.25)
d.txt("diff_inmon", PAD_X, LABEL_Y, COL_W, LABEL_H,
    "Quality first, extra modeling step", 15, color=BLUE[0])
d.txt("diff_kimball", PAD_X + COL_W + COL_GAP, LABEL_Y, COL_W, LABEL_H,
    "Speed first, direct star schemas", 15, color=GREEN[0])

print(f"Canvas: {CANVAS_W}x{LABEL_Y + LABEL_H + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "inmon-vs-kimball"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
