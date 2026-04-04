"""Generate cost-optimization.excalidraw — Cost Optimization & Business Value diagram."""

import json, math, os

data = {
    "type": "excalidraw", "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {}
}
els = data["elements"]
seed = 7000

def ns():
    global seed; seed += 1; return seed

def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2):
    els.append({
        "type": "rectangle", "id": id, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": bg, "fillStyle": fill, "strokeWidth": sw,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": opacity,
        "roundness": {"type": 3}, "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": bnd or [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000
    })

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count('\n') + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25, "autoResize": True,
        "containerId": cid, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1,
        "opacity": op, "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000
    })

def divider_line(id, x, y, w, stroke="#868e96", op=40):
    els.append({
        "type": "line", "id": id, "x": x, "y": y,
        "width": w, "height": 0, "angle": 0,
        "points": [[0, 0], [w, 0]],
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "dashed", "roughness": 1,
        "opacity": op, "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
        "startArrowhead": None, "endArrowhead": None,
        "startBinding": None, "endBinding": None
    })

def dual_box(prefix, x, y, w, h, stroke, bg, title_text, sub_text, dashed=False):
    """Create a box with bound title + free subtitle (Rule 13/14)."""
    box_id = f"{prefix}-box"
    title_id = f"{prefix}-title"
    sub_id = f"{prefix}-sub"

    title_lines = title_text.count('\n') + 1
    sub_lines = sub_text.count('\n') + 1
    title_h = math.ceil(title_lines * 20 * 1.25)
    sub_h = math.ceil(sub_lines * 14 * 1.25)
    gap = 6
    combined = title_h + gap + sub_h
    top_pad = (h - combined) // 2

    title_y = y + top_pad
    sub_y = title_y + title_h + gap

    rect(box_id, x, y, w, h, stroke, bg, dashed=dashed,
         bnd=[{"id": title_id, "type": "text"}])
    txt(title_id, x, title_y, w, title_h, title_text, 20, color="#1e1e1e", cid=box_id)
    txt(sub_id, x, sub_y, w, sub_h, sub_text, 14, color=stroke)


# === LAYOUT CONSTANTS ===
CANVAS_W = 700           # wide canvas — blocks fill full width
PAD_X = 20               # left/right margin
CONTENT_W = CANVAS_W - 2 * PAD_X  # 660
WIDE_W = CONTENT_W       # wide header boxes span full width
WIDE_H = 60              # wide header height
PAIR_GAP = 24            # horizontal gap between pair boxes
PAIR_W = (CONTENT_W - PAIR_GAP) // 2  # each pair box fills half width
PAIR_H = 85              # taller pair boxes for proper text padding
SECTION_GAP = 30         # vertical gap between sections
DIVIDER_GAP = 16         # gap before/after divider

LEFT_X = PAD_X
RIGHT_X = LEFT_X + PAIR_W + PAIR_GAP
WIDE_X = PAD_X

# === COLORS ===
TCO_STROKE, TCO_BG = "#e67700", "#ffec99"
BLUE_STROKE, BLUE_BG = "#1971c2", "#a5d8ff"
PURPLE_STROKE, PURPLE_BG = "#6741d9", "#d0bfff"
GREEN_STROKE, GREEN_BG = "#2f9e44", "#b2f2bb"
TOCO_STROKE, TOCO_BG = "#c92a2a", "#ffc9c9"
CYAN_STROKE, CYAN_BG = "#0c8599", "#99e9f2"
FINOPS_STROKE, FINOPS_BG = "#e67700", "#fff3bf"

# === TITLE ===
TITLE_Y = 20
TITLE_FONT = 24
title_text = "Cost Optimization &\nBusiness Value"
title_lines = 2
title_h = math.ceil(title_lines * TITLE_FONT * 1.25)
txt("diagram-title", 0, TITLE_Y, CANVAS_W, title_h,
    title_text, TITLE_FONT, color="#1e1e1e")

# === SECTION 1: TCO ===
y = TITLE_Y + title_h + 25  # Rule 18: 25px title-to-content gap

# TCO header (wide, single-line title — use dual_box with subtitle as concept)
dual_box("tco", WIDE_X, y, WIDE_W, WIDE_H, TCO_STROKE, TCO_BG,
         "Total Cost of Ownership (TCO)", "")

# Override: TCO is a simple header — replace with just bound title, no subtitle
# Actually, let's keep it simple: single title in the wide box
els.clear()
seed = 7000  # reset

# Re-create everything properly
# Title
title_h = math.ceil(2 * TITLE_FONT * 1.25)
txt("diagram-title", 0, TITLE_Y, CANVAS_W, title_h,
    "Cost Optimization &\nBusiness Value", TITLE_FONT, color="#1e1e1e")

# === Section 1: TCO header + Direct/Indirect pair ===
y = TITLE_Y + title_h + 25

