"""
Excalidraw diagram: Cloud Networking Basics for section 1.2.4.

Shows Region → Availability Zones → VPC with public/private subnets.
Nested container layout to visualize the hierarchy.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, RED, CYAN, GRAY

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT CONSTANTS ===

CANVAS_W = 950
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 890

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Region container
REGION_PAD = 25
REGION_X = PAD_X
REGION_Y = TITLE_Y + TITLE_H + 30
REGION_W = CONTENT_W
REGION_LABEL_H = math.ceil(1 * 24 * 1.25)

# AZ boxes inside region
AZ_PAD = 20
AZ_GAP = 30
AZ_COUNT = 2
AZ_W = (REGION_W - 2 * REGION_PAD - (AZ_COUNT - 1) * AZ_GAP) // AZ_COUNT
AZ_Y = REGION_Y + REGION_LABEL_H + REGION_PAD + 10

# Data center pills inside each AZ
DC_W = AZ_W - 2 * AZ_PAD
DC_H = 50
DC_GAP = 15
DC_Y_START = AZ_Y + math.ceil(1 * 20 * 1.25) + AZ_PAD + 5

AZ_H = (DC_Y_START - AZ_Y) + 2 * DC_H + DC_GAP + AZ_PAD
REGION_H = (AZ_Y - REGION_Y) + AZ_H + REGION_PAD

# VPC container below region
VPC_GAP = 40
VPC_X = PAD_X
VPC_Y = REGION_Y + REGION_H + VPC_GAP
VPC_W = CONTENT_W
VPC_LABEL_H = math.ceil(1 * 24 * 1.25)

# Subnets inside VPC
SUBNET_PAD = 20
SUBNET_GAP = 30
SUBNET_W = (VPC_W - 2 * REGION_PAD - SUBNET_GAP) // 2
SUBNET_Y = VPC_Y + VPC_LABEL_H + REGION_PAD + 10

# Resources inside subnets
RES_W = SUBNET_W - 2 * SUBNET_PAD
RES_H = 50
RES_GAP = 15
RES_Y_START = SUBNET_Y + math.ceil(1 * 20 * 1.25) + SUBNET_PAD + 5

SUBNET_H = (RES_Y_START - SUBNET_Y) + 2 * RES_H + RES_GAP + SUBNET_PAD
VPC_H = (SUBNET_Y - VPC_Y) + SUBNET_H + REGION_PAD

# Internet gateway + NAT gateway row
GW_Y = VPC_Y + VPC_H + 35
GW_W = 200
GW_H = 55
GW_GAP = 80

# Region considerations
CONSID_Y = GW_Y + GW_H + 45
CONSID_LABEL_H = math.ceil(1 * 20 * 1.25)
PILL_W = 180
PILL_H = 50
PILL_GAP = 20
PILLS_TOTAL_W = 4 * PILL_W + 3 * PILL_GAP
PILLS_X0 = (CANVAS_W - PILLS_TOTAL_W) // 2
PILLS_Y = CONSID_Y + CONSID_LABEL_H + 12

CANVAS_H = PILLS_Y + PILL_H + 30

# === BUILD DIAGRAM ===

# --- Title ---
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H, "Cloud Networking Basics", 32)

# --- Region container ---
d.rect(
    "region",
    REGION_X,
    REGION_Y,
    REGION_W,
    REGION_H,
    *PURPLE,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "region_t", "type": "text"}],
)
d.txt(
    "region_t",
    REGION_X,
    REGION_Y,
    REGION_W,
    REGION_LABEL_H + REGION_PAD,
    "Region (e.g. us-east-1)",
    24,
    color=PURPLE[0],
    cid="region",
)

# --- AZ 1 ---
az1_x = REGION_X + REGION_PAD
d.rect("az1", az1_x, AZ_Y, AZ_W, AZ_H, *BLUE, fill="hachure", dashed=True)
d.txt(
    "az1_label",
    az1_x,
    AZ_Y + 8,
    AZ_W,
    math.ceil(1 * 20 * 1.25),
    "Availability Zone 1",
    20,
    color=BLUE[0],
)

d.rect(
    "dc1a",
    az1_x + AZ_PAD,
    DC_Y_START,
    DC_W,
    DC_H,
    *CYAN,
    fill="hachure",
    bnd=[{"id": "dc1a_t", "type": "text"}],
)
d.txt("dc1a_t", az1_x + AZ_PAD, DC_Y_START, DC_W, DC_H, "Data Center", 20, cid="dc1a")

d.rect(
    "dc1b",
    az1_x + AZ_PAD,
    DC_Y_START + DC_H + DC_GAP,
    DC_W,
    DC_H,
    *CYAN,
    fill="hachure",
    bnd=[{"id": "dc1b_t", "type": "text"}],
)
d.txt(
    "dc1b_t",
    az1_x + AZ_PAD,
    DC_Y_START + DC_H + DC_GAP,
    DC_W,
    DC_H,
    "Data Center",
    20,
    cid="dc1b",
)

# --- AZ 2 ---
az2_x = az1_x + AZ_W + AZ_GAP
d.rect("az2", az2_x, AZ_Y, AZ_W, AZ_H, *BLUE, fill="hachure", dashed=True)
d.txt(
    "az2_label",
    az2_x,
    AZ_Y + 8,
    AZ_W,
    math.ceil(1 * 20 * 1.25),
    "Availability Zone 2",
    20,
    color=BLUE[0],
)

d.rect(
    "dc2a",
    az2_x + AZ_PAD,
    DC_Y_START,
    DC_W,
    DC_H,
    *CYAN,
    fill="hachure",
    bnd=[{"id": "dc2a_t", "type": "text"}],
)
d.txt("dc2a_t", az2_x + AZ_PAD, DC_Y_START, DC_W, DC_H, "Data Center", 20, cid="dc2a")

d.rect(
    "dc2b",
    az2_x + AZ_PAD,
    DC_Y_START + DC_H + DC_GAP,
    DC_W,
    DC_H,
    *CYAN,
    fill="hachure",
    bnd=[{"id": "dc2b_t", "type": "text"}],
)
d.txt(
    "dc2b_t",
    az2_x + AZ_PAD,
    DC_Y_START + DC_H + DC_GAP,
    DC_W,
    DC_H,
    "Data Center",
    20,
    cid="dc2b",
)

# --- VPC container ---
d.rect(
    "vpc",
    VPC_X,
    VPC_Y,
    VPC_W,
    VPC_H,
    *GREEN,
    fill="hachure",
    dashed=True,
    bnd=[{"id": "vpc_t", "type": "text"}],
)
d.txt(
    "vpc_t",
    VPC_X,
    VPC_Y,
    VPC_W,
    VPC_LABEL_H + REGION_PAD,
    "VPC (Virtual Private Cloud)",
    24,
    color=GREEN[0],
    cid="vpc",
)

# --- Public subnet ---
pub_x = VPC_X + REGION_PAD
d.rect(
    "pub_sub", pub_x, SUBNET_Y, SUBNET_W, SUBNET_H, *YELLOW, fill="hachure", dashed=True
)
d.txt(
    "pub_label",
    pub_x,
    SUBNET_Y + 8,
    SUBNET_W,
    math.ceil(1 * 20 * 1.25),
    "Public Subnet",
    20,
    color=YELLOW[0],
)

d.rect(
    "alb",
    pub_x + SUBNET_PAD,
    RES_Y_START,
    RES_W,
    RES_H,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "alb_t", "type": "text"}],
)
d.txt("alb_t", pub_x + SUBNET_PAD, RES_Y_START, RES_W, RES_H, "ALB", 20, cid="alb")

d.rect(
    "nat",
    pub_x + SUBNET_PAD,
    RES_Y_START + RES_H + RES_GAP,
    RES_W,
    RES_H,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "nat_t", "type": "text"}],
)
d.txt(
    "nat_t",
    pub_x + SUBNET_PAD,
    RES_Y_START + RES_H + RES_GAP,
    RES_W,
    RES_H,
    "NAT Gateway",
    20,
    cid="nat",
)

# --- Private subnet ---
priv_x = pub_x + SUBNET_W + SUBNET_GAP
d.rect(
    "priv_sub", priv_x, SUBNET_Y, SUBNET_W, SUBNET_H, *RED, fill="hachure", dashed=True
)
d.txt(
    "priv_label",
    priv_x,
    SUBNET_Y + 8,
    SUBNET_W,
    math.ceil(1 * 20 * 1.25),
    "Private Subnet",
    20,
    color=RED[0],
)

d.rect(
    "ec2",
    priv_x + SUBNET_PAD,
    RES_Y_START,
    RES_W,
    RES_H,
    *RED,
    fill="hachure",
    bnd=[{"id": "ec2_t", "type": "text"}],
)
d.txt(
    "ec2_t",
    priv_x + SUBNET_PAD,
    RES_Y_START,
    RES_W,
    RES_H,
    "EC2 Instance",
    20,
    cid="ec2",
)

d.rect(
    "rds",
    priv_x + SUBNET_PAD,
    RES_Y_START + RES_H + RES_GAP,
    RES_W,
    RES_H,
    *RED,
    fill="hachure",
    bnd=[{"id": "rds_t", "type": "text"}],
)
d.txt(
    "rds_t",
    priv_x + SUBNET_PAD,
    RES_Y_START + RES_H + RES_GAP,
    RES_W,
    RES_H,
    "RDS Database",
    20,
    cid="rds",
)

# --- Internet Gateway + arrow ---
igw_x = (CANVAS_W - GW_W) // 2 - GW_W // 2 - GW_GAP // 2
nat_gw_x = (CANVAS_W - GW_W) // 2 + GW_W // 2 + GW_GAP // 2 - GW_W

# Center both gateways
total_gw_w = 2 * GW_W + GW_GAP
gw_start_x = (CANVAS_W - total_gw_w) // 2

d.rect(
    "igw",
    gw_start_x,
    GW_Y,
    GW_W,
    GW_H,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "igw_t", "type": "text"}],
)
d.txt("igw_t", gw_start_x, GW_Y, GW_W, GW_H, "Internet Gateway", 20, cid="igw")

d.rect(
    "rt",
    gw_start_x + GW_W + GW_GAP,
    GW_Y,
    GW_W,
    GW_H,
    *GRAY,
    fill="hachure",
    bnd=[{"id": "rt_t", "type": "text"}],
)
d.txt(
    "rt_t", gw_start_x + GW_W + GW_GAP, GW_Y, GW_W, GW_H, "Route Tables", 20, cid="rt"
)

# Arrows: IGW -> VPC, Route Tables -> VPC
d.arr(
    "a_igw_vpc",
    gw_start_x + GW_W // 2,
    GW_Y,
    [[0, 0], [0, -(GW_Y - VPC_Y - VPC_H)]],
    PURPLE[0],
    sb={"elementId": "igw", "focus": 0, "gap": 4},
    eb={"elementId": "vpc", "focus": 0, "gap": 4},
)

d.arr(
    "a_rt_vpc",
    gw_start_x + GW_W + GW_GAP + GW_W // 2,
    GW_Y,
    [[0, 0], [0, -(GW_Y - VPC_Y - VPC_H)]],
    GRAY[0],
    sb={"elementId": "rt", "focus": 0, "gap": 4},
    eb={"elementId": "vpc", "focus": 0, "gap": 4},
)

# --- Region considerations ---
d.txt(
    "consid_label",
    PAD_X,
    CONSID_Y,
    CONTENT_W,
    CONSID_LABEL_H,
    "Region Considerations",
    20,
    color=GRAY[0],
)

considerations = ["Compliance", "Latency", "Availability", "Cost"]
colors = [PURPLE, BLUE, GREEN, YELLOW]

for i, (label, color) in enumerate(zip(considerations, colors)):
    px = PILLS_X0 + i * (PILL_W + PILL_GAP)
    rid = f"pill_{i}"
    tid = f"pill_t_{i}"
    d.rect(
        rid,
        px,
        PILLS_Y,
        PILL_W,
        PILL_H,
        *color,
        fill="hachure",
        bnd=[{"id": tid, "type": "text"}],
    )
    d.txt(tid, px, PILLS_Y, PILL_W, PILL_H, label, 20, cid=rid)


# === VERIFY ===
print(f"Title: y={TITLE_Y}..{TITLE_Y + TITLE_H}")
print(f"Region: y={REGION_Y}..{REGION_Y + REGION_H}")
print(f"AZs: y={AZ_Y}..{AZ_Y + AZ_H}")
print(f"VPC: y={VPC_Y}..{VPC_Y + VPC_H}")
print(f"Subnets: y={SUBNET_Y}..{SUBNET_Y + SUBNET_H}")
print(f"Gateways: y={GW_Y}..{GW_Y + GW_H}")
print(f"Considerations: y={CONSID_Y}..{PILLS_Y + PILL_H}")
print(f"Canvas: {CANVAS_W} x {CANVAS_H}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/cloud-networking"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
