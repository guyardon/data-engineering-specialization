"""Generate SCD Types diagram: Type 1 (Overwrite) vs Type 2 (Add Row)."""
import json, math, sys

data = {
    "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
    "elements": [], "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {},
}
els = data["elements"]
seed = 1000
def ns():
    global seed; seed += 1; return seed

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
GRAY = ("#868e96", "#dee2e6")

def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
    els.append({"type":"rectangle","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "strokeColor":stroke,"backgroundColor":bg,"fillStyle":fill,"strokeWidth":2,
        "strokeStyle":"dashed" if dashed else "solid","roughness":1,"opacity":opacity,
        "roundness":{"type":3},"seed":ns(),"version":1,"versionNonce":ns(),
        "isDeleted":False,"groupIds":[],"boundElements":bnd or [],
        "frameId":None,"link":None,"locked":False,"updated":1710000000000})

def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,"angle":0,
        "text":t,"originalText":t,"fontSize":sz,"fontFamily":1,
        "textAlign":align,"verticalAlign":"middle","lineHeight":1.25,"autoResize":True,
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

# Title
TITLE_Y = 25
txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Slowly Changing Dimensions", 32)

# --- TYPE 1 SECTION ---
T1_Y = 90
T1_H = 190
rect("t1_bg", PAD_X, T1_Y, CONTENT_W, T1_H, *BLUE, fill="solid", opacity=15, dashed=True)
txt("t1_title", PAD_X, T1_Y + 10, CONTENT_W, 30, "Type 1 — Overwrite", 24, color=BLUE[0])

# Before table
TBL_W = 220
TBL_X = PAD_X + 40
ROW_H = 32
BEFORE_Y = T1_Y + 50
rect("t1_hdr", TBL_X, BEFORE_Y, TBL_W, ROW_H, *BLUE, fill="solid", opacity=30)
txt("t1_hdr_t", TBL_X, BEFORE_Y, TBL_W, ROW_H, "key  |  name  |  city", 16, cid="t1_hdr")
rect("t1_row1", TBL_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, BLUE[0], "transparent")
txt("t1_row1_t", TBL_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, "101  |  Alice  |  NYC", 16, cid="t1_row1")

# Arrow in the middle
ARR_X = TBL_X + TBL_W + 30
ARR_Y = BEFORE_Y + ROW_H
txt("t1_change", ARR_X, ARR_Y - 8, 120, 30, "Alice moves\nto LA →", 15, color=BLUE[0])

# After table
AFTER_X = ARR_X + 130
rect("t1_hdr2", AFTER_X, BEFORE_Y, TBL_W, ROW_H, *BLUE, fill="solid", opacity=30)
txt("t1_hdr2_t", AFTER_X, BEFORE_Y, TBL_W, ROW_H, "key  |  name  |  city", 16, cid="t1_hdr2")
rect("t1_row2", AFTER_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, BLUE[0], "transparent")
txt("t1_row2_t", AFTER_X, BEFORE_Y + ROW_H, TBL_W, ROW_H, "101  |  Alice  |  LA", 16, cid="t1_row2")

# Subtitle
txt("t1_sub", PAD_X, T1_Y + T1_H - 40, CONTENT_W, 25, "No history preserved — previous value is lost", 17, color=BLUE[0])

# --- ARROW BETWEEN SECTIONS ---
SEC_GAP = 70
arr("sec_arr", CW // 2, T1_Y + T1_H, [[0, 0], [0, SEC_GAP]], GRAY[0], dash=True)

# --- TYPE 2 SECTION ---
T2_Y = T1_Y + T1_H + SEC_GAP
T2_H = 220
rect("t2_bg", PAD_X, T2_Y, CONTENT_W, T2_H, *GREEN, fill="solid", opacity=15, dashed=True)
txt("t2_title", PAD_X, T2_Y + 10, CONTENT_W, 30, "Type 2 — Add New Row", 24, color=GREEN[0])

# Table with versioning columns
TBL2_W = CONTENT_W - 60
TBL2_X = PAD_X + 30
T2_TBL_Y = T2_Y + 50
rect("t2_hdr", TBL2_X, T2_TBL_Y, TBL2_W, ROW_H, *GREEN, fill="solid", opacity=30)
txt("t2_hdr_t", TBL2_X, T2_TBL_Y, TBL2_W, ROW_H, "key  |  name  |  city  |  effective  |  current", 15, cid="t2_hdr")

rect("t2_row1", TBL2_X, T2_TBL_Y + ROW_H, TBL2_W, ROW_H, GREEN[0], "transparent")
txt("t2_row1_t", TBL2_X, T2_TBL_Y + ROW_H, TBL2_W, ROW_H, "101  |  Alice  |  NYC  |  2024-01-01  |  false", 15, cid="t2_row1", op=60)

rect("t2_row2", TBL2_X, T2_TBL_Y + 2 * ROW_H, TBL2_W, ROW_H, GREEN[0], "transparent")
txt("t2_row2_t", TBL2_X, T2_TBL_Y + 2 * ROW_H, TBL2_W, ROW_H, "102  |  Alice  |  LA   |  2025-03-15  |  true", 15, cid="t2_row2")

# Subtitle
txt("t2_sub", PAD_X, T2_Y + T2_H - 40, CONTENT_W, 25, "Full history preserved — each version gets a new row", 17, color=GREEN[0])

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "scd-types"
with open(f"diagrams/{name}.excalidraw", "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote diagrams/{name}.excalidraw")
