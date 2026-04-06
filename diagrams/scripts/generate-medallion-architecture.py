"""Generate Medallion Architecture diagram: Bronze → Silver → Gold."""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, YELLOW, GRAY

d = ExcalidrawDiagram(seed=2000)

# === LAYOUT ===
CW = 700
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X

# Title
d.txt("title", PAD_X, 25, CONTENT_W, 40, "Medallion Architecture", 32)

# Three boxes horizontally
BOX_W = 175
BOX_H = 160
BOX_Y = 90
GAP = 35
total_w = 3 * BOX_W + 2 * GAP
start_x = (CW - total_w) // 2

layers = [
    ("bronze", start_x, "Bronze", "Raw Ingestion", "Exact copy of\nsource data", GRAY),
    (
        "silver",
        start_x + BOX_W + GAP,
        "Silver",
        "Cleaned &\nConformed",
        "Deduplicated,\ntyped, validated",
        BLUE,
    ),
    (
        "gold",
        start_x + 2 * (BOX_W + GAP),
        "Gold",
        "Business-Level",
        "Aggregated,\nmodeled, served",
        YELLOW,
    ),
]

for lid, lx, title, subtitle, desc, color in layers:
    d.rect(
        f"{lid}_box",
        lx,
        BOX_Y,
        BOX_W,
        BOX_H,
        *color,
        fill="hachure",
        opacity=25,
        bnd=[{"id": f"{lid}_title", "type": "text"}],
    )
    d.txt(f"{lid}_title", lx, BOX_Y, BOX_W, 50, title, 24, cid=f"{lid}_box")
    d.txt(f"{lid}_sub", lx, BOX_Y + 45, BOX_W, 30, subtitle, 17, color=color[0])
    d.txt(f"{lid}_desc", lx, BOX_Y + 100, BOX_W, 50, desc, 16, color=color[0], op=70)

# Arrows between boxes
for i, (lid, lx, *_) in enumerate(layers[:-1]):
    next_x = layers[i + 1][1]
    ax = lx + BOX_W
    ay = BOX_Y + BOX_H // 2
    d.arr(
        f"arr_{i}",
        ax,
        ay,
        [[0, 0], [GAP, 0]],
        layers[i][5][0],
        sb={"elementId": f"{lid}_box", "focus": 0, "gap": 4},
        eb={"elementId": f"{layers[i + 1][0]}_box", "focus": 0, "gap": 4},
    )

# Storage layer beneath
STORAGE_Y = BOX_Y + BOX_H + 50
STORAGE_H = 50
d.rect(
    "storage",
    start_x - 10,
    STORAGE_Y,
    total_w + 20,
    STORAGE_H,
    *GRAY,
    fill="hachure",
    opacity=10,
    dashed=True,
    bnd=[{"id": "storage_t", "type": "text"}],
)
d.txt(
    "storage_t",
    start_x - 10,
    STORAGE_Y,
    total_w + 20,
    STORAGE_H,
    "Object Storage (S3)",
    20,
    color=GRAY[0],
    cid="storage",
)

# Dashed arrows from each box to storage
for lid, lx, *_ in layers:
    d.arr(
        f"store_{lid}",
        lx + BOX_W // 2,
        BOX_Y + BOX_H,
        [[0, 0], [0, 50]],
        GRAY[0],
        dash=True,
        op=40,
    )

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/medallion-architecture"
d.save(f"diagrams/artifacts/artifacts/{name}.excalidraw")
print(f"Wrote diagrams/{name}.excalidraw")
