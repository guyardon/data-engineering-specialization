"""
Storage tiers diagram with AWS S3 classes.
Shows Hot -> Warm -> Cold tiers vertically, each containing its S3 classes as pills.
Follows skill layout rules: Rule 4 (box padding), Rule 7 (container padding),
Rule 12 (identical dims), Rule 15 (font sizes), Rule 16 (vertical flow),
Rule 24 (widths from canvas).

Canvas: 650px wide (narrow for vertical aspect ratio).
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, YELLOW, RED, GRAY

d = ExcalidrawDiagram(seed=5000)

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
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Storage Tiers & AWS S3 Classes", 32)
d.txt(
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
    d.rect(
        tier_id, PAD_X, y, CONTENT_W, container_h, *color, fill="hachure", dashed=True
    )

    # Title text (Rule 13: title + subtitle as two elements)
    d.txt(
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
    d.txt(
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
        d.rect(
            pid,
            px,
            pill_y,
            pill_w,
            PILL_H,
            *color,
            fill="hachure",
            bnd=[{"id": tid, "type": "text"}],
        )
        d.txt(tid, px, pill_y, pill_w, PILL_H, label, 18, cid=pid)

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

# Arrow hot -> warm
d.arr(
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

# Arrow warm -> cold
d.arr(
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
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/storage-tiers"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
