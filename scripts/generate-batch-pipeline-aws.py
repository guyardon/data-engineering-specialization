#!/usr/bin/env python3
# pyright: reportArgumentType=false
"""Generate AWS Batch ETL Pipeline diagram (light + dark) using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.database import RDS, Redshift
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.analytics import EMR, Glue
from diagrams.aws.storage import S3

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

    out_path = f"{OUT_DIR}/batch-pipeline-aws{suffix}"

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attrs(dark=dark, title="AWS Batch ETL Pipeline"),
        node_attr=node_attrs(dark),
        edge_attr=edge_attrs(dark),
        outformat="png",
    ):
        with Cluster("Source", graph_attr=cluster_attrs("green", dark=dark)):
            source = RDS("RDS")

        with Cluster("Extract", graph_attr=cluster_attrs("blue", dark=dark)):
            lam = Lambda("Lambda")
            ec2 = EC2("EC2")

        with Cluster("Transform", graph_attr=cluster_attrs("yellow", dark=dark)):
            glue = Glue("Glue ETL")
            emr = EMR("EMR")

        with Cluster("Load / Serve", graph_attr=cluster_attrs("purple", dark=dark)):
            rds_out = RDS("RDS")
            redshift = Redshift("Redshift")
            s3 = S3("S3")

        def e(**kw):
            return Edge(color=edge_color, **kw)

        source >> e(lhead="cluster_Extract", ltail="cluster_Source") >> lam
        source >> e(lhead="cluster_Extract", ltail="cluster_Source") >> ec2
        lam >> e(lhead="cluster_Transform", ltail="cluster_Extract") >> glue
        ec2 >> e(lhead="cluster_Transform", ltail="cluster_Extract") >> emr
        glue >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> rds_out
        glue >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> redshift
        glue >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> s3
        emr >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> rds_out
        emr >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> redshift
        emr >> e(lhead="cluster_Load / Serve", ltail="cluster_Transform") >> s3


gen(dark=False)
gen(dark=True)
print("Done — generated light and dark batch pipeline AWS diagrams")
