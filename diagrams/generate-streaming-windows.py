"""
Generate streaming windowing techniques diagram showing tumbling,
sliding, and session windows.
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
seed = 6000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True if cid else False, "containerId": cid,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


# === LAYOUT ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Streaming Window Types", 32, color="#1e1e1e")

# Each window type gets a row with a label and visual representation
SECTION_GAP = 30
WIN_H = 50
WIN_GAP = 8
LABEL_W = 160
VIS_X = PAD_X + LABEL_W + 15
VIS_W = CONTENT_W - LABEL_W - 15

# === TUMBLING WINDOWS ===
TUM_Y = TITLE_Y + TITLE_H + 35
TUM_LABEL_H = math.ceil(1 * 22 * 1.25)
txt("tum_label", PAD_X, TUM_Y + 10, LABEL_W, TUM_LABEL_H,
    "Tumbling\n(Fixed-Time)", 22, color=BLUE[0])

# Three non-overlapping windows
tw = (VIS_W - 2 * WIN_GAP) // 3
for i in range(3):
    x = VIS_X + i * (tw + WIN_GAP)
    bid = f"tw{i}"
    rect(bid, x, TUM_Y, tw, WIN_H, *BLUE,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", x, TUM_Y, tw, WIN_H,
        f"W{i+1}", 20, cid=bid)

# Time arrow below
TUM_ARROW_Y = TUM_Y + WIN_H + 12
txt("tum_time", VIS_X, TUM_ARROW_Y, VIS_W, math.ceil(1 * 15 * 1.25),
    "No overlap — each event belongs to exactly one window", 15, color=BLUE[0])

# === SLIDING WINDOWS ===
SLIDE_Y = TUM_ARROW_Y + 30 + SECTION_GAP
SLIDE_LABEL_H = math.ceil(1 * 22 * 1.25)
txt("slide_label", PAD_X, SLIDE_Y + 10, LABEL_W, SLIDE_LABEL_H,
    "Sliding\n(Overlapping)", 22, color=GREEN[0])

# Three overlapping windows (offset by step)
sw = (VIS_W * 2) // 5
step = sw // 2 + 10
for i in range(3):
    x = VIS_X + i * step
    bid = f"sw{i}"
    rect(bid, x, SLIDE_Y + i * 4, sw, WIN_H, *GREEN,
         opacity=70 if i > 0 else 100,
         bnd=[{"id": f"{bid}_t", "type": "text"}])
    txt(f"{bid}_t", x, SLIDE_Y + i * 4, sw, WIN_H,
        f"W{i+1}", 20, cid=bid, op=70 if i > 0 else 100)

SLIDE_NOTE_Y = SLIDE_Y + WIN_H + 20
txt("slide_time", VIS_X, SLIDE_NOTE_Y, VIS_W, math.ceil(1 * 15 * 1.25),
    "Windows overlap — events can appear in multiple windows", 15, color=GREEN[0])

# === SESSION WINDOWS ===
SESS_Y = SLIDE_NOTE_Y + 30 + SECTION_GAP
SESS_LABEL_H = math.ceil(1 * 22 * 1.25)
txt("sess_label", PAD_X, SESS_Y + 10, LABEL_W, SESS_LABEL_H,
    "Session\n(Activity-Based)", 22, color=YELLOW[0])

# Two sessions with a gap between
s1w = VIS_W * 3 // 8
s2w = VIS_W * 2 // 8
gap_w = VIS_W - s1w - s2w

rect("ss1", VIS_X, SESS_Y, s1w, WIN_H, *YELLOW,
     bnd=[{"id": "ss1_t", "type": "text"}])
txt("ss1_t", VIS_X, SESS_Y, s1w, WIN_H, "Session 1", 20, cid="ss1")

# Gap indicator
gap_x = VIS_X + s1w
gap_mid = gap_x + gap_w // 2
txt("gap_label", gap_x, SESS_Y + 12, gap_w, math.ceil(1 * 16 * 1.25),
    "gap", 16, color=GRAY[0])

rect("ss2", VIS_X + s1w + gap_w, SESS_Y, s2w, WIN_H, *YELLOW,
     bnd=[{"id": "ss2_t", "type": "text"}])
txt("ss2_t", VIS_X + s1w + gap_w, SESS_Y, s2w, WIN_H, "Session 2", 20, cid="ss2")

SESS_NOTE_Y = SESS_Y + WIN_H + 12
txt("sess_time", VIS_X, SESS_NOTE_Y, VIS_W, math.ceil(1 * 15 * 1.25),
    "Variable size — inactivity gap triggers new session", 15, color=YELLOW[0])

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{SESS_NOTE_Y + 30}")

name = sys.argv[1] if len(sys.argv) > 1 else "streaming-windows"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
