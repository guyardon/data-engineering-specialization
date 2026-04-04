#!/usr/bin/env python3
"""Generate Architecting for Compliance excalidraw diagram."""

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
seed = 4000


def ns():
    global seed
    seed += 1
    return seed


def rect(
    id, x, y, w, h, stroke, bg, fill="solid", opacity=100, dashed=False, bnd=None, sw=2
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
            "strokeWidth": sw,
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


def txt_free(id, x, y, w, h, t, sz, color="#868e96"):
    """Free text element (not bound to any container)."""
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
            "containerId": None,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
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


def dual_text_positions(
    box_y, box_h, title_text, title_sz, subtitle_text, subtitle_sz, gap=6
):
    """Calculate y positions for title + subtitle within a box."""
    title_lines = title_text.count("\n") + 1
    subtitle_lines = subtitle_text.count("\n") + 1
    title_h = math.ceil(title_lines * title_sz * 1.25)
    subtitle_h = math.ceil(subtitle_lines * subtitle_sz * 1.25)
    combined = title_h + gap + subtitle_h
    title_y = box_y + (box_h - combined) // 2
    subtitle_y = title_y + title_h + gap
    return title_y, title_h, subtitle_y, subtitle_h


# ---------------------------------------------------------------------------
# Layout constants (fixed sizing/padding)
# ---------------------------------------------------------------------------
FONT_DIAGRAM_TITLE = 28
FONT_BOX_TITLE = 24
FONT_SUBTITLE = 15
FONT_CENTER = 24

# Canvas dimensions
CANVAS_W = 800
MARGIN_LEFT = 50

# Title
TITLE_Y = 20
TITLE_H = math.ceil(FONT_DIAGRAM_TITLE * 1.25)

# Center compliance box
CENTER_BOX_W = 280
CENTER_BOX_H = 85
CENTER_TOP = TITLE_Y + TITLE_H + 40
CENTER_X = MARGIN_LEFT + CANVAS_W // 2

# Regulation boxes (increased height from 110 to 120 for dual text)
REG_BOX_W = 220
REG_BOX_H = 120
REG_TOP = CENTER_TOP + CENTER_BOX_H + 80
REG_GAP = 35

# Total width of 3 regulation boxes + 2 gaps
REG_TOTAL_W = 3 * REG_BOX_W + 2 * REG_GAP
REG_START_X = CENTER_X - REG_TOTAL_W // 2

# Architecture box (increased height from 90 to 100 for dual text)
ARCH_TOP = REG_TOP + REG_BOX_H + 80
ARCH_W = 480
ARCH_H = 100

# ---------------------------------------------------------------------------
# Diagram title (free text)
# ---------------------------------------------------------------------------
title_text = "Architecting for Compliance"
title_w = math.ceil(len(title_text) * FONT_DIAGRAM_TITLE * 0.55 + 40)
txt(
    "title",
    CENTER_X - title_w // 2,
    TITLE_Y,
    title_w,
    TITLE_H,
    title_text,
    FONT_DIAGRAM_TITLE,
)

# ---------------------------------------------------------------------------
# Center: Regulatory Compliance box (red) — single bound text, no subtitle
# ---------------------------------------------------------------------------
comp_x = CENTER_X - CENTER_BOX_W // 2
comp_y = CENTER_TOP

rect(
    "compliance",
    comp_x,
    comp_y,
    CENTER_BOX_W,
    CENTER_BOX_H,
    "#c92a2a",
    "#ffc9c9",
    bnd=[
        {"id": "compliance-t", "type": "text"},
        {"id": "arr-comp-gdpr", "type": "arrow"},
        {"id": "arr-comp-hipaa", "type": "arrow"},
        {"id": "arr-comp-sox", "type": "arrow"},
    ],
)
txt(
    "compliance-t",
    comp_x,
    comp_y,
    CENTER_BOX_W,
    CENTER_BOX_H,
    "Regulatory\nCompliance",
    FONT_CENTER,
    cid="compliance",
)

# ---------------------------------------------------------------------------
# Regulation boxes: GDPR, HIPAA, SOX — dual text (title + subtitle)
# ---------------------------------------------------------------------------
regulations = [
    (
        "gdpr",
        "GDPR",
        "EU Data Protection\nConsent & Right\nto Delete",
        "#1971c2",
        "#a5d8ff",
    ),
    ("hipaa", "HIPAA", "Medical Data\nProtection", "#2f9e44", "#b2f2bb"),
    ("sox", "SOX", "Financial\nReporting", "#6741d9", "#d0bfff"),
]

for i, (rid, title, subtitle, stroke, bg) in enumerate(regulations):
    bx = REG_START_X + i * (REG_BOX_W + REG_GAP)
    by = REG_TOP
    tid = f"{rid}-t"
    sid = f"{rid}-sub"

    rect(
        rid,
        bx,
        by,
        REG_BOX_W,
        REG_BOX_H,
        stroke,
        bg,
        bnd=[
            {"id": tid, "type": "text"},
            {"id": f"arr-comp-{rid}", "type": "arrow"},
            {"id": f"arr-{rid}-arch", "type": "arrow"},
        ],
    )

    # Calculate dual text positions
    title_y, title_h, sub_y, sub_h = dual_text_positions(
        by, REG_BOX_H, title, FONT_BOX_TITLE, subtitle, FONT_SUBTITLE
    )

    # Bound title text
    txt(
        tid,
        bx,
        title_y,
        REG_BOX_W,
        title_h,
        title,
        FONT_BOX_TITLE,
        color="#1e1e1e",
        cid=rid,
    )

    # Free subtitle text (not bound to container)
    txt_free(sid, bx, sub_y, REG_BOX_W, sub_h, subtitle, FONT_SUBTITLE, color=stroke)

# ---------------------------------------------------------------------------
# Arrows: Compliance center -> each regulation box
# ---------------------------------------------------------------------------
comp_cx = comp_x + CENTER_BOX_W // 2
comp_bottom = comp_y + CENTER_BOX_H

for i, (rid, _, _, stroke, _) in enumerate(regulations):
    bx = REG_START_X + i * (REG_BOX_W + REG_GAP)
    reg_cx = bx + REG_BOX_W // 2
    reg_top = REG_TOP

    ax = comp_cx
    ay = comp_bottom
    dx = reg_cx - comp_cx
    dy = reg_top - comp_bottom

    arr(
        f"arr-comp-{rid}",
        ax,
        ay,
        [[0, 0], [dx, dy]],
        stroke,
        sb={"elementId": "compliance", "focus": 0, "gap": 5, "fixedPoint": None},
        eb={"elementId": rid, "focus": 0, "gap": 5, "fixedPoint": None},
    )

# ---------------------------------------------------------------------------
# Bottom: Loosely Coupled Architecture box (yellow/orange) — dual text
# ---------------------------------------------------------------------------
arch_x = CENTER_X - ARCH_W // 2
arch_y = ARCH_TOP

arch_title = "Loosely Coupled Architecture"
arch_subtitle = "Swap components to meet\nnew requirements"
FONT_ARCH_TITLE = 22
FONT_ARCH_SUB = 16

rect(
    "arch",
    arch_x,
    arch_y,
    ARCH_W,
    ARCH_H,
    "#e67700",
    "#ffec99",
    bnd=[
        {"id": "arch-t", "type": "text"},
        {"id": "arr-gdpr-arch", "type": "arrow"},
        {"id": "arr-hipaa-arch", "type": "arrow"},
        {"id": "arr-sox-arch", "type": "arrow"},
    ],
)

# Calculate dual text positions for architecture box
arch_ty, arch_th, arch_sy, arch_sh = dual_text_positions(
    arch_y, ARCH_H, arch_title, FONT_ARCH_TITLE, arch_subtitle, FONT_ARCH_SUB
)

# Bound title text
txt(
    "arch-t",
    arch_x,
    arch_ty,
    ARCH_W,
    arch_th,
    arch_title,
    FONT_ARCH_TITLE,
    color="#1e1e1e",
    cid="arch",
)

# Free subtitle text
txt_free(
    "arch-sub",
    arch_x,
    arch_sy,
    ARCH_W,
    arch_sh,
    arch_subtitle,
    FONT_ARCH_SUB,
    color="#e67700",
)

# ---------------------------------------------------------------------------
# Arrows: each regulation box -> architecture box (dashed)
# ---------------------------------------------------------------------------
arch_cx = arch_x + ARCH_W // 2
arch_top_y = arch_y

for i, (rid, _, _, stroke, _) in enumerate(regulations):
    bx = REG_START_X + i * (REG_BOX_W + REG_GAP)
    reg_cx = bx + REG_BOX_W // 2
    reg_bottom = REG_TOP + REG_BOX_H

    ax = reg_cx
    ay = reg_bottom
    dx = arch_cx - reg_cx
    dy = arch_top_y - reg_bottom

    arr(
        f"arr-{rid}-arch",
        ax,
        ay,
        [[0, 0], [dx, dy]],
        stroke,
        dash=True,
        sb={"elementId": rid, "focus": 0, "gap": 5, "fixedPoint": None},
        eb={"elementId": "arch", "focus": 0, "gap": 5, "fixedPoint": None},
    )

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
out_path = os.path.join(out_dir, "compliance-framework.excalidraw")
os.makedirs(out_dir, exist_ok=True)

with open(out_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Done! Wrote {os.path.abspath(out_path)}")
