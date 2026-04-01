---
title: "2.4 AWS Data Lakehouse"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 2: Storage Abstractions"
weekSlug: "week-2-storage-abstractions"
weekOrder: 2
order: 4
notionId: "1e3969a7-aa01-80c6-8d1b-d10f852165d0"
---


## 2.4.1 AWS Lake Formation

**Data Lakehouse Architecture on AWS**

**AWS Lake Formation**

AWS Lake Formation simplifies building a data lake or lakehouse by wrapping **AWS Glue** (ETL jobs, crawlers) and **AWS IAM** into a managed service that eliminates many manual setup steps.

![](/data-engineering-specialization-website/images/6a6c35fa-7693-43ce-af68-3b083eb56dbc.png)

![](/data-engineering-specialization-website/images/228e538e-d214-49a2-a2ac-cf01a725eadc.png)

**AWS Data Lakehouse**

![](/data-engineering-specialization-website/images/e759ff45-23f9-4b98-a29c-dc435d55597a.png)

## 2.4.2 Implementing a Data Lakehouse on AWS

**Implementing a Data Lakehouse on AWS**

A typical AWS lakehouse implementation consists of three layers:

- **Storage Layer**
  - **Amazon S3** — stores structured, semi-structured, and unstructured data (the data lake portion)
  - **Amazon Redshift** — stores highly curated, structured and semi-structured data with a predefined schema (the warehouse portion)

- **Catalog Layer**
  - **AWS Lake Formation** creates a data catalog using Glue crawlers that capture schema information, partition details, and data locations. Glue can periodically re-crawl the storage layer to keep metadata current as schemas, partitions, or data locations change. **Apache Iceberg** adds schema and data versioning on top.

- **Consumption Layer**
  - **Amazon Redshift Spectrum** — runs unified SQL queries against structured data in S3 without moving it into Redshift. It eliminates complex ETL pipelines by querying data in place and uses MPP for processing. Ideal for keeping large volumes of historical data alongside hot data.
  - **Amazon Athena** — a serverless, pay-on-demand engine that queries data in S3 using standard SQL. No infrastructure to manage. Supports **federated queries** across data sources including Redshift, and reads schema information from the Lake Formation catalog.
