"""
Generate Kafka Architecture diagram.

Vertical flow:
  Producers (top) -> Kafka Cluster (brokers with partitions) -> Consumers (bottom)
"""

import json
import math
import sys

# === FILE STRUCTURE ===

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
    "files": {},
}
els = data["elements"]
seed = 1000


def ns():
    global seed
    seed += 1
    return seed


# === COLOR PALETTE ===

BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


# === HELPER FUNCTIONS ===


def rect(id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None):
    els.append({
        "type": "rectangle", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
        "opacity": opacity, "roundness": {"type": 3},
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": bnd or [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100, align="center"):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "middle", "lineHeight": 1.25,
        "autoResize": True, "containerId": cid,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


def arr(id, x, y, pts, stroke, dash=False, op=100, sb=None, eb=None):
    els.append({
        "type": "arrow", "id": id, "x": x, "y": y,
        "width": pts[-1][0] - pts[0][0], "height": pts[-1][1] - pts[0][1],
        "angle": 0, "points": pts,
        "startArrowhead": None, "endArrowhead": "arrow",
        "startBinding": sb, "endBinding": eb, "elbowed": False,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dash else "solid",
        "roughness": 1, "opacity": op,
        "seed": ns(), "version": 1, "versionNonce": ns(),
        "isDeleted": False, "groupIds": [], "boundElements": [],
        "frameId": None, "link": None, "locked": False, "updated": 1710000000000,
    })


# === LAYOUT CONSTANTS ===

# Overall canvas
PAD_X = 40
TITLE_Y = 20

# Producer boxes
PROD_W = 140
PROD_H = 60
PROD_GAP = 30          # gap between producer boxes
NUM_PROD = 3

# Cluster container
CLUSTER_PAD = 25       # internal padding of cluster container

# Broker boxes
BROKER_W = 220
BROKER_H = 130
BROKER_GAP = 40        # gap between brokers
NUM_BROKERS = 2

# Partition boxes (inside broker)
PART_W = 180
PART_H = 50

# Consumer boxes
CONS_W = 140
CONS_H = 60
CONS_GAP = 30
NUM_CONS = 3

# Arrow gaps
ARR_GAP = 80

# Calculate cluster interior width
CLUSTER_INNER_W = NUM_BROKERS * BROKER_W + (NUM_BROKERS - 1) * BROKER_GAP
CLUSTER_W = CLUSTER_INNER_W + 2 * CLUSTER_PAD
CLUSTER_H = BROKER_H + 2 * CLUSTER_PAD + 50  # extra 50 for cluster title

# Canvas width from cluster (widest element)
CANVAS_W = CLUSTER_W + 2 * PAD_X
CANVAS_CX = PAD_X + CLUSTER_W // 2

# Vertical positions
TITLE_H = 40
PROD_Y = TITLE_Y + TITLE_H + 20
ARR1_Y = PROD_Y + PROD_H           # arrow from producers to cluster
CLUSTER_Y = ARR1_Y + ARR_GAP
BROKER_Y = CLUSTER_Y + CLUSTER_PAD + 40  # 40 for cluster title text
ARR2_Y = CLUSTER_Y + CLUSTER_H     # arrow from cluster to consumers
CONS_Y = ARR2_Y + ARR_GAP

# Producer x positions (centered)
PROD_TOTAL_W = NUM_PROD * PROD_W + (NUM_PROD - 1) * PROD_GAP
PROD_START_X = CANVAS_CX - PROD_TOTAL_W // 2

# Cluster x position
CLUSTER_X = PAD_X

# Broker x positions (inside cluster)
BROKER_START_X = CLUSTER_X + CLUSTER_PAD

# Consumer x positions (centered)
CONS_TOTAL_W = NUM_CONS * CONS_W + (NUM_CONS - 1) * CONS_GAP
CONS_START_X = CANVAS_CX - CONS_TOTAL_W // 2


# === BUILD DIAGRAM ===

# Title
txt("title", 0, TITLE_Y, CANVAS_W + 2 * PAD_X, TITLE_H,
    "Apache Kafka Architecture", 32)

# --- PRODUCERS ---
for i in range(NUM_PROD):
    px = PROD_START_X + i * (PROD_W + PROD_GAP)
    rid = f"prod_{i}"
    tid = f"prod_{i}_t"
    label = f"Producer {i + 1}"
    rect(rid, px, PROD_Y, PROD_W, PROD_H, *BLUE,
         bnd=[{"id": tid, "type": "text"}])
    txt(tid, px, PROD_Y, PROD_W, PROD_H, label, 22, cid=rid)

# --- ARROW: PRODUCERS -> CLUSTER ---
arr("arr_prod_cluster", CANVAS_CX, ARR1_Y, [[0, 0], [0, ARR_GAP]], BLUE[0],
    sb={"elementId": "prod_1", "focus": 0, "gap": 4},
    eb={"elementId": "cluster", "focus": 0, "gap": 4})
# Label: push messages
txt("lbl_push", CANVAS_CX + 12, ARR1_Y + ARR_GAP // 2 - 12, 130, 24,
    "push messages", 18, op=70)

# --- KAFKA CLUSTER ---
rect("cluster", CLUSTER_X, CLUSTER_Y, CLUSTER_W, CLUSTER_H,
     GRAY[0], GRAY[1], dashed=True, opacity=40,
     bnd=[{"id": "arr_prod_cluster", "type": "arrow"},
          {"id": "arr_cluster_cons", "type": "arrow"}])

# Cluster title
txt("cluster_title", CLUSTER_X, CLUSTER_Y + 8, CLUSTER_W, 35,
    "Kafka Cluster", 26)

# --- BROKERS ---
for i in range(NUM_BROKERS):
    bx = BROKER_START_X + i * (BROKER_W + BROKER_GAP)
    bid = f"broker_{i}"
    btid = f"broker_{i}_t"
    pid = f"part_{i}"
    ptid = f"part_{i}_t"

    # Broker container
    rect(bid, bx, BROKER_Y, BROKER_W, BROKER_H, *CYAN, opacity=60,
         bnd=[{"id": btid, "type": "text"}])
    # Broker label at top of broker box
    txt(btid, bx, BROKER_Y + 6, BROKER_W, 28, f"Broker {i + 1}", 22, cid=bid)

    # Partition box inside broker
    part_x = bx + (BROKER_W - PART_W) // 2
    part_y = BROKER_Y + 50
    rect(pid, part_x, part_y, PART_W, PART_H, *PURPLE,
         bnd=[{"id": ptid, "type": "text"}])
    txt(ptid, part_x, part_y, PART_W, PART_H,
        "Topic / Partitions", 20, cid=pid)

# Subtitle: ordered, immutable logs
SUBTITLE_Y = BROKER_Y + BROKER_H + 6
txt("lbl_logs", CLUSTER_X, SUBTITLE_Y, CLUSTER_W, 22,
    "ordered, immutable logs", 18, op=60)

# --- ARROW: CLUSTER -> CONSUMERS ---
arr("arr_cluster_cons", CANVAS_CX, ARR2_Y, [[0, 0], [0, ARR_GAP]], GREEN[0],
    sb={"elementId": "cluster", "focus": 0, "gap": 4},
    eb={"elementId": "cons_1", "focus": 0, "gap": 4})
# Label: pull messages
txt("lbl_pull", CANVAS_CX + 12, ARR2_Y + ARR_GAP // 2 - 12, 130, 24,
    "pull messages", 18, op=70)

# --- CONSUMERS ---
for i in range(NUM_CONS):
    cx = CONS_START_X + i * (CONS_W + CONS_GAP)
    rid = f"cons_{i}"
    tid = f"cons_{i}_t"
    label = f"Consumer {i + 1}"
    rect(rid, cx, CONS_Y, CONS_W, CONS_H, *GREEN,
         bnd=[{"id": tid, "type": "text"}])
    txt(tid, cx, CONS_Y, CONS_W, CONS_H, label, 22, cid=rid)


# === VERIFY ===

print(f"Canvas: {CANVAS_W + 2 * PAD_X} x {CONS_Y + CONS_H + 20}")
print(f"Producers: y={PROD_Y}, Cluster: y={CLUSTER_Y}-{CLUSTER_Y + CLUSTER_H}")
print(f"Consumers: y={CONS_Y}")
print(f"Brokers at y={BROKER_Y}, partitions inside")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "kafka-architecture"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
