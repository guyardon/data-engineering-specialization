#!/usr/bin/env python3
"""Generate Excalidraw diagram: Data Ingestion Continuum (Batch -> Micro-batch -> Streaming)."""

import math

from diagramlib import ExcalidrawDiagram, BLUE, YELLOW, RED, GRAY

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 800
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Pill boxes
PILL_W = 180
PILL_H = 60
PILL_Y = TITLE_Y + TITLE_H + 30  # pills below title

# Arrow line
ARROW_Y = PILL_Y + PILL_H + 20
ARROW_X = PAD_X + 40
ARROW_W = CONTENT_W - 80

# Three pills evenly spaced
pill_positions = [
    ARROW_X + 10,  # Batch (left)
    ARROW_X + (ARROW_W - PILL_W) // 2,  # Micro-batch (center)
    ARROW_X + ARROW_W - PILL_W - 10,  # Streaming (right)
]

# Labels below arrow
LABEL_Y = ARROW_Y + 25
LABEL_H = math.ceil(1 * 20 * 1.25)

# Frequency labels
freq_labels = ["Semi-Frequent", "Frequent", "Very Frequent"]

# Data type labels below frequency
DATA_LABEL_Y = LABEL_Y + LABEL_H + 15
DATA_LABEL_H = math.ceil(1 * 17 * 1.25)
data_labels = ["Bounded Data", "Bounded / Unbounded", "Unbounded Data"]

# === BUILD DIAGRAM ===

# Title
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "Data Ingestion Continuum",
    32,
    color="#1e1e1e",
)

# Main arrow line (horizontal) — has an arrowhead, so use d.arr()
d.arr("arrow-main", ARROW_X, ARROW_Y, [[0, 0], [ARROW_W, 0]], GRAY[0])

# Pill boxes: Batch, Micro-batch, Streaming
pill_colors = [BLUE, YELLOW, RED]
pill_labels = ["Batch", "Micro-batch", "Streaming"]

for i, (px, label, color) in enumerate(zip(pill_positions, pill_labels, pill_colors)):
    box_id = f"pill-{i}"
    txt_id = f"pill-t-{i}"
    d.rect(
        box_id,
        px,
        PILL_Y,
        PILL_W,
        PILL_H,
        color[0],
        color[1],
        bnd=[{"id": txt_id, "type": "text"}],
    )
    d.txt(txt_id, px, PILL_Y, PILL_W, PILL_H, label, 24, cid=box_id)

# Frequency labels below arrow
for i, (px, label) in enumerate(zip(pill_positions, freq_labels)):
    d.txt(f"freq-{i}", px, LABEL_Y, PILL_W, LABEL_H, label, 20, color=GRAY[0])

# Data type labels
for i, (px, label) in enumerate(zip(pill_positions, data_labels)):
    d.txt(
        f"data-{i}",
        px,
        DATA_LABEL_Y,
        PILL_W,
        DATA_LABEL_H,
        label,
        17,
        color=pill_colors[i][0],
    )

# === WRITE FILE ===
outfile = "diagrams/artifacts/ingestion-continuum.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
