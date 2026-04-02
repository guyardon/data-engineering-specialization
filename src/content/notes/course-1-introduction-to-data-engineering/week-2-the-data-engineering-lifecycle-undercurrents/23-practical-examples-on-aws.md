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

**Source Systems**

- **Databases:**
  - `Amazon RDS` — create managed instances of your preferred relational database, reducing operational overhead
  - `Amazon DynamoDB` — a serverless NoSQL option with flexible schemas, best suited for low-latency access to large volumes of data
- **Streaming Sources:**
  - `Amazon Kinesis Data Streams`
  - `Amazon Simple Queue Service (SQS)`
  - `Amazon Managed Streaming for Apache Kafka (MSK)`

---

**Ingestion**

- From a database: `AWS Database Migration Service (DMS)`, `AWS Glue`
- From a streaming source: `Amazon Kinesis Data Streams`, `Amazon Data Firehose`, `Amazon SQS`, `Amazon MSK`

---

**Storage**

- `Amazon Redshift` — traditional cloud data warehouse
- `Amazon S3` — object storage, also the foundation for a lakehouse arrangement that can handle both structured and unstructured data

---

**Transformation**

- `AWS Glue`, `Apache Spark`, `dbt`

---

**Serving**

- **Analytics and BI:**
  - Querying: `Amazon Athena`, `Amazon Redshift`
  - Dashboarding: `Amazon QuickSight`, `Apache Superset`, `Metabase`
- **AI/ML:** Serve batch data for model training and work with vector databases

## 2.3.2 The Undercurrents in AWS

The undercurrents also have direct AWS counterparts.

**Security** — AWS uses a shared responsibility model. `IAM` (Identity and Access Management) enforces permissions based on roles.

---

**Data Management** — `AWS Glue`, `Glue Crawler`, and `Glue Data Catalog` discover, create, and manage metadata for data stored across AWS storage systems.

---

**DataOps** — `Amazon CloudWatch` collects metrics and provides monitoring for cloud resources, applications, and on-prem systems. `Amazon SNS` (Simple Notification Service) handles alerting.

---

**Orchestration** — `Apache Airflow` remains the industry standard, available as a managed service through `Amazon MWAA`.

---

**Architecture** — The AWS Well-Architected Framework provides the guiding principles.

---

**Software Engineering** — AWS Cloud9 IDE (hosted on `EC2`) for development, `AWS CodeDeploy` for automated deployments, and `Git`/`GitHub` for source code management.
