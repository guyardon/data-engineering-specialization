#!/usr/bin/env python3
"""Generate Route Tables diagram (light + dark) using diagrams library.

Shows how route table configuration determines whether a subnet is public or private.
Public subnets route 0.0.0.0/0 → IGW; private subnets route 0.0.0.0/0 → NAT Gateway.

Uses the vpc-networking-aws pattern: Internet/IGW outside VPC, VPC Router fans out
to two wrapper clusters containing public and private subnets side by side.
No cross-cluster edges to avoid Graphviz stacking clusters vertically.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import NATGateway, InternetGateway, RouteTable, VPCRouter
from diagrams.aws.general import User
import os
import re
import subprocess
import tempfile

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public",
    "images",
    "diagrams",
)
os.makedirs(OUT_DIR, exist_ok=True)

DIAGRAM_NAME = "route-tables-aws"


def render_centered(dot_source, png_path, node_ids):
    """Render DOT with target nodes centered horizontally."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
        f.write(dot_source)
        dot_path = f.name

    result = subprocess.run(["dot", "-Tdot", dot_path], capture_output=True, text=True)
    positioned = result.stdout
    os.remove(dot_path)

    bb_match = re.search(r'bb="([^"]+)"', positioned)
    if not bb_match:
        subprocess.run(["dot", "-Tpng", "-o", png_path, dot_path])
        return

    bb = bb_match.group(1).split(",")
    center_x = (float(bb[0]) + float(bb[2])) / 2

    for nid in node_ids:
        pattern = rf'"?{re.escape(nid)}"?\s+\[(?:[^\]]*?)pos="([0-9.]+),([0-9.]+)"'
        match = re.search(pattern, positioned)
        if match:
            new_pos = f"{center_x:.2f},{match.group(2)}"
            positioned = (
                positioned[: match.start(1)] + new_pos + positioned[match.end(2) :]
            )
            print(
                f"    Shifted {nid[:8]}... from x={match.group(1)} to x={center_x:.2f}"
            )

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
            "vpc": {"bg": "#1a1a2a", "fc": "#c4b5fd", "border": "#6741d9"},
            "col": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "pub": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "priv": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
        }
    else:
        cc = {
            "vpc": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
            "col": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "pub": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
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
        "label": "Route Tables\n\n",
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

    out_path = os.path.join(OUT_DIR, f"{DIAGRAM_NAME}{suffix}")
    png_path = out_path + ".png"

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
        user = User("Internet")
        igw = InternetGateway("Internet\nGateway")

        def e(**kw):
            return Edge(color=edge_color, **kw)

        with Cluster("VPC  (10.0.0.0/16)", graph_attr=cattr("vpc")):
            router = VPCRouter("VPC\nRouter")

            with Cluster("0.0.0.0/0 \u2192 IGW  (Direct)", graph_attr=cattr("col")):
                with Cluster("Public Subnet  (10.0.1.0/24)", graph_attr=cattr("pub")):
                    ec2_pub = EC2("EC2")
                    rt_pub = RouteTable("Route\nTable")
                    nat = NATGateway("NAT\nGateway")

            with Cluster("0.0.0.0/0 \u2192 NAT  (Indirect)", graph_attr=cattr("col")):
                with Cluster("Private Subnet  (10.0.2.0/24)", graph_attr=cattr("priv")):
                    ec2_priv = EC2("EC2")
                    rt_priv = RouteTable("Route\nTable")
                    rds = RDS("RDS")

        # Top flow: Internet → IGW → VPC Router
        user >> e() >> igw
        igw >> e(lhead="cluster_VPC  (10.0.0.0/16)", minlen="2") >> router

        # VPC Router fans out to both columns (forces side-by-side layout)
        router >> e(lhead="cluster_0.0.0.0/0 \u2192 IGW  (Direct)") >> ec2_pub
        router >> e(lhead="cluster_0.0.0.0/0 \u2192 NAT  (Indirect)") >> ec2_priv

        # Public subnet: EC2 → Route Table, Route Table manages NAT Gateway
        ec2_pub >> e() >> rt_pub
        rt_pub >> e() >> nat

        # Private subnet: EC2 → Route Table, EC2 → RDS
        ec2_priv >> e() >> rt_priv
        ec2_priv >> e() >> rds

        dot_source = d.dot.source
        top_ids = [user._id, igw._id, router._id]

    render_centered(dot_source, png_path, top_ids)
    print(f"  Centered {len(top_ids)} nodes in {png_path}")


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
