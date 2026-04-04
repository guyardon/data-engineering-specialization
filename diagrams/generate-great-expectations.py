"""
Great Expectations Workflow diagram.
Horizontal flow: Data Context → Data Sources → Expectations → Checkpoints
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
seed = 3000


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
        "width": pts[-1][0] - pts[0][0], "height": pts[-1][1] - pts[0][1],
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


# === LAYOUT — Vertical flow (4 stages stacked) ===
CANVAS_W = 600
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 560

TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Each stage: header box + inner steps stacked vertically
STAGE_START = TITLE_Y + TITLE_H + 30
HDR_H = 50
STEP_H = 55
STEP_GAP = 12
STAGE_GAP = 75  # arrow gap between stages
INNER_PAD = 15

# Metadata store note
META_Y = TITLE_Y + TITLE_H + 5
META_H = math.ceil(2 * 16 * 1.25)

# Stage definitions
stages = [
    ("Data Context", BLUE, [
        "Instantiate a data\ncontext object",
    ]),
    ("Data Sources", GREEN, [
        "Declare the\ndata source",
        "Declare the\ndata assets",
        "Create a\nbatch_request",
    ]),
    ("Expectations", YELLOW, [
        "Define\nexpectations",
        "Create an\nexpectation suite",
    ]),
    ("Checkpoints", PURPLE, [
        "Create a\ncheckpoint",
        "Run validator —\ngenerate results",
    ]),
]

# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Great Expectations Workflow", 32, color="#1e1e1e")

# Metadata note at top right
txt("meta", PAD_X, STAGE_START - 15, CONTENT_W, META_H,
    "Metadata stores: Expectation Store, Validation Store, Checkpoint Store, Data Docs",
    16, color=GRAY[0])

cur_y = STAGE_START + META_H + 10

for si, (stage_name, color, steps) in enumerate(stages):
    # Container box (dashed)
    n_steps = len(steps)
    container_inner_h = n_steps * STEP_H + (n_steps - 1) * STEP_GAP + 2 * INNER_PAD
    container_h = HDR_H + container_inner_h + INNER_PAD

    container_id = f"container{si}"
    rect(container_id, PAD_X, cur_y, CONTENT_W, container_h,
         color[0], "transparent", dashed=True)

    # Header
    hdr_id = f"hdr{si}"
    rect(hdr_id, PAD_X + INNER_PAD, cur_y + INNER_PAD,
         CONTENT_W - 2 * INNER_PAD, HDR_H, color[0], color[1],
         bnd=[{"id": f"hdr-t{si}", "type": "text"}])
    txt(f"hdr-t{si}", PAD_X + INNER_PAD, cur_y + INNER_PAD,
        CONTENT_W - 2 * INNER_PAD, HDR_H,
        stage_name, 24, cid=hdr_id)

    # Steps
    step_start_y = cur_y + INNER_PAD + HDR_H + INNER_PAD
    step_w = CONTENT_W - 4 * INNER_PAD
    step_x = PAD_X + 2 * INNER_PAD

    for ji, step_text in enumerate(steps):
        step_y = step_start_y + ji * (STEP_H + STEP_GAP)
        step_id = f"step{si}_{ji}"
        rect(step_id, step_x, step_y, step_w, STEP_H,
             color[0], color[1], opacity=60,
             bnd=[{"id": f"step-t{si}_{ji}", "type": "text"}])
        txt(f"step-t{si}_{ji}", step_x, step_y, step_w, STEP_H,
            step_text, 20, cid=step_id)

        # Arrow between steps within same stage
        if ji > 0:
            prev_step_id = f"step{si}_{ji - 1}"
            arr_id = f"arr-inner{si}_{ji}"
            arr_x = step_x + step_w // 2
            arr_y_start = step_y - STEP_GAP
            arr(arr_id, arr_x, arr_y_start,
                [[0, 0], [0, STEP_GAP]], color[0],
                sb={"elementId": prev_step_id, "focus": 0, "gap": 4},
                eb={"elementId": step_id, "focus": 0, "gap": 4})

    # Arrow between stages
    if si > 0:
        prev_container_id = f"container{si - 1}"
        arr_id = f"arr-stage{si}"
        arr_x = PAD_X + CONTENT_W // 2
        arr_y_start = cur_y - STAGE_GAP
        arr(arr_id, arr_x, arr_y_start,
            [[0, 0], [0, STAGE_GAP]], GRAY[0],
            sb={"elementId": prev_container_id, "focus": 0, "gap": 4},
            eb={"elementId": container_id, "focus": 0, "gap": 4})

    cur_y += container_h + STAGE_GAP

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "great-expectations-workflow"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
