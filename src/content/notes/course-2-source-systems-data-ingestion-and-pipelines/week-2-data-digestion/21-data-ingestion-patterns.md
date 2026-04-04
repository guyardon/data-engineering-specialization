---
title: "2.1 Data Ingestion Patterns"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 1
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

Data ingestion is the process of acquiring raw data from various sources. This section covers different ingestion patterns, batch and streaming requirements, and key AWS tools for data ingestion.

## 1.1.1 Data Ingestion on a Continuum

Data ingestion isn't a binary choice between batch and streaming -- it exists on a continuum determined by how you bound your data.

**Unbounded vs. Bounded Data**

- **Unbounded Data:** Continuous stream of events (stream ingestion).
- **Bounded Data:** Data ingested in chunks (batch ingestion), either time-based or size-based.

<img src="/data-engineering-specialization-website/images/diagrams/ingestion-continuum-dark.svg" alt="Data Ingestion Continuum" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/ingestion-continuum.svg" alt="Data Ingestion Continuum" class="diagram diagram-light" />

## 1.1.2 Ways to Ingest Data

**Using Connectors:** JDBC/ODBC APIs that support time-based or size-based ingestion.

**Using Ingestion Tools:** Services like `AWS Glue` ETL automate regular data ingestion on a schedule.

**Using APIs:** Protocol-based ingestion that requires careful attention to ingestion limits per request, API call frequency, and the complexity of custom connection code tied to external documentation.

**Ingesting Data from Files:**

- **Manual File Download**
- **Secure File Transfer:** SFTP (Secure File Transfer Protocol) or SCP (Secure Copy Protocol)

**Ingesting Data from Streaming Systems:**
Via **Message Queues** or **Streaming Platforms**.

<img src="/data-engineering-specialization-website/images/diagrams/ways-to-ingest-dark.svg" alt="Ways to Ingest Data" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/ways-to-ingest.svg" alt="Ways to Ingest Data" class="diagram diagram-light" />

**Popular AWS Data Ingestion Tools**

`AWS Glue` ETL ingests, transforms, and loads data from AWS sources (`RDS`, `S3`, `Redshift`). It uses `Apache Spark` for distributed processing and is serverless with automated scaling.

`Amazon EMR` is a managed cluster platform for big data processing (`Hadoop`, `Spark`). It supports large-scale transformations and ingestion and is available in serverless and provisioned modes.

**`AWS Glue` ETL vs. `Amazon EMR`**

| Feature | `AWS Glue` ETL | `Amazon EMR` |
| --- | --- | --- |
| **Ease of Use** | Serverless, minimal setup | Requires configuration |
| **Scaling** | Automated scaling | Custom resource allocation |

`AWS DMS` (Data Migration Service) moves data between databases without transformation, supports migrations between different database engines, and is available in serverless and provisioned modes.

**Other AWS Ingestion Services**

- **AWS Snow Family:** Physical transfer appliances (Snowball, Snowcone) for large-scale migration.
- **AWS Transfer Family:** Secure file transfers to/from `Amazon S3` using SFTP, FTP.

**Third-Party Ingestion Tools:** `Airbyte`, `Matillion`, `Fivetran` -- cloud-based ETL tools.

<img src="/data-engineering-specialization-website/images/diagrams/aws-ingestion-tools-dark.png" alt="AWS Data Ingestion Tools" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/aws-ingestion-tools.png" alt="AWS Data Ingestion Tools" class="diagram diagram-light" />

**Streaming Ingestion Tools**

- `Amazon Kinesis` Data Streams
- Amazon Managed Streaming for `Apache Kafka` (MSK)

Both enable real-time data ingestion, processing, and analytics.

## 1.1.3 Key Considerations: Batch vs. Streaming Ingestion

Choosing between batch and streaming ingestion comes down to business value versus operational complexity.

- **Use Case:** Real-time ingestion is only worthwhile if it provides tangible business value.
- **Machine Learning:** Batch for model training; streaming for real-time predictions.
- **Dashboards & Reporting:** Decide between real-time and batch updates based on stakeholder needs.
- **Latency:** Consider millisecond updates vs. micro-batching.
- **Cost:** Streaming is more complex and expensive.
- **System Readiness:** Both source and destination systems must handle real-time data.
- **Reliability & Availability:** Streaming requires high availability.

**Recommendation:** Use real-time streaming only if the business case justifies the trade-offs.

<img src="/data-engineering-specialization-website/images/diagrams/batch-vs-streaming-dark.svg" alt="Batch vs Streaming Ingestion" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/batch-vs-streaming.svg" alt="Batch vs Streaming Ingestion" class="diagram diagram-light" />
