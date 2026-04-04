import json, math, os

data = {
    "type": "excalidraw", "version": 2,
    "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}
}
els = data["elements"]
seed = 2000

def ns():
    global seed; seed += 1; return seed

def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2):
    els.append({"type":"rectangle","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "strokeColor":stroke,"backgroundColor":bg,"fillStyle":fill,"strokeWidth":sw,
        "strokeStyle":"dashed" if dashed else "solid","roughness":1,"opacity":opacity,
        "roundness":{"type":3},"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":bnd or [],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, valign="middle"):
    """Create a text element. When cid is set, this is bound text (containerId points to parent)."""
    els.append({"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "text":t,"originalText":t,"fontSize":sz,"fontFamily":1,
        "textAlign":"center","verticalAlign":valign,"lineHeight":1.25,"autoResize":True,
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
        "roughness":1,"opacity":op,
        "seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":[],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def th(text, font_size):
    """Text height: ceil(lines * fontSize * 1.25)."""
    return math.ceil((text.count('\n') + 1) * font_size * 1.25)

# ── Layout constants ──
CARD_W = 550
CARD_GAP = 14
PILL_W = 100
PILL_H = 40
PILL_GAP = 12
FONT_TITLE = 22
FONT_SUB = 16
FONT_PILL = 17
START_X = 0
SUB_GAP = 6  # vertical gap between title and subtitle inside a card

TITLE_Y = 0
MAIN_TITLE_H = 70
TITLE_GAP = 25
START_Y = TITLE_Y + MAIN_TITLE_H + TITLE_GAP

CARD3_TO_PILLS_GAP = 50

# ── Card data ──
cards = [
    {"id": 1, "title": "1. Choose Common\nComponents Wisely", "subtitle": "Tools that benefit all teams",
     "stroke": "#1971c2", "bg": "#a5d8ff", "h": 90},
    {"id": 2, "title": "2. Always Be Architecting", "subtitle": "Reversible decisions,\nloosely coupled systems",
     "stroke": "#2f9e44", "bg": "#b2f2bb", "h": 90},
    {"id": 3, "title": "3. Plan for Failure", "subtitle": None,
     "stroke": "#c92a2a", "bg": "#ffc9c9", "h": 55,
     "pills": ["Availability", "Reliability", "Durability", "RTO", "RPO"]},
    {"id": 4, "title": "4. Prioritize Security", "subtitle": "Defense in depth",
     "stroke": "#6741d9", "bg": "#d0bfff", "h": 80},
    {"id": 5, "title": "5. Embrace FinOps", "subtitle": "Cloud spending as\nengineering concern",
     "stroke": "#e67700", "bg": "#ffec99", "h": 90},
]

PILL_STROKE = "#0c8599"
PILL_BG = "#99e9f2"

# ── Main title (free text) ──
txt("title", START_X, TITLE_Y, CARD_W, MAIN_TITLE_H,
    "Principles of Good\nData Architecture", 28)

# ── Build cards ──
cur_y = START_Y

for c in cards:
    idx = c["id"]
    card_id = f"card{idx}"
    title_id = f"card{idx}_title"
    sub_id = f"card{idx}_sub"
    h = c["h"]
    title_text = c["title"]
    subtitle_text = c["subtitle"]

    # boundElements: title text is always bound; arrows for card 3
    bnd = [{"type": "text", "id": title_id}]
    if c.get("pills"):
        for j in range(len(c["pills"])):
            bnd.append({"type": "arrow", "id": f"arrow3_{j}"})

    rect(card_id, START_X, cur_y, CARD_W, h,
         c["stroke"], c["bg"], fill="solid", bnd=bnd)

    if subtitle_text:
        # Compute vertical positions for title + subtitle pair
        title_h = th(title_text, FONT_TITLE)
        sub_h = th(subtitle_text, FONT_SUB)
        combined = title_h + SUB_GAP + sub_h
        top_pad = (h - combined) // 2

        title_y = cur_y + top_pad
        sub_y = title_y + title_h + SUB_GAP

        # Bound title (containerId = card_id)
        txt(title_id, START_X, title_y, CARD_W, title_h,
            title_text, FONT_TITLE, color="#1e1e1e", cid=card_id)

        # Free subtitle (containerId = None), positioned inside the box
        txt(sub_id, START_X, sub_y, CARD_W, sub_h,
            subtitle_text, FONT_SUB, color=c["stroke"], cid=None, valign="top")
    else:
        # No subtitle — bound title centered via auto-centering
        title_h = th(title_text, FONT_TITLE)
        centered_y = cur_y + (h - title_h) // 2
        txt(title_id, START_X, centered_y, CARD_W, title_h,
            title_text, FONT_TITLE, color="#1e1e1e", cid=card_id)

    card_bottom_y = cur_y + h

    # Pills for card 3
    if c.get("pills"):
        pills = c["pills"]
        total_pills_w = len(pills) * PILL_W + (len(pills) - 1) * PILL_GAP
        pill_start_x = START_X + (CARD_W - total_pills_w) // 2
        pill_y = card_bottom_y + CARD3_TO_PILLS_GAP

        pill_ids = []
        for j, label in enumerate(pills):
            pill_id = f"pill3_{j}"
            pill_txt_id = f"pill3_{j}_txt"
            px = pill_start_x + j * (PILL_W + PILL_GAP)

            pill_bnd = [
                {"type": "text", "id": pill_txt_id},
                {"type": "arrow", "id": f"arrow3_{j}"},
            ]
            rect(pill_id, px, pill_y, PILL_W, PILL_H,
                 PILL_STROKE, PILL_BG, fill="solid", bnd=pill_bnd)

            # Pill text: bound, centered by containerId
            ptxt_h = th(label, FONT_PILL)
            ptxt_y = pill_y + (PILL_H - ptxt_h) // 2
            txt(pill_txt_id, px, ptxt_y, PILL_W, ptxt_h,
                label, FONT_PILL, cid=pill_id)
            pill_ids.append((pill_id, px))

        # Arrows from card 3 bottom-center to each pill top-center
        card3_cx = START_X + CARD_W // 2
        for j, (pill_id, px) in enumerate(pill_ids):
            arrow_id = f"arrow3_{j}"
            pill_cx = px + PILL_W // 2
            dx = pill_cx - card3_cx
            dy = pill_y - card_bottom_y

            sb = {"elementId": card_id, "focus": dx / (CARD_W / 2), "gap": 1, "fixedPoint": None}
            eb = {"elementId": pill_id, "focus": 0, "gap": 1, "fixedPoint": None}

            arr(arrow_id, card3_cx, card_bottom_y,
                [[0, 0], [dx, dy]],
                "#c92a2a", sb=sb, eb=eb)

        cur_y = pill_y + PILL_H + CARD_GAP
    else:
        cur_y = card_bottom_y + CARD_GAP

out_path = "diagrams/architecture-principles-w3.excalidraw"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(data, f, indent=2)
print(f"Done! Wrote {out_path}")
