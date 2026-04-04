"""
Generate star schema diagram showing a central fact table
connected to dimension tables.
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
seed = 7000


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


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True if cid else False, "containerId": cid,
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


# === LAYOUT ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Star Schema", 32, color="#1e1e1e")

# Central fact table
FACT_W = 200
FACT_H = 140
CENTER_X = PAD_X + (CONTENT_W - FACT_W) // 2
FACT_Y = TITLE_Y + TITLE_H + 120

rect("fact", CENTER_X, FACT_Y, FACT_W, FACT_H, *YELLOW,
     bnd=[{"id": "fact_t", "type": "text"}])

fact_title = "Fact Table"
fact_sub = "order_key (PK)\nstore_key (FK)\nitem_key (FK)\ndate_key (FK)\nquantity, price"
ft_h = math.ceil(1 * 24 * 1.25)
fs_h = math.ceil(5 * 15 * 1.25)
fg = 4
fc = ft_h + fg + fs_h
ftp = (FACT_H - fc) // 2

txt("fact_t", CENTER_X, FACT_Y + ftp, FACT_W, ft_h,
    fact_title, 24, cid="fact")
txt("fact_sub", CENTER_X, FACT_Y + ftp + ft_h + fg, FACT_W, fs_h,
    fact_sub, 15, color=YELLOW[0])

# Dimension tables around the fact
DIM_W = 170
DIM_H = 100

# Positions: top, left, right, bottom
dims = [
    ("dim_date", "dim_date", "date_key (PK)\nday, month\nquarter, year", BLUE,
     CENTER_X + (FACT_W - DIM_W) // 2, FACT_Y - DIM_H - 70),  # top
    ("dim_store", "dim_store", "store_key (PK)\nstore_name\ncity, zipcode", GREEN,
     PAD_X, FACT_Y + (FACT_H - DIM_H) // 2),  # left
    ("dim_item", "dim_item", "item_key (PK)\nsku, name\nbrand", PURPLE,
     PAD_X + CONTENT_W - DIM_W, FACT_Y + (FACT_H - DIM_H) // 2),  # right
    ("dim_cust", "dim_customer", "customer_key (PK)\nname, email\naddress", CYAN,
     CENTER_X + (FACT_W - DIM_W) // 2, FACT_Y + FACT_H + 70),  # bottom
]

for bid, title, sub, color, dx, dy in dims:
    rect(bid, dx, dy, DIM_W, DIM_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    dt_h = math.ceil(1 * 22 * 1.25)
    ds_h = math.ceil(sub.count("\n") * 15 * 1.25 + math.ceil(1 * 15 * 1.25))
    dg = 4
    dc = dt_h + dg + ds_h
    dtp = (DIM_H - dc) // 2

    txt(f"{bid}_t", dx, dy + dtp, DIM_W, dt_h,
        title, 22, cid=bid)
    txt(f"{bid}_sub", dx, dy + dtp + dt_h + dg, DIM_W, ds_h,
        sub, 15, color=color[0])

# Arrows from dimensions to fact
# Top -> fact
arr("a_date", CENTER_X + FACT_W // 2, FACT_Y - 70,
    [[0, 0], [0, 70]],
    BLUE[0],
    sb={"elementId": "dim_date", "focus": 0, "gap": 4},
    eb={"elementId": "fact", "focus": 0, "gap": 4})

# Left -> fact
arr("a_store", PAD_X + DIM_W, FACT_Y + FACT_H // 2,
    [[0, 0], [CENTER_X - PAD_X - DIM_W, 0]],
    GREEN[0],
    sb={"elementId": "dim_store", "focus": 0, "gap": 4},
    eb={"elementId": "fact", "focus": 0, "gap": 4})

# Right -> fact
arr("a_item", PAD_X + CONTENT_W - DIM_W, FACT_Y + FACT_H // 2,
    [[0, 0], [-(PAD_X + CONTENT_W - DIM_W - CENTER_X - FACT_W), 0]],
    PURPLE[0],
    sb={"elementId": "dim_item", "focus": 0, "gap": 4},
    eb={"elementId": "fact", "focus": 0, "gap": 4})

# Bottom -> fact
arr("a_cust", CENTER_X + FACT_W // 2, FACT_Y + FACT_H,
    [[0, 0], [0, 70]],
    CYAN[0],
    sb={"elementId": "fact", "focus": 0, "gap": 4},
    eb={"elementId": "dim_cust", "focus": 0, "gap": 4})

print(f"Canvas: {CANVAS_W}x{FACT_Y + FACT_H + 70 + DIM_H + 20}")

name = sys.argv[1] if len(sys.argv) > 1 else "star-schema"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
