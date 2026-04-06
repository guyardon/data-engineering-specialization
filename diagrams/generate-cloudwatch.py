"""
AWS CloudWatch diagram — System Metrics, Custom Metrics, and CloudWatch Alarms.
Three-column layout.
"""

import math
import sys

from diagramlib import BLUE, GRAY, GREEN, PURPLE, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=4000)

# === LAYOUT ===
CANVAS_W = 680
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 640
COL_GAP = 20
COL_W = (CONTENT_W - 2 * COL_GAP) // 3  # 200

TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

SUBTITLE_Y = TITLE_Y + TITLE_H + 5
SUBTITLE_H = math.ceil(1 * 17 * 1.25)

# Column start
COL_START_Y = SUBTITLE_Y + SUBTITLE_H + 25
HDR_H = 50
ITEM_H = 45
ITEM_GAP = 10
INNER_PAD = 12

COL1_X = PAD_X
COL2_X = PAD_X + COL_W + COL_GAP
COL3_X = PAD_X + 2 * (COL_W + COL_GAP)

# Column data
col1_items = ["CPU utilization", "Disk I/O", "Network traffic", "Memory usage"]
col2_items = ["Transactions\nprocessed", "API response\ntime", "Active users"]
col3_items = ["Define thresholds", "Establish baselines", "Retains data\nfor 15 months"]

# === BUILD DIAGRAM ===

# Title
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "AWS CloudWatch", 32, color="#1e1e1e")

d.txt(
    "subtitle",
    PAD_X,
    SUBTITLE_Y,
    CONTENT_W,
    SUBTITLE_H,
    "Built-in monitoring service for tracking infrastructure and application metrics",
    17,
    color=GRAY[0],
)

# --- Column 1: System Level Metrics ---
d.rect(
    "sys-hdr",
    COL1_X,
    COL_START_Y,
    COL_W,
    HDR_H,
    *BLUE,
    bnd=[{"id": "sys-hdr-t", "type": "text"}],
)
d.txt("sys-hdr-t", COL1_X, COL_START_Y, COL_W, HDR_H, "System Metrics", 22, cid="sys-hdr")

for i, item in enumerate(col1_items):
    y = COL_START_Y + HDR_H + INNER_PAD + i * (ITEM_H + ITEM_GAP)
    item_id = f"sys{i}"
    d.rect(
        item_id,
        COL1_X,
        y,
        COL_W,
        ITEM_H,
        BLUE[0],
        BLUE[1],
        opacity=50,
        bnd=[{"id": f"sys-t{i}", "type": "text"}],
    )
    d.txt(f"sys-t{i}", COL1_X, y, COL_W, ITEM_H, item, 19, cid=item_id)

# --- Column 2: Custom Metrics ---
d.rect(
    "cust-hdr",
    COL2_X,
    COL_START_Y,
    COL_W,
    HDR_H,
    *GREEN,
    bnd=[{"id": "cust-hdr-t", "type": "text"}],
)
d.txt(
    "cust-hdr-t",
    COL2_X,
    COL_START_Y,
    COL_W,
    HDR_H,
    "Custom Metrics",
    22,
    cid="cust-hdr",
)

for i, item in enumerate(col2_items):
    y = COL_START_Y + HDR_H + INNER_PAD + i * (ITEM_H + ITEM_GAP)
    item_id = f"cust{i}"
    d.rect(
        item_id,
        COL2_X,
        y,
        COL_W,
        ITEM_H,
        GREEN[0],
        GREEN[1],
        opacity=50,
        bnd=[{"id": f"cust-t{i}", "type": "text"}],
    )
    d.txt(f"cust-t{i}", COL2_X, y, COL_W, ITEM_H, item, 19, cid=item_id)

# --- Column 3: CloudWatch Alarms ---
d.rect(
    "alarm-hdr",
    COL3_X,
    COL_START_Y,
    COL_W,
    HDR_H,
    *PURPLE,
    bnd=[{"id": "alarm-hdr-t", "type": "text"}],
)
d.txt("alarm-hdr-t", COL3_X, COL_START_Y, COL_W, HDR_H, "Alarms", 22, cid="alarm-hdr")

for i, item in enumerate(col3_items):
    y = COL_START_Y + HDR_H + INNER_PAD + i * (ITEM_H + ITEM_GAP)
    item_id = f"alarm{i}"
    d.rect(
        item_id,
        COL3_X,
        y,
        COL_W,
        ITEM_H,
        PURPLE[0],
        PURPLE[1],
        opacity=50,
        bnd=[{"id": f"alarm-t{i}", "type": "text"}],
    )
    d.txt(f"alarm-t{i}", COL3_X, y, COL_W, ITEM_H, item, 19, cid=item_id)

# Arrows: System → Alarms, Custom → Alarms
d.arr(
    "sys-to-alarm",
    COL1_X + COL_W,
    COL_START_Y + HDR_H // 2,
    [[0, 0], [2 * COL_W + 2 * COL_GAP, 0]],
    GRAY[0],
    sb={"elementId": "sys-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "alarm-hdr", "focus": 0, "gap": 4},
)

d.arr(
    "cust-to-alarm",
    COL2_X + COL_W,
    COL_START_Y + HDR_H // 2,
    [[0, 0], [COL_W + COL_GAP, 0]],
    GRAY[0],
    sb={"elementId": "cust-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "alarm-hdr", "focus": 0, "gap": 4},
)

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "cloudwatch"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
