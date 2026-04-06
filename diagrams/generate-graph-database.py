"""
Graph Database schematic diagram.
Shows a small property graph with nodes (Product, Category, Customer, Order)
connected by labeled edges (PART_OF, ORDERS) with properties shown.

Canvas: 650px wide, horizontal layout.
"""

import sys

from diagramlib import ExcalidrawDiagram, BLUE, GREEN, YELLOW, PURPLE, CYAN, GRAY

d = ExcalidrawDiagram(seed=9000)


# ellipse is not in diagramlib — define it locally
def ellipse(id, x, y, w, h, stroke, bg, fill="hachure", bnd=None):
    d.elements.append(
        {
            "type": "ellipse",
            "id": id,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": fill,
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "roundness": {"type": 2},
            "seed": d._ns(),
            "version": 1,
            "versionNonce": d._ns(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": bnd or [],
            "frameId": None,
            "link": None,
            "locked": False,
            "updated": 1710000000000,
        }
    )


# === LAYOUT ===
CANVAS_W = 650
PAD_X = 25
CONTENT_W = CANVAS_W - 2 * PAD_X
NW = 130  # node width (ellipse)
NH = 70  # node height (ellipse)

# Title
TITLE_Y = 15
d.txt("title", PAD_X, TITLE_Y, CONTENT_W, 40, "Graph Database", 32)
d.txt(
    "sub",
    PAD_X,
    TITLE_Y + 38,
    CONTENT_W,
    25,
    "Nodes, edges, and properties",
    17,
    color=PURPLE[0],
)

# === NODES (diamond layout) ===
#       Customer (top center)
#      /         \
#   Order -----> Product ----> Category
#

CUSTOMER_X = CANVAS_W // 2 - NW // 2
CUSTOMER_Y = 100

ORDER_X = PAD_X + 40
ORDER_Y = 250

PRODUCT_X = CANVAS_W // 2 - NW // 2
PRODUCT_Y = 250

CATEGORY_X = CANVAS_W - PAD_X - NW - 40
CATEGORY_Y = 250

# Customer node
ellipse(
    "customer",
    CUSTOMER_X,
    CUSTOMER_Y,
    NW,
    NH,
    *BLUE,
    bnd=[{"id": "customer_t", "type": "text"}],
)
d.txt("customer_t", CUSTOMER_X, CUSTOMER_Y, NW, NH, "Customer", 20, cid="customer")

# Properties label below Customer
d.txt(
    "customer_props",
    CUSTOMER_X - 10,
    CUSTOMER_Y + NH + 5,
    NW + 20,
    25,
    "name, email",
    15,
    color=BLUE[0],
    op=70,
)

# Order node
ellipse(
    "order", ORDER_X, ORDER_Y, NW, NH, *GREEN, bnd=[{"id": "order_t", "type": "text"}]
)
d.txt("order_t", ORDER_X, ORDER_Y, NW, NH, "Order", 20, cid="order")

# Properties
d.txt(
    "order_props",
    ORDER_X - 10,
    ORDER_Y + NH + 5,
    NW + 20,
    25,
    "date, total",
    15,
    color=GREEN[0],
    op=70,
)

# Product node
ellipse(
    "product",
    PRODUCT_X,
    PRODUCT_Y,
    NW,
    NH,
    *YELLOW,
    bnd=[{"id": "product_t", "type": "text"}],
)
d.txt("product_t", PRODUCT_X, PRODUCT_Y, NW, NH, "Product", 20, cid="product")

# Properties
d.txt(
    "product_props",
    PRODUCT_X - 15,
    PRODUCT_Y + NH + 5,
    NW + 30,
    25,
    "name, unitPrice",
    15,
    color=YELLOW[0],
    op=70,
)

# Category node
ellipse(
    "category",
    CATEGORY_X,
    CATEGORY_Y,
    NW,
    NH,
    *PURPLE,
    bnd=[{"id": "category_t", "type": "text"}],
)
d.txt("category_t", CATEGORY_X, CATEGORY_Y, NW, NH, "Category", 20, cid="category")

# Properties
d.txt(
    "category_props",
    CATEGORY_X - 10,
    CATEGORY_Y + NH + 5,
    NW + 20,
    25,
    "categoryName",
    15,
    color=PURPLE[0],
    op=70,
)

# === EDGES (arrows between nodes) ===

# Customer → Order  (PLACES)
d.arr(
    "e_places",
    CUSTOMER_X + NW // 4,
    CUSTOMER_Y + NH,
    [[0, 0], [ORDER_X + NW // 2 - CUSTOMER_X - NW // 4, ORDER_Y - CUSTOMER_Y - NH]],
    GREEN[0],
    sb={"elementId": "customer", "focus": 0, "gap": 4},
    eb={"elementId": "order", "focus": 0, "gap": 4},
)
d.txt(
    "l_places", ORDER_X - 25, CUSTOMER_Y + NH + 20, 90, 25, "PLACES", 16, color=GREEN[0]
)

# Order → Product  (ORDERS)
d.arr(
    "e_orders",
    ORDER_X + NW,
    ORDER_Y + NH // 2,
    [[0, 0], [PRODUCT_X - ORDER_X - NW, 0]],
    YELLOW[0],
    sb={"elementId": "order", "focus": 0, "gap": 4},
    eb={"elementId": "product", "focus": 0, "gap": 4},
)
d.txt(
    "l_orders",
    ORDER_X + NW + 10,
    ORDER_Y + NH // 2 - 28,
    80,
    25,
    "ORDERS",
    16,
    color=YELLOW[0],
)

# Product → Category  (PART_OF)
d.arr(
    "e_partof",
    PRODUCT_X + NW,
    PRODUCT_Y + NH // 2,
    [[0, 0], [CATEGORY_X - PRODUCT_X - NW, 0]],
    PURPLE[0],
    sb={"elementId": "product", "focus": 0, "gap": 4},
    eb={"elementId": "category", "focus": 0, "gap": 4},
)
d.txt(
    "l_partof",
    PRODUCT_X + NW + 10,
    PRODUCT_Y + NH // 2 - 28,
    80,
    25,
    "PART_OF",
    16,
    color=PURPLE[0],
)

# Customer → Product  (diagonal, REVIEWED)
d.arr(
    "e_reviewed",
    CUSTOMER_X + 3 * NW // 4,
    CUSTOMER_Y + NH,
    [
        [0, 0],
        [PRODUCT_X + NW // 2 - CUSTOMER_X - 3 * NW // 4, PRODUCT_Y - CUSTOMER_Y - NH],
    ],
    CYAN[0],
    dash=True,
    sb={"elementId": "customer", "focus": 0, "gap": 4},
    eb={"elementId": "product", "focus": 0, "gap": 4},
)
d.txt(
    "l_reviewed",
    PRODUCT_X + NW - 10,
    CUSTOMER_Y + NH + 20,
    100,
    25,
    "REVIEWED",
    16,
    color=CYAN[0],
)

# === Legend ===
LEGEND_Y = 350
d.txt(
    "legend",
    PAD_X,
    LEGEND_Y,
    CONTENT_W,
    25,
    "() = Node (entity)     --> = Edge (relationship)     Properties = key-value attributes",
    15,
    color=GRAY[0],
    op=70,
)


# === WRITE ===
name = sys.argv[1] if len(sys.argv) > 1 else "graph-database"
outfile = f"{name}.excalidraw"
d.save(outfile)
print(f"Wrote {outfile}")
