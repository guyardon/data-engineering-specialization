"""
CAP Theorem diagram.
Three properties in a triangle with labels showing you can only pick 2.
CP, AP, CA pairs shown as connections.

Canvas: 600px wide, compact.
"""

import sys

from diagramlib import BLUE, GRAY, GREEN, RED, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=7000)

# === LAYOUT ===
CANVAS_W = 600
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 200  # property box width
BH = 65  # property box height

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "CAP Theorem", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Choose at most two of three guarantees",
    17,
    color=RED[0],
)

# Triangle layout:
#        C (top center)
#       / \
#      /   \
#     A --- P (bottom left, bottom right)
CX = CANVAS_W // 2

# Consistency (top center)
C_X = CX - BW // 2
C_Y = 100
d.rect("c", C_X, C_Y, BW, BH, *BLUE, fill="hachure", bnd=[{"id": "ct", "type": "text"}])
d.txt("ct", C_X, C_Y, BW, BH, "Consistency\nLatest data on every read", 17, cid="c")

# Availability (bottom left)
A_X = PAD_X + 15
A_Y = 310
d.rect(
    "a", A_X, A_Y, BW, BH, *GREEN, fill="hachure", bnd=[{"id": "at", "type": "text"}]
)
d.txt(
    "at", A_X, A_Y, BW, BH, "Availability\nEvery request gets a response", 17, cid="a"
)

# Partition tolerance (bottom right)
P_X = CANVAS_W - PAD_X - BW - 15
P_Y = 310
d.rect(
    "p", P_X, P_Y, BW, BH, *YELLOW, fill="hachure", bnd=[{"id": "pt", "type": "text"}]
)
d.txt(
    "pt", P_X, P_Y, BW, BH, "Partition Tolerance\nSurvives network splits", 17, cid="p"
)

# Triangle edges (lines connecting the 3 boxes)
# C bottom-center to A top-center
d.line(
    "l_ca",
    C_X + BW // 2,
    C_Y + BH,
    [[0, 0], [A_X + BW // 2 - C_X - BW // 2, A_Y - C_Y - BH]],
    GRAY[0],
    dash=True,
    op=50,
)

# C bottom-center to P top-center
d.line(
    "l_cp",
    C_X + BW // 2,
    C_Y + BH,
    [[0, 0], [P_X + BW // 2 - C_X - BW // 2, P_Y - C_Y - BH]],
    GRAY[0],
    dash=True,
    op=50,
)

# A right-center to P left-center
d.line(
    "l_ap",
    A_X + BW,
    A_Y + BH // 2,
    [[0, 0], [P_X - A_X - BW, 0]],
    GRAY[0],
    dash=True,
    op=50,
)

# Edge labels showing system types
# CA edge (left side) — theoretical only
d.txt(
    "l_ca_t",
    A_X - 15,
    C_Y + BH + 30,
    100,
    40,
    "CA\n(single node)",
    15,
    color=GRAY[0],
    op=60,
)

# CP edge (right side) — HBase, MongoDB
d.txt(
    "l_cp_t",
    P_X + BW - 80,
    C_Y + BH + 30,
    120,
    40,
    "CP\nHBase, MongoDB",
    15,
    color=BLUE[0],
    op=80,
)

# AP edge (bottom) — Cassandra, DynamoDB
d.txt(
    "l_ap_t",
    CX - 75,
    A_Y + BH + 15,
    150,
    40,
    "AP\nCassandra, DynamoDB",
    15,
    color=GREEN[0],
    op=80,
)

# Center note
d.txt(
    "center_note",
    CX - 90,
    230,
    180,
    40,
    "Pick 2\n(can't have all 3)",
    18,
    color=RED[0],
    op=80,
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/cap-theorem"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
