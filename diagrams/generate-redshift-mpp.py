"""
Generate Redshift MPP architecture diagram showing leader node
distributing queries to compute node slices.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, CYAN, GRAY, GREEN, YELLOW

d = ExcalidrawDiagram(seed=2000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 660
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 620

# === TITLE ===
TITLE_Y = 15
TITLE_H = math.ceil(1 * 32 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Redshift MPP Architecture", 32, color="#1e1e1e")

# === CLIENT APPLICATION ===
ARROW_GAP = 70
CLIENT_Y = TITLE_Y + TITLE_H + 30
CLIENT_W = 220
CLIENT_H = 50
CLIENT_X = PAD_X + (CONTENT_W - CLIENT_W) // 2
d.rect("client", CLIENT_X, CLIENT_Y, CLIENT_W, CLIENT_H, *GRAY,
     bnd=[{"id": "client_t", "type": "text"}])
d.txt("client_t", CLIENT_X, CLIENT_Y, CLIENT_W, CLIENT_H,
    "Client Application", 22, cid="client")

# Label
CLIENT_LABEL_Y = CLIENT_Y + CLIENT_H + 6
CLIENT_LABEL_H = math.ceil(1 * 16 * 1.25)
d.txt("client_label", CLIENT_X, CLIENT_LABEL_Y, CLIENT_W, CLIENT_LABEL_H,
    "SQL query", 16, color=GRAY[0])

# === LEADER NODE ===
LEADER_Y = CLIENT_LABEL_Y + CLIENT_LABEL_H + 50
LEADER_W = 280
LEADER_H = 60
LEADER_X = PAD_X + (CONTENT_W - LEADER_W) // 2
d.rect("leader", LEADER_X, LEADER_Y, LEADER_W, LEADER_H, *YELLOW,
     bnd=[{"id": "leader_t", "type": "text"}])
d.txt("leader_t", LEADER_X, LEADER_Y, LEADER_W, LEADER_H,
    "Leader Node", 24, cid="leader")

# Arrow: Client to Leader
d.arr("a_cl", CLIENT_X + CLIENT_W // 2, CLIENT_Y + CLIENT_H,
    [[0, 0], [0, LEADER_Y - CLIENT_Y - CLIENT_H]],
    GRAY[0],
    sb={"elementId": "client", "focus": 0, "gap": 4},
    eb={"elementId": "leader", "focus": 0, "gap": 4})

# Leader subtitle
LEADER_SUB_Y = LEADER_Y + LEADER_H + 6
LEADER_SUB_H = math.ceil(1 * 16 * 1.25)
d.txt("leader_sub", LEADER_X, LEADER_SUB_Y, LEADER_W, LEADER_SUB_H,
    "Query planning & distribution", 16, color=YELLOW[0])

# === COMPUTE NODES CONTAINER ===
CN_CONTAINER_Y = LEADER_SUB_Y + LEADER_SUB_H + 55
CN_PAD = 20
NODE_W = (CONTENT_W - 2 * CN_PAD - 20) // 2  # two nodes side by side
NODE_H = 140
SLICE_W = NODE_W - 20
SLICE_H = 45

CN_CONTAINER_H = CN_PAD + 30 + NODE_H + CN_PAD + 15
d.rect("cn_container", PAD_X, CN_CONTAINER_Y, CONTENT_W, CN_CONTAINER_H,
     BLUE[0], "#dbe4ff", dashed=True)

# Container label
CN_LABEL_Y = CN_CONTAINER_Y + 10
CN_LABEL_H = math.ceil(1 * 20 * 1.25)
d.txt("cn_label", PAD_X, CN_LABEL_Y, CONTENT_W, CN_LABEL_H,
    "Compute Nodes", 20, color=BLUE[0])

# === Compute Node 1 ===
N1_X = PAD_X + CN_PAD
N1_Y = CN_LABEL_Y + CN_LABEL_H + 10
d.rect("node1", N1_X, N1_Y, NODE_W, NODE_H, *BLUE)

N1_LABEL_Y = N1_Y + 8
N1_LABEL_H = math.ceil(1 * 18 * 1.25)
d.txt("n1_label", N1_X, N1_LABEL_Y, NODE_W, N1_LABEL_H,
    "Node 1", 18, color=BLUE[0])

# Slices in node 1
S1_Y = N1_LABEL_Y + N1_LABEL_H + 6
S1_X = N1_X + 10
d.rect("slice1a", S1_X, S1_Y, SLICE_W, SLICE_H, *CYAN,
     bnd=[{"id": "s1a_t", "type": "text"}])
d.txt("s1a_t", S1_X, S1_Y, SLICE_W, SLICE_H, "Slice 1", 17, cid="slice1a")

S2_Y = S1_Y + SLICE_H + 8
d.rect("slice1b", S1_X, S2_Y, SLICE_W, SLICE_H, *CYAN,
     bnd=[{"id": "s1b_t", "type": "text"}])
d.txt("s1b_t", S1_X, S2_Y, SLICE_W, SLICE_H, "Slice 2", 17, cid="slice1b")

# === Compute Node 2 ===
N2_X = PAD_X + CN_PAD + NODE_W + 20
N2_Y = N1_Y
d.rect("node2", N2_X, N2_Y, NODE_W, NODE_H, *BLUE)

N2_LABEL_Y = N2_Y + 8
N2_LABEL_H = math.ceil(1 * 18 * 1.25)
d.txt("n2_label", N2_X, N2_LABEL_Y, NODE_W, N2_LABEL_H,
    "Node 2", 18, color=BLUE[0])

# Slices in node 2
S3_Y = N2_LABEL_Y + N2_LABEL_H + 6
S3_X = N2_X + 10
d.rect("slice2a", S3_X, S3_Y, SLICE_W, SLICE_H, *CYAN,
     bnd=[{"id": "s2a_t", "type": "text"}])
d.txt("s2a_t", S3_X, S3_Y, SLICE_W, SLICE_H, "Slice 3", 17, cid="slice2a")

S4_Y = S3_Y + SLICE_H + 8
d.rect("slice2b", S3_X, S4_Y, SLICE_W, SLICE_H, *CYAN,
     bnd=[{"id": "s2b_t", "type": "text"}])
d.txt("s2b_t", S3_X, S4_Y, SLICE_W, SLICE_H, "Slice 4", 17, cid="slice2b")

# === ARROWS: Leader to Nodes ===
d.arr("a_l_n1", LEADER_X + LEADER_W // 2, LEADER_Y + LEADER_H,
    [[0, 0], [-(LEADER_X + LEADER_W // 2 - N1_X - NODE_W // 2), N1_Y - LEADER_Y - LEADER_H]],
    YELLOW[0],
    sb={"elementId": "leader", "focus": 0, "gap": 4},
    eb={"elementId": "node1", "focus": 0, "gap": 4})

d.arr("a_l_n2", LEADER_X + LEADER_W // 2, LEADER_Y + LEADER_H,
    [[0, 0], [N2_X + NODE_W // 2 - LEADER_X - LEADER_W // 2, N1_Y - LEADER_Y - LEADER_H]],
    YELLOW[0],
    sb={"elementId": "leader", "focus": 0, "gap": 4},
    eb={"elementId": "node2", "focus": 0, "gap": 4})

# === S3 STORAGE ===
S3_BOX_Y = CN_CONTAINER_Y + CN_CONTAINER_H + 70
S3_W = 260
S3_H = 50
S3_X = PAD_X + (CONTENT_W - S3_W) // 2
d.rect("s3", S3_X, S3_BOX_Y, S3_W, S3_H, *GREEN,
     bnd=[{"id": "s3_t", "type": "text"}])
d.txt("s3_t", S3_X, S3_BOX_Y, S3_W, S3_H,
    "S3 (Columnar Storage)", 20, cid="s3")

# Arrows from nodes to S3
d.arr("a_n1_s3", N1_X + NODE_W // 2, CN_CONTAINER_Y + CN_CONTAINER_H,
    [[0, 0], [S3_X + S3_W // 2 - N1_X - NODE_W // 2, S3_BOX_Y - CN_CONTAINER_Y - CN_CONTAINER_H]],
    BLUE[0],
    eb={"elementId": "s3", "focus": 0, "gap": 4})

d.arr("a_n2_s3", N2_X + NODE_W // 2, CN_CONTAINER_Y + CN_CONTAINER_H,
    [[0, 0], [S3_X + S3_W // 2 - N2_X - NODE_W // 2, S3_BOX_Y - CN_CONTAINER_Y - CN_CONTAINER_H]],
    BLUE[0],
    eb={"elementId": "s3", "focus": 0, "gap": 4})

# === VERIFY ===
print(f"Canvas: {CANVAS_W}x{S3_BOX_Y + S3_H + 20}")
print(f"Title: y={TITLE_Y}")
print(f"Client: y={CLIENT_Y} to {CLIENT_Y + CLIENT_H}")
print(f"Leader: y={LEADER_Y} to {LEADER_Y + LEADER_H}")
print(f"CN Container: y={CN_CONTAINER_Y} to {CN_CONTAINER_Y + CN_CONTAINER_H}")
print(f"S3: y={S3_BOX_Y} to {S3_BOX_Y + S3_H}")

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "redshift-mpp"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
