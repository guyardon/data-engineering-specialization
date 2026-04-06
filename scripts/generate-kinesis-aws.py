#!/usr/bin/env python3
# pyright: reportArgumentType=false
"""Generate Kinesis Data Streams architecture diagram (light + dark) using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import (
    KinesisDataStreams,
    KinesisDataFirehose,
    KinesisDataAnalytics,
    Glue,
)
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.general import General

from diagramlib.aws_diagram import (
    cluster_attrs,
    edge_attrs,
    graph_attrs,
    node_attrs,
    output_dir,
)

OUT_DIR = output_dir()


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    edge_color = edge_attrs(dark)["color"]

    out_path = f"{OUT_DIR}/kinesis-data-streams-aws{suffix}"

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attrs(dark=dark, title="Kinesis Data Streams"),
        node_attr=node_attrs(dark),
        edge_attr=edge_attrs(dark),
        outformat="png",
    ):
        with Cluster("Producers", graph_attr=cluster_attrs("green", dark=dark)):
            producers = General("Event\nSources")

        with Cluster("Stream Ingestion", graph_attr=cluster_attrs("blue", dark=dark)):
            kinesis = KinesisDataStreams("Kinesis Data\nStreams")

        with Cluster("Consumers", graph_attr=cluster_attrs("cyan", dark=dark)):
            lam = Lambda("Lambda")
            glue = Glue("Glue")
            flink = KinesisDataAnalytics("Managed\nFlink")

        with Cluster("Delivery", graph_attr=cluster_attrs("yellow", dark=dark)):
            firehose = KinesisDataFirehose("Firehose")

        with Cluster("Storage", graph_attr=cluster_attrs("purple", dark=dark)):
            s3 = S3("S3")

        def e(**kw):
            return Edge(color=edge_color, **kw)

        # Producers -> Kinesis
        (
            producers
            >> e(lhead="cluster_Stream Ingestion", ltail="cluster_Producers")
            >> kinesis
        )

        # Kinesis -> Consumers
        (
            kinesis
            >> e(lhead="cluster_Consumers", ltail="cluster_Stream Ingestion")
            >> lam
        )
        (
            kinesis
            >> e(lhead="cluster_Consumers", ltail="cluster_Stream Ingestion")
            >> glue
        )
        (
            kinesis
            >> e(lhead="cluster_Consumers", ltail="cluster_Stream Ingestion")
            >> flink
        )

        # Kinesis -> Firehose -> S3
        (
            kinesis
            >> e(lhead="cluster_Delivery", ltail="cluster_Stream Ingestion")
            >> firehose
        )
        firehose >> e(lhead="cluster_Storage", ltail="cluster_Delivery") >> s3


gen(dark=False)
gen(dark=True)
print("Done — generated light and dark Kinesis Data Streams AWS diagrams")
