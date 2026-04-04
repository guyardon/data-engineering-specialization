"""
Excalidraw diagram: Configure VPC and Subnets.

Layout: Title at top, VPC container with two AZ containers side by side,
each AZ has public + private subnet stacked vertically.
Below VPC: row of 3 concept pills.
"""

import json
import math
import os

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


BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
YELLOW = ("#e67700", "#ffec99")
PURPLE = ("#6741d9", "#d0bfff")
RED = ("#c92a2a", "#ffc9c9")
CYAN = ("#0c8599", "#99e9f2")
GRAY = ("#868e96", "#dee2e6")


def rect(
    id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None
):
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
            "width": pts[-1][0] - pts[0][0],
            "height": pts[-1][1] - pts[0][1],
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

CANVAS_W = 950
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 890

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)  # 40

# VPC container
VPC_PAD = 25
VPC_Y = TITLE_Y + TITLE_H + 30  # 90
VPC_X = PAD_X

# VPC title + subtitle area
VPC_TITLE_H = math.ceil(1 * 24 * 1.25)  # 30
VPC_SUBTITLE_H = math.ceil(1 * 17 * 1.25)  # 22
VPC_HEADER_AREA = VPC_TITLE_H + VPC_SUBTITLE_H + 10  # space for title + subtitle

# AZ containers side by side
AZ_GAP = 30
AZ_Y = VPC_Y + VPC_PAD + VPC_HEADER_AREA + 10  # after VPC header
AZ_PAD = 20
AZ_INNER_W = (CONTENT_W - 2 * VPC_PAD - AZ_GAP) // 2  # ~395

# Subnet boxes inside each AZ (stacked vertically)
SUBNET_GAP = 20
SUBNET_W = AZ_INNER_W - 2 * AZ_PAD

# Subnet dimensions: title (bound) + subtitle + padding
SUBNET_TITLE_H = math.ceil(1 * 22 * 1.25)  # 28
SUBNET_CIDR_H = math.ceil(1 * 17 * 1.25)  # 22
SUBNET_H = SUBNET_TITLE_H + SUBNET_CIDR_H + 30  # 80

# AZ dimensions
AZ_LABEL_H = math.ceil(1 * 22 * 1.25)  # 28
AZ_H = AZ_LABEL_H + 15 + 2 * SUBNET_H + SUBNET_GAP + AZ_PAD  # ~231

# VPC dimensions
VPC_W = CONTENT_W
VPC_H = VPC_PAD + VPC_HEADER_AREA + 10 + AZ_H + VPC_PAD  # everything inside

# Concept pills below VPC
PILL_Y = VPC_Y + VPC_H + 30
PILL_W = 220
PILL_H = 50
PILL_GAP = 25
PILL_TOTAL = 3 * PILL_W + 2 * PILL_GAP
PILL_X0 = (CANVAS_W - PILL_TOTAL) // 2

CANVAS_H = PILL_Y + PILL_H + 30

# === BUILD DIAGRAM ===

# --- Title (Rule 13: bound text in rect) ---
title_rect_h = TITLE_H + 10
rect(
    "title_r",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    title_rect_h,
    "transparent",
    "transparent",
    fill="solid",
    opacity=0,
    bnd=[{"id": "title_t", "type": "text"}],
)
txt(
    "title_t",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    title_rect_h,
    "Configure VPC and Subnets",
    32,
    cid="title_r",
)

# --- VPC container (PURPLE, dashed) ---
rect(
    "vpc",
    VPC_X,
    VPC_Y,
    VPC_W,
    VPC_H,
    *PURPLE,
    dashed=True,
    bnd=[{"id": "vpc_t", "type": "text"}],
)
txt(
    "vpc_t",
    VPC_X,
    VPC_Y,
    VPC_W,
    VPC_TITLE_H + VPC_PAD,
    "VPC (10.0.0.0/16)",
    24,
    color=PURPLE[0],
    cid="vpc",
)

# VPC subtitle
vpc_sub_y = VPC_Y + VPC_PAD + VPC_TITLE_H + 2
txt(
    "vpc_sub",
    VPC_X,
    vpc_sub_y,
    VPC_W,
    VPC_SUBTITLE_H,
    "Private IP range: 10.0.x.x",
    17,
    color=PURPLE[0],
)

# --- AZ 1 (left, BLUE dashed) ---
az1_x = VPC_X + VPC_PAD
rect("az1", az1_x, AZ_Y, AZ_INNER_W, AZ_H, *BLUE, dashed=True)
txt(
    "az1_label",
    az1_x,
    AZ_Y + 8,
    AZ_INNER_W,
    AZ_LABEL_H,
    "Availability Zone 1",
    22,
    color=BLUE[0],
)

