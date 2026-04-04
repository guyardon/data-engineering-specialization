"""
Generate data warehouse architecture diagram showing ETL flow
from source systems through staging into the warehouse structure.
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


# === LAYOUT CONSTANTS ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620

BW = 180  # source box width
BH = 55   # source box height
ARROW_GAP = 70
COL_GAP = 20

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Data Warehouse Architecture", 32, color="#1e1e1e")

# === ROW 1: Source Systems ===
SOURCES_Y = TITLE_Y + TITLE_H + 30
SRC_W = (CONTENT_W - 2 * COL_GAP) // 3  # ~193

sources = [
    ("src1", "CRM", GRAY),
    ("src2", "ERP", GRAY),
    ("src3", "Flat Files", GRAY),
]

for i, (bid, label, color) in enumerate(sources):
    x = PAD_X + i * (SRC_W + COL_GAP)
    rect(bid, x, SOURCES_Y, SRC_W, BH, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", x, SOURCES_Y, SRC_W, BH, label, 22, cid=bid)

# Source label
SRC_LABEL_Y = SOURCES_Y + BH + 8
SRC_LABEL_H = math.ceil(1 * 17 * 1.25)
txt("src_label", PAD_X, SRC_LABEL_Y, CONTENT_W, SRC_LABEL_H,
    "Source Systems", 17, color=GRAY[0])

# === ARROWS: Sources to ETL ===
ETL_Y = SRC_LABEL_Y + SRC_LABEL_H + ARROW_GAP - 20
ETL_W = CONTENT_W
ETL_H = 65

# Center arrow from sources row to ETL
for i, (bid, _, _) in enumerate(sources):
    sx = PAD_X + i * (SRC_W + COL_GAP) + SRC_W // 2
    arr(f"a_src{i}", sx, SOURCES_Y + BH, [[0, 0], [0, ETL_Y - SOURCES_Y - BH]],
        GRAY[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "etl", "focus": 0, "gap": 4})

# === ROW 2: ETL Process ===
rect("etl", PAD_X, ETL_Y, ETL_W, ETL_H, *YELLOW,
     bnd=[{"id": "etl_t", "type": "text"}])
txt("etl_t", PAD_X, ETL_Y, ETL_W, ETL_H,
    "ETL / ELT Process", 24, cid="etl")

# === ARROW: ETL to Warehouse ===
WH_Y = ETL_Y + ETL_H + ARROW_GAP
arr("a_etl_wh", PAD_X + ETL_W // 2, ETL_Y + ETL_H,
    [[0, 0], [0, WH_Y - ETL_Y - ETL_H]],
    YELLOW[0],
    sb={"elementId": "etl", "focus": 0, "gap": 4},
    eb={"elementId": "wh_container", "focus": 0, "gap": 4})

# === ROW 3: Data Warehouse Container ===
WH_PAD = 20
INNER_W = (CONTENT_W - 2 * WH_PAD - COL_GAP) // 2
INNER_H = 55
INNER_Y = WH_Y + WH_PAD + 35  # space for container label

# Container
WH_CONTAINER_H = WH_PAD + 35 + INNER_H + 15 + INNER_H + WH_PAD + 25
rect("wh_container", PAD_X, WH_Y, CONTENT_W, WH_CONTAINER_H,
     BLUE[0], "#dbe4ff", dashed=True,
     bnd=[{"id": "a_etl_wh", "type": "arrow"}])

# Container label
WH_LABEL_Y = WH_Y + 12
WH_LABEL_H = math.ceil(1 * 22 * 1.25)
txt("wh_label", PAD_X, WH_LABEL_Y, CONTENT_W, WH_LABEL_H,
    "Data Warehouse", 22, color=BLUE[0])

# Staging area
rect("staging", PAD_X + WH_PAD, INNER_Y, INNER_W, INNER_H, *CYAN,
     bnd=[{"id": "staging_t", "type": "text"}])
txt("staging_t", PAD_X + WH_PAD, INNER_Y, INNER_W, INNER_H,
    "Staging Area", 20, cid="staging")

# Data marts
rect("mart", PAD_X + WH_PAD + INNER_W + COL_GAP, INNER_Y, INNER_W, INNER_H, *PURPLE,
     bnd=[{"id": "mart_t", "type": "text"}])
txt("mart_t", PAD_X + WH_PAD + INNER_W + COL_GAP, INNER_Y, INNER_W, INNER_H,
    "Data Marts", 20, cid="mart")

# Modeled tables row
MODEL_Y = INNER_Y + INNER_H + 15
MODEL_W = CONTENT_W - 2 * WH_PAD
rect("modeled", PAD_X + WH_PAD, MODEL_Y, MODEL_W, INNER_H, *GREEN,
     bnd=[{"id": "modeled_t", "type": "text"}])
txt("modeled_t", PAD_X + WH_PAD, MODEL_Y, MODEL_W, INNER_H,
    "Modeled Tables (Star/Snowflake Schema)", 20, cid="modeled")

# === ARROW: Warehouse to Consumers ===
CONSUMERS_Y = WH_Y + WH_CONTAINER_H + ARROW_GAP
arr("a_wh_cons", PAD_X + CONTENT_W // 2, WH_Y + WH_CONTAINER_H,
    [[0, 0], [0, CONSUMERS_Y - WH_Y - WH_CONTAINER_H]],
    BLUE[0],
    sb={"elementId": "wh_container", "focus": 0, "gap": 4},
    eb={"elementId": "consumers", "focus": 0, "gap": 4})

# === ROW 4: Consumers ===
CONS_W = CONTENT_W
CONS_H = 55
rect("consumers", PAD_X, CONSUMERS_Y, CONS_W, CONS_H, *GREEN,
     bnd=[{"id": "cons_t", "type": "text"}])
txt("cons_t", PAD_X, CONSUMERS_Y, CONS_W, CONS_H,
    "BI Tools  /  Analysts  /  Reports", 22, cid="consumers")

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{CONSUMERS_Y + CONS_H + 20}")
print(f"Title: y={TITLE_Y}")
print(f"Sources: y={SOURCES_Y} to {SOURCES_Y + BH}")
print(f"ETL: y={ETL_Y} to {ETL_Y + ETL_H}")
print(f"Warehouse: y={WH_Y} to {WH_Y + WH_CONTAINER_H}")
print(f"Consumers: y={CONSUMERS_Y} to {CONSUMERS_Y + CONS_H}")

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "warehouse-architecture"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
