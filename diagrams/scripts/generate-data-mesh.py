"""Generate Data Mesh Principles diagram: 2x2 grid."""

import sys

from diagramlib import BLUE, GREEN, PURPLE, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=4000)

# === LAYOUT ===
CW = 620
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X
BOX_W = (CONTENT_W - 30) // 2  # 2 columns with 30px gap
BOX_H = 130
COL_GAP = 30
ROW_GAP = 30

# Title
d.txt("title", PAD_X, 25, CONTENT_W, 40, "Data Mesh Principles", 32)

# 2x2 grid
grid = [
    [
        (
            "domain",
            "Domain\nOwnership",
            "Each domain owns and\nserves its own data",
            BLUE,
        ),
        (
            "product",
            "Data as\na Product",
            "Domains publish data\nwith SLAs and docs",
            GREEN,
        ),
    ],
    [
        (
            "platform",
            "Self-Serve\nPlatform",
            "Shared infrastructure\nfor all domains",
            PURPLE,
        ),
        (
            "governance",
            "Federated\nGovernance",
            "Global standards,\nlocal autonomy",
            YELLOW,
        ),
    ],
]

START_Y = 90
for row_i, row in enumerate(grid):
    for col_i, (pid, title, subtitle, color) in enumerate(row):
        bx = PAD_X + col_i * (BOX_W + COL_GAP)
        by = START_Y + row_i * (BOX_H + ROW_GAP)
        d.rect(
            pid,
            bx,
            by,
            BOX_W,
            BOX_H,
            *color,
            opacity=20,
            bnd=[{"id": f"{pid}_title", "type": "text"}],
        )
        d.txt(f"{pid}_title", bx, by, BOX_W, 60, title, 22, cid=pid)
        d.txt(f"{pid}_sub", bx, by + 70, BOX_W, 50, subtitle, 17, color=color[0])

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/data-mesh"
outfile = f"diagrams/artifacts/artifacts/{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
