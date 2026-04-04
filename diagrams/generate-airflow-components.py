"""
Airflow Core Components — layered architecture diagram.
Shows DAG Directory, Scheduler, Workers, Metadata Database,
Web Server, and User Interface with data flow arrows.
"""

import json
import math
import sys

# === FILE STRUCTURE ===

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


# === COLOR PALETTE ===

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


# === HELPER FUNCTIONS ===


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

    rect(box_id, x, y, w, h, color[0], color[1],
         bnd=[{"id": f"t_{box_id}", "type": "text"}])
    txt(f"t_{box_id}", x, title_y, w, title_h,
        title, 22, color="#1e1e1e", cid=box_id)
    txt(f"s_{box_id}", x, sub_y, w, sub_h,
        subtitle, 17, color=color[0])


# === BUILD DIAGRAM ===

Y = 20

# --- Diagram title ---
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, Y, CONTENT_W, TITLE_H,
    "Airflow Core Components", 32, color="#1e1e1e")
Y += TITLE_H + 30

# --- Layer 1: DAG Directory (centered, full width) ---
DAG_Y = Y
component_box("dag", PAD_X, DAG_Y, BOX_FULL_W, BOX_H,
              "DAG Directory", "Stores Python DAG files\nwritten by data engineers", YELLOW)
Y += BOX_H

# Arrow: DAG Directory → Scheduler (reads DAGs)
arr("a_dag_sched", CANVAS_W // 2, Y,
    [[0, 0], [0, ARROW_GAP]],
    YELLOW[0],
    sb={"elementId": "dag", "focus": 0, "gap": 4},
    eb={"elementId": "sched", "focus": 0, "gap": 4})
txt("al_dag_sched", CANVAS_W // 2 + 8, Y + 20, 120, 22,
    "reads DAGs", 17, color=YELLOW[0], op=85)
Y += ARROW_GAP

# --- Layer 2: Scheduler + Workers (side by side) ---
PAIR_Y = Y
SCHED_X = PAD_X
WORKER_X = PAD_X + BOX_W + BOX_GAP

component_box("sched", SCHED_X, PAIR_Y, BOX_W, BOX_H,
              "Scheduler", "Monitors DAGs, triggers\ntask execution", BLUE)
component_box("worker", WORKER_X, PAIR_Y, BOX_W, BOX_H,
              "Workers", "Execute the tasks\npushed by the Scheduler", GREEN)

# Arrow: Scheduler → Workers (horizontal, pushes tasks)
arr("a_sched_worker", SCHED_X + BOX_W, PAIR_Y + BOX_H // 2,
    [[0, 0], [BOX_GAP, 0]],
    BLUE[0],
    sb={"elementId": "sched", "focus": 0, "gap": 4},
    eb={"elementId": "worker", "focus": 0, "gap": 4})
txt("al_sched_worker", SCHED_X + BOX_W + 2, PAIR_Y + BOX_H // 2 - 25, BOX_GAP, 22,
    "pushes\ntasks", 17, color=BLUE[0], op=85)

Y += BOX_H

# Arrow: Workers → Metadata Database (writes status)
arr("a_worker_meta", CANVAS_W // 2, Y,
    [[0, 0], [0, ARROW_GAP]],
    GREEN[0],
    sb={"elementId": "worker", "focus": 0, "gap": 4},
    eb={"elementId": "metadb", "focus": 0, "gap": 4})
txt("al_worker_meta", CANVAS_W // 2 + 8, Y + 20, 130, 22,
    "writes status", 17, color=GREEN[0], op=85)
Y += ARROW_GAP

# --- Layer 3: Metadata Database (centered, full width) ---
META_Y = Y
component_box("metadb", PAD_X, META_Y, BOX_FULL_W, BOX_H,
              "Metadata Database", "Stores DAG runs, task states,\nand configuration", PURPLE)
Y += BOX_H

# Arrow: Metadata DB → Web Server (reads state)
arr("a_meta_web", CANVAS_W // 2, Y,
    [[0, 0], [0, ARROW_GAP]],
    PURPLE[0],
    sb={"elementId": "metadb", "focus": 0, "gap": 4},
    eb={"elementId": "webserver", "focus": 0, "gap": 4})
txt("al_meta_web", CANVAS_W // 2 + 8, Y + 20, 120, 22,
    "reads state", 17, color=PURPLE[0], op=85)
Y += ARROW_GAP

# --- Layer 4: Web Server + User Interface (side by side) ---
BOTTOM_Y = Y
WEB_X = PAD_X
UI_X = PAD_X + BOX_W + BOX_GAP

component_box("webserver", WEB_X, BOTTOM_Y, BOX_W, BOX_H,
              "Web Server", "Reads metadata, serves\nthe dashboard UI", CYAN)
component_box("ui", UI_X, BOTTOM_Y, BOX_W, BOX_H,
              "User Interface", "Visualize DAG runs,\nlogs, and task status", GRAY)

# Arrow: Web Server → User Interface (horizontal, serves UI)
arr("a_web_ui", WEB_X + BOX_W, BOTTOM_Y + BOX_H // 2,
    [[0, 0], [BOX_GAP, 0]],
    CYAN[0],
    sb={"elementId": "webserver", "focus": 0, "gap": 4},
    eb={"elementId": "ui", "focus": 0, "gap": 4})
txt("al_web_ui", WEB_X + BOX_W + 2, BOTTOM_Y + BOX_H // 2 - 25, BOX_GAP, 22,
    "serves\nUI", 17, color=CYAN[0], op=85)

Y += BOX_H + 20

# === VERIFY ===
print(f"Canvas width: {CANVAS_W}")
print(f"Total height: ~{Y}")
print(f"Elements: {len(els)}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "airflow-components"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
