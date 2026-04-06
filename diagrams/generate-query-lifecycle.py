"""
Generate query lifecycle diagram showing the stages a batch query
travels through within a DBMS.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GRAY, GREEN, PURPLE, YELLOW

d = ExcalidrawDiagram(seed=5000)

# === LAYOUT ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X
BOX_W = CONTENT_W
BOX_H = 95  # title + subtitle
ARROW_GAP = 15

TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "The Life of a Query", 32, color="#1e1e1e")

stages = [
    ("transport", "Transport Layer", "Client issues SQL query\nover network connection", GRAY),
    ("parser", "Query Parser", "Tokenize → syntax check →\naccess control → compile to bytecode", BLUE),
    ("optimizer", "Query Optimizer", "Evaluate candidate plans →\ncalculate cost → pick cheapest", YELLOW),
    ("engine", "Execution Engine", "Execute chosen plan\nagainst storage", GREEN),
    ("storage", "Storage Engine", "Read/write data blocks\nreturn results", PURPLE),
]

y = TITLE_Y + TITLE_H + 30

for i, (bid, title, sub, color) in enumerate(stages):
    d.rect(bid, PAD_X, y, BOX_W, BOX_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    title_h = math.ceil(1 * 24 * 1.25)
    sub_h = math.ceil(2 * 17 * 1.25)
    gap = 6
    combined = title_h + gap + sub_h
    top_pad = (BOX_H - combined) // 2

    d.txt(f"{bid}_t", PAD_X, y + top_pad, BOX_W, title_h,
        title, 24, cid=bid)
    d.txt(f"{bid}_sub", PAD_X, y + top_pad + title_h + gap, BOX_W, sub_h,
        sub, 17, color=color[0])

    if i < len(stages) - 1:
        d.arr(f"a{i}", PAD_X + BOX_W // 2, y + BOX_H,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": stages[i + 1][0], "focus": 0, "gap": 4})

    y += BOX_H + ARROW_GAP

print(f"Canvas: {CANVAS_W}x{y + 10}")

name = sys.argv[1] if len(sys.argv) > 1 else "query-lifecycle"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
