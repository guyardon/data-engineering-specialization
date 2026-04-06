"""
Observability Concepts diagram — DevOps vs Data Observability comparison.
Two-column layout with a shared title.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GRAY, GREEN

d = ExcalidrawDiagram(seed=1000)

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
d.txt(
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
d.rect(
    "devops-hdr",
    LEFT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    *BLUE,
    bnd=[{"id": "devops-hdr-t", "type": "text"}],
)
d.txt(
    "devops-hdr-t",
    LEFT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    "DevOps Observability",
    24,
    cid="devops-hdr",
)

d.rect(
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
d.txt(
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

d.rect(
    "devops-metrics",
    LEFT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    BLUE[0],
    "#dbe4ff",
    bnd=[{"id": "devops-metrics-t", "type": "text"}],
)
d.txt(
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
d.rect(
    "data-hdr",
    RIGHT_X,
    HDR_Y,
    COL_W,
    HDR_H,
    *GREEN,
    bnd=[{"id": "data-hdr-t", "type": "text"}],
)
d.txt(
    "data-hdr-t", RIGHT_X, HDR_Y, COL_W, HDR_H, "Data Observability", 24, cid="data-hdr"
)

d.rect(
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
d.txt(
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

d.rect(
    "data-metrics",
    RIGHT_X,
    BULLET_Y,
    COL_W,
    BULLET_H,
    GREEN[0],
    "#d3f9d8",
    bnd=[{"id": "data-metrics-t", "type": "text"}],
)
d.txt(
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
d.arr(
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
d.save(outfile)
print(f"Wrote {outfile}")
