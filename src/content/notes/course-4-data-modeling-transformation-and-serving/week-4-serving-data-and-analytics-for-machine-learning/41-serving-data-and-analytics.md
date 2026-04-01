---
title: "4.1 Serving Data and Analytics"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 4: Serving Data and Analytics for Machine Learning"
weekSlug: "week-4-serving-data-and-analytics-for-machine-learning"
weekOrder: 4
order: 1
notionId: "20a969a7-aa01-800d-8146-c81f183ff15e"
---

## Overview

**Serving Data - Analytical Use Cases**

- Business Intelligence
- Dashboards and reports
- Operational Analytics
  - Monitor data to inform immediate action
  - Serve data within the required latency
- Embedded Analytics
- Client facing data product or dashboard

**Serving Data - Machine Learning Use Cases**

- End Users:
- Data Scientist/ ML Engineer
- Aquire, transform and deliver the data necessary for model training
- Semantic Layer:
- Document definitions
- Derive business metrics
- Create a common language for data
- Ways to serve data:
- Table
- View
- Materialized View
- Ways data scientists accept data for model training:
- As files (for ad hoc requests)
  - txt files: language modeling
  - table formats: tabular ml
  - image formats: computer vision
- From databases and data warehouses
  - accessing data via querying
  - benefits: imposes order and structure through schema
  - gives fine-grained permissions and controls
  - High performance for queries
- From streaming systems
- service data in real time
- enables low latency analytical queries across historical and current data
  - e.g. operational analytics database
- effectively combining the features of an OLAP database with a stream-processing system
- Data management
- ensures data correctness, consistency and trustworthiness
- Data definition: definition of column names
- Data logic: formulas fro deriving metrics from the data

Semantic Layer

![](/data-engineering-specialization-website/images/14fcf985-2d48-4f6d-b059-a967ec9a1582.png)

## Views and Materialized Views

![](/data-engineering-specialization-website/images/8b0a9e7c-d067-49a7-b021-ec6b9c249ed9.png)

![](/data-engineering-specialization-website/images/3997d388-aea3-43e2-a8d8-def28cb8f87d.png)

![](/data-engineering-specialization-website/images/5de4deef-865e-44cd-af94-448451a72b74.png)