# Public subnet 1 (YELLOW dashed)
pub1_x = az1_x + AZ_PAD
pub1_y = AZ_Y + AZ_LABEL_H + 15
rect(
    "pub1",
    pub1_x,
    pub1_y,
    SUBNET_W,
    SUBNET_H,
    *YELLOW,
    dashed=True,
    bnd=[{"id": "pub1_t", "type": "text"}],
)
txt(
    "pub1_t",
    pub1_x,
    pub1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Public Subnet",
    22,
    cid="pub1",
)
txt(
    "pub1_cidr",
    pub1_x,
    pub1_y + SUBNET_TITLE_H + 15,
    SUBNET_W,
    SUBNET_CIDR_H,
    "10.0.1.0/24",
    17,
    color=YELLOW[0],
)

# Private subnet 1 (RED dashed)
priv1_y = pub1_y + SUBNET_H + SUBNET_GAP
rect(
    "priv1",
    pub1_x,
    priv1_y,
    SUBNET_W,
    SUBNET_H,
    *RED,
    dashed=True,
    bnd=[{"id": "priv1_t", "type": "text"}],
)
txt(
    "priv1_t",
    pub1_x,
    priv1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Private Subnet",
    22,
    cid="priv1",
)
txt(
    "priv1_cidr",
    pub1_x,
    priv1_y + SUBNET_TITLE_H + 15,
    SUBNET_W,
    SUBNET_CIDR_H,
    "10.0.2.0/24",
    17,
    color=RED[0],
)

# --- AZ 2 (right, BLUE dashed) ---
az2_x = az1_x + AZ_INNER_W + AZ_GAP
rect("az2", az2_x, AZ_Y, AZ_INNER_W, AZ_H, *BLUE, dashed=True)
txt(
    "az2_label",
    az2_x,
    AZ_Y + 8,
    AZ_INNER_W,
    AZ_LABEL_H,
    "Availability Zone 2",
    22,
    color=BLUE[0],
)

# Public subnet 2 (YELLOW dashed)
pub2_x = az2_x + AZ_PAD
rect(
    "pub2",
    pub2_x,
    pub1_y,
    SUBNET_W,
    SUBNET_H,
    *YELLOW,
    dashed=True,
    bnd=[{"id": "pub2_t", "type": "text"}],
)
txt(
    "pub2_t",
    pub2_x,
    pub1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Public Subnet",
    22,
    cid="pub2",
)
txt(
    "pub2_cidr",
    pub2_x,
    pub1_y + SUBNET_TITLE_H + 15,
    SUBNET_W,
    SUBNET_CIDR_H,
    "10.0.3.0/24",
    17,
    color=YELLOW[0],
)

# Private subnet 2 (RED dashed)
rect(
    "priv2",
    pub2_x,
    priv1_y,
    SUBNET_W,
    SUBNET_H,
    *RED,
    dashed=True,
    bnd=[{"id": "priv2_t", "type": "text"}],
)
txt(
    "priv2_t",
    pub2_x,
    priv1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Private Subnet",
    22,
    cid="priv2",
)
txt(
    "priv2_cidr",
    pub2_x,
    priv1_y + SUBNET_TITLE_H + 15,
    SUBNET_W,
    SUBNET_CIDR_H,
    "10.0.4.0/24",
    17,
    color=RED[0],
)

# --- Concept pills ---
pill_items = [
    ("CIDR Block", GREEN),
    ("Availability Zone", BLUE),
    ("Subnet Isolation", PURPLE),
]
for i, (label, color) in enumerate(pill_items):
    px = PILL_X0 + i * (PILL_W + PILL_GAP)
    rid = f"pill_{i}"
    tid = f"pill_t_{i}"
    rect(rid, px, PILL_Y, PILL_W, PILL_H, *color, bnd=[{"id": tid, "type": "text"}])
    txt(tid, px, PILL_Y, PILL_W, PILL_H, label, 20, cid=rid)


# === VERIFY ===
print(f"Title: y={TITLE_Y}..{TITLE_Y + title_rect_h}")
print(f"VPC: y={VPC_Y}..{VPC_Y + VPC_H}, w={VPC_W}")
print(f"AZs: y={AZ_Y}..{AZ_Y + AZ_H}, w={AZ_INNER_W}")
print(f"Public subnets: y={pub1_y}..{pub1_y + SUBNET_H}")
print(f"Private subnets: y={priv1_y}..{priv1_y + SUBNET_H}")
print(f"Concept pills: y={PILL_Y}..{PILL_Y + PILL_H}")
print(f"Canvas: {CANVAS_W} x {CANVAS_H}")
print(f"Elements: {len(els)}")

# === WRITE FILE ===
outdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams"
)
outfile = os.path.join(outdir, "vpc-subnets.excalidraw")
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
