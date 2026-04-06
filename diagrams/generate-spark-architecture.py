"""
Generate Spark application architecture diagram showing Driver,
Cluster Manager, and Worker Nodes with executors.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, CYAN, PURPLE, YELLOW

d = ExcalidrawDiagram(seed=14000)

CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Spark Application Architecture", 30, color="#1e1e1e")

# === SparkSession / Driver ===
DRIVER_Y = TITLE_Y + TITLE_H + 25
DRIVER_W = 240
DRIVER_H = 60
DRIVER_X = PAD_X + (CONTENT_W - DRIVER_W) // 2

d.rect("driver", DRIVER_X, DRIVER_Y, DRIVER_W, DRIVER_H, *YELLOW,
     bnd=[{"id": "driver_t", "type": "text"}])
driver_title_h = math.ceil(1 * 22 * 1.25)
driver_sub_h = math.ceil(1 * 15 * 1.25)
driver_gap = 3
driver_comb = driver_title_h + driver_gap + driver_sub_h
driver_pad = (DRIVER_H - driver_comb) // 2
d.txt("driver_t", DRIVER_X, DRIVER_Y + driver_pad, DRIVER_W, driver_title_h,
    "Driver Node", 22, cid="driver")
d.txt("driver_sub", DRIVER_X, DRIVER_Y + driver_pad + driver_title_h + driver_gap,
    DRIVER_W, driver_sub_h, "SparkSession + DAG Scheduler", 15, color=YELLOW[0])

# === Cluster Manager ===
CM_Y = DRIVER_Y + DRIVER_H + 55
CM_W = 220
CM_H = 50
CM_X = PAD_X + (CONTENT_W - CM_W) // 2

d.rect("cm", CM_X, CM_Y, CM_W, CM_H, *PURPLE,
     bnd=[{"id": "cm_t", "type": "text"}])
d.txt("cm_t", CM_X, CM_Y, CM_W, CM_H, "Cluster Manager", 20, cid="cm")
CM_SUB_Y = CM_Y + CM_H + 5
CM_SUB_H = math.ceil(1 * 14 * 1.25)
d.txt("cm_sub", CM_X, CM_SUB_Y, CM_W, CM_SUB_H,
    "YARN / Mesos / K8s", 14, color=PURPLE[0])

d.arr("a_driver_cm", DRIVER_X + DRIVER_W // 2, DRIVER_Y + DRIVER_H,
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
    d.rect(wid, wx, WORKERS_Y, WORKER_W, WORKER_H, BLUE[0], "#dbe4ff", dashed=True)

    # Worker label
    wl_y = WORKERS_Y + 8
    wl_h = math.ceil(1 * 16 * 1.25)
    d.txt(f"{wid}_label", wx, wl_y, WORKER_W, wl_h,
        f"Worker {i + 1}", 16, color=BLUE[0])

    # Executor box inside
    EX_PAD = 12
    EX_W = WORKER_W - 2 * EX_PAD
    EX_H = 50
    EX_Y = wl_y + wl_h + 8
    EX_X = wx + EX_PAD

    d.rect(f"ex{i}", EX_X, EX_Y, EX_W, EX_H, *CYAN,
         bnd=[{"id": f"ex{i}_t", "type": "text"}])
    ex_title_h = math.ceil(1 * 17 * 1.25)
    ex_sub_h = math.ceil(1 * 13 * 1.25)
    ex_gap = 2
    ex_comb = ex_title_h + ex_gap + ex_sub_h
    ex_pad = (EX_H - ex_comb) // 2
    d.txt(f"ex{i}_t", EX_X, EX_Y + ex_pad, EX_W, ex_title_h,
        "Executor", 17, cid=f"ex{i}")
    d.txt(f"ex{i}_sub", EX_X, EX_Y + ex_pad + ex_title_h + ex_gap, EX_W, ex_sub_h,
        "Tasks + Cache", 13, color=CYAN[0])

    # Arrow from CM to worker
    d.arr(f"a_cm_w{i}", CM_X + CM_W // 2, CM_SUB_Y + CM_SUB_H,
        [[0, 0], [wx + WORKER_W // 2 - CM_X - CM_W // 2, WORKERS_Y - CM_SUB_Y - CM_SUB_H]],
        PURPLE[0],
        eb={"elementId": wid, "focus": 0, "gap": 4})

print(f"Canvas: {CANVAS_W}x{WORKERS_Y + WORKER_H + 20}")

name = sys.argv[1] if len(sys.argv) > 1 else "spark-architecture"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
