"""
Generate modeling approaches comparison diagram showing
Inmon, Kimball, Data Vault, and One Big Table side by side.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, GRAY

d = ExcalidrawDiagram(seed=8000)

# === LAYOUT ===
CANVAS_W = 700
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 12
COL_W = (CONTENT_W - 3 * COL_GAP) // 4

TITLE_Y = 15
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Data Modeling Approaches", 30, color="#1e1e1e")

approaches = [
    ("inmon", "Inmon", "3NF in warehouse\n→ Star schema\ndata marts", "Data quality\nfirst", BLUE),
    ("kimball", "Kimball", "Star schemas\ndirectly in\nwarehouse", "Fast insights\nand iteration", GREEN),
    ("vault", "Data Vault", "Hubs + Links\n+ Satellites\nseparated", "Flexibility\nand auditability", PURPLE),
    ("obt", "One Big Table", "Single wide\ndenormalized\ntable", "Simple queries\nno joins", YELLOW),
]

BOX_H = 130
y = TITLE_Y + TITLE_H + 25

for i, (bid, title, desc, focus, color) in enumerate(approaches):
    x = PAD_X + i * (COL_W + COL_GAP)
    d.rect(bid, x, y, COL_W, BOX_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    title_h = math.ceil(1 * 22 * 1.25)
    desc_lines = desc.count("\n") + 1
    desc_h = math.ceil(desc_lines * 16 * 1.25)
    gap = 6
    combined = title_h + gap + desc_h
    top_pad = (BOX_H - combined) // 2

    d.txt(f"{bid}_t", x, y + top_pad, COL_W, title_h,
        title, 22, cid=bid)
    d.txt(f"{bid}_desc", x, y + top_pad + title_h + gap, COL_W, desc_h,
        desc, 16, color=color[0])

# Focus row below
FOCUS_Y = y + BOX_H + 15
FOCUS_H = 60

for i, (bid, title, desc, focus, color) in enumerate(approaches):
    x = PAD_X + i * (COL_W + COL_GAP)
    fid = f"{bid}_focus"
    d.rect(fid, x, FOCUS_Y, COL_W, FOCUS_H, *color, opacity=60,
         bnd=[{"id": f"{fid}_t", "type": "text"}])

    focus_lines = focus.count("\n") + 1
    focus_h = math.ceil(focus_lines * 16 * 1.25)
    d.txt(f"{fid}_t", x, FOCUS_Y, COL_W, FOCUS_H,
        focus, 16, cid=fid)

# Focus label
FLABEL_Y = FOCUS_Y + FOCUS_H + 6
FLABEL_H = math.ceil(1 * 15 * 1.25)
d.txt("focus_label", PAD_X, FLABEL_Y, CONTENT_W, FLABEL_H,
    "Primary Focus", 15, color=GRAY[0])

print(f"Canvas: {CANVAS_W}x{FLABEL_Y + FLABEL_H + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "modeling-approaches"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
