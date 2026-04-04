#!/usr/bin/env python3
# pyright: reportArgumentType=false
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ALB, NATGateway, InternetGateway
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

DIAGRAM_NAME = "internet-connectivity-aws"


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
            "pub": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "priv": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
        }
    else:
        cc = {
            "vpc": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
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
        "label": "Internet Connectivity\n\n",
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
    edge_attr = {"color": edge_color, "penwidth": "3.0"}

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
        user = User("User")
        igw = InternetGateway("Internet\nGateway")

        def e(**kw):
            return Edge(color=edge_color, **kw)

        with Cluster("VPC", graph_attr=cattr("vpc")):
            with Cluster("Public Subnet", graph_attr=cattr("pub")):
                alb = ALB("ALB")
                nat = NATGateway("NAT\nGateway")
            with Cluster("Private Subnet", graph_attr=cattr("priv")):
                ec2 = EC2("EC2")

        # Inbound flow
        user >> e() >> igw >> e(lhead="cluster_VPC", minlen="2") >> alb
        alb >> e(lhead="cluster_Private Subnet") >> ec2
        # Outbound flow from private
        ec2 >> e(lhead="cluster_Public Subnet", style="dashed") >> nat
        nat >> e(style="dashed") >> igw

        dot_source = d.dot.source
        top_ids = [user._id, igw._id]

    render_centered(dot_source, png_path, top_ids)


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
