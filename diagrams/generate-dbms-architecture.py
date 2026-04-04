"""
DBMS Architecture diagram.
Vertical stack showing the 4 layers of a database management system:
  Client Application → Transport System → Query Processor → Execution Engine → Storage Engine

Canvas: 600px wide (narrow for vertical).
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
seed = 8000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "middle", "lineHeight": 1.25,
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


# === LAYOUT ===
CANVAS_W = 600
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 300      # box width (Rule 24: derived from canvas)
BH = 70       # box height
ARROW_GAP = 70  # Rule 17
BOX_X = PAD_X + (CONTENT_W - BW) // 2

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40,
    "DBMS Architecture", 32)
txt("sub", PAD_X, TITLE_Y + 38, CONTENT_W, 25,
    "Layers of a database management system", 17, color=BLUE[0])

# === Layers (top to bottom) ===
layers = [
    ("client", "Client Application", "SQL queries, API calls", GRAY),
    ("transport", "Transport System", "Handles client connections", CYAN),
    ("query", "Query Processor", "Parses & optimizes queries", BLUE),
    ("exec", "Execution Engine", "Runs the query plan", GREEN),
    ("storage", "Storage Engine", "Serialization, disk layout, indexes", YELLOW),
]

START_Y = 90

for i, (lid, title, subtitle, color) in enumerate(layers):
    by = START_Y + i * (BH + ARROW_GAP)

    rect(lid, BOX_X, by, BW, BH, *color,
         bnd=[{"id": f"{lid}_t", "type": "text"}])
    # Rule 13: title + subtitle
    txt(f"{lid}_t", BOX_X, by, BW, BH,
        f"{title}\n{subtitle}", 18, cid=lid)

    # Arrow to next layer (except last)
    if i < len(layers) - 1:
        arr(f"a_{i}", BOX_X + BW // 2, by + BH,
            [[0, 0], [0, ARROW_GAP]], color[0],
            sb={"elementId": lid, "focus": 0, "gap": 4},
            eb={"elementId": layers[i + 1][0], "focus": 0, "gap": 4})

# Disk icon at the bottom (simple rect)
DISK_Y = START_Y + len(layers) * (BH + ARROW_GAP) - ARROW_GAP + BH + 15
DISK_W = 160
DISK_H = 50
DISK_X = BOX_X + (BW - DISK_W) // 2
rect("disk", DISK_X, DISK_Y, DISK_W, DISK_H, *GRAY, dashed=True,
     bnd=[{"id": "disk_t", "type": "text"}])
txt("disk_t", DISK_X, DISK_Y, DISK_W, DISK_H, "Disk (SSD / HDD)", 17, cid="disk")

# Arrow storage → disk
arr("a_disk", BOX_X + BW // 2, DISK_Y - 15,
    [[0, 0], [0, 15]], YELLOW[0], dash=True,
    sb={"elementId": "storage", "focus": 0, "gap": 4},
    eb={"elementId": "disk", "focus": 0, "gap": 4})

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "dbms-architecture"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
