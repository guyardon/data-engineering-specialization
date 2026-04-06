"""Generate CDC Implementation Patterns diagram for Course 2, Section 2.4.2."""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, GRAY

d = ExcalidrawDiagram(seed=4000)

# === LAYOUT CONSTANTS ===
# Three columns: Query-based | Log-based | Trigger-based
# Each: Source → Mechanism → Target, with type label and description

CANVAS_W = 650
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 610
COL_GAP = 25
COL_W = (CONTENT_W - 2 * COL_GAP) // 3  # 186

COL1_X = PAD_X
COL2_X = PAD_X + COL_W + COL_GAP
COL3_X = PAD_X + 2 * (COL_W + COL_GAP)

# Box sizing
BOX_W = 170
BOX_H = 65
MECH_H = 80  # mechanism box (taller for description)
DESC_H = 100

# Title + subtitle
HDR_FSZ = 20
SUB_FSZ = 15
title_h = math.ceil(1 * HDR_FSZ * 1.25)
sub_h = math.ceil(1 * SUB_FSZ * 1.25)
gap_ts = 4

# Vertical positions
TITLE_Y = 10
TITLE_FSZ = 32
TITLE_H = math.ceil(1 * TITLE_FSZ * 1.25)

COL_HDR_Y = TITLE_Y + TITLE_H + 25
COL_HDR_H = math.ceil(1 * 24 * 1.25)

TYPE_Y = COL_HDR_Y + COL_HDR_H + 8
TYPE_H = math.ceil(1 * 17 * 1.25)

SRC_Y = TYPE_Y + TYPE_H + 20
ARR_GAP = 75
MECH_Y = SRC_Y + BOX_H + ARR_GAP
TGT_Y = MECH_Y + MECH_H + ARR_GAP
DESC_Y = TGT_Y + BOX_H + 20

BOX_OFF = (COL_W - BOX_W) // 2


