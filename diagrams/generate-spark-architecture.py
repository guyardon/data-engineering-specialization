"""
Generate Spark application architecture diagram showing Driver,
Cluster Manager, and Worker Nodes with executors.
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
seed = 14000


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


CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Spark Application Architecture", 30, color="#1e1e1e")

# === SparkSession / Driver ===
DRIVER_Y = TITLE_Y + TITLE_H + 25
DRIVER_W = 240
DRIVER_H = 60
DRIVER_X = PAD_X + (CONTENT_W - DRIVER_W) // 2

rect("driver", DRIVER_X, DRIVER_Y, DRIVER_W, DRIVER_H, *YELLOW,
     bnd=[{"id": "driver_t", "type": "text"}])
driver_title_h = math.ceil(1 * 22 * 1.25)
driver_sub_h = math.ceil(1 * 15 * 1.25)
driver_gap = 3
driver_comb = driver_title_h + driver_gap + driver_sub_h
driver_pad = (DRIVER_H - driver_comb) // 2
txt("driver_t", DRIVER_X, DRIVER_Y + driver_pad, DRIVER_W, driver_title_h,
    "Driver Node", 22, cid="driver")
txt("driver_sub", DRIVER_X, DRIVER_Y + driver_pad + driver_title_h + driver_gap,
    DRIVER_W, driver_sub_h, "SparkSession + DAG Scheduler", 15, color=YELLOW[0])

# === Cluster Manager ===
CM_Y = DRIVER_Y + DRIVER_H + 55
CM_W = 220
CM_H = 50
CM_X = PAD_X + (CONTENT_W - CM_W) // 2

rect("cm", CM_X, CM_Y, CM_W, CM_H, *PURPLE,
     bnd=[{"id": "cm_t", "type": "text"}])
txt("cm_t", CM_X, CM_Y, CM_W, CM_H, "Cluster Manager", 20, cid="cm")
CM_SUB_Y = CM_Y + CM_H + 5
CM_SUB_H = math.ceil(1 * 14 * 1.25)
txt("cm_sub", CM_X, CM_SUB_Y, CM_W, CM_SUB_H,
    "YARN / Mesos / K8s", 14, color=PURPLE[0])

arr("a_driver_cm", DRIVER_X + DRIVER_W // 2, DRIVER_Y + DRIVER_H,
    [[0, 0], [0, CM_Y - DRIVER_Y - DRIVER_H]],
    YELLOW[0],
    sb={"elementId": "driver", "focus": 0, "gap": 4},
    eb={"elementId": "cm", "focus": 0, "gap": 4})

# === Worker Nodes ===
WORKERS_Y = CM_SUB_Y + CM_SUB_H + 50
WORKER_W = (CONTENT_W - 20) // 3
WORKER_H = 120
WORKER_GAP = 10

for i in range(3):
    wx = PAD_X + i * (WORKER_W + WORKER_GAP)
    wid = f"w{i}"

    # Worker container
    rect(wid, wx, WORKERS_Y, WORKER_W, WORKER_H, BLUE[0], "#dbe4ff", dashed=True)

    # Worker label
    wl_y = WORKERS_Y + 8
    wl_h = math.ceil(1 * 16 * 1.25)
    txt(f"{wid}_label", wx, wl_y, WORKER_W, wl_h,
        f"Worker {i + 1}", 16, color=BLUE[0])

    # Executor box inside
    EX_PAD = 12
    EX_W = WORKER_W - 2 * EX_PAD
    EX_H = 50
    EX_Y = wl_y + wl_h + 8
    EX_X = wx + EX_PAD

    rect(f"ex{i}", EX_X, EX_Y, EX_W, EX_H, *CYAN,
         bnd=[{"id": f"ex{i}_t", "type": "text"}])
    ex_title_h = math.ceil(1 * 17 * 1.25)
    ex_sub_h = math.ceil(1 * 13 * 1.25)
    ex_gap = 2
    ex_comb = ex_title_h + ex_gap + ex_sub_h
    ex_pad = (EX_H - ex_comb) // 2
    txt(f"ex{i}_t", EX_X, EX_Y + ex_pad, EX_W, ex_title_h,
        "Executor", 17, cid=f"ex{i}")
    txt(f"ex{i}_sub", EX_X, EX_Y + ex_pad + ex_title_h + ex_gap, EX_W, ex_sub_h,
        "Tasks + Cache", 13, color=CYAN[0])

    # Arrow from CM to worker
    arr(f"a_cm_w{i}", CM_X + CM_W // 2, CM_SUB_Y + CM_SUB_H,
        [[0, 0], [wx + WORKER_W // 2 - CM_X - CM_W // 2, WORKERS_Y - CM_SUB_Y - CM_SUB_H]],
        PURPLE[0],
        eb={"elementId": wid, "focus": 0, "gap": 4})

print(f"Canvas: {CANVAS_W}x{WORKERS_Y + WORKER_H + 20}")

name = sys.argv[1] if len(sys.argv) > 1 else "spark-architecture"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
