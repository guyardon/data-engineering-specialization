"""
DAG dependency patterns diagram.
Shows 4 common dependency patterns side by side in a 2x2 grid:
  1. Linear chain
  2. Fan-out (parallel)
  3. Fan-in (converge)
  4. Complex (chain utility)

Canvas: ~680px wide, vertical layout with labeled sections.
"""

import sys

from diagramlib import BLUE, GRAY, GREEN, PURPLE, YELLOW, ExcalidrawDiagram

d = ExcalidrawDiagram(seed=2000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 680
PAD_X = 20
BW = 90  # small task box
BH = 45
ARROW_GAP = 50  # horizontal gap between boxes
COL_W = CANVAS_W // 2 - PAD_X  # each pattern column width
COL1_X = PAD_X
COL2_X = CANVAS_W // 2 + 10

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CANVAS_W - 2 * PAD_X, 40, "DAG Dependency Patterns", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CANVAS_W - 2 * PAD_X,
    25,
    "Common ways to wire task dependencies in Airflow",
    17,
    color=BLUE[0],
)

# === PATTERN 1: Linear Chain (top-left) ===
P1_Y = 100
d.txt("p1_title", COL1_X, P1_Y, COL_W, 25, "Linear Chain", 22, color=BLUE[0])
# Code label
d.txt(
    "p1_code",
    COL1_X,
    P1_Y + 28,
    COL_W,
    20,
    "task1 >> task2 >> task3",
    14,
    color=GRAY[0],
)

# Three boxes in a row
P1_BOX_Y = P1_Y + 60
P1_B1_X = COL1_X + 10
P1_B2_X = P1_B1_X + BW + ARROW_GAP
P1_B3_X = P1_B2_X + BW + ARROW_GAP

d.rect(
    "p1_b1",
    P1_B1_X,
    P1_BOX_Y,
    BW,
    BH,
    *BLUE,
    fill="hachure",
    bnd=[{"id": "p1_t1", "type": "text"}],
)
d.txt("p1_t1", P1_B1_X, P1_BOX_Y, BW, BH, "task1", 18, cid="p1_b1")

d.rect(
    "p1_b2",
    P1_B2_X,
    P1_BOX_Y,
    BW,
    BH,
    *BLUE,
    fill="hachure",
    bnd=[{"id": "p1_t2", "type": "text"}],
)
d.txt("p1_t2", P1_B2_X, P1_BOX_Y, BW, BH, "task2", 18, cid="p1_b2")

d.rect(
    "p1_b3",
    P1_B3_X,
    P1_BOX_Y,
    BW,
    BH,
    *BLUE,
    fill="hachure",
    bnd=[{"id": "p1_t3", "type": "text"}],
)
d.txt("p1_t3", P1_B3_X, P1_BOX_Y, BW, BH, "task3", 18, cid="p1_b3")

d.arr(
    "p1_a1",
    P1_B1_X + BW,
    P1_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP, 0]],
    BLUE[0],
    sb={"elementId": "p1_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p1_b2", "focus": 0, "gap": 4},
)
d.arr(
    "p1_a2",
    P1_B2_X + BW,
    P1_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP, 0]],
    BLUE[0],
    sb={"elementId": "p1_b2", "focus": 0, "gap": 4},
    eb={"elementId": "p1_b3", "focus": 0, "gap": 4},
)


# === PATTERN 2: Fan-Out (top-right) ===
P2_Y = 100
d.txt("p2_title", COL2_X, P2_Y, COL_W, 25, "Fan-Out (Parallel)", 22, color=GREEN[0])
d.txt(
    "p2_code",
    COL2_X,
    P2_Y + 28,
    COL_W,
    20,
    "task1 >> [task2, task3]",
    14,
    color=GRAY[0],
)

P2_BOX_Y = P2_Y + 60
P2_B1_X = COL2_X + 10
P2_B2_X = P2_B1_X + BW + ARROW_GAP + 20
P2_B2_Y_TOP = P2_BOX_Y - 5
P2_B3_Y_BOT = P2_BOX_Y + BH + 15

d.rect(
    "p2_b1",
    P2_B1_X,
    P2_BOX_Y,
    BW,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "p2_t1", "type": "text"}],
)
d.txt("p2_t1", P2_B1_X, P2_BOX_Y, BW, BH, "task1", 18, cid="p2_b1")

