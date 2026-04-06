"""
Generate views vs materialized views comparison diagram showing
how views recompute on every query while materialized views
serve cached results.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, GREEN, YELLOW, RED, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=15000)

CANVAS_W = 680
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2
BOX_H = 55
ARROW_GAP = 50

TITLE_Y = 12
TITLE_H = math.ceil(1 * 28 * 1.25)
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "View vs Materialized View",
    28,
    color="#1e1e1e",
)

HDR_Y = TITLE_Y + TITLE_H + 15
HDR_H = math.ceil(1 * 20 * 1.25)
d.txt("hdr_view", PAD_X, HDR_Y, COL_W, HDR_H, "View (recomputes)", 20, color=YELLOW[0])
d.txt(
    "hdr_mv",
    PAD_X + COL_W + COL_GAP,
    HDR_Y,
    COL_W,
    HDR_H,
    "Materialized View (cached)",
    20,
    color=GREEN[0],
)

# === LEFT: View flow ===
LX = PAD_X
y = HDR_Y + HDR_H + 20

view_steps = [
    ("v_query", "SELECT * FROM\ndaily_sales", GRAY),
    ("v_exec", "Re-execute\nSQL definition", YELLOW),
    ("v_scan", "Scan base\ntables", RED),
    ("v_result", "Fresh result\n(always current)", GREEN),
]

for i, (bid, label, color) in enumerate(view_steps):
    h = BOX_H + 10
    d.rect(bid, LX, y, COL_W, h, *color, bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", LX, y, COL_W, h, label, 18, cid=bid)

    if i < len(view_steps) - 1:
        d.arr(
            f"av{i}",
            LX + COL_W // 2,
            y + h,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": view_steps[i + 1][0], "focus": 0, "gap": 4},
        )
    y += h + ARROW_GAP

view_bottom = y

# === RIGHT: Materialized View flow ===
RX = PAD_X + COL_W + COL_GAP
y = HDR_Y + HDR_H + 20

mv_steps = [
    ("mv_query", "SELECT * FROM\ndaily_sales_mv", GRAY),
    ("mv_cache", "Read cached\nresult from disk", GREEN),
    ("mv_result", "Fast result\n(may be stale)", CYAN),
]

# Center vertically -- fewer steps
mv_total = len(mv_steps) * (BOX_H + 10 + ARROW_GAP) - ARROW_GAP
view_total = len(view_steps) * (BOX_H + 10 + ARROW_GAP) - ARROW_GAP
mv_start_y = HDR_Y + HDR_H + 20 + (view_total - mv_total) // 2

y = mv_start_y
for i, (bid, label, color) in enumerate(mv_steps):
    h = BOX_H + 10
    d.rect(bid, RX, y, COL_W, h, *color, bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", RX, y, COL_W, h, label, 18, cid=bid)

    if i < len(mv_steps) - 1:
        d.arr(
            f"amv{i}",
            RX + COL_W // 2,
            y + h,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": mv_steps[i + 1][0], "focus": 0, "gap": 4},
        )
    y += h + ARROW_GAP

# Refresh note for MV
REFRESH_Y = y + 5
REFRESH_H = math.ceil(1 * 14 * 1.25)
d.txt(
    "refresh",
    RX,
    REFRESH_Y,
    COL_W,
    REFRESH_H,
    "REFRESH MATERIALIZED VIEW to update",
    14,
    color=PURPLE[0],
)

print(f"Canvas: {CANVAS_W}x{max(view_bottom, REFRESH_Y + REFRESH_H) + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/views-vs-materialized"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
