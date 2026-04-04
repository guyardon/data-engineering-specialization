"""
Observability Concepts diagram — DevOps vs Data Observability comparison.
Two-column layout with a shared title.
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
seed = 1000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
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
            "textAlign": align,
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
            "width": pts[-1][0] - pts[0][0],
            "height": pts[-1][1] - pts[0][1],
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
CANVAS_W = 650
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 610
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2  # 290

# Positions
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)  # 40

# Column headers
HDR_Y = TITLE_Y + TITLE_H + 30  # 90
HDR_H = 55

# Description boxes
DESC_Y = HDR_Y + HDR_H + 20  # 165
DESC_H = 110

# Bullet items
BULLET_Y = DESC_Y + DESC_H + 20  # 295
BULLET_H = 170

LEFT_X = PAD_X
RIGHT_X = PAD_X + COL_W + COL_GAP

# === BUILD DIAGRAM ===

# Title
title_w = CONTENT_W
txt(
    "title",
    PAD_X,
    TITLE_Y,
    title_w,
    TITLE_H,
    "Observability Concepts",
    32,
    color="#1e1e1e",
)

# --- Left column: DevOps Observability ---
rect(
    "devops-hdr",
    LEFT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    *BLUE,
    bnd=[{"id": "devops-hdr-t", "type": "text"}],
)
txt(
    "devops-hdr-t",
    LEFT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    "DevOps Observability",
    24,
    cid="devops-hdr",
)

rect(
    "devops-desc",
    LEFT_X,
    DESC_Y,
    COL_W,
    DESC_H,
    BLUE[0],
    "transparent",
    dashed=True,
    bnd=[{"id": "devops-desc-t", "type": "text"}],
)
txt(
    "devops-desc-t",
    LEFT_X,
    DESC_Y,
    COL_W,
    DESC_H,
    "Monitors system health:\nCPU, RAM, response time.\nDetects anomalies and\nprevents downtime.",
    20,
    color=BLUE[0],
    cid="devops-desc",
)

rect(
    "devops-metrics",
    LEFT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    BLUE[0],
    "#dbe4ff",
    bnd=[{"id": "devops-metrics-t", "type": "text"}],
)
txt(
    "devops-metrics-t",
    LEFT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    "• CPU utilization\n• Memory usage\n• Response time\n• Error rates\n• Uptime / availability",
    20,
    cid="devops-metrics",
)

# --- Right column: Data Observability ---
rect(
    "data-hdr",
    RIGHT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    *GREEN,
    bnd=[{"id": "data-hdr-t", "type": "text"}],
)
txt(
    "data-hdr-t", RIGHT_X, HDR_Y, COL_W, HDR_H, "Data Observability", 24, cid="data-hdr"
)

rect(
    "data-desc",
    RIGHT_X,
    DESC_Y,
    COL_W,
    DESC_H,
    GREEN[0],
    "transparent",
    dashed=True,
    bnd=[{"id": "data-desc-t", "type": "text"}],
)
txt(
    "data-desc-t",
    RIGHT_X,
    DESC_Y,
    COL_W,
    DESC_H,
    "Monitors data health:\naccuracy, completeness,\ntimeliness. Mitigates\nupstream changes.",
    20,
    color=GREEN[0],
    cid="data-desc",
)

rect(
    "data-metrics",
    RIGHT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    GREEN[0],
    "#d3f9d8",
    bnd=[{"id": "data-metrics-t", "type": "text"}],
)
txt(
    "data-metrics-t",
    RIGHT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    "• Is the data up-to-date?\n• Is the data complete?\n• Are fields in range?\n• Is null rate expected?\n• Has the schema changed?",
    20,
    cid="data-metrics",
)

# Arrow from DevOps to Data (showing evolution)
arr(
    "evolve",
    LEFT_X + COL_W,
    HDR_Y + HDR_H // 2,
    [[0, 0], [COL_GAP, 0]],
    GRAY[0],
    sb={"elementId": "devops-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "data-hdr", "focus": 0, "gap": 4},
)

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "observability-concepts"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
