#!/usr/bin/env python3
"""Generate AWS Streaming Pipeline diagram (light + dark) using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataFirehose, ManagedStreamingForKafka
from diagrams.aws.storage import S3
from diagrams.aws.general import General
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images", "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    edge_color = "#65656e" if dark else "#495057"

    if dark:
        cc = {
            "producers": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "ingest":    {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "deliver":   {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "store":     {"bg": "#2a1a2a", "fc": "#d8b4fe", "border": "#6741d9"},
        }
    else:
        cc = {
            "producers": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "ingest":    {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "deliver":   {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "store":     {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
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
        "label": "AWS Streaming Pipeline\n\n",
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

    out_path = os.path.join(OUT_DIR, f"streaming-pipeline-aws{suffix}")

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
        with Cluster("Producers", graph_attr=cattr("producers")):
            producers = General("Event\nSources")

        with Cluster("Stream Ingestion", graph_attr=cattr("ingest")):
            kinesis = KinesisDataStreams("Kinesis")
            msk = ManagedStreamingForKafka("MSK")

        with Cluster("Delivery", graph_attr=cattr("deliver")):
            firehose = KinesisDataFirehose("Firehose")

        with Cluster("Storage", graph_attr=cattr("store")):
            s3 = S3("S3")

        e = lambda **kw: Edge(color=edge_color, **kw)

        producers >> e(lhead="cluster_Stream Ingestion", ltail="cluster_Producers") >> kinesis
        producers >> e(lhead="cluster_Stream Ingestion", ltail="cluster_Producers") >> msk
        kinesis >> e(lhead="cluster_Delivery", ltail="cluster_Stream Ingestion") >> firehose
        firehose >> e(lhead="cluster_Storage", ltail="cluster_Delivery") >> s3
        msk >> e(lhead="cluster_Storage", ltail="cluster_Stream Ingestion") >> s3


gen(dark=False)
gen(dark=True)
print("Done — generated light and dark streaming pipeline AWS diagrams")
