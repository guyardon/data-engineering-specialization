"""
DBMS Architecture diagram.
Vertical stack showing the 4 layers of a database management system:
  Client Application → Transport System → Query Processor → Execution Engine → Storage Engine

Canvas: 600px wide (narrow for vertical).
"""

import sys

from diagramlib import BLUE, CYAN, GRAY, GREEN, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=8000)

# === LAYOUT ===
CANVAS_W = 600
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 300  # box width (Rule 24: derived from canvas)
BH = 70  # box height
ARROW_GAP = 70  # Rule 17
BOX_X = PAD_X + (CONTENT_W - BW) // 2

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "DBMS Architecture", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Layers of a database management system",
    17,
    color=BLUE[0],
)

# === Layers (top to bottom) ===
layers = [
    ("client", "Client Application", "SQL queries, API calls", GRAY),
    ("transport", "Transport System", "Handles client connections", CYAN),
    ("query", "Query Processor", "Parses & optimizes queries", BLUE),
    ("exec", "Execution Engine", "Runs the query plan", GREEN),
    ("storage", "Storage Engine", "Serialization, disk layout, indexes", YELLOW),
]

START_Y = 90

for i, (lid, title, subtitle, color) in enumerate(layers):
    by = START_Y + i * (BH + ARROW_GAP)

    d.rect(
        lid,
        BOX_X,
        by,
        BW,
        BH,
        *color,
        fill="hachure",
        bnd=[{"id": f"{lid}_t", "type": "text"}],
    )
    # Rule 13: title + subtitle
    d.txt(f"{lid}_t", BOX_X, by, BW, BH, f"{title}\n{subtitle}", 18, cid=lid)

    # Arrow to next layer (except last)
    if i < len(layers) - 1:
        d.arr(
            f"a_{i}",
            BOX_X + BW // 2,
            by + BH,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": lid, "focus": 0, "gap": 4},
            eb={"elementId": layers[i + 1][0], "focus": 0, "gap": 4},
        )

# Disk icon at the bottom (simple rect)
DISK_Y = START_Y + len(layers) * (BH + ARROW_GAP) - ARROW_GAP + BH + 15
DISK_W = 160
DISK_H = 50
DISK_X = BOX_X + (BW - DISK_W) // 2
d.rect(
    "disk",
    DISK_X,
    DISK_Y,
    DISK_W,
    DISK_H,
    *GRAY,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "disk_t", "type": "text"}],
)
d.txt("disk_t", DISK_X, DISK_Y, DISK_W, DISK_H, "Disk (SSD / HDD)", 17, cid="disk")

# Arrow storage → disk
d.arr(
    "a_disk",
    BOX_X + BW // 2,
    DISK_Y - 15,
    [[0, 0], [0, 15]],
    YELLOW[0],
    dash=True,
    sb={"elementId": "storage", "focus": 0, "gap": 4},
    eb={"elementId": "disk", "focus": 0, "gap": 4},
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/dbms-architecture"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
