"""
Storage tiers diagram with AWS S3 classes.
Shows Hot → Warm → Cold tiers vertically, each containing its S3 classes as pills.
Follows skill layout rules: Rule 4 (box padding), Rule 7 (container padding),
Rule 12 (identical dims), Rule 15 (font sizes), Rule 16 (vertical flow),
Rule 24 (widths from canvas).

Canvas: 650px wide (narrow for vertical aspect ratio).
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
seed = 5000


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


def rect(
    id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None
):
    els.append(
        {
            "type": "rectangle",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 3},
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append(
        {
            "type": "text",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "text": t,
            "originalText": t,
            "fontSize": sz,
            "fontFamily": 1,
            "textAlign": align,
            "verticalAlign": "middle",
            "lineHeight": 1.25,
            "autoResize": True,
            "containerId": cid,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# === LAYOUT CONSTANTS ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X  # Rule 24: derive widths from canvas
INNER_PAD = 25  # Rule 7: container internal padding
LABEL_H = 28  # label text height
PILL_H = 45  # Rule 4: enough height for text + padding
PILL_GAP = 12  # gap between pills
ARROW_GAP = 70  # Rule 17: min 70px arrow gap

# Title
TITLE_Y = 15
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Storage Tiers & AWS S3 Classes", 32)
txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Trading access speed for cost",
    17,
    color=BLUE[0],
)


# === TIER BUILDER ===
def build_tier(tier_id, y, title, subtitle, color, s3_classes):
    """
    Build a tier container with a title/subtitle header and a row of S3 class pills.
    Returns the bottom y of the container.
    """
    # Calculate pill row width -- all pills identical width (Rule 12)
    n = len(s3_classes)
    pill_w = (CONTENT_W - 2 * INNER_PAD - (n - 1) * PILL_GAP) // n

    # Container height: pad + label + subtitle gap + pill + pad
    container_h = INNER_PAD + LABEL_H + 18 + PILL_H + INNER_PAD

    # Dashed container (Rule 7)
    rect(tier_id, PAD_X, y, CONTENT_W, container_h, *color, dashed=True)

    # Title text (Rule 13: title + subtitle as two elements)
    txt(
        f"{tier_id}_title",
        PAD_X + INNER_PAD,
        y + INNER_PAD - 5,
        CONTENT_W - 2 * INNER_PAD,
        LABEL_H,
        title,
        22,
        color=color[0],
    )

    # Subtitle (Rule 14: subtitle color = stroke color)
    txt(
        f"{tier_id}_sub",
        PAD_X + INNER_PAD,
        y + INNER_PAD + LABEL_H - 8,
        CONTENT_W - 2 * INNER_PAD,
        20,
        subtitle,
        17,
        color=color[0],
        op=70,
    )

    # Pills row
    pill_y = y + INNER_PAD + LABEL_H + 18
    pill_start_x = PAD_X + INNER_PAD

    for i, label in enumerate(s3_classes):
        px = pill_start_x + i * (pill_w + PILL_GAP)
        pid = f"{tier_id}_p{i}"
        tid = f"{tier_id}_pt{i}"
        rect(pid, px, pill_y, pill_w, PILL_H, *color, bnd=[{"id": tid, "type": "text"}])
        txt(tid, px, pill_y, pill_w, PILL_H, label, 18, cid=pid)

    return y + container_h


# === BUILD TIERS (vertical flow, Rule 16) ===

# Hot tier
Y = 90
hot_bottom = build_tier(
    "hot",
    Y,
    "Hot Storage",
    "Frequent access · SSD & memory · High cost",
    RED,
    ["S3 Express\nOne Zone", "S3 Standard"],
)

# Arrow hot → warm
arr(
    "a_hw",
    PAD_X + CONTENT_W // 2,
    hot_bottom,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "hot", "focus": 0, "gap": 4},
    eb={"elementId": "warm", "focus": 0, "gap": 4},
)

# Warm tier
warm_bottom = build_tier(
    "warm",
    hot_bottom + ARROW_GAP,
    "Warm Storage",
    "Less frequent · Magnetic / hybrid disks · Medium cost",
    YELLOW,
    ["S3 Standard-IA", "S3 One Zone-IA"],
)

# Arrow warm → cold
arr(
    "a_wc",
    PAD_X + CONTENT_W // 2,
    warm_bottom,
    [[0, 0], [0, ARROW_GAP]],
    GRAY[0],
    sb={"elementId": "warm", "focus": 0, "gap": 4},
    eb={"elementId": "cold", "focus": 0, "gap": 4},
)

# Cold tier
cold_bottom = build_tier(
    "cold",
    warm_bottom + ARROW_GAP,
    "Cold Storage",
    "Infrequent / archive · Low-cost disks · High retrieval cost",
    BLUE,
    [
        "Glacier Instant\nRetrieval",
        "Glacier Flexible\nRetrieval",
        "Glacier Deep\nArchive",
    ],
)

# === VERIFY ===
print(f"Hot:  {Y}-{hot_bottom}")
print(f"Warm: {hot_bottom + ARROW_GAP}-{warm_bottom}")
print(f"Cold: {warm_bottom + ARROW_GAP}-{cold_bottom}")
print(f"Total height: {cold_bottom}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "storage-tiers"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
