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
seed = 3000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
    els.append({
        "type": "rectangle", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
        "opacity": opacity, "roundness": {"type": 3},
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": bnd or [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True, "containerId": cid,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({
        "type": "arrow", "id": id, "x": x, "y": y,
        "width": abs(pts[-1][0] - pts[0][0]), "height": abs(pts[-1][1] - pts[0][1]),
        "angle": 0, "points": pts,
        "startArrowhead": None, "endArrowhead": "arrow",
        "startBinding": sb, "endBinding": eb, "elbowed": False,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dash else "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


# === LAYOUT CONSTANTS ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
INNER_PAD = 25          # Rule 7: internal padding inside containers
LABEL_H = 28            # height reserved for the container label text
PILL_H = 42
PILL_GAP = 15
ARROW_GAP = 70          # vertical gap between layers (for arrows)

# Container height = label + gap + pill + padding bottom
CONTAINER_H = LABEL_H + 10 + PILL_H + INNER_PAD


# Helper: build a layer (container + label + pills)
def build_layer(layer_id, y, label, color, pills, pill_w):
    """Create a dashed container with a label at top and centered pills inside."""
    # Container rect
    rect(layer_id, PAD_X, y, CONTENT_W, CONTAINER_H, *color, dashed=True)
    # Label text (free, positioned inside container top area)
    txt(f"{layer_id}_label", PAD_X + INNER_PAD, y + 8, CONTENT_W - 2 * INNER_PAD, LABEL_H,
        label, 20, color=color[0])
    # Pills row, centered horizontally
    total_w = len(pills) * pill_w + (len(pills) - 1) * PILL_GAP
    start_x = PAD_X + (CONTENT_W - total_w) // 2
    pill_y = y + LABEL_H + 15  # below label + small gap
    for i, pill_label in enumerate(pills):
        px = start_x + i * (pill_w + PILL_GAP)
        pid = f"{layer_id}_p{i}"
        tid = f"{layer_id}_t{i}"
        rect(pid, px, pill_y, pill_w, PILL_H, *color,
             bnd=[{"id": tid, "type": "text"}])
        txt(tid, px, pill_y, pill_w, PILL_H, pill_label, 17, cid=pid)
    return y + CONTAINER_H


# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40,
    "Storage Hierarchy", 32)
txt("sub", PAD_X, TITLE_Y + 38, CONTENT_W, 25,
    "From physical hardware to high-level abstractions", 17, color=PURPLE[0])

# === LAYER 1 (top): Physical Components ===
L1_Y = 95
build_layer("l1", L1_Y, "Physical Components", YELLOW,
            ["Magnetic Disks", "SSDs", "RAM", "CPU Cache"], pill_w=125)

# Arrow L1 → L2
arr("a12", PAD_X + CONTENT_W // 2, L1_Y + CONTAINER_H, [[0, 0], [0, ARROW_GAP]], GRAY[0],
    sb={"elementId": "l1", "focus": 0, "gap": 4},
    eb={"elementId": "l2", "focus": 0, "gap": 4})

# === LAYER 2: Processes ===
L2_Y = L1_Y + CONTAINER_H + ARROW_GAP
build_layer("l2", L2_Y, "Processes", GREEN,
            ["Serialization", "Compression", "Networking", "CPU"], pill_w=125)

# Arrow L2 → L3
arr("a23", PAD_X + CONTENT_W // 2, L2_Y + CONTAINER_H, [[0, 0], [0, ARROW_GAP]], GRAY[0],
    sb={"elementId": "l2", "focus": 0, "gap": 4},
    eb={"elementId": "l3", "focus": 0, "gap": 4})

# === LAYER 3: Storage Systems ===
L3_Y = L2_Y + CONTAINER_H + ARROW_GAP
build_layer("l3", L3_Y, "Storage Systems", BLUE,
            ["OLTP", "OLAP", "Object Stores", "Graph DBs", "Vector DBs"], pill_w=105)

# Arrow L3 → L4
arr("a34", PAD_X + CONTENT_W // 2, L3_Y + CONTAINER_H, [[0, 0], [0, ARROW_GAP]], GRAY[0],
    sb={"elementId": "l3", "focus": 0, "gap": 4},
    eb={"elementId": "l4", "focus": 0, "gap": 4})

# === LAYER 4 (bottom): Storage Abstractions ===
L4_Y = L3_Y + CONTAINER_H + ARROW_GAP
build_layer("l4", L4_Y, "Storage Abstractions", PURPLE,
            ["Data Warehouses", "Data Lakes", "Data Lakehouses"], pill_w=170)


# === VERIFY ===
print(f"L1: {L1_Y}-{L1_Y + CONTAINER_H}")
print(f"L2: {L2_Y}-{L2_Y + CONTAINER_H}")
print(f"L3: {L3_Y}-{L3_Y + CONTAINER_H}")
print(f"L4: {L4_Y}-{L4_Y + CONTAINER_H}")
print(f"Total height: {L4_Y + CONTAINER_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "storage-hierarchy"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
