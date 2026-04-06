"""
XCom cross-communication flow diagram.
Shows: Task 1 -> xcom_push -> XCom Variable -> Metadata DB -> xcom_pull -> Task 2

Horizontal flow with a vertical drop to the database.
Canvas: ~700px wide for good aspect ratio.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, PURPLE, GRAY

d = ExcalidrawDiagram(seed=1000)

# === LAYOUT ===
# Horizontal flow: Task 1 -> XCom Variable -> Metadata DB -> Task 2
# With xcom_push / xcom_pull labels on arrows

CANVAS_W = 680
PAD_X = 20

# Title
TITLE_Y = 20
d.txt("title", PAD_X, TITLE_Y, CANVAS_W - 2 * PAD_X, 40, "XCom Cross-Communication", 32)

# Row 1: Task 1 and XCom Variable box
ROW1_Y = 90
BW_TASK = 140
BH = 70
BW_XCOM = 200
BH_XCOM = 130
GAP_H = 90  # horizontal gap for arrows

# Task 1
T1_X = PAD_X + 20
T1_Y = ROW1_Y + 30
d.rect(
    "task1",
    T1_X,
    T1_Y,
    BW_TASK,
    BH,
    *BLUE,
    fill="hachure",
    bnd=[{"id": "t_task1", "type": "text"}],
)
d.txt("t_task1", T1_X, T1_Y, BW_TASK, BH, "Task 1", 24, cid="task1")

# XCom Variable (taller box with bullet list)
XCOM_X = T1_X + BW_TASK + GAP_H
XCOM_Y = ROW1_Y
d.rect(
    "xcom",
    XCOM_X,
    XCOM_Y,
    BW_XCOM,
    BH_XCOM,
    *PURPLE,
    fill="hachure",
    bnd=[{"id": "t_xcom", "type": "text"}],
)
d.txt(
    "t_xcom",
    XCOM_X,
    XCOM_Y,
    BW_XCOM,
    BH_XCOM,
    "XCom Variable\n\nValue\nKey\nTimestamp\nDAG ID\nTask ID",
    18,
    cid="xcom",
)

# Arrow: Task 1 -> XCom Variable
A1_X = T1_X + BW_TASK
A1_Y = T1_Y + BH // 2
d.arr(
    "a1",
    A1_X,
    A1_Y,
    [[0, 0], [GAP_H, 0]],
    BLUE[0],
    sb={"elementId": "task1", "focus": 0, "gap": 4},
    eb={"elementId": "xcom", "focus": 0, "gap": 4},
)

# Label: xcom_push
d.txt("l_push", A1_X + 10, A1_Y - 28, 70, 20, "xcom_push", 16, color=BLUE[0])

# Row 2: Metadata Database (centered below XCom Variable)
DB_W = 200
DB_H = 70
DB_X = XCOM_X
DB_Y = XCOM_Y + BH_XCOM + 70
d.rect(
    "db",
    DB_X,
    DB_Y,
    DB_W,
    DB_H,
    *GRAY,
    fill="hachure",
    bnd=[{"id": "t_db", "type": "text"}],
)
d.txt("t_db", DB_X, DB_Y, DB_W, DB_H, "Metadata\nDatabase", 22, cid="db")

# Arrow: XCom Variable -> Metadata DB (vertical)
A2_X = XCOM_X + BW_XCOM // 2
A2_Y = XCOM_Y + BH_XCOM
d.arr(
    "a2",
    A2_X,
    A2_Y,
    [[0, 0], [0, 70]],
    PURPLE[0],
    sb={"elementId": "xcom", "focus": 0, "gap": 4},
    eb={"elementId": "db", "focus": 0, "gap": 4},
)

# Task 2 (to the right of DB)
T2_X = DB_X + DB_W + GAP_H
T2_Y = DB_Y
d.rect(
    "task2",
    T2_X,
    T2_Y,
    BW_TASK,
    BH,
    *GREEN,
    fill="hachure",
    bnd=[{"id": "t_task2", "type": "text"}],
)
d.txt("t_task2", T2_X, T2_Y, BW_TASK, BH, "Task 2", 24, cid="task2")

# Arrow: Metadata DB -> Task 2
A3_X = DB_X + DB_W
A3_Y = DB_Y + DB_H // 2
d.arr(
    "a3",
    A3_X,
    A3_Y,
    [[0, 0], [GAP_H, 0]],
    GRAY[0],
    sb={"elementId": "db", "focus": 0, "gap": 4},
    eb={"elementId": "task2", "focus": 0, "gap": 4},
)

# Label: xcom_pull
d.txt("l_pull", A3_X + 10, A3_Y - 28, 70, 20, "xcom_pull", 16, color=GREEN[0])

# Subtitle
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CANVAS_W - 2 * PAD_X,
    25,
    "Tasks exchange small data via the metadata database",
    17,
    color=PURPLE[0],
)

# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/xcom-flow"
d.save(f"{name}.excalidraw")
print(f"Wrote {name}.excalidraw")
