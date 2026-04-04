"""
Generate views vs materialized views comparison diagram showing
how views recompute on every query while materialized views
serve cached results.
"""

import json
import math
import sys

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 15000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append({
        "type": "rectangle", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
        "opacity": opacity, "roundness": {"type": 3},
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": bnd or [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True if cid else False, "containerId": cid,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({
        "type": "arrow", "id": id, "x": x, "y": y,
        "width": abs(pts[-1][0] - pts[0][0]), "height": abs(pts[-1][1] - pts[0][1]),
        "angle": 0, "points": pts,
        "startArrowhead": None, "endArrowhead": "arrow",
        "startBinding": sb, "endBinding": eb, "elbowed": False,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dash else "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


CANVAS_W = 680
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2
BOX_H = 55
ARROW_GAP = 50

TITLE_Y = 12
TITLE_H = math.ceil(1 * 28 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "View vs Materialized View", 28, color="#1e1e1e")

HDR_Y = TITLE_Y + TITLE_H + 15
HDR_H = math.ceil(1 * 20 * 1.25)
txt("hdr_view", PAD_X, HDR_Y, COL_W, HDR_H,
    "View (recomputes)", 20, color=YELLOW[0])
txt("hdr_mv", PAD_X + COL_W + COL_GAP, HDR_Y, COL_W, HDR_H,
    "Materialized View (cached)", 20, color=GREEN[0])

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
    rect(bid, LX, y, COL_W, h, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", LX, y, COL_W, h, label, 18, cid=bid)

    if i < len(view_steps) - 1:
        arr(f"av{i}", LX + COL_W // 2, y + h,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": view_steps[i + 1][0], "focus": 0, "gap": 4})
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

# Center vertically — fewer steps
mv_total = len(mv_steps) * (BOX_H + 10 + ARROW_GAP) - ARROW_GAP
view_total = len(view_steps) * (BOX_H + 10 + ARROW_GAP) - ARROW_GAP
mv_start_y = HDR_Y + HDR_H + 20 + (view_total - mv_total) // 2

y = mv_start_y
for i, (bid, label, color) in enumerate(mv_steps):
    h = BOX_H + 10
    rect(bid, RX, y, COL_W, h, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", RX, y, COL_W, h, label, 18, cid=bid)

    if i < len(mv_steps) - 1:
        arr(f"amv{i}", RX + COL_W // 2, y + h,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": mv_steps[i + 1][0], "focus": 0, "gap": 4})
    y += h + ARROW_GAP

# Refresh note for MV
REFRESH_Y = y + 5
REFRESH_H = math.ceil(1 * 14 * 1.25)
txt("refresh", RX, REFRESH_Y, COL_W, REFRESH_H,
    "REFRESH MATERIALIZED VIEW to update", 14, color=PURPLE[0])

print(f"Canvas: {CANVAS_W}x{max(view_bottom, REFRESH_Y + REFRESH_H) + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "views-vs-materialized"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
