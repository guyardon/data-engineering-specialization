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

## Data Lakehouse Architecture on AWS

**AWS Lake Formation**

- Built on top of AWS glue (etl jobs, crawlers) and AWS IAM to build a data lake/lakehouse without multiple manual steps
![](/data-engineering-specialization-website/images/6a6c35fa-7693-43ce-af68-3b083eb56dbc.png)

![](/data-engineering-specialization-website/images/228e538e-d214-49a2-a2ac-cf01a725eadc.png)

**AWS Data Lakehouse**

![](/data-engineering-specialization-website/images/e759ff45-23f9-4b98-a29c-dc435d55597a.png)

**Implementing a Data Lakehouse on AWS**

- **Storage Layer**
- For Data Lake - common to use Amazon S3
- For Data Lakehouse - common to use both S3 and Redshift
  - S3 for structured, semi structured and unstructured data
  - Redshift - highly curated structured and semi structured data with a predefined schema
- **Catalog Layer**
- Provides metadata about all data in the lakehouse
- Uses AWS Lake Formation to create data catalog using glue crawlers
  - Schema information
  - Partition information
  - Data location
- AWS Glue can periodically crawl through the storage layer to update the metadata in case of changing partitions, schemas or data locations.
- Schema and data versioning using Apache Iceberg
- **Consumption Layer**
- Amazon Redshift Spectrum
  - Allows running unified SQL queries on structured data stored in S3 without having to move it to Redshift
  - Eliminates need for complex ETL pipelines
  - Queries data in place (without moving it) - reduces latency, and uses MPP to do processing in the Redshift Spectrum layer
  - Keep large volumes of historical data, and new hot data
- Amazon Athena
  - Makes it possible to query data in S3 using standard SQL
  - No need to load the data into another system
  - Serverless (no need to set up infrastructure or manage)
  - Pay-on-demand
  - Federated queries (query data outside of S3, including Amazon Redshift)
  - Uses the schema stored in Lake Formation Catalog
