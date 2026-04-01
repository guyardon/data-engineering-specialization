---
title: "4.3 AWS Services for Batch Pipelines"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 4: Translating Requirements to Architecture"
weekSlug: "week-4-translating-requirements-to-architecture"
weekOrder: 5
order: 2
notionId: "18d969a7-aa01-808e-8260-ce7edc5dc3a7"
---

ETL Pipeline for batch data

- Source system: e.g Amazon RDS
- Extract/ Transform: e.g. EC2 Instance
The problem with this approach is that you would need to set up installing software, managing security, and all the complexities of managing a server on the cloud

Serverless solution: AWS Lambda

- Lambda function - extract data from source system
- Limitations: 15 minute timeout for each function call, limitations on memory on CPI
- Requires you to write custom code for your use case

Serverless Tools for Batch Processing:

- Amazon EMR
- More control
- Designed as a big data tool
- AWS Glue ETL
- More convenience
- AWS Glue crawler automatically discovers and classifies data and creates metadata
- AWS Glue Data catalog is a central repository with info about all your data assets
- Glue visual ETL to design your pipeline
- Good to start with this

Load/Serve:

- If normalizing tabular data using a star schema - we can store it in another RDS instance
- If we need to perform complex analytical queries on massive datasets - Amazon Redshift
- ML Model can be stored on an S3 instance
- Flexible
- Scalable
- Cost-effecive

