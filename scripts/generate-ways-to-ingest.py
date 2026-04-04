#!/usr/bin/env python3
"""Generate Excalidraw diagram: Ways to Ingest Data."""

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
seed = 3000


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


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({
        "type": "arrow",
        "id": id,
        "x": x,
        "y": y,
        "width": max(p[0] for p in pts) - min(p[0] for p in pts),
        "height": max(p[1] for p in pts) - min(p[1] for p in pts),
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
    })


# === LAYOUT ===
CANVAS_W = 800
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Central hub box
HUB_W = 220
HUB_H = 70
HUB_X = (CANVAS_W - HUB_W) // 2
HUB_Y = TITLE_Y + TITLE_H + 30

# Five method boxes radiating outward — 2 columns layout
# Left column: Connectors, Files
# Right column: APIs, Streaming
# Bottom center: Ingestion Tools
BOX_W = 240
BOX_H = 100
COL_GAP = 80
ARROW_GAP = 70

LEFT_X = PAD_X + 20
RIGHT_X = CANVAS_W - PAD_X - BOX_W - 20

ROW1_Y = HUB_Y + HUB_H + ARROW_GAP + 20
ROW2_Y = ROW1_Y + BOX_H + 30
CENTER_BOT_Y = ROW2_Y + BOX_H + 30
CENTER_X = (CANVAS_W - BOX_W) // 2

# === BUILD ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Ways to Ingest Data", 32, color="#1e1e1e")

# Central hub
rect("hub", HUB_X, HUB_Y, HUB_W, HUB_H, GRAY[0], GRAY[1],
     bnd=[{"id": "hub-t", "type": "text"}])
txt("hub-t", HUB_X, HUB_Y, HUB_W, HUB_H, "Data Ingestion", 24, cid="hub")

# Method boxes with title + subtitle (Rule 13)
methods = [
    # (id, x, y, title, subtitle, color)
    ("conn", LEFT_X, ROW1_Y, "Connectors", "JDBC / ODBC APIs\nTime or size-based", BLUE),
    ("api", RIGHT_X, ROW1_Y, "APIs", "Protocol-based\nRate limits & custom code", PURPLE),
    ("file", LEFT_X, ROW2_Y, "File Transfer", "Manual download\nSFTP / SCP", GREEN),
    ("stream", RIGHT_X, ROW2_Y, "Streaming", "Message Queues\nStreaming Platforms", RED),
    ("tool", CENTER_X, CENTER_BOT_Y, "Ingestion Tools", "Scheduled automated\ningestion (e.g. ETL)", YELLOW),
]

for mid, mx, my, title, subtitle, color in methods:
    title_sz = 24
    sub_sz = 17
    title_lines = title.count("\n") + 1
    sub_lines = subtitle.count("\n") + 1
    title_h = math.ceil(title_lines * title_sz * 1.25)
    sub_h = math.ceil(sub_lines * sub_sz * 1.25)
    gap = 6
    combined = title_h + gap + sub_h
    top_pad = (BOX_H - combined) // 2

    title_y = my + top_pad
    sub_y = title_y + title_h + gap

    rect(mid, mx, my, BOX_W, BOX_H, color[0], color[1],
         bnd=[{"id": f"{mid}-t", "type": "text"}])
    txt(f"{mid}-t", mx, title_y, BOX_W, title_h, title, title_sz, cid=mid)
    txt(f"{mid}-s", mx, sub_y, BOX_W, sub_h, subtitle, sub_sz, color=color[0])

# Arrows from hub to each method
hub_cx = HUB_X + HUB_W // 2
hub_bot = HUB_Y + HUB_H

for mid, mx, my, _, _, color in methods:
    box_cx = mx + BOX_W // 2
    box_top = my
    # Arrow from hub bottom to box top
    start_x = hub_cx
    start_y = hub_bot
    end_x = box_cx
    end_y = box_top
    dx = end_x - start_x
    dy = end_y - start_y
    arr(f"a-{mid}", start_x, start_y,
        [[0, 0], [dx, dy]],
        GRAY[0],
        sb={"elementId": "hub", "focus": 0, "gap": 4},
        eb={"elementId": mid, "focus": 0, "gap": 4})

# === WRITE ===
outfile = os.path.join(OUT_DIR, "ways-to-ingest.excalidraw")
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
