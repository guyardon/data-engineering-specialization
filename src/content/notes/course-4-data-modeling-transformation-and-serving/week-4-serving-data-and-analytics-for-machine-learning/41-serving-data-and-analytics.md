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

## 4.1.1 Serving Data for Analytics and ML

**Overview**

The final stage of the data engineering lifecycle is serving -- delivering processed data to downstream consumers for analytics and machine learning.


---

**Serving Data - Analytical Use Cases**

- **Business Intelligence** -- Dashboards and reports for strategic decision-making
- **Operational Analytics** -- Monitoring data to inform immediate action, served within required latency constraints
- **Embedded Analytics** -- Client-facing data products or dashboards


---

**Serving Data - Machine Learning Use Cases**

The primary end users are data scientists and ML engineers. The data engineer's role is to acquire, transform, and deliver the data necessary for model training.

A **semantic layer** documents definitions, derives business metrics, and creates a common language for data across the organization.


---

**Ways to serve data:**
- Table
- View
- Materialized View


---

**Ways data scientists accept data for model training:**
- **As files** (for ad hoc requests) -- text files for language modeling, table formats for tabular ML, image formats for computer vision
- **From databases and data warehouses** -- Access via queries, with the benefits of schema enforcement, fine-grained permissions, and high query performance
- **From streaming systems** -- Serve data in real time, enabling low-latency analytical queries across both historical and current data. This effectively combines the features of an OLAP database with a stream-processing system (e.g., operational analytics databases).

**Data management** ensures correctness, consistency, and trustworthiness through clear data definitions (column names) and data logic (formulas for deriving metrics).

Semantic Layer

![](/data-engineering-specialization-website/images/14fcf985-2d48-4f6d-b059-a967ec9a1582.png)

## 4.1.2 Views and Materialized Views

**Views and Materialized Views**

![](/data-engineering-specialization-website/images/8b0a9e7c-d067-49a7-b021-ec6b9c249ed9.png)

![](/data-engineering-specialization-website/images/3997d388-aea3-43e2-a8d8-def28cb8f87d.png)

![](/data-engineering-specialization-website/images/5de4deef-865e-44cd-af94-448451a72b74.png)
