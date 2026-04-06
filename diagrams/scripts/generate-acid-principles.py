import math

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, YELLOW

d = ExcalidrawDiagram(seed=4000)

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
d.txt("title", 0, title_y, CANVAS_W, title_h, "ACID Principles", TITLE_FONT)

# ── Cards ──
cards = [
    (
        "Atomicity",
        "All or nothing — transactions fully complete or fully roll back",
        BLUE,
    ),
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
    d.rect(
        card_id,
        PAD_X,
        card_y,
        CONTENT_W,
        CARD_H,
        stroke,
        bg,
        bnd=[{"type": "text", "id": title_id}],
    )

    # Bound title (Rule 13) — positioned in upper portion of card
    d.txt(
        title_id, PAD_X, card_y, CONTENT_W, CARD_H, title, CARD_TITLE_FONT, cid=card_id
    )

    # Free subtitle below title, stroke-colored (Rule 14)
    sub_h = math.ceil(1 * CARD_SUB_FONT * 1.25)
    sub_y = card_y + CARD_H // 2 + 10
    d.txt(sub_id, PAD_X, sub_y, CONTENT_W, sub_h, subtitle, CARD_SUB_FONT, color=stroke)

# ── Write output ──
out = "diagrams/artifacts/acid-principles.excalidraw"
d.save(out)
print(f"Written to {out}")
