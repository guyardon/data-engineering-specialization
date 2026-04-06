"""
Replication vs Partitioning diagram.
Two columns side by side:
  Left: Replication — same data copied to all 3 nodes
  Right: Partitioning — data split into disjoint subsets across 3 nodes

Canvas: 650px wide.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GRAY, GREEN, PURPLE

d = ExcalidrawDiagram(seed=6000)

# === LAYOUT ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
INNER_PAD = 25
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Replication vs Partitioning", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Two strategies for distributing data across nodes",
    17,
    color=BLUE[0],
)

# === Source data box (centered, top) ===
SRC_W = 200
SRC_H = 55
SRC_X = PAD_X + (CONTENT_W - SRC_W) // 2
SRC_Y = 85
d.rect(
    "src",
    SRC_X,
    SRC_Y,
    SRC_W,
    SRC_H,
    *GRAY,
    fill="hachure",
    bnd=[{"id": "src_t", "type": "text"}],
)
d.txt("src_t", SRC_X, SRC_Y, SRC_W, SRC_H, "Full Dataset\nA B C D", 20, cid="src")

# === LEFT COLUMN: Replication ===
LEFT_X = PAD_X
SECTION_Y = SRC_Y + SRC_H + 80

# Column title
d.txt("rep_title", LEFT_X, SECTION_Y - 35, COL_W, 30, "Replication", 24, color=GREEN[0])
d.txt(
    "rep_sub",
    LEFT_X,
    SECTION_Y - 10,
    COL_W,
    20,
    "Same data on every node",
    17,
    color=GREEN[0],
    op=70,
)

# Container
NODE_W = COL_W - 2 * INNER_PAD
NODE_H = 50
NODE_GAP = 15
CONTAINER_H = INNER_PAD + 3 * NODE_H + 2 * NODE_GAP + INNER_PAD
d.rect(
    "rep_c",
    LEFT_X,
    SECTION_Y + 20,
    COL_W,
    CONTAINER_H,
    *GREEN,
    fill="hachure",
    dashed=True,
)

# 3 nodes, each with full data
rep_nodes = ["Node 1:  A B C D", "Node 2:  A B C D", "Node 3:  A B C D"]
for i, label in enumerate(rep_nodes):
    ny = SECTION_Y + 20 + INNER_PAD + i * (NODE_H + NODE_GAP)
    nid = f"rep_n{i}"
    d.rect(
        nid,
        LEFT_X + INNER_PAD,
        ny,
        NODE_W,
        NODE_H,
        *GREEN,
        fill="hachure",
        bnd=[{"id": f"rep_nt{i}", "type": "text"}],
    )
    d.txt(f"rep_nt{i}", LEFT_X + INNER_PAD, ny, NODE_W, NODE_H, label, 18, cid=nid)

# Arrow from source to left column
d.arr(
    "a_rep",
    SRC_X + SRC_W // 4,
    SRC_Y + SRC_H,
    [
        [0, 0],
        [LEFT_X + COL_W // 2 - SRC_X - SRC_W // 4, SECTION_Y + 20 - SRC_Y - SRC_H],
    ],
    GREEN[0],
    sb={"elementId": "src", "focus": 0, "gap": 4},
    eb={"elementId": "rep_c", "focus": 0, "gap": 4},
)

# === RIGHT COLUMN: Partitioning ===
RIGHT_X = PAD_X + COL_W + COL_GAP

# Column title
d.txt(
    "part_title",
    RIGHT_X,
    SECTION_Y - 35,
    COL_W,
    30,
    "Partitioning",
    24,
    color=PURPLE[0],
)
d.txt(
    "part_sub",
    RIGHT_X,
    SECTION_Y - 10,
    COL_W,
    20,
    "Disjoint subsets per node",
    17,
    color=PURPLE[0],
    op=70,
)

# Container
d.rect(
    "part_c",
    RIGHT_X,
    SECTION_Y + 20,
    COL_W,
    CONTAINER_H,
    *PURPLE,
    fill="hachure",
    dashed=True,
)

# 3 nodes, each with a subset
part_nodes = ["Node 1:  A B", "Node 2:  C", "Node 3:  D"]
for i, label in enumerate(part_nodes):
    ny = SECTION_Y + 20 + INNER_PAD + i * (NODE_H + NODE_GAP)
    nid = f"part_n{i}"
    d.rect(
        nid,
        RIGHT_X + INNER_PAD,
        ny,
        NODE_W,
        NODE_H,
        *PURPLE,
        fill="hachure",
        bnd=[{"id": f"part_nt{i}", "type": "text"}],
    )
    d.txt(f"part_nt{i}", RIGHT_X + INNER_PAD, ny, NODE_W, NODE_H, label, 18, cid=nid)

# Arrow from source to right column
d.arr(
    "a_part",
    SRC_X + 3 * SRC_W // 4,
    SRC_Y + SRC_H,
    [
        [0, 0],
        [RIGHT_X + COL_W // 2 - SRC_X - 3 * SRC_W // 4, SECTION_Y + 20 - SRC_Y - SRC_H],
    ],
    PURPLE[0],
    sb={"elementId": "src", "focus": 0, "gap": 4},
    eb={"elementId": "part_c", "focus": 0, "gap": 4},
)

# === WRITE ===
name = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "diagrams/artifacts/replication-vs-partitioning"
)
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
