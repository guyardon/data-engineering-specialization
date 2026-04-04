"""
Terraform Infrastructure Workflow diagram for section 3.1.3.
Shows how Terraform defines infrastructure: HCL config → CLI workflow → cloud resources.
Vertical flow with grouped sections.
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
seed = 2000


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

CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X  # 600

# Vertical spacing
SECTION_GAP = 80  # gap between sections (for arrows)
BOX_H = 55
PILL_H = 42

# === BUILD DIAGRAM ===

# --- SECTION 1: HCL Configuration Files ---
Y = 20

# Section title
txt("sec1_title", 0, Y, CANVAS_W, 35, "1. Define Infrastructure", 28)
Y += 45

# Container box for config files
CONTAINER_H = 220
rect("cfg_container", PAD_X, Y, CONTENT_W, CONTAINER_H, PURPLE[0], PURPLE[1],
     opacity=40, dashed=True,
     bnd=[{"id": "a_cfg_to_tf", "type": "arrow"}])

# Container label
txt("cfg_label", PAD_X, Y + 8, CONTENT_W, 22, "HCL Configuration Files (.tf)", 20, color=PURPLE[0])

# Config file boxes inside container
INNER_PAD = 20
INNER_W = (CONTENT_W - 3 * INNER_PAD) // 2  # two columns
INNER_X1 = PAD_X + INNER_PAD
INNER_X2 = INNER_X1 + INNER_W + INNER_PAD
INNER_Y1 = Y + 40

files_col1 = [
    ("main.tf", "Resources &\nProviders"),
    ("variables.tf", "Input\nVariables"),
]
files_col2 = [
    ("outputs.tf", "Output\nValues"),
    ("terraform.tfvars", "Variable\nDefaults"),
]

for j, (fname, desc) in enumerate(files_col1):
    fy = INNER_Y1 + j * (BOX_H + 15)
    fid = f"f1_{j}"
    rect(fid, INNER_X1, fy, INNER_W, BOX_H, *PURPLE,
         bnd=[{"id": f"t_{fid}", "type": "text"}])
    txt(f"t_{fid}", INNER_X1, fy, INNER_W, BOX_H,
        f"{fname}\n{desc}", 18, cid=fid)

for j, (fname, desc) in enumerate(files_col2):
    fy = INNER_Y1 + j * (BOX_H + 15)
    fid = f"f2_{j}"
    rect(fid, INNER_X2, fy, INNER_W, BOX_H, *PURPLE,
         bnd=[{"id": f"t_{fid}", "type": "text"}])
    txt(f"t_{fid}", INNER_X2, fy, INNER_W, BOX_H,
        f"{fname}\n{desc}", 18, cid=fid)

Y += CONTAINER_H

# Arrow: config → terraform workflow
arr("a_cfg_to_tf", CANVAS_W // 2, Y,
    [[0, 0], [0, SECTION_GAP]],
    PURPLE[0],
    sb={"elementId": "cfg_container", "focus": 0, "gap": 4},
    eb={"elementId": "tf_container", "focus": 0, "gap": 4})

Y += SECTION_GAP

# --- SECTION 2: Terraform CLI Workflow ---
txt("sec2_title", 0, Y, CANVAS_W, 35, "2. Terraform CLI Workflow", 28)
Y += 45

# Workflow steps container
WORKFLOW_H = 230
rect("tf_container", PAD_X, Y, CONTENT_W, WORKFLOW_H, BLUE[0], BLUE[1],
     opacity=40, dashed=True,
     bnd=[{"id": "a_cfg_to_tf", "type": "arrow"},
          {"id": "a_tf_to_cloud", "type": "arrow"}])

txt("tf_label", PAD_X, Y + 8, CONTENT_W, 22, "Terraform Engine", 20, color=BLUE[0])

# Three workflow steps as horizontal flow
STEP_W = 155
STEP_H = 65
STEP_GAP = 40
TOTAL_STEPS_W = 3 * STEP_W + 2 * STEP_GAP
STEP_START_X = PAD_X + (CONTENT_W - TOTAL_STEPS_W) // 2
STEP_Y = Y + 50

steps = [
    ("s1", "terraform init", "Initialize\nworkspace", GREEN),
    ("s2", "terraform plan", "Preview\nchanges", YELLOW),
    ("s3", "terraform apply", "Execute\nchanges", CYAN),
]

for i, (sid, cmd, desc, color) in enumerate(steps):
    sx = STEP_START_X + i * (STEP_W + STEP_GAP)
    rect(sid, sx, STEP_Y, STEP_W, STEP_H, *color,
         bnd=[{"id": f"t_{sid}", "type": "text"}])
    txt(f"t_{sid}", sx, STEP_Y, STEP_W, STEP_H,
        cmd, 19, cid=sid)
    # Description below
    txt(f"d_{sid}", sx, STEP_Y + STEP_H + 5, STEP_W, 35,
        desc, 16, color=color[0])

# Arrows between steps
for i in range(2):
    sx = STEP_START_X + i * (STEP_W + STEP_GAP) + STEP_W
    arr(f"sa{i}", sx, STEP_Y + STEP_H // 2,
        [[0, 0], [STEP_GAP, 0]],
        steps[i][3][0],
        sb={"elementId": steps[i][0], "focus": 0, "gap": 4},
        eb={"elementId": steps[i + 1][0], "focus": 0, "gap": 4})

# Key property labels
PROP_Y = STEP_Y + STEP_H + 55
props = [
    ("Declarative", BLUE),
    ("Idempotent", BLUE),
    ("Version Controlled", BLUE),
]
PROP_W = 160
PROP_GAP = 30
TOTAL_PROPS_W = 3 * PROP_W + 2 * PROP_GAP
PROP_START_X = PAD_X + (CONTENT_W - TOTAL_PROPS_W) // 2

for i, (label, color) in enumerate(props):
    px = PROP_START_X + i * (PROP_W + PROP_GAP)
    pid = f"prop{i}"
    rect(pid, px, PROP_Y, PROP_W, 36, color[0], color[1],
         bnd=[{"id": f"t_{pid}", "type": "text"}])
    txt(f"t_{pid}", px, PROP_Y, PROP_W, 36,
        label, 17, cid=pid)

Y += WORKFLOW_H

# Arrow: terraform → cloud resources
arr("a_tf_to_cloud", CANVAS_W // 2, Y,
    [[0, 0], [0, SECTION_GAP]],
    BLUE[0],
    sb={"elementId": "tf_container", "focus": 0, "gap": 4},
    eb={"elementId": "cloud_container", "focus": 0, "gap": 4})

Y += SECTION_GAP

# --- SECTION 3: Cloud Resources Created ---
txt("sec3_title", 0, Y, CANVAS_W, 35, "3. Cloud Infrastructure", 28)
Y += 45

CLOUD_H = 130
rect("cloud_container", PAD_X, Y, CONTENT_W, CLOUD_H, GREEN[0], GREEN[1],
     opacity=40, dashed=True,
     bnd=[{"id": "a_tf_to_cloud", "type": "arrow"}])

txt("cloud_label", PAD_X, Y + 8, CONTENT_W, 22, "AWS Cloud Resources", 20, color=GREEN[0])

# Resource pills
RES_W = 120
RES_H = 42
RES_GAP = 20
resources = ["EC2", "VPC", "S3", "IAM"]
TOTAL_RES_W = len(resources) * RES_W + (len(resources) - 1) * RES_GAP
RES_START_X = PAD_X + (CONTENT_W - TOTAL_RES_W) // 2
RES_Y = Y + 50

for i, res in enumerate(resources):
    rx = RES_START_X + i * (RES_W + RES_GAP)
    rid = f"r{i}"
    rect(rid, rx, RES_Y, RES_W, RES_H, *GREEN,
         bnd=[{"id": f"t_{rid}", "type": "text"}])
    txt(f"t_{rid}", rx, RES_Y, RES_W, RES_H,
        res, 20, cid=rid)

Y += CLOUD_H

# === VERIFY ===
print(f"Canvas width: {CANVAS_W}")
print(f"Total height: ~{Y + 20}")
print(f"Config section: 20 to ~{20 + 45 + 220}")
print(f"Workflow section: ~{20 + 45 + 220 + SECTION_GAP} to ~{20 + 45 + 220 + SECTION_GAP + 45 + WORKFLOW_H}")
print(f"Cloud section ends: ~{Y}")

# === WRITE FILE ===

name = sys.argv[1] if len(sys.argv) > 1 else "terraform-workflow"
outfile = f"{name}.excalidraw"
with open(outfile, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {outfile}")
