#!/usr/bin/env python3
"""Generate Excalidraw diagram: Batch vs Streaming Ingestion Considerations."""

import json
import math
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diagrams",
)
os.makedirs(OUT_DIR, exist_ok=True)

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 2000


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


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append({
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
    })


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
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
    })


# === LAYOUT CONSTANTS ===
CANVAS_W = 820
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2

LEFT_X = PAD_X
RIGHT_X = PAD_X + COL_W + COL_GAP

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Column headers
HEADER_Y = TITLE_Y + TITLE_H + 30
HEADER_H = 65

# Rows
ROW_GAP = 15
ROW_H = 75
ROW_START_Y = HEADER_Y + HEADER_H + ROW_GAP

# Row data: (aspect, batch_text, streaming_text)
rows = [
    ("Latency", "Minutes to hours", "Milliseconds to seconds"),
    ("Complexity", "Simple to implement\nand maintain", "Complex infrastructure\nand monitoring"),
    ("Cost", "Lower cost,\npay per batch run", "Higher cost,\nalways-on resources"),
    ("Use Cases", "Reports, training ML\nmodels, analytics", "Real-time predictions,\nalerts, dashboards"),
    ("Availability", "Tolerates downtime\nbetween runs", "Requires high\navailability (HA)"),
]

# Calculate row heights dynamically
def row_height(text):
    lines = text.count("\n") + 1
    return max(ROW_H, math.ceil(lines * 22 * 1.25) + 30)

# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Batch vs. Streaming Ingestion", 32, color="#1e1e1e")

# Column headers
rect("h-batch", LEFT_X, HEADER_Y, COL_W, HEADER_H, BLUE[0], BLUE[1],
     bnd=[{"id": "ht-batch", "type": "text"}])
txt("ht-batch", LEFT_X, HEADER_Y, COL_W, HEADER_H,
    "Batch", 26, cid="h-batch")

rect("h-stream", RIGHT_X, HEADER_Y, COL_W, HEADER_H, RED[0], RED[1],
     bnd=[{"id": "ht-stream", "type": "text"}])
txt("ht-stream", RIGHT_X, HEADER_Y, COL_W, HEADER_H,
    "Streaming", 26, cid="h-stream")

# Rows
cur_y = ROW_START_Y
for i, (aspect, batch_txt, stream_txt) in enumerate(rows):
    rh = max(row_height(batch_txt), row_height(stream_txt))

    # Aspect label (centered between columns)
    aspect_h = math.ceil(1 * 20 * 1.25)
    txt(f"aspect-{i}", PAD_X, cur_y, CONTENT_W, aspect_h,
        aspect, 20, color=GRAY[0])

    card_y = cur_y + aspect_h + 8

    # Batch card
    rect(f"batch-{i}", LEFT_X, card_y, COL_W, rh, BLUE[0], BLUE[1], opacity=30,
         bnd=[{"id": f"bt-{i}", "type": "text"}])
    txt(f"bt-{i}", LEFT_X, card_y, COL_W, rh,
        batch_txt, 22, cid=f"batch-{i}")

    # Streaming card
    rect(f"stream-{i}", RIGHT_X, card_y, COL_W, rh, RED[0], RED[1], opacity=30,
         bnd=[{"id": f"st-{i}", "type": "text"}])
    txt(f"st-{i}", RIGHT_X, card_y, COL_W, rh,
        stream_txt, 22, cid=f"stream-{i}")

    cur_y = card_y + rh + ROW_GAP

# === WRITE FILE ===
outfile = os.path.join(OUT_DIR, "batch-vs-streaming.excalidraw")
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
