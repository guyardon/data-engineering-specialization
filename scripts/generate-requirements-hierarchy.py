import math

from diagramlib import ExcalidrawDiagram

d = ExcalidrawDiagram(seed=3000)


def th(text, font_size):
    return math.ceil((text.count("\n") + 1) * font_size * 1.25)


# ── Layout constants ──
CANVAS_W = 860
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 560

CARD_W = CONTENT_W
CARD_GAP = 60  # room for arrows between cards
FONT_TITLE = 22
FONT_SUB = 16
SUB_GAP = 6

# Sub-requirement cards (functional / non-functional) under System Requirements
SUB_CARD_GAP = 16
SUB_CARD_W = (CONTENT_W - SUB_CARD_GAP) // 2  # 272 each

# ── Title ──
TITLE_Y = 0
MAIN_TITLE_H = 70
TITLE_GAP = 25
START_Y = TITLE_Y + MAIN_TITLE_H + TITLE_GAP

d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    MAIN_TITLE_H,
    "Requirements Hierarchy\nof Needs",
    28,
)

# ── Card data (top to bottom) ──
cards = [
    {
        "id": "biz",
        "title": "Business Goals",
        "subtitle": "Revenue, market share,\nuser growth",
        "stroke": "#1971c2",
        "bg": "#a5d8ff",
    },
    {
        "id": "stake",
        "title": "Stakeholder Needs",
        "subtitle": "Resources, tools,\ndata systems",
        "stroke": "#2f9e44",
        "bg": "#b2f2bb",
    },
    {
        "id": "sys",
        "title": "System Requirements",
        "subtitle": None,
        "stroke": "#6741d9",
        "bg": "#d0bfff",
    },
]

# Calculate card heights
for c in cards:
    title_h = th(c["title"], FONT_TITLE)
    if c["subtitle"]:
        sub_h = th(c["subtitle"], FONT_SUB)
        c["h"] = max(90, title_h + SUB_GAP + sub_h + 30)
    else:
        c["h"] = max(60, title_h + 30)

# ── Build main cards with arrows ──
cur_y = START_Y
card_positions = {}

for i, c in enumerate(cards):
    card_id = c["id"]
    title_id = f"{card_id}_title"
    sub_id = f"{card_id}_sub"
    h = c["h"]

    # Arrow bindings
    bnd = [{"type": "text", "id": title_id}]
    if i > 0:
        bnd.append({"type": "arrow", "id": f"arr_{cards[i-1]['id']}_{card_id}"})
    if i < len(cards) - 1:
        bnd.append({"type": "arrow", "id": f"arr_{card_id}_{cards[i+1]['id']}"})

    d.rect(card_id, PAD_X, cur_y, CARD_W, h, c["stroke"], c["bg"], bnd=bnd)

    if c["subtitle"]:
        title_h = th(c["title"], FONT_TITLE)
        sub_h = th(c["subtitle"], FONT_SUB)
        combined = title_h + SUB_GAP + sub_h
        top_pad = (h - combined) // 2

        title_y = cur_y + top_pad
        sub_y = title_y + title_h + SUB_GAP

        d.txt(
            title_id,
            PAD_X,
            title_y,
            CARD_W,
            title_h,
            c["title"],
            FONT_TITLE,
            color="#1e1e1e",
            cid=card_id,
        )
        d.txt(
            sub_id,
            PAD_X,
            sub_y,
            CARD_W,
            sub_h,
            c["subtitle"],
            FONT_SUB,
            color=c["stroke"],
            valign="top",
        )
    else:
        title_h = th(c["title"], FONT_TITLE)
        centered_y = cur_y + (h - title_h) // 2
        d.txt(
            title_id,
            PAD_X,
            centered_y,
            CARD_W,
            title_h,
            c["title"],
            FONT_TITLE,
            color="#1e1e1e",
            cid=card_id,
        )

    card_positions[card_id] = {"y": cur_y, "h": h}
    cur_y += h + CARD_GAP

