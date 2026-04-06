"""Generate Data Mesh Principles diagram: 2x2 grid."""
import json, math, sys

data = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
}
els = data["elements"]
seed = 4000
def ns():
    global seed; seed += 1; return seed

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
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

# === LAYOUT ===
CW = 620
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X
BOX_W = (CONTENT_W - 30) // 2  # 2 columns with 30px gap
BOX_H = 130
COL_GAP = 30
ROW_GAP = 30

# Title
txt("title", PAD_X, 25, CONTENT_W, 40, "Data Mesh Principles", 32)

# 2x2 grid
grid = [
    [("domain", "Domain\nOwnership", "Each domain owns and\nserves its own data", BLUE),
     ("product", "Data as\na Product", "Domains publish data\nwith SLAs and docs", GREEN)],
    [("platform", "Self-Serve\nPlatform", "Shared infrastructure\nfor all domains", PURPLE),
     ("governance", "Federated\nGovernance", "Global standards,\nlocal autonomy", YELLOW)],
]

START_Y = 90
for row_i, row in enumerate(grid):
    for col_i, (pid, title, subtitle, color) in enumerate(row):
        bx = PAD_X + col_i * (BOX_W + COL_GAP)
        by = START_Y + row_i * (BOX_H + ROW_GAP)
        rect(pid, bx, by, BOX_W, BOX_H, *color, fill="solid", opacity=20,
             bnd=[{"id": f"{pid}_title", "type": "text"}])
        txt(f"{pid}_title", bx, by, BOX_W, 60, title, 22, cid=pid)
        txt(f"{pid}_sub", bx, by + 70, BOX_W, 50, subtitle, 17, color=color[0])

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "data-mesh"
with open(f"diagrams/{name}.excalidraw", "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote diagrams/{name}.excalidraw")
