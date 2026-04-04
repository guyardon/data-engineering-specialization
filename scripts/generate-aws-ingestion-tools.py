#!/usr/bin/env python3
"""Generate AWS Data Ingestion Tools diagram using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Glue, EMR, KinesisDataStreams, ManagedStreamingForKafka
from diagrams.aws.database import DatabaseMigrationService
from diagrams.aws.migration import Snowball, TransferForSftp
from diagrams.aws.storage import S3
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public",
    "images",
    "diagrams",
)
os.makedirs(OUT_DIR, exist_ok=True)

DIAGRAM_NAME = "aws-ingestion-tools"


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    bg = "#0f0f13" if dark else "white"
    fc = "#e8e8ea" if dark else "#1e1e1e"
    edge_color = "#65656e" if dark else "#495057"

    if dark:
        cc = {
            "etl": {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "migration": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "streaming": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "transfer": {"bg": "#2a1a2a", "fc": "#d8b4fe", "border": "#6741d9"},
        }
    else:
        cc = {
            "etl": {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "migration": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "streaming": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "transfer": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
        }

    graph_attr = {
        "bgcolor": bg,
        "fontcolor": fc,
        "fontsize": "18",
        "fontname": "Helvetica Bold",
        "pad": "0.3",
        "nodesep": "0.5",
        "ranksep": "0.5",
        "dpi": "150",
        "label": "AWS Data Ingestion Tools\n\n",
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
        direction="TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        outformat="png",
    ):
        with Cluster("ETL & Processing", graph_attr=cattr("etl")):
            glue = Glue("Glue ETL")
            emr = EMR("EMR")

        with Cluster("Data Migration", graph_attr=cattr("migration")):
            dms = DatabaseMigrationService("DMS")

        with Cluster("Streaming", graph_attr=cattr("streaming")):
            kinesis = KinesisDataStreams("Kinesis\nData Streams")
            msk = ManagedStreamingForKafka("MSK")

        with Cluster("Physical & File Transfer", graph_attr=cattr("transfer")):
            snow = Snowball("Snow Family")
            transfer = TransferForSftp("Transfer Family")

        # Invisible edges to align clusters horizontally
        emr >> Edge(style="invis") >> dms
        dms >> Edge(style="invis") >> msk
        msk >> Edge(style="invis") >> transfer


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
