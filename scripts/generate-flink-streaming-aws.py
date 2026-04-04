# pyright: reportArgumentType=false
"""Generate AWS streaming pipeline diagram with Kinesis → Managed Flink → S3/Redshift."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataAnalytics, GlueCrawlers
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images", "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)

DIAGRAM_NAME = "flink-streaming-aws"


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    edge_color = "#65656e" if dark else "#495057"

    if dark:
        cc = {
            "purple": {"bg": "#1a1a2a", "fc": "#c4b5fd", "border": "#6741d9"},
            "green":  {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "yellow": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "blue":   {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "cyan":   {"bg": "#1a2a2a", "fc": "#67e8f9", "border": "#0c8599"},
        }
    else:
        cc = {
            "purple": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
            "green":  {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "yellow": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "blue":   {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "cyan":   {"bg": "#99e9f240", "fc": "#0c8599", "border": "#0c8599"},
        }

    graph_attr = {
        "bgcolor": bg,
        "fontcolor": fc,
        "fontsize": "18",
        "fontname": "Helvetica Bold",
        "pad": "0.3",
        "nodesep": "0.3",
        "ranksep": "1.2",
        "dpi": "150",
        "label": "AWS Streaming Pipeline with Apache Flink\n\n",
        "labelloc": "t",
        "rankdir": "LR",
        "compound": "true",
    }

    node_attr = {
        "fontsize": "12",
        "fontname": "Helvetica",
        "fontcolor": fc,
        "height": "1.1",
    }

    edge_attr = {
        "color": edge_color,
        "penwidth": "2.0",
    }

    def cattr(key):
        c = cc[key]
        return {
            "fontsize": "14",
            "fontname": "Helvetica Bold",
            "penwidth": "1.5",
            "labeljust": "c",
            "labelloc": "t",
            "style": "dashed,rounded",
            "margin": "14",
            "bgcolor": c["bg"],
            "fontcolor": c["fc"],
            "pencolor": c["border"],
        }

    out_path = os.path.join(OUT_DIR, f"{DIAGRAM_NAME}{suffix}")

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat="png",
    ):
        e = lambda **kw: Edge(color=edge_color, **kw)

        # Ingestion
        with Cluster("Ingestion", graph_attr=cattr("blue")):
            kinesis = KinesisDataStreams("Kinesis\nData Streams")

        # Processing
        with Cluster("Processing", graph_attr=cattr("yellow")):
            flink = KinesisDataAnalytics("Managed\nApache Flink")

        # Destinations
        with Cluster("Destinations", graph_attr=cattr("green")):
            s3 = S3("S3")
            redshift = Redshift("Redshift")

        # Alerting
        with Cluster("Alerting", graph_attr=cattr("purple")):
            sns = SNS("SNS")

        # Flow
        kinesis >> e(lhead="cluster_Processing", ltail="cluster_Ingestion") >> flink
        flink >> e(lhead="cluster_Destinations", ltail="cluster_Processing") >> s3
        flink >> e(lhead="cluster_Destinations", ltail="cluster_Processing") >> redshift
        flink >> e(lhead="cluster_Alerting", ltail="cluster_Processing", style="dashed") >> sns


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
