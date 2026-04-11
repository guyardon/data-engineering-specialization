"""Generate Excalidraw diagram: Diagram Pipeline architecture for README."""

import json
import math

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


# === COLOR PALETTE ===
BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
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


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": pts[-1][0] - pts[0][0],
            "height": pts[-1][1] - pts[0][1],
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


# === LAYOUT CONSTANTS ===
CANVAS_W = 700
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 640
BW = 180
BH = 70
GAP_H = 70
GAP_V = 80

# Title
txt("title", 0, 15, CANVAS_W, 40, "Diagram Pipeline", 32)

# === EXCALIDRAW PATH (left column) ===
COL_LEFT_X = PAD_X + 20
COL_RIGHT_X = CANVAS_W // 2 + 20

# Row 1: Python Scripts (two source boxes side by side)
R1_Y = 85
SRC_W = 160

rect(
    "py_excali",
    COL_LEFT_X,
    R1_Y,
    SRC_W,
    BH,
    *BLUE,
    bnd=[{"id": "t_py_excali", "type": "text"}],
)
txt("t_py_excali", COL_LEFT_X, R1_Y, SRC_W, BH, "Python\nScripts", 20, cid="py_excali")

rect(
    "py_aws",
    COL_RIGHT_X,
    R1_Y,
    SRC_W,
    BH,
    *BLUE,
    bnd=[{"id": "t_py_aws", "type": "text"}],
)
txt("t_py_aws", COL_RIGHT_X, R1_Y, SRC_W, BH, "Python\nScripts", 20, cid="py_aws")

# Row 2: Intermediate outputs
R2_Y = R1_Y + BH + GAP_V

rect(
    "excali_json",
    COL_LEFT_X,
    R2_Y,
    SRC_W,
    BH,
    *PURPLE,
    bnd=[{"id": "t_excali_json", "type": "text"}],
)
txt(
    "t_excali_json",
    COL_LEFT_X,
    R2_Y,
    SRC_W,
    BH,
    ".excalidraw\nJSON",
    20,
    cid="excali_json",
)

rect(
    "diagrams_lib",
    COL_RIGHT_X,
    R2_Y,
    SRC_W,
    BH,
    *YELLOW,
    bnd=[{"id": "t_diagrams_lib", "type": "text"}],
)
txt(
    "t_diagrams_lib",
    COL_RIGHT_X,
    R2_Y,
    SRC_W,
    BH,
    "diagrams\nlibrary",
    20,
    cid="diagrams_lib",
)

# Row 3: Export tools
R3_Y = R2_Y + BH + GAP_V

rect(
    "brute_export",
    COL_LEFT_X,
    R3_Y,
    SRC_W,
    BH,
    *CYAN,
    bnd=[{"id": "t_brute_export", "type": "text"}],
)
txt(
    "t_brute_export",
    COL_LEFT_X,
    R3_Y,
    SRC_W,
    BH,
    "brute-export\nCLI",
    20,
    cid="brute_export",
)

# Row 4: Output formats
R4_Y = R3_Y + BH + GAP_V

rect(
    "svg_out",
    COL_LEFT_X,
    R4_Y,
    SRC_W,
    BH,
    *GREEN,
    bnd=[{"id": "t_svg_out", "type": "text"}],
)
txt("t_svg_out", COL_LEFT_X, R4_Y, SRC_W, BH, "SVG\nlight + dark", 20, cid="svg_out")

rect(
    "png_out",
    COL_RIGHT_X,
    R4_Y,
    SRC_W,
    BH,
    *GREEN,
    bnd=[{"id": "t_png_out", "type": "text"}],
)
txt("t_png_out", COL_RIGHT_X, R4_Y, SRC_W, BH, "PNG\nlight + dark", 20, cid="png_out")

# Row 5: Final output (centered)
R5_Y = R4_Y + BH + GAP_V
OUT_X = (CANVAS_W - 200) // 2

rect(
    "public_dir",
    OUT_X,
    R5_Y,
    200,
    BH,
    *GRAY,
    bnd=[{"id": "t_public_dir", "type": "text"}],
)
txt(
    "t_public_dir",
    OUT_X,
    R5_Y,
    200,
    BH,
    "public/images/\ndiagrams/",
    20,
    cid="public_dir",
)

# Column labels
txt("lbl_excali", COL_LEFT_X, R1_Y - 30, SRC_W, 25, "Excalidraw", 19, color=PURPLE[0])
txt(
    "lbl_aws",
    COL_RIGHT_X,
    R1_Y - 30,
    SRC_W,
    25,
    "AWS Architecture",
    19,
    color=YELLOW[0],
)

# === ARROWS ===
LEFT_CX = COL_LEFT_X + SRC_W // 2
RIGHT_CX = COL_RIGHT_X + SRC_W // 2
OUT_CX = OUT_X + 100

# Left column: py → json → export → svg
arr(
    "a1",
    LEFT_CX,
    R1_Y + BH,
    [[0, 0], [0, GAP_V]],
    BLUE[0],
    sb={"elementId": "py_excali", "focus": 0, "gap": 4},
    eb={"elementId": "excali_json", "focus": 0, "gap": 4},
)

arr(
    "a2",
    LEFT_CX,
    R2_Y + BH,
    [[0, 0], [0, GAP_V]],
    PURPLE[0],
    sb={"elementId": "excali_json", "focus": 0, "gap": 4},
    eb={"elementId": "brute_export", "focus": 0, "gap": 4},
)

arr(
    "a3",
    LEFT_CX,
    R3_Y + BH,
    [[0, 0], [0, GAP_V]],
    CYAN[0],
    sb={"elementId": "brute_export", "focus": 0, "gap": 4},
    eb={"elementId": "svg_out", "focus": 0, "gap": 4},
)

# Right column: py → diagrams lib → png
arr(
    "a4",
    RIGHT_CX,
    R1_Y + BH,
    [[0, 0], [0, GAP_V]],
    BLUE[0],
    sb={"elementId": "py_aws", "focus": 0, "gap": 4},
    eb={"elementId": "diagrams_lib", "focus": 0, "gap": 4},
)

arr(
    "a5",
    RIGHT_CX,
    R2_Y + BH,
    [[0, 0], [0, R4_Y - R2_Y - BH]],
    YELLOW[0],
    sb={"elementId": "diagrams_lib", "focus": 0, "gap": 4},
    eb={"elementId": "png_out", "focus": 0, "gap": 4},
)

# SVG → public
arr(
    "a6",
    LEFT_CX,
    R4_Y + BH,
    [[0, 0], [OUT_CX - LEFT_CX, GAP_V]],
    GREEN[0],
    sb={"elementId": "svg_out", "focus": 0, "gap": 4},
    eb={"elementId": "public_dir", "focus": 0, "gap": 4},
)

# PNG → public
arr(
    "a7",
    RIGHT_CX,
    R4_Y + BH,
    [[0, 0], [OUT_CX - RIGHT_CX, GAP_V]],
    GREEN[0],
    sb={"elementId": "png_out", "focus": 0, "gap": 4},
    eb={"elementId": "public_dir", "focus": 0, "gap": 4},
)


# === WRITE FILE ===
outfile = "diagrams/artifacts/readme-diagram-pipeline.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
