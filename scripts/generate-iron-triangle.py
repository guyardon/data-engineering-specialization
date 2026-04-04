import json
import math
import os

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 4000


def ns():
    global seed
    seed += 1
    return seed


def rect(
    id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2
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
            "strokeWidth": sw,
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, valign="middle"):
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
            "textAlign": "center",
            "verticalAlign": valign,
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


def line(id, x, y, pts, stroke, sw=2, op=100):
    els.append(
        {
            "type": "line",
            "id": id,
            "x": x,
            "y": y,
            "width": max(abs(p[0]) for p in pts),
            "height": max(abs(p[1]) for p in pts),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": None,
            "startBinding": None,
            "endBinding": None,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": sw,
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


def diamond(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, bnd=None):
    els.append(
        {
            "type": "diamond",
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
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 2},
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


def th(text, font_size):
    return math.ceil((text.count("\n") + 1) * font_size * 1.25)


# ── Layout constants ──
CANVAS_W = 600
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

# ── Title ──
TITLE_Y = 0
MAIN_TITLE_H = th("The Iron Triangle", 28)

txt("title", PAD_X, TITLE_Y, CONTENT_W, MAIN_TITLE_H, "The Iron Triangle", 28)

# Timeline box extends BOX_H + 10 above TRIANGLE_TOP_Y, so gap must clear the title
TITLE_GAP = 120  # BOX_H(90) + 30 → timeline box top = title_bottom + 20
TRIANGLE_TOP_Y = TITLE_Y + MAIN_TITLE_H + TITLE_GAP

# ── Triangle geometry ──
# Three vertices of an equilateral-ish triangle
TRI_W = 400  # base width
TRI_H = 320  # height of triangle

# Center horizontally
tri_cx = PAD_X + CONTENT_W // 2
top_x = tri_cx
top_y = TRIANGLE_TOP_Y
left_x = tri_cx - TRI_W // 2
left_y = TRIANGLE_TOP_Y + TRI_H
right_x = tri_cx + TRI_W // 2
right_y = TRIANGLE_TOP_Y + TRI_H

# Draw triangle edges
line(
    "tri_left",
    top_x,
    top_y,
    [[0, 0], [left_x - top_x, left_y - top_y]],
    "#868e96",
    sw=2,
    op=60,
)
line(
    "tri_right",
    top_x,
    top_y,
    [[0, 0], [right_x - top_x, right_y - top_y]],
    "#868e96",
    sw=2,
    op=60,
)
line(
    "tri_bottom",
    left_x,
    left_y,
    [[0, 0], [right_x - left_x, 0]],
    "#868e96",
    sw=2,
    op=60,
)

# ── Vertex labels (boxes at each corner) ──
BOX_W = 200
BOX_H = 90
FONT_TITLE = 22
FONT_SUB = 16
SUB_GAP = 6

vertices = [
    {
        "id": "timeline",
        "title": "Timeline",
        "subtitle": "When it's needed",
        "stroke": "#1971c2",
        "bg": "#a5d8ff",
        "x": top_x - BOX_W // 2,
        "y": top_y - BOX_H - 10,
    },
    {
        "id": "budget",
        "title": "Budget",
        "subtitle": "Available resources",
        "stroke": "#2f9e44",
        "bg": "#b2f2bb",
        "x": left_x - BOX_W - 10,
        "y": left_y - BOX_H // 2,
    },
    {
        "id": "scope",
        "title": "Scope",
        "subtitle": "System features",
        "stroke": "#e67700",
        "bg": "#ffec99",
        "x": right_x + 10,
        "y": right_y - BOX_H // 2,
    },
]

for v in vertices:
    vid = v["id"]
    title_id = f"{vid}_title"
    sub_id = f"{vid}_sub"

    bnd = [{"type": "text", "id": title_id}]

    rect(vid, v["x"], v["y"], BOX_W, BOX_H, v["stroke"], v["bg"], fill="solid", bnd=bnd)

    title_h = th(v["title"], FONT_TITLE)
    sub_h = th(v["subtitle"], FONT_SUB)
    combined = title_h + SUB_GAP + sub_h
    top_pad = (BOX_H - combined) // 2

    title_y = v["y"] + top_pad
    sub_y = title_y + title_h + SUB_GAP

    txt(
        title_id,
        v["x"],
        title_y,
        BOX_W,
        title_h,
        v["title"],
        FONT_TITLE,
        color="#1e1e1e",
        cid=vid,
    )
    txt(
        sub_id,
        v["x"],
        sub_y,
        BOX_W,
        sub_h,
        v["subtitle"],
        FONT_SUB,
        color=v["stroke"],
        valign="top",
    )

# ── Center label: "Pick Two" ──
# Place a small diamond in the center of the triangle
center_x = tri_cx
center_y = TRIANGLE_TOP_Y + TRI_H * 2 // 3  # centroid is at 2/3 height

DIAMOND_W = 180
DIAMOND_H = 100

diamond(
    "center",
    center_x - DIAMOND_W // 2,
    center_y - DIAMOND_H // 2,
    DIAMOND_W,
    DIAMOND_H,
    "#c92a2a",
    "#ffc9c9",
    fill="solid",
    bnd=[{"type": "text", "id": "center_txt"}],
)

center_txt_h = th("Pick Two", 22)
txt(
    "center_txt",
    center_x - DIAMOND_W // 2,
    center_y - center_txt_h // 2,
    DIAMOND_W,
    center_txt_h,
    "Pick Two",
    22,
    color="#1e1e1e",
    cid="center",
)

# ── Explanatory note below ──
note_y = left_y + BOX_H // 2 + 30
note_text = "Increasing one dimension inevitably\nputs pressure on the others"
note_h = th(note_text, 18)

txt("note", PAD_X, note_y, CONTENT_W, note_h, note_text, 18, color="#868e96")

# ── Write file ──
out_path = "diagrams/iron-triangle.excalidraw"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
print(f"Done! Wrote {out_path}")
