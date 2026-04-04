"""
Excalidraw diagram: AWS IAM & Permissions overview for section 1.2.3.

Shows cloud security pillars at top, IAM hierarchy in center,
and a role assumption example at bottom.
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

CANVAS_W = 900
PAD_X = 30
CONTENT_W = CANVAS_W - 2 * PAD_X  # 840

# Pillar boxes
PILLAR_W = 250
PILLAR_H = 65
PILLAR_GAP = 22
PILLARS_TOTAL_W = 3 * PILLAR_W + 2 * PILLAR_GAP
PILLARS_X0 = (CANVAS_W - PILLARS_TOTAL_W) // 2

# Title
TITLE_Y = 20
TITLE_H = math.ceil(1 * 32 * 1.25)

# Subtitle for pillars
PILLARS_LABEL_Y = TITLE_Y + TITLE_H + 25
PILLARS_LABEL_H = math.ceil(1 * 20 * 1.25)

PILLARS_Y = PILLARS_LABEL_Y + PILLARS_LABEL_H + 12

# IAM hierarchy section
HIER_LABEL_Y = PILLARS_Y + PILLAR_H + 40
HIER_LABEL_H = math.ceil(1 * 20 * 1.25)

# Hierarchy boxes - vertical stack
BOX_W = 340
BOX_H = 70
BOX_GAP = 75  # gap between boxes (arrow space)
HIER_X = (CANVAS_W - BOX_W) // 2

ROOT_Y = HIER_LABEL_Y + HIER_LABEL_H + 15
USER_Y = ROOT_Y + BOX_H + BOX_GAP
GROUP_Y = USER_Y + BOX_H + BOX_GAP
ROLE_Y = GROUP_Y + BOX_H + BOX_GAP

# Role example section
EXAMPLE_Y = ROLE_Y + BOX_H + 50
EXAMPLE_LABEL_H = math.ceil(1 * 20 * 1.25)

# Example boxes - EC2 -> Role -> S3
EX_BOX_W = 180
EX_BOX_H = 65
EX_GAP = 100
EX_TOTAL_W = 3 * EX_BOX_W + 2 * EX_GAP
EX_X0 = (CANVAS_W - EX_TOTAL_W) // 2
EX_Y = EXAMPLE_Y + EXAMPLE_LABEL_H + 15

# Principle of least privilege label
PRINCIPLE_Y = EX_Y + EX_BOX_H + 35
PRINCIPLE_H = math.ceil(1 * 19 * 1.25)

# === BUILD DIAGRAM ===

# --- Title ---
txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "AWS IAM & Permissions", 32)

# --- Three Pillars of Cloud Security ---
txt("pillars_label", PAD_X, PILLARS_LABEL_Y, CONTENT_W, PILLARS_LABEL_H,
    "Three Pillars of Cloud Security", 20, color=GRAY[0])

p1_x = PILLARS_X0
p2_x = PILLARS_X0 + PILLAR_W + PILLAR_GAP
p3_x = PILLARS_X0 + 2 * (PILLAR_W + PILLAR_GAP)

rect("p1", p1_x, PILLARS_Y, PILLAR_W, PILLAR_H, *CYAN,
     bnd=[{"id": "p1t", "type": "text"}])
txt("p1t", p1_x, PILLARS_Y, PILLAR_W, PILLAR_H,
    "Encryption", 22, cid="p1")

rect("p2", p2_x, PILLARS_Y, PILLAR_W, PILLAR_H, *PURPLE,
     bnd=[{"id": "p2t", "type": "text"}])
txt("p2t", p2_x, PILLARS_Y, PILLAR_W, PILLAR_H,
    "IAM", 22, cid="p2")

rect("p3", p3_x, PILLARS_Y, PILLAR_W, PILLAR_H, *GREEN,
     bnd=[{"id": "p3t", "type": "text"}])
txt("p3t", p3_x, PILLARS_Y, PILLAR_W, PILLAR_H,
    "Networking", 22, cid="p3")

# --- IAM Hierarchy label ---
txt("hier_label", PAD_X, HIER_LABEL_Y, CONTENT_W, HIER_LABEL_H,
    "IAM Identity Hierarchy", 20, color=GRAY[0])

# --- Root User ---
rect("root", HIER_X, ROOT_Y, BOX_W, BOX_H, *RED,
     bnd=[{"id": "root_t", "type": "text"}])
txt("root_t", HIER_X, ROOT_Y, BOX_W, BOX_H,
    "Root User\nUnrestricted access", 22, cid="root")

# --- IAM User ---
rect("user", HIER_X, USER_Y, BOX_W, BOX_H, *BLUE,
     bnd=[{"id": "user_t", "type": "text"}])
txt("user_t", HIER_X, USER_Y, BOX_W, BOX_H,
    "IAM User\nSpecific permissions", 22, cid="user")

# --- IAM Group ---
rect("group", HIER_X, GROUP_Y, BOX_W, BOX_H, *GREEN,
     bnd=[{"id": "group_t", "type": "text"}])
txt("group_t", HIER_X, GROUP_Y, BOX_W, BOX_H,
    "IAM Group\nInherited permissions", 22, cid="group")

# --- IAM Role ---
rect("role", HIER_X, ROLE_Y, BOX_W, BOX_H, *YELLOW,
     bnd=[{"id": "role_t", "type": "text"}])
txt("role_t", HIER_X, ROLE_Y, BOX_W, BOX_H,
    "IAM Role\nTemporary permissions", 22, cid="role")

# --- Arrows between hierarchy boxes ---
arrow_x = HIER_X + BOX_W // 2

arr("a_root_user", arrow_x, ROOT_Y + BOX_H, [[0, 0], [0, BOX_GAP]],
    RED[0],
    sb={"elementId": "root", "focus": 0, "gap": 4},
    eb={"elementId": "user", "focus": 0, "gap": 4})

arr("a_user_group", arrow_x, USER_Y + BOX_H, [[0, 0], [0, BOX_GAP]],
    BLUE[0],
    sb={"elementId": "user", "focus": 0, "gap": 4},
    eb={"elementId": "group", "focus": 0, "gap": 4})

arr("a_group_role", arrow_x, GROUP_Y + BOX_H, [[0, 0], [0, BOX_GAP]],
    GREEN[0],
    sb={"elementId": "group", "focus": 0, "gap": 4},
    eb={"elementId": "role", "focus": 0, "gap": 4})

# --- Role Example label ---
txt("ex_label", PAD_X, EXAMPLE_Y, CONTENT_W, EXAMPLE_LABEL_H,
    "Role Assumption Example", 20, color=GRAY[0])

# EC2
ex1_x = EX_X0
rect("ec2", ex1_x, EX_Y, EX_BOX_W, EX_BOX_H, *BLUE,
     bnd=[{"id": "ec2_t", "type": "text"}])
txt("ec2_t", ex1_x, EX_Y, EX_BOX_W, EX_BOX_H,
    "EC2 Instance", 22, cid="ec2")

# IAM Role (in example)
ex2_x = EX_X0 + EX_BOX_W + EX_GAP
rect("ex_role", ex2_x, EX_Y, EX_BOX_W, EX_BOX_H, *YELLOW,
     bnd=[{"id": "ex_role_t", "type": "text"}])
txt("ex_role_t", ex2_x, EX_Y, EX_BOX_W, EX_BOX_H,
    "IAM Role\nS3 Read Policy", 20, cid="ex_role")

# S3
ex3_x = EX_X0 + 2 * (EX_BOX_W + EX_GAP)
rect("s3", ex3_x, EX_Y, EX_BOX_W, EX_BOX_H, *GREEN,
     bnd=[{"id": "s3_t", "type": "text"}])
txt("s3_t", ex3_x, EX_Y, EX_BOX_W, EX_BOX_H,
    "S3 Bucket", 22, cid="s3")

# Arrows for example
ex_arrow_y = EX_Y + EX_BOX_H // 2

arr("a_ec2_role", ex1_x + EX_BOX_W, ex_arrow_y,
    [[0, 0], [EX_GAP, 0]], BLUE[0],
    sb={"elementId": "ec2", "focus": 0, "gap": 4},
    eb={"elementId": "ex_role", "focus": 0, "gap": 4})

arr("a_role_s3", ex2_x + EX_BOX_W, ex_arrow_y,
    [[0, 0], [EX_GAP, 0]], YELLOW[0],
    sb={"elementId": "ex_role", "focus": 0, "gap": 4},
    eb={"elementId": "s3", "focus": 0, "gap": 4})

# Labels on example arrows
arr_label_h = math.ceil(1 * 17 * 1.25)
txt("assume_label", ex1_x + EX_BOX_W, EX_Y - 22,
    EX_GAP, arr_label_h, "assumes", 17, color=BLUE[0])

txt("grants_label", ex2_x + EX_BOX_W, EX_Y - 22,
    EX_GAP, arr_label_h, "grants access", 17, color=YELLOW[0])

# --- Principle of least privilege ---
txt("principle", PAD_X, PRINCIPLE_Y, CONTENT_W, PRINCIPLE_H,
    "Principle of Least Privilege — every identity gets only the permissions it needs", 19, color=GRAY[0])


# === VERIFY ===
print(f"Title: y={TITLE_Y}..{TITLE_Y + TITLE_H}")
print(f"Pillars label: y={PILLARS_LABEL_Y}..{PILLARS_LABEL_Y + PILLARS_LABEL_H}")
print(f"Pillars: y={PILLARS_Y}..{PILLARS_Y + PILLAR_H}")
print(f"Hier label: y={HIER_LABEL_Y}..{HIER_LABEL_Y + HIER_LABEL_H}")
print(f"Root: y={ROOT_Y}..{ROOT_Y + BOX_H}")
print(f"User: y={USER_Y}..{USER_Y + BOX_H}")
print(f"Group: y={GROUP_Y}..{GROUP_Y + BOX_H}")
print(f"Role: y={ROLE_Y}..{ROLE_Y + BOX_H}")
print(f"Example label: y={EXAMPLE_Y}..{EXAMPLE_Y + EXAMPLE_LABEL_H}")
print(f"Example boxes: y={EX_Y}..{EX_Y + EX_BOX_H}")
print(f"Principle: y={PRINCIPLE_Y}..{PRINCIPLE_Y + PRINCIPLE_H}")
print(f"Canvas: {CANVAS_W} x {PRINCIPLE_Y + PRINCIPLE_H + 20}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "iam-permissions"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
