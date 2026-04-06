"""
Generate B-Tree index diagram showing how tree traversal achieves
O(log n) lookup vs O(n) sequential scan.
"""

import math
import sys

from diagramlib import BLUE, GRAY, GREEN, RED, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=9000)

# === LAYOUT ===
CANVAS_W = 680
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 15
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "B-Tree Index vs Sequential Scan",
    30,
    color="#1e1e1e",
)

# === LEFT SIDE: Sequential Scan ===
LEFT_W = (CONTENT_W - 30) // 2
RIGHT_X = PAD_X + LEFT_W + 30

# Section labels
SEC_Y = TITLE_Y + TITLE_H + 20
SEC_H = math.ceil(1 * 20 * 1.25)
d.txt(
    "seq_label", PAD_X, SEC_Y, LEFT_W, SEC_H, "Sequential Scan — O(n)", 20, color=RED[0]
)
d.txt(
    "idx_label",
    RIGHT_X,
    SEC_Y,
    LEFT_W,
    SEC_H,
    "B-Tree Index — O(log n)",
    20,
    color=GREEN[0],
)

# === Sequential scan: 8 rows, highlight searching through all ===
ROW_H = 38
ROW_GAP = 4
ROW_W = LEFT_W - 20
ROW_X = PAD_X + 10
ROW_START_Y = SEC_Y + SEC_H + 15

rows = ["id=1", "id=3", "id=5", "id=7", "id=9", "id=11", "id=13", "id=15"]
target = "id=13"  # what we're searching for

for i, val in enumerate(rows):
    y = ROW_START_Y + i * (ROW_H + ROW_GAP)
    is_target = val == target
    color = GREEN if is_target else GRAY
    opacity = 100 if is_target else 50
    bid = f"row{i}"
    d.rect(
        bid,
        ROW_X,
        y,
        ROW_W,
        ROW_H,
        *color,
        opacity=opacity,
        bnd=[{"id": f"{bid}_t", "type": "text"}],
    )
    d.txt(f"{bid}_t", ROW_X, y, ROW_W, ROW_H, val, 18, cid=bid, op=opacity)

    # Arrow showing scan direction (down the left side)
    if i < len(rows) - 1 and not is_target:
        d.arr(
            f"scan{i}",
            ROW_X - 12,
            y + ROW_H // 2,
            [[0, 0], [0, ROW_H + ROW_GAP]],
            RED[0],
            op=40,
        )

# "Scans 7 rows" label
SCAN_BOTTOM = ROW_START_Y + len(rows) * (ROW_H + ROW_GAP)
SCAN_LABEL_Y = SCAN_BOTTOM + 5
SCAN_LABEL_H = math.ceil(1 * 16 * 1.25)
d.txt(
    "scan_count",
    PAD_X,
    SCAN_LABEL_Y,
    LEFT_W,
    SCAN_LABEL_H,
    "Checks 7 rows to find id=13",
    16,
    color=RED[0],
)

# === RIGHT SIDE: B-Tree with 3 levels ===
NODE_W = 90
NODE_H = 40
LEVEL_GAP = 55

# Root
ROOT_X = RIGHT_X + (LEFT_W - NODE_W) // 2
ROOT_Y = ROW_START_Y + 10
d.rect(
    "root",
    ROOT_X,
    ROOT_Y,
    NODE_W,
    NODE_H,
    *BLUE,
    bnd=[{"id": "root_t", "type": "text"}],
)
d.txt("root_t", ROOT_X, ROOT_Y, NODE_W, NODE_H, "[7 | 11]", 18, cid="root")

# Level 2: two internal nodes
L2_Y = ROOT_Y + NODE_H + LEVEL_GAP
L2_LEFT_X = RIGHT_X + 15
L2_RIGHT_X = RIGHT_X + LEFT_W - NODE_W - 15

# Left internal (unhighlighted)
d.rect(
    "int_l",
    L2_LEFT_X,
    L2_Y,
    NODE_W,
    NODE_H,
    *GRAY,
    opacity=50,
    bnd=[{"id": "int_l_t", "type": "text"}],
)
d.txt("int_l_t", L2_LEFT_X, L2_Y, NODE_W, NODE_H, "[1 | 3 | 5]", 16, cid="int_l", op=50)

# Right internal (highlighted path)
d.rect(
    "int_r",
    L2_RIGHT_X,
    L2_Y,
    NODE_W,
    NODE_H,
    *BLUE,
    bnd=[{"id": "int_r_t", "type": "text"}],
)
d.txt("int_r_t", L2_RIGHT_X, L2_Y, NODE_W, NODE_H, "[11 | 13 | 15]", 16, cid="int_r")

# Arrows root -> children
d.arr(
    "a_root_l",
    ROOT_X + NODE_W // 2,
    ROOT_Y + NODE_H,
    [[0, 0], [L2_LEFT_X + NODE_W // 2 - ROOT_X - NODE_W // 2, LEVEL_GAP]],
    GRAY[0],
    op=40,
    sb={"elementId": "root", "focus": 0, "gap": 4},
    eb={"elementId": "int_l", "focus": 0, "gap": 4},
)

d.arr(
    "a_root_r",
    ROOT_X + NODE_W // 2,
    ROOT_Y + NODE_H,
    [[0, 0], [L2_RIGHT_X + NODE_W // 2 - ROOT_X - NODE_W // 2, LEVEL_GAP]],
    GREEN[0],
    sb={"elementId": "root", "focus": 0, "gap": 4},
    eb={"elementId": "int_r", "focus": 0, "gap": 4},
)

# Level 3: leaf node with the result
L3_Y = L2_Y + NODE_H + LEVEL_GAP
LEAF_X = RIGHT_X + (LEFT_W - NODE_W) // 2

d.rect(
    "leaf", LEAF_X, L3_Y, NODE_W, NODE_H, *GREEN, bnd=[{"id": "leaf_t", "type": "text"}]
)
d.txt("leaf_t", LEAF_X, L3_Y, NODE_W, NODE_H, "id=13 ✓", 18, cid="leaf")

d.arr(
    "a_int_leaf",
    L2_RIGHT_X + NODE_W // 2,
    L2_Y + NODE_H,
    [[0, 0], [LEAF_X + NODE_W // 2 - L2_RIGHT_X - NODE_W // 2, LEVEL_GAP]],
    GREEN[0],
    sb={"elementId": "int_r", "focus": 0, "gap": 4},
    eb={"elementId": "leaf", "focus": 0, "gap": 4},
)

# "3 steps" label
IDX_LABEL_Y = L3_Y + NODE_H + 15
IDX_LABEL_H = math.ceil(1 * 16 * 1.25)
d.txt(
    "idx_count",
    RIGHT_X,
    IDX_LABEL_Y,
    LEFT_W,
    IDX_LABEL_H,
    "3 steps to find id=13",
    16,
    color=GREEN[0],
)

# === VERIFY ===
bottom = max(SCAN_LABEL_Y + SCAN_LABEL_H, IDX_LABEL_Y + IDX_LABEL_H) + 20
print(f"Canvas: {CANVAS_W}x{bottom}")

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/btree-index"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
