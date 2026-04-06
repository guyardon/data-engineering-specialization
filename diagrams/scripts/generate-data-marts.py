"""Generate data-marts.excalidraw — Data Warehouse breaking down into Data Marts."""

import math

from diagramlib import ExcalidrawDiagram

d = ExcalidrawDiagram(seed=5000)

# ── Layout constants ──────────────────────────────────────────────
dw_w, dw_h = 300, 65
dm_w, dm_h = 150, 70
dm_gap = 20
n_marts = 4
row_w = n_marts * dm_w + (n_marts - 1) * dm_gap  # 660

# Center everything: treat row_w as the reference width
canvas_cx = row_w / 2  # 330

title_y = 20
dw_y = 90
dm_y = 215

dw_x = canvas_cx - dw_w / 2  # 180
dm_start_x = 0  # row starts at 0

# ── Title ─────────────────────────────────────────────────────────
title_text = "Data Warehouse → Data Marts"
title_sz = 28
title_h = math.ceil(1 * title_sz * 1.25)
d.txt("title", 0, title_y, row_w, title_h, title_text, title_sz)

# ── Data Warehouse box ────────────────────────────────────────────
# Build boundElements list for DW (one entry per arrow)
dw_arrow_ids = [f"arr-dm{i}" for i in range(1, n_marts + 1)]
dw_bound = [{"id": aid, "type": "arrow"} for aid in dw_arrow_ids]
dw_bound.append({"id": "dw-text", "type": "text"})

d.rect("dw", dw_x, dw_y, dw_w, dw_h, "#e67700", "#ffec99", bnd=dw_bound)
d.txt("dw-text", dw_x, dw_y, dw_w, dw_h, "Data Warehouse", 22, cid="dw")

# ── Data Mart boxes ───────────────────────────────────────────────
mart_labels = [
    "Data Mart #1\n[Marketing]",
    "Data Mart #2\n[Finance]",
    "Data Mart #3\n[Sales]",
    "Data Mart #4\n[Operations]",
]

for i, label in enumerate(mart_labels):
    dm_id = f"dm{i + 1}"
    dm_text_id = f"dm{i + 1}-text"
    arr_id = f"arr-dm{i + 1}"
    dm_x = dm_start_x + i * (dm_w + dm_gap)

    dm_bound = [
        {"id": arr_id, "type": "arrow"},
        {"id": dm_text_id, "type": "text"},
    ]
    d.rect(dm_id, dm_x, dm_y, dm_w, dm_h, "#0c8599", "#99e9f2", bnd=dm_bound)
    d.txt(dm_text_id, dm_x, dm_y, dm_w, dm_h, label, 18, cid=dm_id)

# ── Arrows from DW to each Data Mart ─────────────────────────────
dw_bottom_cx = dw_x + dw_w / 2
dw_bottom_cy = dw_y + dw_h

for i in range(n_marts):
    dm_id = f"dm{i + 1}"
    arr_id = f"arr-dm{i + 1}"
    dm_x = dm_start_x + i * (dm_w + dm_gap)
    dm_top_cx = dm_x + dm_w / 2
    dm_top_cy = dm_y

    # Arrow starts at DW bottom-center, ends at DM top-center
    start_x = dw_bottom_cx
    start_y = dw_bottom_cy
    dx = dm_top_cx - start_x
    dy = dm_top_cy - start_y

    sb = {"elementId": "dw", "focus": 0, "gap": 1, "fixedPoint": None}
    eb = {"elementId": dm_id, "focus": 0, "gap": 1, "fixedPoint": None}
    d.arr(arr_id, start_x, start_y, [[0, 0], [dx, dy]], "#495057", sb=sb, eb=eb)

# ── Write file ────────────────────────────────────────────────────
outfile = "diagrams/artifacts/data-marts.excalidraw"
d.save(outfile)
print(f"Written: {outfile}")
