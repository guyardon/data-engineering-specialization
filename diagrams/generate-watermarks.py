"""Generate Watermarks and Late Data diagram."""
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, RED, CYAN

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT ===
CW = 620
PAD_X = 30
CONTENT_W = CW - 2 * PAD_X
BOX_W = CONTENT_W
ARR_GAP = 70

# Title
d.txt("title", PAD_X, 25, CONTENT_W, 40, "Watermarks and Late Data", 32)

# Box 1: Event Time vs Processing Time
B1_Y = 90
B1_H = 110
d.rect("b1", PAD_X, B1_Y, BOX_W, B1_H, *BLUE, opacity=20,
     bnd=[{"id": "b1_title", "type": "text"}])
d.txt("b1_title", PAD_X, B1_Y, BOX_W, 50, "Event Time vs Processing Time", 24, cid="b1")
d.txt("b1_sub", PAD_X, B1_Y + 55, BOX_W, 45, "Events may arrive out of order\nor delayed by seconds to hours", 17, color=BLUE[0])

# Arrow 1
d.arr("a1", CW // 2, B1_Y + B1_H, [[0, 0], [0, ARR_GAP]], BLUE[0],
    sb={"elementId": "b1", "focus": 0, "gap": 4},
    eb={"elementId": "b2", "focus": 0, "gap": 4})

# Box 2: Watermark
B2_Y = B1_Y + B1_H + ARR_GAP
B2_H = 130
d.rect("b2", PAD_X, B2_Y, BOX_W, B2_H, *GREEN, opacity=20,
     bnd=[{"id": "b2_title", "type": "text"}])
d.txt("b2_title", PAD_X, B2_Y, BOX_W, 50, "Watermark", 24, cid="b2")
d.txt("b2_sub", PAD_X, B2_Y + 55, BOX_W, 65, "Tracks the expected progress of event time\n— declares when a window is 'complete'", 17, color=GREEN[0])

# Arrow 2
d.arr("a2", CW // 2, B2_Y + B2_H, [[0, 0], [0, ARR_GAP]], GREEN[0],
    sb={"elementId": "b2", "focus": 0, "gap": 4},
    eb={"elementId": "b3", "focus": 0, "gap": 4})

# Box 3: Late Data Handling (header)
B3_Y = B2_Y + B2_H + ARR_GAP
B3_H = 55
d.rect("b3", PAD_X, B3_Y, BOX_W, B3_H, *YELLOW, opacity=20,
     bnd=[{"id": "b3_title", "type": "text"}])
d.txt("b3_title", PAD_X, B3_Y, BOX_W, B3_H, "Late Data Handling", 24, cid="b3")

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
    d.rect(pid, PAD_X + 20, py, BOX_W - 40, PILL_H, *color, opacity=20,
         bnd=[{"id": f"{pid}_t", "type": "text"}])
    d.txt(f"{pid}_t", PAD_X + 20, py, BOX_W - 40, PILL_H, label, 18, cid=pid)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "watermarks"
d.save(f"diagrams/{name}.excalidraw")
print(f"Wrote diagrams/{name}.excalidraw")
