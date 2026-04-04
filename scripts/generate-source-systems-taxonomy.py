"""Generate Source Systems Taxonomy diagram for Course 2, Section 1.1.1."""

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
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True, "containerId": cid,
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

CANVAS_W = 820
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 780

COL_GAP = 30
COL_W = (CONTENT_W - 2 * COL_GAP) // 3  # 240

COL1_X = PAD_X
COL2_X = COL1_X + COL_W + COL_GAP
COL3_X = COL2_X + COL_W + COL_GAP

# Title
TITLE_Y = 15
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)  # 40

# Header boxes (Rule 13: title + subtitle)
HDR_Y = TITLE_Y + TITLE_H + 30
HDR_H = 95
HDR_TITLE_FSZ = 24
HDR_SUB_FSZ = 17

title_h = math.ceil(1 * HDR_TITLE_FSZ * 1.25)  # 30
sub_h = math.ceil(1 * HDR_SUB_FSZ * 1.25)  # 22
gap_ts = 6
combined_h = title_h + gap_ts + sub_h
top_pad = (HDR_H - combined_h) // 2

HDR_TITLE_Y = HDR_Y + top_pad
HDR_SUB_Y = HDR_TITLE_Y + title_h + gap_ts

# Pills (sub-items below each header)
ARR_GAP = 70
PILL_H = 60
PILL_GAP = 20
PILL_INSET = 10
PILL_W = COL_W - 2 * PILL_INSET

PILL_Y1 = HDR_Y + HDR_H + ARR_GAP  # 215
PILL_Y2 = PILL_Y1 + PILL_H + PILL_GAP  # 280
PILL_Y3 = PILL_Y2 + PILL_H + PILL_GAP  # 345


# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Source Systems", TITLE_FSZ)

# --- Column 1: Databases (BLUE) ---
rect("db-hdr", COL1_X, HDR_Y, COL_W, HDR_H, *BLUE,
     bnd=[{"id": "db-title", "type": "text"}])
txt("db-title", COL1_X, HDR_TITLE_Y, COL_W, title_h,
    "Databases", HDR_TITLE_FSZ, cid="db-hdr")
txt("db-sub", COL1_X, HDR_SUB_Y, COL_W, sub_h,
    "CRUD via DBMS", HDR_SUB_FSZ, color=BLUE[0])

pill1_x = COL1_X + PILL_INSET
rect("db-rel", pill1_x, PILL_Y1, PILL_W, PILL_H, *BLUE,
     bnd=[{"id": "db-rel-t", "type": "text"}])
txt("db-rel-t", pill1_x, PILL_Y1, PILL_W, PILL_H,
    "Relational (SQL)", 22, cid="db-rel")

rect("db-nosql", pill1_x, PILL_Y2, PILL_W, PILL_H, *BLUE,
     bnd=[{"id": "db-nosql-t", "type": "text"}])
txt("db-nosql-t", pill1_x, PILL_Y2, PILL_W, PILL_H,
    "NoSQL", 22, cid="db-nosql")

