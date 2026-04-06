"""
Generate ETL vs ELT comparison diagram.

Two vertical columns side by side:
  Left:  ETL — Data Sources ↓ Staging Area (Transform) ↓ Target Destination
  Right: ELT — Data Sources ↓ Data Warehouse (Load) ↓ Transform ↓ Analytics
"""

import math
import sys

from diagramlib import BLUE, GRAY, GREEN, PURPLE, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT CONSTANTS ===

BW = 200  # box width
BH = 70  # box height
ARR_GAP = 80  # vertical gap between boxes (for arrows)
COL_GAP = 120  # horizontal gap between columns
PAD_X = 60  # left padding

# Column x positions
COL1_X = PAD_X
COL2_X = COL1_X + BW + COL_GAP

CANVAS_W = COL2_X + BW + PAD_X

# Vertical positions
TITLE_Y = 20
PILL_Y = 80
PILL_H = 50

ROW1_Y = PILL_Y + PILL_H + 30  # first box (Data Sources)
ROW2_Y = ROW1_Y + BH + ARR_GAP  # second box
ROW3_Y = ROW2_Y + BH + ARR_GAP  # third box
ROW4_Y = ROW3_Y + BH + ARR_GAP  # fourth box (ELT only)

# Center of each column for arrows
COL1_CX = COL1_X + BW // 2
COL2_CX = COL2_X + BW // 2

# === BUILD DIAGRAM ===

# Title
d.txt("title", 0, TITLE_Y, CANVAS_W, 40, "ETL vs. ELT", 32)

# --- ETL COLUMN (left) ---

# ETL pill
d.rect(
    "etl_pill",
    COL1_X + (BW - 100) // 2,
    PILL_Y,
    100,
    PILL_H,
    *BLUE,
    bnd=[{"id": "etl_pill_t", "type": "text"}],
)
d.txt(
    "etl_pill_t",
    COL1_X + (BW - 100) // 2,
    PILL_Y,
    100,
    PILL_H,
    "ETL",
    26,
    cid="etl_pill",
)

# Data Sources
d.rect("etl_ds", COL1_X, ROW1_Y, BW, BH, *GRAY, bnd=[{"id": "etl_ds_t", "type": "text"}])
d.txt("etl_ds_t", COL1_X, ROW1_Y, BW, BH, "Data Sources", 22, cid="etl_ds")

# Arrow down + label
d.arr(
    "etl_a1",
    COL1_CX,
    ROW1_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    GRAY[0],
    sb={"elementId": "etl_ds", "focus": 0, "gap": 4},
    eb={"elementId": "etl_stage", "focus": 0, "gap": 4},
)
d.txt(
    "etl_lab1",
    COL1_CX + 10,
    ROW1_Y + BH + ARR_GAP // 2 - 12,
    80,
    24,
    "raw data",
    17,
    op=70,
)

# Staging Area (Transform)
d.rect(
    "etl_stage",
    COL1_X,
    ROW2_Y,
    BW,
    BH,
    *PURPLE,
    dashed=True,
    bnd=[{"id": "etl_stage_t", "type": "text"}],
)
d.txt(
    "etl_stage_t",
    COL1_X,
    ROW2_Y,
    BW,
    BH,
    "Staging Area\n(Transform)",
    20,
    cid="etl_stage",
)

# Arrow down + label
d.arr(
    "etl_a2",
    COL1_CX,
    ROW2_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    PURPLE[0],
    sb={"elementId": "etl_stage", "focus": 0, "gap": 4},
    eb={"elementId": "etl_tgt", "focus": 0, "gap": 4},
)
d.txt(
    "etl_lab2",
    COL1_CX + 10,
    ROW2_Y + BH + ARR_GAP // 2 - 12,
    100,
    24,
    "transformed\ndata",
    17,
    op=70,
)

# Target Destination
d.rect(
    "etl_tgt", COL1_X, ROW3_Y, BW, BH, *GREEN, bnd=[{"id": "etl_tgt_t", "type": "text"}]
)
d.txt("etl_tgt_t", COL1_X, ROW3_Y, BW, BH, "Target\nDestination", 22, cid="etl_tgt")

# Step labels to the left of ETL boxes
d.txt("etl_s1", COL1_X - 5, ROW1_Y + BH + 4, BW, 20, "Extract", 18, op=60)
d.txt("etl_s2", COL1_X - 5, ROW2_Y + BH + 4, BW, 20, "Transform", 18, op=60)
d.txt("etl_s3", COL1_X - 5, ROW3_Y - 22, BW, 20, "Load", 18, op=60)

