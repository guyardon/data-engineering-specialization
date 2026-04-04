"""Generate Streaming Components diagram for Course 2, Section 1.1.9."""

import json
import math
import sys

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 2000


def ns():
    global seed
    seed += 1
    return seed


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
PURPLE = ("#6741d9", "#d0bfff")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append(
        {
            "type": "rectangle",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1,
            "opacity": opacity,
            "roundness": {"type": 3},
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append(
        {
            "type": "text",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "text": t,
            "originalText": t,
            "fontSize": sz,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "lineHeight": 1.25,
            "autoResize": True,
            "containerId": cid,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append(
        {
            "type": "arrow",
            "id": id,
            "x": x,
            "y": y,
            "width": abs(pts[-1][0] - pts[0][0]),
            "height": abs(pts[-1][1] - pts[0][1]),
            "angle": 0,
            "points": pts,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "startBinding": sb,
            "endBinding": eb,
            "elbowed": False,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "dashed" if dash else "solid",
            "roughness": 1,
            "opacity": op,
            "seed": ns(),
            "version": 1,
            "versionNonce": ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# === LAYOUT CONSTANTS ===
# Vertical flow: Producer → Collector → Broker → (MQ | Platform) → Consumer

CANVAS_W = 700
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 660

BOX_W = 300
BOX_H = 110
BOX_X = PAD_X + (CONTENT_W - BOX_W) // 2  # centered

# Title + subtitle sizing (Rule 13)
HDR_TITLE_FSZ = 26
HDR_SUB_FSZ = 19
title_h = math.ceil(1 * HDR_TITLE_FSZ * 1.25)  # 30
sub_h = math.ceil(1 * HDR_SUB_FSZ * 1.25)  # 22
gap_ts = 6
combined_h = title_h + gap_ts + sub_h  # 58
top_pad = (BOX_H - combined_h) // 2  # 18

# Pair boxes for fan-out
PAIR_GAP = 30
PAIR_W = (BOX_W * 2 + PAIR_GAP - PAIR_GAP) // 2  # same as BOX_W for symmetry
PAIR_W = (CONTENT_W - PAIR_GAP) // 2  # 315 each, full width
# Actually, keep them proportional to the single boxes
PAIR_W = 280
PAIR_X1 = PAD_X + (CONTENT_W - 2 * PAIR_W - PAIR_GAP) // 2
PAIR_X2 = PAIR_X1 + PAIR_W + PAIR_GAP

ARR_GAP = 85

# Vertical positions
TITLE_Y = 15
TITLE_FSZ = 34
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)  # 40

Y1 = TITLE_Y + TITLE_H + 30  # Producer: 80
Y2 = Y1 + BOX_H + ARR_GAP  # Collector: 215
Y3 = Y2 + BOX_H + ARR_GAP  # Broker: 350
Y4 = Y3 + BOX_H + ARR_GAP  # MQ & Platform: 485
Y5 = Y4 + BOX_H + ARR_GAP  # Consumer: 620


# === BUILD DIAGRAM ===

# Title
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Streaming Architecture", TITLE_FSZ)

# --- Producer ---
rect("prod", BOX_X, Y1, BOX_W, BOX_H, *GREEN, bnd=[{"id": "prod-t", "type": "text"}])
txt(
    "prod-t",
    BOX_X,
    Y1 + top_pad,
    BOX_W,
    title_h,
    "Producers",
    HDR_TITLE_FSZ,
    cid="prod",
)
txt(
    "prod-sub",
    BOX_X,
    Y1 + top_pad + title_h + gap_ts,
    BOX_W,
    sub_h,
    "Generate events",
    HDR_SUB_FSZ,
    color=GREEN[0],
)

# --- Event Collector ---
rect("coll", BOX_X, Y2, BOX_W, BOX_H, *BLUE, bnd=[{"id": "coll-t", "type": "text"}])
txt(
    "coll-t",
    BOX_X,
    Y2 + top_pad,
    BOX_W,
    title_h,
    "Event Collector",
    HDR_TITLE_FSZ,
    cid="coll",
)
txt(
    "coll-sub",
    BOX_X,
    Y2 + top_pad + title_h + gap_ts,
    BOX_W,
    sub_h,
    "Groups into batches",
    HDR_SUB_FSZ,
    color=BLUE[0],
)

# --- Broker / Router ---
rect(
    "broker", BOX_X, Y3, BOX_W, BOX_H, *YELLOW, bnd=[{"id": "broker-t", "type": "text"}]
)
txt(
    "broker-t",
    BOX_X,
    Y3 + top_pad,
    BOX_W,
    title_h,
    "Broker / Router",
    HDR_TITLE_FSZ,
    cid="broker",
)
txt(
    "broker-sub",
    BOX_X,
    Y3 + top_pad + title_h + gap_ts,
    BOX_W,
    sub_h,
    "Routes messages",
    HDR_SUB_FSZ,
    color=YELLOW[0],
)

# --- Fan-out: Message Queue & Streaming Platform ---
rect("mq", PAIR_X1, Y4, PAIR_W, BOX_H, *PURPLE, bnd=[{"id": "mq-t", "type": "text"}])
txt(
    "mq-t",
    PAIR_X1,
    Y4 + top_pad,
    PAIR_W,
    title_h,
    "Message Queue",
    HDR_TITLE_FSZ,
    cid="mq",
)
txt(
    "mq-sub",
    PAIR_X1,
    Y4 + top_pad + title_h + gap_ts,
    PAIR_W,
    sub_h,
    "Buffers (SQS, FIFO)",
    HDR_SUB_FSZ,
    color=PURPLE[0],
)

rect("plat", PAIR_X2, Y4, PAIR_W, BOX_H, *CYAN, bnd=[{"id": "plat-t", "type": "text"}])
txt(
    "plat-t",
    PAIR_X2,
    Y4 + top_pad,
    PAIR_W,
    title_h,
    "Streaming Platform",
    HDR_TITLE_FSZ,
    cid="plat",
)
txt(
    "plat-sub",
    PAIR_X2,
    Y4 + top_pad + title_h + gap_ts,
    PAIR_W,
    sub_h,
    "Persistent (Kafka, Kinesis)",
    HDR_SUB_FSZ,
    color=CYAN[0],
)

# --- Consumer ---
rect("cons", BOX_X, Y5, BOX_W, BOX_H, *RED, bnd=[{"id": "cons-t", "type": "text"}])
txt(
    "cons-t",
    BOX_X,
    Y5 + top_pad,
    BOX_W,
    title_h,
    "Consumers",
    HDR_TITLE_FSZ,
    cid="cons",
)
txt(
    "cons-sub",
    BOX_X,
    Y5 + top_pad + title_h + gap_ts,
    BOX_W,
    sub_h,
    "Process or store data",
    HDR_SUB_FSZ,
    color=RED[0],
)

# --- Arrows ---
# Producer → Collector
arr(
    "a1",
    BOX_X + BOX_W // 2,
    Y1 + BOX_H,
    [[0, 0], [0, ARR_GAP]],
    GREEN[0],
    sb={"elementId": "prod", "focus": 0, "gap": 4},
    eb={"elementId": "coll", "focus": 0, "gap": 4},
)

# Collector → Broker
arr(
    "a2",
    BOX_X + BOX_W // 2,
    Y2 + BOX_H,
    [[0, 0], [0, ARR_GAP]],
    BLUE[0],
    sb={"elementId": "coll", "focus": 0, "gap": 4},
    eb={"elementId": "broker", "focus": 0, "gap": 4},
)

# Broker → Message Queue (fan-out left)
broker_cx = BOX_X + BOX_W // 2
mq_cx = PAIR_X1 + PAIR_W // 2
arr(
    "a3",
    broker_cx,
    Y3 + BOX_H,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [mq_cx - broker_cx, ARR_GAP // 2],
        [mq_cx - broker_cx, ARR_GAP],
    ],
    YELLOW[0],
    sb={"elementId": "broker", "focus": 0, "gap": 4},
    eb={"elementId": "mq", "focus": 0, "gap": 4},
)

# Broker → Streaming Platform (fan-out right)
plat_cx = PAIR_X2 + PAIR_W // 2
arr(
    "a4",
    broker_cx,
    Y3 + BOX_H,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [plat_cx - broker_cx, ARR_GAP // 2],
        [plat_cx - broker_cx, ARR_GAP],
    ],
    YELLOW[0],
    sb={"elementId": "broker", "focus": 0, "gap": 4},
    eb={"elementId": "plat", "focus": 0, "gap": 4},
)

# Message Queue → Consumer (fan-in left)
cons_cx = BOX_X + BOX_W // 2
arr(
    "a5",
    mq_cx,
    Y4 + BOX_H,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [cons_cx - mq_cx, ARR_GAP // 2],
        [cons_cx - mq_cx, ARR_GAP],
    ],
    PURPLE[0],
    sb={"elementId": "mq", "focus": 0, "gap": 4},
    eb={"elementId": "cons", "focus": 0, "gap": 4},
)

# Streaming Platform → Consumer (fan-in right)
arr(
    "a6",
    plat_cx,
    Y4 + BOX_H,
    [
        [0, 0],
        [0, ARR_GAP // 2],
        [cons_cx - plat_cx, ARR_GAP // 2],
        [cons_cx - plat_cx, ARR_GAP],
    ],
    CYAN[0],
    sb={"elementId": "plat", "focus": 0, "gap": 4},
    eb={"elementId": "cons", "focus": 0, "gap": 4},
)


# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"Boxes: x={BOX_X}, w={BOX_W}")
print(f"Pairs: x1={PAIR_X1}, x2={PAIR_X2}, w={PAIR_W}")
print(f"Rows: y1={Y1}, y2={Y2}, y3={Y3}, y4={Y4}, y5={Y5}")
print(f"Bottom: {Y5 + BOX_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/streaming-components"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
