---
title: "2.3 Practical Examples on AWS"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 2: The Data Engineering Lifecycle & Undercurrents"
weekSlug: "week-2-the-data-engineering-lifecycle-undercurrents"
weekOrder: 3
order: 3
notionId: "146969a7-aa01-8018-8e73-f2b8bce0869a"
---

## 2.3.1 The Data Engineering Lifecycle on AWS

Each stage of the data engineering lifecycle maps to concrete AWS services. Here is how they break down.

<img src="/data-engineering-specialization/images/diagrams/aws-lifecycle-pipeline-tech-dark.png" alt="Data Engineering Lifecycle on AWS" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/aws-lifecycle-pipeline-tech.png" alt="Data Engineering Lifecycle on AWS" class="diagram diagram-light" />

**Source Systems**

- **Databases:** `Amazon RDS` — managed relational databases, reducing operational overhead. `Amazon DynamoDB` — serverless NoSQL with flexible schemas, best for low-latency access to large volumes of data.
- **Streaming Sources:** `Amazon Kinesis Data Streams`, `Amazon SQS`, `Amazon MSK`

**Ingestion**

- From a database: `AWS Database Migration Service (DMS)`, `AWS Glue`
- From a streaming source: `Amazon Kinesis Data Streams`, `Amazon Data Firehose`, `Amazon SQS`, `Amazon MSK`

**Storage**

- `Amazon Redshift` — traditional cloud data warehouse
- `Amazon S3` — object storage, also the foundation for a lakehouse arrangement that can handle both structured and unstructured data

**Transformation**

- `AWS Glue`, `Apache Spark`, `dbt`

**Serving**

- **Analytics and BI:** Querying with `Amazon Athena` and `Amazon Redshift`. Dashboarding with `Amazon QuickSight`, `Apache Superset`, or `Metabase`.
- **AI/ML:** Serve batch data for model training and work with vector databases

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/kinesis.svg" alt="Amazon Kinesis" class="logo-light" /><img src="/data-engineering-specialization/images/logos/kinesis-dark.svg" alt="Amazon Kinesis" class="logo-dark" />
    <span>Amazon Kinesis</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/glue.svg" alt="AWS Glue" class="logo-light" /><img src="/data-engineering-specialization/images/logos/glue-dark.svg" alt="AWS Glue" class="logo-dark" />
    <span>AWS Glue</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/redshift.svg" alt="Amazon Redshift" class="logo-light" /><img src="/data-engineering-specialization/images/logos/redshift-dark.svg" alt="Amazon Redshift" class="logo-dark" />
    <span>Amazon Redshift</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/s3.svg" alt="Amazon S3" class="logo-light" /><img src="/data-engineering-specialization/images/logos/s3-dark.svg" alt="Amazon S3" class="logo-dark" />
    <span>Amazon S3</span>
  </div>
</div>

## 2.3.2 The Undercurrents in AWS

The undercurrents also have direct AWS counterparts.

<img src="/data-engineering-specialization/images/diagrams/aws-undercurrents-tech-dark.png" alt="AWS Undercurrents" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/aws-undercurrents-tech.png" alt="AWS Undercurrents" class="diagram diagram-light" />

**Security** — AWS uses a shared responsibility model. `IAM` (Identity and Access Management) enforces permissions based on roles.

**Data Management** — `AWS Glue`, `Glue Crawler`, and `Glue Data Catalog` discover, create, and manage metadata for data stored across AWS storage systems.

**DataOps** — `Amazon CloudWatch` collects metrics and provides monitoring for cloud resources, applications, and on-prem systems. `Amazon SNS` (Simple Notification Service) handles alerting.

**Orchestration** — `Apache Airflow` remains the industry standard, available as a managed service through `Amazon MWAA`.

**Architecture** — The AWS Well-Architected Framework provides the guiding principles.

**Software Engineering** — AWS Cloud9 IDE (hosted on `EC2`) for development, `AWS CodeDeploy` for automated deployments, and `Git`/`GitHub` for source code management.