# Arrows from header to pills
arr("a-db1", COL1_X + COL_W // 2, HDR_Y + HDR_H,
    [[0, 0], [0, ARR_GAP]], BLUE[0],
    sb={"elementId": "db-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "db-rel", "focus": 0, "gap": 4})

arr("a-db2", COL1_X + COL_W // 2, PILL_Y1 + PILL_H,
    [[0, 0], [0, PILL_GAP]], BLUE[0],
    sb={"elementId": "db-rel", "focus": 0, "gap": 4},
    eb={"elementId": "db-nosql", "focus": 0, "gap": 4})

# --- Column 2: Files (GREEN) ---
rect("files-hdr", COL2_X, HDR_Y, COL_W, HDR_H, *GREEN,
     bnd=[{"id": "files-title", "type": "text"}])
txt("files-title", COL2_X, HDR_TITLE_Y, COL_W, title_h,
    "Files", HDR_TITLE_FSZ, cid="files-hdr")
txt("files-sub", COL2_X, HDR_SUB_Y, COL_W, sub_h,
    "Various formats", HDR_SUB_FSZ, color=GREEN[0])

pill2_x = COL2_X + PILL_INSET
rect("f-struct", pill2_x, PILL_Y1, PILL_W, PILL_H, *GREEN,
     bnd=[{"id": "f-struct-t", "type": "text"}])
txt("f-struct-t", pill2_x, PILL_Y1, PILL_W, PILL_H,
    "Structured", 22, cid="f-struct")

rect("f-semi", pill2_x, PILL_Y2, PILL_W, PILL_H, *GREEN,
     bnd=[{"id": "f-semi-t", "type": "text"}])
txt("f-semi-t", pill2_x, PILL_Y2, PILL_W, PILL_H,
    "Semi-structured", 22, cid="f-semi")

rect("f-unstruct", pill2_x, PILL_Y3, PILL_W, PILL_H, *GREEN,
     bnd=[{"id": "f-unstruct-t", "type": "text"}])
txt("f-unstruct-t", pill2_x, PILL_Y3, PILL_W, PILL_H,
    "Unstructured", 22, cid="f-unstruct")

arr("a-f1", COL2_X + COL_W // 2, HDR_Y + HDR_H,
    [[0, 0], [0, ARR_GAP]], GREEN[0],
    sb={"elementId": "files-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "f-struct", "focus": 0, "gap": 4})

arr("a-f2", COL2_X + COL_W // 2, PILL_Y1 + PILL_H,
    [[0, 0], [0, PILL_GAP]], GREEN[0],
    sb={"elementId": "f-struct", "focus": 0, "gap": 4},
    eb={"elementId": "f-semi", "focus": 0, "gap": 4})

arr("a-f3", COL2_X + COL_W // 2, PILL_Y2 + PILL_H,
    [[0, 0], [0, PILL_GAP]], GREEN[0],
    sb={"elementId": "f-semi", "focus": 0, "gap": 4},
    eb={"elementId": "f-unstruct", "focus": 0, "gap": 4})

# --- Column 3: Streaming (PURPLE) ---
rect("stream-hdr", COL3_X, HDR_Y, COL_W, HDR_H, *PURPLE,
     bnd=[{"id": "stream-title", "type": "text"}])
txt("stream-title", COL3_X, HDR_TITLE_Y, COL_W, title_h,
    "Streaming", HDR_TITLE_FSZ, cid="stream-hdr")
txt("stream-sub", COL3_X, HDR_SUB_Y, COL_W, sub_h,
    "Real-time data flow", HDR_SUB_FSZ, color=PURPLE[0])

pill3_x = COL3_X + PILL_INSET
rect("s-mq", pill3_x, PILL_Y1, PILL_W, PILL_H, *PURPLE,
     bnd=[{"id": "s-mq-t", "type": "text"}])
txt("s-mq-t", pill3_x, PILL_Y1, PILL_W, PILL_H,
    "Message Queues", 22, cid="s-mq")

rect("s-plat", pill3_x, PILL_Y2, PILL_W, PILL_H, *PURPLE,
     bnd=[{"id": "s-plat-t", "type": "text"}])
txt("s-plat-t", pill3_x, PILL_Y2, PILL_W, PILL_H,
    "Streaming Platforms", 22, cid="s-plat")

arr("a-s1", COL3_X + COL_W // 2, HDR_Y + HDR_H,
    [[0, 0], [0, ARR_GAP]], PURPLE[0],
    sb={"elementId": "stream-hdr", "focus": 0, "gap": 4},
    eb={"elementId": "s-mq", "focus": 0, "gap": 4})

arr("a-s2", COL3_X + COL_W // 2, PILL_Y1 + PILL_H,
    [[0, 0], [0, PILL_GAP]], PURPLE[0],
    sb={"elementId": "s-mq", "focus": 0, "gap": 4},
    eb={"elementId": "s-plat", "focus": 0, "gap": 4})


# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"Cols at x={COL1_X}, {COL2_X}, {COL3_X}, width={COL_W}")
print(f"Headers: y={HDR_Y}, h={HDR_H}")
print(f"Pills: y1={PILL_Y1}, y2={PILL_Y2}, y3={PILL_Y3}, h={PILL_H}")
print(f"Bottom of tallest col (files): {PILL_Y3 + PILL_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/source-systems-taxonomy"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
