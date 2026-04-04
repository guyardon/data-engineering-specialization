"""
Generate data lakehouse architecture diagram showing how open table formats
bridge the gap between data lake storage and warehouse-grade query performance.
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
seed = 4000


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

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
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
    rect(bid, x, QE_Y, QE_W, QE_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", x, QE_Y, QE_W, QE_H, label, 22, cid=bid)

QE_LABEL_Y = QE_Y + QE_H + 6
QE_LABEL_H = math.ceil(1 * 16 * 1.25)
txt("qe_label", PAD_X, QE_LABEL_Y, CONTENT_W, QE_LABEL_H,
    "Query & Processing Engines", 16, color=PURPLE[0])

# === LAYER 2: Open Table Format (metadata layer) ===
OTF_Y = QE_LABEL_Y + QE_LABEL_H + 40
OTF_H = 95
rect("otf", PAD_X, OTF_Y, CONTENT_W, OTF_H, *YELLOW,
     bnd=[{"id": "otf_t", "type": "text"}])

otf_title = "Open Table Format"
otf_sub = "Delta Lake  /  Apache Iceberg  /  Apache Hudi\nACID transactions, time travel, schema evolution"
otf_title_h = math.ceil(1 * 24 * 1.25)
otf_sub_h = math.ceil(2 * 17 * 1.25)
otf_gap = 6
otf_combined = otf_title_h + otf_gap + otf_sub_h
otf_top_pad = (OTF_H - otf_combined) // 2

txt("otf_t", PAD_X, OTF_Y + otf_top_pad, CONTENT_W, otf_title_h,
    otf_title, 24, cid="otf")
txt("otf_sub", PAD_X, OTF_Y + otf_top_pad + otf_title_h + otf_gap, CONTENT_W, otf_sub_h,
    otf_sub, 17, color=YELLOW[0])

# Arrows from engines to OTF
for i, (bid, _, _) in enumerate(engines):
    sx = PAD_X + i * (QE_W + QE_GAP) + QE_W // 2
    arr(f"a_qe{i}", sx, QE_Y + QE_H,
        [[0, 0], [0, OTF_Y - QE_Y - QE_H]],
        PURPLE[0],
        sb={"elementId": bid, "focus": 0, "gap": 4},
        eb={"elementId": "otf", "focus": 0, "gap": 4})

# === LAYER 3: Object Storage ===
STOR_Y = OTF_Y + OTF_H + 50
STOR_H = 65
rect("storage", PAD_X, STOR_Y, CONTENT_W, STOR_H, *BLUE,
     bnd=[{"id": "stor_t", "type": "text"}])

stor_title = "Object Storage (S3, GCS, ADLS)"
stor_sub = "Parquet / ORC files — cheap, scalable, durable"
stor_title_h = math.ceil(1 * 24 * 1.25)
stor_sub_h = math.ceil(1 * 17 * 1.25)
stor_gap = 4
stor_combined = stor_title_h + stor_gap + stor_sub_h
stor_top_pad = (STOR_H - stor_combined) // 2

txt("stor_t", PAD_X, STOR_Y + stor_top_pad, CONTENT_W, stor_title_h,
    stor_title, 24, cid="storage")
txt("stor_sub", PAD_X, STOR_Y + stor_top_pad + stor_title_h + stor_gap, CONTENT_W, stor_sub_h,
    stor_sub, 17, color=BLUE[0])

# Arrow OTF -> Storage
arr("a_otf_stor", PAD_X + CONTENT_W // 2, OTF_Y + OTF_H,
    [[0, 0], [0, STOR_Y - OTF_Y - OTF_H]],
    YELLOW[0],
    sb={"elementId": "otf", "focus": 0, "gap": 4},
    eb={"elementId": "storage", "focus": 0, "gap": 4})

# === KEY BENEFIT LABELS ===
# Left side label for lake benefit
BENEFIT_Y = OTF_Y + OTF_H + 8
BENEFIT_H = math.ceil(1 * 15 * 1.25)
txt("b_left", PAD_X + 10, BENEFIT_Y, 200, BENEFIT_H,
    "Warehouse-grade queries", 15, color=YELLOW[0])

txt("b_right", PAD_X + CONTENT_W - 210, BENEFIT_Y, 200, BENEFIT_H,
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
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
