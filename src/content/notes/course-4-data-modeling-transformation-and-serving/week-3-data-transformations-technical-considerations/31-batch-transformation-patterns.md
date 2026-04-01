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


**Overview**


**Transformation Stage**

- Manipulate and enhance data for downstream stakeholders
- Leverage massively parallel processing for data modeling (e.g. star schemas, data vaults, etc)
- Define Zones for stages of transformed data (e.g. raw, cleaned, enriched)

**Technical Considerations**

**Batch Transformations**

- Size of the data
- Hardware specification
- Performance requirements

**Streaming Transformations**

- Latency requirements

**Traditional Approaches**

- Single machine or use a distributed processing tool
- Writing transformation logic in SQL or python


**Week Overview**

**Batch Transformations**

- Transformation use cases
- Distributed Processing frameworks
- **Hadoop MapReduce**: disk-based storage and processing
  - Considered legacy technology due to
    - complexity
    - high cost of scaling
    - significant maintenance requirements
  - important to know since it influences many of today's technologies
- **Spark**: memory based processing framework
- Compare SQL based transformations with python-based transformations
- Lab: Transforming data with Apache Spark
- AWS expert: Generating Glue processing jobs with Glue Studio

**Streaming Transformations**

- Transformation use cases
- Micro-batch vs true streaming processing tools
- Lab: Implement a CDC pipeline using Apache Kafka and Apache Flink

## 3.1.2 ETL Patterns and Use Cases

**Batch Transformation Patterns and Use Cases**


**ETL vs. ELT vs. EtLT**

![](/data-engineering-specialization-website/images/533b35b2-1d38-4f8d-80ba-741e6b1c2577.png)

- The third approach (EtLT, means simple transformations before loading to the data warehouse (like cleaning) and then applying transformations (like modeling the data into star schema) inside the data warehouse


**Transformations for Data Modeling**

![](/data-engineering-specialization-website/images/1fd6d4b5-06ed-4cf9-90bc-e191041c6bbb.png)


**Transformations for Data Cleaning (Data Wrangling)**

![](/data-engineering-specialization-website/images/bd34135f-782a-4ee5-ab5c-b5c8b2929500.png)


## 3.1.3 Data Updating and Change Data Capture

**Transformations for Data Updating **

Usecase: making sure the data in the data warehouse is in sync with the data from the source system

**2 Approaches: Truncate and reload data vs CDC**

**Truncate and reload data**

- Delete all records in the target system and reload the updated data from the source
- Ok for small datasets, or only update once in a while, but can be very expensive for large datasets

**Change Data Capture (CDC)**

- Identify the changes in the source system, and update only these changes in the target system.
- `last_updated` column
- database transactional logs `I`: row is inserted, `U`: row is updated,`D`: row is deleted
- Capture updates:
- insert-only pattern
  -  insert new records without changing or deleting old records
  - when adding additional information, the new record to distinguish it from the old one
- upsert/merge pattern
  - take a set of source records and look for matches against your target table by using a primary key or another logical condition.
  - When a match occurs, you update the target record by replacing it with a new record.
  - When no match exists, you insert the new record.
- Capture deletes
- With a hard delete, you permanently remove a record from your target system
  - performance reasons (e.g. storage/memory space)
  - legal/compliance reasons
- with a soft delete, you mark the record as deleted.
  - Can be filtered later
- Insert only with a deleted flag

**Insert Types**

Single Row inserts

- good for row-oriented OLTP databases
- bad for column-oriented OLAP databases
- Puts a massive load on the OLAP system
- Extremely inefficient for subsequent reads
**Micro-batch or batch inserts**