d.rect(
    "p2_b2",
    P2_B2_X,
    P2_B2_Y_TOP,
    BW,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "p2_t2", "type": "text"}],
)
d.txt("p2_t2", P2_B2_X, P2_B2_Y_TOP, BW, BH, "task2", 18, cid="p2_b2")

d.rect(
    "p2_b3",
    P2_B2_X,
    P2_B3_Y_BOT,
    BW,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "p2_t3", "type": "text"}],
)
d.txt("p2_t3", P2_B2_X, P2_B3_Y_BOT, BW, BH, "task3", 18, cid="p2_b3")

# Arrow to top
d.arr(
    "p2_a1",
    P2_B1_X + BW,
    P2_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP + 20, -(P2_BOX_Y - P2_B2_Y_TOP) + BH // 2 - BH // 2]],
    GREEN[0],
    sb={"elementId": "p2_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p2_b2", "focus": 0, "gap": 4},
)
# Arrow to bottom
d.arr(
    "p2_a2",
    P2_B1_X + BW,
    P2_BOX_Y + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P2_B3_Y_BOT - P2_BOX_Y]],
    GREEN[0],
    sb={"elementId": "p2_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p2_b3", "focus": 0, "gap": 4},
)


# === PATTERN 3: Fan-In (bottom-left) ===
P3_Y = 280
d.txt("p3_title", COL1_X, P3_Y, COL_W, 25, "Fan-In (Converge)", 22, color=PURPLE[0])
d.txt(
    "p3_code",
    COL1_X,
    P3_Y + 28,
    COL_W,
    20,
    "[task1, task2] >> task3",
    14,
    color=GRAY[0],
)

P3_BOX_Y = P3_Y + 60
P3_B1_Y_TOP = P3_BOX_Y - 5
P3_B2_Y_BOT = P3_BOX_Y + BH + 15
P3_B1_X = COL1_X + 10
P3_B3_X = P3_B1_X + BW + ARROW_GAP + 20

d.rect(
    "p3_b1",
    P3_B1_X,
    P3_B1_Y_TOP,
    BW,
    BH,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "p3_t1", "type": "text"}],
)
d.txt("p3_t1", P3_B1_X, P3_B1_Y_TOP, BW, BH, "task1", 18, cid="p3_b1")

d.rect(
    "p3_b2",
    P3_B1_X,
    P3_B2_Y_BOT,
    BW,
    BH,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "p3_t2", "type": "text"}],
)
d.txt("p3_t2", P3_B1_X, P3_B2_Y_BOT, BW, BH, "task2", 18, cid="p3_b2")

