import json
import math
import os

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 8000


def ns():
    global seed
    seed += 1
    return seed


def rect(
    id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2
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
            "strokeWidth": sw,
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
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
            "textAlign": "center",
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


# === LAYOUT CONSTANTS ===
LAYER_W = 160
LAYER_H = 45
COL_GAP = 40
TITLE_FONT = 28
LABEL_FONT = 22
LAYER_FONT = 18
SUB_FONT = 15
TITLE_GAP = 25  # Rule 18

# Colors
RED_STROKE = "#c92a2a"
RED_BG = "#ffc9c9"
BLUE_STROKE = "#1971c2"
BLUE_BG = "#a5d8ff"
GREEN_STROKE = "#2f9e44"
GREEN_BG = "#b2f2bb"
GRAY_STROKE = "#868e96"
GRAY_BG = "#dee2e6"

# === COLUMN DEFINITIONS ===
columns = [
    {
        "label": "Server",
        "subtitle": "You manage everything\nabove hardware",
        "stroke": RED_STROKE,
        "layers": [
            # bottom to top visually, but we'll reverse for drawing top-to-bottom
            ("Application", RED_STROKE, RED_BG),
            ("Runtime", RED_STROKE, RED_BG),
            ("OS", RED_STROKE, RED_BG),
            ("Hardware", GRAY_STROKE, GRAY_BG),
        ],
    },
    {
        "label": "Container",
        "subtitle": "You manage the\napplication layer",
        "stroke": BLUE_STROKE,
        "layers": [
            ("Application", BLUE_STROKE, BLUE_BG),
            ("Container\nRuntime", GRAY_STROKE, GRAY_BG),
            ("OS", GRAY_STROKE, GRAY_BG),
            ("Hardware", GRAY_STROKE, GRAY_BG),
        ],
    },
    {
        "label": "Serverless",
        "subtitle": "Provider manages\neverything",
        "stroke": GREEN_STROKE,
        "layers": [
            ("Application", GREEN_STROKE, GREEN_BG),
            ("Runtime", GRAY_STROKE, GRAY_BG),
            ("OS", GRAY_STROKE, GRAY_BG),
            ("Hardware", GRAY_STROKE, GRAY_BG),
        ],
    },
]

# === CALCULATE POSITIONS ===
# Total width: 3 columns + 2 gaps
TOTAL_W = 3 * LAYER_W + 2 * COL_GAP  # 560

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * TITLE_FONT * 1.25)  # single line
TITLE_X = 0
TITLE_W = TOTAL_W

# Column labels start after title + gap
LABEL_Y = TITLE_Y + TITLE_H + TITLE_GAP
LABEL_H = math.ceil(1 * LABEL_FONT * 1.25)  # single line

# Stack starts below label with a small gap
STACK_GAP_FROM_LABEL = 12
STACK_TOP = LABEL_Y + LABEL_H + STACK_GAP_FROM_LABEL

# Each stack: 4 layers, 0px gap (flush)
STACK_H = 4 * LAYER_H  # 180

# Subtitle below stack
SUB_GAP = 10
SUB_Y = STACK_TOP + STACK_H + SUB_GAP

# Column X positions
COL_XS = [0, LAYER_W + COL_GAP, 2 * (LAYER_W + COL_GAP)]

# === CREATE TITLE ===
txt(
    "title", TITLE_X, TITLE_Y, TITLE_W, TITLE_H, "Compute Models", TITLE_FONT, "#1e1e1e"
)

