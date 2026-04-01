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

Source Systems on AWS:

- Databases:
- Amazon Relational Database Service (RDS)
  - Create database instances with relational database of your choice
  - Simplifies the operational overhead of hosting a relational database server
- Amazon DynamoDB
  - A serverless NoSQL database option
  - Create stand-alone tables that can be very large
  - Flexible schema
  - Best suited for applications that require low latency access to large volumes of data
- Streaming Sources
- Amazon Kinesis Data Streams
- Amazon Simple Queue Service (SQS)
- Amazon Managed Streaming for Apache Kafka (MSK)
Ingestion

- From a Database:
- AWS Database Migration Service (MGS)
- AWS Glue
- From a Streaming Source
- Amazon Kinesis Data Streams
- Amazon Data Firehouse
- Amazon SQS
- Amazon MSK
Storage

- Traditional Data Warehouse
- Amazon Redshift
- Amazon Simple Storage Service (S3)
- Lakehouse Arrangement (access structured and unstructured data in an object storage lake house)
Transformation

- Data Processing Tools:
- AWS Glue
- Apache Spark
- dbt
Serving

- Business Intelligence or Analytics
- For querying structure or unstructured data:
  - Amazon Athena
  - Amazon Redhisft
- For dashboarding tools:
  - Amazon QuickSight
  - Apache Superset
  - Metabase
- AI/ML
- Serve batch data for model training and work with vector databases

## 2.3.2 The Undercurrents in AWS

Security

- Shared responsibility model on AWS
- Identity and Access Management (IAM)
- Set permissions based on roles
Data Management

- Use AWS Glue, Glue Crawler, Glue Data Catalog
- Discover, create, and manage metadata for data stored in AWS storage systems
DataOps

- Amazon CloudWatch
- Collects metrics and provides monitoring features for cloud resources, applications and on-prem resources.
- Amazon Simple Notification Service (SNS)
Orchestration

- Apache Airflow (the industry standard)
Architecture

- AWS Well-Architected Framework
Software Engineering

- AWS Cloud9 IDE for development hosted on EC2
- AWS CodeDeploy to automate code deployment
- Git and GitHub for source code management.

