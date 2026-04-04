"""
Evolution of Orchestration Tools — horizontal timeline with alternating milestone boxes.
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


def line(id, x, y, pts, stroke, dash=False, op=100):
    els.append({
        "type": "line", "id": id, "x": x, "y": y,
        "width": abs(pts[-1][0] - pts[0][0]), "height": abs(pts[-1][1] - pts[0][1]),
        "angle": 0, "points": pts,
        "startArrowhead": None, "endArrowhead": None,
        "startBinding": None, "endBinding": None, "elbowed": False,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dash else "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({
        "type": "arrow", "id": id, "x": x, "y": y,
        "width": pts[-1][0] - pts[0][0], "height": pts[-1][1] - pts[0][1],
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
CANVAS_W = 700
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 660

# Title
TITLE_Y = 15
TITLE_H = math.ceil(32 * 1.25)  # 40

# Timeline axis
TIMELINE_Y = 260  # vertical center for the horizontal line
TIMELINE_X0 = PAD_X + 10
TIMELINE_X1 = CANVAS_W - PAD_X - 10

# Milestone boxes
BOX_W = 110
BOX_H = 80
STEM_H = 40  # vertical connector from timeline to box
BOX_GAP_ABOVE = 10  # gap between stem end and box

# Milestones: (title, subtitle, color, above_or_below)
# Alternate above/below for visual variety
milestones = [
    ("Dataswarm", "Late 2000s\nFacebook", GRAY, "above"),
    ("Apache Oozie", "2010s\nHadoop-only", YELLOW, "below"),
    ("Airflow", "2014\nAirbnb", BLUE, "above"),
    ("Apache Airflow", "2019\nTop-level project", GREEN, "below"),
    ("Prefect, Dagster\nMage", "Today\nModern tools", PURPLE, "above"),
]

N = len(milestones)
# Distribute milestones evenly along the timeline
usable_w = TIMELINE_X1 - TIMELINE_X0 - 40  # leave room for arrow tip
spacing = usable_w / (N - 1) if N > 1 else 0
first_x = TIMELINE_X0 + 20  # offset from start

# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Evolution of Orchestration Tools", 32, color="#1e1e1e")

# Timeline arrow (horizontal, left to right)
arr("timeline", TIMELINE_X0, TIMELINE_Y, [[0, 0], [TIMELINE_X1 - TIMELINE_X0, 0]],
    GRAY[0])

# Milestone boxes and connectors
for i, (name, sub, color, pos) in enumerate(milestones):
    cx = first_x + i * spacing  # center x of this milestone on timeline
    box_x = cx - BOX_W // 2

    card_id = f"card{i}"
    card_t_id = f"card-t{i}"
    sub_id = f"sub{i}"
    stem_id = f"stem{i}"
    dot_id = f"dot{i}"

    if pos == "above":
        # Box above timeline
        box_y = TIMELINE_Y - STEM_H - BOX_H - BOX_GAP_ABOVE
        stem_y1 = TIMELINE_Y
        stem_y0 = box_y + BOX_H + BOX_GAP_ABOVE
        line(stem_id, cx, stem_y0, [[0, 0], [0, stem_y1 - stem_y0]], color[0])
    else:
        # Box below timeline
        box_y = TIMELINE_Y + STEM_H + BOX_GAP_ABOVE
        stem_y0 = TIMELINE_Y
        stem_y1 = box_y - BOX_GAP_ABOVE
        line(stem_id, cx, stem_y0, [[0, 0], [0, stem_y1 - stem_y0]], color[0])

    # Small dot on the timeline
    dot_sz = 10
    rect(dot_id, cx - dot_sz // 2, TIMELINE_Y - dot_sz // 2, dot_sz, dot_sz,
         color[0], color[1])

    # Card with bound title text (Rule 13) + free subtitle
    title_h = math.ceil((name.count("\n") + 1) * 22 * 1.25)
    sub_lines = sub.count("\n") + 1
    sub_h = math.ceil(sub_lines * 17 * 1.25)
    gap = 4
    combined = title_h + gap + sub_h
    top_pad = (BOX_H - combined) // 2
    title_y = box_y + top_pad
    sub_y = title_y + title_h + gap

    rect(card_id, box_x, box_y, BOX_W, BOX_H, color[0], color[1],
         bnd=[{"id": card_t_id, "type": "text"}])
    txt(card_t_id, box_x, title_y, BOX_W, title_h,
        name, 22, color="#1e1e1e", cid=card_id)
    txt(sub_id, box_x, sub_y, BOX_W, sub_h,
        sub, 17, color=color[0])

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "orchestration-timeline"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
