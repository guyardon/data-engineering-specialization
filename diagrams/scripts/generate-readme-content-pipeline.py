"""Generate Excalidraw diagram: Content Pipeline architecture for README."""

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
seed = 1000


def ns():
    global seed
    seed += 1
    return seed


# === COLOR PALETTE ===
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
BW = 160  # box width
BH = 70  # box height
GAP_H = 80  # horizontal gap between boxes
GAP_V = 80  # vertical gap between rows

# Title
txt("title", 0, 15, CANVAS_W, 40, "Content Pipeline", 32)

# Row 1: Notion → fetch-notion.mjs → Markdown
R1_Y = 80
# 3 boxes evenly across: calculate spacing
TOTAL_BOX_W = 3 * BW
TOTAL_GAP = CONTENT_W - TOTAL_BOX_W
GAP_BETWEEN = TOTAL_GAP // 2

B1_X = PAD_X
B2_X = B1_X + BW + GAP_BETWEEN
B3_X = B2_X + BW + GAP_BETWEEN

rect("notion", B1_X, R1_Y, BW, BH, *PURPLE, bnd=[{"id": "t_notion", "type": "text"}])
txt("t_notion", B1_X, R1_Y, BW, BH, "Notion", 22, cid="notion")

rect("fetch", B2_X, R1_Y, BW, BH, *BLUE, bnd=[{"id": "t_fetch", "type": "text"}])
txt("t_fetch", B2_X, R1_Y, BW, BH, "fetch-notion\n.mjs", 20, cid="fetch")

rect("md", B3_X, R1_Y, BW, BH, *GREEN, bnd=[{"id": "t_md", "type": "text"}])
txt("t_md", B3_X, R1_Y, BW, BH, "Markdown\nFiles", 22, cid="md")

# Row 2: Astro Build (centered)
R2_Y = R1_Y + BH + GAP_V
ASTRO_X = (CANVAS_W - BW) // 2

rect("astro", ASTRO_X, R2_Y, BW, BH, *YELLOW, bnd=[{"id": "t_astro", "type": "text"}])
txt("t_astro", ASTRO_X, R2_Y, BW, BH, "Astro Build", 22, cid="astro")

# Row 3: Pagefind Index (centered)
R3_Y = R2_Y + BH + GAP_V

rect(
    "pagefind", ASTRO_X, R3_Y, BW, BH, *CYAN, bnd=[{"id": "t_pagefind", "type": "text"}]
)
txt("t_pagefind", ASTRO_X, R3_Y, BW, BH, "Pagefind\nIndex", 22, cid="pagefind")

# Row 4: GitHub Pages (centered)
R4_Y = R3_Y + BH + GAP_V

rect("ghpages", ASTRO_X, R4_Y, BW, BH, *GRAY, bnd=[{"id": "t_ghpages", "type": "text"}])
txt("t_ghpages", ASTRO_X, R4_Y, BW, BH, "GitHub\nPages", 22, cid="ghpages")

# Arrows
# Notion → fetch
arr(
    "a1",
    B1_X + BW,
    R1_Y + BH // 2,
    [[0, 0], [GAP_BETWEEN, 0]],
    PURPLE[0],
    sb={"elementId": "notion", "focus": 0, "gap": 4},
    eb={"elementId": "fetch", "focus": 0, "gap": 4},
)

# fetch → Markdown
arr(
    "a2",
    B2_X + BW,
    R1_Y + BH // 2,
    [[0, 0], [GAP_BETWEEN, 0]],
    BLUE[0],
    sb={"elementId": "fetch", "focus": 0, "gap": 4},
    eb={"elementId": "md", "focus": 0, "gap": 4},
)

# Markdown → Astro Build
MD_CX = B3_X + BW // 2
ASTRO_CX = ASTRO_X + BW // 2
arr(
    "a3",
    MD_CX,
    R1_Y + BH,
    [[0, 0], [ASTRO_CX - MD_CX, GAP_V]],
    GREEN[0],
    sb={"elementId": "md", "focus": 0, "gap": 4},
    eb={"elementId": "astro", "focus": 0, "gap": 4},
)

# Astro → Pagefind
arr(
    "a4",
    ASTRO_CX,
    R2_Y + BH,
    [[0, 0], [0, GAP_V]],
    YELLOW[0],
    sb={"elementId": "astro", "focus": 0, "gap": 4},
    eb={"elementId": "pagefind", "focus": 0, "gap": 4},
)

# Pagefind → GitHub Pages
arr(
    "a5",
    ASTRO_CX,
    R3_Y + BH,
    [[0, 0], [0, GAP_V]],
    CYAN[0],
    sb={"elementId": "pagefind", "focus": 0, "gap": 4},
    eb={"elementId": "ghpages", "focus": 0, "gap": 4},
)


# === WRITE FILE ===
outfile = "diagrams/artifacts/readme-content-pipeline.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
