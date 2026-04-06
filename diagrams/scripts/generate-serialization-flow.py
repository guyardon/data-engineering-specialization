"""
Serialization and compression flow diagram.
Shows: In-memory Format -> Serialize -> Disk Format -> Compress -> Storage-efficient Format
Then fan-out to: File, Database, Network

Vertical flow with fan-out at the bottom. Canvas: 650px wide.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, CYAN, GRAY, GREEN, PURPLE, YELLOW

d = ExcalidrawDiagram(seed=4000)

# === LAYOUT ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 250  # main box width
BH = 65  # main box height
ARROW_V = 70  # vertical arrow gap
SMALL_BW = 150
SMALL_BH = 50

# Center X for main flow
CX = CANVAS_W // 2
BOX_X = CX - BW // 2

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Serialization & Compression", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "From in-memory data structures to persistent storage",
    17,
    color=BLUE[0],
)

# === BOX 1: In-memory Format ===
B1_Y = 90
d.rect(
    "b1", BOX_X, B1_Y, BW, BH, *BLUE, fill="hachure", bnd=[{"id": "t1", "type": "text"}]
)
d.txt("t1", BOX_X, B1_Y, BW, BH, "In-Memory Format\n(CPU-optimized)", 20, cid="b1")

# Arrow B1 -> B2
d.arr(
    "a12",
    CX,
    B1_Y + BH,
    [[0, 0], [0, ARROW_V]],
    BLUE[0],
    sb={"elementId": "b1", "focus": 0, "gap": 4},
    eb={"elementId": "b2", "focus": 0, "gap": 4},
)
# Label: Serialize
d.txt("l_ser", CX + 10, B1_Y + BH + 20, 80, 25, "Serialize", 17, color=BLUE[0])

# === BOX 2: Disk Format ===
B2_Y = B1_Y + BH + ARROW_V
d.rect(
    "b2",
    BOX_X,
    B2_Y,
    BW,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "t2", "type": "text"}],
)
d.txt("t2", BOX_X, B2_Y, BW, BH, "Disk Format\n(01001010...)", 20, cid="b2")

# Arrow B2 -> B3
d.arr(
    "a23",
    CX,
    B2_Y + BH,
    [[0, 0], [0, ARROW_V]],
    GREEN[0],
    sb={"elementId": "b2", "focus": 0, "gap": 4},
    eb={"elementId": "b3", "focus": 0, "gap": 4},
)
# Label: Compress
d.txt("l_cmp", CX + 10, B2_Y + BH + 20, 80, 25, "Compress", 17, color=GREEN[0])

# === BOX 3: Storage-efficient Format ===
B3_Y = B2_Y + BH + ARROW_V
d.rect(
    "b3",
    BOX_X,
    B3_Y,
    BW,
    BH,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "t3", "type": "text"}],
)
d.txt("t3", BOX_X, B3_Y, BW, BH, "Storage-Efficient\nFormat", 20, cid="b3")

# === Fan-out to 3 destinations ===
FAN_Y = B3_Y + BH + ARROW_V + 10
FAN_GAP = 20
# Three small boxes in a row
fan_labels = ["File", "Database", "Network"]
fan_colors = [CYAN, YELLOW, GRAY]
total_fan_w = 3 * SMALL_BW + 2 * FAN_GAP
fan_start_x = CX - total_fan_w // 2

for i, (label, color) in enumerate(zip(fan_labels, fan_colors)):
    fx = fan_start_x + i * (SMALL_BW + FAN_GAP)
    fid = f"fan{i}"
    ftid = f"fant{i}"
    d.rect(
        fid,
        fx,
        FAN_Y,
        SMALL_BW,
        SMALL_BH,
        *color,
        fill="hachure",
        bnd=[{"id": ftid, "type": "text"}],
    )
    d.txt(ftid, fx, FAN_Y, SMALL_BW, SMALL_BH, label, 20, cid=fid)

    # Arrow from B3 center to each fan box
    dx = fx + SMALL_BW // 2 - CX
    dy = FAN_Y - (B3_Y + BH)
    d.arr(
        f"afan{i}",
        CX,
        B3_Y + BH,
        [[0, 0], [dx, dy]],
        PURPLE[0],
        dash=True,
        sb={"elementId": "b3", "focus": 0, "gap": 4},
        eb={"elementId": fid, "focus": 0, "gap": 4},
    )

# === Reverse arrow label (De-serialize) on the left ===
d.txt(
    "l_deser",
    BOX_X - 110,
    B1_Y + BH + 20,
    100,
    25,
    "De-serialize",
    16,
    color=GRAY[0],
    op=70,
)
d.arr(
    "a_deser",
    CX - BW // 2 - 15,
    B2_Y,
    [[0, 0], [0, -ARROW_V]],
    GRAY[0],
    dash=True,
    op=50,
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/serialization-flow"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
