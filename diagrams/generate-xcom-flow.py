"""
XCom cross-communication flow diagram.
Shows: Task 1 → xcom_push → XCom Variable → Metadata DB → xcom_pull → Task 2

Horizontal flow with a vertical drop to the database.
Canvas: ~700px wide for good aspect ratio.
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
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(
    id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None
):
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
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


# === LAYOUT ===
# Horizontal flow: Task 1 → XCom Variable → Metadata DB → Task 2
# With xcom_push / xcom_pull labels on arrows

CANVAS_W = 680
PAD_X = 20

# Title
TITLE_Y = 20
txt("title", PAD_X, TITLE_Y, CANVAS_W - 2 * PAD_X, 40, "XCom Cross-Communication", 32)

# Row 1: Task 1 and XCom Variable box
ROW1_Y = 90
BW_TASK = 140
BH = 70
BW_XCOM = 200
BH_XCOM = 130
GAP_H = 90  # horizontal gap for arrows

# Task 1
T1_X = PAD_X + 20
T1_Y = ROW1_Y + 30
rect("task1", T1_X, T1_Y, BW_TASK, BH, *BLUE, bnd=[{"id": "t_task1", "type": "text"}])
txt("t_task1", T1_X, T1_Y, BW_TASK, BH, "Task 1", 24, cid="task1")

# XCom Variable (taller box with bullet list)
XCOM_X = T1_X + BW_TASK + GAP_H
XCOM_Y = ROW1_Y
rect(
    "xcom",
    XCOM_X,
    XCOM_Y,
    BW_XCOM,
    BH_XCOM,
    *PURPLE,
    bnd=[{"id": "t_xcom", "type": "text"}],
)
txt(
    "t_xcom",
    XCOM_X,
    XCOM_Y,
    BW_XCOM,
    BH_XCOM,
    "XCom Variable\n\nValue\nKey\nTimestamp\nDAG ID\nTask ID",
    18,
    cid="xcom",
)

# Arrow: Task 1 → XCom Variable
A1_X = T1_X + BW_TASK
A1_Y = T1_Y + BH // 2
arr(
    "a1",
    A1_X,
    A1_Y,
    [[0, 0], [GAP_H, 0]],
    BLUE[0],
    sb={"elementId": "task1", "focus": 0, "gap": 4},
    eb={"elementId": "xcom", "focus": 0, "gap": 4},
)

# Label: xcom_push
txt("l_push", A1_X + 10, A1_Y - 28, 70, 20, "xcom_push", 16, color=BLUE[0])

# Row 2: Metadata Database (centered below XCom Variable)
DB_W = 200
DB_H = 70
DB_X = XCOM_X
DB_Y = XCOM_Y + BH_XCOM + 70
rect("db", DB_X, DB_Y, DB_W, DB_H, *GRAY, bnd=[{"id": "t_db", "type": "text"}])
txt("t_db", DB_X, DB_Y, DB_W, DB_H, "Metadata\nDatabase", 22, cid="db")

# Arrow: XCom Variable → Metadata DB (vertical)
A2_X = XCOM_X + BW_XCOM // 2
A2_Y = XCOM_Y + BH_XCOM
arr(
    "a2",
    A2_X,
    A2_Y,
    [[0, 0], [0, 70]],
    PURPLE[0],
    sb={"elementId": "xcom", "focus": 0, "gap": 4},
    eb={"elementId": "db", "focus": 0, "gap": 4},
)

# Task 2 (to the right of DB)
T2_X = DB_X + DB_W + GAP_H
T2_Y = DB_Y
rect("task2", T2_X, T2_Y, BW_TASK, BH, *GREEN, bnd=[{"id": "t_task2", "type": "text"}])
txt("t_task2", T2_X, T2_Y, BW_TASK, BH, "Task 2", 24, cid="task2")

# Arrow: Metadata DB → Task 2
A3_X = DB_X + DB_W
A3_Y = DB_Y + DB_H // 2
arr(
    "a3",
    A3_X,
    A3_Y,
    [[0, 0], [GAP_H, 0]],
    GRAY[0],
    sb={"elementId": "db", "focus": 0, "gap": 4},
    eb={"elementId": "task2", "focus": 0, "gap": 4},
)

# Label: xcom_pull
txt("l_pull", A3_X + 10, A3_Y - 28, 70, 20, "xcom_pull", 16, color=GREEN[0])

# Subtitle
txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CANVAS_W - 2 * PAD_X,
    25,
    "Tasks exchange small data via the metadata database",
    17,
    color=PURPLE[0],
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "xcom-flow"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
