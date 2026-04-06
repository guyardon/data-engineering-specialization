/**
 * Detail card builder for the glossary page.
 * Builds the DOM content for a term's detail view.
 * State mutations are delegated to callbacks (DIP).
 */

import {
  findTermByName,
  type GlossaryCategory,
  type GlossaryTerm,
  type TermEntry,
} from "./glossary-data";

/** Maps glossary term names to logo file slugs in public/images/logos/. */
const TERM_LOGO_MAP: Record<string, string> = {
  "AWS CloudFormation": "cloudformation",
  "AWS DMS": "dms",
  "AWS Glue": "glue",
  "AWS IAM": "iam",
  "AWS Lake Formation": "lakeformation",
  "AWS Lambda": "lambda",
  Airbyte: "airbyte",
  "Amazon Athena": "athena",
  "Amazon CloudWatch": "cloudwatch",
  "Amazon Data Firehose": "firehose",
  "Amazon DynamoDB": "dynamodb",
  "Amazon EBS": "ebs",
  "Amazon EC2": "ec2",
  "Amazon EFS": "efs",
  "Amazon EMR": "emr",
  "Amazon Kinesis Data Streams": "kinesis",
  "Amazon MSK": "msk",
  "Amazon MWAA": "mwaa",
  "Amazon Neptune": "neptune",
  "Amazon QuickSight": "quicksight",
  "Amazon RDS": "rds",
  "Amazon Redshift": "redshift",
  "Amazon S3": "s3",
  "Amazon SQS": "sqs",
  "Amazon SageMaker": "sagemaker",
  "Amazon VPC": "vpc",
  "Apache Airflow": "airflow",
  "Apache Avro": "avro",
  "Apache Flink": "flink",
  "Apache Hadoop": "hadoop",
  "Apache Iceberg": "iceberg",
  "Apache Kafka": "kafka",
  "Apache Parquet": "parquet-text",
  "Apache Spark": "spark",
  Boto3: "boto3",
  CSV: "csv",
  Cassandra: "cassandra",
  Dagster: "dagster-text",
  Debezium: "debezium",
  Databricks: "databricks-text",
  "Delta Lake": "delta-lake",
  Fivetran: "fivetran",
  "Glue Data Catalog": "glue",
  "Google BigQuery": "bigquery",
  "Apache Hudi": "hudi.png",
  "Great Expectations": "great-expectations-text",
  HDFS: "hdfs",
  JSON: "json",
  Mage: "mage",
  MapReduce: "hadoop",
  Memcached: "memcached",
  Metabase: "metabase",
  MySQL: "mysql",
  Neo4j: "neo4j",
  Oracle: "oracle",
  PostgreSQL: "postgresql-text",
  Prefect: "prefect-text",
  PySpark: "pyspark",
  Redis: "redis",
  "Redshift Spectrum": "redshift",
  SQL: "sql",
  "Spark DataFrames": "spark",
  Snowflake: "snowflake",
  "Spark Structured Streaming": "spark",
  Terraform: "terraform",
  XML: "xml",
  dbt: "dbt",
};

export interface DetailCallbacks {
  onRelatedTermClick: (entry: TermEntry) => void;
  onShuffleClick: () => void;
  onDiagramClick: (lightSrc: string, darkSrc: string, alt: string) => void;
}

