"""
Generate ML lifecycle diagram showing the four stages
with the data engineer's role highlighted.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=12000)

CANVAS_W = 660
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
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
    d.rect(bid, PAD_X, y, BOX_W, BOX_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    title_h = math.ceil(1 * 22 * 1.25)
    desc_lines = desc.count("\n") + 1
    desc_h = math.ceil(desc_lines * 16 * 1.25)
    gap = 5
    combined = title_h + gap + desc_h
    top_pad = (BOX_H - combined) // 2

    d.txt(f"{bid}_t", PAD_X, y + top_pad, BOX_W, title_h, title, 22, cid=bid)
    d.txt(f"{bid}_sub", PAD_X, y + top_pad + title_h + gap, BOX_W, desc_h,
        desc, 16, color=color[0])

    # Data engineer badge
    if is_de:
        badge_w = 110
        badge_h = 22
        badge_x = PAD_X + BOX_W - badge_w - 8
        badge_y = y + 5
        d.rect(f"{bid}_badge", badge_x, badge_y, badge_w, badge_h,
             PURPLE[0], PURPLE[1], bnd=[{"id": f"{bid}_badge_t", "type": "text"}])
        d.txt(f"{bid}_badge_t", badge_x, badge_y, badge_w, badge_h,
            "DE role", 14, cid=f"{bid}_badge")

    if i < len(stages) - 1:
        d.arr(f"a{i}", PAD_X + BOX_W // 2, y + BOX_H,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": stages[i + 1][0], "focus": 0, "gap": 4})

    y += BOX_H + ARROW_GAP

print(f"Canvas: {CANVAS_W}x{y + 5}")

name = sys.argv[1] if len(sys.argv) > 1 else "ml-lifecycle"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
