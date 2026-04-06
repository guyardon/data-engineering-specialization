"""
Vector Database schematic diagram.
Shows: Input data -> Embedding model -> Vector space with points -> KNN query result

Vertical flow. Canvas: 600px wide.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, RED, CYAN, GRAY

d = ExcalidrawDiagram(seed=10000)


# Custom ellipse helper (not in diagramlib)
def ellipse(id, x, y, w, h, stroke, bg, fill="solid", op=100, bnd=None):
    d.elements.append(
        {
            "type": "ellipse",
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
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "roundness": {"type": 2},
            "seed": d._ns(),
            "version": 1,
            "versionNonce": d._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# === LAYOUT ===
CANVAS_W = 600
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
BW = 260
BH = 65
ARROW_GAP = 70
CX = CANVAS_W // 2
BOX_X = CX - BW // 2

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Vector Database", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Similarity search via vector embeddings",
    17,
    color=CYAN[0],
)

# === Step 1: Input Data ===
S1_Y = 90
d.rect(
    "input",
    BOX_X,
    S1_Y,
    BW,
    BH,
    *GRAY,
    fill="hachure",
    bnd=[{"id": "input_t", "type": "text"}],
)
d.txt(
    "input_t", BOX_X, S1_Y, BW, BH, "Input Data\nText, images, audio", 18, cid="input"
)

# Arrow
d.arr(
    "a1",
    CX,
    S1_Y + BH,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "input", "focus": 0, "gap": 4},
    eb={"elementId": "embed", "focus": 0, "gap": 4},
)
d.txt("l_embed", CX + 10, S1_Y + BH + 20, 80, 25, "Embed", 17, color=CYAN[0])

# === Step 2: Embedding Model ===
S2_Y = S1_Y + BH + ARROW_GAP
d.rect(
    "embed",
    BOX_X,
    S2_Y,
    BW,
    BH,
    *CYAN,
    fill="hachure",
    bnd=[{"id": "embed_t", "type": "text"}],
)
d.txt(
    "embed_t",
    BOX_X,
    S2_Y,
    BW,
    BH,
    "Embedding Model\n→ [0.23, -0.87, 0.45, ...]",
    18,
    cid="embed",
)

# Arrow
d.arr(
    "a2",
    CX,
    S2_Y + BH,
    [[0, 0], [0, ARROW_GAP]],
    CYAN[0],
    sb={"elementId": "embed", "focus": 0, "gap": 4},
    eb={"elementId": "vspace", "focus": 0, "gap": 4},
)
d.txt("l_store", CX + 10, S2_Y + BH + 20, 80, 25, "Store", 17, color=PURPLE[0])

# === Step 3: Vector Space (larger box with scattered dots) ===
S3_Y = S2_Y + BH + ARROW_GAP
VS_W = 350
VS_H = 180
VS_X = CX - VS_W // 2
d.rect("vspace", VS_X, S3_Y, VS_W, VS_H, *PURPLE, fill="hachure", dashed=True)
d.txt(
    "vspace_label",
    VS_X + 10,
    S3_Y + 5,
    VS_W - 20,
    25,
    "Vector Space",
    20,
    color=PURPLE[0],
)

# Scatter some dots (small ellipses) to represent vectors
DOT = 16
dots = [
    # (x_offset, y_offset, color, label)
    (60, 60, BLUE, "A"),
    (80, 110, BLUE, "B"),
    (100, 80, BLUE, "C"),  # cluster 1
    (200, 50, GREEN, "D"),
    (230, 80, GREEN, "E"),
    (210, 110, GREEN, "F"),  # cluster 2
    (140, 140, YELLOW, "G"),  # outlier
    (280, 140, GRAY, "H"),  # far point
]

for i, (dx, dy, color, label) in enumerate(dots):
    ex = VS_X + dx
    ey = S3_Y + dy
    ellipse(f"dot{i}", ex, ey, DOT, DOT, color[0], color[1], op=90)
    d.txt(f"dotl{i}", ex + DOT + 3, ey - 2, 20, DOT, label, 13, color=color[0], op=70)

# Query point (highlighted, larger)
QX = VS_X + 90
QY = S3_Y + 90
ellipse("query_dot", QX, QY, DOT + 4, DOT + 4, RED[0], RED[1], op=100)
d.txt("query_label", QX + DOT + 8, QY - 2, 50, DOT, "Query", 14, color=RED[0])

# Dashed circle around query to show KNN radius
# We'll draw a dashed rectangle as an approximation of the search radius
RADIUS = 70
d.rect(
    "knn_radius",
    QX - RADIUS // 2 + DOT // 2,
    QY - RADIUS // 2 + DOT // 2,
    RADIUS * 2,
    RADIUS * 2,
    RED[0],
    "transparent",
    fill="hachure",
    dashed=True,
    opacity=40,
)

# === Step 4: Query Result ===
S4_Y = S3_Y + VS_H + ARROW_GAP
d.rect(
    "result",
    BOX_X,
    S4_Y,
    BW,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "result_t", "type": "text"}],
)
d.txt(
    "result_t",
    BOX_X,
    S4_Y,
    BW,
    BH,
    "K-Nearest Neighbors\nMost similar results",
    18,
    cid="result",
)

# Arrow
d.arr(
    "a3",
    CX,
    S3_Y + VS_H,
    [[0, 0], [0, ARROW_GAP]],
    PURPLE[0],
    sb={"elementId": "vspace", "focus": 0, "gap": 4},
    eb={"elementId": "result", "focus": 0, "gap": 4},
)
d.txt("l_query", CX + 10, S3_Y + VS_H + 20, 100, 25, "KNN Search", 17, color=GREEN[0])

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/vector-database"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
