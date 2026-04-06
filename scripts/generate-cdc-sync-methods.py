"""Generate CDC Sync Methods comparison diagram for Course 2, Section 2.4.1."""

import math
import sys

from diagramlib import ExcalidrawDiagram, RED, GREEN, GRAY

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT CONSTANTS ===
# Two columns: Full Snapshot vs CDC (Incremental)
# Each column: Source DB → arrow → Target, with description below

CANVAS_W = 800
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 740
COL_GAP = 50
COL_W = (CONTENT_W - COL_GAP) // 2  # 345

COL1_X = PAD_X
COL2_X = PAD_X + COL_W + COL_GAP

# Box sizing
BOX_W = 260
BOX_H = 70
DESC_H = 95

# Title + subtitle sizing (Rule 13)
HDR_FSZ = 24
SUB_FSZ = 18
title_h = math.ceil(1 * HDR_FSZ * 1.25)
sub_h = math.ceil(1 * SUB_FSZ * 1.25)
gap_ts = 4
combined_h = title_h + gap_ts + sub_h
top_pad = (BOX_H - combined_h) // 2

# Vertical positions
TITLE_Y = 15
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)

COL_TITLE_Y = TITLE_Y + TITLE_H + 30
COL_TITLE_H = math.ceil(1 * 26 * 1.25)

SRC_Y = COL_TITLE_Y + COL_TITLE_H + 25
ARR_GAP = 80
TGT_Y = SRC_Y + BOX_H + ARR_GAP
DESC_Y = TGT_Y + BOX_H + 25

# Center boxes within columns
BOX_OFF = (COL_W - BOX_W) // 2
DESC_W = COL_W - 20
DESC_OFF = 10

# === BUILD DIAGRAM ===

# Main title
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Keeping Storage Systems In Sync", TITLE_FSZ)

# --- Column 1: Full Snapshot ---
d.txt("col1-title", COL1_X, COL_TITLE_Y, COL_W, COL_TITLE_H, "Full Snapshot", 26, color=RED[0])

# Source DB
d.rect(
    "src1", COL1_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, *GRAY,
    bnd=[{"id": "src1-t", "type": "text"}],
)
d.txt("src1-t", COL1_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, "Source Database\n(All Rows)", 20, cid="src1")

# Arrow: full re-extract
d.arr(
    "a1",
    COL1_X + BOX_OFF + BOX_W // 2,
    SRC_Y + BOX_H,
    [[0, 0], [0, ARR_GAP]],
    RED[0],
    sb={"elementId": "src1", "focus": 0, "gap": 4},
    eb={"elementId": "tgt1", "focus": 0, "gap": 4},
)
# Arrow label
arr_label_y = SRC_Y + BOX_H + ARR_GAP // 2 - 12
d.txt("a1-lbl", COL1_X + BOX_OFF + BOX_W // 2 + 10, arr_label_y, 120, 25, "Delete + Reload", 17, color=RED[0])

# Target
d.rect(
    "tgt1", COL1_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, *RED,
    bnd=[{"id": "tgt1-t", "type": "text"}],
)
d.txt("tgt1-t", COL1_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, "Target Storage\n(Full Replace)", 20, cid="tgt1")

# Description box
d.rect("desc1", COL1_X + DESC_OFF, DESC_Y, DESC_W, DESC_H, *RED, opacity=40, dashed=True)
d.txt(
    "desc1-t", COL1_X + DESC_OFF, DESC_Y, DESC_W, DESC_H,
    "Simple but expensive\nRe-extracts every row\nBest for small datasets",
    18, cid="desc1",
)

# --- Column 2: CDC (Incremental) ---
d.txt("col2-title", COL2_X, COL_TITLE_Y, COL_W, COL_TITLE_H, "CDC (Incremental)", 26, color=GREEN[0])

# Source DB
d.rect(
    "src2", COL2_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, *GRAY,
    bnd=[{"id": "src2-t", "type": "text"}],
)
d.txt("src2-t", COL2_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, "Source Database\n(Changes Only)", 20, cid="src2")

# Arrow: incremental
d.arr(
    "a2",
    COL2_X + BOX_OFF + BOX_W // 2,
    SRC_Y + BOX_H,
    [[0, 0], [0, ARR_GAP]],
    GREEN[0],
    sb={"elementId": "src2", "focus": 0, "gap": 4},
    eb={"elementId": "tgt2", "focus": 0, "gap": 4},
)
# Arrow label
d.txt("a2-lbl", COL2_X + BOX_OFF + BOX_W // 2 + 10, arr_label_y, 120, 25, "Insert / Update", 17, color=GREEN[0])

# Target
d.rect(
    "tgt2", COL2_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, *GREEN,
    bnd=[{"id": "tgt2-t", "type": "text"}],
)
d.txt("tgt2-t", COL2_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, "Target Storage\n(Merge Changes)", 20, cid="tgt2")

# Description box
d.rect("desc2", COL2_X + DESC_OFF, DESC_Y, DESC_W, DESC_H, *GREEN, opacity=40, dashed=True)
d.txt(
    "desc2-t", COL2_X + DESC_OFF, DESC_Y, DESC_W, DESC_H,
    "Efficient at scale\nCaptures inserts, updates, deletes\nReal-time or near-real-time",
    18, cid="desc2",
)

# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"Columns: col1_x={COL1_X}, col2_x={COL2_X}, col_w={COL_W}")
print(f"Boxes: w={BOX_W}, h={BOX_H}, offset={BOX_OFF}")
print(f"Rows: src={SRC_Y}, tgt={TGT_Y}, desc={DESC_Y}")
print(f"Bottom: {DESC_Y + DESC_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/cdc-sync-methods"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
