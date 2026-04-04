"""
Generate data lake zones diagram showing the three-zone architecture
(raw/landing, cleaned/transformed, curated/enriched) with data flow.
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
RED = ("#c92a2a", "#ffc9c9")
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


# === LAYOUT CONSTANTS ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620
ARROW_GAP = 70

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Data Lake Zone Architecture", 32, color="#1e1e1e")

# === SOURCES ROW ===
SRC_Y = TITLE_Y + TITLE_H + 30
SRC_H = 50
SRC_GAP = 15
SRC_W = (CONTENT_W - 3 * SRC_GAP) // 4

sources = [
    ("s1", "APIs", GRAY),
    ("s2", "Databases", GRAY),
    ("s3", "Files", GRAY),
    ("s4", "Streams", GRAY),
]
for i, (bid, label, color) in enumerate(sources):
    x = PAD_X + i * (SRC_W + SRC_GAP)
    rect(bid, x, SRC_Y, SRC_W, SRC_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", x, SRC_Y, SRC_W, SRC_H, label, 20, cid=bid)

# === BIG CONTAINER: Data Lake on Object Storage ===
LAKE_Y = SRC_Y + SRC_H + ARROW_GAP
ZONE_W = CONTENT_W - 40  # inside container
ZONE_H = 95
ZONE_GAP = 15
LAKE_PAD = 20
LAKE_INNER_X = PAD_X + LAKE_PAD

# Three zones + labels + padding
LAKE_H = LAKE_PAD + 30 + ZONE_H + ZONE_GAP + ZONE_H + ZONE_GAP + ZONE_H + LAKE_PAD + 25

rect("lake", PAD_X, LAKE_Y, CONTENT_W, LAKE_H,
     BLUE[0], "#dbe4ff", dashed=True)

# Lake label
LAKE_LABEL_Y = LAKE_Y + 10
LAKE_LABEL_H = math.ceil(1 * 20 * 1.25)
txt("lake_label", PAD_X, LAKE_LABEL_Y, CONTENT_W, LAKE_LABEL_H,
    "Data Lake (Object Storage)", 20, color=BLUE[0])

# === Zone 1: Raw/Landing ===
Z1_Y = LAKE_LABEL_Y + LAKE_LABEL_H + 12

# Title+subtitle box
rect("z1", LAKE_INNER_X, Z1_Y, ZONE_W, ZONE_H, *RED,
     bnd=[{"id": "z1_t", "type": "text"}])

# Title
z1_title = "Raw / Landing Zone"
z1_sub = "Unprocessed data, original format\nJSON, CSV, logs, images"
z1_title_h = math.ceil(1 * 24 * 1.25)
z1_sub_h = math.ceil(2 * 17 * 1.25)
z1_gap = 6
z1_combined = z1_title_h + z1_gap + z1_sub_h
z1_top_pad = (ZONE_H - z1_combined) // 2

txt("z1_t", LAKE_INNER_X, Z1_Y + z1_top_pad, ZONE_W, z1_title_h,
    z1_title, 24, cid="z1")
txt("z1_sub", LAKE_INNER_X, Z1_Y + z1_top_pad + z1_title_h + z1_gap, ZONE_W, z1_sub_h,
    z1_sub, 17, color=RED[0])

# Arrow z1 -> z2
Z2_Y = Z1_Y + ZONE_H + ZONE_GAP
arr("a_z1z2", LAKE_INNER_X + ZONE_W // 2, Z1_Y + ZONE_H,
    [[0, 0], [0, ZONE_GAP]],
    RED[0],
    sb={"elementId": "z1", "focus": 0, "gap": 4},
    eb={"elementId": "z2", "focus": 0, "gap": 4})

# === Zone 2: Cleaned/Transformed ===
rect("z2", LAKE_INNER_X, Z2_Y, ZONE_W, ZONE_H, *YELLOW,
     bnd=[{"id": "z2_t", "type": "text"}])

z2_title = "Cleaned / Transformed Zone"
z2_sub = "Validated, deduplicated, standardized\nParquet, schema-enforced"
z2_title_h = math.ceil(1 * 24 * 1.25)
z2_sub_h = math.ceil(2 * 17 * 1.25)
z2_combined = z2_title_h + z1_gap + z2_sub_h
z2_top_pad = (ZONE_H - z2_combined) // 2

txt("z2_t", LAKE_INNER_X, Z2_Y + z2_top_pad, ZONE_W, z2_title_h,
    z2_title, 24, cid="z2")
txt("z2_sub", LAKE_INNER_X, Z2_Y + z2_top_pad + z2_title_h + z1_gap, ZONE_W, z2_sub_h,
    z2_sub, 17, color=YELLOW[0])

# Arrow z2 -> z3
Z3_Y = Z2_Y + ZONE_H + ZONE_GAP
arr("a_z2z3", LAKE_INNER_X + ZONE_W // 2, Z2_Y + ZONE_H,
    [[0, 0], [0, ZONE_GAP]],
    YELLOW[0],
    sb={"elementId": "z2", "focus": 0, "gap": 4},
    eb={"elementId": "z3", "focus": 0, "gap": 4})

# === Zone 3: Curated/Enriched ===
rect("z3", LAKE_INNER_X, Z3_Y, ZONE_W, ZONE_H, *GREEN,
     bnd=[{"id": "z3_t", "type": "text"}])

z3_title = "Curated / Enriched Zone"
z3_sub = "Business-ready, aggregated, feature-engineered\nReady for analytics and ML"
z3_title_h = math.ceil(1 * 24 * 1.25)
z3_sub_h = math.ceil(2 * 17 * 1.25)
z3_combined = z3_title_h + z1_gap + z3_sub_h
z3_top_pad = (ZONE_H - z3_combined) // 2

txt("z3_t", LAKE_INNER_X, Z3_Y + z3_top_pad, ZONE_W, z3_title_h,
    z3_title, 24, cid="z3")
txt("z3_sub", LAKE_INNER_X, Z3_Y + z3_top_pad + z3_title_h + z1_gap, ZONE_W, z3_sub_h,
    z3_sub, 17, color=GREEN[0])

# === ARROWS: Sources to Lake ===
for i, (bid, _, _) in enumerate(sources):
    sx = PAD_X + i * (SRC_W + SRC_GAP) + SRC_W // 2
    arr(f"a_s{i}", sx, SRC_Y + SRC_H,
        [[0, 0], [0, LAKE_Y - SRC_Y - SRC_H]],
        GRAY[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "lake", "focus": 0, "gap": 4})

# === DATA CATALOG (below lake) ===
CAT_Y = LAKE_Y + LAKE_H + 15
CAT_W = CONTENT_W
CAT_H = 55
rect("catalog", PAD_X, CAT_Y, CAT_W, CAT_H, *PURPLE,
     bnd=[{"id": "cat_t", "type": "text"}])
txt("cat_t", PAD_X, CAT_Y, CAT_W, CAT_H,
    "Data Catalog (Schema, Partitions, Lineage)", 20, cid="catalog")

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{CAT_Y + CAT_H + 20}")
print(f"Title: y={TITLE_Y}")
print(f"Sources: y={SRC_Y} to {SRC_Y + SRC_H}")
print(f"Lake: y={LAKE_Y} to {LAKE_Y + LAKE_H}")
print(f"Catalog: y={CAT_Y} to {CAT_Y + CAT_H}")

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "data-lake-zones"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