d.rect(
    "p3_b3",
    P3_B3_X,
    P3_BOX_Y + BH // 2,
    BW,
    BH,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "p3_t3", "type": "text"}],
)
d.txt("p3_t3", P3_B3_X, P3_BOX_Y + BH // 2, BW, BH, "task3", 18, cid="p3_b3")

# Arrow from top
d.arr(
    "p3_a1",
    P3_B1_X + BW,
    P3_B1_Y_TOP + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P3_BOX_Y + BH // 2 + BH // 2 - P3_B1_Y_TOP - BH // 2]],
    PURPLE[0],
    sb={"elementId": "p3_b1", "focus": 0, "gap": 4},
    eb={"elementId": "p3_b3", "focus": 0, "gap": 4},
)
# Arrow from bottom
d.arr(
    "p3_a2",
    P3_B1_X + BW,
    P3_B2_Y_BOT + BH // 2,
    [[0, 0], [ARROW_GAP + 20, P3_BOX_Y + BH // 2 + BH // 2 - P3_B2_Y_BOT - BH // 2]],
    PURPLE[0],
    sb={"elementId": "p3_b2", "focus": 0, "gap": 4},
    eb={"elementId": "p3_b3", "focus": 0, "gap": 4},
)


# === PATTERN 4: Complex with chain() (bottom-right) ===
P4_Y = 280
d.txt("p4_title", COL2_X, P4_Y, COL_W, 25, "Complex (chain)", 22, color=YELLOW[0])
d.txt(
    "p4_code",
    COL2_X,
    P4_Y + 28,
    COL_W,
    20,
    "chain(t0, [t1, t2], [t3, t4], t5)",
    14,
    color=GRAY[0],
)

P4_BOX_Y = P4_Y + 60
BW_S = 70  # smaller boxes for this pattern
BH_S = 38
COL_GAP = 45

# t0 on the left
T0_X = COL2_X + 5
T0_Y = P4_BOX_Y + 30
d.rect(
    "p4_t0",
    T0_X,
    T0_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t0t", "type": "text"}],
)
d.txt("p4_t0t", T0_X, T0_Y, BW_S, BH_S, "t0", 16, cid="p4_t0")

# t1, t2 column
T12_X = T0_X + BW_S + COL_GAP
T1_Y = P4_BOX_Y + 5
T2_Y = T1_Y + BH_S + 20
d.rect(
    "p4_t1",
    T12_X,
    T1_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t1t", "type": "text"}],
)
d.txt("p4_t1t", T12_X, T1_Y, BW_S, BH_S, "t1", 16, cid="p4_t1")

d.rect(
    "p4_t2",
    T12_X,
    T2_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t2t", "type": "text"}],
)
d.txt("p4_t2t", T12_X, T2_Y, BW_S, BH_S, "t2", 16, cid="p4_t2")

# t3, t4 column
T34_X = T12_X + BW_S + COL_GAP
T3_Y = T1_Y
T4_Y = T2_Y
d.rect(
    "p4_t3",
    T34_X,
    T3_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t3t", "type": "text"}],
)
d.txt("p4_t3t", T34_X, T3_Y, BW_S, BH_S, "t3", 16, cid="p4_t3")

d.rect(
    "p4_t4",
    T34_X,
    T4_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t4t", "type": "text"}],
)
d.txt("p4_t4t", T34_X, T4_Y, BW_S, BH_S, "t4", 16, cid="p4_t4")

# t5 on the right
T5_X = T34_X + BW_S + COL_GAP
T5_Y = T0_Y
d.rect(
    "p4_t5",
    T5_X,
    T5_Y,
    BW_S,
    BH_S,
    *YELLOW,
    fill="hachure",
    bnd=[{"id": "p4_t5t", "type": "text"}],
)
d.txt("p4_t5t", T5_X, T5_Y, BW_S, BH_S, "t5", 16, cid="p4_t5")

# Arrows: t0 → t1, t0 → t2
d.arr(
    "p4_a01",
    T0_X + BW_S,
    T0_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T1_Y + BH_S // 2 - T0_Y - BH_S // 2]],
    YELLOW[0],
    sb={"elementId": "p4_t0", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t1", "focus": 0, "gap": 4},
)
d.arr(
    "p4_a02",
    T0_X + BW_S,
    T0_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T2_Y + BH_S // 2 - T0_Y - BH_S // 2]],
    YELLOW[0],
    sb={"elementId": "p4_t0", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t2", "focus": 0, "gap": 4},
)

# Arrows: t1 → t3, t1 → t4, t2 → t3, t2 → t4
d.arr(
    "p4_a13",
    T12_X + BW_S,
    T1_Y + BH_S // 2,
    [[0, 0], [COL_GAP, 0]],
    YELLOW[0],
    sb={"elementId": "p4_t1", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t3", "focus": 0, "gap": 4},
)
d.arr(
    "p4_a14",
    T12_X + BW_S,
    T1_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T4_Y - T1_Y]],
    YELLOW[0],
    sb={"elementId": "p4_t1", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t4", "focus": 0, "gap": 4},
)
d.arr(
    "p4_a23",
    T12_X + BW_S,
    T2_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T3_Y - T2_Y]],
    YELLOW[0],
    sb={"elementId": "p4_t2", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t3", "focus": 0, "gap": 4},
)
d.arr(
    "p4_a24",
    T12_X + BW_S,
    T2_Y + BH_S // 2,
    [[0, 0], [COL_GAP, 0]],
    YELLOW[0],
    sb={"elementId": "p4_t2", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t4", "focus": 0, "gap": 4},
)

# Arrows: t3 → t5, t4 → t5
d.arr(
    "p4_a35",
    T34_X + BW_S,
    T3_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T5_Y + BH_S // 2 - T3_Y - BH_S // 2]],
    YELLOW[0],
    sb={"elementId": "p4_t3", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t5", "focus": 0, "gap": 4},
)
d.arr(
    "p4_a45",
    T34_X + BW_S,
    T4_Y + BH_S // 2,
    [[0, 0], [COL_GAP, T5_Y + BH_S // 2 - T4_Y - BH_S // 2]],
    YELLOW[0],
    sb={"elementId": "p4_t4", "focus": 0, "gap": 4},
    eb={"elementId": "p4_t5", "focus": 0, "gap": 4},
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/dag-dependencies"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