# ── Arrows between main cards ──
for i in range(len(cards) - 1):
    src = cards[i]
    tgt = cards[i + 1]
    arrow_id = f"arr_{src['id']}_{tgt['id']}"
    src_bottom = card_positions[src["id"]]["y"] + card_positions[src["id"]]["h"]
    tgt_top = card_positions[tgt["id"]]["y"]
    cx = PAD_X + CARD_W // 2

    sb = {"elementId": src["id"], "focus": 0, "gap": 4, "fixedPoint": None}
    eb = {"elementId": tgt["id"], "focus": 0, "gap": 4, "fixedPoint": None}

    d.arr(
        arrow_id,
        cx,
        src_bottom,
        [[0, 0], [0, tgt_top - src_bottom]],
        "#868e96",
        sb=sb,
        eb=eb,
    )

# ── Sub-cards for System Requirements (Functional / Non-functional) ──
sys_bottom = card_positions["sys"]["y"] + card_positions["sys"]["h"]
sub_top = sys_bottom + CARD_GAP

sub_cards = [
    {
        "id": "func",
        "title": "Functional",
        "subtitle": "Specific functionality\nthe system must provide",
        "stroke": "#c92a2a",
        "bg": "#ffc9c9",
    },
    {
        "id": "nonfunc",
        "title": "Non-Functional",
        "subtitle": "Latency, scalability,\nreliability, cost, security",
        "stroke": "#e67700",
        "bg": "#ffec99",
    },
]

# Calculate sub-card heights
for sc in sub_cards:
    title_h = th(sc["title"], FONT_TITLE)
    sub_h = th(sc["subtitle"], FONT_SUB)
    sc["h"] = max(90, title_h + SUB_GAP + sub_h + 30)  # type: ignore

sub_h_max = max(sc["h"] for sc in sub_cards)
for sc in sub_cards:
    sc["h"] = sub_h_max  # uniform height

# Place sub-cards side by side
left_x = PAD_X
right_x = PAD_X + SUB_CARD_W + SUB_CARD_GAP

for j, sc in enumerate(sub_cards):
    sc_x = left_x if j == 0 else right_x
    sc_id = sc["id"]
    title_id = f"{sc_id}_title"
    sub_id = f"{sc_id}_sub"
    h = sc["h"]

    bnd = [
        {"type": "text", "id": title_id},
        {"type": "arrow", "id": f"arr_sys_{sc_id}"},
    ]

    d.rect(
        sc_id,
        sc_x,
        sub_top,
        SUB_CARD_W,
        h,
        sc["stroke"],
        sc["bg"],
        bnd=bnd,
    )

    title_h = th(sc["title"], FONT_TITLE)
    sub_h_val = th(sc["subtitle"], FONT_SUB)
    combined = title_h + SUB_GAP + sub_h_val
    top_pad = (h - combined) // 2

    title_y = sub_top + top_pad
    sub_y = title_y + title_h + SUB_GAP

    d.txt(
        title_id,
        sc_x,
        title_y,
        SUB_CARD_W,
        title_h,
        sc["title"],
        FONT_TITLE,
        color="#1e1e1e",
        cid=sc_id,
    )
    d.txt(
        sub_id,
        sc_x,
        sub_y,
        SUB_CARD_W,
        sub_h_val,
        sc["subtitle"],
        FONT_SUB,
        color=sc["stroke"],
        valign="top",
    )

# ── Fan-out arrows from System Requirements to sub-cards ──
sys_cx = PAD_X + CARD_W // 2
sys_bot = card_positions["sys"]["y"] + card_positions["sys"]["h"]

for j, sc in enumerate(sub_cards):
    sc_x = left_x if j == 0 else right_x
    sc_cx = sc_x + SUB_CARD_W // 2
    arrow_id = f"arr_sys_{sc['id']}"

    dx = sc_cx - sys_cx
    dy = sub_top - sys_bot

    sb = {"elementId": "sys", "focus": dx / (CARD_W / 2), "gap": 4, "fixedPoint": None}
    eb = {"elementId": sc["id"], "focus": 0, "gap": 4, "fixedPoint": None}

    d.arr(arrow_id, sys_cx, sys_bot, [[0, 0], [dx, dy]], "#6741d9", sb=sb, eb=eb)

# ── Write file ──
d.save("diagrams/requirements-hierarchy.excalidraw")
print("Done! Wrote diagrams/requirements-hierarchy.excalidraw")
