import json
import math
import os

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 5000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(
    id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2
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
            "strokeWidth": sw,
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, valign="middle"):
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
            "textAlign": "center",
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


def th(text, font_size):
    return math.ceil((text.count("\n") + 1) * font_size * 1.25)


# ── Layout constants ──
CANVAS_W = 800
PAD_X = 40
CONTENT_W = CANVAS_W - 2 * PAD_X

# ── Title ──
TITLE_Y = 0
TITLE_H = th("Object Storage", 32)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Object Storage", 32)

# ── Object Section ──
SECTION_GAP = 40
OBJ_HEADER_Y = TITLE_Y + TITLE_H + SECTION_GAP

# Header box: "Object"
OBJ_HDR_W = 200
OBJ_HDR_H = 70
OBJ_HDR_X = PAD_X + (CONTENT_W - OBJ_HDR_W) // 2

rect(
    "obj_hdr",
    OBJ_HDR_X,
    OBJ_HEADER_Y,
    OBJ_HDR_W,
    OBJ_HDR_H,
    BLUE[0],
    BLUE[1],
    bnd=[{"type": "text", "id": "obj_hdr_txt"}],
)
txt(
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

arr(
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
    rect(
        cid,
        px,
        COMP_Y,
        PILL_W,
        PILL_H,
        BLUE[0],
        BLUE[1],
        bnd=[{"type": "text", "id": tid}],
    )
    txt(tid, px, COMP_Y, PILL_W, PILL_H, label, 22, cid=cid)

# ── Divider line (subtle) ──
DIVIDER_Y = COMP_Y + PILL_H + 50

# ── Advantages Section ──
ADV_LABEL_Y = DIVIDER_Y
ADV_LABEL_H = th("Why Object Storage?", 24)
txt(
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
    rect(
        aid,
        gx,
        gy,
        GRID_PILL_W,
        GRID_PILL_H,
        GREEN[0],
        GREEN[1],
        bnd=[{"type": "text", "id": atid}],
    )
    txt(atid, gx, gy, GRID_PILL_W, GRID_PILL_H, label, 22, cid=aid)

# ── Write file ──
out_path = "diagrams/object-storage.excalidraw"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Done! Wrote {out_path}")
