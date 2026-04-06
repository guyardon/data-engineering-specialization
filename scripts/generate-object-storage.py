import math

from diagramlib import ExcalidrawDiagram, BLUE, GREEN

d = ExcalidrawDiagram(seed=5000)


def th(text, font_size):
    return math.ceil((text.count("\n") + 1) * font_size * 1.25)


# ── Layout constants ──
CANVAS_W = 800
PAD_X = 40
CONTENT_W = CANVAS_W - 2 * PAD_X

# ── Title ──
TITLE_Y = 0
TITLE_H = th("Object Storage", 32)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Object Storage", 32)

# ── Object Section ──
SECTION_GAP = 40
OBJ_HEADER_Y = TITLE_Y + TITLE_H + SECTION_GAP

# Header box: "Object"
OBJ_HDR_W = 200
OBJ_HDR_H = 70
OBJ_HDR_X = PAD_X + (CONTENT_W - OBJ_HDR_W) // 2

d.rect(
    "obj_hdr",
    OBJ_HDR_X,
    OBJ_HEADER_Y,
    OBJ_HDR_W,
    OBJ_HDR_H,
    BLUE[0],
    BLUE[1],
    bnd=[{"type": "text", "id": "obj_hdr_txt"}],
)
d.txt(
    "obj_hdr_txt",
    OBJ_HDR_X,
    OBJ_HEADER_Y,
    OBJ_HDR_W,
    OBJ_HDR_H,
    "Object",
    24,
    cid="obj_hdr",
)

# Arrow from header to component row
ARROW_GAP = 30
ARROW_START_Y = OBJ_HEADER_Y + OBJ_HDR_H
ARROW_LEN = 50
ARROW_X = PAD_X + CONTENT_W // 2

d.arr(
    "obj_arrow",
    ARROW_X,
    ARROW_START_Y + ARROW_GAP // 2,
    [[0, 0], [0, ARROW_LEN]],
    BLUE[0],
)

# Component pills row
PILL_GAP = 20
PILL_H = 85
COMP_Y = ARROW_START_Y + ARROW_GAP // 2 + ARROW_LEN + 10

components = [
    {"id": "uuid", "title": "UUID (Key)", "sub": "Unique identifier"},
    {"id": "meta", "title": "Metadata", "sub": "Date, owner, version"},
    {"id": "immut", "title": "Immutable", "sub": "Replace, never modify"},
]

NUM_PILLS = len(components)
PILL_W = (CONTENT_W - (NUM_PILLS - 1) * PILL_GAP) // NUM_PILLS

for i, comp in enumerate(components):
    px = PAD_X + i * (PILL_W + PILL_GAP)
    cid = comp["id"]
    tid = f"{cid}_txt"

    label = f"{comp['title']}\n{comp['sub']}"
    d.rect(
        cid,
        px,
        COMP_Y,
        PILL_W,
        PILL_H,
        BLUE[0],
        BLUE[1],
        bnd=[{"type": "text", "id": tid}],
    )
    d.txt(tid, px, COMP_Y, PILL_W, PILL_H, label, 22, cid=cid)

# ── Divider line (subtle) ──
DIVIDER_Y = COMP_Y + PILL_H + 50

# ── Advantages Section ──
ADV_LABEL_Y = DIVIDER_Y
ADV_LABEL_H = th("Why Object Storage?", 24)
d.txt(
    "adv_label",
    PAD_X,
    ADV_LABEL_Y,
    CONTENT_W,
    ADV_LABEL_H,
    "Why Object Storage?",
    24,
    color=GREEN[0],
)

# 2x2 grid of advantage pills
GRID_GAP_X = 20
GRID_GAP_Y = 28
GRID_TOP = ADV_LABEL_Y + ADV_LABEL_H + 25
GRID_PILL_W = (CONTENT_W - GRID_GAP_X) // 2
GRID_PILL_H = 85

advantages = [
    {"id": "scale", "title": "Scalability", "sub": "Virtually unlimited"},
    {"id": "redun", "title": "Redundancy", "sub": "Replicated across AZs"},
    {"id": "cost", "title": "Cost-Effective", "sub": "Pay per use"},
    {"id": "lakes", "title": "Data Lakes", "sub": "Lakes & Lakehouses"},
]

for i, adv in enumerate(advantages):
    row = i // 2
    col = i % 2
    gx = PAD_X + col * (GRID_PILL_W + GRID_GAP_X)
    gy = GRID_TOP + row * (GRID_PILL_H + GRID_GAP_Y)
    aid = adv["id"]
    atid = f"{aid}_txt"

    label = f"{adv['title']}\n{adv['sub']}"
    d.rect(
        aid,
        gx,
        gy,
        GRID_PILL_W,
        GRID_PILL_H,
        GREEN[0],
        GREEN[1],
        bnd=[{"type": "text", "id": atid}],
    )
    d.txt(atid, gx, gy, GRID_PILL_W, GRID_PILL_H, label, 22, cid=aid)

# ── Write file ──
d.save("diagrams/object-storage.excalidraw")
print("Done! Wrote diagrams/object-storage.excalidraw")
