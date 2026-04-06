#!/usr/bin/env python3
"""Generate Excalidraw diagram: Batch vs Streaming Ingestion Considerations."""

import math

from diagramlib import ExcalidrawDiagram, BLUE, RED, GRAY

d = ExcalidrawDiagram(seed=2000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 820
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
COL_GAP = 30
COL_W = (CONTENT_W - COL_GAP) // 2

LEFT_X = PAD_X
RIGHT_X = PAD_X + COL_W + COL_GAP

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Column headers
HEADER_Y = TITLE_Y + TITLE_H + 30
HEADER_H = 65

# Rows
ROW_GAP = 15
ROW_H = 75
ROW_START_Y = HEADER_Y + HEADER_H + ROW_GAP

# Row data: (aspect, batch_text, streaming_text)
rows = [
    ("Latency", "Minutes to hours", "Milliseconds to seconds"),
    (
        "Complexity",
        "Simple to implement\nand maintain",
        "Complex infrastructure\nand monitoring",
    ),
    ("Cost", "Lower cost,\npay per batch run", "Higher cost,\nalways-on resources"),
    (
        "Use Cases",
        "Reports, training ML\nmodels, analytics",
        "Real-time predictions,\nalerts, dashboards",
    ),
    (
        "Availability",
        "Tolerates downtime\nbetween runs",
        "Requires high\navailability (HA)",
    ),
]


# Calculate row heights dynamically
def row_height(text):
    lines = text.count("\n") + 1
    return max(ROW_H, math.ceil(lines * 22 * 1.25) + 30)


# === BUILD DIAGRAM ===

# Title
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "Batch vs. Streaming Ingestion",
    32,
    color="#1e1e1e",
)

# Column headers
d.rect(
    "h-batch",
    LEFT_X,
    HEADER_Y,
    COL_W,
    HEADER_H,
    BLUE[0],
    BLUE[1],
    bnd=[{"id": "ht-batch", "type": "text"}],
)
d.txt("ht-batch", LEFT_X, HEADER_Y, COL_W, HEADER_H, "Batch", 26, cid="h-batch")

d.rect(
    "h-stream",
    RIGHT_X,
    HEADER_Y,
    COL_W,
    HEADER_H,
    RED[0],
    RED[1],
    bnd=[{"id": "ht-stream", "type": "text"}],
)
d.txt("ht-stream", RIGHT_X, HEADER_Y, COL_W, HEADER_H, "Streaming", 26, cid="h-stream")

# Rows
cur_y = ROW_START_Y
for i, (aspect, batch_txt, stream_txt) in enumerate(rows):
    rh = max(row_height(batch_txt), row_height(stream_txt))

    # Aspect label (centered between columns)
    aspect_h = math.ceil(1 * 20 * 1.25)
    d.txt(f"aspect-{i}", PAD_X, cur_y, CONTENT_W, aspect_h, aspect, 20, color=GRAY[0])

    card_y = cur_y + aspect_h + 8

    # Batch card
    d.rect(
        f"batch-{i}",
        LEFT_X,
        card_y,
        COL_W,
        rh,
        BLUE[0],
        BLUE[1],
        opacity=30,
        bnd=[{"id": f"bt-{i}", "type": "text"}],
    )
    d.txt(f"bt-{i}", LEFT_X, card_y, COL_W, rh, batch_txt, 22, cid=f"batch-{i}")

    # Streaming card
    d.rect(
        f"stream-{i}",
        RIGHT_X,
        card_y,
        COL_W,
        rh,
        RED[0],
        RED[1],
        opacity=30,
        bnd=[{"id": f"st-{i}", "type": "text"}],
    )
    d.txt(f"st-{i}", RIGHT_X, card_y, COL_W, rh, stream_txt, 22, cid=f"stream-{i}")

    cur_y = card_y + rh + ROW_GAP

# === WRITE FILE ===
outfile = "diagrams/artifacts/batch-vs-streaming.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
