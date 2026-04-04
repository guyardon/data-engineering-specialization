"""
Replication vs Partitioning diagram.
Two columns side by side:
  Left: Replication — same data copied to all 3 nodes
  Right: Partitioning — data split into disjoint subsets across 3 nodes

Canvas: 650px wide.
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
seed = 6000


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


def rect(
    id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None
):
    els.append(
        {
            "type": "rectangle",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 3},
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append(
        {
            "type": "text",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "text": t,
            "originalText": t,
            "fontSize": sz,
            "fontFamily": 1,
            "textAlign": align,
            "verticalAlign": "middle",
            "lineHeight": 1.25,
            "autoResize": True,
            "containerId": cid,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# === LAYOUT ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
INNER_PAD = 25
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Replication vs Partitioning", 32)
txt(
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
rect("src", SRC_X, SRC_Y, SRC_W, SRC_H, *GRAY, bnd=[{"id": "src_t", "type": "text"}])
txt("src_t", SRC_X, SRC_Y, SRC_W, SRC_H, "Full Dataset\nA B C D", 20, cid="src")

# === LEFT COLUMN: Replication ===
LEFT_X = PAD_X
SECTION_Y = SRC_Y + SRC_H + 80

# Column title
txt("rep_title", LEFT_X, SECTION_Y - 35, COL_W, 30, "Replication", 24, color=GREEN[0])
txt(
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
rect("rep_c", LEFT_X, SECTION_Y + 20, COL_W, CONTAINER_H, *GREEN, dashed=True)

# 3 nodes, each with full data
rep_nodes = ["Node 1:  A B C D", "Node 2:  A B C D", "Node 3:  A B C D"]
for i, label in enumerate(rep_nodes):
    ny = SECTION_Y + 20 + INNER_PAD + i * (NODE_H + NODE_GAP)
    nid = f"rep_n{i}"
    rect(
        nid,
        LEFT_X + INNER_PAD,
        ny,
        NODE_W,
        NODE_H,
        *GREEN,
        bnd=[{"id": f"rep_nt{i}", "type": "text"}],
    )
    txt(f"rep_nt{i}", LEFT_X + INNER_PAD, ny, NODE_W, NODE_H, label, 18, cid=nid)

# Arrow from source to left column
arr(
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
txt(
    "part_title",
    RIGHT_X,
    SECTION_Y - 35,
    COL_W,
    30,
    "Partitioning",
    24,
    color=PURPLE[0],
)
txt(
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
rect("part_c", RIGHT_X, SECTION_Y + 20, COL_W, CONTAINER_H, *PURPLE, dashed=True)

# 3 nodes, each with a subset
part_nodes = ["Node 1:  A B", "Node 2:  C", "Node 3:  D"]
for i, label in enumerate(part_nodes):
    ny = SECTION_Y + 20 + INNER_PAD + i * (NODE_H + NODE_GAP)
    nid = f"part_n{i}"
    rect(
        nid,
        RIGHT_X + INNER_PAD,
        ny,
        NODE_W,
        NODE_H,
        *PURPLE,
        bnd=[{"id": f"part_nt{i}", "type": "text"}],
    )
    txt(f"part_nt{i}", RIGHT_X + INNER_PAD, ny, NODE_W, NODE_H, label, 18, cid=nid)

# Arrow from source to right column
arr(
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
name = sys.argv[1] if len(sys.argv) > 1 else "replication-vs-partitioning"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
