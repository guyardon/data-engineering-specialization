---
title: "4.2 AWS Services for Batch Pipelines"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 4: Translating Requirements to Architecture"
weekSlug: "week-4-translating-requirements-to-architecture"
weekOrder: 5
order: 2
notionId: "18d969a7-aa01-808e-8260-ce7edc5dc3a7"
---

## 4.2.1 AWS Services for Batch Pipelines

A typical batch ETL pipeline starts with a source system (e.g., `Amazon RDS`) and needs an extraction and transformation layer. Running this on a raw `EC2` instance works but means managing software installation, security, and all the complexity of a cloud server yourself.

`AWS Lambda` offers a serverless alternative — you write a function to extract data from the source system with no infrastructure to manage. However, Lambda has a 15-minute timeout per invocation and limited memory and CPU, so it is best suited for lightweight tasks.

---

**Serverless Tools for Batch Processing:**

- `Amazon EMR` — more control, designed as a big data processing tool
- `AWS Glue ETL` — more convenience; `Glue Crawler` automatically discovers and classifies data, `Glue Data Catalog` serves as a central metadata repository, and Glue Visual ETL lets you design pipelines graphically. A good starting point for most teams.

---

**Load/Serve:**

Where you land the processed data depends on the use case:

- `Amazon RDS` — if normalizing tabular data using a star schema
- `Amazon Redshift` — if running complex analytical queries on massive datasets
- `Amazon S3` — for ML model artifacts or any workload that benefits from flexible, scalable, cost-effective object storage

<img src="/data-engineering-specialization-website/images/diagrams/batch-pipeline-aws-dark.png" alt="AWS Batch ETL Pipeline" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/batch-pipeline-aws.png" alt="AWS Batch ETL Pipeline" class="diagram diagram-light" />
