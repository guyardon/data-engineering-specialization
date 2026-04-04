"""
CAP Theorem diagram.
Three properties in a triangle with labels showing you can only pick 2.
CP, AP, CA pairs shown as connections.

Canvas: 600px wide, compact.
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
seed = 7000


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


def line(id, x, y, pts, stroke, dash=False, op=100):
    """A line (no arrowhead)."""
    els.append({
        "type": "arrow", "id": id, "x": x, "y": y,
        "width": abs(pts[-1][0] - pts[0][0]), "height": abs(pts[-1][1] - pts[0][1]),
        "angle": 0, "points": pts,
        "startArrowhead": None, "endArrowhead": None,
        "startBinding": None, "endBinding": None, "elbowed": False,
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
BW = 200  # property box width
BH = 65   # property box height

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40,
    "CAP Theorem", 32)
txt("sub", PAD_X, TITLE_Y + 38, CONTENT_W, 25,
    "Choose at most two of three guarantees", 17, color=RED[0])

# Triangle layout:
#        C (top center)
#       / \
#      /   \
#     A --- P (bottom left, bottom right)
CX = CANVAS_W // 2

# Consistency (top center)
C_X = CX - BW // 2
C_Y = 100
rect("c", C_X, C_Y, BW, BH, *BLUE,
     bnd=[{"id": "ct", "type": "text"}])
txt("ct", C_X, C_Y, BW, BH, "Consistency\nLatest data on every read", 17, cid="c")

# Availability (bottom left)
A_X = PAD_X + 15
A_Y = 310
rect("a", A_X, A_Y, BW, BH, *GREEN,
     bnd=[{"id": "at", "type": "text"}])
txt("at", A_X, A_Y, BW, BH, "Availability\nEvery request gets a response", 17, cid="a")

# Partition tolerance (bottom right)
P_X = CANVAS_W - PAD_X - BW - 15
P_Y = 310
rect("p", P_X, P_Y, BW, BH, *YELLOW,
     bnd=[{"id": "pt", "type": "text"}])
txt("pt", P_X, P_Y, BW, BH, "Partition Tolerance\nSurvives network splits", 17, cid="p")

# Triangle edges (lines connecting the 3 boxes)
# C bottom-center to A top-center
line("l_ca", C_X + BW // 2, C_Y + BH,
     [[0, 0], [A_X + BW // 2 - C_X - BW // 2, A_Y - C_Y - BH]],
     GRAY[0], dash=True, op=50)

# C bottom-center to P top-center
line("l_cp", C_X + BW // 2, C_Y + BH,
     [[0, 0], [P_X + BW // 2 - C_X - BW // 2, P_Y - C_Y - BH]],
     GRAY[0], dash=True, op=50)

# A right-center to P left-center
line("l_ap", A_X + BW, A_Y + BH // 2,
     [[0, 0], [P_X - A_X - BW, 0]],
     GRAY[0], dash=True, op=50)

# Edge labels showing system types
# CA edge (left side) — theoretical only
txt("l_ca_t", A_X - 15, C_Y + BH + 30, 100, 40,
    "CA\n(single node)", 15, color=GRAY[0], op=60)

# CP edge (right side) — HBase, MongoDB
txt("l_cp_t", P_X + BW - 80, C_Y + BH + 30, 120, 40,
    "CP\nHBase, MongoDB", 15, color=BLUE[0], op=80)

# AP edge (bottom) — Cassandra, DynamoDB
txt("l_ap_t", CX - 75, A_Y + BH + 15, 150, 40,
    "AP\nCassandra, DynamoDB", 15, color=GREEN[0], op=80)

# Center note
txt("center_note", CX - 90, 230, 180, 40,
    "Pick 2\n(can't have all 3)", 18, color=RED[0], op=80)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "cap-theorem"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
