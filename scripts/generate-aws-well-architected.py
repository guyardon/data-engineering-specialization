#!/usr/bin/env python3
"""Generate AWS Well-Architected Framework diagram (light + dark) using diagrams library."""

import os

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.cost import CostAndUsageReport
from diagrams.aws.general import General
from diagrams.aws.management import Cloudwatch, WellArchitectedTool
from diagrams.aws.security import Shield
from diagrams.aws.storage import S3

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public",
    "images",
    "diagrams",
)
os.makedirs(OUT_DIR, exist_ok=True)


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    edge_color = "#65656e" if dark else "#495057"

    # Cluster colors
    if dark:
        cluster_colors = {
            "ops": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "sec": {"bg": "#2a1a1a", "fc": "#fca5a5", "border": "#c92a2a"},
            "rel": {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "perf": {"bg": "#2a1a2a", "fc": "#d8b4fe", "border": "#6741d9"},
            "cost": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "sust": {"bg": "#1a2a2a", "fc": "#67e8f9", "border": "#0c8599"},
        }
    else:
        cluster_colors = {
            "ops": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "sec": {"bg": "#ffc9c940", "fc": "#c92a2a", "border": "#c92a2a"},
            "rel": {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "perf": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
            "cost": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "sust": {"bg": "#99e9f240", "fc": "#0c8599", "border": "#0c8599"},
        }

    graph_attr = {
        "bgcolor": bg,
        "fontcolor": fc,
        "fontsize": "28",
        "fontname": "Helvetica Bold",
        "pad": "0.6",
        "nodesep": "1.0",
        "ranksep": "1.4",
        "dpi": "150",
        "label": "AWS Well-Architected Framework",
        "labelloc": "t",
        "compound": "true",
    }
    node_attr = {
        "fontsize": "18",
        "fontname": "Helvetica",
        "fontcolor": fc,
    }
    edge_attr = {
        "color": edge_color,
        "penwidth": "2.0",
    }

    cluster_common = {
        "fontsize": "22",
        "fontname": "Helvetica Bold",
        "penwidth": "2.0",
        "labeljust": "c",
        "style": "rounded",
        "margin": "20",
    }

    out_path = os.path.join(OUT_DIR, f"aws-well-architected{suffix}")

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat="png",
    ):
        center = WellArchitectedTool("\nWell-Architected\nFramework")

        def pillar_cluster(key, label, NodeClass, node_label):
            c = cluster_colors[key]
            attrs = {
                **cluster_common,
                "bgcolor": c["bg"],
                "fontcolor": c["fc"],
                "pencolor": c["border"],
            }
            with Cluster(label, graph_attr=attrs):
                node = NodeClass(node_label)
            return node

        ops = pillar_cluster(
            "ops", "Operational\nExcellence", Cloudwatch, "\nMonitor &\nImprove"
        )
        sec = pillar_cluster("sec", "Security", Shield, "\nProtect Data\n& Systems")
        rel = pillar_cluster("rel", "Reliability", S3, "\nPlan for\nFailure")
        perf = pillar_cluster(
            "perf", "Performance\nEfficiency", Lambda, "\nRight-size\nResources"
        )
        cost = pillar_cluster(
            "cost", "Cost\nOptimization", CostAndUsageReport, "\nMaximize\nValue"
        )
        sust = pillar_cluster("sust", "Sustainability", General, "\nMinimize\nImpact")

        # Use lhead to stop arrows at cluster borders instead of going inside
        center >> Edge(color=edge_color, lhead="cluster_Operational\nExcellence") >> ops
        center >> Edge(color=edge_color, lhead="cluster_Security") >> sec
        center >> Edge(color=edge_color, lhead="cluster_Reliability") >> rel
        (
            center
            >> Edge(color=edge_color, lhead="cluster_Performance\nEfficiency")
            >> perf
        )
        center >> Edge(color=edge_color, lhead="cluster_Cost\nOptimization") >> cost
        center >> Edge(color=edge_color, lhead="cluster_Sustainability") >> sust


gen(dark=False)
gen(dark=True)
print("Done — generated light and dark AWS Well-Architected diagrams")
