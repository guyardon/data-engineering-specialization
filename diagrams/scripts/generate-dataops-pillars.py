"""
DataOps 3 Pillars diagram for section 3.1.1.
Shows DataOps at top with three pillars below, each with key sub-items.
"""

import sys

from diagramlib import BLUE, GREEN, PURPLE, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT CONSTANTS ===

CANVAS_W = 660
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 600

# Title
TITLE_Y = 20

# Top DataOps box
TOP_Y = 65
TOP_W = 300
TOP_H = 60
TOP_X = (CANVAS_W - TOP_W) // 2

# Subtitle under DataOps
SUB_Y = TOP_Y + TOP_H + 8

# Three pillars
COL_W = 180
COL_GAP = 30
TOTAL_COLS_W = 3 * COL_W + 2 * COL_GAP  # 600
COL_START_X = PAD_X
PILLAR_Y = SUB_Y + 30 + 75  # after subtitle + arrow gap
PILLAR_H = 60

# Sub-item pills under each pillar
PILL_GAP = 12
PILL_H = 40
PILL_Y1 = PILLAR_Y + PILLAR_H + 75  # arrow gap
PILL_Y2 = PILL_Y1 + PILL_H + PILL_GAP

# Arrow gap between DataOps and pillars
ARROW_GAP = 75

# === BUILD DIAGRAM ===

# Title
d.txt("title", 0, TITLE_Y, CANVAS_W, 40, "DataOps", 32)

# Main DataOps box
d.rect(
    "dataops",
    TOP_X,
    TOP_Y + 55,
    TOP_W,
    TOP_H,
    *PURPLE,
    bnd=[
        {"id": "t_dataops", "type": "text"},
        {"id": "a1", "type": "arrow"},
        {"id": "a2", "type": "arrow"},
        {"id": "a3", "type": "arrow"},
    ],
)
d.txt("t_dataops", TOP_X, TOP_Y + 55, TOP_W, TOP_H, "DataOps", 26, cid="dataops")

# Subtitle
d.txt(
    "sub",
    0,
    TOP_Y + 55 + TOP_H + 5,
    CANVAS_W,
    25,
    "Practices for building robust data systems",
    18,
    color=PURPLE[0],
)

# Three pillar columns
col_xs = [COL_START_X + i * (COL_W + COL_GAP) for i in range(3)]
PILLAR_TOP = TOP_Y + 55 + TOP_H + 5 + 25 + ARROW_GAP

pillars = [
    ("p1", "Automation", BLUE),
    ("p2", "Observability\n& Monitoring", GREEN),
    ("p3", "Incident\nResponse", YELLOW),
]

for i, (pid, label, color) in enumerate(pillars):
    px = col_xs[i]
    d.rect(
        pid,
        px,
        PILLAR_TOP,
        COL_W,
        PILLAR_H,
        *color,
        bnd=[{"id": f"t_{pid}", "type": "text"}],
    )
    d.txt(f"t_{pid}", px, PILLAR_TOP, COL_W, PILLAR_H, label, 22, cid=pid)

# Arrows from DataOps to pillars
dataops_cx = TOP_X + TOP_W // 2
dataops_bottom = TOP_Y + 55 + TOP_H

for i, (pid, _, color) in enumerate(pillars):
    px = col_xs[i] + COL_W // 2
    d.arr(
        f"a{i + 1}",
        dataops_cx,
        dataops_bottom + 30,
        [[0, 0], [px - dataops_cx, PILLAR_TOP - dataops_bottom - 30]],
        color[0],
        sb={"elementId": "dataops", "focus": 0, "gap": 4},
        eb={"elementId": pid, "focus": 0, "gap": 4},
    )

# Sub-items under each pillar
sub_items = [
    [("CI/CD Pipelines", BLUE), ("Infrastructure\nas Code", BLUE)],
    [("Data Quality\nChecks", GREEN), ("Pipeline\nMetrics", GREEN)],
    [("Alerting &\nEscalation", YELLOW), ("Root Cause\nAnalysis", YELLOW)],
]

SUB_TOP = PILLAR_TOP + PILLAR_H + 70

for i, items in enumerate(sub_items):
    px = col_xs[i]
    for j, (label, color) in enumerate(items):
        sy = SUB_TOP + j * (PILL_H + PILL_GAP)
        sid = f"s{i}_{j}"
        d.rect(
            sid,
            px,
            sy,
            COL_W,
            PILL_H,
            color[0],
            color[1],
            bnd=[{"id": f"t_{sid}", "type": "text"}],
        )
        d.txt(f"t_{sid}", px, sy, COL_W, PILL_H, label, 18, cid=sid)

    # Arrow from pillar to first sub-item
    d.arr(
        f"pa{i}",
        col_xs[i] + COL_W // 2,
        PILLAR_TOP + PILLAR_H,
        [[0, 0], [0, 70]],
        pillars[i][2][0],
        sb={"elementId": pillars[i][0], "focus": 0, "gap": 4},
        eb={"elementId": f"s{i}_0", "focus": 0, "gap": 4},
    )


# === VERIFY ===
print(f"Title: y={TITLE_Y}")
print(f"DataOps box: y={TOP_Y + 55} to {TOP_Y + 55 + TOP_H}")
print(f"Pillars: y={PILLAR_TOP} to {PILLAR_TOP + PILLAR_H}")
print(f"Sub-items: y={SUB_TOP} to {SUB_TOP + PILL_H + PILL_GAP + PILL_H}")
print(f"Canvas width: {CANVAS_W}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/dataops-pillars"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
