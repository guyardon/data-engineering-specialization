---
title: "3.1 Batch Transformation Patterns"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 3: Data Transformations & Technical Considerations"
weekSlug: "week-3-data-transformations-technical-considerations"
weekOrder: 3
order: 1
notionId: "1fc969a7-aa01-805e-8f9a-f648e027b479"
---


## 3.1.1 Batch Transformation Overview

**Batch Transformations**

The transformation stage is where raw data is manipulated and enhanced for downstream stakeholders. This section covers the technical considerations for batch transformations.

**Transformation Stage**

Transformations serve three purposes: manipulate and enhance data for downstream consumers, leverage massively parallel processing for data modeling (star schemas, data vaults, etc.), and define zones for stages of transformed data (raw, cleaned, enriched).

**Technical Considerations**

For **batch transformations**, the key factors are data size, hardware specifications, and performance requirements. For **streaming transformations**, latency requirements dominate. The traditional approach is to run transformations on a single machine or use a distributed processing tool, writing logic in SQL or Python.

**Week Overview**

**Batch Transformations**
- Transformation use cases
- Distributed processing frameworks:
  - **Hadoop MapReduce**: disk-based storage and processing. Considered legacy due to complexity, high scaling costs, and significant maintenance -- but important to understand since it influenced many modern technologies.
  - **Spark**: memory-based processing framework
- Comparison of SQL-based vs. Python-based transformations
- Lab: Transforming data with Apache Spark
- AWS expert: Generating Glue processing jobs with Glue Studio

**Streaming Transformations**
- Transformation use cases
- Micro-batch vs. true streaming processing tools
- Lab: Implement a CDC pipeline using Apache Kafka and Apache Flink

## 3.1.2 ETL Patterns and Use Cases

**Batch Transformation Patterns and Use Cases**


**ETL vs. ELT vs. EtLT**

![](/data-engineering-specialization-website/images/533b35b2-1d38-4f8d-80ba-741e6b1c2577.png)

The third approach, **EtLT**, applies simple transformations (like cleaning) before loading into the data warehouse, then performs heavier transformations (like modeling into star schemas) inside the warehouse.

**Transformations for Data Modeling**

![](/data-engineering-specialization-website/images/1fd6d4b5-06ed-4cf9-90bc-e191041c6bbb.png)


**Transformations for Data Cleaning (Data Wrangling)**

![](/data-engineering-specialization-website/images/bd34135f-782a-4ee5-ab5c-b5c8b2929500.png)


## 3.1.3 Data Updating and Change Data Capture

**Transformations for Data Updating**

A common use case is keeping the data warehouse in sync with source systems. There are two main approaches.

**Truncate and reload data**

Delete all records in the target system and reload from source. This works for small datasets or infrequent updates, but becomes very expensive at scale.

**Change Data Capture (CDC)**

CDC identifies changes in the source system and applies only those changes to the target. Changes can be detected through a `last_updated` column or database transaction logs (`I` for insert, `U` for update, `D` for delete).

**Capture updates:**
- **Insert-only pattern** -- Insert new records without modifying or deleting old ones. New records include additional information to distinguish them from previous versions.
- **Upsert/merge pattern** -- Match source records against the target table by primary key or another logical condition. On match, replace the target record; on no match, insert the new record.

**Capture deletes:**
- **Hard delete** -- Permanently remove a record from the target, typically for performance (storage/memory) or legal/compliance reasons.
- **Soft delete** -- Mark the record as deleted so it can be filtered later.
- **Insert-only with a deleted flag** -- Append a new record with a deletion marker.

**Insert Types**

**Single-row inserts** work well for row-oriented OLTP databases but are problematic for column-oriented OLAP systems -- they put massive load on the system and are extremely inefficient for subsequent reads.

**Micro-batch or batch inserts** are the preferred approach for OLAP systems.
