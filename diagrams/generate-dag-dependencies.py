"""
DAG dependency patterns diagram.
Shows 4 common dependency patterns side by side in a 2x2 grid:
  1. Linear chain
  2. Fan-out (parallel)
  3. Fan-in (converge)
  4. Complex (chain utility)

Canvas: ~680px wide, vertical layout with labeled sections.
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
seed = 2000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
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
CANVAS_W = 680
PAD_X = 20
BW = 90       # small task box
BH = 45
ARROW_GAP = 50  # horizontal gap between boxes
COL_W = CANVAS_W // 2 - PAD_X  # each pattern column width
COL1_X = PAD_X
COL2_X = CANVAS_W // 2 + 10

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CANVAS_W - 2 * PAD_X, 40,
    "DAG Dependency Patterns", 32)
txt("sub", PAD_X, TITLE_Y + 38, CANVAS_W - 2 * PAD_X, 25,
    "Common ways to wire task dependencies in Airflow", 17, color=BLUE[0])

# === PATTERN 1: Linear Chain (top-left) ===
P1_Y = 100
txt("p1_title", COL1_X, P1_Y, COL_W, 25, "Linear Chain", 22, color=BLUE[0])
# Code label
txt("p1_code", COL1_X, P1_Y + 28, COL_W, 20,
    "task1 >> task2 >> task3", 14, color=GRAY[0])

# Three boxes in a row
P1_BOX_Y = P1_Y + 60
P1_B1_X = COL1_X + 10
P1_B2_X = P1_B1_X + BW + ARROW_GAP
P1_B3_X = P1_B2_X + BW + ARROW_GAP

rect("p1_b1", P1_B1_X, P1_BOX_Y, BW, BH, *BLUE,
     bnd=[{"id": "p1_t1", "type": "text"}])
txt("p1_t1", P1_B1_X, P1_BOX_Y, BW, BH, "task1", 18, cid="p1_b1")

rect("p1_b2", P1_B2_X, P1_BOX_Y, BW, BH, *BLUE,
     bnd=[{"id": "p1_t2", "type": "text"}])
txt("p1_t2", P1_B2_X, P1_BOX_Y, BW, BH, "task2", 18, cid="p1_b2")

rect("p1_b3", P1_B3_X, P1_BOX_Y, BW, BH, *BLUE,
     bnd=[{"id": "p1_t3", "type": "text"}])
txt("p1_t3", P1_B3_X, P1_BOX_Y, BW, BH, "task3", 18, cid="p1_b3")

arr("p1_a1", P1_B1_X + BW, P1_BOX_Y + BH // 2, [[0, 0], [ARROW_GAP, 0]], BLUE[0],
    sb={"elementId": "p1_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p1_b2", "focus": 0, "gap": 4})
arr("p1_a2", P1_B2_X + BW, P1_BOX_Y + BH // 2, [[0, 0], [ARROW_GAP, 0]], BLUE[0],
    sb={"elementId": "p1_b2", "focus": 0, "gap": 4},
    eb={"elementId": "p1_b3", "focus": 0, "gap": 4})


# === PATTERN 2: Fan-Out (top-right) ===
P2_Y = 100
txt("p2_title", COL2_X, P2_Y, COL_W, 25, "Fan-Out (Parallel)", 22, color=GREEN[0])
txt("p2_code", COL2_X, P2_Y + 28, COL_W, 20,
    "task1 >> [task2, task3]", 14, color=GRAY[0])

P2_BOX_Y = P2_Y + 60
P2_B1_X = COL2_X + 10
P2_B2_X = P2_B1_X + BW + ARROW_GAP + 20
P2_B2_Y_TOP = P2_BOX_Y - 5
P2_B3_Y_BOT = P2_BOX_Y + BH + 15

rect("p2_b1", P2_B1_X, P2_BOX_Y, BW, BH, *GREEN,
     bnd=[{"id": "p2_t1", "type": "text"}])
txt("p2_t1", P2_B1_X, P2_BOX_Y, BW, BH, "task1", 18, cid="p2_b1")

rect("p2_b2", P2_B2_X, P2_B2_Y_TOP, BW, BH, *GREEN,
     bnd=[{"id": "p2_t2", "type": "text"}])
txt("p2_t2", P2_B2_X, P2_B2_Y_TOP, BW, BH, "task2", 18, cid="p2_b2")

rect("p2_b3", P2_B2_X, P2_B3_Y_BOT, BW, BH, *GREEN,
     bnd=[{"id": "p2_t3", "type": "text"}])
txt("p2_t3", P2_B2_X, P2_B3_Y_BOT, BW, BH, "task3", 18, cid="p2_b3")

# Arrow to top
arr("p2_a1", P2_B1_X + BW, P2_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP + 20, -(P2_BOX_Y - P2_B2_Y_TOP) + BH // 2 - BH // 2]], GREEN[0],
    sb={"elementId": "p2_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p2_b2", "focus": 0, "gap": 4})
# Arrow to bottom
arr("p2_a2", P2_B1_X + BW, P2_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P2_B3_Y_BOT - P2_BOX_Y]], GREEN[0],
    sb={"elementId": "p2_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p2_b3", "focus": 0, "gap": 4})


# === PATTERN 3: Fan-In (bottom-left) ===
P3_Y = 280
txt("p3_title", COL1_X, P3_Y, COL_W, 25, "Fan-In (Converge)", 22, color=PURPLE[0])
txt("p3_code", COL1_X, P3_Y + 28, COL_W, 20,
    "[task1, task2] >> task3", 14, color=GRAY[0])

P3_BOX_Y = P3_Y + 60
P3_B1_Y_TOP = P3_BOX_Y - 5
P3_B2_Y_BOT = P3_BOX_Y + BH + 15
P3_B1_X = COL1_X + 10
P3_B3_X = P3_B1_X + BW + ARROW_GAP + 20

rect("p3_b1", P3_B1_X, P3_B1_Y_TOP, BW, BH, *PURPLE,
     bnd=[{"id": "p3_t1", "type": "text"}])
txt("p3_t1", P3_B1_X, P3_B1_Y_TOP, BW, BH, "task1", 18, cid="p3_b1")

rect("p3_b2", P3_B1_X, P3_B2_Y_BOT, BW, BH, *PURPLE,
     bnd=[{"id": "p3_t2", "type": "text"}])
txt("p3_t2", P3_B1_X, P3_B2_Y_BOT, BW, BH, "task2", 18, cid="p3_b2")

rect("p3_b3", P3_B3_X, P3_BOX_Y + BH // 2, BW, BH, *PURPLE,
     bnd=[{"id": "p3_t3", "type": "text"}])
txt("p3_t3", P3_B3_X, P3_BOX_Y + BH // 2, BW, BH, "task3", 18, cid="p3_b3")

# Arrow from top
arr("p3_a1", P3_B1_X + BW, P3_B1_Y_TOP + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P3_BOX_Y + BH // 2 + BH // 2 - P3_B1_Y_TOP - BH // 2]], PURPLE[0],
    sb={"elementId": "p3_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p3_b3", "focus": 0, "gap": 4})
# Arrow from bottom
arr("p3_a2", P3_B1_X + BW, P3_B2_Y_BOT + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P3_BOX_Y + BH // 2 + BH // 2 - P3_B2_Y_BOT - BH // 2]], PURPLE[0],
    sb={"elementId": "p3_b2", "focus": 0, "gap": 4},
    eb={"elementId": "p3_b3", "focus": 0, "gap": 4})


# === PATTERN 4: Complex with chain() (bottom-right) ===
P4_Y = 280
txt("p4_title", COL2_X, P4_Y, COL_W, 25, "Complex (chain)", 22, color=YELLOW[0])
txt("p4_code", COL2_X, P4_Y + 28, COL_W, 20,
    "chain(t0, [t1, t2], [t3, t4], t5)", 14, color=GRAY[0])

P4_BOX_Y = P4_Y + 60
BW_S = 70   # smaller boxes for this pattern
BH_S = 38
COL_GAP = 45

# t0 on the left
T0_X = COL2_X + 5
T0_Y = P4_BOX_Y + 30
rect("p4_t0", T0_X, T0_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t0t", "type": "text"}])
txt("p4_t0t", T0_X, T0_Y, BW_S, BH_S, "t0", 16, cid="p4_t0")

# t1, t2 column
T12_X = T0_X + BW_S + COL_GAP
T1_Y = P4_BOX_Y + 5
T2_Y = T1_Y + BH_S + 20
rect("p4_t1", T12_X, T1_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t1t", "type": "text"}])
txt("p4_t1t", T12_X, T1_Y, BW_S, BH_S, "t1", 16, cid="p4_t1")

rect("p4_t2", T12_X, T2_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t2t", "type": "text"}])
txt("p4_t2t", T12_X, T2_Y, BW_S, BH_S, "t2", 16, cid="p4_t2")

# t3, t4 column
T34_X = T12_X + BW_S + COL_GAP
T3_Y = T1_Y
T4_Y = T2_Y
rect("p4_t3", T34_X, T3_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t3t", "type": "text"}])
txt("p4_t3t", T34_X, T3_Y, BW_S, BH_S, "t3", 16, cid="p4_t3")

rect("p4_t4", T34_X, T4_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t4t", "type": "text"}])
txt("p4_t4t", T34_X, T4_Y, BW_S, BH_S, "t4", 16, cid="p4_t4")

# t5 on the right
T5_X = T34_X + BW_S + COL_GAP
T5_Y = T0_Y
rect("p4_t5", T5_X, T5_Y, BW_S, BH_S, *YELLOW,
     bnd=[{"id": "p4_t5t", "type": "text"}])
txt("p4_t5t", T5_X, T5_Y, BW_S, BH_S, "t5", 16, cid="p4_t5")

# Arrows: t0 → t1, t0 → t2
arr("p4_a01", T0_X + BW_S, T0_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T1_Y + BH_S // 2 - T0_Y - BH_S // 2]], YELLOW[0],
    sb={"elementId": "p4_t0", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t1", "focus": 0, "gap": 4})
arr("p4_a02", T0_X + BW_S, T0_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T2_Y + BH_S // 2 - T0_Y - BH_S // 2]], YELLOW[0],
    sb={"elementId": "p4_t0", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t2", "focus": 0, "gap": 4})

# Arrows: t1 → t3, t1 → t4, t2 → t3, t2 → t4
arr("p4_a13", T12_X + BW_S, T1_Y + BH_S // 2,
    [[0, 0], [COL_GAP, 0]], YELLOW[0],
    sb={"elementId": "p4_t1", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t3", "focus": 0, "gap": 4})
arr("p4_a14", T12_X + BW_S, T1_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T4_Y - T1_Y]], YELLOW[0],
    sb={"elementId": "p4_t1", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t4", "focus": 0, "gap": 4})
arr("p4_a23", T12_X + BW_S, T2_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T3_Y - T2_Y]], YELLOW[0],
    sb={"elementId": "p4_t2", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t3", "focus": 0, "gap": 4})
arr("p4_a24", T12_X + BW_S, T2_Y + BH_S // 2,
    [[0, 0], [COL_GAP, 0]], YELLOW[0],
    sb={"elementId": "p4_t2", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t4", "focus": 0, "gap": 4})

# Arrows: t3 → t5, t4 → t5
arr("p4_a35", T34_X + BW_S, T3_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T5_Y + BH_S // 2 - T3_Y - BH_S // 2]], YELLOW[0],
    sb={"elementId": "p4_t3", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t5", "focus": 0, "gap": 4})
arr("p4_a45", T34_X + BW_S, T4_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T5_Y + BH_S // 2 - T4_Y - BH_S // 2]], YELLOW[0],
    sb={"elementId": "p4_t4", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t5", "focus": 0, "gap": 4})

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "dag-dependencies"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
