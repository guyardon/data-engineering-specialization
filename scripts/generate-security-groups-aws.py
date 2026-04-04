#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB
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

DIAGRAM_NAME = "security-groups-aws"


def render_centered(dot_source, png_path, node_ids):
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
            "alb_sg": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "ec2_sg": {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "rds_sg": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
        }
    else:
        cc = {
            "vpc": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
            "alb_sg": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "ec2_sg": {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "rds_sg": {"bg": "#ffc9c940", "fc": "#c92a2a", "border": "#c92a2a"},
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
        "label": "Security Groups\n\n",
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
        user = User("Internet\n(0.0.0.0/0)")

        def e(**kw):
            return Edge(color=edge_color, **kw)

        with Cluster("VPC", graph_attr=cattr("vpc")):
            with Cluster(
                "ALB Security Group\nInbound: HTTP/HTTPS from 0.0.0.0/0",
                graph_attr=cattr("alb_sg"),
            ):
                alb = ALB("ALB")

            with Cluster(
                "EC2 Security Group\nInbound: from ALB SG", graph_attr=cattr("ec2_sg")
            ):
                ec2 = EC2("EC2")

            with Cluster(
                "RDS Security Group\nInbound: from EC2 SG", graph_attr=cattr("rds_sg")
            ):
                rds = RDS("RDS")

        # Security group chain
        (
            user
            >> e(
                lhead="cluster_VPC",
                label="HTTP/HTTPS\n(80, 443)",
                fontsize="16",
                fontname="Helvetica",
                fontcolor=fc,
            )
            >> alb
        )
        (
            alb
            >> e(
                label="Source: ALB SG",
                fontsize="16",
                fontname="Helvetica",
                fontcolor=fc,
            )
            >> ec2
        )
        (
            ec2
            >> e(
                label="Source: EC2 SG",
                fontsize="16",
                fontname="Helvetica",
                fontcolor=fc,
            )
            >> rds
        )

        dot_source = d.dot.source
        top_ids = [user._id]

    render_centered(dot_source, png_path, top_ids)


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