# TCO wide header (just a title, no subtitle)
tco_h = 55
rect("tco-box", WIDE_X, y, WIDE_W, tco_h, TCO_STROKE, TCO_BG,
     bnd=[{"id": "tco-title", "type": "text"}])
txt("tco-title", WIDE_X, y, WIDE_W, tco_h,
    "Total Cost of\nOwnership (TCO)", 20, color="#1e1e1e", cid="tco-box")

y += tco_h + 16  # small gap to paired boxes below

# Direct Costs / Indirect Costs
dual_box("direct", LEFT_X, y, PAIR_W, PAIR_H, BLUE_STROKE, BLUE_BG,
         "Direct Costs", "Salaries, cloud bills,\nsoftware subscriptions")
dual_box("indirect", RIGHT_X, y, PAIR_W, PAIR_H, BLUE_STROKE, BLUE_BG,
         "Indirect Costs", "Downtime, IT support,\nlost productivity")

y += PAIR_H

# === Divider 1 ===
y += DIVIDER_GAP
divider_line("div1", LEFT_X + 20, y, WIDE_W - 40)
y += DIVIDER_GAP

# === Section 2: CapEx vs OpEx ===
# Section label
label_h = math.ceil(1 * 20 * 1.25)
txt("capex-opex-label", LEFT_X, y, WIDE_W, label_h,
    "CapEx vs OpEx", 20, color="#868e96")
y += label_h + 12

# CapEx / OpEx pair
dual_box("capex", LEFT_X, y, PAIR_W, PAIR_H, PURPLE_STROKE, PURPLE_BG,
         "CapEx", "Upfront payments\nfor fixed assets")
dual_box("opex", RIGHT_X, y, PAIR_W, PAIR_H, GREEN_STROKE, GREEN_BG,
         "OpEx", "Pay-as-you-go\nday-to-day costs")

y += PAIR_H

# === Divider 2 ===
y += DIVIDER_GAP
divider_line("div2", LEFT_X + 20, y, WIDE_W - 40)
y += DIVIDER_GAP

# === Section 3: TOCO header + Immutable/Transitory pair ===
toco_h = 70
# TOCO header with subtitle
toco_title = "TOCO"
toco_sub = "Total Opportunity Cost\nof Ownership"
title_lines_t = 1
sub_lines_t = 2
t_title_h = math.ceil(title_lines_t * 20 * 1.25)
t_sub_h = math.ceil(sub_lines_t * 14 * 1.25)
gap = 6
combined = t_title_h + gap + t_sub_h
top_pad = (toco_h - combined) // 2
title_y_t = y + top_pad
sub_y_t = title_y_t + t_title_h + gap

rect("toco-box", WIDE_X, y, WIDE_W, toco_h, TOCO_STROKE, TOCO_BG,
     bnd=[{"id": "toco-title", "type": "text"}])
txt("toco-title", WIDE_X, title_y_t, WIDE_W, t_title_h,
    toco_title, 20, color="#1e1e1e", cid="toco-box")
txt("toco-sub", WIDE_X, sub_y_t, WIDE_W, t_sub_h,
    toco_sub, 14, color=TOCO_STROKE)

y += toco_h + 16

# Immutable / Transitory pair
dual_box("immutable", LEFT_X, y, PAIR_W, PAIR_H, CYAN_STROKE, CYAN_BG,
         "Immutable Tech", "Object storage,\nnetworking, SQL")
dual_box("transitory", RIGHT_X, y, PAIR_W, PAIR_H, CYAN_STROKE, CYAN_BG,
         "Transitory Tech", "Stream processing,\norchestration, AI")

y += PAIR_H

# === Divider 3 ===
y += DIVIDER_GAP
divider_line("div3", LEFT_X + 20, y, WIDE_W - 40)
y += DIVIDER_GAP

# === Section 4: FinOps (dashed border) ===
finops_h = 75
dual_box("finops", WIDE_X, y, WIDE_W, finops_h, FINOPS_STROKE, FINOPS_BG,
         "FinOps", "Minimize TCO + TOCO,\nmaximize revenue")
# Make FinOps box dashed — need to update the rect we just created
for el in els:
    if el.get("id") == "finops-box":
        el["strokeStyle"] = "dashed"
        break

# === VERIFY NO OVERLAPS ===
print("=== Element positions ===")
for el in els:
    if el["type"] in ("rectangle", "text", "line"):
        bottom = el["y"] + el.get("height", 0)
        print(f"  {el['id']:25s}  type={el['type']:10s}  y={el['y']:.0f}  h={el.get('height',0):.0f}  bottom={bottom:.0f}")

print(f"\nDiagram total height: {y + finops_h - TITLE_Y:.0f}px")
print(f"Canvas width: {CANVAS_W}px, Content width: {CONTENT_W}px")

# === WRITE FILE ===
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "cost-optimization.excalidraw")
with open(out_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nWritten to: {out_path}")
