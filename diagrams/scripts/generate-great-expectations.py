"""
Great Expectations Workflow diagram.
Horizontal flow: Data Context → Data Sources → Expectations → Checkpoints
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, GRAY

d = ExcalidrawDiagram(seed=3000)

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
    (
        "Data Context",
        BLUE,
        [
            "Instantiate a data\ncontext object",
        ],
    ),
    (
        "Data Sources",
        GREEN,
        [
            "Declare the\ndata source",
            "Declare the\ndata assets",
            "Create a\nbatch_request",
        ],
    ),
    (
        "Expectations",
        YELLOW,
        [
            "Define\nexpectations",
            "Create an\nexpectation suite",
        ],
    ),
    (
        "Checkpoints",
        PURPLE,
        [
            "Create a\ncheckpoint",
            "Run validator —\ngenerate results",
        ],
    ),
]

# === BUILD DIAGRAM ===

# Title
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "Great Expectations Workflow",
    32,
    color="#1e1e1e",
)

# Metadata note at top right
d.txt(
    "meta",
    PAD_X,
    STAGE_START - 15,
    CONTENT_W,
    META_H,
    "Metadata stores: Expectation Store, Validation Store, Checkpoint Store, Data Docs",
    16,
    color=GRAY[0],
)

cur_y = STAGE_START + META_H + 10

for si, (stage_name, color, steps) in enumerate(stages):
    # Container box (dashed)
    n_steps = len(steps)
    container_inner_h = n_steps * STEP_H + (n_steps - 1) * STEP_GAP + 2 * INNER_PAD
    container_h = HDR_H + container_inner_h + INNER_PAD

    container_id = f"container{si}"
    d.rect(
        container_id,
        PAD_X,
        cur_y,
        CONTENT_W,
        container_h,
        color[0],
        "transparent",
        dashed=True,
    )

    # Header
    hdr_id = f"hdr{si}"
    d.rect(
        hdr_id,
        PAD_X + INNER_PAD,
        cur_y + INNER_PAD,
        CONTENT_W - 2 * INNER_PAD,
        HDR_H,
        color[0],
        color[1],
        bnd=[{"id": f"hdr-t{si}", "type": "text"}],
    )
    d.txt(
        f"hdr-t{si}",
        PAD_X + INNER_PAD,
        cur_y + INNER_PAD,
        CONTENT_W - 2 * INNER_PAD,
        HDR_H,
        stage_name,
        24,
        cid=hdr_id,
    )

    # Steps
    step_start_y = cur_y + INNER_PAD + HDR_H + INNER_PAD
    step_w = CONTENT_W - 4 * INNER_PAD
    step_x = PAD_X + 2 * INNER_PAD

    for ji, step_text in enumerate(steps):
        step_y = step_start_y + ji * (STEP_H + STEP_GAP)
        step_id = f"step{si}_{ji}"
        d.rect(
            step_id,
            step_x,
            step_y,
            step_w,
            STEP_H,
            color[0],
            color[1],
            opacity=60,
            bnd=[{"id": f"step-t{si}_{ji}", "type": "text"}],
        )
        d.txt(
            f"step-t{si}_{ji}",
            step_x,
            step_y,
            step_w,
            STEP_H,
            step_text,
            20,
            cid=step_id,
        )

        # Arrow between steps within same stage
        if ji > 0:
            prev_step_id = f"step{si}_{ji - 1}"
            arr_id = f"arr-inner{si}_{ji}"
            arr_x = step_x + step_w // 2
            arr_y_start = step_y - STEP_GAP
            d.arr(
                arr_id,
                arr_x,
                arr_y_start,
                [[0, 0], [0, STEP_GAP]],
                color[0],
                sb={"elementId": prev_step_id, "focus": 0, "gap": 4},
                eb={"elementId": step_id, "focus": 0, "gap": 4},
            )

    # Arrow between stages
    if si > 0:
        prev_container_id = f"container{si - 1}"
        arr_id = f"arr-stage{si}"
        arr_x = PAD_X + CONTENT_W // 2
        arr_y_start = cur_y - STAGE_GAP
        d.arr(
            arr_id,
            arr_x,
            arr_y_start,
            [[0, 0], [0, STAGE_GAP]],
            GRAY[0],
            sb={"elementId": prev_container_id, "focus": 0, "gap": 4},
            eb={"elementId": container_id, "focus": 0, "gap": 4},
        )

    cur_y += container_h + STAGE_GAP

# === WRITE FILE ===
name = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "diagrams/artifacts/great-expectations-workflow"
)
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