def build_column(
    prefix,
    col_x,
    title,
    type_label,
    type_color,
    src_label,
    mech_title,
    mech_sub,
    tgt_label,
    desc_text,
    color,
):
    """Build one CDC pattern column."""
    stroke, bg = color

    # Column header
    d.txt(f"{prefix}-hdr", col_x, COL_HDR_Y, COL_W, COL_HDR_H, title, 22, color=stroke)

    # Type label (pull/push)
    d.txt(
        f"{prefix}-type", col_x, TYPE_Y, COL_W, TYPE_H, type_label, 15, color=type_color
    )

    # Source DB
    d.rect(
        f"{prefix}-src",
        col_x + BOX_OFF,
        SRC_Y,
        BOX_W,
        BOX_H,
        *GRAY,
        bnd=[{"id": f"{prefix}-src-t", "type": "text"}],
    )
    d.txt(
        f"{prefix}-src-t",
        col_x + BOX_OFF,
        SRC_Y,
        BOX_W,
        BOX_H,
        src_label,
        17,
        cid=f"{prefix}-src",
    )

    # Arrow: Source → Mechanism
    d.arr(
        f"{prefix}-a1",
        col_x + BOX_OFF + BOX_W // 2,
        SRC_Y + BOX_H,
        [[0, 0], [0, ARR_GAP]],
        stroke,
        sb={"elementId": f"{prefix}-src", "focus": 0, "gap": 4},
        eb={"elementId": f"{prefix}-mech", "focus": 0, "gap": 4},
    )

    # Mechanism box
    d.rect(
        f"{prefix}-mech",
        col_x + BOX_OFF,
        MECH_Y,
        BOX_W,
        MECH_H,
        stroke,
        bg,
        bnd=[{"id": f"{prefix}-mech-t", "type": "text"}],
    )
    # Title + subtitle in mechanism box
    mech_title_h = math.ceil(1 * HDR_FSZ * 1.25)
    mech_sub_h = math.ceil(1 * SUB_FSZ * 1.25)
    mech_combined = mech_title_h + gap_ts + mech_sub_h
    mech_top = (MECH_H - mech_combined) // 2
    d.txt(
        f"{prefix}-mech-t",
        col_x + BOX_OFF,
        MECH_Y + mech_top,
        BOX_W,
        mech_title_h,
        mech_title,
        HDR_FSZ,
        cid=f"{prefix}-mech",
    )
    d.txt(
        f"{prefix}-mech-sub",
        col_x + BOX_OFF,
        MECH_Y + mech_top + mech_title_h + gap_ts,
        BOX_W,
        mech_sub_h,
        mech_sub,
        SUB_FSZ,
        color=stroke,
    )

    # Arrow: Mechanism → Target
    d.arr(
        f"{prefix}-a2",
        col_x + BOX_OFF + BOX_W // 2,
        MECH_Y + MECH_H,
        [[0, 0], [0, ARR_GAP]],
        stroke,
        sb={"elementId": f"{prefix}-mech", "focus": 0, "gap": 4},
        eb={"elementId": f"{prefix}-tgt", "focus": 0, "gap": 4},
    )

    # Target
    d.rect(
        f"{prefix}-tgt",
        col_x + BOX_OFF,
        TGT_Y,
        BOX_W,
        BOX_H,
        stroke,
        bg,
        bnd=[{"id": f"{prefix}-tgt-t", "type": "text"}],
    )
    d.txt(
        f"{prefix}-tgt-t",
        col_x + BOX_OFF,
        TGT_Y,
        BOX_W,
        BOX_H,
        tgt_label,
        17,
        cid=f"{prefix}-tgt",
    )

    # Description
    d.rect(
        f"{prefix}-desc",
        col_x + 5,
        DESC_Y,
        COL_W - 10,
        DESC_H,
        stroke,
        bg,
        opacity=40,
        dashed=True,
    )
    d.txt(
        f"{prefix}-desc-t",
        col_x + 5,
        DESC_Y,
        COL_W - 10,
        DESC_H,
        desc_text,
        15,
        cid=f"{prefix}-desc",
    )


# === BUILD DIAGRAM ===

# Main title
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "CDC Implementation Patterns",
    TITLE_FSZ,
)

# Column 1: Query-based (Pull)
build_column(
    "qry",
    COL1_X,
    title="Query-Based",
    type_label="Pull-based (batch)",
    type_color=BLUE[0],
    src_label="Source Database",
    mech_title="SQL Query",
    mech_sub="last_modified column",
    tgt_label="Target Table",
    desc_text="Simple to implement\nCan miss deletes\nScanning overhead",
    color=BLUE,
)

# Column 2: Log-based (Pull)
build_column(
    "log",
    COL2_X,
    title="Log-Based",
    type_label="Pull-based (continuous)",
    type_color=GREEN[0],
    src_label="Transaction Log",
    mech_title="Log Reader",
    mech_sub="Debezium / Kafka Connect",
    tgt_label="Streaming Platform",
    desc_text="Real-time capture\nNo source overhead\nCaptures all changes",
    color=GREEN,
)

# Column 3: Trigger-based (Push)
build_column(
    "trg",
    COL3_X,
    title="Trigger-Based",
    type_label="Push-based",
    type_color=PURPLE[0],
    src_label="Source Database",
    mech_title="DB Trigger",
    mech_sub="Stored procedure fires",
    tgt_label="CDC System",
    desc_text="Immediate capture\nAdds write overhead\nComplex to maintain",
    color=PURPLE,
)

# === VERIFY ===
print(f"Canvas: {CANVAS_W}w")
print(f"Columns: x1={COL1_X}, x2={COL2_X}, x3={COL3_X}, w={COL_W}")
print(f"Rows: src={SRC_Y}, mech={MECH_Y}, tgt={TGT_Y}, desc={DESC_Y}")
print(f"Bottom: {DESC_Y + DESC_H}")

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/cdc-patterns"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
