"""Generate SCD Types diagram: Type 1 (Overwrite) vs Type 2 (Add Row)."""
import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GRAY, GREEN

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT ===
CW = 620
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X

# Title
TITLE_Y = 25
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Slowly Changing Dimensions", 32)

# --- TYPE 1 SECTION ---
T1_Y = 90
T1_H = 190
d.rect("t1_bg", PAD_X, T1_Y, CONTENT_W, T1_H, *BLUE, opacity=15, dashed=True)
d.txt("t1_title", PAD_X, T1_Y + 10, CONTENT_W, 30, "Type 1 — Overwrite", 24, color=BLUE[0])

# Before table
TBL_W = 220
TBL_X = PAD_X + 40
ROW_H = 32
BEFORE_Y = T1_Y + 50
d.rect("t1_hdr", TBL_X, BEFORE_Y, TBL_W, ROW_H, *BLUE, opacity=30)
d.txt("t1_hdr_t", TBL_X, BEFORE_Y, TBL_W, ROW_H, "key  |  name  |  city", 16, cid="t1_hdr")
d.rect("t1_row1", TBL_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, BLUE[0], "transparent")
d.txt("t1_row1_t", TBL_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, "101  |  Alice  |  NYC", 16, cid="t1_row1")

# Arrow in the middle
ARR_X = TBL_X + TBL_W + 30
ARR_Y = BEFORE_Y + ROW_H
d.txt("t1_change", ARR_X, ARR_Y - 8, 120, 30, "Alice moves\nto LA →", 15, color=BLUE[0])

# After table
AFTER_X = ARR_X + 130
d.rect("t1_hdr2", AFTER_X, BEFORE_Y, TBL_W, ROW_H, *BLUE, opacity=30)
d.txt("t1_hdr2_t", AFTER_X, BEFORE_Y, TBL_W, ROW_H, "key  |  name  |  city", 16, cid="t1_hdr2")
d.rect("t1_row2", AFTER_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, BLUE[0], "transparent")
d.txt("t1_row2_t", AFTER_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, "101  |  Alice  |  LA", 16, cid="t1_row2")

# Subtitle
d.txt("t1_sub", PAD_X, T1_Y + T1_H - 40, CONTENT_W, 25, "No history preserved — previous value is lost", 17, color=BLUE[0])

# --- ARROW BETWEEN SECTIONS ---
SEC_GAP = 70
d.arr("sec_arr", CW // 2, T1_Y + T1_H, [[0, 0], [0, SEC_GAP]], GRAY[0], dash=True)

# --- TYPE 2 SECTION ---
T2_Y = T1_Y + T1_H + SEC_GAP
T2_H = 220
d.rect("t2_bg", PAD_X, T2_Y, CONTENT_W, T2_H, *GREEN, opacity=15, dashed=True)
d.txt("t2_title", PAD_X, T2_Y + 10, CONTENT_W, 30, "Type 2 — Add New Row", 24, color=GREEN[0])

# Table with versioning columns
TBL2_W = CONTENT_W - 60
TBL2_X = PAD_X + 30
T2_TBL_Y = T2_Y + 50
d.rect("t2_hdr", TBL2_X, T2_TBL_Y, TBL2_W, ROW_H, *GREEN, opacity=30)
d.txt("t2_hdr_t", TBL2_X, T2_TBL_Y, TBL2_W, ROW_H, "key  |  name  |  city  |  effective  |  current", 15, cid="t2_hdr")

d.rect("t2_row1", TBL2_X, T2_TBL_Y + ROW_H, TBL2_W, ROW_H, GREEN[0], "transparent")
d.txt("t2_row1_t", TBL2_X, T2_TBL_Y + ROW_H, TBL2_W, ROW_H, "101  |  Alice  |  NYC  |  2024-01-01  |  false", 15, cid="t2_row1", op=60)

d.rect("t2_row2", TBL2_X, T2_TBL_Y + 2 * ROW_H, TBL2_W, ROW_H, GREEN[0], "transparent")
d.txt("t2_row2_t", TBL2_X, T2_TBL_Y + 2 * ROW_H, TBL2_W, ROW_H, "102  |  Alice  |  LA   |  2025-03-15  |  true", 15, cid="t2_row2")

# Subtitle
d.txt("t2_sub", PAD_X, T2_Y + T2_H - 40, CONTENT_W, 25, "Full history preserved — each version gets a new row", 17, color=GREEN[0])

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "scd-types"
d.save(f"diagrams/{name}.excalidraw")
print(f"Wrote diagrams/{name}.excalidraw")
