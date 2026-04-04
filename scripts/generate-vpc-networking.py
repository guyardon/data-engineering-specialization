"""
Excalidraw diagram: AWS VPC Networking for section 1.2.5.

Layout: User + IGW at top, VPC below with ALB,
two AZs side by side, each with public + private subnet stacked vertically.
Public and private subnets are the same height.
"""

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


def rect(id, x, y, w, h, stroke, bg, fill="hachure", opacity=100, dashed=False, bnd=None):
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


def txt(id, x, y, w, h, t, sz, color="#1e1e1e", cid=None, op=100):
    if cid:
        num_lines = t.count("\n") + 1
        actual_h = math.ceil(num_lines * sz * 1.25)
        y = y + (h - actual_h) // 2
        h = actual_h
    els.append({
        "type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "text": t, "originalText": t, "fontSize": sz, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "middle", "lineHeight": 1.25,
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

CANVAS_W = 1000
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 940

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Top row: User -> IGW
TOP_BOX_W = 160
TOP_BOX_H = 65
TOP_Y = TITLE_Y + TITLE_H + 30
TOP_GAP = 100
# Center user + igw
TOP_TOTAL = 2 * TOP_BOX_W + TOP_GAP
TOP_X0 = (CANVAS_W - TOP_TOTAL) // 2

# VPC container
VPC_PAD = 25
VPC_Y = TOP_Y + TOP_BOX_H + 80
VPC_X = PAD_X

# ALB inside VPC top
ALB_W = 160
ALB_H = 60
ALB_Y = VPC_Y + 50
ALB_X = (CANVAS_W - ALB_W) // 2

# AZ containers side by side
AZ_PAD = 20
AZ_GAP = 40
AZ_Y = ALB_Y + ALB_H + 80
AZ_INNER_W = (CONTENT_W - 2 * VPC_PAD - AZ_GAP) // 2

# Subnet boxes inside each AZ (stacked vertically)
SUBNET_PAD = 15
SUBNET_GAP = 25
SUBNET_W = AZ_INNER_W - 2 * AZ_PAD

# Resource pills inside subnets
PILL_W = (SUBNET_W - 2 * SUBNET_PAD - 20) // 2
PILL_H = 55
PILL_PAD = SUBNET_PAD

# Subnet height — same for both public and private
# Private has 2 pills side by side, public has 1 pill centered
# Use the same height: label + padding + pill + padding
SUBNET_LABEL_H = math.ceil(1 * 20 * 1.25)
SUBNET_H = SUBNET_LABEL_H + 15 + PILL_H + SUBNET_PAD + 10

# AZ height
AZ_LABEL_H = math.ceil(1 * 22 * 1.25)
AZ_H = AZ_LABEL_H + 15 + 2 * SUBNET_H + SUBNET_GAP + AZ_PAD

# VPC dimensions
VPC_LABEL_H = math.ceil(1 * 24 * 1.25)
VPC_W = CONTENT_W
VPC_H = (AZ_Y - VPC_Y) + AZ_H + VPC_PAD

# Security groups section
SG_Y = VPC_Y + VPC_H + 35
SG_LABEL_H = math.ceil(1 * 20 * 1.25)
SG_PILL_W = 200
SG_PILL_H = 50
SG_PILL_GAP = 25
SG_TOTAL = 3 * SG_PILL_W + 2 * SG_PILL_GAP
SG_X0 = (CANVAS_W - SG_TOTAL) // 2
SG_PILL_Y = SG_Y + SG_LABEL_H + 12

CANVAS_H = SG_PILL_Y + SG_PILL_H + 30

# === BUILD DIAGRAM ===

# --- Title ---
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "AWS VPC Networking", 32)

# --- User ---
user_x = TOP_X0
rect("user", user_x, TOP_Y, TOP_BOX_W, TOP_BOX_H, *GRAY,
     bnd=[{"id": "user_t", "type": "text"}])
txt("user_t", user_x, TOP_Y, TOP_BOX_W, TOP_BOX_H,
    "User", 22, cid="user")

# --- Internet Gateway ---
igw_x = TOP_X0 + TOP_BOX_W + TOP_GAP
rect("igw", igw_x, TOP_Y, TOP_BOX_W, TOP_BOX_H, *PURPLE,
     bnd=[{"id": "igw_t", "type": "text"}])
txt("igw_t", igw_x, TOP_Y, TOP_BOX_W, TOP_BOX_H,
    "Internet\nGateway", 22, cid="igw")

# Arrow: User -> IGW
arr("a_user_igw", user_x + TOP_BOX_W, TOP_Y + TOP_BOX_H // 2,
    [[0, 0], [TOP_GAP, 0]], GRAY[0],
    sb={"elementId": "user", "focus": 0, "gap": 4},
    eb={"elementId": "igw", "focus": 0, "gap": 4})

# --- VPC container ---
rect("vpc", VPC_X, VPC_Y, VPC_W, VPC_H, *PURPLE, dashed=True,
     bnd=[{"id": "vpc_t", "type": "text"}])
txt("vpc_t", VPC_X, VPC_Y, VPC_W, VPC_LABEL_H + VPC_PAD,
    "VPC (10.0.0.0/16)", 24, color=PURPLE[0], cid="vpc")

# Arrow: IGW -> VPC
arr("a_igw_vpc", igw_x + TOP_BOX_W // 2, TOP_Y + TOP_BOX_H,
    [[0, 0], [0, VPC_Y - TOP_Y - TOP_BOX_H]], PURPLE[0],
    sb={"elementId": "igw", "focus": 0, "gap": 4},
    eb={"elementId": "vpc", "focus": 0, "gap": 4})

# --- ALB ---
rect("alb", ALB_X, ALB_Y, ALB_W, ALB_H, *PURPLE,
     bnd=[{"id": "alb_t", "type": "text"}])
txt("alb_t", ALB_X, ALB_Y, ALB_W, ALB_H,
    "ALB", 22, cid="alb")

# --- AZ 1 (left) ---
az1_x = VPC_X + VPC_PAD
rect("az1", az1_x, AZ_Y, AZ_INNER_W, AZ_H, *GREEN, dashed=True)
txt("az1_label", az1_x, AZ_Y + 8, AZ_INNER_W, AZ_LABEL_H,
    "Availability Zone 1", 22, color=GREEN[0])

# Public subnet 1
pub1_x = az1_x + AZ_PAD
pub1_y = AZ_Y + AZ_LABEL_H + 15
rect("pub1", pub1_x, pub1_y, SUBNET_W, SUBNET_H, *YELLOW, dashed=True)
txt("pub1_label", pub1_x, pub1_y + 5, SUBNET_W, SUBNET_LABEL_H,
    "Public Subnet  10.0.1.0/24", 20, color=YELLOW[0])

# NAT Gateway centered in public subnet
nat1_x = pub1_x + (SUBNET_W - PILL_W) // 2
nat1_y = pub1_y + SUBNET_LABEL_H + 15
rect("nat1", nat1_x, nat1_y, PILL_W, PILL_H, *YELLOW,
     bnd=[{"id": "nat1_t", "type": "text"}])
txt("nat1_t", nat1_x, nat1_y, PILL_W, PILL_H,
    "NAT Gateway", 19, cid="nat1")

# Private subnet 1
priv1_y = pub1_y + SUBNET_H + SUBNET_GAP
rect("priv1", pub1_x, priv1_y, SUBNET_W, SUBNET_H, *RED, dashed=True)
txt("priv1_label", pub1_x, priv1_y + 5, SUBNET_W, SUBNET_LABEL_H,
    "Private Subnet  10.0.2.0/24", 20, color=RED[0])

# EC2 + RDS side by side
ec2_1_x = pub1_x + PILL_PAD
ec2_1_y = priv1_y + SUBNET_LABEL_H + 15
rect("ec2_1", ec2_1_x, ec2_1_y, PILL_W, PILL_H, *BLUE,
     bnd=[{"id": "ec2_1_t", "type": "text"}])
txt("ec2_1_t", ec2_1_x, ec2_1_y, PILL_W, PILL_H,
    "EC2", 20, cid="ec2_1")

rds_1_x = pub1_x + SUBNET_W - PILL_PAD - PILL_W
rect("rds_1", rds_1_x, ec2_1_y, PILL_W, PILL_H, *CYAN,
     bnd=[{"id": "rds_1_t", "type": "text"}])
txt("rds_1_t", rds_1_x, ec2_1_y, PILL_W, PILL_H,
    "RDS", 20, cid="rds_1")

# --- AZ 2 (right) ---
az2_x = az1_x + AZ_INNER_W + AZ_GAP
rect("az2", az2_x, AZ_Y, AZ_INNER_W, AZ_H, *GREEN, dashed=True)
txt("az2_label", az2_x, AZ_Y + 8, AZ_INNER_W, AZ_LABEL_H,
    "Availability Zone 2", 22, color=GREEN[0])

# Public subnet 2
pub2_x = az2_x + AZ_PAD
rect("pub2", pub2_x, pub1_y, SUBNET_W, SUBNET_H, *YELLOW, dashed=True)
txt("pub2_label", pub2_x, pub1_y + 5, SUBNET_W, SUBNET_LABEL_H,
    "Public Subnet  10.0.3.0/24", 20, color=YELLOW[0])

nat2_x = pub2_x + (SUBNET_W - PILL_W) // 2
rect("nat2", nat2_x, nat1_y, PILL_W, PILL_H, *YELLOW,
     bnd=[{"id": "nat2_t", "type": "text"}])
txt("nat2_t", nat2_x, nat1_y, PILL_W, PILL_H,
    "NAT Gateway", 19, cid="nat2")

# Private subnet 2
rect("priv2", pub2_x, priv1_y, SUBNET_W, SUBNET_H, *RED, dashed=True)
txt("priv2_label", pub2_x, priv1_y + 5, SUBNET_W, SUBNET_LABEL_H,
    "Private Subnet  10.0.4.0/24", 20, color=RED[0])

ec2_2_x = pub2_x + PILL_PAD
rect("ec2_2", ec2_2_x, ec2_1_y, PILL_W, PILL_H, *BLUE,
     bnd=[{"id": "ec2_2_t", "type": "text"}])
txt("ec2_2_t", ec2_2_x, ec2_1_y, PILL_W, PILL_H,
    "EC2", 20, cid="ec2_2")

rds_2_x = pub2_x + SUBNET_W - PILL_PAD - PILL_W
rect("rds_2", rds_2_x, ec2_1_y, PILL_W, PILL_H, *CYAN,
     bnd=[{"id": "rds_2_t", "type": "text"}])
txt("rds_2_t", rds_2_x, ec2_1_y, PILL_W, PILL_H,
    "RDS", 20, cid="rds_2")

# --- Arrows: ALB -> EC2s ---
arr("a_alb_ec2_1", ALB_X + ALB_W // 4, ALB_Y + ALB_H,
    [[0, 0], [0, ec2_1_y - ALB_Y - ALB_H + PILL_H // 2],
     [ec2_1_x + PILL_W // 2 - ALB_X - ALB_W // 4, ec2_1_y - ALB_Y - ALB_H + PILL_H // 2]],
    PURPLE[0])

arr("a_alb_ec2_2", ALB_X + 3 * ALB_W // 4, ALB_Y + ALB_H,
    [[0, 0], [0, ec2_1_y - ALB_Y - ALB_H + PILL_H // 2],
     [ec2_2_x + PILL_W // 2 - ALB_X - 3 * ALB_W // 4, ec2_1_y - ALB_Y - ALB_H + PILL_H // 2]],
    PURPLE[0])

# --- Arrows: EC2 -> RDS ---
arr("a_ec2_rds_1", ec2_1_x + PILL_W, ec2_1_y + PILL_H // 2,
    [[0, 0], [rds_1_x - ec2_1_x - PILL_W, 0]], BLUE[0],
    sb={"elementId": "ec2_1", "focus": 0, "gap": 4},
    eb={"elementId": "rds_1", "focus": 0, "gap": 4})

arr("a_ec2_rds_2", ec2_2_x + PILL_W, ec2_1_y + PILL_H // 2,
    [[0, 0], [rds_2_x - ec2_2_x - PILL_W, 0]], BLUE[0],
    sb={"elementId": "ec2_2", "focus": 0, "gap": 4},
    eb={"elementId": "rds_2", "focus": 0, "gap": 4})

# --- Arrows: EC2 -> NAT (upward) ---
arr("a_ec2_nat_1", ec2_1_x + PILL_W // 2, ec2_1_y,
    [[0, 0], [0, -(ec2_1_y - nat1_y - PILL_H)]],
    RED[0])

arr("a_ec2_nat_2", ec2_2_x + PILL_W // 2, ec2_1_y,
    [[0, 0], [0, -(ec2_1_y - nat1_y - PILL_H)]],
    RED[0])

# --- Security layer labels ---
txt("sg_label", PAD_X, SG_Y, CONTENT_W, SG_LABEL_H,
    "Security Layers", 20, color=GRAY[0])

sg_items = [("Security\nGroups", BLUE), ("Network\nACLs", GREEN), ("Route\nTables", YELLOW)]
for i, (label, color) in enumerate(sg_items):
    sx = SG_X0 + i * (SG_PILL_W + SG_PILL_GAP)
    rid = f"sg_{i}"
    tid = f"sg_t_{i}"
    rect(rid, sx, SG_PILL_Y, SG_PILL_W, SG_PILL_H, *color,
         bnd=[{"id": tid, "type": "text"}])
    txt(tid, sx, SG_PILL_Y, SG_PILL_W, SG_PILL_H, label, 19, cid=rid)


# === VERIFY ===
print(f"Title: y={TITLE_Y}..{TITLE_Y + TITLE_H}")
print(f"Top row: y={TOP_Y}..{TOP_Y + TOP_BOX_H}")
print(f"VPC: y={VPC_Y}..{VPC_Y + VPC_H}")
print(f"ALB: y={ALB_Y}..{ALB_Y + ALB_H}")
print(f"AZs: y={AZ_Y}..{AZ_Y + AZ_H}")
print(f"Public subnets: y={pub1_y}..{pub1_y + SUBNET_H}")
print(f"Private subnets: y={priv1_y}..{priv1_y + SUBNET_H}")
print(f"Security: y={SG_Y}..{SG_PILL_Y + SG_PILL_H}")
print(f"Canvas: {CANVAS_W} x {CANVAS_H}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "vpc-networking"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
