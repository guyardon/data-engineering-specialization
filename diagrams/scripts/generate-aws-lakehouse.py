# pyright: reportArgumentType=false
"""Generate AWS Data Lakehouse architecture diagram showing the three-layer
implementation: storage (S3 + Redshift), catalog (Lake Formation + Glue),
and consumption (Athena + Redshift Spectrum).
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Athena, LakeFormation, GlueCrawlers
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3

from diagramlib.aws_diagram import (
    cluster_attrs,
    edge_attrs,
    graph_attrs,
    node_attrs,
    output_dir,
)

OUT_DIR = output_dir()
DIAGRAM_NAME = "aws-lakehouse"


def gen(dark: bool):
    suffix = "-dark" if dark else ""
    edge_color = edge_attrs(dark)["color"]

    out_path = f"{OUT_DIR}/{DIAGRAM_NAME}{suffix}"

    with Diagram(
        "",
        filename=out_path,
        show=False,
        direction="LR",
        graph_attr=graph_attrs(dark=dark, title="AWS Data Lakehouse Architecture"),
        node_attr=node_attrs(dark),
        edge_attr=edge_attrs(dark),
        outformat="png",
    ):
        e = lambda **kw: Edge(color=edge_color, **kw)

        # Storage layer
        with Cluster("Storage Layer", graph_attr=cluster_attrs("blue", dark=dark)):
            s3 = S3("S3")
            redshift = Redshift("Redshift")

        # Catalog layer
        with Cluster("Catalog Layer", graph_attr=cluster_attrs("yellow", dark=dark)):
            lake_formation = LakeFormation("Lake Formation")
            glue_crawlers = GlueCrawlers("Glue Crawlers")

        # Consumption layer
        with Cluster("Consumption Layer", graph_attr=cluster_attrs("green", dark=dark)):
            athena = Athena("Athena")
            spectrum = Redshift("Redshift\nSpectrum")

        # Edges: storage to catalog
        (
            s3
            >> e(lhead="cluster_Catalog Layer", ltail="cluster_Storage Layer")
            >> glue_crawlers
        )
        glue_crawlers >> e() >> lake_formation

        # Edges: catalog to consumption
        (
            lake_formation
            >> e(lhead="cluster_Consumption Layer", ltail="cluster_Catalog Layer")
            >> athena
        )

        # Cross-layer queries
        (
            athena
            >> e(
                ltail="cluster_Consumption Layer",
                lhead="cluster_Storage Layer",
                style="dashed",
            )
            >> s3
        )
        (
            spectrum
            >> e(
                ltail="cluster_Consumption Layer",
                lhead="cluster_Storage Layer",
                style="dashed",
            )
            >> redshift
        )


gen(dark=False)
gen(dark=True)
print(f"Done — generated light and dark {DIAGRAM_NAME} diagrams")
