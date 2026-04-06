"""
Storage hierarchy diagram.
Shows 4 layers stacked vertically, from physical (top) to abstract (bottom):
  1. Physical Components (top) - Magnetic Disks, SSDs, RAM, CPU Cache
  2. Processes - Serialization, Compression, Networking, CPU
  3. Storage Systems - OLTP, OLAP, Object Stores, Graph/Vector DBs
  4. Storage Abstractions (bottom) - Data Warehouses, Data Lakes, Data Lakehouses

Narrow canvas (650px) for good vertical aspect ratio.
Uses Rule 7 padding (PAD=25) for encapsulating containers around inner pills.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, GRAY

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
INNER_PAD = 25  # Rule 7: internal padding inside containers
LABEL_H = 28  # height reserved for the container label text
PILL_H = 42
PILL_GAP = 15
ARROW_GAP = 70  # vertical gap between layers (for arrows)

# Container height = label + gap + pill + padding bottom
CONTAINER_H = LABEL_H + 10 + PILL_H + INNER_PAD


# Helper: build a layer (container + label + pills)
def build_layer(layer_id, y, label, color, pills, pill_w):
    """Create a dashed container with a label at top and centered pills inside."""
    # Container rect
    d.rect(
        layer_id, PAD_X, y, CONTENT_W, CONTAINER_H, *color, fill="hachure", dashed=True
    )
    # Label text (free, positioned inside container top area)
    d.txt(
        f"{layer_id}_label",
        PAD_X + INNER_PAD,
        y + 8,
        CONTENT_W - 2 * INNER_PAD,
        LABEL_H,
        label,
        20,
        color=color[0],
    )
    # Pills row, centered horizontally
    total_w = len(pills) * pill_w + (len(pills) - 1) * PILL_GAP
    start_x = PAD_X + (CONTENT_W - total_w) // 2
    pill_y = y + LABEL_H + 15  # below label + small gap
    for i, pill_label in enumerate(pills):
        px = start_x + i * (pill_w + PILL_GAP)
        pid = f"{layer_id}_p{i}"
        tid = f"{layer_id}_t{i}"
        d.rect(
            pid,
            px,
            pill_y,
            pill_w,
            PILL_H,
            *color,
            fill="hachure",
            bnd=[{"id": tid, "type": "text"}],
        )
        d.txt(tid, px, pill_y, pill_w, PILL_H, pill_label, 17, cid=pid)
    return y + CONTAINER_H


# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Storage Hierarchy", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "From physical hardware to high-level abstractions",
    17,
    color=PURPLE[0],
)

# === LAYER 1 (top): Physical Components ===
L1_Y = 95
build_layer(
    "l1",
    L1_Y,
    "Physical Components",
    YELLOW,
    ["Magnetic Disks", "SSDs", "RAM", "CPU Cache"],
    pill_w=125,
)

# Arrow L1 -> L2
d.arr(
    "a12",
    PAD_X + CONTENT_W // 2,
    L1_Y + CONTAINER_H,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "l1", "focus": 0, "gap": 4},
    eb={"elementId": "l2", "focus": 0, "gap": 4},
)

# === LAYER 2: Processes ===
L2_Y = L1_Y + CONTAINER_H + ARROW_GAP
build_layer(
    "l2",
    L2_Y,
    "Processes",
    GREEN,
    ["Serialization", "Compression", "Networking", "CPU"],
    pill_w=125,
)

# Arrow L2 -> L3
d.arr(
    "a23",
    PAD_X + CONTENT_W // 2,
    L2_Y + CONTAINER_H,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "l2", "focus": 0, "gap": 4},
    eb={"elementId": "l3", "focus": 0, "gap": 4},
)

# === LAYER 3: Storage Systems ===
L3_Y = L2_Y + CONTAINER_H + ARROW_GAP
build_layer(
    "l3",
    L3_Y,
    "Storage Systems",
    BLUE,
    ["OLTP", "OLAP", "Object Stores", "Graph DBs", "Vector DBs"],
    pill_w=105,
)

# Arrow L3 -> L4
d.arr(
    "a34",
    PAD_X + CONTENT_W // 2,
    L3_Y + CONTAINER_H,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "l3", "focus": 0, "gap": 4},
    eb={"elementId": "l4", "focus": 0, "gap": 4},
)

# === LAYER 4 (bottom): Storage Abstractions ===
L4_Y = L3_Y + CONTAINER_H + ARROW_GAP
build_layer(
    "l4",
    L4_Y,
    "Storage Abstractions",
    PURPLE,
    ["Data Warehouses", "Data Lakes", "Data Lakehouses"],
    pill_w=170,
)


# === VERIFY ===
print(f"L1: {L1_Y}-{L1_Y + CONTAINER_H}")
print(f"L2: {L2_Y}-{L2_Y + CONTAINER_H}")
print(f"L3: {L3_Y}-{L3_Y + CONTAINER_H}")
print(f"L4: {L4_Y}-{L4_Y + CONTAINER_H}")
print(f"Total height: {L4_Y + CONTAINER_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/storage-hierarchy"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
