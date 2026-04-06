"""
Airflow Core Components — layered architecture diagram.
Shows DAG Directory, Scheduler, Workers, Metadata Database,
Web Server, and User Interface with data flow arrows.
"""

import math
import sys

from diagramlib import BLUE, CYAN, GRAY, GREEN, PURPLE, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT CONSTANTS ===

CANVAS_W = 630
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X  # 580

BOX_W = 260  # width for paired boxes (side by side)
BOX_FULL_W = CONTENT_W  # width for centered single box
BOX_H = 85  # consistent box height
BOX_GAP = CONTENT_W - 2 * BOX_W  # gap between side-by-side boxes
ARROW_GAP = 75  # vertical gap between layers for arrows

# === HELPER: title+subtitle box (Rule 13) ===


def component_box(box_id, x, y, w, h, title, subtitle, color):
    """Draw a box with bound title text and free subtitle text."""
    title_h = math.ceil(1 * 22 * 1.25)  # ~28
    sub_lines = subtitle.count("\n") + 1
    sub_h = math.ceil(sub_lines * 17 * 1.25)
    gap = 5
    combined = title_h + gap + sub_h
    top_pad = (h - combined) // 2
    title_y = y + top_pad
    sub_y = title_y + title_h + gap

    d.rect(
        box_id,
        x,
        y,
        w,
        h,
        color[0],
        color[1],
        bnd=[{"id": f"t_{box_id}", "type": "text"}],
    )
    d.txt(f"t_{box_id}", x, title_y, w, title_h, title, 22, color="#1e1e1e", cid=box_id)
    d.txt(f"s_{box_id}", x, sub_y, w, sub_h, subtitle, 17, color=color[0])


# === BUILD DIAGRAM ===

Y = 20

# --- Diagram title ---
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt(
    "title",
    PAD_X,
    Y,
    CONTENT_W,
    TITLE_H,
    "Airflow Core Components",
    32,
    color="#1e1e1e",
)
Y += TITLE_H + 30

# --- Layer 1: DAG Directory (centered, full width) ---
DAG_Y = Y
component_box(
    "dag",
    PAD_X,
    DAG_Y,
    BOX_FULL_W,
    BOX_H,
    "DAG Directory",
    "Stores Python DAG files\nwritten by data engineers",
    YELLOW,
)
Y += BOX_H

# Arrow: DAG Directory → Scheduler (reads DAGs)
d.arr(
    "a_dag_sched",
    CANVAS_W // 2,
    Y,
    [[0, 0], [0, ARROW_GAP]],
    YELLOW[0],
    sb={"elementId": "dag", "focus": 0, "gap": 4},
    eb={"elementId": "sched", "focus": 0, "gap": 4},
)
d.txt(
    "al_dag_sched",
    CANVAS_W // 2 + 8,
    Y + 20,
    120,
    22,
    "reads DAGs",
    17,
    color=YELLOW[0],
    op=85,
)
Y += ARROW_GAP

# --- Layer 2: Scheduler + Workers (side by side) ---
PAIR_Y = Y
SCHED_X = PAD_X
WORKER_X = PAD_X + BOX_W + BOX_GAP

component_box(
    "sched",
    SCHED_X,
    PAIR_Y,
    BOX_W,
    BOX_H,
    "Scheduler",
    "Monitors DAGs, triggers\ntask execution",
    BLUE,
)
component_box(
    "worker",
    WORKER_X,
    PAIR_Y,
    BOX_W,
    BOX_H,
    "Workers",
    "Execute the tasks\npushed by the Scheduler",
    GREEN,
)

# Arrow: Scheduler → Workers (horizontal, pushes tasks)
d.arr(
    "a_sched_worker",
    SCHED_X + BOX_W,
    PAIR_Y + BOX_H // 2,
    [[0, 0], [BOX_GAP, 0]],
    BLUE[0],
    sb={"elementId": "sched", "focus": 0, "gap": 4},
    eb={"elementId": "worker", "focus": 0, "gap": 4},
)
d.txt(
    "al_sched_worker",
    SCHED_X + BOX_W + 2,
    PAIR_Y + BOX_H // 2 - 25,
    BOX_GAP,
    22,
    "pushes\ntasks",
    17,
    color=BLUE[0],
    op=85,
)

Y += BOX_H

# Arrow: Workers → Metadata Database (writes status)
d.arr(
    "a_worker_meta",
    CANVAS_W // 2,
    Y,
    [[0, 0], [0, ARROW_GAP]],
    GREEN[0],
    sb={"elementId": "worker", "focus": 0, "gap": 4},
    eb={"elementId": "metadb", "focus": 0, "gap": 4},
)
d.txt(
    "al_worker_meta",
    CANVAS_W // 2 + 8,
    Y + 20,
    130,
    22,
    "writes status",
    17,
    color=GREEN[0],
    op=85,
)
Y += ARROW_GAP

# --- Layer 3: Metadata Database (centered, full width) ---
META_Y = Y
component_box(
    "metadb",
    PAD_X,
    META_Y,
    BOX_FULL_W,
    BOX_H,
    "Metadata Database",
    "Stores DAG runs, task states,\nand configuration",
    PURPLE,
)
Y += BOX_H

# Arrow: Metadata DB → Web Server (reads state)
d.arr(
    "a_meta_web",
    CANVAS_W // 2,
    Y,
    [[0, 0], [0, ARROW_GAP]],
    PURPLE[0],
    sb={"elementId": "metadb", "focus": 0, "gap": 4},
    eb={"elementId": "webserver", "focus": 0, "gap": 4},
)
d.txt(
    "al_meta_web",
    CANVAS_W // 2 + 8,
    Y + 20,
    120,
    22,
    "reads state",
    17,
    color=PURPLE[0],
    op=85,
)
Y += ARROW_GAP

# --- Layer 4: Web Server + User Interface (side by side) ---
BOTTOM_Y = Y
WEB_X = PAD_X
UI_X = PAD_X + BOX_W + BOX_GAP

component_box(
    "webserver",
    WEB_X,
    BOTTOM_Y,
    BOX_W,
    BOX_H,
    "Web Server",
    "Reads metadata, serves\nthe dashboard UI",
    CYAN,
)
component_box(
    "ui",
    UI_X,
    BOTTOM_Y,
    BOX_W,
    BOX_H,
    "User Interface",
    "Visualize DAG runs,\nlogs, and task status",
    GRAY,
)

# Arrow: Web Server → User Interface (horizontal, serves UI)
d.arr(
    "a_web_ui",
    WEB_X + BOX_W,
    BOTTOM_Y + BOX_H // 2,
    [[0, 0], [BOX_GAP, 0]],
    CYAN[0],
    sb={"elementId": "webserver", "focus": 0, "gap": 4},
    eb={"elementId": "ui", "focus": 0, "gap": 4},
)
d.txt(
    "al_web_ui",
    WEB_X + BOX_W + 2,
    BOTTOM_Y + BOX_H // 2 - 25,
    BOX_GAP,
    22,
    "serves\nUI",
    17,
    color=CYAN[0],
    op=85,
)

Y += BOX_H + 20

# === VERIFY ===
print(f"Canvas width: {CANVAS_W}")
print(f"Total height: ~{Y}")
print(f"Elements: {len(d.elements)}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/airflow-components"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