# === CREATE COLUMNS ===
for ci, col in enumerate(columns):
    cx = COL_XS[ci]
    prefix = f"c{ci}"

    # Column label (free text, not bound)
    txt(
        f"{prefix}-label",
        cx,
        LABEL_Y,
        LAYER_W,
        LABEL_H,
        col["label"],
        LABEL_FONT,
        "#1e1e1e",
    )

    # Layer stack (top to bottom: Application, Runtime/ContainerRuntime, OS, Hardware)
    for li, (layer_name, l_stroke, l_bg) in enumerate(col["layers"]):
        ly = STACK_TOP + li * LAYER_H
        layer_id = f"{prefix}-layer-{li}"
        layer_txt_id = f"{prefix}-ltxt-{li}"

        rect(
            layer_id,
            cx,
            ly,
            LAYER_W,
            LAYER_H,
            l_stroke,
            l_bg,
            fill="solid",
            bnd=[{"id": layer_txt_id, "type": "text"}],
        )
        txt(
            layer_txt_id,
            cx,
            ly,
            LAYER_W,
            LAYER_H,
            layer_name,
            LAYER_FONT,
            "#1e1e1e",
            cid=layer_id,
        )

    # Subtitle (free text, uses column stroke color per Rule 14)
    sub_lines = col["subtitle"].count("\n") + 1
    sub_h = math.ceil(sub_lines * SUB_FONT * 1.25)
    txt(
        f"{prefix}-sub",
        cx,
        SUB_Y,
        LAYER_W,
        sub_h,
        col["subtitle"],
        SUB_FONT,
        col["stroke"],
    )

# === LEGEND ===
LEGEND_GAP = 30
# Calculate subtitle max height (2 lines)
max_sub_h = math.ceil(2 * SUB_FONT * 1.25)
LEGEND_Y = SUB_Y + max_sub_h + LEGEND_GAP

LEGEND_BOX_SZ = 14
LEGEND_TEXT_W = 120
LEGEND_ITEM_W = LEGEND_BOX_SZ + 6 + LEGEND_TEXT_W  # box + gap + text
LEGEND_SPACING = 20  # between items

# Two legend items: "You Manage" (colored) + "Provider Manages" (gray)
legend_total_w = 2 * LEGEND_ITEM_W + LEGEND_SPACING
legend_start_x = (TOTAL_W - legend_total_w) // 2

# Item 1: "You Manage" - use blue as representative color
item1_x = legend_start_x
rect(
    "leg-box1",
    item1_x,
    LEGEND_Y,
    LEGEND_BOX_SZ,
    LEGEND_BOX_SZ,
    BLUE_STROKE,
    BLUE_BG,
    fill="solid",
    sw=1,
)
leg_txt_h = math.ceil(1 * SUB_FONT * 1.25)
txt(
    "leg-txt1",
    item1_x + LEGEND_BOX_SZ + 6,
    LEGEND_Y - 2,
    LEGEND_TEXT_W,
    leg_txt_h,
    "You Manage",
    SUB_FONT,
    "#1e1e1e",
)

# Item 2: "Provider Manages"
item2_x = item1_x + LEGEND_ITEM_W + LEGEND_SPACING
rect(
    "leg-box2",
    item2_x,
    LEGEND_Y,
    LEGEND_BOX_SZ,
    LEGEND_BOX_SZ,
    GRAY_STROKE,
    GRAY_BG,
    fill="solid",
    sw=1,
)
txt(
    "leg-txt2",
    item2_x + LEGEND_BOX_SZ + 6,
    LEGEND_Y - 2,
    LEGEND_TEXT_W,
    leg_txt_h,
    "Provider Manages",
    SUB_FONT,
    "#1e1e1e",
)

# === VERIFY POSITIONS ===
print(f"Title: y={TITLE_Y} to {TITLE_Y + TITLE_H}")
print(f"Label: y={LABEL_Y} to {LABEL_Y + LABEL_H}")
print(f"Stack: y={STACK_TOP} to {STACK_TOP + STACK_H}")
print(f"Subtitle: y={SUB_Y} to {SUB_Y + max_sub_h}")
print(f"Legend: y={LEGEND_Y}")
print(f"Total width: {TOTAL_W}")
print(f"Column Xs: {COL_XS}")

# === WRITE FILE ===
out_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams"
)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "compute-models.excalidraw")
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"\nWrote {out_path}")
