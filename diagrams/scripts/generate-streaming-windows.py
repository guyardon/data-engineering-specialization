"""
Generate streaming windowing techniques diagram showing tumbling,
sliding, and session windows.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, GRAY

d = ExcalidrawDiagram(seed=6000)

# === LAYOUT ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X

TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "Streaming Window Types",
    32,
    color="#1e1e1e",
)

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
d.txt(
    "tum_label",
    PAD_X,
    TUM_Y + 10,
    LABEL_W,
    TUM_LABEL_H,
    "Tumbling\n(Fixed-Time)",
    22,
    color=BLUE[0],
)

# Three non-overlapping windows
tw = (VIS_W - 2 * WIN_GAP) // 3
for i in range(3):
    x = VIS_X + i * (tw + WIN_GAP)
    bid = f"tw{i}"
    d.rect(bid, x, TUM_Y, tw, WIN_H, *BLUE, bnd=[{"id": f"{bid}_t", "type": "text"}])
    d.txt(f"{bid}_t", x, TUM_Y, tw, WIN_H, f"W{i + 1}", 20, cid=bid)

# Time arrow below
TUM_ARROW_Y = TUM_Y + WIN_H + 12
d.txt(
    "tum_time",
    VIS_X,
    TUM_ARROW_Y,
    VIS_W,
    math.ceil(1 * 15 * 1.25),
    "No overlap — each event belongs to exactly one window",
    15,
    color=BLUE[0],
)

# === SLIDING WINDOWS ===
SLIDE_Y = TUM_ARROW_Y + 30 + SECTION_GAP
SLIDE_LABEL_H = math.ceil(1 * 22 * 1.25)
d.txt(
    "slide_label",
    PAD_X,
    SLIDE_Y + 10,
    LABEL_W,
    SLIDE_LABEL_H,
    "Sliding\n(Overlapping)",
    22,
    color=GREEN[0],
)

# Three overlapping windows (offset by step)
sw = (VIS_W * 2) // 5
step = sw // 2 + 10
for i in range(3):
    x = VIS_X + i * step
    bid = f"sw{i}"
    d.rect(
        bid,
        x,
        SLIDE_Y + i * 4,
        sw,
        WIN_H,
        *GREEN,
        opacity=70 if i > 0 else 100,
        bnd=[{"id": f"{bid}_t", "type": "text"}],
    )
    d.txt(
        f"{bid}_t",
        x,
        SLIDE_Y + i * 4,
        sw,
        WIN_H,
        f"W{i + 1}",
        20,
        cid=bid,
        op=70 if i > 0 else 100,
    )

SLIDE_NOTE_Y = SLIDE_Y + WIN_H + 20
d.txt(
    "slide_time",
    VIS_X,
    SLIDE_NOTE_Y,
    VIS_W,
    math.ceil(1 * 15 * 1.25),
    "Windows overlap — events can appear in multiple windows",
    15,
    color=GREEN[0],
)

# === SESSION WINDOWS ===
SESS_Y = SLIDE_NOTE_Y + 30 + SECTION_GAP
SESS_LABEL_H = math.ceil(1 * 22 * 1.25)
d.txt(
    "sess_label",
    PAD_X,
    SESS_Y + 10,
    LABEL_W,
    SESS_LABEL_H,
    "Session\n(Activity-Based)",
    22,
    color=YELLOW[0],
)

# Two sessions with a gap between
s1w = VIS_W * 3 // 8
s2w = VIS_W * 2 // 8
gap_w = VIS_W - s1w - s2w

d.rect("ss1", VIS_X, SESS_Y, s1w, WIN_H, *YELLOW, bnd=[{"id": "ss1_t", "type": "text"}])
d.txt("ss1_t", VIS_X, SESS_Y, s1w, WIN_H, "Session 1", 20, cid="ss1")

# Gap indicator
gap_x = VIS_X + s1w
gap_mid = gap_x + gap_w // 2
d.txt(
    "gap_label",
    gap_x,
    SESS_Y + 12,
    gap_w,
    math.ceil(1 * 16 * 1.25),
    "gap",
    16,
    color=GRAY[0],
)

d.rect(
    "ss2",
    VIS_X + s1w + gap_w,
    SESS_Y,
    s2w,
    WIN_H,
    *YELLOW,
    bnd=[{"id": "ss2_t", "type": "text"}],
)
d.txt("ss2_t", VIS_X + s1w + gap_w, SESS_Y, s2w, WIN_H, "Session 2", 20, cid="ss2")

SESS_NOTE_Y = SESS_Y + WIN_H + 12
d.txt(
    "sess_time",
    VIS_X,
    SESS_NOTE_Y,
    VIS_W,
    math.ceil(1 * 15 * 1.25),
    "Variable size — inactivity gap triggers new session",
    15,
    color=YELLOW[0],
)

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{SESS_NOTE_Y + 30}")

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/streaming-windows"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
