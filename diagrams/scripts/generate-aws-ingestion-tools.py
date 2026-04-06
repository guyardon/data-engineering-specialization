#!/usr/bin/env python3
"""Generate AWS Data Ingestion Tools diagram using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import (
    Glue,
    EMR,
    KinesisDataStreams,
    ManagedStreamingForKafka,
)
from diagrams.aws.database import DatabaseMigrationService
from diagrams.aws.migration import Snowball, TransferForSftp

from diagramlib.aws_diagram import (
    cluster_attrs,
    edge_attrs,
    graph_attrs,
    node_attrs,
    output_dir,
)

OUT_DIR = output_dir()
DIAGRAM_NAME = "aws-ingestion-tools"


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    # Custom graph attrs: tighter spacing for this grid layout
    ga = graph_attrs(dark=dark, title="AWS Data Ingestion Tools")
    ga["nodesep"] = "0.5"
    ga["ranksep"] = "0.5"

    out_path = f"{OUT_DIR}/{DIAGRAM_NAME}{suffix}"

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="TB",
        graph_attr=ga,
        node_attr=node_attrs(dark),
        edge_attr=edge_attrs(dark),
        outformat="png",
    ):
        with Cluster("ETL & Processing", graph_attr=cluster_attrs("blue", dark=dark)):
            Glue("Glue ETL")
            emr = EMR("EMR")

        with Cluster("Data Migration", graph_attr=cluster_attrs("green", dark=dark)):
            dms = DatabaseMigrationService("DMS")

        with Cluster("Streaming", graph_attr=cluster_attrs("yellow", dark=dark)):
            KinesisDataStreams("Kinesis\nData Streams")
            msk = ManagedStreamingForKafka("MSK")

        with Cluster(
            "Physical & File Transfer", graph_attr=cluster_attrs("purple", dark=dark)
        ):
            Snowball("Snow Family")
            transfer = TransferForSftp("Transfer Family")

        # Invisible edges to align clusters horizontally
        emr >> Edge(style="invis") >> dms
        dms >> Edge(style="invis") >> msk
        msk >> Edge(style="invis") >> transfer


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
