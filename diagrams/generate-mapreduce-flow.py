"""
Generate MapReduce flow diagram showing Map → Shuffle → Reduce
with a word count example.
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
seed = 13000


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
COL_GAP = 12

TITLE_Y = 12
TITLE_H = math.ceil(1 * 28 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "MapReduce: Count User Events", 28, color="#1e1e1e")

# Three columns: Map, Shuffle, Reduce
COL_W = (CONTENT_W - 2 * COL_GAP) // 3

HDR_Y = TITLE_Y + TITLE_H + 15
HDR_H = math.ceil(1 * 20 * 1.25)
txt("hdr_map", PAD_X, HDR_Y, COL_W, HDR_H, "Map", 20, color=BLUE[0])
txt("hdr_shuf", PAD_X + COL_W + COL_GAP, HDR_Y, COL_W, HDR_H, "Shuffle", 20, color=YELLOW[0])
txt("hdr_red", PAD_X + 2 * (COL_W + COL_GAP), HDR_Y, COL_W, HDR_H, "Reduce", 20, color=GREEN[0])

PILL_H = 38
PILL_GAP = 6
START_Y = HDR_Y + HDR_H + 12

# === MAP: input blocks emit key-value pairs ===
map_x = PAD_X
map_items = [
    ("m1", "(A, 1)", BLUE),
    ("m2", "(B, 1)", BLUE),
    ("m3", "(A, 1)", BLUE),
    ("m4", "(C, 1)", BLUE),
    ("m5", "(B, 1)", BLUE),
    ("m6", "(A, 1)", BLUE),
]

for i, (bid, label, color) in enumerate(map_items):
    y = START_Y + i * (PILL_H + PILL_GAP)
    rect(bid, map_x, y, COL_W, PILL_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", map_x, y, COL_W, PILL_H, label, 18, cid=bid)

# === SHUFFLE: group by key ===
shuf_x = PAD_X + COL_W + COL_GAP
shuf_items = [
    ("s1", "A → [1, 1, 1]", YELLOW),
    ("s2", "B → [1, 1]", YELLOW),
    ("s3", "C → [1]", YELLOW),
]

# Center vertically in the column
shuf_total = len(shuf_items) * (PILL_H + PILL_GAP) - PILL_GAP
map_total = len(map_items) * (PILL_H + PILL_GAP) - PILL_GAP
shuf_start = START_Y + (map_total - shuf_total) // 2

for i, (bid, label, color) in enumerate(shuf_items):
    y = shuf_start + i * (PILL_H + PILL_GAP)
    rect(bid, shuf_x, y, COL_W, PILL_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", shuf_x, y, COL_W, PILL_H, label, 18, cid=bid)

# === REDUCE: sum values ===
red_x = PAD_X + 2 * (COL_W + COL_GAP)
red_items = [
    ("r1", "A = 3", GREEN),
    ("r2", "B = 2", GREEN),
    ("r3", "C = 1", GREEN),
]

red_start = shuf_start  # align with shuffle

for i, (bid, label, color) in enumerate(red_items):
    y = red_start + i * (PILL_H + PILL_GAP)
    rect(bid, red_x, y, COL_W, PILL_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", red_x, y, COL_W, PILL_H, label, 18, cid=bid)

# Arrows between columns
map_mid_y = START_Y + map_total // 2
shuf_mid_y = shuf_start + shuf_total // 2

arr("a_map_shuf", map_x + COL_W, map_mid_y,
    [[0, 0], [COL_GAP, 0]],
    BLUE[0])

arr("a_shuf_red", shuf_x + COL_W, shuf_mid_y,
    [[0, 0], [COL_GAP, 0]],
    YELLOW[0])

# Disk write warning
DISK_Y = START_Y + map_total + 20
DISK_H = math.ceil(1 * 15 * 1.25)
txt("disk_note", PAD_X, DISK_Y, CONTENT_W, DISK_H,
    "Each phase writes to disk — no in-memory caching (unlike Spark)",
    15, color=RED[0])

print(f"Canvas: {CANVAS_W}x{DISK_Y + DISK_H + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "mapreduce-flow"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
