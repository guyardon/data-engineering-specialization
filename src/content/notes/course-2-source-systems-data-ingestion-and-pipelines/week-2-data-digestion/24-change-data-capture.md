---
title: "2.4 Change Data Capture"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 4
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---


## 2.4.1 CDC Fundamentals

**Change Data Capture (CDC)**


**Definition**

Change data capture (CDC) is a method for extracting each change event (insert, update, delete) that occurs in a database and making it more available for downstream systems


**Ways to ensure Storage Systems are In-Sync with Data in Source System**

- Full Snapshots/ Full load
- Update all the data in the storage systems
- In case of tabular data - deleting all the old data and extracting all the rows from a source table
- Ensures consistency, but for high volume data can be processing and memory heavy
- Suitable for applications where there's no need for frequent data updates
- Incremental (differential) load
- only load updates and changes since the last read from the source system
- e.g. utilize a "last_updated_at" column and update based on these columns. may require more complex logic.
- When working with databases, this processes is called "Change Data Capture" (CDC).

**Use Cases for CDC**

- Synchronize data across different databases
- e.g. PostgreSQL system that supports an app. Periodically we want to update our storage system (data warehouse) based on the table changes to support analytics.
- e.g. CDC to capture changes in on-premises databases and apply those changes to on-cloud databases
- Capture historical changes for auditing or other business purposes (e.g. regulations, insights, etc)
- Enable microservices to track any changes in the source database (e.g. CDC captures changes from purchance service, and relays information to shipment service and customer service).


## 2.4.2 CDC Approaches and Implementation

**Approaches to CDC**

- **Push**
- Logic that captures changes in source database → changes are pushed to target system. 
- Target systems are updated with latest data in near-real-time.
- **Pull**
- The target system continuously polls the source database to check for changes and then pulls updates when changes occur.
- If changes are batched before pull requests, this can cause a lag in the target system.


**CDC Implementation Patterns**

- **Batch-oriented or query-based CDC (pull-based)**
- Query the database to check for changes (based on a "last_modified" column. 
- Get changed rows and update target table
- Can be slow since we have to scan rows.
- **Continuous/Log-based CDC (pull-based)**
- Each change in the database is logged (every create, update, read) in case of failure to restore database state.
- We can check the log records (by writing custom code or using a tool such as Debezium)
- Send changes to a streaming platform, such as Apache Kafka. 
- Advantages: capture changes in real-time, no computational overhead, no need for extra column in source database.
- **Trigger-based CDC (push-based)**
- A trigger is a stored function that you can configure to run when a specific column changes. 
- The triggers informs (pushes to) the CDC of the changes in the source databases.
- Disadvantage: too many triggers can impact the write performance of the source database.

**CDC Tools:**

- Debezium
- AWS DMS
- Kafka Connect API
- Airbyte log-based CDC.
---


## 2.4.3 General Considerations for Choosing Ingestion Tools

**Summary: General Consideration for Choosing Ingestion Tools**


**Characteristics of the Data**

- **Data Type and Structure**
- Structured/ unstructured/ semi structured
- **Data Volume**
- Data size in bytes that you need to ingest
- If data is needed to be transferred over the network that has a limited bandwidth, you may ned to reduce the payload into smaller sections
- In case of streaming ingestion, you need a tool that can handle the maximum expected message size. E.g. Kinesis data stream supports a message size of 1 MB. Kafka defaults to 1 MB but can be configured to support 20 MB or more.
- Is the amount of data you ingest expected to grow over time?
- **Latency Requirements**
- How fast/often do we need to operate on the data?
- What is the use case?
- **Data Quality**
- Does the data need post-processing before downstream use?
- What post processing is required to serve the data?
- **Changes in Schema**
- If schema changes are expected (new columns, changing types, renaming columns) use tools that automatically detect schema changes.
- Ensure good communication between you and the upstream stakeholder.

**Reliability and Durability**

Reliability

- ingestion systems are preforming their intended function properly
Durability

- Data isn't lost or corrupted.
Evaluate the tradeoffs between the cost of losing data vs building an appropriate level of redundancy.
