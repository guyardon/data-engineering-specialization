# pyright: reportArgumentType=false
"""Generate AWS streaming pipeline diagram with Kinesis -> Managed Flink -> S3/Redshift."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataAnalytics
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS

from diagramlib.aws_diagram import (
    cluster_attrs,
    edge_attrs,
    graph_attrs,
    node_attrs,
    output_dir,
)

OUT_DIR = output_dir()
DIAGRAM_NAME = "flink-streaming-aws"


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    edge_color = edge_attrs(dark)["color"]

    out_path = f"{OUT_DIR}/{DIAGRAM_NAME}{suffix}"

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attrs(
            dark=dark, title="AWS Streaming Pipeline with Apache Flink"
        ),
        node_attr=node_attrs(dark),
        edge_attr=edge_attrs(dark),
        outformat="png",
    ):
        e = lambda **kw: Edge(color=edge_color, **kw)

        # Ingestion
        with Cluster("Ingestion", graph_attr=cluster_attrs("blue", dark=dark)):
            kinesis = KinesisDataStreams("Kinesis\nData Streams")

        # Processing
        with Cluster("Processing", graph_attr=cluster_attrs("yellow", dark=dark)):
            flink = KinesisDataAnalytics("Managed\nApache Flink")

        # Destinations
        with Cluster("Destinations", graph_attr=cluster_attrs("green", dark=dark)):
            s3 = S3("S3")
            redshift = Redshift("Redshift")

        # Alerting
        with Cluster("Alerting", graph_attr=cluster_attrs("purple", dark=dark)):
            sns = SNS("SNS")

        # Flow
        kinesis >> e(lhead="cluster_Processing", ltail="cluster_Ingestion") >> flink
        flink >> e(lhead="cluster_Destinations", ltail="cluster_Processing") >> s3
        flink >> e(lhead="cluster_Destinations", ltail="cluster_Processing") >> redshift
        (
            flink
            >> e(lhead="cluster_Alerting", ltail="cluster_Processing", style="dashed")
            >> sns
        )


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
