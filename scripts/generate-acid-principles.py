import json, math, sys

data = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
}
els = data["elements"]
seed = 4000

def ns():
    global seed; seed += 1; return seed

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")

def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append({"type": "rectangle", "id": id, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": stroke, "backgroundColor": bg, "fillStyle": fill, "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": opacity, "roundness": {"type": 3}, "seed": ns(), "version": 1, "versionNonce": ns(), "isDeleted": False, "groupIds": [], "boundElements": bnd or [], "frameId": None, "link": None, "locked": False, "updated": 1710000000000})

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({"type": "text", "id": id, "x": x, "y": y, "width": w, "height": h, "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1, "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25, "autoResize": True, "containerId": cid, "strokeColor": color, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": op, "seed": ns(), "version": 1, "versionNonce": ns(), "isDeleted": False, "groupIds": [], "boundElements": [], "frameId": None, "link": None, "locked": False, "updated": 1710000000000})

# ── Layout constants ──
CANVAS_W = 700
PAD_X = 40
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620
CARD_H = 95
CARD_GAP = 30
TITLE_FONT = 32
CARD_TITLE_FONT = 24
CARD_SUB_FONT = 17

# ── Title ──
title_y = 20
title_h = math.ceil(1 * TITLE_FONT * 1.25)
txt("title", 0, title_y, CANVAS_W, title_h, "ACID Principles", TITLE_FONT)

# ── Cards ──
cards = [
    ("Atomicity", "All or nothing — transactions fully complete or fully roll back", BLUE),
    ("Consistency", "Transactions maintain data integrity", GREEN),
    ("Isolation", "Concurrent transactions execute independently", YELLOW),
    ("Durability", "Completed transactions remain permanent", PURPLE),
]

start_y = title_y + title_h + 35  # Rule 18: 25-30px title-to-content gap (increased)

for i, (title, subtitle, (stroke, bg)) in enumerate(cards):
    card_y = start_y + i * (CARD_H + CARD_GAP)
    card_id = f"card_{i}"
    title_id = f"card_title_{i}"
    sub_id = f"card_sub_{i}"

    # Rectangle with bound text
    rect(card_id, PAD_X, card_y, CONTENT_W, CARD_H, stroke, bg, fill="solid",
         bnd=[{"type": "text", "id": title_id}])

    # Bound title (Rule 13) — positioned in upper portion of card
    txt(title_id, PAD_X, card_y, CONTENT_W, CARD_H, title, CARD_TITLE_FONT, cid=card_id)

    # Free subtitle below title, stroke-colored (Rule 14)
    sub_h = math.ceil(1 * CARD_SUB_FONT * 1.25)
    sub_y = card_y + CARD_H // 2 + 10
    txt(sub_id, PAD_X, sub_y, CONTENT_W, sub_h, subtitle, CARD_SUB_FONT, color=stroke)

# ── Write output ──
out = "diagrams/acid-principles.excalidraw"
with open(out, "w") as f:
    json.dump(data, f, indent=2)
print(f"Written to {out}")
