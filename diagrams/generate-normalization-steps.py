"""
Generate normalization progression diagram showing a practical example
going from denormalized -> 1NF -> 2NF -> 3NF with real order data.
"""

import math
import sys

from diagramlib import ExcalidrawDiagram, BLUE, CYAN, GRAY, GREEN, RED, YELLOW

d = ExcalidrawDiagram(seed=10000)

# === LAYOUT ===
CANVAS_W = 660
PAD_X = 15
CONTENT_W = CANVAS_W - 2 * PAD_X
BOX_W = CONTENT_W
ARROW_GAP = 18

TITLE_Y = 12
TITLE_H = math.ceil(1 * 30 * 1.25)
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, TITLE_H,
    "Normalization: A Practical Example", 30, color="#1e1e1e")

# Each step: colored box with title + subtitle showing what changed
steps = [
    ("denorm", "Denormalized", RED,
     "One wide table: order_id, product, price,\ncustomer_name, address, items_json\nRedundant data everywhere"),
    ("nf1", "1st Normal Form (1NF)", YELLOW,
     "Atomic values, composite PK (order_id + line_no)\nNo nested JSON — each item gets its own row\nRemoves: repeating groups"),
    ("nf2", "2nd Normal Form (2NF)", CYAN,
     "Split into: orders, order_items, products\nRemoves: partial dependencies\n(price depends on product, not on full PK)"),
    ("nf3", "3rd Normal Form (3NF)", GREEN,
     "Split into: orders, order_items, products, customers\nRemoves: transitive dependencies\n(customer_name depends on customer_id, not PK)"),
]

BOX_H = 100
y = TITLE_Y + TITLE_H + 20

for i, (bid, title, color, desc) in enumerate(steps):
    d.rect(bid, PAD_X, y, BOX_W, BOX_H, *color,
         bnd=[{"id": f"{bid}_t", "type": "text"}])

    title_h = math.ceil(1 * 24 * 1.25)
    desc_lines = desc.count("\n") + 1
    desc_h = math.ceil(desc_lines * 16 * 1.25)
    gap = 5
    combined = title_h + gap + desc_h
    top_pad = (BOX_H - combined) // 2

    d.txt(f"{bid}_t", PAD_X, y + top_pad, BOX_W, title_h,
        title, 24, cid=bid)
    d.txt(f"{bid}_sub", PAD_X, y + top_pad + title_h + gap, BOX_W, desc_h,
        desc, 16, color=color[0])

    if i < len(steps) - 1:
        d.arr(f"a{i}", PAD_X + BOX_W // 2, y + BOX_H,
            [[0, 0], [0, ARROW_GAP]],
            color[0],
            sb={"elementId": bid, "focus": 0, "gap": 4},
            eb={"elementId": steps[i + 1][0], "focus": 0, "gap": 4})

    y += BOX_H + ARROW_GAP

# Summary label
SUM_Y = y + 5
SUM_H = math.ceil(1 * 16 * 1.25)
d.txt("summary", PAD_X, SUM_Y, CONTENT_W, SUM_H,
    "Each step removes a type of dependency → less redundancy, better integrity",
    16, color=GRAY[0])

print(f"Canvas: {CANVAS_W}x{SUM_Y + SUM_H + 15}")

name = sys.argv[1] if len(sys.argv) > 1 else "normalization-steps"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
