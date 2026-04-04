"""
Generate ML lifecycle diagram showing the four stages
with the data engineer's role highlighted.
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
seed = 12000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
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
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Machine Learning Lifecycle", 30, color="#1e1e1e")

BOX_W = CONTENT_W
BOX_H = 85
ARROW_GAP = 18

stages = [
    ("scope", "1. Scoping", "Define project goals\nand success criteria", GRAY, False),
    ("data", "2. Data", "Define requirements, label,\norganize — data engineer focus", BLUE, True),
    ("algo", "3. Algorithm Development", "Train/test split → train →\ncross-validate → iterate", YELLOW, False),
    ("deploy", "4. Deployment", "Productionize model, monitor,\nserve data for retraining", GREEN, True),
]

y = TITLE_Y + TITLE_H + 20

for i, (bid, title, desc, color, is_de) in enumerate(stages):
    rect(bid, PAD_X, y, BOX_W, BOX_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    title_h = math.ceil(1 * 22 * 1.25)
    desc_lines = desc.count("\n") + 1
    desc_h = math.ceil(desc_lines * 16 * 1.25)
    gap = 5
    combined = title_h + gap + desc_h
    top_pad = (BOX_H - combined) // 2

    txt(f"{bid}_t", PAD_X, y + top_pad, BOX_W, title_h, title, 22, cid=bid)
    txt(f"{bid}_sub", PAD_X, y + top_pad + title_h + gap, BOX_W, desc_h,
        desc, 16, color=color[0])

    # Data engineer badge
    if is_de:
        badge_w = 110
        badge_h = 22
        badge_x = PAD_X + BOX_W - badge_w - 8
        badge_y = y + 5
        rect(f"{bid}_badge", badge_x, badge_y, badge_w, badge_h,
             PURPLE[0], PURPLE[1], bnd=[{"id": f"{bid}_badge_t", "type": "text"}])
        txt(f"{bid}_badge_t", badge_x, badge_y, badge_w, badge_h,
            "DE role", 14, cid=f"{bid}_badge")

    if i < len(stages) - 1:
        arr(f"a{i}", PAD_X + BOX_W // 2, y + BOX_H,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": stages[i + 1][0], "focus": 0, "gap": 4})

    y += BOX_H + ARROW_GAP

print(f"Canvas: {CANVAS_W}x{y + 5}")

name = sys.argv[1] if len(sys.argv) > 1 else "ml-lifecycle"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
