"""
Generate data lake zones diagram showing the three-zone architecture
(raw/landing, cleaned/transformed, curated/enriched) with data flow.
"""

import math
import sys

from diagramlib import BLUE, GRAY, GREEN, PURPLE, RED, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620
ARROW_GAP = 70

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
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
    d.rect(bid, x, SRC_Y, SRC_W, SRC_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", x, SRC_Y, SRC_W, SRC_H, label, 20, cid=bid)

# === BIG CONTAINER: Data Lake on Object Storage ===
LAKE_Y = SRC_Y + SRC_H + ARROW_GAP
ZONE_W = CONTENT_W - 40  # inside container
ZONE_H = 95
ZONE_GAP = 15
LAKE_PAD = 20
LAKE_INNER_X = PAD_X + LAKE_PAD

# Three zones + labels + padding
LAKE_H = LAKE_PAD + 30 + ZONE_H + ZONE_GAP + ZONE_H + ZONE_GAP + ZONE_H + LAKE_PAD + 25

d.rect("lake", PAD_X, LAKE_Y, CONTENT_W, LAKE_H,
     BLUE[0], "#dbe4ff", dashed=True)

# Lake label
LAKE_LABEL_Y = LAKE_Y + 10
LAKE_LABEL_H = math.ceil(1 * 20 * 1.25)
d.txt("lake_label", PAD_X, LAKE_LABEL_Y, CONTENT_W, LAKE_LABEL_H,
    "Data Lake (Object Storage)", 20, color=BLUE[0])

# === Zone 1: Raw/Landing ===
Z1_Y = LAKE_LABEL_Y + LAKE_LABEL_H + 12

# Title+subtitle box
d.rect("z1", LAKE_INNER_X, Z1_Y, ZONE_W, ZONE_H, *RED,
     bnd=[{"id": "z1_t", "type": "text"}])

# Title
z1_title = "Raw / Landing Zone"
z1_sub = "Unprocessed data, original format\nJSON, CSV, logs, images"
z1_title_h = math.ceil(1 * 24 * 1.25)
z1_sub_h = math.ceil(2 * 17 * 1.25)
z1_gap = 6
z1_combined = z1_title_h + z1_gap + z1_sub_h
z1_top_pad = (ZONE_H - z1_combined) // 2

d.txt("z1_t", LAKE_INNER_X, Z1_Y + z1_top_pad, ZONE_W, z1_title_h,
    z1_title, 24, cid="z1")
d.txt("z1_sub", LAKE_INNER_X, Z1_Y + z1_top_pad + z1_title_h + z1_gap, ZONE_W, z1_sub_h,
    z1_sub, 17, color=RED[0])

# Arrow z1 -> z2
Z2_Y = Z1_Y + ZONE_H + ZONE_GAP
d.arr("a_z1z2", LAKE_INNER_X + ZONE_W // 2, Z1_Y + ZONE_H,
    [[0, 0], [0, ZONE_GAP]],
    RED[0],
    sb={"elementId": "z1", "focus": 0, "gap": 4},
    eb={"elementId": "z2", "focus": 0, "gap": 4})

# === Zone 2: Cleaned/Transformed ===
d.rect("z2", LAKE_INNER_X, Z2_Y, ZONE_W, ZONE_H, *YELLOW,
     bnd=[{"id": "z2_t", "type": "text"}])

z2_title = "Cleaned / Transformed Zone"
z2_sub = "Validated, deduplicated, standardized\nParquet, schema-enforced"
z2_title_h = math.ceil(1 * 24 * 1.25)
z2_sub_h = math.ceil(2 * 17 * 1.25)
z2_combined = z2_title_h + z1_gap + z2_sub_h
z2_top_pad = (ZONE_H - z2_combined) // 2

d.txt("z2_t", LAKE_INNER_X, Z2_Y + z2_top_pad, ZONE_W, z2_title_h,
    z2_title, 24, cid="z2")
d.txt("z2_sub", LAKE_INNER_X, Z2_Y + z2_top_pad + z2_title_h + z1_gap, ZONE_W, z2_sub_h,
    z2_sub, 17, color=YELLOW[0])

# Arrow z2 -> z3
Z3_Y = Z2_Y + ZONE_H + ZONE_GAP
d.arr("a_z2z3", LAKE_INNER_X + ZONE_W // 2, Z2_Y + ZONE_H,
    [[0, 0], [0, ZONE_GAP]],
    YELLOW[0],
    sb={"elementId": "z2", "focus": 0, "gap": 4},
    eb={"elementId": "z3", "focus": 0, "gap": 4})

# === Zone 3: Curated/Enriched ===
d.rect("z3", LAKE_INNER_X, Z3_Y, ZONE_W, ZONE_H, *GREEN,
     bnd=[{"id": "z3_t", "type": "text"}])

z3_title = "Curated / Enriched Zone"
z3_sub = "Business-ready, aggregated, feature-engineered\nReady for analytics and ML"
z3_title_h = math.ceil(1 * 24 * 1.25)
z3_sub_h = math.ceil(2 * 17 * 1.25)
z3_combined = z3_title_h + z1_gap + z3_sub_h
z3_top_pad = (ZONE_H - z3_combined) // 2

d.txt("z3_t", LAKE_INNER_X, Z3_Y + z3_top_pad, ZONE_W, z3_title_h,
    z3_title, 24, cid="z3")
d.txt("z3_sub", LAKE_INNER_X, Z3_Y + z3_top_pad + z3_title_h + z1_gap, ZONE_W, z3_sub_h,
    z3_sub, 17, color=GREEN[0])

# === ARROWS: Sources to Lake ===
for i, (bid, _, _) in enumerate(sources):
    sx = PAD_X + i * (SRC_W + SRC_GAP) + SRC_W // 2
    d.arr(f"a_s{i}", sx, SRC_Y + SRC_H,
        [[0, 0], [0, LAKE_Y - SRC_Y - SRC_H]],
        GRAY[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "lake", "focus": 0, "gap": 4})

# === DATA CATALOG (below lake) ===
CAT_Y = LAKE_Y + LAKE_H + 15
CAT_W = CONTENT_W
CAT_H = 55
d.rect("catalog", PAD_X, CAT_Y, CAT_W, CAT_H, *PURPLE,
     bnd=[{"id": "cat_t", "type": "text"}])
d.txt("cat_t", PAD_X, CAT_Y, CAT_W, CAT_H,
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
d.save(outfile)
print(f"Wrote {outfile}")
