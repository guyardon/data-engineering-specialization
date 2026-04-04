"""
5 Pillars of Data Observability — stacked cards layout.
Each pillar gets a colored card with title + subtitle.
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
seed = 2000


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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True, "containerId": cid,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


# === LAYOUT CONSTANTS ===
CANVAS_W = 620
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 580

# Number label width
NUM_W = 50
CARD_W = CONTENT_W - NUM_W - 15  # 515
CARD_H = 95
CARD_GAP = 15

TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

CARDS_START = TITLE_Y + TITLE_H + 30

# Pillars data
pillars = [
    ("Distribution", "Checks NULL rates, unique percentages,\nsummary stats, and expected ranges", BLUE),
    ("Freshness", "How up-to-date the data is —\nwhen last updated and how frequently", GREEN),
    ("Volume", "Monitors data amounts for\nunexpected spikes or drops", YELLOW),
    ("Lineage", "Traces data journey from source\nto destination to locate errors", PURPLE),
    ("Schema", "Monitors changes in data\nstructure or types", RED),
]

# === BUILD DIAGRAM ===

txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "5 Pillars of Data Observability", 32, color="#1e1e1e")

for i, (name, desc, color) in enumerate(pillars):
    y = CARDS_START + i * (CARD_H + CARD_GAP)
    num_id = f"num{i}"
    card_id = f"card{i}"
    card_t_id = f"card-t{i}"
    sub_id = f"sub{i}"

    # Number circle-ish badge
    rect(num_id, PAD_X, y, NUM_W, CARD_H, color[0], color[1],
         bnd=[{"id": f"num-t{i}", "type": "text"}])
    txt(f"num-t{i}", PAD_X, y, NUM_W, CARD_H,
        str(i + 1), 26, cid=num_id)

    # Card with title + subtitle (Rule 13)
    card_x = PAD_X + NUM_W + 15
    title_text = name
    sub_text = desc

    title_h = math.ceil(1 * 24 * 1.25)  # 30
    sub_lines = sub_text.count("\n") + 1
    sub_h = math.ceil(sub_lines * 17 * 1.25)  # varies
    gap = 6
    combined = title_h + gap + sub_h
    top_pad = (CARD_H - combined) // 2
    title_y = y + top_pad
    sub_y = title_y + title_h + gap

    rect(card_id, card_x, y, CARD_W, CARD_H, color[0], color[1],
         bnd=[{"id": card_t_id, "type": "text"}])
    txt(card_t_id, card_x, title_y, CARD_W, title_h,
        title_text, 24, color="#1e1e1e", cid=card_id)
    txt(sub_id, card_x, sub_y, CARD_W, sub_h,
        sub_text, 17, color=color[0])

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "five-pillars"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
