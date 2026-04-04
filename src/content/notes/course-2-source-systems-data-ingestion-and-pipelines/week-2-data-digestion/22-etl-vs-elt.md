---
title: "2.2 ETL vs. ELT and REST APIs"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 2
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

## 2.2.1 ETL vs. ELT

The order in which you extract, transform, and load data has significant implications for pipeline speed, flexibility, and data quality.

![](/data-engineering-specialization-website/images/b3d34b42-a540-4f17-ab01-e20c5386ee3e.png)

**ETL (Extract-Transform-Load)** extracts raw data from the source, transforms it in a staging area, then loads the transformed data into the target destination.

**ELT (Extract-Load-Transform)** loads raw data directly into a cloud data warehouse (e.g., `Redshift`, Snowflake), then transforms it within the warehouse. This allows flexible transformations to be applied later.

---


---

**Advantages of ELT**

- Faster implementation and data availability
- More flexibility in transformations
- Suitable for semi-structured/unstructured data (e.g., JSON, text, images)

---

**Downsides of ELT**

The main risk is creating an "EL pipeline" where no transformation ever happens, turning your data warehouse into a data swamp.

---

**Comparison of ETL vs. ELT**

| Feature | ETL | ELT |
| --- | --- | --- |
| **History** | Developed in the 80s/90s when storage was expensive | Gained popularity in the cloud era |
| **Transformation Timing** | Before loading | After loading |
| **Load Time** | Longer | Faster |
| **Flexibility** | Structured data only | Structured, semi-structured, and unstructured data |
| **Scalability** | Manual effort required for scaling | Uses cloud warehouse power for large-scale processing |
| **Data Quality** | Ensures data quality before loading | Requires transformations after loading |

## 2.2.2 REST API

APIs are a fundamental ingestion mechanism. Jeff Bezos famously enforced API-based communication within Amazon, a mandate that laid the foundation for AWS.

**What is an API?** A set of rules and specifications for programmatic communication between applications, typically including metadata, documentation, authentication, and error handling.

**REST API (Representational State Transfer)** is the most common API type, using HTTP as its communication protocol.

---


---

**HTTP Request Types**

| Method | Purpose |
| --- | --- |
| `GET` | Retrieve a resource |
| `POST` | Create a resource |
| `PUT` | Update/replace a resource |
| `DELETE` | Remove a resource |
