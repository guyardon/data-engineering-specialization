"""
Generate Message Queue vs Event Streaming Platform comparison diagram.

Two vertical columns side by side:
  Left:  Message Queue -- Producer -> Queue (FIFO) -> Consumer (consumed & removed)
  Right: Event Streaming -- Producer -> Event Log (append-only) -> Consumer A, Consumer B (fan-out)
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT CONSTANTS ===

BW = 220  # box width
BH = 70  # box height
ARR_GAP = 90  # vertical gap between boxes (for arrows)
COL_GAP = 140  # horizontal gap between columns
PAD_X = 60  # left padding

# Consumer boxes are narrower for the fan-out
CBW = 180  # consumer box width
CBH = 60  # consumer box height
FAN_GAP = 30  # horizontal gap between fan-out consumers

# Column x positions
COL1_X = PAD_X
COL2_X = COL1_X + BW + COL_GAP

CANVAS_W = COL2_X + BW + PAD_X

# Vertical positions
TITLE_Y = 20
PILL_Y = 80
PILL_H = 50

ROW1_Y = PILL_Y + PILL_H + 40  # Producer
ROW2_Y = ROW1_Y + BH + ARR_GAP  # Queue / Event Log
ROW3_Y = ROW2_Y + BH + ARR_GAP  # Consumer(s)

# Center of each column for arrows
COL1_CX = COL1_X + BW // 2
COL2_CX = COL2_X + BW // 2

# Fan-out consumer positions (right column, row 3)
# Two consumers centered under the Event Log box
TOTAL_FANS_W = CBW * 2 + FAN_GAP
FAN_LEFT_X = COL2_X + (BW - TOTAL_FANS_W) // 2
FAN_RIGHT_X = FAN_LEFT_X + CBW + FAN_GAP

# === BUILD DIAGRAM ===

# Title
d.txt("title", 0, TITLE_Y, CANVAS_W, 40, "Message Queue vs. Event Streaming", 32)

# --- MESSAGE QUEUE COLUMN (left) ---

# Pill
PILL_W = 180
d.rect(
    "mq_pill",
    COL1_X + (BW - PILL_W) // 2,
    PILL_Y,
    PILL_W,
    PILL_H,
    *BLUE,
    bnd=[{"id": "mq_pill_t", "type": "text"}],
)
d.txt(
    "mq_pill_t",
    COL1_X + (BW - PILL_W) // 2,
    PILL_Y,
    PILL_W,
    PILL_H,
    "Message Queue",
    24,
    cid="mq_pill",
)

# Producer
d.rect(
    "mq_prod", COL1_X, ROW1_Y, BW, BH, *GRAY, bnd=[{"id": "mq_prod_t", "type": "text"}]
)
d.txt("mq_prod_t", COL1_X, ROW1_Y, BW, BH, "Producer", 22, cid="mq_prod")

# Arrow: Producer -> Queue
d.arr(
    "mq_a1",
    COL1_CX,
    ROW1_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    GRAY[0],
    sb={"elementId": "mq_prod", "focus": 0, "gap": 4},
    eb={"elementId": "mq_queue", "focus": 0, "gap": 4},
)

# Message Queue (FIFO buffer)
d.rect(
    "mq_queue",
    COL1_X,
    ROW2_Y,
    BW,
    BH,
    *BLUE,
    bnd=[{"id": "mq_queue_t", "type": "text"}],
)
d.txt(
    "mq_queue_t",
    COL1_X,
    ROW2_Y,
    BW,
    BH,
    "Message Queue\n(FIFO buffer)",
    20,
    cid="mq_queue",
)

# Arrow: Queue -> Consumer
d.arr(
    "mq_a2",
    COL1_CX,
    ROW2_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    BLUE[0],
    sb={"elementId": "mq_queue", "focus": 0, "gap": 4},
    eb={"elementId": "mq_cons", "focus": 0, "gap": 4},
)

# Label on last arrow: "message consumed & removed"
d.txt(
    "mq_lab_consumed",
    COL1_CX + 12,
    ROW2_Y + BH + ARR_GAP // 2 - 14,
    160,
    28,
    "message consumed\n& removed",
    17,
    op=70,
)

# Consumer
d.rect(
    "mq_cons",
    COL1_X,
    ROW3_Y,
    BW,
    BH,
    *PURPLE,
    bnd=[{"id": "mq_cons_t", "type": "text"}],
)
d.txt("mq_cons_t", COL1_X, ROW3_Y, BW, BH, "Consumer", 22, cid="mq_cons")

# --- EVENT STREAMING COLUMN (right) ---

# Pill
ESP_PILL_W = 220
d.rect(
    "es_pill",
    COL2_X + (BW - ESP_PILL_W) // 2,
    PILL_Y,
    ESP_PILL_W,
    PILL_H,
    *GREEN,
    bnd=[{"id": "es_pill_t", "type": "text"}],
)
d.txt(
    "es_pill_t",
    COL2_X + (BW - ESP_PILL_W) // 2,
    PILL_Y,
    ESP_PILL_W,
    PILL_H,
    "Event Streaming",
    24,
    cid="es_pill",
)

# Producer
d.rect(
    "es_prod", COL2_X, ROW1_Y, BW, BH, *GRAY, bnd=[{"id": "es_prod_t", "type": "text"}]
)
d.txt("es_prod_t", COL2_X, ROW1_Y, BW, BH, "Producer", 22, cid="es_prod")

# Arrow: Producer -> Event Log
d.arr(
    "es_a1",
    COL2_CX,
    ROW1_Y + BH,
    [[0, 0], [0, ARR_GAP]],
    GRAY[0],
    sb={"elementId": "es_prod", "focus": 0, "gap": 4},
    eb={"elementId": "es_log", "focus": 0, "gap": 4},
)

# Event Log (append-only)
d.rect("es_log", COL2_X, ROW2_Y, BW, BH, *GREEN, bnd=[{"id": "es_log_t", "type": "text"}])
d.txt("es_log_t", COL2_X, ROW2_Y, BW, BH, "Event Log\n(append-only)", 20, cid="es_log")

# Label near event log: "replay / reprocess"
d.txt(
    "es_lab_replay",
    COL2_X + BW + 12,
    ROW2_Y + BH // 2 - 12,
    140,
    24,
    "replay /\nreprocess",
    17,
    op=70,
    align="left",
)

# Curved arrow looping back to the log (dashed, indicating replay)
d.arr(
    "es_replay_arr",
    COL2_X + BW + 8,
    ROW2_Y + BH - 10,
    [[0, 0], [30, 30], [0, 50], [-20, 30]],
    GREEN[0],
    dash=True,
    op=50,
)

# Arrow: Event Log -> Consumer A (fan-out left)
FAN_A_CX = FAN_LEFT_X + CBW // 2
d.arr(
    "es_a2a",
    COL2_CX,
    ROW2_Y + BH,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [FAN_A_CX - COL2_CX, ARR_GAP // 2],
        [FAN_A_CX - COL2_CX, ARR_GAP],
    ],
    GREEN[0],
    sb={"elementId": "es_log", "focus": 0, "gap": 4},
    eb={"elementId": "es_cons_a", "focus": 0, "gap": 4},
)

# Arrow: Event Log -> Consumer B (fan-out right)
FAN_B_CX = FAN_RIGHT_X + CBW // 2
d.arr(
    "es_a2b",
    COL2_CX,
    ROW2_Y + BH,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [FAN_B_CX - COL2_CX, ARR_GAP // 2],
        [FAN_B_CX - COL2_CX, ARR_GAP],
    ],
    GREEN[0],
    sb={"elementId": "es_log", "focus": 0, "gap": 4},
    eb={"elementId": "es_cons_b", "focus": 0, "gap": 4},
)

# Consumer A
d.rect(
    "es_cons_a",
    FAN_LEFT_X,
    ROW3_Y,
    CBW,
    CBH,
    *PURPLE,
    bnd=[{"id": "es_cons_a_t", "type": "text"}],
)
d.txt("es_cons_a_t", FAN_LEFT_X, ROW3_Y, CBW, CBH, "Consumer A", 22, cid="es_cons_a")

# Consumer B
d.rect(
    "es_cons_b",
    FAN_RIGHT_X,
    ROW3_Y,
    CBW,
    CBH,
    *CYAN,
    bnd=[{"id": "es_cons_b_t", "type": "text"}],
)
d.txt("es_cons_b_t", FAN_RIGHT_X, ROW3_Y, CBW, CBH, "Consumer B", 22, cid="es_cons_b")

# Vertical divider between columns
DIV_X = COL1_X + BW + COL_GAP // 2
d.rect(
    "divider",
    DIV_X,
    PILL_Y,
    2,
    ROW3_Y + BH - PILL_Y,
    GRAY[0],
    "transparent",
    opacity=15,
)

# === VERIFY ===

print(f"Column 1 (MQ):  x={COL1_X} to {COL1_X + BW}")
print(f"Column 2 (ESP): x={COL2_X} to {COL2_X + BW}")
print(f"Canvas width: {CANVAS_W}")
print(f"Fan-out left:  x={FAN_LEFT_X} to {FAN_LEFT_X + CBW}")
print(f"Fan-out right: x={FAN_RIGHT_X} to {FAN_RIGHT_X + CBW}")
print(f"Vertical extent: {TITLE_Y} to {ROW3_Y + BH}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "streaming-concepts"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
