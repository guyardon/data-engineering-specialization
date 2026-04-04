#!/usr/bin/env python3
"""Generate AWS VPC Networking diagram (light + dark) using diagrams library.

Post-processes Graphviz layout to center User/IGW/ALB between the AZ clusters.
Saves DOT source, runs `dot -Tdot` to get positions, shifts target nodes
to horizontal center, then renders with `neato -n2`.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB, NATGateway, InternetGateway
from diagrams.aws.general import User
import os
import re
import subprocess
import tempfile

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images", "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)


def render_centered(dot_source, png_path, node_ids):
    """Render DOT with target nodes centered horizontally."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
        f.write(dot_source)
        dot_path = f.name

    # Get positioned DOT from dot layout engine
    result = subprocess.run(
        ["dot", "-Tdot", dot_path], capture_output=True, text=True
    )
    positioned = result.stdout
    os.remove(dot_path)

    # Find bounding box center
    bb_match = re.search(r'bb="([^"]+)"', positioned)
    if not bb_match:
        subprocess.run(["dot", "-Tpng", "-o", png_path, dot_path])
        return

    bb = bb_match.group(1).split(",")
    center_x = (float(bb[0]) + float(bb[2])) / 2

    # Shift each target node's x-position to center
    for nid in node_ids:
        # Node IDs may or may not be quoted in the positioned DOT
        pattern = rf'"?{re.escape(nid)}"?\s+\[(?:[^\]]*?)pos="([0-9.]+),([0-9.]+)"'
        match = re.search(pattern, positioned)
        if match:
            old_pos = f'{match.group(1)},{match.group(2)}'
            new_pos = f'{center_x:.2f},{match.group(2)}'
            positioned = positioned[:match.start(1)] + new_pos + positioned[match.end(2):]
            print(f"    Shifted {nid[:8]}... from x={match.group(1)} to x={center_x:.2f}")

    # Write centered DOT and render
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
        f.write(positioned)
        centered_path = f.name

    subprocess.run(["neato", "-n", "-Tpng", "-o", png_path, centered_path])
    os.remove(centered_path)


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    edge_color = "#65656e" if dark else "#495057"

    if dark:
        cc = {
            "vpc":  {"bg": "#1a1a2a", "fc": "#c4b5fd", "border": "#6741d9"},
            "az":   {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "pub":  {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "priv": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
        }
    else:
        cc = {
            "vpc":  {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
            "az":   {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "pub":  {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "priv": {"bg": "#ffc9c940", "fc": "#c92a2a", "border": "#c92a2a"},
        }

    graph_attr = {
        "bgcolor": bg,
        "fontcolor": fc,
        "fontsize": "32",
        "fontname": "Helvetica Bold",
        "pad": "0.3",
        "nodesep": "3.0",
        "ranksep": "0.7",
        "dpi": "150",
        "label": "AWS VPC Networking\n\n",
        "labelloc": "t",
        "rankdir": "TB",
        "compound": "true",
    }
    node_attr = {
        "fontsize": "20",
        "fontname": "Helvetica",
        "fontcolor": fc,
        "height": "1.7",
    }
    edge_attr = {
        "color": edge_color,
        "penwidth": "3.0",
    }

    def cattr(key):
        c = cc[key]
        return {
            "fontsize": "22",
            "fontname": "Helvetica Bold",
            "penwidth": "1.5",
            "labeljust": "c",
            "labelloc": "t",
            "style": "dashed,rounded",
            "margin": "18",
            "bgcolor": c["bg"],
            "fontcolor": c["fc"],
            "pencolor": c["border"],
        }

    out_path = os.path.join(OUT_DIR, f"vpc-networking-aws{suffix}")
    png_path = out_path + ".png"

    # Build the diagram and capture DOT source + node IDs
    dot_source = None
    top_ids = []

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat="png",
    ) as d:
        user = User("User")
        igw = InternetGateway("Internet\nGateway")

        e = lambda **kw: Edge(color=edge_color, **kw)

        with Cluster("VPC  (10.0.0.0/16)", graph_attr=cattr("vpc")):
            alb = ALB("ALB")

            with Cluster("Availability Zone 1", graph_attr=cattr("az")):
                with Cluster("Public Subnet\n10.0.1.0/24", graph_attr=cattr("pub")):
                    nat1 = NATGateway("NAT\nGateway")

                with Cluster("Private Subnet\n10.0.2.0/24", graph_attr=cattr("priv")):
                    ec2_1 = EC2("EC2")
                    rds_1 = RDS("RDS")

            with Cluster("Availability Zone 2", graph_attr=cattr("az")):
                with Cluster("Public Subnet\n10.0.3.0/24", graph_attr=cattr("pub")):
                    nat2 = NATGateway("NAT\nGateway")

                with Cluster("Private Subnet\n10.0.4.0/24", graph_attr=cattr("priv")):
                    ec2_2 = EC2("EC2")
                    rds_2 = RDS("RDS")

        # Top flow (minlen=1 to keep User→IGW close despite large ranksep)
        user >> e() >> igw >> e(lhead="cluster_VPC  (10.0.0.0/16)", minlen="2") >> alb
        alb >> e(lhead="cluster_Availability Zone 1") >> ec2_1
        alb >> e(lhead="cluster_Availability Zone 2") >> ec2_2
        ec2_1 >> e() >> rds_1
        ec2_2 >> e() >> rds_2
        ec2_1 >> e(lhead="cluster_Public Subnet\n10.0.1.0/24") >> nat1
        ec2_2 >> e(lhead="cluster_Public Subnet\n10.0.3.0/24") >> nat2

        # Capture before __exit__ renders and deletes
        dot_source = d.dot.source
        top_ids = [user._id, igw._id, alb._id]

    # Now re-render with centering
    render_centered(dot_source, png_path, top_ids)
    print(f"  Centered {len(top_ids)} nodes in {png_path}")


gen(dark=False)
gen(dark=True)
print("Done — generated light and dark VPC networking AWS diagrams")
