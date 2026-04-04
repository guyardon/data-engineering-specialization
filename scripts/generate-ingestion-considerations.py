"""Generate Ingestion Tool Selection Considerations diagram for Course 2, Section 2.4.3."""

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
seed = 5000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
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
            "strokeWidth": 2,
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


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
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


# === LAYOUT CONSTANTS ===
# Central title → two category containers stacked vertically
# Each container has a header + grid of factor pills

CANVAS_W = 850
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X  # 800

# Pill sizing (5 pills in a row for data characteristics, 2 for reliability)
PILL_H = 55
PILL_GAP = 15
PILL_PAD = 20  # padding inside container around pills

# Container sizing
CONTAINER_PAD = 25
CONTAINER_HDR_H = 45

# Vertical positions
TITLE_Y = 10
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)

SUBTITLE_Y = TITLE_Y + TITLE_H + 5
SUBTITLE_FSZ = 19
SUBTITLE_H = math.ceil(1 * SUBTITLE_FSZ * 1.25)

# Container 1: Data Characteristics (5 pills in a row, then wrap)
C1_Y = SUBTITLE_Y + SUBTITLE_H + 25
C1_PILLS = ["Data Type &\nStructure", "Data\nVolume", "Latency\nRequirements", "Data\nQuality", "Schema\nChanges"]
C1_COLS = 5
C1_PILL_W = (CONTENT_W - 2 * CONTAINER_PAD - (C1_COLS - 1) * PILL_GAP) // C1_COLS
C1_ROWS = 1
C1_H = CONTAINER_HDR_H + PILL_PAD + C1_ROWS * PILL_H + CONTAINER_PAD

# Container 2: Reliability & Durability (2 pills centered)
C2_Y = C1_Y + C1_H + 30
C2_PILLS = ["Reliability\nProper function under load", "Durability\nData not lost or corrupted"]
C2_COLS = 2
C2_PILL_W = 320
C2_PILL_TOTAL = 2 * C2_PILL_W + PILL_GAP
C2_PILL_X_START = PAD_X + CONTAINER_PAD + (CONTENT_W - 2 * CONTAINER_PAD - C2_PILL_TOTAL) // 2
C2_H = CONTAINER_HDR_H + PILL_PAD + PILL_H + CONTAINER_PAD

# Arrow between containers
ARR_GAP_C = 30

# Adjust C2_Y to account for arrow
C2_Y = C1_Y + C1_H + ARR_GAP_C


# === BUILD DIAGRAM ===

# Main title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Choosing Ingestion Tools", TITLE_FSZ)
txt("subtitle", PAD_X, SUBTITLE_Y, CONTENT_W, SUBTITLE_H, "Key evaluation criteria", SUBTITLE_FSZ, color=GRAY[0])

# --- Container 1: Data Characteristics ---
rect("c1", PAD_X, C1_Y, CONTENT_W, C1_H, *BLUE, opacity=30, dashed=True)
# Container header
txt("c1-hdr", PAD_X, C1_Y + 8, CONTENT_W, math.ceil(24 * 1.25), "Data Characteristics", 24, color=BLUE[0])

# Pills
C1_COLORS = [BLUE, CYAN, GREEN, YELLOW, PURPLE]
pill_start_y = C1_Y + CONTAINER_HDR_H + PILL_PAD
for i, (label, color) in enumerate(zip(C1_PILLS, C1_COLORS)):
    px = PAD_X + CONTAINER_PAD + i * (C1_PILL_W + PILL_GAP)
    py = pill_start_y
    pid = f"c1-p{i}"
    rect(pid, px, py, C1_PILL_W, PILL_H, *color, bnd=[{"id": f"{pid}-t", "type": "text"}])
    txt(f"{pid}-t", px, py, C1_PILL_W, PILL_H, label, 18, cid=pid)

# Arrow down
arr_x = PAD_X + CONTENT_W // 2
arr(
    "c-arr",
    arr_x,
    C1_Y + C1_H,
    [[0, 0], [0, ARR_GAP_C]],
    GRAY[0],
    dash=True,
)

# --- Container 2: Reliability & Durability ---
rect("c2", PAD_X, C2_Y, CONTENT_W, C2_H, *RED, opacity=30, dashed=True)
txt("c2-hdr", PAD_X, C2_Y + 8, CONTENT_W, math.ceil(24 * 1.25), "Reliability & Durability", 24, color=RED[0])

C2_COLORS = [RED, PURPLE]
pill_start_y2 = C2_Y + CONTAINER_HDR_H + PILL_PAD
for i, (label, color) in enumerate(zip(C2_PILLS, C2_COLORS)):
    px = C2_PILL_X_START + i * (C2_PILL_W + PILL_GAP)
    py = pill_start_y2
    pid = f"c2-p{i}"
    rect(pid, px, py, C2_PILL_W, PILL_H, *color, bnd=[{"id": f"{pid}-t", "type": "text"}])
    txt(f"{pid}-t", px, py, C2_PILL_W, PILL_H, label, 18, cid=pid)

# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"C1: y={C1_Y}, h={C1_H}, pills={C1_PILL_W}w")
print(f"C2: y={C2_Y}, h={C2_H}, pills={C2_PILL_W}w")
print(f"Bottom: {C2_Y + C2_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/ingestion-considerations"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
