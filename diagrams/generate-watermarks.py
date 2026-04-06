"""Generate Watermarks and Late Data diagram."""
import json, math, sys

data = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
}
els = data["elements"]
seed = 3000
def ns():
    global seed; seed += 1; return seed

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")

def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
    els.append({"type":"rectangle","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "strokeColor":stroke,"backgroundColor":bg,"fillStyle":fill,"strokeWidth":2,
        "strokeStyle":"dashed" if dashed else "solid","roughness":1,"opacity":opacity,
        "roundness":{"type":3},"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":bnd or [],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "text":t,"originalText":t,"fontSize":sz,"fontFamily":1,
        "textAlign":"center","verticalAlign":"middle","lineHeight":1.25,"autoResize":True,
        "containerId":cid,"strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":1,"opacity":op,
        "seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":[],"frameId":None,"link":None,
        "locked":False,"updated":1710000000000})

def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({"type":"arrow","id":id,"x":x,"y":y,
        "width":pts[-1][0]-pts[0][0],"height":pts[-1][1]-pts[0][1],"angle":0,"points":pts,
        "startArrowhead":None,"endArrowhead":"arrow","startBinding":sb,"endBinding":eb,
        "elbowed":False,"strokeColor":stroke,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":2,"strokeStyle":"dashed" if dash else "solid",
        "roughness":1,"opacity":op,"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":[],"frameId":None,"link":None,
        "locked":False,"updated":1710000000000})

# === LAYOUT ===
CW = 620
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X
BOX_W = CONTENT_W
ARR_GAP = 70

# Title
txt("title", PAD_X, 25, CONTENT_W, 40, "Watermarks and Late Data", 32)

# Box 1: Event Time vs Processing Time
B1_Y = 90
B1_H = 110
rect("b1", PAD_X, B1_Y, BOX_W, B1_H, *BLUE, fill="solid", opacity=20,
     bnd=[{"id": "b1_title", "type": "text"}])
txt("b1_title", PAD_X, B1_Y, BOX_W, 50, "Event Time vs Processing Time", 24, cid="b1")
txt("b1_sub", PAD_X, B1_Y + 55, BOX_W, 45, "Events may arrive out of order\nor delayed by seconds to hours", 17, color=BLUE[0])

# Arrow 1
arr("a1", CW // 2, B1_Y + B1_H, [[0, 0], [0, ARR_GAP]], BLUE[0],
    sb={"elementId": "b1", "focus": 0, "gap": 4},
    eb={"elementId": "b2", "focus": 0, "gap": 4})

# Box 2: Watermark
B2_Y = B1_Y + B1_H + ARR_GAP
B2_H = 130
rect("b2", PAD_X, B2_Y, BOX_W, B2_H, *GREEN, fill="solid", opacity=20,
     bnd=[{"id": "b2_title", "type": "text"}])
txt("b2_title", PAD_X, B2_Y, BOX_W, 50, "Watermark", 24, cid="b2")
txt("b2_sub", PAD_X, B2_Y + 55, BOX_W, 65, "Tracks the expected progress of event time\n— declares when a window is 'complete'", 17, color=GREEN[0])

# Arrow 2
arr("a2", CW // 2, B2_Y + B2_H, [[0, 0], [0, ARR_GAP]], GREEN[0],
    sb={"elementId": "b2", "focus": 0, "gap": 4},
    eb={"elementId": "b3", "focus": 0, "gap": 4})

# Box 3: Late Data Handling (header)
B3_Y = B2_Y + B2_H + ARR_GAP
B3_H = 55
rect("b3", PAD_X, B3_Y, BOX_W, B3_H, *YELLOW, fill="solid", opacity=20,
     bnd=[{"id": "b3_title", "type": "text"}])
txt("b3_title", PAD_X, B3_Y, BOX_W, B3_H, "Late Data Handling", 24, cid="b3")

# Strategy pills
PILL_H = 45
PILL_GAP = 12
PILL_Y = B3_Y + B3_H + 15
pills = [
    ("p1", "Drop — discard events past watermark", RED),
    ("p2", "Allow — accept within grace period", YELLOW),
    ("p3", "Side Output — route to separate stream", CYAN),
]
for i, (pid, label, color) in enumerate(pills):
    py = PILL_Y + i * (PILL_H + PILL_GAP)
    rect(pid, PAD_X + 20, py, BOX_W - 40, PILL_H, *color, fill="solid", opacity=20,
         bnd=[{"id": f"{pid}_t", "type": "text"}])
    txt(f"{pid}_t", PAD_X + 20, py, BOX_W - 40, PILL_H, label, 18, cid=pid)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "watermarks"
with open(f"diagrams/{name}.excalidraw", "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote diagrams/{name}.excalidraw")
