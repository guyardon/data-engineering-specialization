"""Generate Medallion Architecture diagram: Bronze → Silver → Gold."""
import json, math, sys

data = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
}
els = data["elements"]
seed = 2000
def ns():
    global seed; seed += 1; return seed

GRAY = ("#868e96", "#dee2e6")
BLUE = ("#1971c2", "#a5d8ff")
YELLOW = ("#e67700", "#ffec99")

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
CW = 700
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X

# Title
txt("title", PAD_X, 25, CONTENT_W, 40, "Medallion Architecture", 32)

# Three boxes horizontally
BOX_W = 175
BOX_H = 160
BOX_Y = 90
GAP = 35
total_w = 3 * BOX_W + 2 * GAP
start_x = (CW - total_w) // 2

layers = [
    ("bronze", start_x, "Bronze", "Raw Ingestion", "Exact copy of\nsource data", GRAY),
    ("silver", start_x + BOX_W + GAP, "Silver", "Cleaned &\nConformed", "Deduplicated,\ntyped, validated", BLUE),
    ("gold", start_x + 2 * (BOX_W + GAP), "Gold", "Business-Level", "Aggregated,\nmodeled, served", YELLOW),
]

for lid, lx, title, subtitle, desc, color in layers:
    rect(f"{lid}_box", lx, BOX_Y, BOX_W, BOX_H, *color, fill="solid", opacity=25,
         bnd=[{"id": f"{lid}_title", "type": "text"}])
    txt(f"{lid}_title", lx, BOX_Y, BOX_W, 50, title, 24, cid=f"{lid}_box")
    txt(f"{lid}_sub", lx, BOX_Y + 45, BOX_W, 30, subtitle, 17, color=color[0])
    txt(f"{lid}_desc", lx, BOX_Y + 100, BOX_W, 50, desc, 16, color=color[0], op=70)

# Arrows between boxes
for i, (lid, lx, *_) in enumerate(layers[:-1]):
    next_x = layers[i + 1][1]
    ax = lx + BOX_W
    ay = BOX_Y + BOX_H // 2
    arr(f"arr_{i}", ax, ay, [[0, 0], [GAP, 0]], layers[i][5][0],
        sb={"elementId": f"{lid}_box", "focus": 0, "gap": 4},
        eb={"elementId": f"{layers[i+1][0]}_box", "focus": 0, "gap": 4})

# Storage layer beneath
STORAGE_Y = BOX_Y + BOX_H + 50
STORAGE_H = 50
rect("storage", start_x - 10, STORAGE_Y, total_w + 20, STORAGE_H, *GRAY, fill="solid", opacity=10, dashed=True,
     bnd=[{"id": "storage_t", "type": "text"}])
txt("storage_t", start_x - 10, STORAGE_Y, total_w + 20, STORAGE_H, "Object Storage (S3)", 20, color=GRAY[0], cid="storage")

# Dashed arrows from each box to storage
for lid, lx, *_ in layers:
    arr(f"store_{lid}", lx + BOX_W // 2, BOX_Y + BOX_H, [[0, 0], [0, 50]], GRAY[0], dash=True, op=40)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "medallion-architecture"
with open(f"diagrams/{name}.excalidraw", "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote diagrams/{name}.excalidraw")
