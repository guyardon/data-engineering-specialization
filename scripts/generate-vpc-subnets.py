"""
Excalidraw diagram: Configure VPC and Subnets.

Layout: Title at top, VPC container with two AZ containers side by side,
each AZ has public + private subnet stacked vertically.
Below VPC: row of 3 concept pills.
"""

import math

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, RED

d = ExcalidrawDiagram(seed=1000)

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
d.rect(
    "title_r",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    title_rect_h,
    "transparent",
    "transparent",
    fill="hachure",
    opacity=0,
    bnd=[{"id": "title_t", "type": "text"}],
)
d.txt(
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
d.rect(
    "vpc",
    VPC_X,
    VPC_Y,
    VPC_W,
    VPC_H,
    *PURPLE,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "vpc_t", "type": "text"}],
)
d.txt(
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
d.txt(
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
d.rect("az1", az1_x, AZ_Y, AZ_INNER_W, AZ_H, *BLUE, fill="hachure", dashed=True)
d.txt(
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
d.rect(
    "pub1",
    pub1_x,
    pub1_y,
    SUBNET_W,
    SUBNET_H,
    *YELLOW,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "pub1_t", "type": "text"}],
)
d.txt(
    "pub1_t",
    pub1_x,
    pub1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Public Subnet",
    22,
    cid="pub1",
)
d.txt(
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
d.rect(
    "priv1",
    pub1_x,
    priv1_y,
    SUBNET_W,
    SUBNET_H,
    *RED,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "priv1_t", "type": "text"}],
)
d.txt(
    "priv1_t",
    pub1_x,
    priv1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Private Subnet",
    22,
    cid="priv1",
)
d.txt(
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
d.rect("az2", az2_x, AZ_Y, AZ_INNER_W, AZ_H, *BLUE, fill="hachure", dashed=True)
d.txt(
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
d.rect(
    "pub2",
    pub2_x,
    pub1_y,
    SUBNET_W,
    SUBNET_H,
    *YELLOW,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "pub2_t", "type": "text"}],
)
d.txt(
    "pub2_t",
    pub2_x,
    pub1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Public Subnet",
    22,
    cid="pub2",
)
d.txt(
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
d.rect(
    "priv2",
    pub2_x,
    priv1_y,
    SUBNET_W,
    SUBNET_H,
    *RED,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "priv2_t", "type": "text"}],
)
d.txt(
    "priv2_t",
    pub2_x,
    priv1_y,
    SUBNET_W,
    SUBNET_TITLE_H + 15,
    "Private Subnet",
    22,
    cid="priv2",
)
d.txt(
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
    d.rect(rid, px, PILL_Y, PILL_W, PILL_H, *color, fill="hachure", bnd=[{"id": tid, "type": "text"}])
    d.txt(tid, px, PILL_Y, PILL_W, PILL_H, label, 20, cid=rid)


# === VERIFY ===
print(f"Title: y={TITLE_Y}..{TITLE_Y + title_rect_h}")
print(f"VPC: y={VPC_Y}..{VPC_Y + VPC_H}, w={VPC_W}")
print(f"AZs: y={AZ_Y}..{AZ_Y + AZ_H}, w={AZ_INNER_W}")
print(f"Public subnets: y={pub1_y}..{pub1_y + SUBNET_H}")
print(f"Private subnets: y={priv1_y}..{priv1_y + SUBNET_H}")
print(f"Concept pills: y={PILL_Y}..{PILL_Y + PILL_H}")
print(f"Canvas: {CANVAS_W} x {CANVAS_H}")
print(f"Elements: {len(d.elements)}")

# === WRITE FILE ===
d.save("diagrams/vpc-subnets.excalidraw")
print("Wrote diagrams/vpc-subnets.excalidraw")
