"""
Generate data warehouse architecture diagram showing ETL flow
from source systems through staging into the warehouse structure.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=1000)

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
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
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
    d.rect(bid, x, SOURCES_Y, SRC_W, BH, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", x, SOURCES_Y, SRC_W, BH, label, 22, cid=bid)

# Source label
SRC_LABEL_Y = SOURCES_Y + BH + 8
SRC_LABEL_H = math.ceil(1 * 17 * 1.25)
d.txt("src_label", PAD_X, SRC_LABEL_Y, CONTENT_W, SRC_LABEL_H,
    "Source Systems", 17, color=GRAY[0])

# === ARROWS: Sources to ETL ===
ETL_Y = SRC_LABEL_Y + SRC_LABEL_H + ARROW_GAP - 20
ETL_W = CONTENT_W
ETL_H = 65

# Center arrow from sources row to ETL
for i, (bid, _, _) in enumerate(sources):
    sx = PAD_X + i * (SRC_W + COL_GAP) + SRC_W // 2
    d.arr(f"a_src{i}", sx, SOURCES_Y + BH, [[0, 0], [0, ETL_Y - SOURCES_Y - BH]],
        GRAY[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "etl", "focus": 0, "gap": 4})

# === ROW 2: ETL Process ===
d.rect("etl", PAD_X, ETL_Y, ETL_W, ETL_H, *YELLOW,
     bnd=[{"id": "etl_t", "type": "text"}])
d.txt("etl_t", PAD_X, ETL_Y, ETL_W, ETL_H,
    "ETL / ELT Process", 24, cid="etl")

# === ARROW: ETL to Warehouse ===
WH_Y = ETL_Y + ETL_H + ARROW_GAP
d.arr("a_etl_wh", PAD_X + ETL_W // 2, ETL_Y + ETL_H,
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
d.rect("wh_container", PAD_X, WH_Y, CONTENT_W, WH_CONTAINER_H,
     BLUE[0], "#dbe4ff", dashed=True,
     bnd=[{"id": "a_etl_wh", "type": "arrow"}])

# Container label
WH_LABEL_Y = WH_Y + 12
WH_LABEL_H = math.ceil(1 * 22 * 1.25)
d.txt("wh_label", PAD_X, WH_LABEL_Y, CONTENT_W, WH_LABEL_H,
    "Data Warehouse", 22, color=BLUE[0])

# Staging area
d.rect("staging", PAD_X + WH_PAD, INNER_Y, INNER_W, INNER_H, *CYAN,
     bnd=[{"id": "staging_t", "type": "text"}])
d.txt("staging_t", PAD_X + WH_PAD, INNER_Y, INNER_W, INNER_H,
    "Staging Area", 20, cid="staging")

# Data marts
d.rect("mart", PAD_X + WH_PAD + INNER_W + COL_GAP, INNER_Y, INNER_W, INNER_H, *PURPLE,
     bnd=[{"id": "mart_t", "type": "text"}])
d.txt("mart_t", PAD_X + WH_PAD + INNER_W + COL_GAP, INNER_Y, INNER_W, INNER_H,
    "Data Marts", 20, cid="mart")

# Modeled tables row
MODEL_Y = INNER_Y + INNER_H + 15
MODEL_W = CONTENT_W - 2 * WH_PAD
d.rect("modeled", PAD_X + WH_PAD, MODEL_Y, MODEL_W, INNER_H, *GREEN,
     bnd=[{"id": "modeled_t", "type": "text"}])
d.txt("modeled_t", PAD_X + WH_PAD, MODEL_Y, MODEL_W, INNER_H,
    "Modeled Tables (Star/Snowflake Schema)", 20, cid="modeled")

# === ARROW: Warehouse to Consumers ===
CONSUMERS_Y = WH_Y + WH_CONTAINER_H + ARROW_GAP
d.arr("a_wh_cons", PAD_X + CONTENT_W // 2, WH_Y + WH_CONTAINER_H,
    [[0, 0], [0, CONSUMERS_Y - WH_Y - WH_CONTAINER_H]],
    BLUE[0],
    sb={"elementId": "wh_container", "focus": 0, "gap": 4},
    eb={"elementId": "consumers", "focus": 0, "gap": 4})

# === ROW 4: Consumers ===
CONS_W = CONTENT_W
CONS_H = 55
d.rect("consumers", PAD_X, CONSUMERS_Y, CONS_W, CONS_H, *GREEN,
     bnd=[{"id": "cons_t", "type": "text"}])
d.txt("cons_t", PAD_X, CONSUMERS_Y, CONS_W, CONS_H,
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
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
