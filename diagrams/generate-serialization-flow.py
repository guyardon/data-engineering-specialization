"""
Serialization and compression flow diagram.
Shows: In-memory Format → Serialize → Disk Format → Compress → Storage-efficient Format
Then fan-out to: File, Database, Network

Vertical flow with fan-out at the bottom. Canvas: 650px wide.
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
seed = 4000


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
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 250      # main box width
BH = 65       # main box height
ARROW_V = 70  # vertical arrow gap
SMALL_BW = 150
SMALL_BH = 50

# Center X for main flow
CX = CANVAS_W // 2
BOX_X = CX - BW // 2

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40,
    "Serialization & Compression", 32)
txt("sub", PAD_X, TITLE_Y + 38, CONTENT_W, 25,
    "From in-memory data structures to persistent storage", 17, color=BLUE[0])

# === BOX 1: In-memory Format ===
B1_Y = 90
rect("b1", BOX_X, B1_Y, BW, BH, *BLUE,
     bnd=[{"id": "t1", "type": "text"}])
txt("t1", BOX_X, B1_Y, BW, BH, "In-Memory Format\n(CPU-optimized)", 20, cid="b1")

# Arrow B1 → B2
arr("a12", CX, B1_Y + BH, [[0, 0], [0, ARROW_V]], BLUE[0],
    sb={"elementId": "b1", "focus": 0, "gap": 4},
    eb={"elementId": "b2", "focus": 0, "gap": 4})
# Label: Serialize
txt("l_ser", CX + 10, B1_Y + BH + 20, 80, 25, "Serialize", 17, color=BLUE[0])

# === BOX 2: Disk Format ===
B2_Y = B1_Y + BH + ARROW_V
rect("b2", BOX_X, B2_Y, BW, BH, *GREEN,
     bnd=[{"id": "t2", "type": "text"}])
txt("t2", BOX_X, B2_Y, BW, BH, "Disk Format\n(01001010...)", 20, cid="b2")

# Arrow B2 → B3
arr("a23", CX, B2_Y + BH, [[0, 0], [0, ARROW_V]], GREEN[0],
    sb={"elementId": "b2", "focus": 0, "gap": 4},
    eb={"elementId": "b3", "focus": 0, "gap": 4})
# Label: Compress
txt("l_cmp", CX + 10, B2_Y + BH + 20, 80, 25, "Compress", 17, color=GREEN[0])

# === BOX 3: Storage-efficient Format ===
B3_Y = B2_Y + BH + ARROW_V
rect("b3", BOX_X, B3_Y, BW, BH, *PURPLE,
     bnd=[{"id": "t3", "type": "text"}])
txt("t3", BOX_X, B3_Y, BW, BH, "Storage-Efficient\nFormat", 20, cid="b3")

# === Fan-out to 3 destinations ===
FAN_Y = B3_Y + BH + ARROW_V + 10
FAN_GAP = 20
# Three small boxes in a row
fan_labels = ["File", "Database", "Network"]
fan_colors = [CYAN, YELLOW, GRAY]
total_fan_w = 3 * SMALL_BW + 2 * FAN_GAP
fan_start_x = CX - total_fan_w // 2

for i, (label, color) in enumerate(zip(fan_labels, fan_colors)):
    fx = fan_start_x + i * (SMALL_BW + FAN_GAP)
    fid = f"fan{i}"
    ftid = f"fant{i}"
    rect(fid, fx, FAN_Y, SMALL_BW, SMALL_BH, *color,
         bnd=[{"id": ftid, "type": "text"}])
    txt(ftid, fx, FAN_Y, SMALL_BW, SMALL_BH, label, 20, cid=fid)

    # Arrow from B3 center to each fan box
    dx = fx + SMALL_BW // 2 - CX
    dy = FAN_Y - (B3_Y + BH)
    arr(f"afan{i}", CX, B3_Y + BH, [[0, 0], [dx, dy]], PURPLE[0], dash=True,
        sb={"elementId": "b3", "focus": 0, "gap": 4},
        eb={"elementId": fid, "focus": 0, "gap": 4})

# === Reverse arrow label (De-serialize) on the left ===
txt("l_deser", BOX_X - 110, B1_Y + BH + 20, 100, 25, "De-serialize", 16, color=GRAY[0], op=70)
arr("a_deser", CX - BW // 2 - 15, B2_Y, [[0, 0], [0, -ARROW_V]], GRAY[0], dash=True, op=50)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "serialization-flow"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