# --- ELT COLUMN (right) ---

# ELT pill
d.rect(
    "elt_pill",
    COL2_X + (BW - 100) // 2,
    PILL_Y,
    100,
    PILL_H,
    *GREEN,
    bnd=[{"id": "elt_pill_t", "type": "text"}],
)
d.txt(
    "elt_pill_t",
    COL2_X + (BW - 100) // 2,
    PILL_Y,
    100,
    PILL_H,
    "ELT",
    26,
    cid="elt_pill",
)

# Data Sources
d.rect("elt_ds", COL2_X, ROW1_Y, BW, BH, *GRAY, bnd=[{"id": "elt_ds_t", "type": "text"}])
d.txt("elt_ds_t", COL2_X, ROW1_Y, BW, BH, "Data Sources", 22, cid="elt_ds")

# Arrow down + label
d.arr(
    "elt_a1",
    COL2_CX,
    ROW1_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    GRAY[0],
    sb={"elementId": "elt_ds", "focus": 0, "gap": 4},
    eb={"elementId": "elt_wh", "focus": 0, "gap": 4},
)
d.txt(
    "elt_lab1",
    COL2_CX + 10,
    ROW1_Y + BH + ARR_GAP // 2 - 12,
    80,
    24,
    "raw data",
    17,
    op=70,
)

# Data Warehouse (Load)
d.rect("elt_wh", COL2_X, ROW2_Y, BW, BH, *BLUE, bnd=[{"id": "elt_wh_t", "type": "text"}])
d.txt("elt_wh_t", COL2_X, ROW2_Y, BW, BH, "Data\nWarehouse", 22, cid="elt_wh")

# Arrow down + label
d.arr(
    "elt_a2",
    COL2_CX,
    ROW2_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    BLUE[0],
    sb={"elementId": "elt_wh", "focus": 0, "gap": 4},
    eb={"elementId": "elt_xform", "focus": 0, "gap": 4},
)
d.txt(
    "elt_lab2",
    COL2_CX + 10,
    ROW2_Y + BH + ARR_GAP // 2 - 12,
    80,
    24,
    "raw data",
    17,
    op=70,
)

# Transform (in Warehouse)
d.rect(
    "elt_xform",
    COL2_X,
    ROW3_Y,
    BW,
    BH,
    *PURPLE,
    dashed=True,
    bnd=[{"id": "elt_xform_t", "type": "text"}],
)
d.txt(
    "elt_xform_t",
    COL2_X,
    ROW3_Y,
    BW,
    BH,
    "Transform\n(in Warehouse)",
    20,
    cid="elt_xform",
)

# Arrow down + label
d.arr(
    "elt_a3",
    COL2_CX,
    ROW3_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    PURPLE[0],
    sb={"elementId": "elt_xform", "focus": 0, "gap": 4},
    eb={"elementId": "elt_out", "focus": 0, "gap": 4},
)
d.txt(
    "elt_lab3",
    COL2_CX + 10,
    ROW3_Y + BH + ARR_GAP // 2 - 12,
    80,
    24,
    "query\ndata",
    17,
    op=70,
)

# Analytics / Reports
d.rect(
    "elt_out", COL2_X, ROW4_Y, BW, BH, *GREEN, bnd=[{"id": "elt_out_t", "type": "text"}]
)
d.txt("elt_out_t", COL2_X, ROW4_Y, BW, BH, "Analytics /\nReports", 22, cid="elt_out")

# Step labels
d.txt("elt_s1", COL2_X - 5, ROW1_Y + BH + 4, BW, 20, "Extract", 18, op=60)
d.txt("elt_s2", COL2_X - 5, ROW2_Y - 22, BW, 20, "Load", 18, op=60)
d.txt("elt_s3", COL2_X - 5, ROW3_Y - 22, BW, 20, "Transform", 18, op=60)

# Vertical divider between columns
DIV_X = COL1_X + BW + COL_GAP // 2
d.rect(
    "divider",
    DIV_X,
    PILL_Y,
    2,
    ROW4_Y + BH - PILL_Y,
    GRAY[0],
    "transparent",
    opacity=15,
)

# === VERIFY ===

print(f"Column 1 (ETL): x={COL1_X} to {COL1_X + BW}")
print(f"Column 2 (ELT): x={COL2_X} to {COL2_X + BW}")
print(f"Canvas width: {CANVAS_W}")
print(f"Vertical extent: {TITLE_Y} to {ROW4_Y + BH}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "etl-vs-elt"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
