#!/usr/bin/env python3
"""Generate monolith-modular.excalidraw — side-by-side comparison diagram."""
import json, math, os

data = {
    "type": "excalidraw", "version": 2,
    "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}
}
els = data["elements"]
seed = 6000

def ns():
    global seed; seed += 1; return seed

def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2):
    els.append({"type":"rectangle","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "strokeColor":stroke,"backgroundColor":bg,"fillStyle":fill,"strokeWidth":sw,
        "strokeStyle":"dashed" if dashed else "solid","roughness":1,"opacity":opacity,
        "roundness":{"type":3},"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":bnd or [],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count('\n') + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "text":t,"originalText":t,"fontSize":sz,"fontFamily":1,
        "textAlign":"center","verticalAlign":"middle","lineHeight":1.25,"autoResize":True,
        "containerId":cid,"strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":1,"opacity":op,
        "seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":[],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({"type":"arrow","id":id,"x":x,"y":y,
        "width":abs(pts[-1][0]-pts[0][0]),"height":abs(pts[-1][1]-pts[0][1]),"angle":0,
        "points":pts,"startArrowhead":None,"endArrowhead":"arrow",
        "startBinding":sb,"endBinding":eb,"elbowed":False,
        "strokeColor":stroke,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":2,"strokeStyle":"dashed" if dash else "solid",
        "roughness":1,"opacity":op,"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":[],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

# ─── Colors ───
RED_S, RED_B = "#c92a2a", "#ffc9c9"
GREEN_S, GREEN_B = "#2f9e44", "#b2f2bb"
GRAY_S, GRAY_B = "#868e96", "#dee2e6"
ARROW_COLOR = "#495057"

# ─── Layout constants ───
TOTAL_W = 700
COL_GAP = 80          # gap between left and right columns

# Monolith block
MONO_W = 220
MONO_H = 250

# Modular small boxes
MOD_W = 100
MOD_H = 55
MOD_GAP_X = 20        # horizontal gap between modular boxes
MOD_GAP_Y = 20        # vertical gap between modular rows

# Starting position
START_X = 50
START_Y = 0

# ─── Title ───
title_w = TOTAL_W
title_h = math.ceil(1 * 28 * 1.25)
title_x = START_X
title_y = START_Y
txt("title", title_x, title_y, title_w, title_h,
    "Monolith vs. Modular Systems", 28, "#1e1e1e")

# ─── Column positions ───
content_y = title_y + title_h + 25  # 25px gap below title

# Left column: Monolith
left_x = START_X
# Right column: Modular — center it in the right half
right_col_start = START_X + MONO_W + COL_GAP

# ─── Left column: "Monolith" label ───
mono_label_h = math.ceil(1 * 22 * 1.25)
mono_label_x = left_x
mono_label_y = content_y
txt("mono_label", mono_label_x, mono_label_y, MONO_W, mono_label_h,
    "Monolith", 22, RED_S)

# ─── Monolith big rectangle ───
mono_rect_y = mono_label_y + mono_label_h + 15
rect("mono_rect", left_x, mono_rect_y, MONO_W, MONO_H, RED_S, RED_B, fill="solid")

# ─── Internal component dividers (dashed lines as thin rects) + labels ───
# Divide the monolith into 4 sections: UI, API, Business Logic, Data Layer
# Each section is ~62.5h (250/4), use dashed separator lines between them
section_h = MONO_H // 4
components = ["UI", "API", "Business\nLogic", "Data Layer"]

for i, comp in enumerate(components):
    comp_y = mono_rect_y + i * section_h
    comp_h = section_h

    # Dashed separator line (except for first section)
    if i > 0:
        rect(f"mono_sep_{i}", left_x + 10, comp_y, MONO_W - 20, 0, GRAY_S, "transparent",
             fill="solid", dashed=True, sw=1)

    # Component label — free text (not bound to monolith rect)
    num_lines = comp.count('\n') + 1
    label_h = math.ceil(num_lines * 16 * 1.25)
    label_y = comp_y + (comp_h - label_h) // 2
    txt(f"mono_comp_{i}", left_x, label_y, MONO_W, label_h,
        comp, 16, GRAY_S)

# ─── Monolith subtitle ───
mono_sub_y = mono_rect_y + MONO_H + 15
mono_sub_h = math.ceil(2 * 16 * 1.25)
txt("mono_sub", left_x, mono_sub_y, MONO_W, mono_sub_h,
    "Single codebase,\ntightly coupled", 16, RED_S)

# ─── Right column: "Modular" label ───
# Calculate modular grid width: 3 columns of boxes
mod_grid_w = 3 * MOD_W + 2 * MOD_GAP_X  # 340
mod_label_h = math.ceil(1 * 22 * 1.25)
mod_label_x = right_col_start
mod_label_y = content_y
txt("mod_label", mod_label_x, mod_label_y, mod_grid_w, mod_label_h,
    "Modular", 22, GREEN_S)

# ─── Modular service boxes ───
# Layout: row 1 = Auth, API, Data; row 2 = Analytics, UI (centered)
services = [
    ("Auth", 0, 0),
    ("API", 1, 0),
    ("Data", 2, 0),
    ("Analytics", 0, 1),
    ("UI", 1, 1),
]

mod_start_y = mod_label_y + mod_label_h + 15
# Offset row 2 to be slightly shifted for visual interest
# Row 2 has 2 items — center them under 3-col grid
row2_offset = (MOD_W + MOD_GAP_X) // 2

service_positions = {}  # store {name: (cx, cy, x, y, w, h)} for arrow connections

for name, col, row in services:
    if row == 1:
        bx = right_col_start + row2_offset + col * (MOD_W + MOD_GAP_X)
    else:
        bx = right_col_start + col * (MOD_W + MOD_GAP_X)
    by = mod_start_y + row * (MOD_H + MOD_GAP_Y)

    box_id = f"mod_{name.lower()}"
    txt_id = f"mod_{name.lower()}_t"

    rect(box_id, bx, by, MOD_W, MOD_H, GREEN_S, GREEN_B, fill="solid",
         bnd=[{"type":"text","id":txt_id}])
    txt(txt_id, bx, by, MOD_W, MOD_H, name, 20, "#1e1e1e", cid=box_id)

    # Store center and bounds for arrows
    service_positions[name] = {
        "x": bx, "y": by, "w": MOD_W, "h": MOD_H,
        "cx": bx + MOD_W // 2, "cy": by + MOD_H // 2,
        "id": box_id,
    }

# ─── Arrows between modular services ───
# Connections: Auth->API, API->Data, Data->Analytics, API->UI
connections = [
    ("Auth", "API", "right", "left"),       # Auth right edge -> API left edge
    ("API", "Data", "right", "left"),        # API right edge -> Data left edge
    ("Data", "Analytics", "bottom", "top"),  # Data bottom -> Analytics top
    ("API", "UI", "bottom", "top"),          # API bottom -> UI top
]

arr_gap = 5  # gap from box edge to arrow start/end

for i, (src, dst, src_side, dst_side) in enumerate(connections):
    s = service_positions[src]
    d = service_positions[dst]

    # Calculate start point based on side
    if src_side == "right":
        sx = s["x"] + s["w"] + arr_gap
        sy = s["cy"]
    elif src_side == "bottom":
        sx = s["cx"]
        sy = s["y"] + s["h"] + arr_gap
    elif src_side == "left":
        sx = s["x"] - arr_gap
        sy = s["cy"]
    else:  # top
        sx = s["cx"]
        sy = s["y"] - arr_gap

    # Calculate end point
    if dst_side == "left":
        ex = d["x"] - arr_gap
        ey = d["cy"]
    elif dst_side == "top":
        ex = d["cx"]
        ey = d["y"] - arr_gap
    elif dst_side == "right":
        ex = d["x"] + d["w"] + arr_gap
        ey = d["cy"]
    else:  # bottom
        ex = d["cx"]
        ey = d["y"] + d["h"] + arr_gap

    # Arrow points are relative to start
    pts = [[0, 0], [ex - sx, ey - sy]]

    sb = {"elementId": s["id"], "focus": 0, "gap": arr_gap}
    eb = {"elementId": d["id"], "focus": 0, "gap": arr_gap}

    arr(f"arr_{i}", sx, sy, pts, ARROW_COLOR, sb=sb, eb=eb)

# ─── Modular subtitle ───
# Position below the second row of boxes
mod_sub_y = mod_start_y + 2 * (MOD_H + MOD_GAP_Y) - MOD_GAP_Y + 15
mod_sub_h = math.ceil(2 * 16 * 1.25)
txt("mod_sub", right_col_start, mod_sub_y, mod_grid_w, mod_sub_h,
    "Independent services,\nloosely coupled", 16, GREEN_S)

# ─── Write output ───
out_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "monolith-modular.excalidraw")
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {os.path.abspath(out_path)}")
print(f"  {len(els)} elements")
