"""
Evolution of Orchestration Tools — horizontal timeline with alternating milestone boxes.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, GRAY, GREEN, PURPLE, YELLOW

d = ExcalidrawDiagram(seed=3000)

# === LAYOUT CONSTANTS ===
CANVAS_W = 700
PAD_X = 20
CONTENT_W = CANVAS_W - 2 * PAD_X  # 660

# Title
TITLE_Y = 15
TITLE_H = math.ceil(32 * 1.25)  # 40

# Timeline axis
TIMELINE_Y = 260  # vertical center for the horizontal line
TIMELINE_X0 = PAD_X + 10
TIMELINE_X1 = CANVAS_W - PAD_X - 10

# Milestone boxes
BOX_W = 110
BOX_H = 80
STEM_H = 40  # vertical connector from timeline to box
BOX_GAP_ABOVE = 10  # gap between stem end and box

# Milestones: (title, subtitle, color, above_or_below)
# Alternate above/below for visual variety
milestones = [
    ("Dataswarm", "Late 2000s\nFacebook", GRAY, "above"),
    ("Apache Oozie", "2010s\nHadoop-only", YELLOW, "below"),
    ("Airflow", "2014\nAirbnb", BLUE, "above"),
    ("Apache Airflow", "2019\nTop-level project", GREEN, "below"),
    ("Prefect, Dagster\nMage", "Today\nModern tools", PURPLE, "above"),
]

N = len(milestones)
# Distribute milestones evenly along the timeline
usable_w = TIMELINE_X1 - TIMELINE_X0 - 40  # leave room for arrow tip
spacing = usable_w / (N - 1) if N > 1 else 0
first_x = TIMELINE_X0 + 20  # offset from start

# === BUILD DIAGRAM ===

# Title
d.txt(
    "title",
    PAD_X,
    TITLE_Y,
    CONTENT_W,
    TITLE_H,
    "Evolution of Orchestration Tools",
    32,
    color="#1e1e1e",
)

# Timeline arrow (horizontal, left to right)
d.arr(
    "timeline",
    TIMELINE_X0,
    TIMELINE_Y,
    [[0, 0], [TIMELINE_X1 - TIMELINE_X0, 0]],
    GRAY[0],
)

# Milestone boxes and connectors
for i, (name, sub, color, pos) in enumerate(milestones):
    cx = first_x + i * spacing  # center x of this milestone on timeline
    box_x = cx - BOX_W // 2

    card_id = f"card{i}"
    card_t_id = f"card-t{i}"
    sub_id = f"sub{i}"
    stem_id = f"stem{i}"
    dot_id = f"dot{i}"

    if pos == "above":
        # Box above timeline
        box_y = TIMELINE_Y - STEM_H - BOX_H - BOX_GAP_ABOVE
        stem_y1 = TIMELINE_Y
        stem_y0 = box_y + BOX_H + BOX_GAP_ABOVE
        d.line(stem_id, cx, stem_y0, [[0, 0], [0, stem_y1 - stem_y0]], color[0])
    else:
        # Box below timeline
        box_y = TIMELINE_Y + STEM_H + BOX_GAP_ABOVE
        stem_y0 = TIMELINE_Y
        stem_y1 = box_y - BOX_GAP_ABOVE
        d.line(stem_id, cx, stem_y0, [[0, 0], [0, stem_y1 - stem_y0]], color[0])

    # Small dot on the timeline
    dot_sz = 10
    d.rect(
        dot_id,
        cx - dot_sz // 2,
        TIMELINE_Y - dot_sz // 2,
        dot_sz,
        dot_sz,
        color[0],
        color[1],
    )

    # Card with bound title text (Rule 13) + free subtitle
    title_h = math.ceil((name.count("\n") + 1) * 22 * 1.25)
    sub_lines = sub.count("\n") + 1
    sub_h = math.ceil(sub_lines * 17 * 1.25)
    gap = 4
    combined = title_h + gap + sub_h
    top_pad = (BOX_H - combined) // 2
    title_y = box_y + top_pad
    sub_y = title_y + title_h + gap

    d.rect(
        card_id,
        box_x,
        box_y,
        BOX_W,
        BOX_H,
        color[0],
        color[1],
        bnd=[{"id": card_t_id, "type": "text"}],
    )
    d.txt(
        card_t_id,
        box_x,
        title_y,
        BOX_W,
        title_h,
        name,
        22,
        color="#1e1e1e",
        cid=card_id,
    )
    d.txt(sub_id, box_x, sub_y, BOX_W, sub_h, sub, 17, color=color[0])

# === WRITE FILE ===
name = sys.argv[1] if len(sys.argv) > 1 else "diagrams/artifacts/orchestration-timeline"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
