"""
Generate data lakehouse architecture diagram showing how open table formats
bridge the gap between data lake storage and warehouse-grade query performance.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, YELLOW, PURPLE, GRAY

d = ExcalidrawDiagram(seed=4000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Data Lakehouse Architecture", 32, color="#1e1e1e")

# === LAYER 1: Query Engines (top) ===
QE_Y = TITLE_Y + TITLE_H + 30
QE_H = 55
QE_GAP = 15
QE_W = (CONTENT_W - 2 * QE_GAP) // 3

engines = [
    ("qe1", "BI / SQL", PURPLE),
    ("qe2", "ML / DS", PURPLE),
    ("qe3", "Streaming", PURPLE),
]
for i, (bid, label, color) in enumerate(engines):
    x = PAD_X + i * (QE_W + QE_GAP)
    d.rect(bid, x, QE_Y, QE_W, QE_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", x, QE_Y, QE_W, QE_H, label, 22, cid=bid)

QE_LABEL_Y = QE_Y + QE_H + 6
QE_LABEL_H = math.ceil(1 * 16 * 1.25)
d.txt("qe_label", PAD_X, QE_LABEL_Y, CONTENT_W, QE_LABEL_H,
    "Query & Processing Engines", 16, color=PURPLE[0])

# === LAYER 2: Open Table Format (metadata layer) ===
OTF_Y = QE_LABEL_Y + QE_LABEL_H + 40
OTF_H = 95
d.rect("otf", PAD_X, OTF_Y, CONTENT_W, OTF_H, *YELLOW,
     bnd=[{"id": "otf_t", "type": "text"}])

otf_title = "Open Table Format"
otf_sub = "Delta Lake  /  Apache Iceberg  /  Apache Hudi\nACID transactions, time travel, schema evolution"
otf_title_h = math.ceil(1 * 24 * 1.25)
otf_sub_h = math.ceil(2 * 17 * 1.25)
otf_gap = 6
otf_combined = otf_title_h + otf_gap + otf_sub_h
otf_top_pad = (OTF_H - otf_combined) // 2

d.txt("otf_t", PAD_X, OTF_Y + otf_top_pad, CONTENT_W, otf_title_h,
    otf_title, 24, cid="otf")
d.txt("otf_sub", PAD_X, OTF_Y + otf_top_pad + otf_title_h + otf_gap, CONTENT_W, otf_sub_h,
    otf_sub, 17, color=YELLOW[0])

# Arrows from engines to OTF
for i, (bid, _, _) in enumerate(engines):
    sx = PAD_X + i * (QE_W + QE_GAP) + QE_W // 2
    d.arr(f"a_qe{i}", sx, QE_Y + QE_H,
        [[0, 0], [0, OTF_Y - QE_Y - QE_H]],
        PURPLE[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "otf", "focus": 0, "gap": 4})

# === LAYER 3: Object Storage ===
STOR_Y = OTF_Y + OTF_H + 50
STOR_H = 65
d.rect("storage", PAD_X, STOR_Y, CONTENT_W, STOR_H, *BLUE,
     bnd=[{"id": "stor_t", "type": "text"}])

stor_title = "Object Storage (S3, GCS, ADLS)"
stor_sub = "Parquet / ORC files — cheap, scalable, durable"
stor_title_h = math.ceil(1 * 24 * 1.25)
stor_sub_h = math.ceil(1 * 17 * 1.25)
stor_gap = 4
stor_combined = stor_title_h + stor_gap + stor_sub_h
stor_top_pad = (STOR_H - stor_combined) // 2

d.txt("stor_t", PAD_X, STOR_Y + stor_top_pad, CONTENT_W, stor_title_h,
    stor_title, 24, cid="storage")
d.txt("stor_sub", PAD_X, STOR_Y + stor_top_pad + stor_title_h + stor_gap, CONTENT_W, stor_sub_h,
    stor_sub, 17, color=BLUE[0])

# Arrow OTF -> Storage
d.arr("a_otf_stor", PAD_X + CONTENT_W // 2, OTF_Y + OTF_H,
    [[0, 0], [0, STOR_Y - OTF_Y - OTF_H]],
    YELLOW[0],
    sb={"elementId": "otf", "focus": 0, "gap": 4},
    eb={"elementId": "storage", "focus": 0, "gap": 4})

# === KEY BENEFIT LABELS ===
# Left side label for lake benefit
BENEFIT_Y = OTF_Y + OTF_H + 8
BENEFIT_H = math.ceil(1 * 15 * 1.25)
d.txt("b_left", PAD_X + 10, BENEFIT_Y, 200, BENEFIT_H,
    "Warehouse-grade queries", 15, color=YELLOW[0])

d.txt("b_right", PAD_X + CONTENT_W - 210, BENEFIT_Y, 200, BENEFIT_H,
    "Lake-grade storage cost", 15, color=BLUE[0])

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{STOR_Y + STOR_H + 20}")
print(f"Title: y={TITLE_Y}")
print(f"Engines: y={QE_Y} to {QE_Y + QE_H}")
print(f"OTF: y={OTF_Y} to {OTF_Y + OTF_H}")
print(f"Storage: y={STOR_Y} to {STOR_Y + STOR_H}")

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "lakehouse-architecture"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
