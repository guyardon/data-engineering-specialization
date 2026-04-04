"""Generate CDC Sync Methods comparison diagram for Course 2, Section 2.4.1."""

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
seed = 3000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
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
            "textAlign": "center",
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
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
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
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Keeping Storage Systems In Sync", TITLE_FSZ)

# --- Column 1: Full Snapshot ---
txt("col1-title", COL1_X, COL_TITLE_Y, COL_W, COL_TITLE_H, "Full Snapshot", 26, color=RED[0])

# Source DB
rect(
    "src1", COL1_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, *GRAY,
    bnd=[{"id": "src1-t", "type": "text"}],
)
txt("src1-t", COL1_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, "Source Database\n(All Rows)", 20, cid="src1")

# Arrow: full re-extract
arr(
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
txt("a1-lbl", COL1_X + BOX_OFF + BOX_W // 2 + 10, arr_label_y, 120, 25, "Delete + Reload", 17, color=RED[0])

# Target
rect(
    "tgt1", COL1_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, *RED,
    bnd=[{"id": "tgt1-t", "type": "text"}],
)
txt("tgt1-t", COL1_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, "Target Storage\n(Full Replace)", 20, cid="tgt1")

# Description box
rect("desc1", COL1_X + DESC_OFF, DESC_Y, DESC_W, DESC_H, *RED, opacity=40, dashed=True)
txt(
    "desc1-t", COL1_X + DESC_OFF, DESC_Y, DESC_W, DESC_H,
    "Simple but expensive\nRe-extracts every row\nBest for small datasets",
    18, cid="desc1",
)

# --- Column 2: CDC (Incremental) ---
txt("col2-title", COL2_X, COL_TITLE_Y, COL_W, COL_TITLE_H, "CDC (Incremental)", 26, color=GREEN[0])

# Source DB
rect(
    "src2", COL2_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, *GRAY,
    bnd=[{"id": "src2-t", "type": "text"}],
)
txt("src2-t", COL2_X + BOX_OFF, SRC_Y, BOX_W, BOX_H, "Source Database\n(Changes Only)", 20, cid="src2")

# Arrow: incremental
arr(
    "a2",
    COL2_X + BOX_OFF + BOX_W // 2,
    SRC_Y + BOX_H,
    [[0, 0], [0, ARR_GAP]],
    GREEN[0],
    sb={"elementId": "src2", "focus": 0, "gap": 4},
    eb={"elementId": "tgt2", "focus": 0, "gap": 4},
)
# Arrow label
txt("a2-lbl", COL2_X + BOX_OFF + BOX_W // 2 + 10, arr_label_y, 120, 25, "Insert / Update", 17, color=GREEN[0])

# Target
rect(
    "tgt2", COL2_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, *GREEN,
    bnd=[{"id": "tgt2-t", "type": "text"}],
)
txt("tgt2-t", COL2_X + BOX_OFF, TGT_Y, BOX_W, BOX_H, "Target Storage\n(Merge Changes)", 20, cid="tgt2")

# Description box
rect("desc2", COL2_X + DESC_OFF, DESC_Y, DESC_W, DESC_H, *GREEN, opacity=40, dashed=True)
txt(
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
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
