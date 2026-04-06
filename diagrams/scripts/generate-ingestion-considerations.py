"""Generate Ingestion Tool Selection Considerations diagram for Course 2, Section 2.4.3."""

import math

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, YELLOW, RED, CYAN, GRAY

d = ExcalidrawDiagram(seed=5000)

# === LAYOUT CONSTANTS ===
# Central title -> two category containers stacked vertically
# Each container has a header + grid of factor pills

CANVAS_W = 850
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X  # 800

# Pill sizing (5 pills in a row for data characteristics, 2 for reliability)
PILL_H = 55
PILL_GAP = 15
PILL_PAD = 20  # padding inside container around pills

# Container sizing
CONTAINER_PAD = 25
CONTAINER_HDR_H = 45

# Vertical positions
TITLE_Y = 10
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)

SUBTITLE_Y = TITLE_Y + TITLE_H + 5
SUBTITLE_FSZ = 19
SUBTITLE_H = math.ceil(1 * SUBTITLE_FSZ * 1.25)

# Container 1: Data Characteristics (5 pills in a row, then wrap)
C1_Y = SUBTITLE_Y + SUBTITLE_H + 25
C1_PILLS = [
    "Data Type &\nStructure",
    "Data\nVolume",
    "Latency\nRequirements",
    "Data\nQuality",
    "Schema\nChanges",
]
C1_COLS = 5
C1_PILL_W = (CONTENT_W - 2 * CONTAINER_PAD - (C1_COLS - 1) * PILL_GAP) // C1_COLS
C1_ROWS = 1
C1_H = CONTAINER_HDR_H + PILL_PAD + C1_ROWS * PILL_H + CONTAINER_PAD

# Container 2: Reliability & Durability (2 pills centered)
C2_Y = C1_Y + C1_H + 30
C2_PILLS = [
    "Reliability\nProper function under load",
    "Durability\nData not lost or corrupted",
]
C2_COLS = 2
C2_PILL_W = 320
C2_PILL_TOTAL = 2 * C2_PILL_W + PILL_GAP
C2_PILL_X_START = (
    PAD_X + CONTAINER_PAD + (CONTENT_W - 2 * CONTAINER_PAD - C2_PILL_TOTAL) // 2
)
C2_H = CONTAINER_HDR_H + PILL_PAD + PILL_H + CONTAINER_PAD

# Arrow between containers
ARR_GAP_C = 30

# Adjust C2_Y to account for arrow
C2_Y = C1_Y + C1_H + ARR_GAP_C


# === BUILD DIAGRAM ===

# Main title
d.txt(
    "title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Choosing Ingestion Tools", TITLE_FSZ
)
d.txt(
    "subtitle",
    PAD_X,
    SUBTITLE_Y,
    CONTENT_W,
    SUBTITLE_H,
    "Key evaluation criteria",
    SUBTITLE_FSZ,
    color=GRAY[0],
)

# --- Container 1: Data Characteristics ---
d.rect("c1", PAD_X, C1_Y, CONTENT_W, C1_H, *BLUE, opacity=30, dashed=True)
# Container header
d.txt(
    "c1-hdr",
    PAD_X,
    C1_Y + 8,
    CONTENT_W,
    math.ceil(24 * 1.25),
    "Data Characteristics",
    24,
    color=BLUE[0],
)

# Pills
C1_COLORS = [BLUE, CYAN, GREEN, YELLOW, PURPLE]
pill_start_y = C1_Y + CONTAINER_HDR_H + PILL_PAD
for i, (label, color) in enumerate(zip(C1_PILLS, C1_COLORS)):
    px = PAD_X + CONTAINER_PAD + i * (C1_PILL_W + PILL_GAP)
    py = pill_start_y
    pid = f"c1-p{i}"
    d.rect(
        pid, px, py, C1_PILL_W, PILL_H, *color, bnd=[{"id": f"{pid}-t", "type": "text"}]
    )
    d.txt(f"{pid}-t", px, py, C1_PILL_W, PILL_H, label, 18, cid=pid)

# Arrow down
arr_x = PAD_X + CONTENT_W // 2
d.arr(
    "c-arr",
    arr_x,
    C1_Y + C1_H,
    [[0, 0], [0, ARR_GAP_C]],
    GRAY[0],
    dash=True,
)

# --- Container 2: Reliability & Durability ---
d.rect("c2", PAD_X, C2_Y, CONTENT_W, C2_H, *RED, opacity=30, dashed=True)
d.txt(
    "c2-hdr",
    PAD_X,
    C2_Y + 8,
    CONTENT_W,
    math.ceil(24 * 1.25),
    "Reliability & Durability",
    24,
    color=RED[0],
)

C2_COLORS = [RED, PURPLE]
pill_start_y2 = C2_Y + CONTAINER_HDR_H + PILL_PAD
for i, (label, color) in enumerate(zip(C2_PILLS, C2_COLORS)):
    px = C2_PILL_X_START + i * (C2_PILL_W + PILL_GAP)
    py = pill_start_y2
    pid = f"c2-p{i}"
    d.rect(
        pid, px, py, C2_PILL_W, PILL_H, *color, bnd=[{"id": f"{pid}-t", "type": "text"}]
    )
    d.txt(f"{pid}-t", px, py, C2_PILL_W, PILL_H, label, 18, cid=pid)

# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"C1: y={C1_Y}, h={C1_H}, pills={C1_PILL_W}w")
print(f"C2: y={C2_Y}, h={C2_H}, pills={C2_PILL_W}w")
print(f"Bottom: {C2_Y + C2_H}")

# === WRITE ===
outfile = "diagrams/artifacts/ingestion-considerations.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