/** Build detail card contents into target element. */
export function buildDetailCard(
  target: HTMLElement,
  term: GlossaryTerm,
  data: GlossaryCategory[],
  basePath: string,
  callbacks: DetailCallbacks,
): void {
  // Clear existing content
  while (target.firstChild) target.removeChild(target.firstChild);

  // Title — use logo as title when available, fall back to text
  const logoSlug = TERM_LOGO_MAP[term.term];
  if (logoSlug) {
    const logoWrap = document.createElement("div");
    logoWrap.className = "detail-logo-title";
    const isPng = logoSlug.endsWith(".png");

    if (isPng) {
      const baseName = logoSlug.replace(".png", "");
      const src = basePath + "/images/logos/" + baseName + ".png";
      const lightImg = document.createElement("img");
      lightImg.src = src;
      lightImg.alt = term.term;
      lightImg.className = "logo-light";
      logoWrap.appendChild(lightImg);

      const darkImg = document.createElement("img");
      darkImg.src = src;
      darkImg.alt = term.term;
      darkImg.className = "logo-dark";
      darkImg.style.filter = "brightness(1.6)";
      logoWrap.appendChild(darkImg);
    } else {
      const lightImg = document.createElement("img");
      lightImg.src = basePath + "/images/logos/" + logoSlug + ".svg";
      lightImg.alt = term.term;
      lightImg.className = "logo-light";
      logoWrap.appendChild(lightImg);

      const darkImg = document.createElement("img");
      darkImg.src = basePath + "/images/logos/" + logoSlug + "-dark.svg";
      darkImg.alt = term.term;
      darkImg.className = "logo-dark";
      logoWrap.appendChild(darkImg);
    }

    target.appendChild(logoWrap);
  } else {
    const title = document.createElement("h3");
    title.className = "detail-title";
    title.textContent = term.term;
    target.appendChild(title);
  }

  // Description
  if (term.description) {
    const desc = document.createElement("p");
    desc.className = "detail-desc";
    desc.textContent = term.description;
    target.appendChild(desc);
  }

  // Diagram
  if (term.diagram) {
    const isPng = term.diagram.endsWith(".png");
    const baseName = isPng ? term.diagram.replace(".png", "") : term.diagram;
    const ext = isPng ? "png" : "svg";

    const lightSrc = basePath + "/images/diagrams/" + baseName + "." + ext;
    const darkSrc = basePath + "/images/diagrams/" + baseName + "-dark." + ext;

    const diagramWrap = document.createElement("div");
    diagramWrap.className = "detail-diagram detail-diagram-clickable";
    diagramWrap.style.cursor = "pointer";
    diagramWrap.addEventListener("click", () => {
      callbacks.onDiagramClick(lightSrc, darkSrc, term.term);
    });

    const imgLight = document.createElement("img");
    imgLight.src = lightSrc;
    imgLight.alt = term.term;
    imgLight.className = "diagram diagram-light";
    diagramWrap.appendChild(imgLight);

    const imgDark = document.createElement("img");
    imgDark.src = darkSrc;
    imgDark.alt = term.term;
    imgDark.className = "diagram diagram-dark";
    diagramWrap.appendChild(imgDark);

    target.appendChild(diagramWrap);
  }

  // See more links
  const seeMore = document.createElement("div");
  seeMore.className = "detail-see-more";

  const label = document.createElement("span");
  label.className = "detail-label";
  label.textContent = "See more at:";
  seeMore.appendChild(label);

  const links = document.createElement("div");
  links.className = "detail-links";
  term.notes.forEach((ref) => {
    const a = document.createElement("a");
    a.href = ref.href;
    a.className = "pill note-card";
    a.textContent = ref.title;
    links.appendChild(a);
  });
  seeMore.appendChild(links);
  target.appendChild(seeMore);

  // Related terms
  if (term.relatedTerms && term.relatedTerms.length > 0) {
    const relatedSection = document.createElement("div");
    relatedSection.className = "detail-related";

    const relatedLabel = document.createElement("span");
    relatedLabel.className = "detail-label";
    relatedLabel.textContent = "Related terms:";
    relatedSection.appendChild(relatedLabel);

    const relatedLinks = document.createElement("div");
    relatedLinks.className = "detail-links";
    term.relatedTerms.forEach((relatedName) => {
      const found = findTermByName(data, relatedName);
      if (!found) return;

      const btn = document.createElement("button");
      btn.className = "pill related-term-pill";
      btn.textContent = relatedName;
      btn.addEventListener("click", () => {
        callbacks.onRelatedTermClick(found);
      });
      relatedLinks.appendChild(btn);
    });
    relatedSection.appendChild(relatedLinks);
    target.appendChild(relatedSection);
  }

  // Shuffle button
  const shuffleWrap = document.createElement("div");
  shuffleWrap.className = "detail-shuffle";

  const shuffleBtn = document.createElement("button");
  shuffleBtn.className = "pill shuffle-btn";
  shuffleBtn.setAttribute("aria-label", "Random term");

  const shuffleSvg = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "svg",
  );
  shuffleSvg.setAttribute("width", "14");
  shuffleSvg.setAttribute("height", "14");
  shuffleSvg.setAttribute("viewBox", "0 0 24 24");
  shuffleSvg.setAttribute("fill", "none");
  shuffleSvg.setAttribute("stroke", "currentColor");
  shuffleSvg.setAttribute("stroke-width", "2");
  shuffleSvg.setAttribute("stroke-linecap", "round");
  shuffleSvg.setAttribute("stroke-linejoin", "round");

  const p1 = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
  p1.setAttribute("points", "16 3 21 3 21 8");
  shuffleSvg.appendChild(p1);

  const l1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  l1.setAttribute("x1", "4");
  l1.setAttribute("y1", "20");
  l1.setAttribute("x2", "21");
  l1.setAttribute("y2", "3");
  shuffleSvg.appendChild(l1);

  const p2 = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
  p2.setAttribute("points", "21 16 21 21 16 21");
  shuffleSvg.appendChild(p2);

  const l2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  l2.setAttribute("x1", "15");
  l2.setAttribute("y1", "15");
  l2.setAttribute("x2", "21");
  l2.setAttribute("y2", "21");
  shuffleSvg.appendChild(l2);

  const l3 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  l3.setAttribute("x1", "4");
  l3.setAttribute("y1", "4");
  l3.setAttribute("x2", "9");
  l3.setAttribute("y2", "9");
  shuffleSvg.appendChild(l3);

  shuffleBtn.appendChild(shuffleSvg);
  const shuffleText = document.createElement("span");
  shuffleText.textContent = "Shuffle";
  shuffleBtn.appendChild(shuffleText);

  shuffleBtn.addEventListener("click", () => {
    callbacks.onShuffleClick();
  });

  shuffleWrap.appendChild(shuffleBtn);
  target.appendChild(shuffleWrap);
}
