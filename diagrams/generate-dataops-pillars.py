"""
DataOps 3 Pillars diagram for section 3.1.1.
Shows DataOps at top with three pillars below, each with key sub-items.
"""

import json
import math
import sys

# === FILE STRUCTURE ===

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


# === HELPER FUNCTIONS ===


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
        "autoResize": True, "containerId": cid,
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
        "width": pts[-1][0] - pts[0][0], "height": pts[-1][1] - pts[0][1],
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


# === LAYOUT CONSTANTS ===

CANVAS_W = 660
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 600

# Title
TITLE_Y = 20

# Top DataOps box
TOP_Y = 65
TOP_W = 300
TOP_H = 60
TOP_X = (CANVAS_W - TOP_W) // 2

# Subtitle under DataOps
SUB_Y = TOP_Y + TOP_H + 8

# Three pillars
COL_W = 180
COL_GAP = 30
TOTAL_COLS_W = 3 * COL_W + 2 * COL_GAP  # 600
COL_START_X = PAD_X
PILLAR_Y = SUB_Y + 30 + 75  # after subtitle + arrow gap
PILLAR_H = 60

# Sub-item pills under each pillar
PILL_GAP = 12
PILL_H = 40
PILL_Y1 = PILLAR_Y + PILLAR_H + 75  # arrow gap
PILL_Y2 = PILL_Y1 + PILL_H + PILL_GAP

# Arrow gap between DataOps and pillars
ARROW_GAP = 75

# === BUILD DIAGRAM ===

# Title
txt("title", 0, TITLE_Y, CANVAS_W, 40, "DataOps", 32)

# Main DataOps box
rect("dataops", TOP_X, TOP_Y + 55, TOP_W, TOP_H, *PURPLE,
     bnd=[{"id": "t_dataops", "type": "text"},
          {"id": "a1", "type": "arrow"},
          {"id": "a2", "type": "arrow"},
          {"id": "a3", "type": "arrow"}])
txt("t_dataops", TOP_X, TOP_Y + 55, TOP_W, TOP_H,
    "DataOps", 26, cid="dataops")

# Subtitle
txt("sub", 0, TOP_Y + 55 + TOP_H + 5, CANVAS_W, 25,
    "Practices for building robust data systems", 18, color=PURPLE[0])

# Three pillar columns
col_xs = [COL_START_X + i * (COL_W + COL_GAP) for i in range(3)]
PILLAR_TOP = TOP_Y + 55 + TOP_H + 5 + 25 + ARROW_GAP

pillars = [
    ("p1", "Automation", BLUE),
    ("p2", "Observability\n& Monitoring", GREEN),
    ("p3", "Incident\nResponse", YELLOW),
]

for i, (pid, label, color) in enumerate(pillars):
    px = col_xs[i]
    rect(pid, px, PILLAR_TOP, COL_W, PILLAR_H, *color,
         bnd=[{"id": f"t_{pid}", "type": "text"}])
    txt(f"t_{pid}", px, PILLAR_TOP, COL_W, PILLAR_H,
        label, 22, cid=pid)

# Arrows from DataOps to pillars
dataops_cx = TOP_X + TOP_W // 2
dataops_bottom = TOP_Y + 55 + TOP_H

for i, (pid, _, color) in enumerate(pillars):
    px = col_xs[i] + COL_W // 2
    arr(f"a{i+1}", dataops_cx, dataops_bottom + 30,
        [[0, 0], [px - dataops_cx, PILLAR_TOP - dataops_bottom - 30]],
        color[0],
        sb={"elementId": "dataops", "focus": 0, "gap": 4},
        eb={"elementId": pid, "focus": 0, "gap": 4})

# Sub-items under each pillar
sub_items = [
    [("CI/CD Pipelines", BLUE), ("Infrastructure\nas Code", BLUE)],
    [("Data Quality\nChecks", GREEN), ("Pipeline\nMetrics", GREEN)],
    [("Alerting &\nEscalation", YELLOW), ("Root Cause\nAnalysis", YELLOW)],
]

SUB_TOP = PILLAR_TOP + PILLAR_H + 70

for i, items in enumerate(sub_items):
    px = col_xs[i]
    for j, (label, color) in enumerate(items):
        sy = SUB_TOP + j * (PILL_H + PILL_GAP)
        sid = f"s{i}_{j}"
        rect(sid, px, sy, COL_W, PILL_H, color[0], color[1],
             bnd=[{"id": f"t_{sid}", "type": "text"}])
        txt(f"t_{sid}", px, sy, COL_W, PILL_H,
            label, 18, cid=sid)

    # Arrow from pillar to first sub-item
    arr(f"pa{i}", col_xs[i] + COL_W // 2, PILLAR_TOP + PILLAR_H,
        [[0, 0], [0, 70]],
        pillars[i][2][0],
        sb={"elementId": pillars[i][0], "focus": 0, "gap": 4},
        eb={"elementId": f"s{i}_0", "focus": 0, "gap": 4})


# === VERIFY ===
print(f"Title: y={TITLE_Y}")
print(f"DataOps box: y={TOP_Y + 55} to {TOP_Y + 55 + TOP_H}")
print(f"Pillars: y={PILLAR_TOP} to {PILLAR_TOP + PILLAR_H}")
print(f"Sub-items: y={SUB_TOP} to {SUB_TOP + PILL_H + PILL_GAP + PILL_H}")
print(f"Canvas width: {CANVAS_W}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "dataops-pillars"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
