#!/usr/bin/env python3
"""Generate AWS Batch ETL Pipeline diagram (light + dark) using diagrams library."""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.database import RDS, Redshift
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.analytics import EMR, Glue
from diagrams.aws.storage import S3
import os

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

    if dark:
        cc = {
            "source": {"bg": "#1a2a1a", "fc": "#86efac", "border": "#2f9e44"},
            "extract": {"bg": "#1a1a2a", "fc": "#93c5fd", "border": "#1971c2"},
            "transform": {"bg": "#2a2a1a", "fc": "#fde68a", "border": "#e67700"},
            "load": {"bg": "#2a1a2a", "fc": "#d8b4fe", "border": "#6741d9"},
        }
    else:
        cc = {
            "source": {"bg": "#b2f2bb40", "fc": "#2f9e44", "border": "#2f9e44"},
            "extract": {"bg": "#a5d8ff40", "fc": "#1971c2", "border": "#1971c2"},
            "transform": {"bg": "#ffec9940", "fc": "#e67700", "border": "#e67700"},
            "load": {"bg": "#d0bfff40", "fc": "#6741d9", "border": "#6741d9"},
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
        "label": "AWS Batch ETL Pipeline\n\n",
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

    out_path = os.path.join(OUT_DIR, f"batch-pipeline-aws{suffix}")

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
        with Cluster("Source", graph_attr=cattr("source")):
            source = RDS("RDS")

        with Cluster("Extract", graph_attr=cattr("extract")):
            lam = Lambda("Lambda")
            ec2 = EC2("EC2")

        with Cluster("Transform", graph_attr=cattr("transform")):
            glue = Glue("Glue ETL")
            emr = EMR("EMR")

        with Cluster("Load / Serve", graph_attr=cattr("load")):
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
